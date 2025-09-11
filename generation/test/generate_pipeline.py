# -*- coding: utf-8 -*-
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from PIL import Image
import os
import json
import traceback
from tqdm import tqdm
import torch
import yaml
import re  # for ${var} substitution
from util.repair_strategy import generate_and_repair
from util.save_and_complie import compile_and_save

# logging & env
import datetime
import platform
from pprint import pformat
from pathlib import Path

# ===== 可选：PEFT（LoRA） =====
try:
    from peft import PeftModel  # noqa: F401
    _HAS_PEFT = True
except Exception:
    _HAS_PEFT = False


# ---------------------------
# 工具：文件读取 / instruction 查找
# ---------------------------
def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def _stem_without_ext(path: str) -> str:
    return Path(path).stem


def _find_instruction_for_image(
    image_abs_path: str,
    instruction_dir: str,
    model_tag: str | None = None,
    ext: str = ".md",
) -> tuple[str | None, str]:
    """
    优先匹配 instruction/{model_tag}/{stem}.md；
    未命中则在 instruction/** 里递归找 {stem}.md。
    返回 (文件路径或 None, 文本内容或 "")。
    同时对文本做轻度清洗：去头部 1~3 行的标题/空行。
    """
    img_stem = _stem_without_ext(image_abs_path)
    root = Path(instruction_dir)

    candidates = []
    if model_tag:
        candidates.append(root / model_tag / f"{img_stem}{ext}")
    # 兜底递归
    candidates += list(root.rglob(f"{img_stem}{ext}"))

    seen = set()
    for c in candidates:
        try:
            rc = c.resolve()
        except Exception:
            continue
        if rc in seen:
            continue
        seen.add(rc)
        if rc.exists():
            text = _read_text(rc)
            if text.strip():
                # 轻量清洗：剔除前 3 行内的标题/空行
                lines = text.splitlines()
                cleaned, dropped = [], 0
                for ln in lines:
                    if dropped < 3 and (ln.strip().startswith("#") or ln.strip() == ""):
                        dropped += 1
                        continue
                    cleaned.append(ln)
                return str(rc), "\n".join(cleaned).strip()
    return None, ""


# ---------------------------
# 设备与运行概要
# ---------------------------
def _safe_gpu_info():
    try:
        if torch.cuda.is_available():
            idx = torch.cuda.current_device()
            return {
                "cuda_available": True,
                "device_count": torch.cuda.device_count(),
                "current_device": int(idx),
                "device_name": torch.cuda.get_device_name(idx),
                "capability": ".".join(map(str, torch.cuda.get_device_capability(idx))),
            }
        else:
            return {"cuda_available": False}
    except Exception as e:
        return {"cuda_available": False, "error": str(e)}


def _summarize_config(
    cfg: dict,
    parsed_dtype,
    model_device: str,
    lora_enabled: bool,
    override_outputs: dict | None = None
) -> dict:
    """组装一份可序列化的运行概要，便于打印和落盘"""
    model_cfg = cfg.get("model", {})
    data_cfg = cfg.get("data", {})
    gen_cfg = cfg.get("gen", {})
    run_cfg = cfg.get("run", {})

    # 使用本次真实输出目录（两阶段时为 outputs_instruct）
    outputs_cfg = override_outputs if override_outputs is not None else (
        cfg["outputs_lora"] if lora_enabled else cfg["outputs_base"]
    )

    env = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": getattr(torch, "__version__", "unknown"),
        "transformers": getattr(__import__("transformers"), "__version__", "unknown"),
        "peft": "installed" if globals().get("_HAS_PEFT", False) else "not_installed",
        "gpu": _safe_gpu_info(),
    }

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    info = {
        "timestamp": now,
        "base_model": model_cfg.get("model_path"),
        "device": model_device,
        "dtype_cfg": model_cfg.get("dtype", "auto"),
        "effective_dtype": str(parsed_dtype),
        "lora": {
            "enabled": bool(model_cfg.get("enable_lora", False)),
            "path": model_cfg.get("lora_path"),
            "merge": bool(model_cfg.get("lora_merge", False)),
        },
        "data": {
            "metadata_path": data_cfg.get("metadata_path"),
            "base_dir": data_cfg.get("base_dir"),
            "instruction_dir": data_cfg.get("instruction_dir"),
            "instruction_model_tag": data_cfg.get("instruction_model_tag"),
        },
        "generation": {
            "do_sample": gen_cfg.get("do_sample"),
            "temperature": gen_cfg.get("temperature"),
            "top_p": gen_cfg.get("top_p"),
            "max_new_tokens": gen_cfg.get("max_new_tokens"),
        },
        "run": {
            "max_attempts": run_cfg.get("max_attempts"),
            "limit": run_cfg.get("limit"),
        },
        "pipeline": cfg.get("pipeline", {}),
        "outputs": outputs_cfg,
        "env": env,
    }
    return info


def _print_and_save_summary(summary: dict, log_dir: str):
    """打印到控制台 + 保存到 log_dir"""
    banner = "=" * 80
    pretty = pformat(summary, width=100, compact=False)
    print(f"\n{banner}\n运行配置总览\n{banner}\n{pretty}\n{banner}\n")

    try:
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "run_config.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        with open(os.path.join(log_dir, "run_summary.txt"), "w", encoding="utf-8") as f:
            f.write(pretty + "\n")
    except Exception as e:
        print(f"[WARN] 保存运行概要失败：{e}")


def _parse_dtype(dtype_cfg):
    """
    支持在 yaml 里写：
      - "auto"
      - "bf16" / "bfloat16"
      - "fp16" / "float16"
      - "fp32" / "float32"
    也兼容直接是 torch.dtype
    """
    if isinstance(dtype_cfg, torch.dtype):
        return dtype_cfg
    if not isinstance(dtype_cfg, str):
        return "auto"

    s = dtype_cfg.strip().lower()
    if s == "auto":
        return "auto"
    if s in ("bf16", "bfloat16"):
        return torch.bfloat16
    if s in ("fp16", "float16", "half"):
        return torch.float16
    if s in ("fp32", "float32"):
        return torch.float32
    return "auto"


# ---------------------------
# YAML 变量替换
# ---------------------------
_VAR_PATTERN = re.compile(r"\$\{([A-Za-z0-9_]+)\}")


def _collect_vars(cfg: dict) -> dict:
    """
    从 YAML 的顶层收集可替换变量：
    - checkpoint -> 提供 checkpoint / ckpt 两个别名
    - 顶层所有标量（str/int/float/bool）加入变量表
    """
    vars_map = {}
    if "checkpoint" in cfg and isinstance(cfg["checkpoint"], (str, int, float)):
        v = str(cfg["checkpoint"])
        vars_map["checkpoint"] = v
        vars_map["ckpt"] = v

    for k, v in cfg.items():
        if isinstance(v, (str, int, float, bool)):
            vars_map.setdefault(k, str(v))
    return vars_map


def _subst_in_str(s: str, vars_map: dict) -> str:
    def repl(m):
        name = m.group(1)
        return vars_map.get(name, m.group(0))
    return _VAR_PATTERN.sub(repl, s)


def _subst_cfg(obj, vars_map: dict):
    """递归地对 dict/list/str 做 ${var} 替换。"""
    if isinstance(obj, dict):
        return {k: _subst_cfg(v, vars_map) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_subst_cfg(v, vars_map) for v in obj]
    elif isinstance(obj, str):
        return _subst_in_str(obj, vars_map)
    else:
        return obj


# ---------------------------
# 配置加载
# ---------------------------
def load_config(cfg_path: str = "config.yaml") -> dict:
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"未找到配置文件：{cfg_path}")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    vars_map = _collect_vars(cfg if isinstance(cfg, dict) else {})
    cfg = _subst_cfg(cfg, vars_map)

    # ---- model ----
    cfg.setdefault("model", {})
    cfg["model"].setdefault("device", "cuda")
    cfg["model"].setdefault("dtype", "auto")
    cfg["model"].setdefault("enable_lora", False)
    cfg["model"].setdefault("lora_path", None)
    cfg["model"].setdefault("lora_merge", False)

    # ---- pipeline ----
    cfg.setdefault("pipeline", {})
    cfg["pipeline"].setdefault("two_stage", False)
    cfg["pipeline"].setdefault("require_instruction", False)

    # ---- data ----
    cfg.setdefault("data", {})
    if "metadata_path" not in cfg["data"] or "base_dir" not in cfg["data"]:
        raise ValueError("config.yaml 中 data.metadata_path / data.base_dir 不能为空")
    cfg["data"].setdefault("instruction_dir", "instruction")
    cfg["data"].setdefault("instruction_model_tag", None)

    # 顶层 instruction_model_name -> data.instruction_model_tag（若未显式提供）
    if not cfg["data"].get("instruction_model_tag") and cfg.get("instruction_model_name"):
        cfg["data"]["instruction_model_tag"] = cfg["instruction_model_name"]

    # ---- gen ----
    cfg.setdefault("gen", {})
    cfg["gen"].setdefault("do_sample", True)
    cfg["gen"].setdefault("temperature", 0.9)
    cfg["gen"].setdefault("max_new_tokens", 4096)
    cfg["gen"].setdefault("top_p", 0.9)

    # ---- run ----
    cfg.setdefault("run", {})
    cfg["run"].setdefault("max_attempts", 3)
    cfg["run"].setdefault("limit", None)

    # ---- outputs（提供安全默认，避免 KeyError）----
    cfg.setdefault("outputs_lora", {})
    cfg["outputs_lora"].setdefault("json_dir", "output/lora/json")
    cfg["outputs_lora"].setdefault("tex_dir",  "output/lora/tex")
    cfg["outputs_lora"].setdefault("pdf_dir",  "output/lora/pdf")
    cfg["outputs_lora"].setdefault("png_dir",  "output/lora/png")
    cfg["outputs_lora"].setdefault("log_dir",  "output/lora/log")

    cfg.setdefault("outputs_base", {})
    cfg["outputs_base"].setdefault("json_dir", "output/base/json")
    cfg["outputs_base"].setdefault("tex_dir",  "output/base/tex")
    cfg["outputs_base"].setdefault("pdf_dir",  "output/base/pdf")
    cfg["outputs_base"].setdefault("png_dir",  "output/base/png")
    cfg["outputs_base"].setdefault("log_dir",  "output/base/log")

    cfg.setdefault("outputs_instruct", {})
    cfg["outputs_instruct"].setdefault("json_dir", "output/instruct/json")
    cfg["outputs_instruct"].setdefault("tex_dir",  "output/instruct/tex")
    cfg["outputs_instruct"].setdefault("pdf_dir",  "output/instruct/pdf")
    cfg["outputs_instruct"].setdefault("png_dir",  "output/instruct/png")
    cfg["outputs_instruct"].setdefault("log_dir",  "output/instruct/log")

    cfg.setdefault("output_log", {})
    cfg["output_log"].setdefault("log_dir", "log/")

    # 末尾再跑一次替换，保证上面默认值也能吃到 ${var}
    cfg = _subst_cfg(cfg, _collect_vars(cfg))
    return cfg


def ensure_dirs(*paths: str):
    for p in paths:
        os.makedirs(p, exist_ok=True)


# ---------------------------
# 主程序
# ---------------------------
def main(cfg_path: str = "config.yaml"):
    # 载入配置
    cfg = load_config(cfg_path)
    model_path = cfg["model"]["model_path"]
    device = cfg["model"]["device"]
    dtype_cfg = cfg["model"]["dtype"]
    lora_enabled = bool(cfg["model"]["enable_lora"])
    lora_path = cfg["model"]["lora_path"]
    lora_merge = bool(cfg["model"]["lora_merge"])

    metadata_path = cfg["data"]["metadata_path"]
    base_dir = cfg["data"]["base_dir"]

    # pipeline 开关
    two_stage = bool(cfg["pipeline"]["two_stage"])
    require_instruction = bool(cfg["pipeline"]["require_instruction"])

    # instruction 源
    instruction_dir = cfg["data"].get("instruction_dir", "instruction")
    instruction_model_tag = cfg["data"].get("instruction_model_tag", None)

    # 生成参数
    do_sample = cfg["gen"]["do_sample"]
    temperature = cfg["gen"]["temperature"]
    max_new_tokens = cfg["gen"]["max_new_tokens"]
    top_p = cfg["gen"]["top_p"]

    # 运行控制
    max_attempts = cfg["run"]["max_attempts"]
    limit = cfg["run"]["limit"]

    log_dir = cfg["output_log"]["log_dir"]

    # 选择输出组：两阶段优先，其次 LoRA，否则 base
    if two_stage:
        outputs_cfg = cfg["outputs_instruct"]
        print("输出目录使用：outputs_instruct（两阶段）")
    else:
        outputs_cfg = cfg["outputs_lora"] if lora_enabled else cfg["outputs_base"]
        print(f"输出目录使用：{'outputs_lora' if lora_enabled else 'outputs_base'}")

    out_json = outputs_cfg["json_dir"]
    out_tex  = outputs_cfg["tex_dir"]
    out_pdf  = outputs_cfg["pdf_dir"]
    out_png  = outputs_cfg["png_dir"]
    out_log  = outputs_cfg["log_dir"]

    # —— 先打印一次基于配置的概览（输出目录用本次真实 outputs_cfg）——
    prelim_summary = _summarize_config(cfg, _parse_dtype(dtype_cfg), str(device), lora_enabled, override_outputs=outputs_cfg)
    _print_and_save_summary(prelim_summary, log_dir)

    # 1) 加载模型与处理器
    try:
        print("正在加载模型和处理器...")
        parsed_dtype = _parse_dtype(dtype_cfg)
        torch_dtype = parsed_dtype  # "auto" 或 torch.dtype

        load_kwargs = dict(torch_dtype=torch_dtype, trust_remote_code=True)

        if isinstance(device, str) and device.lower() == "auto":
            try:
                import accelerate  # noqa: F401
            except ImportError:
                raise RuntimeError(
                    "device: auto 需要 accelerate，请先 `pip install -U accelerate`，"
                    "或把 YAML 的 device 改为 'cuda'/'cuda:0' 使用单卡。"
                )
            load_kwargs["device_map"] = "auto"
            model = Qwen2_5_VLForConditionalGeneration.from_pretrained(model_path, **load_kwargs)
            # 多卡时不要再 .to("cuda")
        else:
            model = Qwen2_5_VLForConditionalGeneration.from_pretrained(model_path, **load_kwargs)
            if isinstance(device, str):
                model = model.to(device)

        processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)

        # 打印设备信息
        real_device = getattr(model, "device", None)
        if hasattr(model, "hf_device_map"):
            used = sorted({
                int(str(v).split(":")[-1])
                for v in model.hf_device_map.values()
                if isinstance(v, str) and v.startswith("cuda")
            })
            print(f"[Info] 多卡切分已启用，使用的逻辑 GPU：{used}，device_map 条目数：{len(model.hf_device_map)}")

        print(
            f"模型加载成功，设备：{real_device if real_device is not None else 'multi-GPU'}，"
            f"LoRA：{'启用' if lora_enabled else '未启用'}，合并：{lora_merge if lora_enabled else 'N/A'}"
        )

        # 最终概要
        final_dev_str = "multi-GPU (device_map=auto)" if hasattr(model, "hf_device_map") else str(real_device)
        final_summary = _summarize_config(cfg, torch_dtype, final_dev_str, lora_enabled, override_outputs=outputs_cfg)
        _print_and_save_summary(final_summary, log_dir)

    except Exception as e:
        print(f"模型加载失败：{e}")
        traceback.print_exc()
        return

    # 2) 读取数据集（并在两阶段时附带 instruction）
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"读取metadata失败：{e}")
        return

    ds = []
    for item in metadata:
        img_abs_path = os.path.join(base_dir, item["image_path"])
        if not os.path.exists(img_abs_path):
            print(f"Warning: 图片不存在 {img_abs_path}，已跳过")
            continue
        try:
            image = Image.open(img_abs_path).convert("RGB")

            ins_path, ins_text = (None, "")
            if two_stage:  # 仅两阶段时查找 instruction，避免多余 IO
                ins_path, ins_text = _find_instruction_for_image(
                    image_abs_path=img_abs_path,
                    instruction_dir=instruction_dir,
                    model_tag=instruction_model_tag,
                    ext=".md"
                )
                if require_instruction and not ins_text:
                    print(f"[Skip] require_instruction=True 且未找到 instruction：{img_abs_path}")
                    continue

            ds.append({
                "image": image,
                "caption": item.get("caption", ""),
                "code": item.get("code", ""),
                "instruction_text": ins_text,     # 可能为空
                "instruction_path": ins_path,     # 可能为 None
                "image_abs_path": img_abs_path,
            })
        except Exception as e:
            print(f"Error: 读取图片 {img_abs_path} 失败: {e}，已跳过")
            continue

    print(f"数据集装载完成：有效样本数 = {len(ds)}（来自 {metadata_path}）")
    num_to_process = len(ds) if limit is None else min(len(ds), int(limit))
    print(f"处理样本数量 = {num_to_process}（limit = {limit}）")
    if len(ds) == 0:
        print("无有效样本，程序退出")
        return

    # 3) 输出目录
    ensure_dirs(out_tex, out_json, out_pdf, out_png, out_log)

    # 4) 主循环
    skip_list = []
    try:
        iterable = ds if limit in (None, 0) else ds[:int(limit)]
        for i, example in enumerate(tqdm(iterable, desc="Processing samples")):
            print("\n" + "-" * 60)
            print(f"[Sample {i}]")

            instruction_text = (example.get("instruction_text") or "").strip()
            caption = (example.get("caption") or "").strip()

            if two_stage and instruction_text:
                prompt = (
                    "你将看到一段用于“图像到 LaTeX 复刻”的指导说明。\n"
                    "请严格依照说明生成**可直接编译**的 LaTeX 源码（推荐 standalone + TikZ/PGFPlots）。\n"
                    "仅输出 LaTeX 源码，无需解释；若有不确定参数请给出合理近似并保持结构一致。\n\n"
                    f"{instruction_text}\n"
                )
            else:
                prompt = (
                    "根据这张图的排版风格与结构，生成可直接编译的 LaTeX（standalone + TikZ/PGFPlots）。"
                    "仅输出代码，无需解释。若有不确定参数请做合理近似。\n\n"
                    f"提示信息：{caption}"
                )

            brief = (prompt[:160] + "...") if len(prompt) > 160 else prompt
            print(f"Prompt(brief): {brief}")
            print(f"GenParams: do_sample={do_sample} | max_new_tokens={max_new_tokens} | temperature={temperature} | top_p={top_p}")

            image = example["image"]

            final_doc, all_attempts = generate_and_repair(
                model=model,
                processor=processor,
                image=image,
                prompt=prompt,
                max_attempts=max_attempts,
                return_all=True,
                do_sample=do_sample,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p
            )

            if final_doc is not None:
                compiled = getattr(final_doc, "has_content", False)
                print(f"[Sample {i}] attempts={len(all_attempts)} | compiled={compiled} | json -> {os.path.join(out_json, f'sample_img_{i}.json')}")
            else:
                print(f"[Sample {i}] attempts={len(all_attempts)} | compiled=False | result=None")

            device_str_for_json = "multi-GPU (device_map=auto)" if hasattr(model, "hf_device_map") else str(getattr(model, "device", device))

            result = {
                "prompt": prompt,
                "final_latex_code": getattr(final_doc, "code", "") if final_doc is not None else "",
                "compiled_successfully": getattr(final_doc, "has_content", False) if final_doc is not None else False,
                "ground_truth": example.get("code", ""),
                "attempts": len(all_attempts),
                "temperature": temperature,
                "max_new_tokens": max_new_tokens,
                "max_attempts": max_attempts,
                "lora_path": lora_path,
                "lora_merged": lora_merge,
                "dtype": str(_parse_dtype(dtype_cfg)),
                "device": device_str_for_json,
                "base_model": model_path,
                "instruction_path": example.get("instruction_path"),
                "image_path": example.get("image_abs_path"),
                "used_instruction": bool(instruction_text),
                "two_stage": two_stage,
                "require_instruction": require_instruction,
            }

            # 保存 JSON
            with open(os.path.join(out_json, f"sample_img_{i}.json"), "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            # 保存 TeX / PDF / PNG / LOG
            if final_doc is not None:
                with open(os.path.join(out_tex, f"sample_img_{i}.tex"), "w", encoding="utf-8") as tex_file:
                    tex_file.write(getattr(final_doc, "code", ""))
                print(f"样本 {i} 处理完成，尝试次数：{len(all_attempts)}，编译成功：{getattr(final_doc, 'has_content', False)}")
                compile_and_save(getattr(final_doc, "code", ""), i, out_pdf, out_png, out_log)
            else:
                skip_list.append(i)
                print(f"样本 {i} 处理失败，尝试次数：{len(all_attempts)}，返回结果为 None")

    except Exception as e:
        print(f"主循环出错：{e}")
        traceback.print_exc()

    print(f"============ 所有跳过的条目 {skip_list} ==================")


if __name__ == "__main__":
    # 推荐从项目根目录运行： python -m test.generate
    # 或指定其他 yaml： main("path/to/your_config.yaml")
    main("yaml/pipeline.yaml")