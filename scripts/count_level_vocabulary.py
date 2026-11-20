#!/usr/bin/env python3
"""Provider-level vocabulary census across docs/ — read-only, no edits.

Answers the three questions the 2026-11-20 grid-relabel card asks separately,
because they have different answers:

  1. per-row level CHIP labels   (`<span class="lvl lvl-x">LABEL</span>`) — the one
     place where the letters the owner is replacing still print on the page.
  2. full level names in PROSE and TABLE cells, outside any chip span — the
     legend, protocol notes, SOPs, the owner-facing decisions page.
  3. which files mention a full level name at all.

Chips are stripped before pass 2 so a chip's text is never counted twice.

Usage:  python3 scripts/count_level_vocabulary.py [--root DIR]
"""
import argparse
import collections
import os
import re

CHIP = re.compile(r'<span class="lvl lvl-(?:emr|emt|a|i|p)">([^<]*)</span>')
NAMES = {
    'EMR': re.compile(r'\bEMR\b'),
    'EMT': re.compile(r'\bEMT\b'),
    'AEMT': re.compile(r'\bAEMT\b'),
    'Intermediate': re.compile(r'\bIntermediate\b'),
    'Paramedic': re.compile(r'\bParamedic\b'),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()
    docs = os.path.join(args.root, 'docs')

    chip_dir = collections.Counter()
    chip_label = collections.Counter()
    prose_tok = collections.Counter()
    prose_file = collections.defaultdict(collections.Counter)

    for root, dirs, names in os.walk(docs):
        dirs[:] = sorted(d for d in dirs if d != '.git')
        for n in sorted(names):
            if not n.endswith('.md'):
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, docs).replace(os.sep, '/')
            parts = rel.split('/')
            bucket = '/'.join(parts[:2]) if len(parts) > 2 else ('/'.join(parts[:-1]) or '(root)')
            text = open(p, encoding='utf-8').read()
            for m in CHIP.finditer(text):
                chip_dir[bucket] += 1
                chip_label[m.group(1)] += 1
            stripped = CHIP.sub('', text)
            for name, rx in NAMES.items():
                c = len(rx.findall(stripped))
                if c:
                    prose_tok[name] += c
                    prose_file[bucket][rel] += c

    print('=== 1. per-row chip labels ===')
    for lab, c in sorted(chip_label.items(), key=lambda kv: -kv[1]):
        print(f'  {lab:5s} {c}')
    print(f'  TOTAL {sum(chip_label.values())} chip(s) in {len(chip_dir)} director(ies)')

    print('\n=== 2. full level names in prose/table cells (chips excluded) ===')
    for name, c in sorted(prose_tok.items(), key=lambda kv: -kv[1]):
        print(f'  {name:12s} {c}')
    print(f'  TOTAL {sum(prose_tok.values())}')
    print()
    for bucket in sorted(prose_file):
        print(f'  [{bucket}] {sum(prose_file[bucket].values())}')
        for rel, c in sorted(prose_file[bucket].items()):
            print(f'      {c:5d}  {rel}')

    allf = sorted({rel for b in prose_file for rel in prose_file[b]})
    print(f'\n=== 3. {len(allf)} file(s) mention a full level name ===')


if __name__ == '__main__':
    main()
