#!/usr/bin/env python3
"""Protocol rows must name the FUNCTION "Medical Control" — never a local office
("Poquoson OMD", "Poquoson Medical Control"), never a Medical Director, never a named
individual, and never the local agency's name inside a protocol table row.

This guard is LEVEL-INDEPENDENT (owner ruling 2026-11-15): every protocol table row at
every provider level (EMR / EMT / A / I / P / MC) is checked, not just MC-badged rows.

Two directions, both derived from the docs tree, never hand-listed:

  * every table row (any level) whose action text names the office/person/agency
    -> a violation; `--check` exits 1
  * prose (non-table) lines mentioning the office -> reported, NOT touched (out of scope)

`--write-rows` emits `audit/mc-wording/mc-rows.json`: one record per MC-badged row with
its status derived against the pre-sweep revision, so the MC-row total is
`len(records)`, never a hand-sum.

Usage:
    python3 scripts/mc_wording.py --list          # derive and print the sweep
    python3 scripts/mc_wording.py --check         # exit 1 if ANY protocol row is bad
    python3 scripts/mc_wording.py --write-rows    # write audit/mc-wording/mc-rows.json
    python3 scripts/mc_wording.py --check --root X   # point the guard at another docs tree
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOCS = os.path.join(ROOT, 'docs')
MC_ROWS = os.path.join(ROOT, 'audit', 'mc-wording', 'mc-rows.json')

LV = ['EMR', 'EMT', 'A', 'I', 'P']
HEADER_ANY = re.compile(r'^\|\s*#\s*\|')
SEPARATOR = re.compile(r'^\|[\s:|-]+\|$')
CHIP_RE = re.compile(r'<span class="lvl lvl-([a-z]+)">([A-Z]+)</span>')

# The naming ban. Level-independent: these apply to every row, whatever its badge.
FORBIDDEN = [
    (re.compile(r'\bPoquoson\b', re.I), 'Poquoson'),
    (re.compile(r'\bOMD\b'), 'OMD'),
    (re.compile(r'\bOperational Medical Director\b', re.I), 'Operational Medical Director'),
    (re.compile(r'\bMedical Director\b', re.I), 'Medical Director'),
]
# named individuals: Dr. <Name>, <Name>, MD/DO after a capitalised name
NAMED = re.compile(r'\b(?:Dr\.?|Doctor)\s+[A-Z][a-z]+|\b[A-Z][a-z]+\s*,?\s*(?:MD|DO)\b')

# what a prose (non-table) mention of the office looks like — reported, not edited
OMD_MENTION = re.compile(r'\bOMD\b|\bOperational Medical Director\b|\bMedical Director\b',
                         re.I)


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


# ------------------------------------------------- reading pages print no repo paths
# A provider reading a protocol page has no checkout, so a clinical page may not print a
# repository path or a repository file name (`audit/level-scan/level-rule-ledger.md`,
# `row-bindings.yaml`, `scripts/mc_wording.py`, ...). Provenance belongs in the audit trail,
# which `outstanding-decisions.md` links to on purpose — that generated page and the format
# front matter are the only exemptions.
REPO_PATH = re.compile(r'(?<![\w/.-])(?:audit|scripts|docs|pems_chunks)/[\w./-]+')
REPO_FILE = re.compile(r'(?<![\w/.-])[\w-]+\.(?:ya?ml|json|md)\b')
REPO_PATH_EXEMPT = {'protocols/outstanding-decisions.md'}


def repo_path_hits(text):
    plain = strip_md(text)
    return sorted({m.group(0) for m in REPO_PATH.finditer(plain)}
                  | {m.group(0) for m in REPO_FILE.finditer(plain)})


def walk(docs):
    for base, _dirs, files in os.walk(docs):
        for fn in sorted(files):
            if fn.endswith('.md'):
                yield os.path.relpath(os.path.join(base, fn), docs)


def derive(docs=DEFAULT_DOCS):
    """Every violating table row (any level), every MC row, every prose mention."""
    bad, mc_rows, prose, pages, paths = [], [], [], set(), []
    for rel in walk(docs):
        path = os.path.join(docs, rel)
        text = open(path, encoding='utf-8').read()
        lines = text.split('\n')
        if (rel.startswith('protocols/') and rel not in REPO_PATH_EXEMPT
                and not rel.startswith('protocols/front-matter/')):
            for lineno, line in enumerate(lines, 1):
                hits = repo_path_hits(line)
                if hits:
                    paths.append({'file': rel, 'line': lineno,
                                  'text': line.strip(), 'hits': hits})
        table_lines = set()
        for lineno, row in parse_tables(text):
            table_lines.add(lineno)
            if is_banner(row):
                continue
            hits = forbidden_hits(row['action'])
            # the whole row line is checked too: a chip tooltip or other cell markup is
            # still part of the row the provider reads.
            raw_line = lines[lineno - 1] if lineno - 1 < len(lines) else ''
            for rx, name in FORBIDDEN:
                if name not in hits and rx.search(raw_line):
                    hits.append(name)
            rec = {'file': rel, 'line': lineno, 'row': row['ordinal'],
                   'level': row['level'], 'text': row['action'], 'hits': hits}
            if hits:
                bad.append(rec)
                rec['line_text'] = raw_line
            if row['level'] == 'MC':
                pages.add(rel)
                mc_rows.append(rec)
        for lineno, line in enumerate(lines, 1):
            if lineno in table_lines or line.lstrip().startswith('|'):
                continue
            if OMD_MENTION.search(line):
                prose.append({'file': rel, 'line': lineno, 'text': line.strip()})
    return {'bad': bad, 'mc_rows': mc_rows, 'prose': prose, 'paths': paths,
            'pages': sorted(pages)}


# --------------------------------------------------------------- mc-rows artifact
def base_rev():
    """The revision the MC sweep started from: the parent of the commit that added
    audit/mc-wording/sweep.json. Derived from git, never typed in."""
    try:
        out = subprocess.run(['git', '-C', ROOT, 'log', '--diff-filter=A', '--format=%H',
                              '--', 'audit/mc-wording/sweep.json'],
                             capture_output=True, text=True, check=True).stdout.split()
        return (out[-1] + '^') if out else 'HEAD^'
    except subprocess.CalledProcessError:
        return 'HEAD^'


def base_mc_texts(rev, docs=DEFAULT_DOCS):
    """{file: {ordinal: action}} for MC rows as they read at `rev`."""
    out = {}
    for rel in walk(docs):
        try:
            text = subprocess.run(['git', '-C', ROOT, 'show', f'{rev}:docs/{rel}'],
                                  capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError:
            continue
        for _lineno, row in parse_tables(text):
            if is_banner(row) or row['level'] != 'MC':
                continue
            out.setdefault(rel, {})[str(row['ordinal'])] = row['action']
    return out


def write_rows(docs=DEFAULT_DOCS, rev=None):
    d = derive(docs)
    rev = rev or base_rev()
    before = base_mc_texts(rev)
    records = []
    for rec in d['mc_rows']:
        old = before.get(rec['file'], {}).get(str(rec['row']))
        if old is None:
            status = 'unknown_base'
        elif forbidden_hits(old):
            status = 'rewritten'
        else:
            status = 'already_correct'
        records.append({'file': rec['file'], 'row': rec['row'], 'line': rec['line'],
                        'text': rec['text'], 'status': status,
                        'text_before': old})
    payload = {
        'generated_by': 'scripts/mc_wording.py --write-rows',
        'rule': 'every MC-badged row says "Contact Medical Control"; no MC row names a local '
                'office, a Medical Director, or a named individual',
        'base_rev': rev,
        'total': len(records),
        'pages': len(d['pages']),
        'counts': {s: sum(1 for r in records if r['status'] == s)
                   for s in ('rewritten', 'already_correct', 'unknown_base')},
        'records': records,
    }
    os.makedirs(os.path.dirname(MC_ROWS), exist_ok=True)
    with open(MC_ROWS, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--write-rows', action='store_true')
    ap.add_argument('--base-rev', default=None,
                    help='revision mc-rows.json derives "rewritten" against')
    ap.add_argument('--root', default=DEFAULT_DOCS,
                    help='docs tree to sweep (default: docs/)')
    args = ap.parse_args()

    if args.write_rows:
        p = write_rows(args.root, args.base_rev)
        print(f"wrote {os.path.relpath(MC_ROWS, ROOT)}")
        print(f"total (len(records)) = {p['total']}   pages = {p['pages']}   "
              f"counts = {p['counts']}   base_rev = {p['base_rev']}")
        return 0

    d = derive(args.root)
    if args.json:
        print(json.dumps(d, indent=1, ensure_ascii=False))
        return 0

    if args.check:
        if d['paths']:
            print(f'FAIL — {len(d["paths"])} line(s) on reader-facing protocol pages print a '
                  f'repository path or file name. A provider on scene has no checkout; '
                  f'provenance belongs in the audit trail, not on the page.')
            for p in d['paths']:
                print(f" - {p['file']}:{p['line']}: {', '.join(p['hits'])}")
                print(f"     {p['text'][:160]}")
            return 1
        if d['bad']:
            print(f'FAIL — {len(d["bad"])} protocol table row(s) name a local office, a '
                  f'Medical Director, a named individual, or the local agency instead of the '
                  f'function "Medical Control". Guard is level-independent: every row, '
                  f'every level.')
            for r in d['bad']:
                print(f" - {r['file']}:{r['line']} row {r['row']} [{r['level'] or '-'}]: "
                      f"{strip_md(r['text'])[:160]}")
                print(f"     forbidden: {', '.join(r['hits'])}")
            return 1
        print(f"OK — {len(d['mc_rows'])} MC row(s) on {len(d['pages'])} page(s) plus every other "
              f"protocol table row (all levels): none name OMD / Poquoson / a Medical "
              f"Director / a named individual.")
        print(f"     prose lines still mentioning the office (out of scope, not edited): "
              f"{len(d['prose'])}")
        return 0

    print(f"pages with MC rows: {len(d['pages'])}")
    for p in d['pages']:
        print('  ', p)
    print(f"\nPROTOCOL ROWS violating the naming ban (any level): {len(d['bad'])}")
    for r in d['bad']:
        print(f"  {r['file']}:{r['line']} row {r['row']} level={r['level']}  "
              f"[{', '.join(r['hits'])}]  {strip_md(r['text'])[:130]}")
    print(f"\nMC rows: {len(d['mc_rows'])}")
    print(f"\nPROSE mentions of the office (report only, not touched): {len(d['prose'])}")
    for r in d['prose']:
        print(f"  {r['file']}:{r['line']}  {r['text'][:140]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
