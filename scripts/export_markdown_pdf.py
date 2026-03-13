#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from fpdf import FPDF


DEFAULT_FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"


def normalize_inline_markdown(line: str) -> str:
    line = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1 (\2)", line)
    line = re.sub(r"`([^`]*)`", r"\1", line)
    return line


def render_markdown_to_pdf(markdown_path: Path, pdf_path: Path, font_path: str) -> None:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font("CJK", style="", fname=font_path)
    pdf.set_font("CJK", size=12)

    def write_line(height: float, content: str) -> None:
        pdf.multi_cell(0, height, content, new_x="LMARGIN", new_y="NEXT")

    in_code_block = False
    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            pdf.ln(2)
            continue

        if in_code_block:
            pdf.set_font("CJK", size=10)
            write_line(5, f"    {line}")
            pdf.set_font("CJK", size=12)
            continue

        if line.startswith("# "):
            pdf.set_font("CJK", size=18)
            write_line(9, normalize_inline_markdown(line[2:]))
            pdf.ln(1)
            pdf.set_font("CJK", size=12)
            continue
        if line.startswith("## "):
            pdf.set_font("CJK", size=15)
            write_line(8, normalize_inline_markdown(line[3:]))
            pdf.ln(1)
            pdf.set_font("CJK", size=12)
            continue
        if line.startswith("### "):
            pdf.set_font("CJK", size=13)
            write_line(7, normalize_inline_markdown(line[4:]))
            pdf.set_font("CJK", size=12)
            continue

        if line.startswith("- "):
            rendered = normalize_inline_markdown(line[2:])
            write_line(6, f"• {rendered}")
            continue

        if re.match(r"^\d+\.\s+", line):
            write_line(6, normalize_inline_markdown(line))
            continue

        if line.strip() == "---":
            pdf.ln(2)
            continue

        if line.strip() == "":
            pdf.ln(2)
            continue

        write_line(6, normalize_inline_markdown(line))

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(pdf_path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Export markdown file to PDF.")
    parser.add_argument("--input", required=True, help="Input markdown file path")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    parser.add_argument(
        "--font-path",
        default=DEFAULT_FONT,
        help=f"Path to UTF-8 capable font (default: {DEFAULT_FONT})",
    )
    args = parser.parse_args()

    render_markdown_to_pdf(
        markdown_path=Path(args.input),
        pdf_path=Path(args.output),
        font_path=args.font_path,
    )


if __name__ == "__main__":
    main()

