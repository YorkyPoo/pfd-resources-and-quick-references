#!/usr/bin/env python3
"""PEMS provider-level scanner / corrector for the Poquoson EMS protocol site.

WHAT THIS DOES
--------------
Every protocol page carries a markdown table whose five level columns are
`EMR | EMT | A | I | P`. This tool pairs each site intervention row with the
corresponding row on the PEMS 2024 regional protocol page, derives the provider
level PEMS actually codes for that intervention, and reports (or, with
`--apply`, rewrites) the five level cells so they match.

  python scripts/pems_level_scan.py --report        # report only, no writes
  python scripts/pems_level_scan.py --apply         # rewrite level cells in place
  python scripts/pems_level_scan.py --apply --dry-run
  python scripts/pems_level_scan.py --report --only 'protocols/cardiac/*' --verbose

WHY MATCHING IS CONSERVATIVE (read this before loosening any threshold)
-----------------------------------------------------------------------
A wrong provider level is a clinical-safety defect: publishing "EMT may do X"
when the regional protocol says "A may do X" hands an intervention to a
provider who is not authorized to perform it, and nothing downstream catches
it. A blank cell is a visible gap that a human sees; a confidently wrong cell
looks finished and never gets looked at again. So this tool is built to leave
rows alone:

  1. A site page is only compared to a PEMS page when BOTH the title match and
     the row-by-row text alignment agree. Title matching alone was proven
     untrustworthy (`Asystole / PEA` scored highest against `Electrical
     Injuries` because both contain the word "electrical"), so the page is
     chosen by which PEMS page's rows actually align with the site's rows.
  2. Rows are aligned with a monotonic dynamic-programming alignment, one
     PEMS row per site row, and a pair is only accepted above a similarity
     floor. Everything else is reported `UNMATCHED` and is never edited.
  3. Ambiguous level evidence (two badges on one PEMS row, left/right badge
     disagreement on the page, a borderline text score) is tagged
     `confidence: inferred` and is excluded from `--apply` even when the
     expected cells differ. It is reported for a human to resolve in the PDF.
  4. `--apply` writes ONLY the five level cells of existing table rows. It
     never touches intervention text, doses, criteria, pearls or destination
     rules; anything in that class is emitted to `needs-authoring.md`.
  5. Deliberate local deviations (divider rows, merged PEMS pages, Poquoson
     additions with no upstream source) must be declared in
     `audit/level-scan/exceptions.yaml` WITH a reason. An exception without a
     reason is a hard error, not a warning, so the exception list cannot
     quietly become a list of every row the matcher failed on.

LEVEL SEMANTICS (owner ruling, do not change)
---------------------------------------------
  * A level in a row means that level AND every level above it may perform the
    intervention as a standing order.
  * Bracketed `[A]` means that level must contact Medical Control for
    permission; the levels above perform it standing; no level below may
    perform it at all.
  * Bare `MC` in every cell means ALL levels must contact Medical Control.
  * Divider rows (section labels such as `Anaphylaxis`) authorize nothing and
    are not level-gated.

PEMS source rows are read from the PDF with `pdftotext -bbox-layout`, i.e. by
word coordinates, not by the flattened text stream: the flattened stream
interleaves the badge column into the middle of sentences and loses the
row/level pairing (see `pems_chunks/PEMS2024_full.txt`). Coordinates let each
row's badge be read off the left and right margin of the same visual line.
The extraction is cached under `audit/level-scan/.cache/`; delete that file or
pass `--rebuild-pems` to re-read the PDF.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import fnmatch
import glob
import html
import json
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    sys.exit("pyyaml is required: python -m pip install pyyaml")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
OUTDIR = os.path.join(REPO, "audit", "level-scan")
CACHE = os.path.join(OUTDIR, ".cache", "pems_bbox.xml")
PDF = os.environ.get("PEMS_PDF", "/root/System/mindpalace/40 - areas/Paramedic/PEMS2024.pdf")
EXCEPTIONS = os.path.join(OUTDIR, "exceptions.yaml")
FIXLIST = os.path.join(REPO, "audit", "protocol-reconciliation", "FIXLIST.md")
CHANGELOG = os.path.join(OUTDIR, "changelog.md")

LEVELS = ["EMR", "EMT", "A", "I", "P"]
LV_CELLS = ["", "•", "MC", "[A]", "[I]", "[P]"]

# --------------------------------------------------------------------------
# PEMS extraction
# --------------------------------------------------------------------------
PAGE_RE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
LVT = re.compile(r'^\[?\s?(EMR|EMT|A|I|P|MC)\s?\]?$')
BRK = re.compile(r'^\[\s?(EMR|EMT|A|I|P)\s?\]$')
SEC = re.compile(r'^(PEARLS|NOTES|REFERENCES|PROCEDURES|CRITERIA|ADMINISTRATIVE)$')


def _read_pdf_xml(force: bool) -> str:
    if not force and os.path.exists(CACHE):
        return open(CACHE, encoding="utf-8", errors="replace").read()
    if not os.path.exists(PDF):
        sys.exit(f"PEMS PDF not found at {PDF!r}; set PEMS_PDF or restore the file")
    try:
        xml = subprocess.run(["pdftotext", "-bbox-layout", PDF, "-"],
                             capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("pdftotext (poppler-utils) is required to read the PEMS PDF")
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    open(CACHE, "w", encoding="utf-8").write(xml)
    return xml


def _words(body: str) -> list[dict]:
    return [{"x0": float(a), "y0": float(b), "x1": float(c), "t": html.unescape(e)}
            for a, b, c, d, e in WORD_RE.findall(body)]


def _norm_tok(t: str) -> str | None:
    t = re.sub(r"\s", "", t)
    m = LVT.match(t)
    if not m:
        return None
    return f"[{m.group(1)}]" if BRK.match(t) else m.group(1)


def parse_pems_page(body: str) -> tuple[list[dict], bool]:
    """One PEMS page -> (rows, has_protocol_heading).

    Badge columns are located per page (their x position drifts between 42pt and
    96pt on the left and 540-556pt on the right), so the two margin columns are
    clustered from the level-shaped words themselves instead of hard-coded.
    """
    ws = _words(body)
    prot = [w for w in ws if w["t"].strip().upper() == "PROTOCOL" and w["x0"] < 80 and w["y0"] < 700]
    # A continuation page repeats the protocol grid but has no CRITERIA section,
    # so it must not be treated as the start of a new protocol document.
    has_criteria = any(w["t"].strip().upper() == "CRITERIA" and w["x0"] < 80 and w["y0"] < 700 for w in ws)
    has_prot = bool(prot) and has_criteria
    # A continuation page has no PROTOCOL heading; its badge grid starts right
    # under the running header.
    py = prot[0]["y0"] if (prot and has_criteria) else 88.0

    def alone(w) -> bool:
        return not any(o is not w and abs(o["y0"] - w["y0"]) < 3 and o["x0"] > w["x1"] + 2 for o in ws)

    ends = [w["y0"] for w in ws
            if SEC.match(w["t"].strip().upper()) and w["y0"] > py + 2 and w["x0"] < 80 and alone(w)]
    ey = min(ends) if ends else 700.0
    reg = [w for w in ws if py + 2 < w["y0"] < min(ey, 725)]
    cand = [w for w in reg if _norm_tok(w["t"].strip())]
    if not cand:
        return [], has_prot
    left = [w for w in cand if w["x0"] < 306]
    right = [w for w in cand if w["x0"] >= 306]
    if not left or not right:            # one-sided page: fall back to whichever exists
        left = left or right
        right = right or left
    lx = sum(w["x0"] for w in left) / len(left)
    rx = sum(w["x0"] for w in right) / len(right)

    # Badges are printed as a level word in a narrow margin column, and a
    # bracket is TWO extra words ("[" and "]") flanking it. Group everything in
    # the margin columns by line, then reassemble the text in reading order so
    # "[ I ]" comes back as the bracketed token `[I]` instead of a bare `I`.
    def in_margin(w) -> bool:
        return abs(w["x0"] - lx) <= 12 or abs(w["x0"] - rx) <= 12

    margin = sorted((w for w in reg if in_margin(w)), key=lambda w: (w["y0"], w["x0"]))
    groups: list[list[dict]] = []
    for w in margin:
        if groups and abs(groups[-1][0]["y0"] - w["y0"]) < 4:
            groups[-1].append(w)
        else:
            groups.append([w])

    def token(chunk: list[dict]) -> str | None:
        s = re.sub(r"\s+", "", "".join(w["t"] for w in sorted(chunk, key=lambda w: w["x0"])))
        m = re.match(r"^\[?(EMR|EMT|A|I|P|MC)\]?$", s)
        if not m:
            return None
        return f"[{m.group(1)}]" if s.startswith("[") else m.group(1)

    rows = []
    for g in groups:
        lside = [w for w in g if w["x0"] < 306]
        rside = [w for w in g if w["x0"] >= 306]
        lt, rt = token(lside) if lside else None, token(rside) if rside else None
        toks = [t for t in (lt, rt) if t]
        if not toks:                       # stray bracket or margin text: not a row
            continue
        uniq = []
        for t in toks:
            if t not in uniq:
                uniq.append(t)
        rows.append({"y": sum(a["y0"] for a in g) / len(g), "levels": uniq,
                     "side": "both" if (lt and rt) else ("left" if lt else "right"),
                     "words": []})
    if not rows:
        return [], has_prot
    ys = [r["y"] for r in rows]
    bounds = [py - 2] + [(ys[i] + ys[i + 1]) / 2 for i in range(len(ys) - 1)] + [ey]
    for w in reg:
        if in_margin(w):
            continue
        for i, r in enumerate(rows):
            if bounds[i] <= w["y0"] < bounds[i + 1]:
                r["words"].append(w)
                break
    for r in rows:
        r["words"].sort(key=lambda w: (round(w["y0"] / 4), w["x0"]))
        r["text"] = re.sub(r"\s+", " ", " ".join(w["t"] for w in r["words"])).strip()
        r["y"] = round(r["y"], 1)
        r.pop("words")
    return rows, has_prot


def build_pems(force: bool = False) -> dict[int, dict]:
    """{page_no: {title, rows, has_protocol}} for every page carrying level badges."""
    xml = _read_pdf_xml(force)
    out: dict[int, dict] = {}
    for pno, m in enumerate(PAGE_RE.finditer(xml), 1):
        body = m.group(3)
        rows, has_prot = parse_pems_page(body)
        if not rows:
            continue
        title = ""
        head = [w for w in _words(body) if w["y0"] < 90]
        if head:
            ymin = min(w["y0"] for w in head)
            first = sorted((w for w in head if abs(w["y0"] - ymin) < 6), key=lambda w: w["x0"])
            title = " ".join(w["t"] for w in first)
        out[pno] = {"page": pno, "title": re.sub(r"\s+", " ", title), "rows": rows,
                    "has_protocol": has_prot}
    return out


def build_docs(pems: dict[int, dict]) -> list[dict]:
    """Group PEMS pages into protocol DOCUMENTS.

    A protocol routinely runs onto a continuation page that has no `PROTOCOL`
    heading of its own (Allergic Reaction p.99 -> p.100, Bradycardia p.103 ->
    p.104). Treating each PDF page as a protocol silently truncated those and
    left half of every such site page unmatched. A page joins the current
    document when it carries badges, has no `PROTOCOL` heading and its running
    header still reads as the same protocol title.
    """
    docs: list[dict] = []
    for pno in sorted(pems):
        p = pems[pno]
        cur = docs[-1] if docs else None
        same = False
        if cur and not p["has_protocol"]:
            a, b = specific(nz(p["title"])), specific(nz(cur["title"]))
            same = difflib.SequenceMatcher(None, a, b).ratio() >= 0.6 or a in b or b in a
        if cur is not None and same and pno == cur["pages"][-1] + 1:
            cur["pages"].append(pno)
            for j, r in enumerate(p["rows"]):
                cur["rows"].append({"page": pno, "j": j, **r})
        else:
            docs.append({"title": p["title"], "pages": [pno],
                         "rows": [{"page": pno, "j": j, **r} for j, r in enumerate(p["rows"])]})
    return docs


# --------------------------------------------------------------------------
# text matching
# --------------------------------------------------------------------------
CLEAN_MD = re.compile(r"\[([^\]]+)\]\([^)]*\)")
STOPW = {
    "cardiac", "medical", "trauma", "general", "respiratory", "neurologic", "toxicology",
    "administrative", "front", "matter", "symptomatic", "the", "and", "of", "for", "patient",
    "care", "injury", "injuries", "emergencies", "emergency", "related", "management",
    "procedures", "procedure", "protocol",
}
SYN = {"rosc": "resuscitation", "aemt": "advanced emt", "cpr": "cardiopulmonary resuscitation",
       "ob": "obstruction", "fbfo": "foreign body airway obstruction", "acs": "acute coronary syndrome",
       "svt": "supraventricular tachycardia", "vf": "vfib", "vt": "vtach", "copd": "chronic obstructive pulmonary disease"}
ROW_STOP = set("""the and with for from that this into than then when which while also may should must
consider administer administered administering patient patients adult pediatric dose maximum repeat
once until after before only per via apply applied obtain provide perform assess assessed monitor
maintain initial protocol protocol refer refer to as needed if is are be been was were has have had
following indicate indicated according appropriate per each any all other another using use used
""".split())


def nz(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def clean(s: str) -> str:
    s = CLEAN_MD.sub(r"\1", s)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"[`*_\\]", "", s)
    s = re.sub(r"\[\s?([A-Z])\s?\]", r" \1 ", s)      # keep bracket semantics out of prose matching
    return re.sub(r"\s+", " ", s).strip()


def specific(t: str) -> str:
    return " ".join(SYN.get(x, x) for x in nz(t).split() if x not in STOPW)


def title_score(t: str, pt: str) -> float:
    if not t or not pt:
        return -1.0
    ratio = difflib.SequenceMatcher(None, t, pt).ratio()
    a, b = set(t.split()), set(pt.split())
    bonus = 0.45 if (t in pt or pt in t) else 0.30 * len(a & b) / max(len(a | b), 1)
    sc = ratio * 0.7 + bonus
    if ("non traumatic" in t) != ("non traumatic" in pt):
        sc -= 1.2
    if "neonatal" in pt and "neonatal" not in t:
        sc -= 0.8
    if "pediatric" in pt and "pediatric" not in t:
        sc -= 0.4
    return sc


def sig_tokens(s: str) -> set[str]:
    out = set()
    for w in re.findall(r"[a-z0-9][a-z0-9%/.-]*", s.lower()):
        w = w.strip(".")
        if len(w) >= 4 and w not in ROW_STOP and not w.isdigit():
            out.add(w)
    return out


def row_sim(site: str, pems: str) -> float:
    """Similarity of an intervention described two ways.

    Coverage of the SHORTER side dominates because the PEMS row text carries
    section headings that were pulled into the cell by layout extraction.
    """
    a, b = sig_tokens(clean(site)), sig_tokens(pems)
    if not a or not b:
        return 0.0
    jac = len(a & b) / min(len(a), len(b))
    ratio = difflib.SequenceMatcher(None, " ".join(sorted(a)), " ".join(sorted(b))).ratio()
    return 0.65 * jac + 0.35 * ratio


ROW_THRESHOLD = 0.40


def align(site_texts: list[str], pems_texts: list[str]) -> list[tuple[int, int, float]]:
    """Monotonic one-to-one alignment maximising total (score - threshold)."""
    n, m = len(site_texts), len(pems_texts)
    S = [[row_sim(a, b) for b in pems_texts] for a in site_texts]
    NEG = -1e9
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opts = [(best[i - 1][j], "up"), (best[i][j - 1], "left")]
            if S[i - 1][j - 1] >= ROW_THRESHOLD:
                opts.append((best[i - 1][j - 1] + S[i - 1][j - 1] - ROW_THRESHOLD, "diag"))
            best[i][j], back[i][j] = max(opts, key=lambda x: x[0])
    pairs = []
    i, j = n, m
    while i > 0 and j > 0:
        b = back[i][j]
        if b == "diag":
            pairs.append((i - 1, j - 1, S[i - 1][j - 1]))
            i, j = i - 1, j - 1
        elif b == "up":
            i -= 1
        else:
            j -= 1
    return list(reversed(pairs))


# --------------------------------------------------------------------------
# levels -> cells
# --------------------------------------------------------------------------
def expected_cells(levels: list[str]) -> tuple[list[str], str]:
    """PEMS badge tokens -> the five site cells, plus a confidence note.

    Returns (cells, note). `note` is "" when the evidence is unambiguous, else a
    human-readable reason the row must stay `inferred`.
    """
    if not levels:
        return [""] * 5, "no level badge on the PEMS row"
    if len(levels) > 1:
        if all(tok in ("MC",) for tok in levels):
            return ["MC"] * 5, ""
        return [""] * 5, f"multiple level badges on one PEMS row: {levels}"
    tok = levels[0]
    if tok == "MC":
        return ["MC"] * 5, ""
    br = BRK.match(tok)
    name = br.group(1) if br else tok
    if name not in LEVELS:
        return [""] * 5, f"unknown badge {tok}"
    i = LEVELS.index(name)
    cells = [""] * 5
    if br:
        cells[i] = f"[{name}]"
        for k in range(i + 1, 5):
            cells[k] = "•"
    else:
        for k in range(i, 5):
            cells[k] = "•"
    return cells, ""


def cell_kind(c: str) -> str:
    s = c.strip()
    if not s:
        return "empty"
    if BRK.match(s):
        return "bracketed"
    if "MC" in s.upper():
        return "mc"
    return "grant"


def cells_equal(a: list[str], b: list[str]) -> bool:
    return [c.strip() for c in a] == [c.strip() for c in b]


# --------------------------------------------------------------------------
# site pages
# --------------------------------------------------------------------------
HDR_RE = re.compile(r"\|\s*EMR\s*\|\s*EMT\s*\|\s*A\s*\|\s*I\s*\|\s*P\s*\|")
DIVIDER_WORDS = re.compile(r"\b(pathway|anaphylaxis|non-anaphylaxis|hypoglycemia|hyperglycemia)\b", re.I)


def cells(line: str) -> list[str]:
    """Escape-aware: `\\|` is cell TEXT, not a separator (same rule as the review packet)."""
    s = line.strip().strip("|").replace("\\|", "\x00")
    return [c.strip().replace("\x00", "|") for c in s.split("|")]


def is_divider(num: str, action: str) -> bool:
    a = action.strip()
    if not a:
        return True
    if num:
        return len(a) <= 32 and bool(DIVIDER_WORDS.search(a))
    return len(a) <= 48 and not re.search(
        r"\d|\b(administer|apply|consider|obtain|monitor|repeat|assess|provide|transport|contact)\b", a, re.I)


def read_page(path: str) -> dict:
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    rel = os.path.relpath(path, DOCS).replace(os.sep, "/")
    hdr = next((i for i, l in enumerate(lines) if HDR_RE.search(l)), None)
    if hdr is None:
        return {"file": path, "rel": rel, "has_table": False, "rows": [], "lines": lines}
    n = len(cells(lines[hdr]))
    title = next((re.sub(r"^##\s*(General\s*-\s*)?", "", l).strip() for l in lines[:hdr]
                  if l.startswith("## ")), os.path.basename(path))
    rows = []
    for idx in range(hdr + 2, len(lines)):
        raw = lines[idx]
        s = raw.strip()
        if not s.startswith("|"):
            if s:
                break
            continue
        c = cells(raw)
        if len(c) != n or len(c) < 7:
            continue
        rows.append({"idx": idx, "num": c[0], "action": c[1], "cells": c[2:7], "ncols": n,
                     "divider": is_divider(c[0], clean(c[1]))})
    return {"file": path, "rel": os.path.relpath(path, DOCS).replace(os.sep, "/"),
            "has_table": True, "title": title, "hdr": hdr, "rows": rows, "lines": lines, "ncols": n}


def rewrite_line(raw: str, new_cells: list[str], ncols: int) -> str:
    parts = cells(raw)
    parts[2:7] = new_cells
    return "| " + " | ".join(parts) + " |"


# --------------------------------------------------------------------------
# exceptions
# --------------------------------------------------------------------------
EXC_TEMPLATE = """\
# Deliberate deviations from the PEMS regional source.
#
# Every entry MUST carry a `reason`. An exception without a reason is a hard
# error: the whole point of this file is that a human looked at the row and
# decided the local text is right. Anything the matcher simply could not pair
# belongs in the report as UNMATCHED, not here.
#
# pages:
#   - file: protocols/cardiac/04_Foo_PROC.md
#     reason: one line explaining why this page deviates
#     pems_pages: [57, 63]          # optional: force the source page(s)
#     row_match: false              # optional: title+rows may disagree
#     rows:
#       "3": {kind: divider, reason: "section label, authorizes nothing"}
#       "7": {kind: local, reason: "Poquoson addition, no PEMS source row"}
#       "9": {pems_page: 63, pems_row: 2, reason: "row lives on the VF/pVT half"}
#       "11": {cells: ["", "•", "•", "•", "•"], reason: "OMD-ordered deviation"}
"""


def load_exceptions(path: str) -> dict:
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(EXC_TEMPLATE)
        return {"pages": {}}
    doc = yaml.safe_load(open(path, encoding="utf-8")) or {}
    problems = []
    pages: dict[str, dict] = {}
    for i, ent in enumerate(doc.get("pages") or []):
        f = (ent or {}).get("file", "").strip()
        if not f:
            problems.append(f"pages[{i}]: missing `file`")
            continue
        if not str(ent.get("reason", "")).strip():
            problems.append(f"{f}: page exception has no `reason`")
        rows = {}
        for key, spec in (ent.get("rows") or {}).items():
            spec = spec or {}
            if not str(spec.get("reason", "")).strip():
                problems.append(f"{f} row {key}: exception has no `reason`")
            if not (spec.get("kind") or spec.get("cells") or spec.get("pems_row") is not None
                    or spec.get("pems_page") is not None):
                problems.append(f"{f} row {key}: exception states no kind/cells/pems_row")
            rows[str(key)] = spec
        pages[f] = {"reason": ent.get("reason", ""), "pems_pages": ent.get("pems_pages"),
                    "kind": ent.get("kind"), "row_match": ent.get("row_match", True), "rows": rows}
    if problems:
        print("EXCEPTION FILE INVALID:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        sys.exit(2)
    return {"pages": pages}


# --------------------------------------------------------------------------
# analysis
# --------------------------------------------------------------------------
def choose_docs(site: dict, docs: list[dict], exc: dict | None) -> tuple[list[dict], float, float]:
    """Pick the PEMS protocol document(s) this site page is compared against.

    Returns (docs, page_score, coverage). Page choice is driven by row
    alignment, not title alone: `Asystole / PEA` scores highest by title against
    `Electrical Injuries` (shared word "electrical"), but only the asystole
    document's rows actually line up with the site's rows.
    """
    if exc and exc.get("pems_pages"):
        pages = set(exc["pems_pages"])
        chosen = [d for d in docs if pages & set(d["pages"])]
        # include continuation pages of a forced document automatically
        return chosen, 1.0, 1.0
    t = specific(site["title"])
    texts = [r["action"] for r in site["rows"] if not r["divider"]]
    scored = []
    for d in docs:
        ts = title_score(t, specific(d["title"]))
        if ts < 0.15:
            continue
        pairs = align(texts, [r["text"] for r in d["rows"]])
        cover = sum(sc for _, _, sc in pairs) / max(len(texts), 1)
        scored.append((0.4 * max(ts, 0.0) + 0.6 * cover, ts, cover, d))
    if not scored:
        return [], 0.0, 0.0
    scored.sort(key=lambda x: -x[0])
    best = scored[0]
    return [best[3]], round(best[1], 3), round(best[2], 3)
    return [scored[0][3]]


PAGE_TITLE_FLOOR = 0.45
PAGE_COVER_FLOOR = 0.30
STRONG_BAND = 0.85


def analyse(site: dict, docs: list[dict], exc_page: dict | None, verbose: bool) -> dict:
    out = {"file": site["rel"], "title": site.get("title") or site["rel"], "rows": [], "pems_pages": [],
           "page_band": None, "notes": []}
    if not site.get("has_table"):
        out["notes"].append("no EMR|EMT|A|I|P level table on this page")
        return out
    if exc_page and exc_page.get("kind") in ("administrative", "explanatory"):
        out["notes"].append(f"declared `{exc_page['kind']}` in exceptions.yaml — not level-gated")
        out["page_band"] = "n/a"
        for r in site["rows"]:
            key = r["num"] or f"divider:{nz(clean(r['action']))[:40]}"
            out["rows"].append({"row": key, "action": clean(r["action"])[:220], "idx": r["idx"],
                                "cells": [c.strip() for c in r["cells"]], "status": "not_level_gated",
                                "confidence": "n/a", "pems": None, "expected": None,
                                "reason": exc_page.get("reason", "")})
        return out
    forced = bool(exc_page and exc_page.get("pems_pages"))
    chosen, tsc, cover = choose_docs(site, docs, exc_page)
    if not forced and chosen and tsc < STRONG_BAND:
        out["notes"].append(
            f"no PEMS protocol matched with a strong title band (best {tsc:.2f}); "
            "declare the source in exceptions.yaml if this page does have a regional counterpart")
        chosen = []
    out["candidate"] = {"title_score": tsc, "coverage": cover}
    if not chosen:
        if not out["notes"]:
            out["notes"].append("no PEMS source page matched this page")
    else:
        out["pems_pages"] = [pg for d in chosen for pg in d["pages"]]
        out["page_band"] = "forced" if forced else (
            "strong" if tsc >= 0.85 else ("probable" if tsc >= 0.55 else "weak"))
        out["title_score"] = tsc
        out["coverage"] = cover

    exc_rows = (exc_page or {}).get("rows", {})
    pems_rows = [r for d in chosen for r in d["rows"]]
    data_rows = [r for r in site["rows"] if not r["divider"]]
    pairs = align([r["action"] for r in data_rows], [pr["text"] for pr in pems_rows]) if pems_rows else []
    by_site = {i: (j, sc) for i, j, sc in pairs}

    # divider / label rows first: they are never level-gated
    for r in site["rows"]:
        if not r["divider"]:
            continue
        key = r["num"] or f"divider:{nz(clean(r['action']))[:40]}"
        erec = exc_rows.get(key) or exc_rows.get(r["num"] or "")
        item = {"row": key, "action": clean(r["action"])[:220], "idx": r["idx"],
                "cells": [c.strip() for c in r["cells"]], "status": "divider",
                "confidence": "strong", "pems": None, "expected": None,
                "reason": "section-label row; authorizes nothing"}
        if not (erec and erec.get("kind") == "divider"):
            item["status"] = "divider-undeclared"
            item["reason"] += " (not declared in exceptions.yaml)"
        out["rows"].append(item)

    for i, r in enumerate(data_rows):
        key = r["num"] or ""
        erec = exc_rows.get(key)
        item = {"row": key, "action": clean(r["action"])[:220], "idx": r["idx"],
                "cells": [c.strip() for c in r["cells"]], "status": None, "confidence": "strong",
                "pems": None, "expected": None, "reason": ""}
        if erec and erec.get("kind") in ("local", "skip"):
            item.update(status="local", reason=erec.get("reason", ""))
            if erec.get("cells"):
                item["expected"] = [c.strip() for c in erec["cells"]]
                item["pems"] = {"exception": True}
                item["status"] = "ok" if cells_equal(item["cells"], item["expected"]) else "level_mismatch"
            out["rows"].append(item)
            continue
        if not pems_rows:
            item.update(status="UNMATCHED", reason="no PEMS source page for this protocol")
            out["rows"].append(item)
            continue
        if erec and erec.get("cells"):
            exp = [c.strip() for c in erec["cells"]]
            item["expected"] = exp
            item["pems"] = {"exception": True, "note": erec.get("reason", "")}
            item["status"] = "ok" if cells_equal(item["cells"], exp) else "level_mismatch"
            out["rows"].append(item)
            continue
        if erec and erec.get("pems_row") is not None:
            pg = erec.get("pems_page") or (pems_rows[0]["page"] if pems_rows else None)
            k = next((x for x, pr in enumerate(pems_rows)
                      if pr["page"] == pg and pr["j"] == erec["pems_row"]), None)
            if k is None:
                item.update(status="UNMATCHED",
                            reason=f"exceptions.yaml points at p.{pg} row {erec['pems_row']}, which is not in the extracted source")
                out["rows"].append(item)
                continue
            j, sc = k, 1.0
        elif i in by_site:
            j, sc = by_site[i]
        else:
            item.update(status="UNMATCHED",
                        reason="no PEMS row above the similarity floor for this intervention")
            out["rows"].append(item)
            continue
        pr = pems_rows[j]
        exp, note = expected_cells(pr["levels"])
        item["pems"] = {"page": pr["page"], "row": pr["j"], "y": pr["y"], "levels": pr["levels"],
                        "text": pr["text"][:220], "score": round(sc, 3), "side": pr["side"]}
        item["expected"] = exp
        notes = []
        if note:
            notes.append(note)
        if sc < 0.55:
            notes.append(f"text similarity only {sc:.2f}")
        if pr["side"] != "both":
            notes.append(f"level badge read from the {pr['side']} margin only")
        if out["page_band"] == "weak":
            notes.append("page title match is weak")
        # Removing an authorization is as consequential as granting one, and it
        # is the case a reader is least likely to notice ("it still says EMT and
        # above"). Unless the row text is a near-verbatim match, leave it.
        cur_grant = {i for i, c in enumerate(item["cells"]) if cell_kind(c) != "empty"}
        exp_grant = {i for i, c in enumerate(exp) if cell_kind(c) != "empty"}
        if exp_grant < cur_grant and sc < 0.85:
            notes.append("expected cells REMOVE a currently authorized level; needs review")
        item["confidence"] = "inferred" if notes else "strong"
        item["reason"] = "; ".join(notes)
        item["status"] = "ok" if cells_equal(item["cells"], exp) else "level_mismatch"
        out["rows"].append(item)

    # PEMS rows with no site counterpart: work the site is missing (never auto-created)
    used = {id(pems_rows[j]) for _, j, _ in pairs}
    missing = [pr for pr in pems_rows if id(pr) not in used]
    out["pems_unused"] = [{"page": pr["page"], "row": pr["j"], "levels": pr["levels"],
                           "text": pr["text"][:140]} for pr in missing]
    return out


# --------------------------------------------------------------------------
# FIXLIST -> out-of-scope authoring list
# --------------------------------------------------------------------------
LEVEL_FIX = re.compile(
    r"\b(?:Set|Move|Clear)\b[^.]*\b(?:EMR|EMT|A|I|P)\b[^.]*\b(?:cell|column|bullet)\b"
    r"|\bSet the \w+ column\b|\bSet (?:EMR|EMT|A|I|P) (?:cell|bullet)\b", re.I)


def needs_authoring() -> list[dict]:
    if not os.path.exists(FIXLIST):
        return []
    items = []
    for line in open(FIXLIST, encoding="utf-8"):
        if not line.startswith("- ["):
            continue
        m = re.match(r"- \[(\w+)\] (AUD-\d+) \| ([^|]+?) \| ([^|]*?) \|", line)
        if not m:
            continue
        sev, aud, path, row = m.group(1), m.group(2), m.group(3).strip(), m.group(4).strip()
        text = line[m.end():].strip()
        if LEVEL_FIX.search(text) and not re.search(r"\brow absent\b", row, re.I):
            continue
        items.append({"id": aud, "severity": sev, "file": path.replace("docs/", ""), "row": row,
                      "instruction": text[:400]})
    return items


def write_needs_authoring(items: list[dict]) -> str:
    path = os.path.join(OUTDIR, "needs-authoring.md")
    by_file: dict[str, list[dict]] = {}
    for it in items:
        by_file.setdefault(it["file"], []).append(it)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# Needs authoring — everything `--apply` refused to touch\n\n")
        fh.write("`pems_level_scan.py --apply` writes only EMR/EMT/A/I/P level cells. The\n"
                 "findings below are clinical-prose, dose, contraindication, destination or\n"
                 "missing-row work: they change what the protocol *says*, not who may perform it,\n"
                 "and they need an author (or the OMD) — not a script. Source: the audit FIXLIST.\n\n")
        fh.write(f"Total: **{len(items)}** items across **{len(by_file)}** files.\n\n")
        for f in sorted(by_file):
            fh.write(f"## {f}\n\n")
            for it in sorted(by_file[f], key=lambda x: x["id"]):
                fh.write(f"- `{it['id']}` [{it['severity']}] row {it['row']} — {it['instruction']}\n")
            fh.write("\n")
    return path


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
STATUS_LABEL = {
    "ok": "OK",
    "level_mismatch": "MISMATCH",
    "UNMATCHED": "UNMATCHED",
    "divider": "divider",
    "divider-undeclared": "DIVIDER-UNDECLARED",
    "local": "local",
    "skip": "skip",
}


def summarise(results: list[dict]) -> dict:
    c = {"pages": len(results), "pages_with_table": 0, "rows": 0, "ok": 0, "mismatch": 0,
         "inferred_mismatch": 0, "unmatched": 0, "divider": 0, "divider_undeclared": 0,
         "local": 0, "not_level_gated": 0, "pems_unused": 0}
    for p in results:
        if p.get("notes") and "no EMR|EMT|A|I|P" in p["notes"][0]:
            continue
        c["pages_with_table"] += 1
        c["pems_unused"] += len(p.get("pems_unused") or [])
        for r in p["rows"]:
            c["rows"] += 1
            st = r["status"]
            if st == "ok":
                c["ok"] += 1
            elif st == "level_mismatch":
                c["mismatch"] += 1
                if r["confidence"] == "inferred":
                    c["inferred_mismatch"] += 1
            elif st == "UNMATCHED":
                c["unmatched"] += 1
            elif st == "divider":
                c["divider"] += 1
            elif st == "divider-undeclared":
                c["divider_undeclared"] += 1
            elif st in ("local", "skip"):
                c["local"] += 1
            elif st == "not_level_gated":
                c["not_level_gated"] += 1
    return c


def write_report(results: list[dict], summ: dict, date: str) -> tuple[str, str]:
    os.makedirs(OUTDIR, exist_ok=True)
    jpath = os.path.join(OUTDIR, f"{date}-findings.json")
    mpath = os.path.join(OUTDIR, f"{date}-report.md")
    with open(jpath, "w", encoding="utf-8") as fh:
        json.dump({"scan_date": date, "summary": summ, "pages": results}, fh, indent=1)
    L = []
    A = L.append
    A(f"# PEMS provider-level scan — {date}\n\n")
    A("Generated by `scripts/pems_level_scan.py`. Level semantics: a level means that level and\n"
      "every level above it; `[A]` means that level calls Medical Control and the levels above act\n"
      "standing; bare `MC` in every cell means all levels call. See the script docstring for why\n"
      "unpaired rows are left alone.\n\n")
    A("| metric | count |\n|---|---|\n")
    for k, v in (("pages on disk", summ["pages"]), ("pages with a level table", summ["pages_with_table"]),
                 ("rows examined", summ["rows"]), ("rows already correct", summ["ok"]),
                 ("level mismatches (fixable)", summ["mismatch"] - summ["inferred_mismatch"]),
                 ("level mismatches inferred (reported, not applied)", summ["inferred_mismatch"]),
                 ("rows UNMATCHED", summ["unmatched"]), ("divider rows declared", summ["divider"]),
                 ("divider rows undeclared", summ["divider_undeclared"]),
                 ("rows declared local/exception", summ["local"]),
                 ("rows on pages declared not level-gated", summ["not_level_gated"]),
                 ("PEMS rows with no site row", summ["pems_unused"])):
        A(f"| {k} | {v} |\n")
    A("\n## Pages\n\n| page | PEMS p. | band | rows | ok | mismatch | inferred | UNMATCHED |\n|---|---|---|---|---|---|---|---|\n")
    for p in results:
        if "no EMR|EMT|A|I|P" in (p.get("notes") or [""])[0]:
            continue
        rr = p["rows"]
        mm = sum(1 for r in rr if r["status"] == "level_mismatch")
        inf = sum(1 for r in rr if r["status"] == "level_mismatch" and r["confidence"] == "inferred")
        un = sum(1 for r in rr if r["status"] == "UNMATCHED")
        oks = sum(1 for r in rr if r["status"] == "ok")
        A(f"| `{p['file']}` | {','.join(str(x) for x in p['pems_pages']) or '—'} | "
          f"{p['page_band'] or '—'} | {len(rr)} | {oks} | {mm - inf} | {inf} | {un} |\n")
    A("\n## Rows left UNMATCHED (residual human work)\n\n")
    unm = [(p["file"], r) for p in results for r in p["rows"] if r["status"] == "UNMATCHED"]
    if not unm:
        A("_None._\n")
    else:
        A(f"**{len(unm)} rows across {len({f for f, _ in unm})} files.** No PEMS row could be paired\n"
          "confidently, so these were not edited. Read the regional page and set the cells by hand.\n\n")
        cur = None
        for f, r in unm:
            if f != cur:
                A(f"\n### `{f}`\n\n")
                cur = f
            A(f"- row **{r['row']}** — {r['action'][:150]}  \n  current: `{r['cells']}` — {r['reason']}\n")
    A("\n## Level mismatches\n\n")
    mism = [(p["file"], r) for p in results for r in p["rows"] if r["status"] == "level_mismatch"]
    if not mism:
        A("_None._\n")
    for f, r in mism:
        tag = "INFERRED — not applied" if r["confidence"] == "inferred" else "apply"
        A(f"- `{f}` row **{r['row']}** ({tag}) — {r['action'][:120]}\n")
        A(f"  - current `EMR|EMT|A|I|P`: `{' | '.join(c or '·' for c in r['cells'])}`\n")
        A(f"  - PEMS `{' | '.join(c or '·' for c in r['expected'])}`"
          f" — p.{r['pems']['page']} row {r['pems']['row']} badge `{r['pems']['levels']}` (score {r['pems']['score']})\n")
        if r["reason"]:
            A(f"  - why: {r['reason']}\n")
    A("\n## PEMS rows with no site counterpart (missing site work, never auto-created)\n\n")
    any_missing = False
    for p in results:
        for m in p.get("pems_unused") or []:
            any_missing = True
            A(f"- `{p['file']}` ← p.{m['page']} row {m['row']} badge `{m['levels']}`: {m['text']}\n")
    if not any_missing:
        A("_None._\n")
    open(mpath, "w", encoding="utf-8").write("".join(L))
    return jpath, mpath


# --------------------------------------------------------------------------
# apply
# --------------------------------------------------------------------------
def git_dirty_tracked() -> list[str]:
    try:
        r = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                           cwd=REPO, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        sys.exit(f"`git status` failed ({e}); refusing to rewrite pages")
    return [l for l in r.stdout.splitlines() if l.strip()]


def apply_changes(results: list[dict], dry_run: bool) -> int:
    """Rewrite level cells for every mismatch that is not `inferred`.

    The clean-tree precondition is enforced once, in `main`, before any file is
    written (the report itself is tracked, so checking again here would abort on
    this run's own output).
    """
    changed_files = 0
    changed_rows = 0
    log = []
    for p in results:
        edits = [r for r in p["rows"]
                 if r["status"] == "level_mismatch" and r["confidence"] != "inferred" and r["expected"]]
        if not edits:
            continue
        path = os.path.join(DOCS, p["file"])
        lines = open(path, encoding="utf-8").read().splitlines()
        ncols = None
        for r in edits:
            if cells_equal(r["cells"], r["expected"]):
                continue
            old = lines[r["idx"]]
            ncols = len(cells(old))
            new = rewrite_line(old, [c or "" for c in r["expected"]], ncols)
            if new != old:
                lines[r["idx"]] = new
                changed_rows += 1
                src = r["pems"]
                where = (f"p.{src['page']} row {src['row']} (y={src.get('y')}, "
                         f"badge `{src.get('levels')}`)") if not src.get("exception") else "exceptions.yaml"
                log.append((p["file"], r["row"], r["cells"], r["expected"], where))
        if dry_run:
            changed_files += 1
            continue
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        changed_files += 1
    if log and not dry_run:
        os.makedirs(OUTDIR, exist_ok=True)
        new = not os.path.exists(CHANGELOG)
        with open(CHANGELOG, "a", encoding="utf-8") as fh:
            if new:
                fh.write("# Level-scan changelog\n\nEvery rewrite made by `pems_level_scan.py --apply`: "
                         "file, row, old cells, new cells, and the PEMS evidence.\n\n"
                         "Cells are written in EMR/EMT/A/I/P order; `·` is an empty cell.\n\n"
                         "| when | file | row | old cells | new cells | source |\n"
                         "|---|---|---|---|---|---|\n")
            now = _dt.datetime.now().isoformat(timespec="seconds")
            for f, row, old, newc, where in log:
                fmt = lambda cs: " ".join(c or "·" for c in cs)
                fh.write(f"| {now} | `{f}` | {row} | `{fmt(old)}` | `{fmt(newc)}` | {where} |\n")
    print(f"{'would rewrite' if dry_run else 'rewrote'} {changed_rows} rows in {changed_files} files")
    return 0


# --------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--report", action="store_true", help="analyse only; write findings + markdown report")
    g.add_argument("--apply", action="store_true", help="rewrite level cells in place")
    ap.add_argument("--dry-run", action="store_true", help="with --apply: show what would change, write nothing")
    ap.add_argument("--only", metavar="GLOB", help="limit to files matching this glob (relative to docs/)")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--rebuild-pems", action="store_true", help="re-read the PDF instead of the cached extraction")
    args = ap.parse_args(argv)

    date = _dt.date.today().isoformat()
    # --apply rewrites tracked files: refuse before writing anything (the report
    # is also tracked, so a late check would abort on our own output).
    if args.apply and not args.dry_run:
        dirty = git_dirty_tracked()
        if dirty:
            print("ABORT: tracked files already modified; commit or stash first:", file=sys.stderr)
            for d in dirty[:20]:
                print("  " + d, file=sys.stderr)
            return 3
    pems = build_pems(args.rebuild_pems)
    if not pems:
        sys.exit("no PEMS protocol pages could be extracted — check pdftotext and the PDF path")
    docs = build_docs(pems)
    exc = load_exceptions(EXCEPTIONS)

    files = sorted(glob.glob(os.path.join(DOCS, "protocols", "**", "*.md"), recursive=True))
    if args.only:
        files = [f for f in files
                 if fnmatch.fnmatch(os.path.relpath(f, DOCS).replace(os.sep, "/"), args.only)]
    if not files:
        sys.exit(f"no protocol pages matched {args.only!r}")

    results = []
    for f in files:
        site = read_page(f)
        ep = exc["pages"].get(site["rel"])
        res = analyse(site, docs, ep, args.verbose)
        results.append(res)
        if args.verbose:
            print(f"{res['file']}: pems={res['pems_pages']} band={res['page_band']} "
                  f"rows={len(res['rows'])}")
            for r in res["rows"]:
                print(f"   row {r['row']:>3} {r['status']:<18} {r['confidence']:<8} {r['action'][:70]}")

    summ = summarise(results)
    jpath, mpath = write_report(results, summ, date)
    npath = write_needs_authoring(needs_authoring())

    undeclared = [p["file"] for p in results if any(r["status"] == "divider-undeclared" for r in p["rows"])]
    print(f"pages: {summ['pages']} ({summ['pages_with_table']} with a level table) | rows: {summ['rows']}")
    print(f"ok: {summ['ok']} | mismatch: {summ['mismatch']} (inferred {summ['inferred_mismatch']}) | "
          f"UNMATCHED: {summ['unmatched']} | dividers: {summ['divider']} | local: {summ['local']}")
    print(f"wrote {os.path.relpath(jpath, REPO)} and {os.path.relpath(mpath, REPO)}")
    print(f"wrote {os.path.relpath(npath, REPO)} ({len(needs_authoring())} out-of-scope audit items)")
    if undeclared:
        print(f"undeclared divider rows on: {', '.join(undeclared)}", file=sys.stderr)

    if args.report:
        hard = summ["mismatch"] + summ["unmatched"] + summ["divider_undeclared"]
        return 1 if hard else 0
    rc = apply_changes(results, args.dry_run)
    if rc == 0 and not args.dry_run:
        # Re-scan so the committed report describes the tree AFTER the rewrite
        # (the first pass necessarily described the pre-apply state).
        after = [analyse(read_page(f), docs, exc["pages"].get(read_page(f)["rel"]), False) for f in files]
        summ = summarise(after)
        write_report(after, summ, date)
        print(f"post-apply: ok {summ['ok']} | mismatch {summ['mismatch']} "
              f"(inferred {summ['inferred_mismatch']}) | UNMATCHED {summ['unmatched']}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
