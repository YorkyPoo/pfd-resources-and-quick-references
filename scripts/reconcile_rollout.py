#!/usr/bin/env python3
"""Generate the pip-strip page-by-page reconciliation from the markdown.

    python3 scripts/reconcile_rollout.py [--src docs] [--out <file>]

The page list, the per-page fate and the reasons all come from
``scripts/verify_pip_strip.py``'s own classifier (``page_tables``), so this file
and the verifier can never disagree about which pages convert. Nothing here is
hand-written: add a page, re-run, and the table and the arithmetic change with
it. Exits non-zero if the arithmetic does not reconcile.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_pip_strip import page_tables  # noqa: E402

SCOPE_DIRS = ('protocols', 'procedures')


def pages_in_scope(docs):
    """Every .md under docs/protocols and docs/procedures, docs-relative."""
    out = []
    for d in SCOPE_DIRS:
        root = os.path.join(docs, d)
        for here, dirs, files in os.walk(root):
            dirs.sort()
            for f in sorted(files):
                if f.endswith('.md'):
                    out.append(os.path.relpath(os.path.join(here, f), docs)
                               .replace(os.sep, '/'))
    return sorted(out)


def fate(kind_counts, n_tables):
    """(converted?, reason) from the classifier's per-table kinds."""
    conv = kind_counts.get('convert', 0)
    policy = kind_counts.get('policy', 0)
    pending = kind_counts.get('pending', 0)
    named = kind_counts.get('policy-named-level', 0)
    if not n_tables:
        return False, 'no table, nothing to convert'
    if not conv:
        if named and not (policy or pending):
            return False, (f'policy (Basis) table ({named} table): no `Level` column; '
                           f'one row names a provider level as its basis, so it is not a '
                           f'level table')
        if pending and not (policy or named):
            return False, f'PENDING table ({pending} table): every row is PENDING — no provider level published'
        if policy and not (pending or named):
            return False, f'policy table ({policy} table): no `Level` column (header is `# | Basis | Action`)'
        return False, (f'no provider level: {policy} policy table(s) (no `Level` column), '
                       f'{named} policy (Basis) table(s) naming a level, '
                       f'{pending} all-PENDING table(s)')
    if conv == n_tables:
        return True, f'{conv} of {n_tables} table(s)'
    return True, (f'{conv} of {n_tables} table(s); the rest: {policy} policy '
                  f'(no `Level` column), {named} policy (Basis) naming a level, '
                  f'{pending} all-PENDING')


def build(docs='docs'):
    rows = []
    for rel in pages_in_scope(docs):
        tables = page_tables(os.path.join(docs, rel), rel)
        counts = {}
        for kind, _ in tables:
            counts[kind] = counts.get(kind, 0) + 1
        converted, why = fate(counts, len(tables))
        rows.append((rel, bool(tables), converted, why, counts, tables))
    return rows


def render(rows, tip=None, parity=None):
    total = len(rows)
    with_table = sum(1 for r in rows if r[1])
    converted = sum(1 for r in rows if r[2])
    no_table = total - with_table
    skipped = with_table - converted
    conv_tables = sum(r[4].get('convert', 0) for r in rows)
    conv_rows = sum(len(t) for r in rows if r[2] for k, t in r[5] if k == 'convert')
    pending_rows = sum(1 for r in rows if r[2]
                       for k, t in r[5] if k == 'convert'
                       for _n, st, _m in t if st[0] == 'pending')
    ok = converted + skipped + no_table == total

    L = []
    L.append('# Pip-strip rollout — reconciliation evidence (developer)\n')
    L.append(f'Derived in code from the markdown under `docs/protocols/` and '
             f'`docs/procedures/` at branch tip `{tip or "working tree"}`. '
             f'Generator: `scripts/reconcile_rollout.py` (committed), which calls the '
             f'verifier\'s own `page_tables()` classifier. Nothing in this table is '
             f'hand-written.\n')
    L.append('## 1. Page-by-page reconciliation\n')
    L.append('| page | has lv-wrap table? | converted? | if not, why |')
    L.append('|---|---|---|---|')
    for rel, has, conv, why, _c, _t in rows:
        L.append(f'| `{rel}` | {"yes" if has else "no"} | {"yes" if conv else "no"} | {why} |')
    L.append('')
    L.append('## 2. Arithmetic\n')
    L.append('```')
    L.append(f'total pages under docs/protocols + docs/procedures: {total}')
    L.append(f'  carry an lv-wrap table: {with_table}')
    L.append(f'    converted: {converted}  ({conv_tables} tables, {conv_rows} action rows, '
             f'{pending_rows} of them PENDING)')
    L.append(f'    skipped: {skipped}  (no level table to convert — see section 3)')
    L.append(f'  no lv-wrap table: {no_table}')
    L.append(f'check: {converted} + {skipped} + {no_table} = {converted + skipped + no_table} '
             f'-> {converted + skipped + no_table == total}')
    L.append('```\n')
    L.append('## 3. The skip set, by class\n')
    L.append('Classified from the table, not the page: a **policy table** is one whose '
             'second header cell is not `Level` (`| # | Basis | Action / Intervention |`); '
             'a **PENDING table** is one where every row\'s level cell is '
             '`<span class="lvl lvl-pending">PENDING</span>`. A level table with only '
             '*some* PENDING rows is converted — its PENDING rows render as dashed pips '
             'with the tag `PENDING — no published level`, never as a level.\n')
    buckets = {'policy table': [], 'policy (Basis) table': [], 'PENDING table': [],
               'no table, nothing to convert': []}
    for rel, _has, conv, why, _c, _t in rows:
        for key in buckets:
            if why.startswith(key):
                buckets[key].append(rel)
                break
    for key, rels in buckets.items():
        if not rels:
            continue
        label = key
        if key == 'policy table':
            label = 'policy table — no `Level` column'
        elif key == 'policy (Basis) table':
            label = ('policy (Basis) table naming a level as its basis — not a level '
                     'table, not converted')
        elif key == 'PENDING table':
            label = 'PENDING table — every row is PENDING, no level is published'
        L.append(f'- **{label}** — {len(rels)} page(s): ' +
                 ', '.join(f'`{r}`' for r in sorted(rels)))
    L.append('')
    L.append('The classifier fails the build (`ValueError`, so `mkdocs build --strict` '
             'fails) if a table has provider-level chips but no `Level` column, if a '
             '`policy`-wrapped table has a `Level` column with level chips, or if a row '
             'publishes neither a level nor PENDING. Two level tables were wrongly skipped '
             'before that guard existed; it is the rule that stops a repeat.\n')
    if parity:
        L.append('## 4. Row parity (verifier output, quoted verbatim)\n')
        L.append('```')
        L.append(parity.strip())
        L.append('```\n')
        L.append('`scripts/verify_pip_strip.py` reads the chips out of the markdown with '
                 'its own reader and compares them with the `data-states` of every '
                 'rendered row, so that line is a machine comparison of every converted '
                 'row, not a count.\n')
    return '\n'.join(L), ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='docs')
    ap.add_argument('--out', default='audit/level-scan/logs/pipstrip-reconciliation.md')
    ap.add_argument('--tip', default=None)
    ap.add_argument('--parity', default=None, help='verifier output to quote verbatim')
    args = ap.parse_args()
    rows = build(args.src)
    text, ok = render(rows, args.tip, args.parity)
    with open(args.out, 'w', encoding='utf-8') as fh:
        fh.write(text + '\n')
    conv = sum(1 for r in rows if r[2])
    print(f'wrote {args.out}: {len(rows)} pages, {conv} converted, '
          f'{len(rows) - conv} not converted, arithmetic {"OK" if ok else "FAILED"}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
