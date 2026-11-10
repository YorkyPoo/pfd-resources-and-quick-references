#!/usr/bin/env python3
"""wrap_tables.py — deterministic sc-wrap treatment for raw markdown tables.
Wraps every un-wrapped md table in <div class="sc-wrap" markdown="1">…</div>
(5+ col: scope layout; <=4 col: + tw class for prose widths).
Idempotent: skips tables already inside sc/dz/fx wrapper within lookback.
Usage: python3 wrap_tables.py [--dry] [file1 file2 ...]   (no files = all docs)
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY = "--dry" in sys.argv
FILES = [f for f in sys.argv[1:] if not f.startswith("--")]

def blocks(text):
    """yield (start_line_idx, end_line_idx_exclusive, ncols) for md table blocks"""
    lines = text.split("\n")
    i = 0
    out = []
    while i < len(lines):
        if re.match(r"^\s*\|.*\|\s*$", lines[i]) and i+1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i+1]):
            j = i
            while j < len(lines) and re.match(r"^\s*\|.*\|\s*$", lines[j]): j += 1
            back = "\n".join(lines[max(0,i-4):i])
            if not any(w in back for w in ("sc-wrap", "dz-wrap", "fx-wrap")):
                out.append((i, j, lines[i].count("|") - 1))
            i = j
            continue
        i += 1
    return out

def wrap(path, dry=None):
    dry = DRY if dry is None else dry
    text = path.read_text()
    bl = blocks(text)
    if not bl:
        return 0
    lines = text.split("\n")
    # process bottom-up so indices stay valid
    for start, end, cols in sorted(bl, reverse=True):
        cls = "sc-wrap" if cols >= 5 else "sc-wrap tw"
        lines.insert(end, "\n</div>\n")
        lines.insert(start, f'<div class="{cls}" markdown="1">\n')
    new = "\n".join(lines)
    new = re.sub(r"\n{3,}", "\n\n", new)
    if not dry:
        path.write_text(new)
    return len(bl)

def main():
    files = [Path(f) for f in FILES] if FILES else sorted((ROOT/"docs").rglob("*.md"))
    touched = []
    for p in files:
        if p.name == "index.md" and False: continue
        n = wrap(p)
        if n: touched.append((p, n))
    for p, n in touched:
        print(f"{n:2d} block(s): {p.relative_to(ROOT.parent)}")
    print(f"TOTAL files touched: {len(touched)}")

if __name__ == "__main__":
    main()
