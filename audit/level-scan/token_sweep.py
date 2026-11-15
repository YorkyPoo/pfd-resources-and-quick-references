"""Independent sweep for provider-level words left inside action text.

Deliberately wider than scripts/level_rule.py's TEXT_TOKEN (which only sees
"LEVEL:" prefixes the stripper itself recorded). Run from the repo root:

    python3 audit/level-scan/token_sweep.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
os.chdir(ROOT)
import level_rule as L  # noqa: E402

WORD = re.compile(r'\b(?:EMR|EMT|AEMT|Paramedic|Intermediate)\b', re.I)
PAREN = re.compile(r'\([^)]*\b(?:A|I|P)\b[^)]*\)')
PAIR = re.compile(r'(?<![A-Za-z0-9])(?:A|I|P|EMR|EMT)\s*/\s*(?:A|I|P|EMR|EMT)(?![A-Za-z0-9])')
DASHOR = re.compile(r'(?<![A-Za-z0-9])(?:EMR|EMT|A|I|P)\s*(?:-|or)\s*(?:A|I|P)(?![A-Za-z0-9])')


def hits(text):
    out = []
    for rx in (WORD, PAREN, PAIR, DASHOR):
        out += [(m.group(0), rx.pattern) for m in rx.finditer(text)]
    return out


def main():
    total = 0
    pages = 0
    for rel in L.TARGETS + L.PENDING_TARGETS:
        rows = L.parse_page(os.path.join(L.DOCS, rel))
        page_hits = 0
        for r in rows:
            h = hits(r['action'])
            if h:
                page_hits += len(h)
                print(f"{os.path.basename(rel)} row {r['ordinal']}: "
                      f"{[x[0] for x in h]}")
        if page_hits:
            pages += 1
        total += page_hits
    print(f"\nTOTAL: {total} hit(s) on {pages} page(s) "
          f"out of {len(L.TARGETS) + len(L.PENDING_TARGETS)} pages")
    return 0


if __name__ == '__main__':
    sys.exit(main())
