# util/latex_utils.py
import os
os.environ["PATH"] = "/home/wudongze/texlive/2024/bin/x86_64-linux:" + os.environ.get("PATH", "")
import re
import traceback
from typing import List, Optional, Tuple
from automatikz.infer import TikzDocument  # 依赖 TikzDocument


def compile_and_save(tex_code: str, sample_id: int,
                     output_pdf_dir: str, output_png_dir: str, output_log_dir: str) -> bool:
    """编译 LaTeX 代码并保存 PDF、PNG 和日志"""
    filename = f"sample_img_{sample_id}"

    # print(f"Current PATH: {os.environ.get('PATH', 'Not set')}")
    try:
        # 创建 TikzDocument 实例
        tikzdoc = TikzDocument(code=tex_code)
        print(f"TikzDocument created successfully: {tikzdoc is not None}")
        print(f"TikzDocument has_content: {getattr(tikzdoc, 'has_content', 'Unknown')}")
        print(f"TikzDocument compiled_with_errors: {getattr(tikzdoc, 'compiled_with_errors', 'Unknown')}")
        # 保存 PDF
        if getattr(tikzdoc, "pdf", None):
            print("正在尝试编译pdf")
            os.makedirs(output_pdf_dir, exist_ok=True)
            pdf_path = os.path.join(output_pdf_dir, f"{filename}.pdf")
            tikzdoc.save(pdf_path)
            print(f"✅ 已保存 PDF 到 {pdf_path}")

        # 保存 PNG
        if getattr(tikzdoc, "has_content", False):
            os.makedirs(output_png_dir, exist_ok=True)
            png_path = os.path.join(output_png_dir, f"{filename}.png")
            img = tikzdoc.rasterize()
            img.save(png_path)
            print(f"✅ 已保存 PNG 到 {png_path}")

        # 保存错误日志
        if getattr(tikzdoc, "compiled_with_errors", False):
            os.makedirs(output_log_dir, exist_ok=True)
            log_path = os.path.join(output_log_dir, f"{filename}.log")
            with open(log_path, "w", encoding="utf-8") as log_file:
                log_file.write(getattr(tikzdoc, "log", ""))
            print(f"⚠️ 编译 {filename} 时可能出错！日志已保存至 {log_path}")

        return True
    except Exception as e:
        print(f"❌ 编译或保存 {filename} 失败: {e}")
        traceback.print_exc()
        return False