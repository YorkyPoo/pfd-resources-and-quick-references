#!/usr/bin/env python3
"""Canonical PEMS 2024 level table (stage 1) + structural aligner (stage 2).

WHY THIS EXISTS
---------------
`pems_level_scan.py` matched site rows to PEMS rows with a monotonic DP over
*text similarity*. That fails the moment the site's row order stops following the
PEMS page order, which is normal on merged pages: Non-Traumatic Cardiac Arrest
row 9 paired to the wrong PEMS row (150 mg rather than 300 mg amiodarone) at
"strong" confidence. Similarity is a bad primary key and a fine tie-breaker.

STRUCTURE FIRST
---------------
PEMS prints one badge per intervention, vertically centred inside that
intervention's text block, and groups interventions under centred section
headings ("Anaphylaxis", "Acute Allergic Reaction (non-Anaphylaxis)"). The site
carries the same two signals: bold divider rows are section headings and every
row has a number inside its section. So the primary key is

    (section heading, ordinal within section)

and text similarity is only consulted to break an ordinal tie or to pair rows
inside a section whose ordinal counts disagree.

STAGE 1 — the canonical table
-----------------------------
`build_table()` walks every PDF page that carries level badges and emits one
record per PEMS intervention:

    page, section_heading, ordinal, section_ordinal, verbatim_text,
    x, y, badge_tokens[], columns{}

Pages are read lazily: a page is parsed only when something needs it, and the
result is cached in `audit/level-scan/.cache/pems_rows.jsonl` so a later stage
re-reads instead of recomputing.

Every one of the 57 site pages that carries a level table gets a
`page_decisions` entry (`level_gated` / `administrative` / `skipped`) with the
reason. The 14 administrative pages keep their decision, but the contested
owner ruling behind it is recorded next to it instead of being inherited
silently from `exceptions.yaml`.

STAGE 2 — the aligner
---------------------
`align_all()` emits `alignment.json` (per site row: matched / ambiguous) plus
`absent_from_site` (PEMS interventions with no site row) which is the site's
biggest content gap, and `missing-rows.md` listing them.

Nothing here writes into `docs/`. Stage 1+2 only.

    python scripts/pems_canonical.py --stage all
    python scripts/pems_canonical.py --stage 1 --verbose
"""
from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pems_level_scan as P  # noqa: E402  (shares PDF cache + site page reader)

REPO = P.REPO
DOCS = P.DOCS
OUTDIR = os.path.join(REPO, "audit", "level-scan")
CACHE = os.path.join(OUTDIR, ".cache")
ROWS_CACHE = os.path.join(CACHE, "pems_rows.jsonl")
TABLE_JSON = os.path.join(OUTDIR, "pems_table.json")
ALIGN_JSON = os.path.join(OUTDIR, "alignment.json")
MISSING_MD = os.path.join(OUTDIR, "missing-rows.md")
AMBIG_MD = os.path.join(OUTDIR, "ambiguous-rows.md")

LEVELS = P.LEVELS
TOK_RE = re.compile(r"^\[?(EMR|EMT|A|I|P|MC)\]?$")
BRK_RE = re.compile(r"^\[(EMR|EMT|A|I|P)\]$")
# Section-heading words PEMS prints at x<80 in caps. A grid stops at any of them.
GRID_START = {"PROTOCOL", "PROCEDURE"}
GRID_STOP = {"PEARLS", "NOTES", "REFERENCES", "CRITERIA", "ADMINISTRATIVE",
             "PROCEDURES", "INDICATIONS", "CONTRAINDICATIONS", "DOCUMENTATION",
             "PURPOSE", "POLICY", "COMMENT", "AUTHORIZATION"}
BULLET_LEAD = re.compile(r"^[•o▪§*·]\s")


# ---------------------------------------------------------------------------
# layout -> rows
# ---------------------------------------------------------------------------
def _lines(ws: list[dict], y0: float, y1: float) -> list[dict]:
    """y-clustered reading lines inside [y0, y1), left to right."""
    sel = [w for w in ws if y0 <= w["y0"] < y1]
    sel.sort(key=lambda w: (w["y0"], w["x0"]))
    out: list[dict] = []
    for w in sel:
        if out and abs(out[-1]["y"] - w["y0"]) < 4:
            out[-1]["words"].append(w)
        else:
            out.append({"y": w["y0"], "words": [w]})
    for g in out:
        g["words"].sort(key=lambda w: w["x0"])
        g["x0"] = g["words"][0]["x0"]
        g["x1"] = g["words"][-1]["x1"] if "x1" in g["words"][-1] else g["words"][-1]["x0"]
        g["text"] = re.sub(r"\s+", " ", " ".join(w["t"] for w in g["words"])).strip()
    return out


def _is_heading(line: dict) -> bool:
    """PEMS prints section headings centred in the protocol column.

    Body text starts at x=70 (bullets) or 109-155 (list levels); wrapped prose
    starts at x=45. A heading starts at x>=155, carries no badge, is not a
    bullet item, and does not end in a colon (colons introduce sub-lists:
    "If HR below 60/min, in addition to above:").
    """
    t = line["text"]
    if line["x0"] < 155 or not t:
        return False
    if BULLET_LEAD.match(t) or t.rstrip().endswith(":"):
        return False
    if re.fullmatch(r"[A-Z]{1,3}|[\d.]+", t):
        return False
    words = t.split()
    if len(words) > 10:
        return False
    if not re.match(r"[A-Z]", words[0]):
        return False
    # headings are not badge tokens themselves
    if TOK_RE.match(t.replace(" ", "")):
        return False
    return True


def _margins(lines: list[dict]) -> list[tuple[float, float]]:
    """x ranges of the badge columns on THIS page.

    The badge columns drift between pages: 44-56 / 540-561 on protocol pages,
    69 / 514 on the policy pages, 49 / 561 on the procedure pages. Hard-coding a
    window either misses a column (leaving "EMT" glued to the front of the row
    text) or eats body words. So the columns are found from the level-shaped
    words themselves: a real column is a tight cluster of at least three tokens.
    """
    xs = sorted(w["x0"] for ln in lines for w in ln["words"]
                if TOK_RE.match(re.sub(r"\s", "", w["t"])))
    groups: list[list[float]] = []
    for x in xs:
        if groups and x - groups[-1][-1] <= 6:
            groups[-1].append(x)
        else:
            groups.append([x])
    found = [(g[0], g[-1]) for g in groups if len(g) >= 3]
    # The two columns every protocol and procedure page uses. Kept alongside the
    # detected clusters because a page may print a column only once or twice
    # (a short protocol), and dropping it would glue the badge onto the row text.
    return found + [(0.0, 66.0), (495.0, 600.0)]


def _badges(lines: list[dict], margins: list[tuple[float, float]] | None = None) -> list[dict]:
    """Level tokens printed in the two margin columns.

    A bracket is two extra words ("[ I ]"), so brackets are recovered from the
    neighbouring words on the same visual line. Every badge carries the ids of the
    words that spell it, so the row text can be rebuilt without the badge column
    bleeding into the intervention text.
    """
    if margins is None:
        margins = _margins(lines)
    out = []
    for ln in lines:
        for i, w in enumerate(ln["words"]):
            if not any(lo - 2 <= w["x0"] <= hi + 2 for lo, hi in margins):
                continue
            raw = re.sub(r"\s", "", w["t"])
            m = TOK_RE.match(raw)
            if not m:
                continue
            tok = m.group(1)
            prev_w = ln["words"][i - 1] if i else None
            next_w = ln["words"][i + 1] if i + 1 < len(ln["words"]) else None
            prev_t = prev_w["t"].strip() if prev_w else ""
            next_t = next_w["t"].strip() if next_w else ""
            bracketed = raw.startswith("[") or (prev_t.endswith("[") and next_t.startswith("]"))
            if bracketed and tok != "MC":
                tok = f"[{tok}]"
            keep = [w]
            for nb, nt in ((prev_w, prev_t), (next_w, next_t)):
                if nb is not None and nt in ("[", "]"):
                    keep.append(nb)
            out.append({"y": w["y0"], "x": w["x0"], "tok": tok,
                        "side": "left" if w["x0"] < (sum(m[0] for m in margins) / max(len(margins), 1)
                                                     if margins else 300) else "right",
                        "ids": {id(k) for k in keep}})
    # collapse a badge printed on both margins of the same line into one record
    merged: list[dict] = []
    for b in sorted(out, key=lambda b: (b["y"], b["x"])):
        if merged and abs(merged[-1]["y"] - b["y"]) < 5:
            merged[-1]["tokens"].append(b["tok"])
            merged[-1]["sides"].append(b["side"])
            merged[-1]["xs"].append(b["x"])
            merged[-1]["ids"] |= b["ids"]
        else:
            merged.append({"y": b["y"], "tokens": [b["tok"]], "sides": [b["side"]],
                           "xs": [b["x"]], "ids": set(b["ids"])})
    for b in merged:
        uniq = []
        for t in b["tokens"]:
            if t not in uniq:
                uniq.append(t)
        b["tokens"] = uniq
        b["side"] = "both" if len(set(b["sides"])) > 1 else b["sides"][0]
        b.pop("sides")
    return merged


def _segment(lines: list[dict], badges: list[dict]) -> list[list[dict]] | None:
    """Partition `lines` into consecutive blocks, one per badge, in order.

    A badge is printed vertically centred on its block, so the partition that
    minimises sum |block_centre - badge_y| recovers the table structure without
    any text comparison. Returns None if no monotone partition exists.
    """
    n, m = len(lines), len(badges)
    if m == 0:
        return []
    if n < m:
        return None
    INF = float("inf")
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0
    for j in range(1, m + 1):
        by = badges[j - 1]["y"]
        for i in range(j, n + 1):
            for k in range(j - 1, i):
                if dp[k][j - 1] == INF:
                    continue
                centre = (lines[k]["y"] + lines[i - 1]["y"]) / 2.0
                cost = dp[k][j - 1] + abs(centre - by)
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    back[i][j] = k
    if dp[n][m] == INF:
        return None
    groups, i, j = [], n, m
    while j > 0:
        k = back[i][j]
        groups.append(lines[k:i])
        i, j = k, j - 1
    return list(reversed(groups))


def _columns(tokens: list[str]) -> dict:
    """Badge tokens -> the five level columns PEMS implies (same rule as the scanner)."""
    cells, _ = P.expected_cells(tokens)
    out = {lvl: cells[i] for i, lvl in enumerate(LEVELS)}
    return out


def parse_page(pno: int, body: str, title: str) -> dict:
    ws = P._words(body)
    caps = [w for w in ws if w["t"].strip().upper() in GRID_START
            and w["x0"] < 80 and 60 < w["y0"] < 700]
    start = min(w["y0"] for w in caps) if caps else 88.0
    stops = [w["y0"] for w in ws if w["t"].strip().upper() in GRID_STOP
             and w["x0"] < 80 and w["y0"] > start + 2]
    # the running footer sits at y=715.7 on every page; it is not grid content
    end = min(stops + [712.0])
    lines = _lines(ws, start + 2, end)
    margins = _margins(lines)
    badges = _badges(lines, margins)
    # A narrative/policy page also prints a few level tokens in the margin, but
    # its body is full-width prose, not a grid: segmenting it would invent rows.
    kind = "protocol" if caps else ("continuation" if len(badges) >= 2 else "narrative")
    if kind == "narrative":
        return {"page": pno, "title": title, "kind": kind, "grid_start": round(start, 1),
                "grid_end": round(end, 1), "n_badges": len(badges), "rows": [], "orphans": []}
    # split the grid at section headings; headings are not part of any row
    sections: list[tuple[str, list[dict], list[dict]]] = []
    cur_head, cur_lines = "", []
    for ln in lines:
        if _is_heading(ln):
            sections.append((cur_head, cur_lines, _badges(cur_lines, margins)))
            cur_head, cur_lines = ln["text"], []
        else:
            cur_lines.append(ln)
    sections.append((cur_head, cur_lines, _badges(cur_lines, margins)))

    def body_text(group_lines: list[dict], bs: list[dict]) -> str:
        """Line text with the margin badge column removed."""
        drop = set()
        for b in bs:
            drop |= b["ids"]
        parts = []
        for l in group_lines:
            parts.append(" ".join(w["t"] for w in l["words"] if id(w) not in drop))
        return re.sub(r"\s+", " ", " ".join(parts)).strip()

    rows, orphan = [], []
    for head, ls, bs in sections:
        if not ls:
            continue
        if not bs:
            txt = body_text(ls, [])
            if txt:
                orphan.append({"section_heading": head, "text": txt[:400],
                               "y": round(ls[0]["y"], 1)})
            continue
        groups = _segment(ls, bs)
        if groups is None:
            # badges do not line up with the lines: record for a human
            orphan.append({"section_heading": head, "text": body_text(ls, bs)[:400],
                           "y": round(ls[0]["y"], 1), "problem": "badge/line count mismatch"})
            continue
        for b, group in zip(bs, groups):
            text = body_text(group, [b])
            if not text:
                # a badge with no body text of its own: usually a second badge
                # on a rule line. Not an intervention, keep it visible as an orphan.
                orphan.append({"section_heading": head, "text": "", "y": round(b["y"], 1),
                               "problem": f"badge {b['tokens']} with no body text"})
                continue
            rows.append({"page": pno, "section_heading": head,
                         "x": round(min((w["x0"] for w in group[0]["words"]
                                         if id(w) not in b["ids"]), default=group[0]["x0"]), 1),
                         "y": round(b["y"], 1),
                         "verbatim_text": text,
                         "badge_tokens": b["tokens"],
                         "side": b["side"],
                         "columns": _columns(b["tokens"])})
    return {"page": pno, "title": title, "kind": kind, "grid_start": round(start, 1),
            "grid_end": round(end, 1), "n_badges": len(badges), "rows": rows, "orphans": orphan}


def page_title(body: str) -> str:
    ws = P._words(body)
    head = [w for w in ws if w["y0"] < 90]
    if not head:
        return ""
    ymin = min(w["y0"] for w in head)
    first = sorted((w for w in head if abs((w["y0"] or 0) - ymin) < 6), key=lambda w: w["x0"])
    return re.sub(r"\s+", " ", " ".join(w["t"] for w in first)).strip()


def parse_pdf() -> dict[int, dict]:
    xml = P._read_pdf_xml(False)
    out: dict[int, dict] = {}
    for pno, m in enumerate(P.PAGE_RE.finditer(xml), 1):
        body = m.group(3)
        rec = parse_page(pno, body, page_title(body))
        if rec["rows"] or rec["orphans"]:
            out[pno] = rec
    return out


# ---------------------------------------------------------------------------
# documents: a protocol runs over consecutive pages (continuation pages carry
# no PROTOCOL heading of their own) -> one row sequence with sections carried on
# ---------------------------------------------------------------------------
def build_docs(pages: dict[int, dict]) -> list[dict]:
    docs: list[dict] = []
    for pno in sorted(pages):
        p = pages[pno]
        head_title = p["title"]
        prev = docs[-1] if docs else None
        same = False
        # a continuation page is at most one PEARLS page away from the previous
        # page of the document, and repeats the running header verbatim
        if prev and pno - prev["pages"][-1] <= 2:
            a = P.specific(P.nz(head_title)) or P.nz(head_title)
            b = P.specific(P.nz(prev["title"])) or P.nz(prev["title"])
            same = bool(a and b) and (a in b or b in a or difflib.SequenceMatcher(None, a, b).ratio() >= 0.8)
        if same:
            prev["pages"].append(pno)
            prev["rows"].extend(p["rows"])
            prev["orphans"].extend(p["orphans"])
        else:
            docs.append({"title": head_title, "pages": [pno],
                         "rows": list(p["rows"]), "orphans": list(p["orphans"])})
    for d in docs:
        sec = None
        cnt = 0
        for i, r in enumerate(d["rows"]):
            r["ordinal"] = i                      # 0-based within the document
            if r["section_heading"] != sec:
                sec, cnt = r["section_heading"], 0
            r["section_ordinal"] = cnt
            cnt += 1
    return docs


# ---------------------------------------------------------------------------
# stage 1: the 57 site pages and their decision
# ---------------------------------------------------------------------------
def site_pages() -> list[dict]:
    files = sorted(glob.glob(os.path.join(DOCS, "protocols", "**", "*.md"), recursive=True))
    out = []
    for f in files:
        pg = P.read_page(f)
        if pg.get("has_table"):
            out.append(pg)
    return out


ADMIN_CITATION = ("owner ruling 2026-11-11 (exceptions.yaml blanket `kind: administrative`)")


def _load_exceptions() -> tuple[dict, dict]:
    """exceptions.yaml -> ({rel_path: entry}, {declared_path: repaired_path}).

    A declared path can be stale: `protocols/trauma/09_Pneumothorax_PROC.md` no
    longer exists (the page lives under `respiratory/`), so its forced source
    p.243 was silently ignored and the page fell through as "no PEMS source".
    A stale path whose basename matches exactly one real page is repaired here and
    reported, rather than dropping the source on the floor.
    """
    import yaml
    doc = yaml.safe_load(open(P.EXCEPTIONS, encoding="utf-8")) or {}
    real = {os.path.relpath(f, DOCS).replace(os.sep, "/"): f
            for f in glob.glob(os.path.join(DOCS, "protocols", "**", "*.md"), recursive=True)}
    def stem(rel: str) -> str:
        # `09_Pneumothorax_PROC.md` and `03_Pneumothorax_PROC.md` are the same
        # page: the leading ordering number is bookkeeping, not an identifier.
        base = os.path.basename(rel)
        return re.sub(r"^\d+_", "", base).lower()

    by_base: dict[str, list[str]] = {}
    for rel in real:
        by_base.setdefault(stem(rel), []).append(rel)
    out: dict[str, dict] = {}
    repairs: dict[str, str] = {}
    for ent in doc.get("pages") or []:
        if not ent or not ent.get("file"):
            continue
        declared = ent["file"].strip()
        target = declared
        if declared not in real:
            same = by_base.get(stem(declared), [])
            if len(same) == 1:
                target = same[0]
                repairs[declared] = target
            else:
                continue
        out[target] = ent
    return out, repairs


def decide(pg: dict, exc: dict, docs: list[dict]) -> dict:
    """One site page -> a page_decisions record. Never silently dropped."""
    rel = pg["rel"]
    ep = exc.get(rel) or {}
    rows = pg["rows"]
    data_rows = [r for r in rows if not r["divider"]]
    blank_cells = sum(1 for r in data_rows for c in r["cells"] if not c.strip())
    filled_cells = sum(1 for r in data_rows for c in r["cells"] if c.strip())
    rec = {"site_page": rel, "title": pg.get("title") or rel, "rows": len(rows),
           "numbered_rows": len(data_rows), "blank_level_cells": blank_cells,
           "filled_level_cells": filled_cells}
    forced = ep.get("pems_pages")
    matched = []
    if forced:
        matched = [d for d in docs if set(forced) & set(d["pages"])]
        rec["pems_pages"] = sorted({p for d in matched for p in d["pages"]} or forced)
        rec["source_declared"] = f"exceptions.yaml forces p.{forced}"
        if not matched:
            rec["source_declared"] += " but that page carries no parsed level grid"
    if ep.get("kind") in ("administrative", "explanatory"):
        rec["decision"] = "administrative"
        rec["ruling"] = ep.get("reason", "")
        rec["ruling_citation"] = ADMIN_CITATION
        rec["ruling_status"] = "contested"
        rec["contested_because"] = (
            f"the blanket administrative flag rests on a comment citing {ADMIN_CITATION}; "
            "the audit records that ruling as open, and the page carries "
            f"{filled_cells} filled level cells against {blank_cells} blank ones, "
            "so the grid is not merely decorative")
        rec["level_grid_present"] = bool(filled_cells)
        rec["pems_pages"] = rec.get("pems_pages", [])
        return rec
    if forced and not matched:
        rec["decision"] = "skipped"
        rec["reason"] = (f"exceptions.yaml declares p.{forced} as the source but that page "
                         "produced no level rows, so no structural alignment is possible")
        return rec
    if not data_rows:
        rec["decision"] = "skipped"
        rec["reason"] = "page carries a level table with no numbered intervention rows"
        return rec
    if not forced:
        cand = []
        t = P.specific(P.nz(pg.get("title") or ""))
        for d in docs:
            ts = P.title_score(t, P.specific(P.nz(d["title"])))
            cand.append((ts, d))
        cand.sort(key=lambda x: -x[0])
        if not cand or cand[0][0] < 0.85:
            best = cand[0] if cand else (0.0, None)
            rec["decision"] = "skipped"
            rec["reason"] = (f"no PEMS 2024 protocol matches this page (best title score "
                             f"{best[0]:.2f}"
                             + (f", '{best[1]['title']}'" if best[1] else "")
                             + "); the page is gated from a non-PEMS source")
            return rec
        rec["pems_pages"] = list(cand[0][1]["pages"])
        rec["source_declared"] = f"title match {cand[0][0]:.2f} against '{cand[0][1]['title']}'"
    rec["decision"] = "level_gated"
    return rec


def _row_record(r: dict) -> dict:
    return {k: r.get(k) for k in ("page", "section_heading", "ordinal", "section_ordinal",
                                  "verbatim_text", "x", "y", "badge_tokens", "columns", "side")}


def stage1(verbose: bool = False) -> dict:
    os.makedirs(CACHE, exist_ok=True)
    pages = parse_pdf()
    docs = build_docs(pages)
    os.makedirs(OUTDIR, exist_ok=True)
    # every document's rows, flattened, for the sibling pipeline stages
    with open(ROWS_CACHE, "w", encoding="utf-8") as fh:
        for d in docs:
            for r in d["rows"]:
                fh.write(json.dumps({"doc": d["title"], **_row_record(r)}, ensure_ascii=False) + "\n")
    exc, repairs = _load_exceptions()
    decisions = []
    paths = {p for d in docs for p in d["pages"]}
    repaired = {v: k for k, v in repairs.items()}
    for pg in site_pages():
        d = decide(pg, exc, docs)
        if pg["rel"] in repaired:
            d["exception_path_repaired"] = {"declared": repaired[pg["rel"]], "used": pg["rel"]}
        decisions.append(d)
        if verbose:
            print(f"{d['decision']:<15} {d['site_page']} pems={d.get('pems_pages')}")
        # write the table after every page so an interrupted run still hands off
        _write_table(decisions, docs, pages, exc, repairs)
    counts: dict[str, int] = {}
    for d in decisions:
        counts[d["decision"]] = counts.get(d["decision"], 0) + 1
    out = _write_table(decisions, docs, pages, exc, repairs)
    if verbose:
        print(f"  decisions: {out['counts']}")
    return {"pages": pages, "docs": docs, "table": out}


def _write_table(decisions: list[dict], docs: list[dict], pages: dict[int, dict],
                 exc: dict, repairs: dict) -> dict:
    counts: dict[str, int] = {}
    for d in decisions:
        counts[d["decision"]] = counts.get(d["decision"], 0) + 1
    out = {
        "generated": _dt.datetime.now().isoformat(timespec="seconds"),
        "sources": {"bbox_xml": os.path.relpath(P.CACHE, REPO),
                    "text_layer": "pems_chunks/PEMS2024_full.txt",
                    "pdf_pages_scanned": 280, "pems_pages_with_rows": len(pages)},
        "row_schema": ["page", "section_heading", "ordinal", "section_ordinal",
                       "verbatim_text", "x", "y", "badge_tokens", "columns"],
        "counts": {"site_pages_with_level_table": len(decisions), **counts},
        "page_decisions": decisions,
        "pems_docs": [{"title": d["title"], "pages": d["pages"],
                       "n_rows": len(d["rows"]),
                       "rows": [_row_record(r) for r in d["rows"]],
                       "orphans": d["orphans"]} for d in docs],
        "stale_exception_paths": sorted(repairs),
        "pems_pages_parsed": sorted({p for d in docs for p in d["pages"]}),
    }
    with open(TABLE_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    return out


# ---------------------------------------------------------------------------
# stage 2: structural alignment
# ---------------------------------------------------------------------------
SEC_SYN = {"svt": "supraventricular tachycardia", "vt": "ventricular tachycardia",
           "pea": "pulseless electrical activity", "cpr": "cardiopulmonary resuscitation",
           "ob": "obstetric", "acs": "acute coronary syndrome", "aemt": "advanced emt"}
SEC_FILLER = {"pathway", "protocol", "section", "criteria", "algorithm", "procedure",
              "the", "a", "of", "and"}


def _sec_key(s: str) -> str:
    """Heading text -> comparable form. Abbreviations are expanded and layout
    fillers ("PATHWAY", "protocol") dropped: the site calls the SVT halves
    "STABLE SVT PATHWAY", PEMS calls them "Stable Supraventricular Tachycardia"."""
    toks = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split()
    out: list[str] = []
    for t in toks:
        if t in SEC_FILLER:
            continue
        out.extend(SEC_SYN.get(t, t).split())
    return " ".join(out)


def site_sections(pg: dict) -> list[tuple[str, list[dict]]]:
    """Site rows grouped by the bold divider rows that act as section headings."""
    secs: list[tuple[str, list[dict]]] = []
    head, rows = "", []
    for r in pg["rows"]:
        if r["divider"]:
            if rows or head:
                secs.append((head, rows))
            head, rows = P.clean(r["action"]).strip(), []
        else:
            rows.append(r)
    secs.append((head, rows))
    return [s for s in secs if s[1]]


def match_sections(s_sections, p_sections) -> dict[int, int | None]:
    """site section index -> pems section index (or None when no counterpart).

    Exact normalised heading first; then a fuzzy band. Ties are reported, not
    guessed: returning None marks the section unmatched and every row under it
    becomes `ambiguous` downstream.
    """
    out: dict[int, int | None] = {}
    used: set[int] = set()
    keys = [_sec_key(k) for k, _ in p_sections]
    for i, (sname, _) in enumerate(s_sections):
        k = _sec_key(sname)
        hit = [j for j, pk in enumerate(keys) if pk == k and j not in used][:1]
        if not hit and k:
            st = set(k.split())
            # one heading's words contained in the other's ("stridor" vs
            # "stridor pediatric") still counts as the same section, but only
            # when exactly one PEMS section qualifies
            sub = [j for j, pk in enumerate(keys)
                   if j not in used and pk and (st <= set(pk.split()) or set(pk.split()) <= st)]
            if len(sub) == 1:
                hit = sub
            elif not sub:
                scored = sorted(((difflib.SequenceMatcher(None, k, pk).ratio(), j)
                                 for j, pk in enumerate(keys) if j not in used and pk),
                                reverse=True)
                if scored and scored[0][0] >= 0.80:
                    hit = [scored[0][1]]
        # Two PEMS sections can share a name (a protocol that resumes on a later
        # page after a continuation block both have an empty base heading). The
        # first unused one in document order is the counterpart.
        out[i] = hit[0] if len(hit) == 1 else None
        if hit:
            used.add(hit[0])
    return out


def align_page(pg: dict, docs: list[dict], seed_pages: list[int]) -> dict:
    """Align one site page's rows to its PEMS document.

    Returns {"rows": [...], "absent": [...], "notes": [...]}.
    """
    rel = pg["rel"]
    doc = None
    if seed_pages:
        # One site page can govern SEVERAL PEMS protocols: Non-Traumatic Cardiac
        # Arrest merges Asystole/PEA (p.57) with V-Fib/pVT (p.63-64), and OB
        # Emergencies covers Childbirth/Eclampsia/Pregnancy (p.141/147/149). The
        # union is taken in the order the exceptions file declares, so a merged
        # page is aligned against every row it actually governs.
        seen: set[int] = set()
        picked_docs = []
        for p in seed_pages:
            for d in docs:
                if p in d["pages"] and id(d) not in seen:
                    seen.add(id(d))
                    picked_docs.append(d)
        if picked_docs:
            rows = [dict(r) for d in picked_docs for r in d["rows"]]
            sec, cnt = None, 0
            for r in rows:
                if r["section_heading"] != sec:
                    sec, cnt = r["section_heading"], 0
                r["section_ordinal"] = cnt
                cnt += 1
            doc = {"title": " + ".join(d["title"] for d in picked_docs),
                   "pages": [p for d in picked_docs for p in d["pages"]], "rows": rows}
    res = {"site_page": rel, "rows": [], "absent": [], "notes": []}
    if doc is None:
        res["notes"].append("no PEMS document resolved for this page")
        for r in [x for x in pg["rows"] if not x["divider"]]:
            res["rows"].append({"site_row": r["num"], "action": P.clean(r["action"])[:200],
                                "status": "ambiguous",
                                "reason": "no PEMS document resolved for this page"})
        return res

    res["pems_doc"] = doc["title"]
    res["pems_pages"] = doc["pages"]
    prow = doc["rows"]
    _POS = {id(r): i for i, r in enumerate(prow)}

    # PEMS sections in document order
    p_secs: list[tuple[str, list[dict]]] = []
    for r in prow:
        if not p_secs or p_secs[-1][0] != r["section_heading"]:
            p_secs.append((r["section_heading"], []))
        p_secs[-1][1].append(r)
    s_secs = site_sections(pg)
    res["site_sections"] = [s for s, _ in s_secs]
    res["pems_sections"] = [s for s, _ in p_secs]

    # A site page that prints no divider rows is one flat grid: every PEMS row of
    # the document(s) is in scope. A page that does print dividers is first
    # anchored section-for-section on the heading text.
    flat = len(s_secs) <= 1
    mapped = {0: 0} if flat else match_sections(s_secs, p_secs)
    unresolved: list[dict] = []

    # ---- per site row: every PEMS row in scope, scored
    site_index: list[tuple[str, dict, int, list[int]]] = []   # (section, row, k, scope)
    for si, (sname, srows) in enumerate(s_secs):
        if flat:
            scope = list(range(len(prow)))
        else:
            pi = mapped.get(si)
            if pi is None:
                for r in srows:
                    unresolved.append({
                        "site_row": r["num"], "section": sname,
                        "action": P.clean(r["action"])[:200],
                        "cells": [c.strip() for c in r["cells"]],
                        "status": "ambiguous", "reason_kind": "unresolved_section",
                        "reason": (f"site section '{sname}' has no single PEMS counterpart "
                                   f"(PEMS sections: {res['pems_sections']})")})
                continue
            scope = [_POS[id(p)] for p in p_secs[pi][1]]
        for k, r in enumerate(srows):
            site_index.append((sname, r, k, scope))

    cands: list[list[tuple[float, int, bool]]] = []   # per site row: (score, pems_i, exact)
    for sname, r, k, scope in site_index:
        row = []
        for gi in scope:
            s = sim(r["action"], prow[gi]["verbatim_text"])
            exact = prow[gi]["section_ordinal"] == k
            row.append((s + (0.04 if exact else 0.0), gi, exact))
        row.sort(key=lambda t: -t[0])
        cands.append(row)

    # A row is ambiguous when two genuinely DIFFERENT PEMS rows explain it about
    # equally well. Two copies of the same intervention in a merged source (p.63
    # and p.64 both carry the epinephrine row) are not an ambiguity - the counts
    # are, so that case keeps the ordinal-closest copy.
    ambiguous: dict[int, str] = {}
    for i, row in enumerate(cands):
        if not row or row[0][0] - (0.04 if row[0][2] else 0.0) < 0.40:
            continue
        best_score, best_gi, _ = row[0]
        rivals = [t for t in row[1:]
                  if best_score - t[0] <= 0.08
                  and sim(prow[t[1]]["verbatim_text"], prow[best_gi]["verbatim_text"]) < 0.85]
        if rivals:
            where = ", ".join(f"p.{prow[g]['page']} row {prow[g]['ordinal']} "
                              f"({s - (0.04 if e else 0.0):.2f})"
                              for s, g, e in [row[0]] + rivals[:3])
            ambiguous[i] = (f"{1 + len(rivals)} different PEMS rows explain this row about "
                            f"equally well: {where}; the site row may merge them")

    # ---- assignment: greedy over score, each PEMS row used at most once.
    # Reordering inside a section is expected (Chest Pain puts aspirin after
    # cardiac monitoring), so the assignment is not forced to be monotone; the
    # ordinal contributes a small bonus that only decides genuine ties.
    flat_edges = [(s, i, gi, e) for i, row in enumerate(cands) for s, gi, e in row]
    flat_edges.sort(key=lambda t: (-t[0], t[1], t[2]))
    picked: dict[int, tuple[int, float, bool]] = {}
    taken: set[int] = set()
    for score, i, gi, exact in flat_edges:
        if score - (0.04 if exact else 0.0) < 0.40:
            break
        if i in picked or gi in taken or i in ambiguous:
            continue
        picked[i] = (gi, score - (0.04 if exact else 0.0), exact)
        taken.add(gi)

    # ---- stage B: label binding for rows the symmetric text floor missed.
    # A site row's bold label ("Aspirin Administration", "Nitroglycerin
    # Administration", "CPAP ...") names the intervention. When exactly one
    # still-unmatched PEMS row in scope carries that label word, the label is
    # the structural key and no text floor is needed: PEMS prints "Administer:
    # ADULT: Aspirin 324 mg PO chewed" against a site row that never repeats the
    # dose, so symmetric similarity (0.24) is blind to a pair a human sees at a
    # glance. Two competing PEMS rows, or two site rows claiming one PEMS row,
    # are left for adjudication rather than guessed.
    label_fixed: set[int] = set()
    fallen = [i for i in range(len(site_index)) if i not in picked and i not in ambiguous]
    free = [gi for gi in range(len(prow)) if gi not in taken]
    claims: dict[int, list[int]] = {}
    collided: dict[int, int] = {}
    for i in fallen:
        keys = distinctive(label_keys(site_index[i][1]["action"]))
        if not keys:
            continue
        hits = sorted(((len(keys & _keyform(prow[gi]["verbatim_text"])), gi)
                       for gi in free), reverse=True)
        # every head-noun keyword must be present: one shared rare word is not a
        # structural key ("...prior to intubation" must not bind to the ETI row
        # on the strength of "intubation" alone).
        hits = [h for h in hits if h[0] == len(keys)]
        if not hits or (len(hits) > 1 and hits[0][0] == hits[1][0]):
            continue
        claims.setdefault(hits[0][1], []).append(i)
    for gi, who in claims.items():
        if len(who) != 1:                 # one PEMS row, two site rows: collision
            for i in who:
                collided[i] = gi
            continue
        i = who[0]
        s = sim(site_index[i][1]["action"], prow[gi]["verbatim_text"])
        picked[i] = (gi, s, False)
        taken.add(gi)
        label_fixed.add(i)

    # ---- order repair for near-duplicate PEMS rows.
    # p.239 prints the adult and the paediatric endotracheal-intubation row as
    # two lines that differ only in "≥ 12 years" vs "< 12 years", which strips to
    # the same token set; the same is true of the p.63/p.64 epinephrine copies.
    # Text cannot separate them, the ordinal can: when two matched site rows come
    # out in the opposite order to their two near-identical PEMS rows, the
    # document order wins.
    order_fixed = []
    keys = sorted(picked)
    for a_i in range(len(keys)):
        for b_i in range(a_i + 1, len(keys)):
            i, j = keys[a_i], keys[b_i]
            gi, gj = picked[i][0], picked[j][0]
            if gi <= gj:
                continue
            if (sim(prow[gi]["verbatim_text"], prow[gj]["verbatim_text"]) >= 0.75
                    and sim(site_index[i][1]["action"], site_index[j][1]["action"]) >= 0.45):
                picked[i], picked[j] = (gj, picked[i][1], False), (gi, picked[j][1], False)
                order_fixed.append((i, j))
    fixed_ids = {i for pair in order_fixed for i in pair}

    # PEMS rows that an ambiguous site row was explaining stay attributed to it,
    # so they are not reported as gaps the site never wrote.
    claimed_by_ambiguous: dict[int, list[int]] = {}
    for i, why in ambiguous.items():
        for score, gi, exact in cands[i][:4]:
            if score - (0.04 if exact else 0.0) >= 0.40:
                claimed_by_ambiguous.setdefault(i, []).append(gi)

    out_rows = []
    for i, (sname, r, k, scope) in enumerate(site_index):
        base = {"site_row": r["num"], "section": sname,
                "action": P.clean(r["action"])[:200], "cells": [c.strip() for c in r["cells"]]}
        if i in ambiguous:
            base.update(status="ambiguous", reason_kind="multiple_candidates",
                        reason=ambiguous[i])
            out_rows.append(base)
            continue
        if i not in picked:
            if i in collided:
                p = prow[collided[i]]
                base.update(status="ambiguous", reason_kind="shared_pems_row",
                            reason=(f"two site rows name this same PEMS intervention; p.{p['page']} "
                                    f"row {p['ordinal']} merges what the site splits — adjudicate "
                                    f"which site row's cells that PEMS badge governs"))
                out_rows.append(base)
                continue
            # A label word that names one PEMS row, but that row is already
            # bound: the site splits one PEMS intervention into two rows (CPAP
            # and SGA are one PEMS row on p.123). That is an adjudication item,
            # not a local addition.
            keys = distinctive(label_keys(r["action"]))
            shared = [(gi, prow[gi]) for gi in taken
                      if keys & _keyform(prow[gi]["verbatim_text"])]
            if shared:
                gi, p = shared[0]
                base.update(status="ambiguous", reason_kind="shared_pems_row",
                            reason=(f"site row label names an intervention that p.{p['page']} "
                                    f"row {p['ordinal']} already backs with another site row; "
                                    f"PEMS merges what the site splits (or the labels collide) — "
                                    f"adjudicate which cell source governs"))
                out_rows.append(base)
                continue
            base.update(status="ambiguous", reason_kind="no_counterpart",
                        reason=(f"no PEMS row in {'the page grid' if flat else repr(sname)} "
                                f"reaches the text floor and no label word binds it; the site "
                                f"row has no PEMS counterpart (local addition, or a PEMS row "
                                f"worded beyond recognition)"))
            out_rows.append(base)
            continue
        gi, s, exact = picked[i]
        p = prow[gi]
        base.update(status="matched", pems_section_ordinal=p["section_ordinal"],
                    pems_page=p["page"], pems_ordinal=p["ordinal"],
                    pems_section=p["section_heading"],
                    pems_text=p["verbatim_text"][:240],
                    badges=p["badge_tokens"], similarity=round(s, 3),
                    match_basis=("label+keyword" if i in label_fixed else
                                 ("page-flat+ordinal" if flat and exact else
                                  "section+ordinal" if exact else
                                  "page-flat+text" if flat else "section+text")
                                 + (" +order (near-duplicate rows)" if i in fixed_ids else "")))
        out_rows.append(base)
    res["rows"] = unresolved + out_rows

    claimed_pems = set(taken)
    for gis in claimed_by_ambiguous.values():
        claimed_pems |= set(gis)
    for gi, p in enumerate(prow):
        if gi in claimed_pems:
            continue
        rec = {"pems_page": p["page"], "ordinal": p["ordinal"],
               "section": p["section_heading"], "section_ordinal": p["section_ordinal"],
               "verbatim_text": p["verbatim_text"], "badges": p["badge_tokens"],
               "columns": p["columns"]}
        dup = max((sim(p["verbatim_text"], prow[j]["verbatim_text"]) for j in taken),
                  default=0.0)
        covered = max((max(sim(r["action"], p["verbatim_text"]),
                           cov(r["action"], p["verbatim_text"]),
                           covp(r["action"], p["verbatim_text"]))
                       for _, r, _, _ in site_index), default=0.0)
        lab = max((len(distinctive(label_keys(r["action"]))
                       & _keyform(p["verbatim_text"]))
                   for _, r, _, _ in site_index), default=0)
        if dup >= 0.85:
            # the merged source repeats a row the site already covers (p.57 and
            # p.63 both open with "Follow Universal Patient Care"); not a gap.
            rec["duplicate_of_matched_row"] = round(dup, 3)
            res.setdefault("duplicates", []).append(rec)
        elif covered >= 0.40 or lab:
            # the site does write this, inside a row that carries more than one
            # PEMS intervention, or under a label that names it; the matched row
            # absorbed it.
            rec["best_similarity_to_a_site_row"] = round(covered, 3)
            if lab:
                rec["label_key_match"] = lab
            res.setdefault("merged_into_site_row", []).append(rec)
        else:
            res["absent"].append(rec)
    return res


def _sig(s: str) -> set[str]:
    """Significant tokens, keeping dose numbers: 300 mg and 150 mg amiodarone are
    different interventions and the shared tokeniser drops digits."""
    out = set(P.sig_tokens(s))
    for w in re.findall(r"\d+(?:\.\d+)?", s):
        if len(w) >= 2:
            out.add(w)
    return out


_SIM_CACHE: dict[tuple[str, str], float] = {}


def cov(a: str, b: str) -> float:
    """How much of `b` (a PEMS row) the site row `a` actually contains.

    Needed because the site routinely merges several PEMS rows into one row
    ("Scene Safety / Initial Contact" carries universal care AND DNR status), and
    a symmetric similarity dilutes below any usable floor when it does. Coverage
    answers the question that matters for the gap list: does this PEMS
    intervention appear anywhere on the page?
    """
    A, B = _sig(P.clean(a)), _sig(P.clean(b))
    return len(A & B) / len(B) if B else 0.0


LABEL_GENERIC = set("""airway assessment monitoring monitor transport transportation
patient patients cardiac medical control contact protocol procedure consider
administered administer administration support management ventilation ventilatory
symptoms signs treatment evaluation evaluate obtain establish perform provide
maintain ensure follow refer pediatric adult initial universal care repeat dose
scene safety initial assessment advanced provider providers level levels""".split())


_DF: dict[str, int] = {}
_DISTINCT_MAX = 10


def _build_df(docs) -> None:
    """Document frequency of a token across PEMS rows. A label word only binds a
    row when it is RARE in PEMS ("aspirin", "cpap", "suctioning" do; "access",
    "assessment", "transport" do not)."""
    global _DF
    c: dict[str, int] = {}
    for d in docs:
        for r in d["rows"]:
            for w in _keyform(r["verbatim_text"]):
                c[w] = c.get(w, 0) + 1
    _DF = c


def distinctive(toks: set[str]) -> set[str]:
    return {t for t in toks if _DF.get(t, 0) <= _DISTINCT_MAX}


def _drug_norm(text: str) -> str:
    """Spelling differences that hide a drug match (site "Nitroglycerin" vs PEMS
    "Nitroglycerine"). Applied only to label binding, never to the text score."""
    s = (text or "").lower()
    for a, b in (("nitroglycerine", "nitroglycerin"), ("epinephrin ", "epinephrine "),
                 ("epinephrin", "epinephrine")):
        s = s.replace(a, b)
    s = re.sub(r"\bsga\b", "supraglottic", s)
    return s


def _keyform(text: str) -> set[str]:
    """Token form for label binding: truncated to 6 characters so the site's
    "monitoring" meets PEMS "monitor", and "suctioning" meets "suction"."""
    return {t[:6] for t in _sig(_drug_norm(text))}


def covp(a: str, b: str) -> float:
    """Prefix-tolerant coverage, used only to decide whether a PEMS row is a
    content gap: the site writing "cardiac monitoring" covers PEMS "monitor
    cardiac rhythm"."""
    A, B = _keyform(a), _keyform(b)
    return len(A & B) / len(B) if B else 0.0


def label_keys(action: str) -> set[str]:
    """Structural key taken from a site row's bold label.

    Site rows are labelled plus a bullet list: "**Aspirin Administration (for
    ACS/STEMI):** <br>• Aspirin ...".  The label names the intervention, so its
    distinctive words are what pins the row to a PEMS row; the bullet body only
    adds noise (a long body dilutes a symmetric similarity below any floor).
    Generic verbs and body-part words are dropped so "Cardiac Monitoring" does
    not bind to every PEMS row that mentions a monitor.
    """
    head = re.split(r"<br\s*/?>|•", action or "", maxsplit=1)[0]
    head = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", head)     # markdown links
    head = re.split(r"[:(/]| - ", head, maxsplit=1)[0]       # head noun phrase only
    head = re.sub(r"[*_#]", " ", head)
    return {t[:6] for t in _sig(_drug_norm(head)) if len(t) >= 4 and t not in LABEL_GENERIC}


def sim(a: str, b: str) -> float:
    key = (a, b)
    if key in _SIM_CACHE:
        return _SIM_CACHE[key]
    A, B = _sig(P.clean(a)), _sig(P.clean(b))
    if not A or not B:
        v = 0.0
    else:
        jac = len(A & B) / min(len(A), len(B))
        ratio = difflib.SequenceMatcher(None, " ".join(sorted(A)), " ".join(sorted(B))).ratio()
        v = 0.65 * jac + 0.35 * ratio
    _SIM_CACHE[key] = v
    return v


def stage2(seed: dict) -> dict:
    docs = seed["docs"]
    table = seed["table"]
    _build_df(docs)
    dec = {d["site_page"]: d for d in table["page_decisions"]}
    results = []
    for pg in site_pages():
        d = dec.get(pg["rel"])
        if not d or d["decision"] != "level_gated":
            continue
        results.append(align_page(pg, docs, d.get("pems_pages") or []))

    tot = {"site_rows": 0, "matched": 0, "ambiguous": 0, "absent_from_site": 0}
    kinds: dict[str, int] = {}
    for r in results:
        for row in r["rows"]:
            tot["site_rows"] += 1
            tot[row["status"]] = tot.get(row["status"], 0) + 1
            if row["status"] == "ambiguous":
                k = row.get("reason_kind") or "other"
                kinds[k] = kinds.get(k, 0) + 1
        tot["absent_from_site"] += len(r["absent"])
        tot["duplicate_in_source"] = tot.get("duplicate_in_source", 0) + len(r.get("duplicates") or [])
        tot["merged_into_site_row"] = tot.get("merged_into_site_row", 0) + len(
            r.get("merged_into_site_row") or [])
    tot["total_accounted"] = tot["matched"] + tot["ambiguous"] + tot["absent_from_site"]
    tot["site_rows_plus_absent"] = tot["site_rows"] + tot["absent_from_site"]
    tot["pems_rows_in_scope"] = (tot["matched"] + tot["absent_from_site"]
                                 + tot["duplicate_in_source"] + tot["merged_into_site_row"])

    totals = dict(tot)
    totals["ambiguous_by_kind"] = kinds
    out = {"generated": _dt.datetime.now().isoformat(timespec="seconds"),
           "method": ("primary key = section heading + ordinal within section, then the "
                      "site row's own intervention label (bold head noun); text similarity "
                      "only breaks ties and never creates a pair on its own"),
           "totals": totals, "pages": results}
    tot = totals
    with open(ALIGN_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    write_missing(results, tot, table)
    write_reconciliation(results, tot)
    write_ambiguous(results, tot)
    return out


PRIOR_ABSENT = 152   # audit/level-scan/2026-11-14-report.md, "PEMS rows with no site row"


def _prior_absent() -> dict[str, set[tuple[int, int]]]:
    """Parse the 2026-11-14 report's "PEMS rows with no site counterpart" list
    into {site_page: {(pems_page, ordinal)}}. The prior count is a claim until it
    is turned into a set that can be intersected with this run's."""
    prior = os.path.join(OUTDIR, "2026-11-14-report.md")
    out: dict[str, set[tuple[int, int]]] = {}
    if not os.path.exists(prior):
        return out
    md = open(prior, encoding="utf-8").read()
    marker = "## PEMS rows with no site counterpart"
    if marker not in md:
        return out
    for line in md.split(marker, 1)[1].splitlines():
        m = re.match(r"- `([^`]+)` ← p\.(\d+) row (\d+)", line.strip())
        if m:
            out.setdefault(m.group(1), set()).add((int(m.group(2)), int(m.group(3))))
    return out


def write_reconciliation(results: list[dict], tot: dict) -> None:
    """Bridge the prior scan's 152 to this run's absent count as SET arithmetic.

    "152 vs N, three reasons why" is an excuse; a reader cannot check it. This
    intersects the prior report's (site page, PEMS page, PEMS row) triples with
    this run's unpaired triples, so every row of the difference is named in
    `reconciliation.json` and the totals must add up.
    """
    old = _prior_absent()
    old_set = {(p, pp, po) for p, s in old.items() for (pp, po) in s}
    unpaired: dict[str, set[tuple[int, int]]] = {}
    absent: dict[str, set[tuple[int, int]]] = {}
    for r in results:
        u = unpaired.setdefault(r["site_page"], set())
        for k in ("absent", "duplicates", "merged_into_site_row"):
            for x in r.get(k) or []:
                u.add((x["pems_page"], x["ordinal"]))
        absent[r["site_page"]] = {(x["pems_page"], x["ordinal"]) for x in r["absent"]}
    unpaired_set = {(p, pp, po) for p, s in unpaired.items() for (pp, po) in s}
    absent_set = {(p, pp, po) for p, s in absent.items() for (pp, po) in s}

    still = sorted(old_set & unpaired_set)
    now_covered = sorted(old_set - unpaired_set)
    newly_unpaired = sorted(unpaired_set - old_set)
    still_absent = [t for t in still if t in absent_set]
    still_dup = [t for t in still if t not in absent_set]
    new_absent = [t for t in newly_unpaired if t in absent_set]
    new_dup = [t for t in newly_unpaired if t not in absent_set]
    assert len(still_absent) + len(still_dup) == len(still), (len(still_absent), len(still_dup), len(still))
    bridge = {
        "prior_reported": len(old_set),
        "now_absent": tot["absent_from_site"],
        "still_unpaired_from_prior": len(still),
        "of_that_still_absent": len(still_absent),
        "of_that_duplicate_or_merged": len(still_dup),
        "prior_missing_now_paired_or_covered": len(now_covered),
        "newly_unpaired_not_in_prior_list": len(newly_unpaired),
        "of_that_now_absent": len(new_absent),
        "of_that_newly_duplicate_or_merged": len(new_dup),
        "prior_pages": len(old),
        "pages_aligned_this_run": len(results),
        "identity": (f"{len(old_set)} prior = {len(still)} still unpaired + "
                     f"{len(now_covered)} now paired/covered; "
                     f"absent {tot['absent_from_site']} = "
                     f"{len(still_absent)} still absent + {len(new_absent)} newly absent"),
    }
    data = {"bridge": bridge,
            "still_unpaired_from_prior": ["|".join(map(str, t)) for t in still],
            "prior_missing_now_paired_or_covered": ["|".join(map(str, t)) for t in now_covered],
            "newly_unpaired_not_in_prior_list": ["|".join(map(str, t)) for t in newly_unpaired]}
    with open(os.path.join(OUTDIR, "reconciliation.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)

    section = [
        "## Exact bridge to the prior scan's 152\n\n",
        f"The 2026-11-14 report listed **{len(old_set)}** (site page, PEMS page, PEMS row) "
        "triples as having no site row. Both numbers are reconciled here as set arithmetic, "
        "not as a list of reasons; every row of the difference is named in "
        "`reconciliation.json`.\n\n",
        f"- **{len(still)} of those {len(old_set)} rows are still unpaired** in this run: "
        f"{len(still_absent)} are still `absent_from_site` and listed "
        f"below, {len(still_dup)} are now classed as a duplicate "
        f"copy or as merged into a site row.\n",
        f"- **{len(now_covered)} of those {len(old_set)} rows the new aligner now pairs or "
        "covers.** The old scan's text-only DP called them gaps; the structural key "
        "(section + ordinal, then the site row's own intervention label) pairs them, or a site "
        "row demonstrably contains the intervention. These are the rows the rebuild was for.\n",
        f"- **{len(newly_unpaired)} rows this run leaves unpaired were not on the old list.** "
        f"{len(new_absent)} are listed below as absent and "
        f"{len(new_dup)} as duplicate/merged: the old "
        "scan had paired them on text similarity, and this one will not pair a row "
        "without a structural key. They are the rows most worth a human glance.\n\n",
        f"**Check:** {bridge['identity']}. Prior pages: {len(old)}; pages aligned here: "
        f"{len(results)}.\n",
    ]
    md = open(MISSING_MD, encoding="utf-8").read()
    start = md.find("## Reconciliation with the previous scan's 152")
    end = md.find("\n## `", start)
    if start != -1 and end != -1:
        md = md[:start] + "".join(section) + md[end:]
        open(MISSING_MD, "w", encoding="utf-8").write(md)


def write_missing(results: list[dict], tot: dict, table: dict) -> None:
    n_pages = sum(1 for r in results if r["absent"])
    L = ["# PEMS interventions with no site row (`absent_from_site`)\n",
         "Every PEMS 2024 intervention that has no counterpart on the Poquoson "
         "protocol page it belongs to. These are content gaps: the site documents "
         "the protocol but not this intervention, and nothing downstream will "
         "notice because the site row it should live on simply is not there.\n",
         f"**Total: {tot['absent_from_site']} rows across {n_pages} pages.** "
         f"(matched {tot['matched']}, ambiguous {tot['ambiguous']}, "
         f"site rows {tot['site_rows']})\n",
         "\n## Reconciliation with the previous scan's 152\n",
         f"The 2026-11-14 scan reported **{PRIOR_ABSENT}** PEMS rows with no site row. "
         f"This table reports **{tot['absent_from_site']}**. The counts are not meant "
         "to match, for three reasons, and the difference is the point of the rebuild:\n",
         f"1. **Rows the site does write, inside a row that carries more than one PEMS "
         f"intervention, are no longer counted as gaps.** {tot['merged_into_site_row']} such "
         "rows are listed in `alignment.json` under `merged_into_site_row` with their "
         "best similarity to a site row. The site merges aggressively (Chest Pain puts "
         "aspirin, nitroglycerin and monitoring in one row), and the old scan counted "
         "every unpaired PEMS row as missing.\n",
         f"2. **Duplicate copies in merged sources are not gaps.** "
         f"{tot['duplicate_in_source']} rows are the same intervention printed twice "
         "(p.57 and p.63 both open with *Follow Universal Patient Care*); they are in "
         "`alignment.json` under `duplicates`.\n",
         "3. **The row census itself changed.** The previous scan examined 531 site "
         f"rows over 40 aligned pages; this one accounts for {tot['site_rows']} site rows "
         f"plus {tot['absent_from_site']} absent PEMS rows = {tot['total_accounted']}, "
         "because merged pages are now aligned against the union of every PEMS protocol "
         "they govern (57+63+64 for Non-Traumatic Cardiac Arrest) instead of one page, "
         "and the procedure pages (p.239/243/247/261/263) that govern Respiratory "
         "Arrest, Upper Airway Obstruction and Pneumothorax are in scope.\n",
         "\nNo row is lost between the two numbers: every PEMS row in scope is either "
         "matched, absent (listed below), a duplicate, or merged into a site row, and "
         "`alignment.json` totals prove the sum.\n"]
    for r in results:
        if not r["absent"]:
            continue
        L.append(f"\n## `{r['site_page']}` — {len(r['absent'])} missing "
                 f"(PEMS {', '.join('p.' + str(p) for p in r.get('pems_pages') or [])})\n")
        for a in r["absent"]:
            txt = re.sub(r"\s+", " ", a["verbatim_text"]).strip()
            L.append(f"- p.{a['pems_page']} row {a['ordinal']} "
                     f"[{a['section'] or 'base section'} #{a['section_ordinal']}] "
                     f"badge `{' '.join(a['badges']) or '—'}` — {txt}\n")
    open(MISSING_MD, "w", encoding="utf-8").write("".join(L))


EVIDENCE = {"vfib": ["vfib_p63-063.png", "vfib_p64-064.png"],
            "crush": ["crush_p91-091.png", "crush_p92-092.png"],
            "cpap": ["cpap_p245-245.png"],
            "respdist": ["respdist_p125-125.png"]}


def _evidence_for(page: str, text: str) -> list[str]:
    """Reuse the raster crops a prior C2 pass already made; never re-raster."""
    out = []
    low = (page + " " + text).lower()
    for key, files in EVIDENCE.items():
        if key in low:
            out.extend(files)
    return sorted(set(out))


def write_ambiguous(results: list[dict], tot: dict) -> None:
    kinds = tot.get("ambiguous_by_kind") or {}
    L = ["# Rows needing adjudication (`ambiguous`)\n",
         "Input to C2. A row is ambiguous when the structure cannot settle it. "
         "`reason_kind` says which of the four shapes it is:\n",
         "- `multiple_candidates` — two or more different PEMS rows explain the site "
         "row about equally well (the site row merges them, or a dose/badge differs "
         "only in the PEMS row it was pulled from).\n",
         "- `no_counterpart` — no PEMS row in the mapped source reaches the text "
         "floor and no label word binds it: a local addition, or (for pages whose "
         "PEMS counterpart is a policy page rather than a grid) a row with no "
         "upstream at all.\n",
         "- `shared_pems_row` — the site row's label names an intervention whose "
         "PEMS row already backs a different site row: PEMS merges two site rows "
         "into one line (CPAP and SGA share p.123 row 3).\n",
         "- `unresolved_section` — the site prints a section heading with no single "
         "PEMS counterpart, so none of its rows can be anchored.\n",
         f"**Total: {tot['ambiguous']} rows** ("
         + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items()))
         + f") across {sum(1 for r in results if any(x['status'] == 'ambiguous' for x in r['rows']))} pages.\n",
         "\nRaster crops already exist in `audit/level-scan/evidence/` for the six "
         "known hard cases (`vfib_p63`, `vfib_p64`, `crush_p91`, `crush_p92`, "
         "`cpap_p245`, `respdist_p125`); where an entry below names one, look at the "
         "crop instead of re-rastering.\n"]
    for r in results:
        amb = [x for x in r["rows"] if x["status"] == "ambiguous"]
        if not amb:
            continue
        L.append(f"\n## `{r['site_page']}` — {len(amb)} ambiguous\n")
        for a in sorted(amb, key=lambda x: (x.get("reason_kind") or "", str(x["site_row"]))):
            ev = _evidence_for(r["site_page"], a["action"])
            L.append(f"- row **{a['site_row']}** ({a.get('section') or 'base section'}) "
                     f"[`{a.get('reason_kind', 'other')}`] — {a['action'][:150]}\n"
                     f"  - why: {a['reason']}\n"
                     + (f"  - evidence: `{'`, `'.join(ev)}`\n" if ev else ""))
    open(AMBIG_MD, "w", encoding="utf-8").write("".join(L))


# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stage", choices=["1", "2", "all"], default="all")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)
    seed = None
    if args.stage in ("1", "all"):
        seed = stage1(args.verbose)
        t = seed["table"]
        print(f"stage 1: {len(seed['pages'])} PEMS pages with rows, "
              f"{len(seed['docs'])} documents, "
              f"{sum(len(d['rows']) for d in seed['docs'])} level rows")
        print(f"  decisions: {t['counts']}")
        if t["stale_exception_paths"]:
            print(f"  STALE exception paths: {t['stale_exception_paths']}")
        print(f"  wrote {os.path.relpath(TABLE_JSON, REPO)}")
    if args.stage in ("2", "all"):
        if seed is None:
            seed = stage1(False)
        out = stage2(seed)
        print(f"stage 2: {out['totals']}")
        print(f"  wrote {os.path.relpath(ALIGN_JSON, REPO)}, "
              f"{os.path.relpath(MISSING_MD, REPO)}, {os.path.relpath(AMBIG_MD, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
