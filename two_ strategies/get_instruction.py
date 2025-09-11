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
    "你是一个“图像到 LaTeX 复刻”专家。请在不臆造内容的前提下，"
    "从给定图像中提炼出能够最大程度复刻版式与排版细节的 LaTeX 指导说明。"
    "输出用 Markdown，结构化且可操作。"
)

# API 设置
temperature = 0.7
top_p = 1
max_tokens = 2048
model = "ernie-x1-turbo-32k-preview"     #"gpt-4o" # "gpt-5-2025-08-07"  # "grok-4"  # "ernie-4.5-turbo-vl-preview"  # "gpt-5-2025-08-07" 备注：gpt不支持topp maxtoken等参数 # "gemini-2.5-pro" # "claude-3-7-sonnet-20250219" # ernie-x1-turbo-32k-preview

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
    user_instruction = """请针对这张科研绘图，生成完整的 LaTeX/TikZ 重构指导，涵盖以下内容并保持条理清晰：
1. 概览
- 描述图像的整体视觉要点：图形类型（流程图、坐标图、网络结构、热图等）、构图布局、主要元素关系。
2. 文档骨架与依赖
- 推荐的文档类（如 standalone）与核心宏包（TikZ, PGFPlots, xcolor, booktabs 等）。
- 若有特定功能（渐变、箭头、三维、矩阵），请指出需要的 TikZ 库或扩展。
3. 版面与画布设置
- 图形的尺寸（宽/高）、坐标系范围、纵横比。
- 节点与元素的间距、对齐方式。
- 建议的 \\tikzpicture 或 axis 环境参数。
4. 字体与配色
- 节点标签、坐标轴标题、注释所用字体（族、大小、粗细）。
- 主色、辅助色（RGB/CMYK/HTML 色值）。
- 如有渐变/透明度/阴影，请说明对应 TikZ 语法。
5. 结构与组件样式
- 节点（形状、边框、填充、对齐）。
- 边与箭头（线型、粗细、箭头样式）。
- 坐标轴（刻度、标签、网格线、legend 样式）。
6. 数学/表格/图形细节
- 若有公式，说明在 TikZ 节点中的排版方法。
- 若含表格，请指出列宽、对齐方式，以及是否用 booktabs 或 array。
- 若需曲线/柱状图/散点图，请给出 PGFPlots 核心片段。
7. 自定义宏与命令
- 封装常用样式（如节点样式、颜色、箭头），提高复用性。
8. 最小可运行示例 (MWE)
- 提供一个可直接编译的 standalone LaTeX 示例，生成与目标图最接近的效果。
- 用 fenced code block（```latex ... ```）。
9. 复刻检查清单
- 图形尺寸、坐标范围
- 节点/边样式
- 字体与字号
- 配色与线型
- 特殊效果（渐变、阴影）
- 与原图的差异点
10. 风险与替代方案
- 说明可能存在的不确定因素（如精确色值、字体差异）。
- 提出可接受的替代方案（如默认 Computer Modern vs Times New Roman，近似色替换）。
"""
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
):
    def numeric_tail_key(path: Path):
        m = re.search(r'(\d+)$', path.stem)
        return int(m.group(1)) if m else float('inf')

    image_paths = sorted(image_dir.glob("*.png"), key=numeric_tail_key)
    if not image_paths:
        print(f"目录中没有找到 PNG：{image_dir.resolve()}")
        return

    output_dir = Path("instruction") / model
    output_dir.mkdir(parents=True, exist_ok=True)

    failed_indices = []

    for p in image_paths:
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
            # 失败：不输出 md，仅记录 index
            if idx is not None:
                failed_indices.append(idx)
            print(f"[ERR] {p.name}: {e}")

        time.sleep(rate_limit_sleep)

    # 将失败 index 写入文件（每行一个 index）
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
)
