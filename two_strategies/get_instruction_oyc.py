import base64
from pathlib import Path
import time
import os
import re
from datetime import datetime
from openai import OpenAI

# === 可选：根据需要改一改 ===
IMAGE_DIR = Path("../eval_dataset/images")
SYSTEM_PROMPT = (
    " "
)

# API 设置
temperature = 1
top_p = 1
max_tokens = 2048
model = "ernie-x1-turbo-32k-preview"     # "claude-sonnet-4-20250514" #"gpt-4o" # "gpt-5-2025-08-07"  # "grok-4"  # "ernie-4.5-turbo-vl-preview"  # "gpt-5-2025-08-07" 备注：gpt不支持topp maxtoken等参数 # "gemini-2.5-pro" # "claude-3-7-sonnet-20250219" # ernie-x1-turbo-32k-preview
START_INDEX = 100
PROCESS_NUM = 10  # 设置 None 则处理全部

api_key = os.getenv("BAIDU_LLM_API_KEY")
if not api_key:
    raise ValueError("请先设置BAIDU_LLM_API_KEY环境变量")

client = OpenAI(
    api_key=api_key,
    base_url="http://llms-se.baidu-int.com:8200/",
)

# === 开关 ===
USE_SAMPLING_ARGS = True

def get_response(messages, temperature, top_p, max_tokens, model):
    kwargs = {
        "model": model,
        "messages": messages,
    }

    if USE_SAMPLING_ARGS:
        # 仅在开关为 True 时才加这些参数
        kwargs.update({
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
        })

    response = client.chat.completions.create(**kwargs)

    return response.choices[0].message.content


def encode_image_to_data_url(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    # 这里默认是 PNG，如有其他格式按需替换 MIME
    return f"data:image/png;base64,{b64}"

def build_messages_for_image(image_path: Path):
    data_url = encode_image_to_data_url(image_path)
    user_instruction = r"""You are an expert technical writer specializing in LaTeX and TikZ. Your task is to analyze the uploaded image and generate a detailed Markdown guide to reconstruct it.

    Please structure your response strictly according to the following 10 sections. Ensure the content is detailed and the code is accurate.

    **1. Overview**
    - Briefly describe the core content, theme, and main components of the image in plain language.

    **2. Document Skeleton & Dependencies**
    - List the required `\documentclass` and all necessary `\usepackage` packages (e.g., `tikz`, `xcolor`, `amssymb`).

    **3. Layout & Canvas Settings**
    - Estimate and recommend appropriate canvas dimensions, scaling factors, and global style settings for the `tikzpicture` environment.

    **4. Fonts & Colors**
    - Identify all colors in the image (fills, borders, text) and provide suggested definitions (`\colorlet`, RGB values, or names).
    - Describe the font styles used for different elements (e.g., title, labels, math symbols).

    **5. Structure & Component Styles**
    - Break down each core graphical component in the image (e.g., ellipses, rectangles, lines).
    - Detail their styles, including shape, approximate dimensions, border thickness, and fill effects (like opacity).

    **6. Math/Table/Graphic Details**
    - Point out any special mathematical symbols, Greek letters, or unique graphics and explain how to implement them in LaTeX (e.g., `$\chi$`, `$\blacksquare$`).

    **7. Custom Macros & Commands**
    - (If applicable) Suggest custom `\tikzset` styles to simplify the code and improve readability.

    **8. MWE (Minimum Working Example)**
    - **This is the most critical section.** Provide a complete, copy-paste-ready, and compilable LaTeX code block that generates an image highly similar to the original.

    **9. Replication Checklist**
    - Create a simple checklist of key points for the user to verify against the original image during replication.

    **10. Risks & Alternatives**
        - Mention potential challenges in the replication process (e.g., exact color matching, font availability) and suggest possible solutions or alternative implementation methods.

    Please analyze the image I've uploaded and generate this guide now."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_instruction},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        },
    ]
    return messages

def slugify(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^\w\-\.]+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name or "image"

def extract_index(path: Path):
    """从文件名末尾提取数字 index，例如 test_12.png -> 12"""
    m = re.search(r'(\d+)$', path.stem)
    return int(m.group(1)) if m else None

# === 新增：按照起始index与数量筛选 ===
def _select_image_paths(image_paths, start_index=None, nums=None):
    """
    根据 start_index（基于文件名末尾数字）与 nums 进行选择。
    - 仅当 start_index 不为 None 时，才过滤出 index >= start_index 且带有数字尾巴的图片。
    - 保持原有排序（按数字尾巴升序，非数字在最后）。
    - 若 nums 不为 None，则截取前 nums 个。
    """
    pairs = [(p, extract_index(p)) for p in image_paths]
    if start_index is not None:
        pairs = [(p, idx) for (p, idx) in pairs if idx is not None and idx >= start_index]
    selected = [p for (p, _) in pairs]
    if nums is not None:
        selected = selected[:nums]
    return selected

def write_markdown_for_image(image_path: Path, md_body: str, output_dir: Path):
    """
    以图片名生成单独的 Markdown 文件，立刻写盘。
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    rel_img_path = os.path.relpath(image_path, output_dir)
    section_slug = slugify(image_path.stem)
    md_path = output_dir / f"{section_slug}.md"

    lines = []
    lines.append(f"# {image_path.name}")
    lines.append("")
    lines.append(f"![{image_path.name}]({rel_img_path})")
    lines.append("")
    lines.append(md_body.strip())
    lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return md_path

def caption_all_pngs_to_markdown(
    image_dir: Path,
    temperature: float,
    top_p: float,
    max_tokens: int,
    model: str,
    rate_limit_sleep: float = 0.5,
    start_index: int | None = None,   # 新增
    nums: int | None = None,          # 新增
):
    def numeric_tail_key(path: Path):
        m = re.search(r'(\d+)$', path.stem)
        return int(m.group(1)) if m else float('inf')

    image_paths = sorted(image_dir.glob("*.png"), key=numeric_tail_key)
    if not image_paths:
        print(f"目录中没有找到 PNG：{image_dir.resolve()}")
        return

    # 选择要处理的图片
    selected_paths = _select_image_paths(image_paths, start_index=start_index, nums=nums)
    if not selected_paths:
        if start_index is not None:
            print(f"按 start_index={start_index} 过滤后没有图片。请检查文件名数字尾巴，例如 foo_12.png。")
        else:
            print("没有匹配到待处理的图片。")
        return

    output_dir = Path("instruction_oyc") / model
    output_dir.mkdir(parents=True, exist_ok=True)

    print("[PLAN]")
    for p in selected_paths:
        print(" -", p.name)

    failed_indices = []

    for p in selected_paths:
        idx = extract_index(p)
        try:
            messages = build_messages_for_image(p)
            md_body = get_response(
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                model=model,
            )
            md_path = write_markdown_for_image(
                image_path=p,
                md_body=md_body,
                output_dir=output_dir,
            )
            print(f"[OK] {p.name} -> {md_path.resolve()}")
        except Exception as e:
            if idx is not None:
                failed_indices.append(idx)
            print(f"[ERR] {p.name}: {e}")

        time.sleep(rate_limit_sleep)

    if failed_indices:
        failed_path = output_dir / "failed_indices.txt"
        with open(failed_path, "w", encoding="utf-8") as f:
            for i in failed_indices:
                f.write(f"{i}\n")
        print(f"[SUMMARY] 失败 index 已保存到: {failed_path.resolve()} ({len(failed_indices)} 个)")


# === 运行 ===
caption_all_pngs_to_markdown(
    IMAGE_DIR,
    temperature=temperature,
    top_p=top_p,
    max_tokens=max_tokens,
    model=model,
    start_index=START_INDEX,
    nums=PROCESS_NUM,
)
