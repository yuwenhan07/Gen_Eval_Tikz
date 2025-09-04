#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gradio pager for TikZ Gen/Eval dataset with Google Translation support only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import gradio as gr
from PIL import Image, ImageDraw, ImageFont

# ------------------------
# Data loading utilities
# ------------------------

def load_records(meta_path: Path) -> List[Dict[str, Any]]:
    text = meta_path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
    except json.JSONDecodeError:
        pass
    out: List[Dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                out.append(obj)
        except json.JSONDecodeError:
            continue
    return out


def find_generated_image(gen_dir: Path, ref_img_path: Path, index: Optional[int]) -> Optional[Path]:
    if not gen_dir.exists():
        return None
    stem = ref_img_path.stem
    exts = [".png", ".jpg", ".jpeg", ".webp", ".bmp"]
    for ext in exts:
        p = gen_dir / f"{stem}{ext}"
        if p.exists():
            return p
    for p in gen_dir.glob(f"{stem}*"):
        if p.is_file() and p.suffix.lower() in exts:
            return p
    if index is not None:
        for name in (f"test_{index}", str(index), f"sample_img_{index}"):
            for ext in exts:
                p = gen_dir / f"{name}{ext}"
                if p.exists():
                    return p
            for p in gen_dir.glob(f"{name}*"):
                if p.is_file() and p.suffix.lower() in exts:
                    return p
    return None


def _open_image(path: Path) -> Optional[Image.Image]:
    try:
        return Image.open(path).convert("RGBA")
    except Exception:
        return None


def _placeholder(w: int, h: int, text: str = "No image") -> Image.Image:
    img = Image.new("RGBA", (w, h), (16, 18, 24, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.rectangle([(0, 0), (w - 1, h - 1)], outline=(42, 47, 61, 255), width=1)
    draw.text(((w - tw) // 2, (h - th) // 2), text, fill=(154, 163, 178, 255), font=font)
    return img


def scale_to_fit_height(im: Image.Image, target_h: int) -> Image.Image:
    w, h = im.size
    if h <= 0:
        h = 1
    new_w = max(1, int(round(w * (target_h / h))))
    return im.resize((new_w, target_h), Image.BICUBIC)

# ------------------------
# Translation helpers (Google only)
# ------------------------

def translate_caption_google(caption: str) -> str:
    try:
        from deep_translator import GoogleTranslator  # type: ignore
        zh = GoogleTranslator(source='auto', target='zh-CN').translate(caption)
        return zh or caption
    except Exception as e:
        print("[GoogleTranslator] 翻译失败:", e)
        return caption


def make_caption_md(caption_en: str, idx_int: Optional[int], zh_text: Optional[str]) -> str:
    idx_tag = f"#{idx_int}" if idx_int is not None else "—"
    if zh_text and zh_text.strip() and zh_text.strip() != caption_en.strip():
        return f"**Index:** `{idx_tag}`\n\n**Caption (EN):**\n{caption_en}\n\n**翻译（ZH）:**\n{zh_text}"
    else:
        return f"**Index:** `{idx_tag}`\n\n{caption_en}"

# ------------------------
# Render one page
# ------------------------

def render_page(records: List[Dict[str, Any]], idx: int, base_dir: Path, gen_dir: Path, target_h: int = 480) -> Tuple[str, Image.Image, Image.Image, str, Optional[int]]:
    if not records:
        return ("**空数据**", _placeholder(640, target_h, "No records"), _placeholder(640, target_h, "No records"), "0 / 0", None)
    idx = max(0, min(idx, len(records) - 1))
    rec = records[idx]
    caption = str(rec.get("caption", ""))
    img_rel = str(rec.get("image_path", "")).strip()
    ref_path = (base_dir / img_rel) if not Path(img_rel).is_absolute() else Path(img_rel)
    ref_img = _open_image(ref_path)
    if ref_img is None:
        ref_img = _placeholder(640, target_h, "Missing ref")
    ref_img = scale_to_fit_height(ref_img, target_h)
    idx_val = rec.get("index")
    try:
        idx_int = int(idx_val) if idx_val is not None else None
    except Exception:
        idx_int = None
    gen_path = find_generated_image(gen_dir, ref_path, idx_int)
    gen_img = _open_image(gen_path) if gen_path else None
    if gen_img is None:
        gen_img = _placeholder(ref_img.width, target_h, "No image")
    else:
        gen_img = scale_to_fit_height(gen_img, target_h)
    page_label = f"{idx + 1} / {len(records)}"
    return caption, ref_img.convert("RGB"), gen_img.convert("RGB"), page_label, idx_int

# ------------------------
# Gradio app
# ------------------------

def make_app(default_meta: Optional[str] = None, default_gen: Optional[str] = None) -> gr.Blocks:
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), css="""
    .gradio-container {max-width: 1000px !important}
    """) as demo:
        gr.Markdown("# TikZ Gen/Eval 样本可视化展示（仅支持Google翻译）")
        with gr.Row():
            meta_in = gr.Textbox(label="Metadata JSON 路径", value=default_meta or "", lines=1)
            gen_in = gr.Textbox(label="生成图片目录", value=default_gen or "", lines=1)
        with gr.Row():
            height_in = gr.Slider(240, 720, value=480, step=24, label="显示高度")
            jump_in = gr.Number(value=1, precision=0, label="跳转到第 N 条（1-based）")
            use_trans = gr.Checkbox(label="使用Google翻译Caption", value=False)
        with gr.Row():
            load_btn = gr.Button("📂 载入/刷新", variant="primary")
            prev_btn = gr.Button("⬅️ 上一条")
            next_btn = gr.Button("➡️ 下一条")

        caption_md = gr.Markdown("请先点击【载入/刷新】")
        with gr.Row():
            ref_out = gr.Image(label="Reference", interactive=False)
            gen_out = gr.Image(label="Generated", interactive=False)
        page_lab = gr.Label(value="0 / 0", label="进度")

        records_state = gr.State([])
        base_dir_state = gr.State("")
        gen_dir_state = gr.State("")
        idx_state = gr.State(0)

        def _compose_caption(rec, idx_int, use_trans_val):
            caption_en = str(rec.get("caption", ""))
            zh = None
            if use_trans_val:
                zh = translate_caption_google(caption_en)
            return make_caption_md(caption_en, idx_int, zh)

        def _load(meta_path: str, gen_dir: str, height: int, use_trans_val: bool):
            m = Path(meta_path).expanduser()
            g = Path(gen_dir).expanduser()
            if not m.exists():
                raise gr.Error(f"Meta file not found: {m}")
            recs = load_records(m)
            if not recs:
                raise gr.Error("No records parsed from metadata file")
            cap_raw, ref, gen, lab, idx_int = render_page(recs, 0, m.parent, g, target_h=height)
            cap_md = _compose_caption(recs[0], idx_int, use_trans_val)
            return recs, str(m.parent), str(g), 0, cap_md, ref, gen, lab, 1

        def _prev(recs, base_dir, gen_dir, idx, height, use_trans_val):
            if not recs:
                raise gr.Error("Records not loaded yet")
            idx = max(0, int(idx) - 1)
            cap_raw, ref, gen, lab, idx_int = render_page(recs, idx, Path(base_dir), Path(gen_dir), target_h=height)
            cap_md = _compose_caption(recs[idx], idx_int, use_trans_val)
            return idx, cap_md, ref, gen, lab, idx + 1

        def _next(recs, base_dir, gen_dir, idx, height, use_trans_val):
            if not recs:
                raise gr.Error("Records not loaded yet")
            idx = min(len(recs) - 1, int(idx) + 1)
            cap_raw, ref, gen, lab, idx_int = render_page(recs, idx, Path(base_dir), Path(gen_dir), target_h=height)
            cap_md = _compose_caption(recs[idx], idx_int, use_trans_val)
            return idx, cap_md, ref, gen, lab, idx + 1

        def _jump(recs, base_dir, gen_dir, height, n, use_trans_val):
            if not recs:
                raise gr.Error("Records not loaded yet")
            try:
                n_int = int(n)
            except Exception:
                raise gr.Error("请输入有效的整数 N（1-based）")
            if len(recs) == 0:
                raise gr.Error("No records")
            n_int = max(1, min(n_int, len(recs)))
            idx = n_int - 1
            cap_raw, ref, gen, lab, idx_int = render_page(recs, idx, Path(base_dir), Path(gen_dir), target_h=height)
            cap_md = _compose_caption(recs[idx], idx_int, use_trans_val)
            return idx, cap_md, ref, gen, lab

        load_btn.click(
            fn=_load,
            inputs=[meta_in, gen_in, height_in, use_trans],
            outputs=[records_state, base_dir_state, gen_dir_state, idx_state, caption_md, ref_out, gen_out, page_lab, jump_in],
        )

        prev_btn.click(
            fn=_prev,
            inputs=[records_state, base_dir_state, gen_dir_state, idx_state, height_in, use_trans],
            outputs=[idx_state, caption_md, ref_out, gen_out, page_lab, jump_in],
        )

        next_btn.click(
            fn=_next,
            inputs=[records_state, base_dir_state, gen_dir_state, idx_state, height_in, use_trans],
            outputs=[idx_state, caption_md, ref_out, gen_out, page_lab, jump_in],
        )

        jump_in.change(
            fn=_jump,
            inputs=[records_state, base_dir_state, gen_dir_state, height_in, jump_in, use_trans],
            outputs=[idx_state, caption_md, ref_out, gen_out, page_lab],
        )

    return demo


def main(argv: Optional[Iterable[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Gradio pager for TikZ Gen/Eval dataset with Google translation")
    ap.add_argument("--serve", action="store_true", help="Launch Gradio UI")
    ap.add_argument("--meta", type=str, default="", help="Default metadata path for the UI")
    ap.add_argument("--gen-dir", type=str, default="", help="Default generated image directory for the UI")
    ap.add_argument("--server-name", type=str, default="0.0.0.0", help="Host for gradio app")
    ap.add_argument("--server-port", type=int, default=7860, help="Port for gradio app")
    args = ap.parse_args()

    if args.serve:
        demo = make_app(default_meta=args.meta or None, default_gen=args.gen_dir)
        demo.launch(server_name=args.server_name, server_port=args.server_port, inbrowser=False)
        return 0
    else:
        print("Use --serve to launch the Gradio UI. Example: python gradio_show.py --serve --meta /path/to/test_metadata.json --gen-dir /path/to/png")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())