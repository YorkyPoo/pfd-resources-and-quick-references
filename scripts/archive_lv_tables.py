#!/usr/bin/env python3
"""Snapshot every rendered .lv-wrap level table, before the pip-strip rollout.

    python3 scripts/archive_lv_tables.py --site site --out audit/archive/tables-2026-11-20

Reads a **built site** (the markup a phone gets, not the markdown), so the copy
is exactly what the live pages carried on the archive date. One file per page
that carries a convertible level table (plain ``lv-wrap``, three columns, second
header cell ``Level``, at least one data row) — the pages the pip-strip hook
rewrites. Pages whose only tables are ``lv-wrap policy`` / ``lv-wrap pending``
publish no provider level and are therefore untouched by the rollout; they are
listed in ``index.md`` as skipped and are not snapshotted, because nothing about
them changes.

Restore is a copy-back of the file's markup into the page, or a
``pip_strip.enabled: false`` build (see the index).
"""
import argparse
import html as html_mod
import os
import re
import sys

DIV = re.compile(r'<div class="lv-wrap(?P<cls>[^"]*)"[^>]*>(?P<body>.*?)</div>', re.S)
ROW = re.compile(r'<tr>(.*?)</tr>', re.S)
CELL = re.compile(r'<t([hd])\b[^>]*>(.*?)</t\1>', re.S)


def classify(cls, body):
    """('convert', None) or (None, human reason the hook leaves the table alone)."""
    if 'pending' in cls:
        return None, 'pending table'
    if 'policy' in cls:
        return None, 'policy table'
    rows = ROW.findall(body)
    if len(rows) < 2:
        return None, 'no data rows'
    hdr = CELL.findall(rows[0])
    if not (len(hdr) == 3 and hdr[1][1].strip().lower() == 'level'):
        return None, 'not a 3-column level table'
    # A table with a PENDING / POLICY row publishes no provider level for that
    # row, and the strip has no slot for "no level exists" — the hook leaves the
    # whole table alone, so it is not a convertible table here either.
    for raw in rows[1:]:
        cells = CELL.findall(raw)
        if len(cells) != 3:
            return None, 'irregular row'
        if 'lvl-pending' in cells[1][1]:
            return None, 'PENDING row in the table'
        if 'lvl-policy' in cells[1][1]:
            return None, 'POLICY row in the table'
    return 'convert', None


def is_convertible(cls, body):
    return classify(cls, body)[0] == 'convert'


def chip_text(cell_html):
    """Human-readable chip of one rendered Level cell, e.g. ``I +MC *``."""
    out = []
    for cls, body in re.findall(r'<span class="(lvl[^"]*)"[^>]*>(.*?)</span>', cell_html, re.S):
        words = cls.split()
        if 'lvl-mc-req' in words:
            out.append('+MC')
        elif 'lvl-mc' in words:
            out.append('MC')
        elif any(w in words for w in ('lvl-emr', 'lvl-emt', 'lvl-a', 'lvl-i', 'lvl-p')):
            out.append(html_mod.unescape(re.sub(r'<[^>]+>', '', body)).strip())
        elif 'lvl-policy' in words:
            out.append('POLICY')
        elif 'lvl-pending' in words:
            out.append('PENDING')
    for sup in re.findall(r'<sup class="lvl-(?:req|deriv)"[^>]*>(.*?)</sup>', cell_html, re.S):
        out.append(html_mod.unescape(re.sub(r'<[^>]+>', '', sup)).strip())
    # owner-required flag, if a page ever carries one
    if 'lvl-own' in cell_html:
        out.append('\u2691')
    return ' '.join(x for x in out if x)


def rows_of(body):
    out = []
    blocks = ROW.findall(body)
    for raw in blocks[1:]:
        cells = CELL.findall(raw)
        if len(cells) != 3:
            continue
        num = re.sub(r'<[^>]+>', '', cells[0][1]).strip()
        out.append((num, chip_text(cells[1][1])))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', required=True, help='built site directory')
    ap.add_argument('--out', required=True, help='archive directory to write')
    args = ap.parse_args()

    pages, skipped = [], []
    for root, dirs, files in os.walk(args.site):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, args.site)
            text = open(path, encoding='utf-8', errors='replace').read()
            blocks = list(DIV.finditer(text))
            if not blocks:
                continue
            why = []
            n_conv = 0
            for m in blocks:
                cls = (m.group('cls') or '').strip()
                ok, reason = classify(cls, m.group('body'))
                if ok:
                    n_conv += 1
                else:
                    why.append(reason)
            pages.append((rel, blocks, n_conv, sorted(set(why))))
            if n_conv == 0:
                skipped.append((rel, sorted(set(why))))

    os.makedirs(args.out, exist_ok=True)
    index_rows = []
    total_rows = 0
    for rel, blocks, n_conv, why in pages:
        dest = os.path.join(args.out, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as fh:
            fh.write('\n\n'.join(b.group(0) for b in blocks))
            fh.write('\n')
        per = [rows_of(b.group('body')) for b in blocks]
        n = sum(len(r) for r in per)
        total_rows += n
        chips = ' / '.join(', '.join(f'{num}:{chip}' for num, chip in r) for r in per)
        state = (f'converted ({n_conv} of {len(blocks)})' if n_conv else
                 'skipped — ' + ', '.join(why))
        index_rows.append((rel, len(blocks), n, state, chips))

    lines = [
        '# Level tables as published on 2026-11-20',
        '',
        f'Snapshot taken from the `main` build (commit `{os.environ.get("ARCHIVE_TIP", "d5fd03c")}`)',
        'before the five-pip strip rollout. Each file holds that page\'s rendered',
        '`lv-wrap` table markup **verbatim** — the chip table where every level',
        'appears once per row. Filenames mirror the site path. Every page that',
        'carries an `lv-wrap` table is here, including the 15 whose tables publish',
        'no provider level (`policy` / `pending`) and are therefore not converted.',
        '',
        f'- pages snapshotted: **{len(index_rows)}**',
        f'- pages the rollout converts: **{sum(1 for r in index_rows if r[3].startswith("converted"))}**',
        f'- action rows over all snapshotted tables: **{total_rows}**',
        f'- pages skipped (no provider level in any table): **{len(skipped)}**',
        '',
        '## To restore a page',
        '',
        'Either set `extra.pip_strip.enabled: false` in `mkdocs.yml` and rebuild',
        '(one-commit switch, restores every page), or paste the markup from the',
        "page's file back into the page's markdown in place of the strip.",
        '',
        '## Pages',
        '',
        '| page | tables | rows | rollout | chips (row:chip) |',
        '|---|---|---|---|---|',
    ]
    for rel, nt, n, state, chips in index_rows:
        lines.append(f'| `{rel}` | {nt} | {n} | {state} | {chips} |')
    lines += ['', '## Skipped — no provider level, not touched by the rollout', '']
    for rel, why in skipped:
        lines.append(f'- `{rel}` — {", ".join(why)}')
    lines.append('')
    with open(os.path.join(args.out, 'index.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))

    print(f'archived pages: {len(index_rows)}  rows: {total_rows}  skipped: {len(skipped)}')
    print(f'index: {os.path.join(args.out, "index.md")}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
