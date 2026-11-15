#!/usr/bin/env python3
"""MC row wording: the level chip says MC, so the action text must name the function
"Medical Control" — never a local office ("Poquoson OMD", "Poquoson Medical Control")
and never a named individual.

Two directions are derived from the docs tree, never hand-listed:

  * MC rows whose text contains a forbidden token  -> must be fixed
  * non-MC rows whose text mentions the OMD        -> reported, NOT touched (owner decides)
  * prose (non-table) lines mentioning the OMD     -> reported separately, NOT touched

Usage:
    python3 scripts/mc_wording.py --list          # derive and print the sweep
    python3 scripts/mc_wording.py --check         # exit 1 if any MC row is bad
    python3 scripts/mc_wording.py --check --root X   # point the guard at another docs tree
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOCS = os.path.join(ROOT, 'docs')

LV = ['EMR', 'EMT', 'A', 'I', 'P']
OLD_HEADER = re.compile(r'^\|\s*#\s*\|\s*Action\s*/\s*Intervention\s*\|\s*EMR\s*\|', re.M)
NEW_HEADER = re.compile(r'^\|\s*#\s*\|\s*Level\s*\|\s*Action\s*/\s*Intervention\s*\|', re.M)
HEADER_ANY = re.compile(r'^\|\s*#\s*\|')
SEPARATOR = re.compile(r'^\|[\s:|-]+\|$')
CHIP_RE = re.compile(r'<span class="lvl lvl-([a-z]+)">([A-Z]+)</span>')

# the naming ban for MC rows
FORBIDDEN = [
    (re.compile(r'\bPoquoson\b', re.I), 'Poquoson'),
    (re.compile(r'\bOMD\b'), 'OMD'),
    (re.compile(r'\bOperational Medical Director\b', re.I), 'Operational Medical Director'),
    (re.compile(r'\bMedical Director\b', re.I), 'Medical Director'),
]
# named individuals: Dr. <Name>, <Name>, MD/DO after a capitalised name
NAMED = re.compile(r'\b(?:Dr\.?|Doctor)\s+[A-Z][a-z]+|\b[A-Z][a-z]+\s*,?\s*(?:MD|DO)\b')

# what a non-MC OMD mention looks like (reported, not edited)
OMD_MENTION = re.compile(r'\bOMD\b|\bOperational Medical Director\b|\bMedical Director\b',
                         re.I)
OMD_ROW = re.compile(r'\bOMD\b|\bOperational Medical Director\b|\bMedical Director\b|'
                     r'\bPoquoson Medical Control\b', re.I)


def split_cells(line):
    return [p.strip() for p in line.strip().strip('|').split('|')]


def parse_tables(text):
    """Yield (line_no, row_dict) for every table row in either table format."""
    fmt = None
    for i, line in enumerate(text.split('\n'), 1):
        if HEADER_ANY.match(line):
            if '| Level |' in line:
                fmt = 'new'
            elif '| EMR |' in line:
                fmt = 'old'
            else:
                fmt = None
            continue
        if fmt is None:
            continue
        if not line.strip().startswith('|'):
            fmt = None
            continue
        if SEPARATOR.match(line):
            continue
        cells = split_cells(line)
        if fmt == 'new':
            if len(cells) < 3:
                continue
            chips = CHIP_RE.findall(cells[1])
            level = chips[0][1] if chips else None
            yield i, {'lineno': i, 'ordinal': cells[0], 'level': level,
                      'action': cells[2], 'cells': None}
        else:
            if len(cells) < 7:
                continue
            marks = [c.strip() for c in cells[2:7]]
            filled = [t for t in marks if t]
            if filled and all(re.fullmatch(r'MC', t.strip('[] ').upper()) for t in filled):
                level = 'MC'
            elif filled:
                level = LV[marks.index(filled[0])] if marks.index(filled[0]) < len(LV) else None
            else:
                level = None
            yield i, {'lineno': i, 'ordinal': cells[0], 'level': level,
                      'action': cells[1], 'cells': marks}


def is_banner(row):
    if row['cells'] is None:
        return False
    t = row['action'].strip()
    return t.startswith('**') and t.endswith('**') and not any(c.strip() for c in row['cells'])


def strip_md(text):
    text = re.sub(r'<br\s*/?>', ' / ', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    return re.sub(r'[*_`]', '', text)


def forbidden_hits(text):
    plain = strip_md(text)
    hits = []
    for rx, name in FORBIDDEN:
        if rx.search(plain):
            hits.append(name)
    m = NAMED.search(plain)
    if m:
        hits.append('named individual: ' + m.group(0))
    return hits


def walk(docs):
    for base, _dirs, files in os.walk(docs):
        for fn in sorted(files):
            if fn.endswith('.md'):
                yield os.path.relpath(os.path.join(base, fn), docs)


def derive(docs=DEFAULT_DOCS):
    mc_bad, mc_ok, non_mc_omd, prose_omd, pages = [], [], [], [], set()
    for rel in walk(docs):
        path = os.path.join(docs, rel)
        text = open(path, encoding='utf-8').read()
        lines = text.split('\n')
        table_lines = set()
        for lineno, row in parse_tables(text):
            table_lines.add(lineno)
            if is_banner(row):
                continue
            hits = forbidden_hits(row['action'])
            if row['level'] == 'MC':
                pages.add(rel)
                rec = {'file': rel, 'line': lineno, 'row': row['ordinal'],
                       'text': row['action'], 'hits': hits}
                (mc_bad if hits else mc_ok).append(rec)
            elif OMD_ROW.search(strip_md(row['action'])):
                non_mc_omd.append({'file': rel, 'line': lineno, 'row': row['ordinal'],
                                   'level': row['level'], 'text': row['action'],
                                   'hits': sorted({m.group(0) for m in OMD_ROW.finditer(strip_md(row['action']))})})
        for lineno, line in enumerate(lines, 1):
            if lineno in table_lines or line.lstrip().startswith('|'):
                continue
            if OMD_MENTION.search(line):
                prose_omd.append({'file': rel, 'line': lineno, 'text': line.strip()})
    return {'mc_bad': mc_bad, 'mc_ok': mc_ok, 'non_mc_omd': non_mc_omd,
            'prose_omd': prose_omd, 'pages': sorted(pages)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--root', default=DEFAULT_DOCS,
                    help='docs tree to sweep (default: docs/)')
    args = ap.parse_args()
    d = derive(args.root)
    if args.json:
        print(json.dumps(d, indent=1))
        return 0
    if args.list or not args.check:
        print(f"pages with MC rows: {len(d['pages'])}")
        for p in d['pages']:
            print('  ', p)
        print(f"\nMC rows bad: {len(d['mc_bad'])}")
        for r in d['mc_bad']:
            print(f"  {r['file']}:{r['line']} row {r['row']}  [{', '.join(r['hits'])}]  {strip_md(r['text'])}")
        print(f"\nMC rows already naming only Medical Control: {len(d['mc_ok'])}")
        for r in d['mc_ok']:
            print(f"  {r['file']}:{r['line']} row {r['row']}  {strip_md(r['text'])[:120]}")
        print(f"\nNON-MC rows mentioning the OMD (report only, not touched): {len(d['non_mc_omd'])}")
        for r in d['non_mc_omd']:
            print(f"  {r['file']}:{r['line']} row {r['row']} level={r['level']}  {strip_md(r['text'])[:140]}")
        print(f"\nPROSE mentions of the OMD (report only, not touched): {len(d['prose_omd'])}")
        for r in d['prose_omd']:
            print(f"  {r['file']}:{r['line']}  {r['text'][:140]}")
        return 0
    fails = d['mc_bad']
    if fails:
        print(f'FAIL — {len(fails)} MC-badged row(s) name a local office or person instead of '
              f'"Medical Control":')
        for r in fails:
            print(f" - {r['file']}:{r['line']} row {r['row']}: {strip_md(r['text'])[:160]}")
            print(f"     forbidden: {', '.join(r['hits'])}")
        return 1
    print(f'OK — {len(d["mc_ok"])} MC-badged row(s) across {len(d["pages"])} page(s), none name '
          f'OMD / Poquoson / a named individual.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
