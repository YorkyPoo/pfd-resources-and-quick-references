#!/usr/bin/env python3
"""caption_label_negative.py — prove check_caption_labels.py rule 3 still bites.

Card t_a4b01dd6: the guard gained "no chip may equal its own row's caption".
A guard nobody has seen fail is not evidence. This copies the built homepage into
a throwaway directory, renames the EMS row's first chip back to the caption's own
words, and requires the guard to exit 1 — then restores and requires exit 0.

Nothing in the repo is written: only site/index.html is read.

Usage: python3 audit/gates/caption_label_negative.py [site_dir]
Exit 0 = the planted collision was caught and the clean page passes,
     1 = the guard missed the plant (or the clean page fails), 2 = no site.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SITE = Path(sys.argv[1] if len(sys.argv) > 1 else REPO / "site")
GUARD = REPO / "scripts/check_caption_labels.py"
PLANTS = (
    # (clean label, label the plant rewrites it to, the caption it collides with)
    ("EMS Clinical Hub", "EMS Hub", "EMS Hub"),
    ("Reference shelf", "Fire resources", "Fire resources"),
    ("Station Policies", "City & Personnel Policies", "City & personnel policies"),
)


def guard(site: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(GUARD), str(site)],
                       cwd=str(REPO), capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main() -> int:
    page = SITE / "index.html"
    if not page.is_file():
        print(f"no built homepage at {page} — run mkdocs build first")
        return 2
    clean = page.read_text(encoding="utf-8")

    tmp = Path(tempfile.mkdtemp(prefix="cap_label_negative_"))
    try:
        site = tmp / "site"
        site.mkdir()
        (site / "index.html").write_text(clean, encoding="utf-8")

        rc, _ = guard(site)
        print(f"clean copy                    EXIT={rc}")
        if rc != 0:
            print("  the guard fails a page that has no collision — refusing to call this a proof")
            return 1

        failed = False
        for good_label, bad_label, caption in PLANTS:
            needle = f">{good_label}<"
            if clean.count(needle) != 1:
                print(f"  cannot plant {bad_label!r}: {good_label!r} appears "
                      f"{clean.count(needle)}x in index.html")
                failed = True
                continue
            (site / "index.html").write_text(
                clean.replace(needle, f">{bad_label}<"), encoding="utf-8")
            rc, out = guard(site)
            hit = [ln.strip() for ln in out.splitlines() if "repeats its row caption" in ln]
            print(f"planted {bad_label!r:24} EXIT={rc}  {hit[0] if hit else 'NO MATCH'}")
            if rc != 1 or not hit or caption.lower() not in hit[0].lower():
                failed = True

        (site / "index.html").write_text(clean, encoding="utf-8")
        rc, _ = guard(site)
        print(f"restored                      EXIT={rc}")
        if rc != 0:
            failed = True

        print("CAPTION LABEL NEGATIVE: " + ("FAIL" if failed else "PASS "
              "(3 plants caught, clean page passes)"))
        return 1 if failed else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
