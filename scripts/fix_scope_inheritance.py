# fix_scope_inheritance.py — apply cumulative scope inheritance to protocol matrices
# Rule: on every data row, if a LOWER tier cell has a mark (• or MC) and the next
# higher tier cell is BLANK, copy the mark upward. Tier order: EMR -> EMT -> A -> I -> P.
# Cells that already carry a mark are never touched (intentional grants/limits preserved).
# PENDING OMD RATIFICATION — see Scope_Matrix_Audit_2026-10-30.
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIERS = ['EMR', 'EMT', 'A', 'I', 'P']

def cols(line):
    s = line.strip().strip('|').replace('\\|', '\x00')
    return [c.replace('\x00', '|') for c in s.split('|')]

def has(x):
    return ('\u2022' in x) or re.search(r'\bMC\b', x)

changed_files = {}
for f in sorted((ROOT / 'docs').rglob('*.md')):
    lines = f.read_text().splitlines()
    out, i, nfile = [], 0, 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1]):
            names = [c.strip(' *').upper() for c in cols(ln)]
            if len(names) == 7 and set(TIERS) <= set(names):
                idx = [names.index(t) for t in TIERS]
                j = i + 2
                block = lines[i:j]
                while j < len(lines) and lines[j].startswith('|'):
                    block.append(lines[j]); j += 1
                new_block = [block[0], block[1]]
                for row in block[2:]:
                    cells = cols(row)
                    if len(cells) == 7:
                        for k in range(4):
                            src, dst = cells[idx[k]], cells[idx[k + 1]]
                            if has(src) and not has(dst):
                                cells[idx[k + 1]] = src   # verbatim copy: • or MC condition inherits upward
                                nfile += 1
                        new_block.append('| ' + ' | '.join(c.strip() for c in cells) + ' |')
                    else:
                        new_block.append(row)
                out.extend(new_block)
                i = j
                continue
        out.append(ln); i += 1
    if nfile:
        f.write_text('\n'.join(out) + '\n')
        changed_files[str(f.relative_to(ROOT / 'docs'))] = nfile

total = sum(changed_files.values())
print(f'filled {total} cells across {len(changed_files)} files')
for k, v in sorted(changed_files.items(), key=lambda x: -x[1])[:8]:
    print(f'  {k}: +{v}')
if total:
    Path('/root/.hermes/cache/scratch/scope_fill_log.json').write_text(
        __import__('json').dumps(changed_files, indent=1))
