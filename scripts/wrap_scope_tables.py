# wrap_scope_tables.py — mobile framing for the 70 provider-level scope matrices
# Wraps each standard EMR/EMT/A/I/P markdown table in <div class="sc-wrap" markdown="1">
# so CSS can pin the # + Action columns and squeeze the role columns on phones.
# Idempotent: skips tables already wrapped.
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def cols(line):
    s = line.strip().strip('|').replace('\\|', '\x00')
    return [c.strip().replace('\x00', '|') for c in s.split('|')]

SEP = re.compile(r'^\|[\s:|-]+\|$')
total = 0
for f in sorted((ROOT / 'docs').rglob('*.md')):
    lines = f.read_text(errors='replace').splitlines(keepends=True)
    out, i, touched, in_wrap = [], 0, False, False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('<div class="sc-wrap"'):
            in_wrap = True
        elif ln.startswith('</div>'):
            in_wrap = False
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if not in_wrap and ln.startswith('|') and SEP.match(nxt.strip()):
            names = [c.strip(' *').upper() for c in cols(ln)]
            if len(names) == 7 and {'EMR', 'EMT', 'A', 'I', 'P'} <= set(names):
                # find end of table block
                j = i + 2
                while j < len(lines) and lines[j].startswith('|'):
                    j += 1
                out.append('<div class="sc-wrap" markdown="1">\n\n')
                out.extend(lines[i:j])
                out.append('\n</div>\n')
                touched = True
                total += 1
                i = j
                continue
        out.append(ln)
        i += 1
    if touched:
        txt = ''.join(out)
        txt = re.sub(r'\n{3,}', '\n\n', txt)
        f.write_text(txt)
print(f'wrapped {total} scope tables')
