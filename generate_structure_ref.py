#!/usr/bin/env python3
"""Generate a structure_reference.toml from a PDF's table of contents.

Usage:
    python3 generate_structure_ref.py --pdf <file.pdf> --out <output.toml>

The output file lists every chapter, section, and subsection found in the
PDF TOC.  It is consumed by build_book.py as an authoritative structural
reference: numbering and section existence override whatever the DOCX
parser detects, while titles are used only for soft matching (PDF text
extraction is unreliable).
"""

import argparse
import re
import sys


def extract_toc_pages(doc):
    """Find pages that contain TOC-like content (many numbered entries with dot leaders)."""
    toc_pages = []
    for pg_num in range(min(40, len(doc))):
        page = doc[pg_num]
        text = page.get_text()
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        toc_like = [l for l in lines if re.match(r"^\d+\.\d+", l) and "..." in l]
        if len(toc_like) >= 3:
            toc_pages.append(pg_num)
    return toc_pages


def extract_entries(doc, toc_pages):
    """Extract structured TOC entries from the identified TOC pages."""
    entries = []
    seen = set()

    for pg_num in toc_pages:
        page = doc[pg_num]
        text = page.get_text()
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            cleaned = re.sub(r"\s*\.{2,}\s*\d*\s*$", "", line).strip()

            # Subsection N.X.Y
            m = re.match(r"^(\d+)\.\s*(\d+)\.\s*(\d+)\s+(.*)", cleaned)
            if m:
                ch, sec, sub = int(m.group(1)), int(m.group(2)), int(m.group(3))
                title = m.group(4).strip()
                key = (ch, sec, sub)
                if key not in seen:
                    seen.add(key)
                    entries.append({
                        "type": "subsection",
                        "chapter": ch, "section": sec, "subsection": sub,
                        "title": title,
                    })
                continue

            # Chapter N.0
            m = re.match(r"^(\d+)\.\s*0\s+(.*)", cleaned)
            if m:
                ch = int(m.group(1))
                title = m.group(2).strip()
                key = (ch, 0, None)
                if key not in seen:
                    seen.add(key)
                    entries.append({
                        "type": "chapter",
                        "chapter": ch, "section": 0, "subsection": None,
                        "title": title,
                    })
                continue

            # Section N.X (X > 0)
            m = re.match(r"^(\d+)\.\s*(\d+)\s+(.*)", cleaned)
            if m and int(m.group(2)) > 0:
                ch, sec = int(m.group(1)), int(m.group(2))
                title = m.group(3).strip()
                key = (ch, sec, None)
                if key not in seen:
                    seen.add(key)
                    entries.append({
                        "type": "section",
                        "chapter": ch, "section": sec, "subsection": None,
                        "title": title,
                    })

    return entries


def format_toml(entries, pdf_path):
    """Format entries as TOML."""
    lines = []
    lines.append("# Structure reference extracted from PDF table of contents")
    lines.append(f"# Source: {pdf_path}")
    lines.append("#")
    lines.append("# This file is authoritative for STRUCTURE (which sections exist,")
    lines.append("# their numbering and hierarchy).  Titles are for soft matching")
    lines.append("# only — PDF text extraction introduces artifacts.")
    lines.append("#")
    lines.append("# Used by build_book.py when present in lang-store/<lang>/.")
    lines.append("")

    chapters = sorted(set(e["chapter"] for e in entries))
    lines.append(f"# {len(entries)} entries across {len(chapters)} chapters")
    lines.append("")

    current_chapter = None
    for e in entries:
        if e["chapter"] != current_chapter:
            current_chapter = e["chapter"]
            lines.append("")

        lines.append("[[entry]]")
        if e["subsection"] is not None:
            lines.append(f'num = "{e["chapter"]}.{e["section"]}.{e["subsection"]}"')
        elif e["section"] == 0:
            lines.append(f'num = "{e["chapter"]}.0"')
        else:
            lines.append(f'num = "{e["chapter"]}.{e["section"]}"')
        lines.append(f'type = "{e["type"]}"')
        # Escape quotes in title for TOML
        safe_title = e["title"].replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'title = "{safe_title}"')

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Generate structure_reference.toml from a PDF's table of contents"
    )
    parser.add_argument("--pdf", required=True, help="Input PDF file")
    parser.add_argument("--out", required=True, help="Output TOML file path")
    args = parser.parse_args()

    try:
        import fitz
    except ImportError:
        print("Error: PyMuPDF (fitz) is required. Install with: pip install pymupdf")
        sys.exit(1)

    print(f"Opening {args.pdf}...")
    doc = fitz.open(args.pdf)
    print(f"  {len(doc)} pages")

    print("Scanning for TOC pages...")
    toc_pages = extract_toc_pages(doc)
    if not toc_pages:
        print("Error: no TOC found in PDF")
        sys.exit(1)
    print(f"  TOC on pages {[p + 1 for p in toc_pages]}")

    print("Extracting entries...")
    entries = extract_entries(doc, toc_pages)
    chapters = sorted(set(e["chapter"] for e in entries))
    sections = [e for e in entries if e["type"] == "section"]
    subsections = [e for e in entries if e["type"] == "subsection"]
    print(f"  {len(entries)} entries: {len(chapters)} chapters, "
          f"{len(sections)} sections, {len(subsections)} subsections")

    toml_content = format_toml(entries, args.pdf)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(toml_content)
    print(f"✓ Written to {args.out}")


if __name__ == "__main__":
    main()
