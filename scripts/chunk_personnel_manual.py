# chunk_personnel_manual.py — split the flat personnel-policy dump into indexed, jumpable pages
# Idempotent: re-run regenerates everything under docs/personnel-policies/policies/ + index.md.
# Source stays untouched at docs/personnel-policies/other/personnel-policy-manual.md (nav'd as archive).
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/personnel-policies/other/personnel-policy-manual.md"
OUT_DIR = ROOT / "docs/personnel-policies/policies"
INDEX = ROOT / "docs/personnel-policies/index.md"

title_re = re.compile(r"^\s*Policy Title:\s*(.+?)\s*(?:Effective Date:|$)")
sec_re = re.compile(r"^\s*Section No\.:\s*(\d+)")
date_re = re.compile(r"Effective Date:\s*([0-9/]+)")
sup_re = re.compile(r"Supersedes Policy:\s*(.+?)\s*$")

# ALL-CAPS section heads: >=3 chars, letters only (plus common punct), no lowercase
head_re = re.compile(r"^[A-Z][A-Z0-9 ,'’&/\-–—()\.:]{2,68}:?$")

def is_head(line):
    s = line.strip()
    if not s or len(s) > 70 or head_re.match(s) is None:
        return False
    letters = sum(c.isalpha() for c in s)
    if letters < 3:
        return False
    # skip single shout-words that are usually body fragments or noise
    if s.rstrip(":") in {"WARNING", "NOTICE", "NOTE", "ATTENTION"}:
        return False
    return True

def slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t[:48] or "policy"

lines = SRC.read_text().splitlines()

# 1) locate policy anchors
anchors = []  # (line_idx, title, secno, effdate)
for i, ln in enumerate(lines):
    m = title_re.match(ln)
    if m:
        title = m.group(1).strip()
        sec, eff = None, ""
        if i + 1 < len(lines):
            sm = sec_re.search(lines[i + 1])
            sec = sm.group(1) if sm else None
            em = date_re.search(lines[i + 1]) or date_re.search(ln)
            eff = em.group(1) if em else ""
        anchors.append((i, title, sec, eff))

print(f"anchors: {len(anchors)}")

blocks = []
# preamble
if anchors and anchors[0][0] > 0:
    blocks.append(("Introduction", "00", "", lines[: anchors[0][0]]))
for k, (idx, title, sec, eff) in enumerate(anchors):
    end = anchors[k + 1][0] if k + 1 < len(anchors) else len(lines)
    body = lines[idx + 2: end]  # skip the two header lines (they become page meta)
    blocks.append((title, sec or f"{k+1:02d}", eff, body))

OUT_DIR.mkdir(parents=True, exist_ok=True)
index_rows = []
for title, sec, eff, body in blocks:
    secn = int(sec) if str(sec).isdigit() else sec
    fname = f"{int(sec):02d}-{slugify(title)}.md" if str(sec).isdigit() else f"{sec}-{slugify(title)}.md"
    out = [f"# {title}", ""]
    meta = [f"**Section No.: {sec}**"]
    if eff:
        meta.append(f"Effective: {eff}")
    out += ["_{}_".format("  ·  ".join(meta)), ""]
    prev_blank_head = False
    for ln in body:
        if is_head(ln):
            h = ln.strip().rstrip(":")
            h = h.title().replace("Fmla", "FMLA").replace("Flsa", "FLSA").replace("Adeas", "ADEAS")
            h = re.sub(r"\bOidc\b", "OIDC", re.sub(r"\bEo\b", "EO", re.sub(r"\bUsa|Eeo", "EEO", h)))
            out.append(f"## {h}")
            prev_blank_head = True
        else:
            out.append(ln)
        # collapse 3+ blank runs
    txt = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    (OUT_DIR / fname).write_text(txt)
    heads = txt.count("\n## ")
    index_rows.append((sec, title, fname, eff, heads))

# index page
ix = ["# Personnel Policy Manual — Indexed", "",
      "The City of Poquoson personnel policy manual, split into its policy sections for fast",
      "mobile navigation. Each page carries jumpable sub-section headings in the right sidebar",
      "(table of contents). The complete original text remains available in the",
      "[Full Text Archive](other/personnel-policy-manual.md).", "",
      "| Sec | Policy | Sections |",
      "|:---:|--------|:---:|"]
for sec, title, fname, eff, heads in index_rows:
    ix.append(f"| {sec} | [{title}](policies/{fname}) | {heads} |")
INDEX.write_text("\n".join(ix) + "\n")
print(f"pages: {len(index_rows)} -> {OUT_DIR}")
