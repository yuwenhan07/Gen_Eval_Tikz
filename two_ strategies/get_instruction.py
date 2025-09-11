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
    "输出用 Markdown，结构化且可操作，尽量给出可复制的最小可运行示例（MWE）。"
)

# 输出为 Markdown
WRITE_PER_IMAGE_MD = False  # 若希望为每张图单独生成 md，可改为 True

# API 设置
temperature = 0.7
top_p = 1
max_tokens = 1024
model = "deepseek-reasoner"

api_key = os.getenv("BAIDU_LLM_API_KEY")
if not api_key:
    raise ValueError("请先设置BAIDU_LLM_API_KEY环境变量")

client = OpenAI(
    api_key=api_key,
    base_url="http://llms-se.baidu-int.com:8200",
)

def get_response(messages, temperature, top_p, max_tokens, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    # 思考过程: response.choices[0].message.reasoning_content
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
    # 生成锚点/文件名友好的 slug
    name = name.lower()
    name = re.sub(r"[^\w\-\.]+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name or "image"

def caption_all_pngs_to_markdown(
    image_dir: Path,
    temperature: float,
    top_p: float,
    max_tokens: int,
    model: str,
    rate_limit_sleep: float = 0.5,
):
    image_paths = sorted(p for p in image_dir.glob("*.png"))
    if not image_paths:
        print(f"目录中没有找到 PNG：{image_dir.resolve()}")
        return

    # 输出目录：output/<model>/
    output_dir = Path("instruction") / model
    output_dir.mkdir(parents=True, exist_ok=True)
    readme_path = output_dir / "README.md"

    lines = []
    lines.append(f"# TikZ/LaTeX 重构指导（模型：{model}）")
    lines.append("")
    lines.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 图像目录：`{image_dir}`")
    lines.append("")
    lines.append("## 目录")
    lines.append("")

    toc_entries = []
    per_image_sections = []

    for p in image_paths:
        try:
            messages = build_messages_for_image(p)
            md_body = get_response(
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                model=model,
            )
            # 从输出目录到图片的相对路径，确保 README 可以正确显示图片
            rel_img_path = os.path.relpath(p, output_dir)
            section_slug = slugify(p.name)
            toc_entries.append(f"- [{p.name}](#{section_slug})")

            # 可选：为每张图生成单独 md
            if WRITE_PER_IMAGE_MD:
                per_md_path = output_dir / f"{section_slug}.md"
                with open(per_md_path, "w", encoding="utf-8") as f:
                    f.write(f"# {p.name}\n\n")
                    f.write(f"![{p.name}]({rel_img_path})\n\n")
                    f.write(md_body.strip() + "\n")

            # 汇总到 README.md 的分节
            per_image_sections.append(f"## {p.name}\n")
            per_image_sections.append(f"![{p.name}]({rel_img_path})\n")
            # 确保模型输出是 Markdown；若不是，仍原样写入
            per_image_sections.append(md_body.strip() + "\n")

            print(f"[OK] {p.name}")
        except Exception as e:
            print(f"[ERR] {p.name}: {e}")
            section_slug = slugify(p.name)
            toc_entries.append(f"- [{p.name}](#{section_slug})")
            per_image_sections.append(f"## {p.name}\n")
            per_image_sections.append(f"> 处理出错：`{e}`\n")

        time.sleep(rate_limit_sleep)

    # 写入 README.md
    lines.extend(toc_entries)
    lines.append("")
    lines.extend(per_image_sections)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n已写出 Markdown 到：{readme_path.resolve()}")

# === 运行 ===
caption_all_pngs_to_markdown(
    IMAGE_DIR,
    temperature=temperature,
    top_p=top_p,
    max_tokens=max_tokens,
    model=model,
)