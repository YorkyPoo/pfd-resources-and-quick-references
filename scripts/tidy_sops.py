#!/usr/bin/env python3
"""tidy_sops.py — deterministic PDF-dump cleanup for SOP and policy pages.

1. docs/sops/**: strip the PDF header block (address/phone/underscore labels),
   extract metadata into a .sop-meta card, promote Roman-numeral section
   headings to H2, unwrap hard-wrapped paragraphs.
2. docs/personnel-policies/**: unwrap hard-wrapped lines only.
Idempotent: processed pages have no header patterns left to match; unwrapping
an already-unwrapped line is a no-op. Never touches pages carrying fx/dz
components (hand-built tables).
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOPS = ROOT / "docs" / "sops"
POLS = ROOT / "docs" / "personnel-policies" / "policies"

ROMAN = re.compile(r"^(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX)\.?\s+[A-Z][A-Z /&\-']{2,60}$")
HDR_PATTERNS = [
    re.compile(r"^City of Poquoson(\s+Fire\s+and\s+Rescue)?$"), re.compile(r"^Fire and Rescue$"),
    re.compile(r"^\d{3} Poquoson Ave\.?$", re.I), re.compile(r"^(Poquoson,? )?VA 23662$"),
    re.compile(r"^Poquoson,? VA ?23662$"), re.compile(r"^757-\d{3}-\d{4}$"), re.compile(r"^F757-\d{3}-\d{4}$"),
    re.compile(r"^GENERAL ADMINISTRATION$|^EMERGENCY OPERATIONS$|^EMS PROTOCOLS?$|^EQUIPMENT AND APPARATUS$|^SAFETY AND HEALTH$|^PUBLIC RELATIONS$|^FIRE PREVENTION$|^TRAINING$"),
    re.compile(r"^SOP#?:\s*(\S.*)$"), re.compile(r"^Title:?\s*_*\s*(.*)$"),
    re.compile(r"^(?:Effective|Reviewed|Review) ?Date:?\s*_*\s*(\d{1,2}/\d{1,2}/\d{2,4})$"),
    re.compile(r"^_+$"),
]
SOPNUM = re.compile(r"^SOP#?:\s*(GA|EO|EMS|EQ|SH|PR|FP|TR)?\s*\d[\w.\-]*")

def is_listy(line):
    return bool(re.match(r"^\s*([A-Za-z]|\d{1,2})[\.\)]\s", line)) or re.match(r"^\s*[-*•]\s", line)

def unwrap(paragraph_lines):
    return re.sub(r"\s+", " ", " ".join(paragraph_lines)).strip()

def process_body(text):
    """unwrap hard-wraps + promote roman headings"""
    out = []
    buf = []
    def flush():
        if buf:
            out.append(unwrap(buf)); buf.clear()
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            flush(); out.append("")
            continue
        if ROMAN.match(s):
            flush()
            words = s.split(" ", 1)
            num, rest = words[0].rstrip("."), words[1] if len(words) > 1 else ""
            title = rest.title().replace("And", "and").replace("Or", "or").replace("Of", "of")
            out.append(f"## {num}. {title}")
            continue
        if (s.startswith("#") or s.startswith("|") or s.startswith("<div") or s.startswith("![")
                or is_listy(s) or s.startswith("> ") or s.startswith("???") or s.startswith("!!!")):
            flush(); out.append(line)
            continue
        buf.append(s)
    flush()
    # collapse triple blanks
    txt = "\n".join(out)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt

def process_sop(path):
    raw = path.read_text()
    if "<div" in raw and "sop-meta" in raw:
        return False
    if not (re.search(r"^SOP#?:", raw, re.M) or ROMAN.match(raw.split("\n")[6].strip() if len(raw.split("\n")) > 6 else "")):
        # not a raw pdf dump (already ported/clean) — unwrap only if wrapped lines exist
        body = process_body(raw)
        if body != raw:
            path.write_text(body)
        return body != raw
    lines = raw.split("\n")
    meta = {"sop": "", "title": "", "eff": "", "rev": "", "cat": ""}
    # find header region: after H1 until first roman heading
    idx_h1 = next((i for i, l in enumerate(lines) if l.startswith("# ")), 0)
    idx_roman = None
    for i in range(idx_h1 + 1, len(lines)):
        if ROMAN.match(lines[i].strip()):
            idx_roman = i; break
    head = lines[idx_h1 + 1: idx_roman] if idx_roman else lines[idx_h1 + 1: idx_h1 + 18]
    body = lines[idx_roman:] if idx_roman else lines[idx_h1 + 1:]
    for l in head:
        s = l.strip()
        m = re.match(r"^SOP#?:\s*(\S.*?)\s*$", s)
        if m: meta["sop"] = m.group(1); continue
        m = re.match(r"^(?:Effective|Reviewed) ?Date:?\s*_*\s*(\d{1,2}/\d{1,2}/\d{2,4})$", s)
        if m: meta["eff"] = m.group(1); continue
        m = re.match(r"^Revi?sed Date:?\s*_*\s*(\d{1,2}/\d{1,2}/\d{2,4})$", s)
        if m: meta["rev"] = m.group(1); continue
        m = re.match(r"^Title:?\s*_*\s*(\S.*)$", s)
        if m: meta["title"] = m.group(1).strip(); continue
    cat = ""
    for l in head:
        s = l.strip()
        if re.match(r"^[A-Z][A-Z /&\-']{4,40}$", s) and not ROMAN.match(s) and "CITY" not in s:
            cat = s.title(); break
    parts = []
    if meta["sop"]: parts.append(f"**SOP** {meta['sop']}")
    if cat: parts.append(f"**Category:** {cat}")
    if meta["eff"]: parts.append(f"**Effective:** {meta['eff']}")
    if meta["rev"]: parts.append(f"**Revised:** {meta['rev']}")
    title = meta["title"]
    h1 = lines[idx_h1]
    if title and title.lower() not in h1.lower():
        h1 = h1  # keep filename title
    card = '<div class="sop-meta">' + " &nbsp;·&nbsp; ".join(parts) + "</div>" if parts else ""
    new = "\n".join([h1, "", card, ""] + body) if card else "\n".join([h1, ""] + body)
    new = process_body(new)
    if not new.endswith("\n"): new += "\n"
    path.write_text(new)
    return True

def main():
    changed = skipped = 0
    for p in sorted(SOPS.rglob("*.md")):
        if "index" in p.name.lower(): continue
        try:
            if process_sop(p): changed += 1
            else: skipped += 1
        except Exception as e:
            print(f"ERR {p}: {e}")
    for p in sorted(POLS.glob("*.md")):
        raw = p.read_text()
        if "fx-wrap" in raw or "dz-wrap" in raw: skipped += 1; continue
        body = process_body(raw)
        if body != raw: p.write_text(body); changed += 1
        else: skipped += 1
    print(f"tidied={changed} unchanged={skipped}")

if __name__ == "__main__":
    sys.exit(main())
