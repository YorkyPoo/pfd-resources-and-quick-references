#!/usr/bin/env python3
"""tidy_pass2.py — OCR-garble cleanup after tidy_sops (2026-11-09 live-phone audit).
1. sop-meta cards: **bold** -> <strong> (markdown is inert inside raw divs).
2. Roman-numeral OCR garbles: Ill->III, lV->IV, VI-> Vl variants; then re-run heading promotion.
3. Strip PDF running footers/headers (Page N 0f M, category+page lines, 'P r <SOP#>' remnants).
4. Stray 'e ' bullet glyphs (OCR'd bullets) -> markdown list items.
Idempotent.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = [ROOT / "docs" / "sops", ROOT / "docs" / "personnel-policies"]

FOOTER = re.compile(r"^\s*(?:[A-Z][A-Z /&\-']* ?)?[Pp]age \d+ ?[0oO]f? ?\d*(?: ?[0oO]f ?\d+)?\s*$")
REMnant_H = re.compile(r"^\s*[Pp] ?(?:[a-z] )?(?=(?:GA|EO|SO|EMS|PR|SH|FP|TR)\.? ?\d)")
ROMAN_GARBLE = {r"^Ill\.": "III.", r"^lV\.": "IV.", r"^IIX\.": "IX.", r"^Vl\.": "VI.", r"^Vll\.": "VII.", r"^Vlll\.": "VIII."}
ROMAN_OK = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV)\. [A-Z][A-Z /&\-']{2,60}$")

def fix_card(line):
    if 'class="sop-meta"' not in line:
        return line
    inner = re.search(r">(.*)</div>", line)
    if not inner or "<strong>" in line:
        return line
    body = inner.group(1)
    body = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", body)
    return line[:inner.start(1)] + body + line[inner.end(1):]

def process(text):
    out = []
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            out.append(line); continue
        if 'sop-meta' in s:
            out.append(fix_card(line)); continue
        if FOOTER.match(s) or REMnant_H.match(s):
            continue  # strip PDF running furniture
        g = None
        for pat, rep in ROMAN_GARBLE.items():
            m = re.match(pat, s)
            if m:
                g = s.replace(m.group(0), rep, 1); break
        if g is not None and ROMAN_OK.match(g):
            num, rest = g.split(" ", 1)
            title = rest.title().replace("And", "and").replace("Or", "or").replace("Of", "of").replace("The", "the")
            out.append(f"## {num} {title}")
            continue
        m = re.match(r"^e (?=[A-Z][a-z])", s)
        if m:
            out.append("- " + s[2:]); continue
        out.append(line)
    return "\n".join(out)

def main():
    n = 0
    for d in DIRS:
        for p in sorted(d.rglob("*.md")):
            raw = t = p.read_text()
            t = process(t)
            t = re.sub(r"\n{3,}", "\n\n", t)
            if t != raw:
                p.write_text(t); n += 1
    print(f"pass2 touched {n} files")

if __name__ == "__main__":
    main()
