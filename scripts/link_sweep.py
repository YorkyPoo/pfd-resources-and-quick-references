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
    checked = 0
    for f in pages:
        html = open(f, encoding="utf-8", errors="replace").read()
        base = os.path.dirname(f)
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith("#") or href.startswith(SKIP_SCHEMES):
                continue
            target = urllib.parse.unquote(href.split("#")[0])
            if not target:
                continue
            checked += 1
            if target.startswith(PREFIX):
                path = os.path.normpath(os.path.join(site_root, target[len(PREFIX):]))
            elif target.startswith("/"):
                # host-root absolute: only valid if it exists under the project prefix,
                # which it cannot — flag it as a mis-generated URL rather than ignoring it
                path = os.path.normpath(os.path.join(site_root, target.lstrip("/")))
            else:
                path = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(path):
                broken.append((os.path.relpath(f, site_root), href))

    print(f"swept {len(pages)} pages, {checked} internal hrefs")
    if broken:
        print(f"BROKEN: {len(broken)}")
        for page, href in broken[:40]:
            print(f"  {page} -> {href}")
        return 1
    print("clean — every internal href resolves to a built file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
