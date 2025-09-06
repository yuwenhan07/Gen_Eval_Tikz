from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from PIL import Image
import os
import json
import traceback
from tqdm import tqdm
import torch
import yaml
import re  # NEW: for ${var} substitution
from util.repair_strategy import generate_and_repair
from util.save_and_complie import compile_and_save

# log 落盘
import datetime
import platform
from pprint import pformat

# 新增：可选导入 PEFT（用于 LoRA）
try:
    from peft import PeftModel
    _HAS_PEFT = True
except Exception:
    _HAS_PEFT = False

# log输出函数
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

def _summarize_config(cfg: dict, parsed_dtype, model_device: str, lora_enabled: bool) -> dict:
    """组装一份可序列化的运行概要，便于打印和落盘"""
    model_cfg = cfg.get("model", {})
    data_cfg = cfg.get("data", {})
    gen_cfg = cfg.get("gen", {})
    run_cfg = cfg.get("run", {})

    outputs_cfg = cfg["outputs_lora"] if lora_enabled else cfg["outputs_base"]

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
        # 保存 JSON
        with open(os.path.join(log_dir, "run_config.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        # 保存可读文本
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
    # 兜底
    return "auto"


# =========================
# NEW: YAML 变量替换工具
# =========================
_VAR_PATTERN = re.compile(r"\$\{([A-Za-z0-9_]+)\}")

def _collect_vars(cfg: dict) -> dict:
    """
    从 YAML 的顶层收集可替换变量。
    - 推荐在 YAML 顶层写：checkpoint: 562
    - 自动提供两个等价变量名：checkpoint 与 ckpt
    - 也会把所有顶层的标量（str/int/float/bool）加入变量表，便于复用
    """
    vars_map = {}
    # 常见约定：checkpoint / ckpt
    if "checkpoint" in cfg and isinstance(cfg["checkpoint"], (str, int, float)):
        v = str(cfg["checkpoint"])
        vars_map["checkpoint"] = v
        vars_map["ckpt"] = v

    # 其他顶层标量也允许作为变量
    for k, v in cfg.items():
        if isinstance(v, (str, int, float, bool)):
            vars_map.setdefault(k, str(v))

    return vars_map


def _subst_in_str(s: str, vars_map: dict) -> str:
    def repl(m):
        name = m.group(1)
        return vars_map.get(name, m.group(0))  # 未知变量保持原样
    return _VAR_PATTERN.sub(repl, s)


def _subst_cfg(obj, vars_map: dict):
    """
    递归地对 dict/list/str 做 ${var} 替换。
    """
    if isinstance(obj, dict):
        return {k: _subst_cfg(v, vars_map) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_subst_cfg(v, vars_map) for v in obj]
    elif isinstance(obj, str):
        return _subst_in_str(obj, vars_map)
    else:
        return obj
# =========================


def load_config(cfg_path: str = "config.yaml") -> dict:
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"未找到配置文件：{cfg_path}")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # ---- 在设默认值之前，先做一次变量替换，确保路径等能被替换出来 ----
    vars_map = _collect_vars(cfg if isinstance(cfg, dict) else {})
    cfg = _subst_cfg(cfg, vars_map)

    # ---- model ----
    cfg.setdefault("model", {})
    cfg["model"].setdefault("device", "cuda")
    cfg["model"].setdefault("dtype", "auto")
    # 新增：LoRA 配置（可选）
    cfg["model"].setdefault("enable_lora", False)
    cfg["model"].setdefault("lora_path", None)     # 例如: "./checkpoint-${ckpt}"
    cfg["model"].setdefault("lora_merge", False)   # True 时 merge_and_unload

    # ---- data ----
    cfg.setdefault("data", {})
    if "metadata_path" not in cfg["data"] or "base_dir" not in cfg["data"]:
        raise ValueError("config.yaml 中 data.metadata_path / data.base_dir 不能为空")

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

    # ----------- outputs（新增双配置 + 兼容）-----------
    cfg.setdefault("outputs_lora", {})
    cfg["outputs_lora"].setdefault("json_dir", cfg["outputs_lora"]["json_dir"])
    cfg["outputs_lora"].setdefault("tex_dir",  cfg["outputs_lora"]["tex_dir"])
    cfg["outputs_lora"].setdefault("pdf_dir",  cfg["outputs_lora"]["pdf_dir"])
    cfg["outputs_lora"].setdefault("png_dir",  cfg["outputs_lora"]["png_dir"])
    cfg["outputs_lora"].setdefault("log_dir",  cfg["outputs_lora"]["log_dir"])

    cfg.setdefault("outputs_base", {})
    cfg["outputs_base"].setdefault("json_dir", cfg["outputs_base"]["json_dir"])
    cfg["outputs_base"].setdefault("tex_dir",  cfg["outputs_base"]["tex_dir"])
    cfg["outputs_base"].setdefault("pdf_dir",  cfg["outputs_base"]["pdf_dir"])
    cfg["outputs_base"].setdefault("png_dir",  cfg["outputs_base"]["png_dir"])
    cfg["outputs_base"].setdefault("log_dir",  cfg["outputs_base"]["log_dir"])

    cfg = _subst_cfg(cfg, _collect_vars(cfg))

    return cfg


def ensure_dirs(*paths: str):
    for p in paths:
        os.makedirs(p, exist_ok=True)


def main(cfg_path: str = "config.yaml"):
    # 载入配置
    cfg = load_config(cfg_path)
    model_path = cfg["model"]["model_path"]
    device = cfg["model"]["device"]
    dtype_cfg = cfg["model"]["dtype"]
    lora_enabled = bool(cfg["model"]["enable_lora"])  # ← 新增：判断是否启用 LoRA
    lora_path = cfg["model"]["lora_path"]
    lora_merge = bool(cfg["model"]["lora_merge"])

    metadata_path = cfg["data"]["metadata_path"]
    base_dir = cfg["data"]["base_dir"]

    do_sample = cfg["gen"]["do_sample"]
    temperature = cfg["gen"]["temperature"]
    max_new_tokens = cfg["gen"]["max_new_tokens"]
    top_p = cfg["gen"]["top_p"]

    max_attempts = cfg["run"]["max_attempts"]
    limit = cfg["run"]["limit"]

    log_dir = cfg["output_log"]["log_dir"]

    # 选择输出组：启用 LoRA 用 outputs_lora，否则 outputs_base
    outputs_cfg = cfg["outputs_lora"] if lora_enabled else cfg["outputs_base"]
    out_json = outputs_cfg["json_dir"]
    out_tex  = outputs_cfg["tex_dir"]
    out_pdf  = outputs_cfg["pdf_dir"]
    out_png  = outputs_cfg["png_dir"]
    out_log  = outputs_cfg["log_dir"]
    print(f"输出目录使用：{'outputs_lora' if lora_enabled else 'outputs_base'}")

    # === Logging additions: 先打印一次基于配置的概览（设备等稍后再补齐） ===
    # 这里先用 dtype_cfg 和 device 字段占位，等模型成功加载后会再打印一次“实效设备/权重状态”
    prelim_summary = _summarize_config(cfg, _parse_dtype(dtype_cfg), device, lora_enabled)
    _print_and_save_summary(prelim_summary, log_dir)

    # 1. 加载模型和处理器
    try:
        print("正在加载模型和处理器...")
        parsed_dtype = _parse_dtype(dtype_cfg)

        # 注意：transformers 接受 torch_dtype="auto" 或 torch.dtype
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=parsed_dtype,
            trust_remote_code=True,
        )

        # 如果需要指定设备（不是 device_map），则放到指定设备
        if isinstance(device, str) and device.lower() != "auto":
            model = model.to(device)

        # 可选：注入 LoRA
        if lora_enabled and lora_path:
            if not _HAS_PEFT:
                raise RuntimeError("检测到需要加载 LoRA，但未安装 peft。请先 pip install peft。")
            if not os.path.exists(lora_path):
                raise FileNotFoundError(f"指定的 LoRA 路径不存在：{lora_path}")

            print(f"正在加载 LoRA 适配器：{lora_path}")
            model = PeftModel.from_pretrained(model, lora_path)
            # 可选：合并 LoRA 到基座权重（推理更方便，不能再训练 LoRA）
            if lora_merge:
                print("正在将 LoRA 合并进基座（merge_and_unload）...")
                model = model.merge_and_unload()

        processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
        print(f"模型加载成功，设备：{model.device}，LoRA：{'启用' if lora_enabled else '未启用'}，合并：{lora_merge if lora_enabled else 'N/A'}")
        # === Logging additions: 基于“真实已加载模型”的最终概览 ===
        final_summary = _summarize_config(cfg, _parse_dtype(dtype_cfg), str(model.device), lora_enabled)
        _print_and_save_summary(final_summary, log_dir)
    except Exception as e:
        print(f"模型加载失败：{e}")
        traceback.print_exc()
        return

    # 2. 读取数据集
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
            ds.append({
                "image": image,
                "caption": item.get("caption", ""),
                "code": item.get("code", "")
            })
        except Exception as e:
            print(f"Error: 读取图片 {img_abs_path} 失败: {e}，已跳过")
            continue

    print(f"数据集装载完成：有效样本数 = {len(ds)}（来自 {metadata_path}）")
    if len(ds) == 0:
        print("无有效样本，程序退出")
        return

    # 3. 输出目录
    ensure_dirs(out_tex, out_json, out_pdf, out_png, out_log)

    # 4. 主循环
    skip_list = []
    try:
        iterable = ds if limit in (None, 0) else ds[:int(limit)]
        for i, example in enumerate(tqdm(iterable, desc="Processing samples")):
            print("\n" + "-" * 60)
            print(f"[Sample {i}]")
            print(f"Prompt: {example.get('caption', '')[:120]}{'...' if len(example.get('caption',''))>120 else ''}")
            print(f"GenParams: do_sample={do_sample} | max_new_tokens={max_new_tokens} | temperature={temperature} | top_p={top_p}")

            image = example["image"]
            prompt = example["caption"]
            # 生成+修复（按 YAML 中的参数调整）
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

            result = {
                "prompt": prompt,
                "final_latex_code": getattr(final_doc, "code", "") if final_doc is not None else "",
                "compiled_successfully": getattr(final_doc, "has_content", False) if final_doc is not None else False,
                "ground_truth": example["code"],
                "attempts": len(all_attempts),
                "temperature": temperature,
                "max_new_tokens": max_new_tokens,
                "max_attempts": max_attempts,
                # 记录 LoRA 状态以便复现实验
                "lora_path": lora_path,
                "lora_merged": lora_merge,
                "dtype": str(parsed_dtype),
                "device": str(model.device),
                "base_model": model_path,
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
    # 推荐从项目根目录运行（确保包导入路径正确）：
    #   python -m test.generate
    #
    # 如需指定其他配置文件路径，可改成：
    #   main("path/to/your_config.yaml")
    main("yaml/lora_model.yaml")
