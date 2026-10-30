# port_reference.py — vault note -> site reference page (Obsidian -> mkdocs-material)
# Usage: python scripts/port_reference.py <vault_md> <site_out.md>
# Conversions: frontmatter dropped w/ provenance footer; [!callouts] -> !!! admonitions;
# wikilinks -> site links (via SITE_MAP) or plain display text; wide tables wrapped in .fx-wrap.
import re, sys, posixpath
from pathlib import Path

SITE_MAP = {  # vault title -> repo path (docs/...)
    "EO 6.00 First To Arrive Duties": "sops/emergency-operations/EO-600-First-to-Arrive-Duties.md",
    "EO 6.00 FORCES Mnemonic": "sops/emergency-operations/EO-600a-FORCES-Mnemonic.md",
    "Initial Alarm Company Assignments": "fire-ems-references/initial-alarm-company-assignments.md",
}

def wikilink_repl(out_dir, m):
    inner = m.group(1)
    if "|" in inner:
        target, disp = inner.split("|", 1)
    else:
        target = disp = inner
    target = target.split("#")[0].strip()
    key = target.replace("_", " ").strip()
    if key in SITE_MAP:
        rel = posixpath.relpath("docs/" + SITE_MAP[key], start=out_dir)
        return f"[{disp.strip()}]({rel})"
    return disp.strip() or target

def wide_table_wrap(text):
    out = []
    i, lines = 0, text.splitlines()
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
            ncols = len([c for c in ln.strip().strip("|").split("|")])
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            if ncols >= 4:
                out.append('<div class="fx-wrap" markdown="1">\n')
                out.append("")
                out.extend(lines[i:j])
                out.append("")
                out.append("</div>")
            else:
                out.extend(lines[i:j])
            i = j
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)

def convert(src_path, out_path):
    raw = Path(src_path).read_text()
    # strip frontmatter, capture provenance
    prov = ""
    m = re.match(r"^---\n.*?\n---\n", raw, re.S)
    if m:
        fm = m.group(0)
        sm = re.search(r"source:\s*(.+)", fm)
        mm = re.search(r"modified:\s*(.+)", fm)
        prov = f"\n\n---\n*Formatted from **{sm.group(1).strip() if sm else 'the source PDF'}** (vault note, last modified {mm.group(1).strip() if mm else 'n/a'}). The signed PDF remains the authoritative document.*\n"
        raw = raw[m.end():]
    # callouts -> admonitions  (> [!type]- Title \n > body...)
    def callout(mt):
        kind = mt.group(1).lower()
        title = (mt.group(2) or "").strip() or kind.capitalize()
        body = re.sub(r"^> ?", "    ", mt.group(3), flags=re.M)
        return f'!!! {kind} "{title}"\n{body.rstrip()}\n'
    raw = re.sub(r"(?m)^> \[!(\w+)(?:[-+])?\]\s*(.*)\n((?:^>.*(?:\n|$))*)", callout, raw)
    # wikilinks
    out_dir = str(Path(out_path).parent)
    raw = re.sub(r"\[\[([^\]]+)\]\]", lambda m: wikilink_repl(out_dir, m), raw)
    raw = raw.replace("[Benchmarks]", "Benchmarks")
    # drop the vault backlinks footer block
    raw = re.sub(r"\n---\n\*\*Backlinks / Related\*\*\n(?:- .*\n?)+", "\n", raw)
    raw = wide_table_wrap(raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw).strip() + prov
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(raw + "\n")
    print("ported ->", out_path, f"({len(raw)} chars)")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
