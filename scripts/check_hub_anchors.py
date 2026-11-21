#!/usr/bin/env python3
"""check_hub_anchors.py — every navigation control must land on something.

Why this exists: the Protocols page carries a static button row (.qldots) and the
other hubs a "Jump:" row (.qljump). Each button is an in-page anchor
(``#pediatric-dosing-reference``) or a link to an anchor on another page
(``../medications.html#advanced-drip-rate-protocol-calculator``). MkDocs rewrites
the URL but never checks the fragment, so a row can point at a heading that was
renamed, moved or never generated: the button renders, looks live, and does
nothing. That is invisible to ``mkdocs build --strict`` (every link is a valid
file) and invisible in review (the source row reads fine); it is obvious to a
medic on a call.

So this gate works on the RENDERED pages, not on the source lists:

  * for ``#frag``            — an element with ``id="frag"`` must exist on the
                               same page;
  * for ``page.html#frag``   — the target page must exist and carry that id.

Every failure names the page, the control label and the missing anchor, and the
process exits 1. A button row that drifts from its own sections therefore fails
the build instead of shipping.

Containers scanned (same set as check_scroller_hrefs.py):

    .qldots         Protocols page static category buttons
    .qljump         hub "Jump:" rows
    .pfd-scroller   homepage rows

Usage:  python3 scripts/check_hub_anchors.py [site_dir]   (default: site)
Exit 0 = every control resolves, 1 = at least one dead anchor, 2 = no site dir.
"""
from __future__ import annotations

import glob
import html as htmllib
import os
import posixpath
import re
import sys

CONTAINERS = ("qldots", "qljump", "pfd-scroller")
DIV_OPEN = re.compile(r'<div class="([^"]*)">')
ANCHOR = re.compile(r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.S)
TAG = re.compile(r"<[^>]+>")
ID = re.compile(r'\bid="([^"]*)"')
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)


def container_bodies(text: str):
    """[(container_name, body_html)] for every scanned container div."""
    out = []
    for m in DIV_OPEN.finditer(text):
        classes = m.group(1).split()
        name = next((c for c in classes if c in CONTAINERS), None)
        if not name:
            continue
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
        out.append((name, text[m.end():i]))
    return out


def label_of(raw: str) -> str:
    txt = htmllib.unescape(TAG.sub(" ", raw))
    return re.sub(r"\s+", " ", txt).strip() or "(unlabelled)"


def main() -> int:
    site = sys.argv[1] if len(sys.argv) > 1 else "site"
    if not os.path.isdir(site):
        print(f"no site dir at {os.path.abspath(site)} — run mkdocs build first")
        return 2

    pages = sorted(glob.glob(os.path.join(site, "**", "*.html"), recursive=True))
    checked_rows = checked_controls = 0
    dead = []  # (page, container, label, href, reason)

    for page in pages:
        with open(page, encoding="utf-8") as fh:
            text = fh.read()
        if not any(c in text for c in CONTAINERS):
            continue
        ids = set(ID.findall(text))
        rel_page = os.path.relpath(page, site)

        for name, body in container_bodies(text):
            checked_rows += 1
            for href, raw in ANCHOR.findall(body):
                if EXTERNAL.match(href):
                    continue
                checked_controls += 1
                label = label_of(raw)
                path, _, frag = href.partition("#")
                if not frag:
                    continue  # plain page link: existence is link_sweep's job
                if not path:  # same-page anchor
                    if frag not in ids:
                        dead.append((rel_page, name, label, href, "no such id on this page"))
                    continue
                # cross-page anchor: resolve the target file inside the site dir
                target = posixpath.normpath(
                    posixpath.join(posixpath.dirname(rel_page.replace(os.sep, "/")), path))
                target_abs = os.path.join(site, target)
                if not os.path.isfile(target_abs):
                    dead.append((rel_page, name, label, href,
                                 f"target page {target} does not exist"))
                    continue
                with open(target_abs, encoding="utf-8") as fh:
                    target_ids = set(ID.findall(fh.read()))
                if frag not in target_ids:
                    dead.append((rel_page, name, label, href,
                                 f"{target} has no id '{frag}'"))

    print(f"scanned {len(pages)} pages · {checked_rows} controls rows · "
          f"{checked_controls} controls")
    if dead:
        print(f"DEAD ANCHORS IN {len(dead)} CONTROL(S):")
        for rel_page, name, label, href, reason in dead:
            print(f"  {rel_page}  .{name}  [{label}] -> {href}  ({reason})")
        return 1
    print("every navigation control resolves to an id that exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
