# latex_utils.py
import re
import traceback
from typing import List, Optional, Tuple
from automatikz.infer import TikzDocument  # 还是依赖这个类


def parse_latex_errors(log: str, rootfile: str = "temp.tex") -> dict:
    errors = {}
    error_pattern = re.compile(
        rf"^{re.escape(rootfile)}:(\d+):\s*(.*?)(?=\n[^:]+:|$)",
        re.MULTILINE | re.DOTALL
    )
    for match in error_pattern.finditer(log):
        line = int(match.group(1))
        msg = match.group(2).strip()
        errors[line] = msg
    
    if not errors and re.search(r"Emergency stop|Fatal error", log, re.IGNORECASE):
        errors[0] = "Fatal error during compilation"
    return errors


def generate_and_repair(
    model,
    processor,
    image,
    prompt: str,
    max_attempts: int = 5,
    return_all: bool = False,
    do_sample: bool = False,
    max_new_tokens: int = 2048,
    temperature: float = 0.8,
    top_p: float = 0.9
) -> Tuple[TikzDocument, List[TikzDocument]]:
    """使用TikzDocument进行生成与修复（修复 _generate 参数/作用域问题，并加入 gen_id）"""

    all_attempts: List[TikzDocument] = []

    def _generate(snippet: str, gen_id: int) -> str:
        """基于当前 snippet 生成追加代码；gen_id 从 1 开始计数"""
        try:
            messages = [
                {"role": "system",
                 "content": ("You are a professional TikZ coding assistant, specializing in accurately "
                             "reconstructing LaTeX code that matches the visual effect of the original image (img) "
                             "based on the image content and its corresponding descriptive text (caption). "
                             "Your primary goal is to ensure that all graphic elements—including layout, dimensions, "
                             "colors, labels, and geometric relationships—rendered after compilation are highly "
                             "consistent with the original image. Additionally, maintain code standardization and "
                             "readability by using proper TikZ syntax and logical parameter settings, ensuring the "
                             "generated code is directly compilable and produces the expected results.\n"
                             "Please analyze the referenced image below and reconstruct an equivalent LaTeX/TikZ code "
                             "implementation that matches the visual appearance exactly.")},
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": (
                            f"[gen_id={gen_id}] Please generate LaTeX code based on the image and description:\n"
                            f"Existing code:\n{snippet}\n"
                            f"Description to be supplemented: {prompt}"
                        )}
                    ]
                }
            ]

            print(f"[gen_id={gen_id}] 当前输入 prompt 片段长度: {len(messages[-1]['content'][1]['text'])}")
            text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = processor(text=[text], images=[image], return_tensors="pt", padding=True).to(model.device)

            generated_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature,
                top_p=top_p
            )
            output_text = processor.batch_decode(
                generated_ids[:, inputs.input_ids.shape[1]:],
                skip_special_tokens=True
            )[0]

            # 优先提取代码块
            patterns = [
                r"```(?:latex|tex)?\s*(.*?)\s*```",
                r"(\\documentclass{standalone}.*?\\end{document})",
                r"(\\begin{tikzpicture}.*?\\end{tikzpicture})"
            ]
            for pattern in patterns:
                m = re.search(pattern, output_text, re.DOTALL | re.IGNORECASE)
                if m:
                    return m.group(1).strip()
            return output_text.strip()
        except Exception:
            traceback.print_exc()
            return ""

    def _recursive_repair(attempts_left: int, snippet: str = "", offset: int = 1, prev_first_error: Optional[int] = None):
        # 计算本次尝试序号：1..max_attempts
        gen_id = (max_attempts - attempts_left) + 1
        gen_id = max(1, gen_id)

        new_code = _generate(snippet, gen_id)
        full_code = (snippet + new_code) if snippet else new_code

        try:
            tikz_doc = TikzDocument(code=full_code)
            # 挂上 gen_id 便于后续定位
            setattr(tikz_doc, "gen_id", gen_id)
            all_attempts.append(tikz_doc)
        except Exception as e:
            class Dummy:
                pass
            dummy = Dummy()
            dummy.has_content = False
            dummy.compiled_with_errors = True
            dummy.log = f"TikzDocument error: {e}"
            dummy.code = full_code
            dummy.gen_id = gen_id
            all_attempts.append(dummy)
            return dummy

        # 成功或没有剩余尝试时退出
        if tikz_doc.has_content or attempts_left <= 1:
            return tikz_doc

        # 解析错误并裁剪回退
        errors = parse_latex_errors(tikz_doc.log)
        if not errors:
            return tikz_doc

        first_error = min(errors.keys())
        # 若错误行变化，offset 重置；否则指数回退，但给上限
        offset = 1 if first_error != prev_first_error else min(4 * offset, 4096)

        lines = full_code.splitlines(keepends=True)
        keep_lines = max(first_error - offset, 0)
        new_snippet = "".join(lines[:keep_lines])

        return _recursive_repair(attempts_left - 1, new_snippet, offset, first_error)

    final_doc = _recursive_repair(max_attempts)
    return final_doc, all_attempts