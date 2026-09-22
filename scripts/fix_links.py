#!/usr/bin/env python3
"""Repair broken relative Markdown links in a MkDocs docs/ tree.

Why this exists
---------------
Bare links like `[Epinephrine](Epinephrine.md)` resolve relative to the *page*
they appear in, so a protocol at docs/protocols/cardiac/foo.md looks for
docs/protocols/cardiac/Epinephrine.md -- which does not exist. MkDocs only
rewrites a `.md` link to its `.html` output when the source target genuinely
exists at that relative source path; otherwise the raw `Epinephrine.md` href
survives into the built site and 404s.

Resolution order for each broken target:
  1. target already resolves relative to the file        -> leave alone
  2. progressively drop leading path segments until the  -> rewrite to the
     remainder resolves against docs/                      correct relpath
  3. unique file in docs/ with the same basename         -> rewrite to the
                                                           correct relpath
Anything still unresolved is reported and left untouched.

Usage:  python scripts/fix_links.py [--apply]
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.parse
from collections import Counter

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
DOC_EXTS = {".md", ".markdown"}
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")

SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "data:", "javascript:", "tel:")


def build_basename_index(docs_dir: str) -> dict[str, list[str]]:
    idx: dict[str, list[str]] = {}
    for dp, dn, fn in os.walk(docs_dir):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
        for f in fn:
            if os.path.splitext(f)[1].lower() in DOC_EXTS:
                rel = os.path.relpath(os.path.join(dp, f), docs_dir).replace("\\", "/")
                idx.setdefault(f, []).append(rel)
    return idx


def resolve(target: str, file_dir: str, docs_dir: str, idx) -> str | None:
    """Return the correct link target (relative to file_dir) or None."""
    raw = urllib.parse.unquote(target)
    if os.path.isabs(raw):
        return None

    # 1. already correct
    if os.path.exists(os.path.normpath(os.path.join(file_dir, raw))):
        return None

    # 2. strip leading segments, resolve against docs/
    parts = raw.split("/")
    for i in range(1, len(parts)):
        cand = "/".join(parts[i:])
        abs_cand = os.path.normpath(os.path.join(docs_dir, cand))
        if os.path.exists(abs_cand):
            if os.path.splitext(abs_cand)[1].lower() in DOC_EXTS:
                rel = os.path.relpath(abs_cand, file_dir).replace("\\", "/")
                return rel
            return cand

    # 3. unique basename elsewhere in the tree
    base = os.path.basename(raw)
    hits = idx.get(base, [])
    if len(hits) == 1:
        abs_cand = os.path.join(docs_dir, hits[0])
        return os.path.relpath(abs_cand, file_dir).replace("\\", "/")

    return None


def quote_spaces(path: str) -> str:
    return path.replace(" ", "%20")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = ap.parse_args()

    if not os.path.isdir(DOCS_DIR):
        print(f"docs dir not found: {DOCS_DIR}", file=sys.stderr)
        return 1

    idx = build_basename_index(DOCS_DIR)
    fixed_files = 0
    fixed_links = 0
    unresolved = Counter()
    unresolved_examples: dict[str, str] = {}

    for dp, dn, fn in os.walk(DOCS_DIR):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
        for f in fn:
            if os.path.splitext(f)[1].lower() not in DOC_EXTS:
                continue
            path = os.path.join(dp, f)
            file_dir = os.path.dirname(path)
            with open(path, encoding="utf-8") as fh:
                original = fh.read()

            changes = 0

            def sub(m):
                nonlocal changes
                target, title = m.group(1), m.group(2) or ""
                if target.startswith(SKIP_PREFIXES):
                    return m.group(0)
                anchor = ""
                if "#" in target:
                    target, anchor = target.split("#", 1)
                    anchor = "#" + anchor
                if not target:
                    return m.group(0)
                if os.path.exists(os.path.normpath(os.path.join(file_dir, urllib.parse.unquote(target)))):
                    return m.group(0)
                new = resolve(target, file_dir, DOCS_DIR, idx)
                if new is None:
                    unresolved[target] += 1
                    unresolved_examples.setdefault(
                        target, os.path.relpath(path, DOCS_DIR).replace("\\", "/")
                    )
                    return m.group(0)
                changes += 1
                return f"[{m.group(0)[1:m.group(0).index(']')]}]({quote_spaces(new)}{anchor}{title})"

            updated = LINK_RE.sub(sub, original)

            if changes:
                fixed_files += 1
                fixed_links += changes
                rel = os.path.relpath(path, DOCS_DIR).replace("\\", "/")
                print(f"  {changes:4d} link(s)  {rel}")
                if args.apply:
                    with open(path, "w", encoding="utf-8", newline="") as fh:
                        fh.write(updated)

    print()
    print(f"{'APPLIED' if args.apply else 'DRY RUN'}: {fixed_links} link(s) in {fixed_files} file(s)")
    if unresolved:
        print(f"\nStill unresolved ({sum(unresolved.values())} occurrence(s), "
              f"{len(unresolved)} distinct target(s)) -- left untouched:")
        for t, n in unresolved.most_common(25):
            print(f"  {n:4d}  {t}   (first in {unresolved_examples[t]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())