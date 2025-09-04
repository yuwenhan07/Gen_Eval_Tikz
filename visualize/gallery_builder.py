#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gallery Builder for TikZ Gen/Eval Dataset

Purpose
-------
Create a compact HTML gallery that shows, for each record in a metadata JSON,
its caption, the reference (dataset) image, and the corresponding generated
image (if present). Missing generated images appear as an empty placeholder.

Usage
-----
python gallery_builder.py \
  --meta \
  "/Users/yuwenhan/Library/Mobile Documents/com~apple~CloudDocs/Documents/🐟/科研/面向语义控制的可编辑可视结构生成/tikz/Gen_Eval_Tikz/eval_dataset/test_metadata.json" \
  --gen-dir \
  "/Users/yuwenhan/Library/Mobile Documents/com~apple~CloudDocs/Documents/🐟/科研/面向语义控制的可编辑可视结构生成/tikz/Gen_Eval_Tikz/generation/save/png" \
  --out gallery.html

Notes
-----
- The script tolerates 3 metadata formats: (a) a JSON array of records,
  (b) a single JSON object (wrapped to a list), or (c) NDJSON (one JSON per line).
- Generated image matching: by default, we try to match the base filename of the
  reference image (stem + any extension) within --gen-dir. As a fallback, we also
  try the numeric `index` if provided (e.g., test_123.png, 123.png).
- The output HTML uses absolute file paths converted to file:// URIs to ensure
  images render regardless of where you open the HTML file from.
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import html
import urllib.parse
import re


def load_records(meta_path: Path) -> List[Dict[str, Any]]:
    """Load records from JSON (array/object) or NDJSON.

    Each record is expected to include at least:
      - "caption": str
      - "image_path": str (relative or absolute)
    Optional:
      - "index": int
      - other fields like "code", "code_path", etc.
    """
    text = meta_path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # Try JSON first
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
    except json.JSONDecodeError:
        pass

    # Fallback: NDJSON (one JSON record per non-empty line)
    records: List[Dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                records.append(obj)
        except json.JSONDecodeError:
            continue
    return records


essential_keys = ("caption", "image_path")


def to_file_uri(p: Path) -> str:
    """Convert a Path to a file:// URI with proper quoting for spaces/emoji."""
    # Resolve for safety; don't strictly require existence here, handled elsewhere.
    ap = p.expanduser().resolve()
    # For macOS/unix paths like /Users/xxx/…
    return "file://" + urllib.parse.quote(str(ap))


def find_generated_image(gen_dir: Path, ref_img_path: Path, index: Optional[int]) -> Optional[Path]:
    """Try to find a generated image matching ref_img_path (by stem) or index."""
    if not gen_dir.exists():
        return None

    # 1) Try exact stem match first
    stem = ref_img_path.stem  # e.g., test_0

    # Common image extensions
    exts = [".png", ".jpg", ".jpeg", ".webp", ".bmp"]

    # a) Exact filename in gen_dir (stem + any ext)
    for ext in exts:
        candidate = gen_dir / f"{stem}{ext}"
        if candidate.exists():
            return candidate

    # b) Any file that starts with the stem (handles variants like test_0_v1.png)
    for p in gen_dir.glob(f"{stem}*"):
        if p.is_file() and p.suffix.lower() in exts:
            return p

    # 2) Try index-based guesses
    if index is not None:
        # i) Common patterns: test_{index}.png, {index}.png
        for name in (f"test_{index}", str(index)):
            for ext in exts:
                candidate = gen_dir / f"{name}{ext}"
                if candidate.exists():
                    return candidate
            for p in gen_dir.glob(f"{name}*"):
                if p.is_file() and p.suffix.lower() in exts:
                    return p

    return None


def short_path_display(p: Path, base: Optional[Path] = None, maxlen: int = 80) -> str:
    """Human-friendly short path for tooltips/captions in HTML."""
    try:
        ap = p.resolve()
    except Exception:
        ap = p
    s = str(ap)
    if base:
        try:
            s = str(ap.relative_to(base.resolve()))
        except Exception:
            pass
    if len(s) <= maxlen:
        return s
    return s[: maxlen - 3] + "…"


def render_html(records: List[Dict[str, Any]], meta_path: Path, gen_dir: Path, out_path: Path) -> None:
    total = len(records)
    found = 0

    # Precompute rows
    rows_html: List[str] = []

    meta_base = meta_path.parent

    for rec in records:
        # Validate minimal keys
        if not all(k in rec for k in essential_keys):
            # Skip silently if malformed
            continue
        caption = str(rec.get("caption", "")).strip()
        image_path = str(rec.get("image_path", "")).strip()
        idx = rec.get("index")
        try:
            index_int = int(idx) if idx is not None else None
        except Exception:
            index_int = None

        # Resolve reference image absolute path
        ref_img = (meta_base / image_path) if not Path(image_path).is_absolute() else Path(image_path)
        ref_img_uri = to_file_uri(ref_img)
        ref_title = html.escape(short_path_display(ref_img))
        ref_exists = ref_img.exists()

        # Find generated
        gen_img = find_generated_image(gen_dir, ref_img, index_int)
        if gen_img is not None and gen_img.exists():
            gen_img_uri = to_file_uri(gen_img)
            gen_title = html.escape(short_path_display(gen_img))
            gen_cell = f'<a href="{gen_img_uri}" target="_blank" title="{gen_title}"><img loading="lazy" src="{gen_img_uri}" alt="generated"/></a>'
            found += 1
        else:
            gen_cell = '<div class="placeholder" title="No generated image">No image</div>'

        # Caption HTML (escape, keep basic LaTeX commands as text)
        cap_html = html.escape(caption)

        # Index tag
        idx_label = f"#{index_int}" if index_int is not None else "—"

        row = f"""
        <div class="card" data-hasgen="{'1' if gen_img else '0'}">
          <div class="header">
            <div class="meta">Index: <span class="badge">{idx_label}</span></div>
          </div>
          <div class="caption">{cap_html}</div>
          <div class="cols">
            <div class="col">
              <div class="col-title">Reference</div>
              {f'<a href="{ref_img_uri}" target="_blank" title="{ref_title}"><img loading="lazy" src="{ref_img_uri}" alt="reference"/></a>' if ref_exists else '<div class="placeholder">Missing ref</div>'}
            </div>
            <div class="col">
              <div class="col-title">Generated</div>
              {gen_cell}
            </div>
          </div>
        </div>
        """
        rows_html.append(row)

    percent = (found / total * 100.0) if total else 0.0

    html_out = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<title>TikZ Gen/Eval Gallery</title>
<style>
  :root {{
    --bg: #0b0c10;      /* dark slate */
    --card: #12131a;    /* deep gray */
    --muted: #9aa3b2;   /* cool gray */
    --text: #e6e7eb;    /* near white */
    --accent: #6ea8fe;  /* blue */
    --warn: #ffb86b;    /* amber */
    --ok:   #7ee787;    /* green */
    --border: #232634;
  }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font: 14px/1.5 -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', 'Helvetica Neue', Arial, 'Apple Color Emoji', 'Segoe UI Emoji'; margin: 0; }}
  header {{ position: sticky; top: 0; z-index: 5; background: linear-gradient(180deg, rgba(18,19,26,0.95) 0%, rgba(18,19,26,0.85) 100%); backdrop-filter: saturate(180%) blur(6px); border-bottom: 1px solid var(--border); }}
  .wrap {{ max-width: 1280px; margin: 0 auto; padding: 16px; }}
  h1 {{ margin: 0 0 6px; font-weight: 700; font-size: 20px; }}
  .stats {{ color: var(--muted); font-size: 13px; }}
  .controls {{ display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }}
  .controls input[type="text"] {{ flex: 1 1 300px; padding: 8px 10px; border: 1px solid var(--border); background: #0e0f15; color: var(--text); border-radius: 10px; }}
  .controls .btn {{ padding: 8px 10px; border: 1px solid var(--border); background: #0e0f15; color: var(--text); border-radius: 10px; cursor: pointer; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 14px; padding: 16px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; display: flex; flex-direction: column; }}
  .card .header {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-bottom: 1px solid var(--border); background: rgba(255,255,255,0.02); }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; background: #0e213d; color: var(--accent); font-weight: 600; font-size: 12px; }}
  .caption {{ padding: 10px 12px; color: var(--muted); min-height: 56px; }}
  .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0; border-top: 1px solid var(--border); }}
  .col {{ padding: 10px; border-right: 1px solid var(--border); }}
  .col:last-child {{ border-right: 0; }}
  .col-title {{ font-weight: 600; margin-bottom: 6px; color: var(--text); font-size: 13px; }}
  img {{ width: 100%; height: 260px; object-fit: contain; background: #0e0f15; border: 1px dashed #1f2330; border-radius: 10px; padding: 6px; }}
  .placeholder {{ width: 100%; height: 260px; display: grid; place-items: center; color: var(--muted); border: 1px dashed #2a2f3d; border-radius: 10px; background: #0e0f15; }}
  footer {{ color: var(--muted); padding: 16px; text-align: center; }}
</style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>TikZ Gen/Eval Gallery</h1>
      <div class="stats">Records: <strong>{total}</strong> · Generated found: <strong style=\"color: var(--ok)\">{found}</strong> ({percent:.1f}%)</div>
      <div class="controls">
        <input id="search" type="text" placeholder="Filter by caption (regex supported)…" />
        <button class="btn" onclick="toggleMissing()">Show only missing generated</button>
        <button class="btn" onclick="resetFilters()">Reset</button>
      </div>
    </div>
  </header>

  <div class="grid" id="grid">
    {''.join(rows_html)}
  </div>

  <footer>Built from
    <code>{html.escape(str(meta_path))}</code>
    & · gen-dir: <code>{html.escape(str(gen_dir))}</code>
  </footer>

<script>
  const input = document.getElementById('search');
  const grid = document.getElementById('grid');
  let onlyMissing = false;

  function applyFilters() {{
    const q = input.value.trim();
    const cards = grid.children;
    for (const el of cards) {{
      const captionEl = el.querySelector('.caption');
      const hasGen = el.getAttribute('data-hasgen') === '1';
      let show = true;
      if (q) {{
        try {{
          const re = new RegExp(q, 'i');
          show = re.test(captionEl.textContent || '');
        }} catch(e) {{
          // Invalid regex -> simple substring match
          show = (captionEl.textContent || '').toLowerCase().includes(q.toLowerCase());
        }}
      }}
      if (onlyMissing && hasGen) show = false;
      el.style.display = show ? '' : 'none';
    }}
  }}

  input.addEventListener('input', applyFilters);

  function toggleMissing() {{
    onlyMissing = !onlyMissing;
    applyFilters();
  }}
  function resetFilters() {{
    onlyMissing = false;
    input.value = '';
    applyFilters();
  }}
</script>
</body>
</html>
"""

    out_path.write_text(html_out, encoding="utf-8")


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Build an HTML gallery of captions + reference + generated images.")
    p.add_argument("--meta", type=str, required=True, help="Path to test_metadata.json (or NDJSON)")
    p.add_argument("--gen-dir", type=str, required=True, help="Directory containing generated images (png/jpg/…)")
    p.add_argument("--out", type=str, default="gallery.html", help="Output HTML path")

    args = p.parse_args(argv)

    meta_path = Path(args.meta)
    gen_dir = Path(args.gen_dir)
    out_path = Path(args.out)

    if not meta_path.exists():
        print(f"[ERROR] meta file not found: {meta_path}", file=sys.stderr)
        return 2

    records = load_records(meta_path)
    if not records:
        print(f"[WARN] No records found in {meta_path}")

    render_html(records, meta_path, gen_dir, out_path)
    print(f"[OK] Wrote gallery -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
