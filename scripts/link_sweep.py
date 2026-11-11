"""link_sweep.py — catch broken internal links that MkDocs validation cannot see.

Why this exists: `on_post_page` hooks (report buttons, quick-reference bars) inject raw HTML
AFTER MkDocs has finished validating links, so a bad href injected by a hook ships silently
and green. That is exactly how 41 broken quick-ref links reached a build on 2026-11-11:
the bar hardcoded `../quick-refs/...` while protocol pages sit two levels deep.

Usage:  python scripts/link_sweep.py [site_dir]
Exit 0 = clean, 1 = broken links found.
"""
import glob
import os
import re
import sys
import urllib.parse

SITE = sys.argv[1] if len(sys.argv) > 1 else "site"
# The site is served from a project subpath, so root-relative hrefs start with this prefix.
PREFIX = "/pfd-resources-and-quick-references/"

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")


def main():
    site_root = os.path.abspath(SITE)
    if not os.path.isdir(site_root):
        print(f"no site dir at {site_root} — run mkdocs build first")
        return 1

    pages = glob.glob(os.path.join(site_root, "**", "*.html"), recursive=True)
    broken = []
    frag_broken = []
    checked = 0
    # built ids per file, for fragment validation. Markdown headings get auto-slugs, but the
    # curated anchors on the homepage door strip are hand-written {#id} and MUST be asserted:
    # a renamed heading otherwise keeps the path check green while jumping to the top of page.
    ids_cache = {}

    def ids_of(path):
        if path not in ids_cache:
            try:
                txt = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                txt = ""
            ids_cache[path] = set(re.findall(r'\bid="([^"]+)"', txt))
        return ids_cache[path]

    for f in pages:
        html = open(f, encoding="utf-8", errors="replace").read()
        base = os.path.dirname(f)
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith("#"):
                if href[1:] and href[1:] not in ids_of(f):
                    frag_broken.append((os.path.relpath(f, site_root), href))
                continue
            if href.startswith(SKIP_SCHEMES):
                continue
            target, _, frag = urllib.parse.unquote(href).partition("#")
            if not target:
                continue
            checked += 1
            if target.startswith(PREFIX):
                path = os.path.normpath(os.path.join(site_root, target[len(PREFIX):]))
            elif target.startswith("/"):
                path = os.path.normpath(os.path.join(site_root, target.lstrip("/")))
            else:
                path = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(path):
                broken.append((os.path.relpath(f, site_root), href))
            elif frag and path.endswith(".html") and frag not in ids_of(path):
                frag_broken.append((os.path.relpath(f, site_root), href))

    print(f"swept {len(pages)} pages, {checked} internal hrefs (+ fragment checks)")
    if broken or frag_broken:
        if broken:
            print(f"BROKEN PATHS: {len(broken)}")
            for page, href in broken[:30]:
                print(f"  {page} -> {href}")
        if frag_broken:
            print(f"BROKEN FRAGMENTS: {len(frag_broken)}")
            for page, href in frag_broken[:30]:
                print(f"  {page} -> {href}")
        return 1
    print("clean — every internal href and #anchor resolves to a built file and a real id")
    return 0


if __name__ == "__main__":
    sys.exit(main())
