#!/usr/bin/env python3
"""check_scroller_hrefs.py — no two controls in one row may share an href.

Why this exists: the crew-links row once carried six chips that all pointed at
``links.md`` — one destination wearing six labels. On a phone that reads as a broken
row: tapping three different words lands on the same page. Nothing in MkDocs, the link
sweep, or ``build --strict`` catches it, because every href is *valid*.

Scanned containers (the horizontal chip rows and the static button block):

    .pfd-scroller   homepage rows
    .qljump         hub "Jump:" rows
    .qldots         Protocols page static category buttons

A duplicate href inside one of these containers is an exit-1 failure and names the
page, the container and the repeated href.

Usage:  python3 scripts/check_scroller_hrefs.py [site_dir]   (default: site)
Exit 0 = every row is distinct, 1 = a row repeats an href, 2 = no site dir.
"""
from __future__ import annotations

import glob
import os
import re
import sys

CONTAINERS = ("pfd-scroller", "qljump", "qldots")
OPEN = re.compile(r'<div class="([^"]*)">')
HREF = re.compile(r'href="([^"]*)"')


def rows_in(text: str):
    """[(container_name, [href, ...])] — one entry per matching container div."""
    out = []
    for m in OPEN.finditer(text):
        classes = m.group(1).split()
        name = next((c for c in classes if c in CONTAINERS), None)
        if not name:
            continue
        # walk to the matching </div>
        depth, i = 1, m.end()
        while depth and i < len(text):
            nxt_open = text.find("<div", i)
            nxt_close = text.find("</div>", i)
            if nxt_close == -1:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open + 4
            else:
                depth -= 1
                i = nxt_close + 6
        body = text[m.end():i]
        out.append((name, HREF.findall(body)))
    return out


def main() -> int:
    site = sys.argv[1] if len(sys.argv) > 1 else "site"
    if not os.path.isdir(site):
        print(f"no site dir at {os.path.abspath(site)} — run mkdocs build first")
        return 2
    pages = sorted(glob.glob(os.path.join(site, "**", "*.html"), recursive=True))
    bad, checked_rows, checked_links = [], 0, 0
    for page in pages:
        with open(page, encoding="utf-8") as fh:
            text = fh.read()
        if not any(c in text for c in CONTAINERS):
            continue
        for name, hrefs in rows_in(text):
            checked_rows += 1
            checked_links += len(hrefs)
            seen, dupes = set(), []
            for h in hrefs:
                if h in seen and h not in dupes:
                    dupes.append(h)
                seen.add(h)
            if dupes:
                bad.append((os.path.relpath(page, site), name, dupes))
    print(f"scanned {len(pages)} pages · {checked_rows} rows · {checked_links} controls")
    if bad:
        print(f"DUPLICATE HREFS IN {len(bad)} ROW(S):")
        for page, name, dupes in bad:
            print(f"  {page}  .{name}  {dupes}")
        return 1
    print("every row has distinct hrefs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
