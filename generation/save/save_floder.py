import os
import traceback
from automatikz.infer import TikzDocument 

# 根目录（包含多个模型子目录）
base_dir = "../output/api"

# 遍历 base_dir 下的所有子目录
for model_name in os.listdir(base_dir):
    model_dir = os.path.join(base_dir, model_name)
    input_dir = os.path.join(model_dir, "output-tex")
    output_pdf_dir = os.path.join(model_dir, "pdf")
    output_png_dir = os.path.join(model_dir, "png")
    output_log_dir = os.path.join(model_dir, "log")

    # 如果没有 output-tex，就跳过
    if not os.path.isdir(input_dir):
        continue

    # 创建输出目录
    os.makedirs(output_pdf_dir, exist_ok=True)
    os.makedirs(output_png_dir, exist_ok=True)
    os.makedirs(output_log_dir, exist_ok=True)

    print(f"\n📂 正在处理模型目录: {model_name}")

    for filename in os.listdir(input_dir):
        if not filename.endswith(".tex"):
            continue

        tex_path = os.path.join(input_dir, filename)

        try:
            with open(tex_path, "r", encoding="utf-8") as f:
                tex_code = f.read()
        except Exception as e:
            print(f"❌ 无法读取文件 {filename}: {e}")
            continue

        tikzdoc = TikzDocument(code=tex_code)
        name_without_ext = os.path.splitext(filename)[0]

        print(f"🛠️ 正在处理: {filename}...")

        try:
            # 保存 PDF
            if tikzdoc.pdf:
                pdf_path = os.path.join(output_pdf_dir, name_without_ext + ".pdf")
                tikzdoc.save(pdf_path)
                print(f"✅ 已保存 PDF 到 {pdf_path}")

            # 保存 PNG
            if tikzdoc.has_content:
                png_path = os.path.join(output_png_dir, name_without_ext + ".png")
                img = tikzdoc.rasterize()
                img.save(png_path)
                print(f"✅ 已保存 PNG 到 {png_path}")

            # 编译失败写日志
            if tikzdoc.compiled_with_errors:
                log_path = os.path.join(output_log_dir, name_without_ext + ".log")
                with open(log_path, "w", encoding="utf-8") as log_file:
                    log_file.write(tikzdoc.log)
                print(f"⚠️ 编译 {filename} 出错，日志已保存到 {log_path}")

        except Exception as e:
            print(f"❌ 编译或保存 {filename} 失败: {e}")
            traceback.print_exc()