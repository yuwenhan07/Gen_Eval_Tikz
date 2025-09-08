import os
import io
import re
import json
import base64
import datetime
import random
from typing import Dict, List, Tuple
from PIL import Image
from openai import OpenAI
from tqdm.auto import tqdm  # ← 新增

# ======== 可按需修改的常量 ========
MODEL_NAME    = "grok-4"  # "ernie-4.5-turbo-vl-preview"  # "gpt-5-2025-08-07" 备注：gpt不支持topp maxtoken等参数 # "gemini-2.5-pro" # "claude-3-7-sonnet-20250219"
BASE_URL      = "http://llms-se.baidu-int.com:8200"

METADATA_PATH = "../../eval_dataset/test_metadata.json"
BASE_DIR      = "../../eval_dataset"

# 批处理相关
START_INDEX   = 1    # 起始索引（0-based）
NUM_SAMPLES   = 99     # 要处理的样本数；<=0 表示处理全部
SHUFFLE       = False

# 超参数
TEMPERATURE   = 0.8
TOP_P         = 0.9
MAX_TOKENS    = 2048

# 控制是否传递超参数
USE_SYSTEM_PROMPT = True   # 控制是否使用 system 消息 gemini不支持system
USE_SAMPLING_PARAMS = True   # 不支持 temperature/top_p 的模型可设为 False
USE_MAX_TOKENS      = True   # 不支持 max_tokens 的模型可设为 False

# 输出目录：用模型名生成
MODEL_DIRNAME = re.sub(r"[^\w\-]+", "_", MODEL_NAME)
OUT_TEX_DIR   = os.path.join("../output/api", MODEL_DIRNAME, "output-tex")
OUT_JSON_DIR  = os.path.join("../output/api", MODEL_DIRNAME, "original-output")
# =================================


def _chat_create(client: OpenAI, messages):
    """
    统一的聊天创建封装
    """
    kwargs = {"model": MODEL_NAME, "messages": messages}
    if USE_MAX_TOKENS and MAX_TOKENS is not None:
        kwargs["max_tokens"] = MAX_TOKENS
    if USE_SAMPLING_PARAMS:
        kwargs["temperature"] = TEMPERATURE
        kwargs["top_p"] = TOP_P
    return client.chat.completions.create(**kwargs)


def _ensure_dirs(*paths: str):
    for p in paths:
        os.makedirs(p, exist_ok=True)


def _pil_to_data_url(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def _build_messages(image: Image.Image, caption: str, snippet: str = "") -> list:
    """
    构建 OpenAI Chat Completions 风格的多模态消息：
    - 文本部分描述任务与需求
    - 图片以 data URL 的 image_url 传给模型
    """
    system_text = (
        "You are a professional TikZ coding assistant, specializing in accurately "
        "reconstructing LaTeX code that matches the visual effect of the original image (img) "
        "based on the image content and its corresponding descriptive text (caption). "
        "Your primary goal is to ensure that all graphic elements—including layout, dimensions, "
        "colors, labels, and geometric relationships—rendered after compilation are highly "
        "consistent with the original image. Additionally, maintain code standardization and "
        "readability by using proper TikZ syntax and logical parameter settings, ensuring the "
        "generated code is directly compilable and produces the expected results.\n"
        "Please analyze the referenced image below and reconstruct an equivalent LaTeX/TikZ code "
        "implementation that matches the visual appearance exactly."
    )

    # user 内容
    lines = []
    if not USE_SYSTEM_PROMPT:
        # 如果不用 system，就直接拼进 user prompt
        lines.append(system_text)

    lines.append("Please generate LaTeX code based on the image and description:")
    if snippet.strip():
        lines.append("Existing code:\n" + snippet)
    if caption.strip():
        lines.append("Description to be supplemented: " + caption)

    text_part = "\n".join(lines)
    data_url = _pil_to_data_url(image)

    messages = []
    if USE_SYSTEM_PROMPT:
        messages.append({"role": "system", "content": system_text})

    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": text_part},
            {"type": "image_url", "image_url": {"url": data_url}},
        ],
    })
    return messages


def _extract_latex(text: str) -> str:
    patterns = [
        r"```(?:latex|tex)?\s*(.*?)\s*```",
        r"(\\documentclass\{standalone\}.*?\\end\{document\})",
        r"(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})",
    ]
    for p in patterns:
        m = re.search(p, text, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return text.strip()


def _safe_stem(idx: int, img_rel_path: str) -> str:
    base = os.path.splitext(os.path.basename(img_rel_path))[0]
    base = re.sub(r"[^\w\-]+", "_", base)
    return f"sample_img_{idx}"


def _load_metadata(path: str) -> List[Dict]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到 metadata：{path}")
    with open(path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    if not isinstance(meta, list) or len(meta) == 0:
        raise ValueError("metadata 内容为空或格式非列表")
    return meta


def _select_indices(n_total: int, start: int, num: int, shuffle: bool) -> List[int]:
    start = max(0, min(start, n_total - 1))
    if num is None or num <= 0:
        indices = list(range(start, n_total))
    else:
        end = min(n_total, start + num)
        indices = list(range(start, end))
    if shuffle:
        random.seed(42)
        random.shuffle(indices)
    return indices


def _save_outputs(
    tex_dir: str,
    json_dir: str,
    stem: str,
    final_code: str,
    raw_output: str,
    payload_extra: Dict,
):
    _ensure_dirs(tex_dir, json_dir)
    tex_path = os.path.join(tex_dir, f"{stem}.tex")
    json_path = os.path.join(json_dir, f"{stem}.json")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(final_code)

    payload = {
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        **payload_extra,
        "raw_output": raw_output,
        "extracted_code": final_code,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"已保存 TEX:  {tex_path}")
    print(f"已保存原始输出(JSON): {json_path}")


def process_one(
    client: OpenAI,
    rec: Dict,
    idx: int,
) -> Tuple[bool, str]:
    img_rel = rec.get("image_path")
    caption = rec.get("caption", "")
    snippet = ""

    if not img_rel:
        return False, f"第 {idx} 条样本缺少 image_path"

    img_abs = os.path.join(BASE_DIR, img_rel)
    if not os.path.exists(img_abs):
        return False, f"样本图片不存在：{img_abs}"

    image = Image.open(img_abs).convert("RGB")
    messages = _build_messages(image=image, caption=caption, snippet=snippet)
    # resp = client.chat.completions.create(
    #     model=MODEL_NAME,
    #     messages=messages,
    #     temperature=TEMPERATURE,
    #     top_p=TOP_P,
    #     max_tokens=MAX_TOKENS,
    # )
    resp = _chat_create(client, messages)
    raw_output = (resp.choices[0].message.content or "").strip()
    final_code = _extract_latex(raw_output)

    stem = _safe_stem(idx, img_rel)
    _save_outputs(
        OUT_TEX_DIR,
        OUT_JSON_DIR,
        stem,
        final_code,
        raw_output,
        {
            "sample_index": idx,
            "image_rel_path": img_rel,
            "caption": caption,
            "snippet_input": snippet,
        },
    )
    return True, ""


def main():
    # 1) API 初始化
    api_key = os.getenv("BAIDU_LLM_API_KEY")
    if not api_key:
        raise ValueError("请先设置环境变量 BAIDU_LLM_API_KEY")
    client = OpenAI(api_key=api_key, base_url=BASE_URL)

    # 2) 读取数据
    meta = _load_metadata(METADATA_PATH)
    n_total = len(meta)
    indices = _select_indices(n_total, START_INDEX, NUM_SAMPLES, SHUFFLE)

    print(f"准备处理 {len(indices)} 条样本（数据集总数：{n_total}，起始：{START_INDEX}，"
          f"数量：{NUM_SAMPLES if NUM_SAMPLES>0 else 'ALL'}，shuffle={SHUFFLE}）")

    # 3) 循环生成（集成 tqdm）
    success_cnt = 0
    failures: List[Tuple[int, str]] = []

    pbar = tqdm(indices, total=len(indices), desc="Processing", unit="sample")
    for i, idx in enumerate(pbar, start=1):
        pbar.set_postfix({"ok": success_cnt, "fail": len(failures), "idx": idx})
        try:
            ok, err = process_one(client, meta[idx], idx)
            if ok:
                success_cnt += 1
            else:
                failures.append((idx, err))
                pbar.write(f"[跳过] idx={idx} -> {err}")
        except Exception as e:
            failures.append((idx, repr(e)))
            pbar.write(f"[异常] idx={idx}: {repr(e)}")
        # 每步更新后缀（让 ok/fail 实时刷新）
        pbar.set_postfix({"ok": success_cnt, "fail": len(failures), "idx": idx})

    pbar.close()

    # 4) 汇总
    print("\n================== 处理完成 ==================")
    print(f"成功：{success_cnt} / {len(indices)}")
    if failures:
        print(f"失败：{len(failures)} 条，详情：")
        for idx, msg in failures:
            print(f" - idx={idx}: {msg}")


if __name__ == "__main__":
    main()
