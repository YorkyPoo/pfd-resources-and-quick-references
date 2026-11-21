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
import collections
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
OVERRIDES_YAML = os.path.join(OUTDIR, "badge-overrides.yaml")
SPLITS_YAML = os.path.join(OUTDIR, "row-splits.yaml")
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
    if caps:
        start = min(w["y0"] for w in caps)
    else:
        # A continuation page prints no PROTOCOL heading, and its grid can open
        # with a SECTION heading a few points above the default 88pt start
        # (p.252 "Total Artificial Heart (TAH)", p.258 "INTRAMUSCULAR (IM)").
        # That heading belongs to the grid: dropped, the rows under it read as an
        # unnamed section continuing the previous page's section, and the site
        # section they really belong to loses them. Page furniture in the same
        # band ("CLASS: ...", "CRITERIA", table-of-contents lines) starts at
        # x<155 and is not heading-shaped, so it is not picked up here.
        start = 88.0
        band = [ln for ln in _lines(ws, 55.0, 88.0)
                if ln["x0"] >= 155 and _is_heading(ln)]
        if band:
            # -2 because the grid slice below starts at `start + 2`; the heading
            # itself must be inside the slice to open the section.
            start = min(ln["y"] for ln in band) - 2.0
    stops = [w["y0"] for w in ws if w["t"].strip().upper() in GRID_STOP
             and w["x0"] < 80 and w["y0"] > start + 2]
    # the running footer sits at y=715.7 on every page; it is not grid content
    end = min(stops + [712.0])
    lines = _lines(ws, start + 2, end)
    margins = _margins(lines)
    badges = _badges(lines, margins)
    # A page carrying ANY level badge group is a grid page. With no PROTOCOL
    # heading of its own it is a continuation: p.78 prints exactly ONE badged
    # row (the Pain Control MC escalation) and the old `>= 2` test classed it
    # narrative, silently discarding the row — the sole badged row in all 280
    # pages that the extractor dropped. Only a page with NO badge group at all
    # is narrative prose.
    kind = "protocol" if caps else ("continuation" if badges else "narrative")
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
def _merge_page_break_sections(doc: dict) -> None:
    """Give a section that resumes after a page break back to the section it
    interrupts.

    PEMS prints a section heading once. When the section runs past the bottom of
    the page it resumes at the top of the next page with NO heading, so read
    literally it is a new, unnamed section. That is not a cosmetic difference:
    the site's UNSTABLE SVT section maps to the p.135 half only, and the
    cardioversion rows printed on p.136 then belong to no site section at all —
    they are never scored against the site rows that describe them.

    The test is structural, never per-protocol: the run's heading is empty, its
    first row is the first row of its page in this document (so it starts a new
    page), and the heading printed above it is a named one. A heading that the
    page really prints (p.252 "Total Artificial Heart (TAH)", p.258
    "INTRAMUSCULAR (IM)") is parsed as a heading by `parse_page`, so it never
    looks like a continuation.
    """
    rows = doc["rows"]
    merged: list[dict] = []
    notes: list[dict] = []
    pages_seen: set[int] = set()
    i = 0
    while i < len(rows):
        j = i + 1
        while j < len(rows) and rows[j]["section_heading"] == rows[i]["section_heading"]:
            j += 1
        run = rows[i:j]
        head = run[0]["section_heading"]
        prev_head = merged[-1]["section_heading"] if merged else ""
        if not head and prev_head and run[0]["page"] not in pages_seen:
            from_page = merged[-1]["page"]
            for r in run:
                r = dict(r)
                r["section_heading"] = prev_head
                r["section_continued"] = True
                merged.append(r)
            notes.append({"heading": prev_head, "from_page": from_page,
                          "to_page": run[0]["page"], "rows": len(run)})
        else:
            merged.extend(run)
        pages_seen.update(r["page"] for r in run)
        i = j
    doc["rows"] = merged
    if notes:
        doc["section_continuations"] = notes


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
        _merge_page_break_sections(d)
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
# `scripts/level_rule.py` rewrote every protocol page's level matrix to the
# one-chip table `| # | Level | Action / Intervention |` (and the administrative
# pages to `| # | Basis | ... |` with a POLICY chip). `pems_level_scan.read_page()`
# only understands the legacy 7-column matrix, so on a converted page it returns
# `has_table: False` — not "the page lost its table" but "this reader never looked".
# Asked in November 2026, that reader saw 2 tables instead of 55 and stage 1 wrote
# page_decisions for 4 pages; stage 2 then reported 0 site rows.
#
# This reader accepts both formats. It mirrors `read_action_rows()` and widens
# the chip column to `Basis` so an administrative POLICY page is still a page
# with a table. A chip is turned into the same 5-cell spread the legacy matrix
# encoded (`chip_cells`), a `POLICY`/`PENDING` chip into five blanks, so every
# downstream consumer keeps seeing the shape it always saw.
SITE_HDR_RE = re.compile(r"^\|\s*#\s*\|\s*(?:Level|Basis)\s*\|\s*Action\s*/\s*Intervention\s*\|\s*$")
SITE_CHIP_RE = re.compile(r'<span class="lvl lvl-([a-z]+)">([A-Z]+)</span>')
NOT_A_PROTOCOL_PAGE = {"protocols/outstanding-decisions.md"}


def _site_rows_collapsed(path: str) -> list[dict] | None:
    """Rows of a one-chip table page, in the legacy row shape, or None."""
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    rows: list[dict] = []
    for i, line in enumerate(lines):
        if not SITE_HDR_RE.match(line.strip()):
            continue
        for raw in lines[i + 2:]:
            s = raw.strip()
            if not s.startswith("|"):
                break
            c = P.cells(raw)
            if len(c) < 3 or all(set(x) <= set(":- ") for x in c):
                continue
            m = SITE_CHIP_RE.search(c[1])
            lvl = m.group(2) if m else ""
            # `cells` keeps the legacy 5-cell cumulative spread: `levels()`,
            # text-binding and the C2 scope check all read a non-blank cell as
            # "this level and every level above it". `chip` is the published
            # level itself, which is what `decide()` counts (see the note there).
            rows.append({"idx": len(rows), "num": c[0], "action": c[2],
                         "cells": P.chip_cells(lvl), "chip": lvl, "ncols": 3,
                         "divider": P.is_divider(c[0], P.clean(c[2]))})
    return rows or None


def _site_title(path: str) -> str:
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines()[:40]:
        if line.startswith("## "):
            return re.sub(r"^##\s*(General\s*-\s*)?", "", line).strip()
    return os.path.basename(path)


def site_pages() -> list[dict]:
    files = sorted(glob.glob(os.path.join(DOCS, "protocols", "**", "*.md"), recursive=True))
    out = []
    for f in files:
        rel = os.path.relpath(f, DOCS).replace(os.sep, "/")
        if rel in NOT_A_PROTOCOL_PAGE:      # generated digest, not a protocol page
            continue
        pg = P.read_page(f)
        if pg.get("has_table"):
            pg["format"] = "matrix"
            out.append(pg)
            continue
        rows = _site_rows_collapsed(f)
        if rows is None:
            continue
        out.append({"file": f, "rel": rel, "has_table": True, "title": _site_title(f),
                    "hdr": None, "rows": rows, "lines": pg.get("lines") or [], "ncols": 3,
                    "format": "collapsed"})
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
    if pg.get("format") == "collapsed":
        # The published table carries ONE chip per row, and that is what
        # `filled_level_cells` must mean — otherwise `POLICY`/`PENDING`, which
        # map to five blank legacy cells, make a grid-carrying page report
        # "0 filled level cells against 40 blank ones, so the grid is not merely
        # decorative", and a level chip's cumulative 5-cell spread inflates the
        # count on level-gated pages (Chest Pain 37 -> 51 for the same 14 rows).
        # One chip = one filled level cell; the four remaining legacy matrix
        # columns stay blank. `cells` itself is untouched: `levels()` and
        # text-binding depend on its cumulative spread.
        filled_cells = sum(1 for r in data_rows if (r.get("chip") or "").strip())
        blank_cells = 5 * len(data_rows) - filled_cells
    else:
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
    rec = {k: r.get(k) for k in ("page", "section_heading", "ordinal", "section_ordinal",
                                 "verbatim_text", "x", "y", "badge_tokens", "columns", "side",
                                 "row_split")}
    if rec.get("row_split") is None:
        rec.pop("row_split")
    if r.get("section_continued"):
        # the heading printed above this row is on an earlier page: the section
        # resumes here without reprinting it (see _merge_page_break_sections)
        rec["section_continued"] = True
    return rec


def rows_cache_records(docs: list[dict]) -> list[dict]:
    """Every document's rows, flattened, for the sibling pipeline stages."""
    return [{"doc": d["title"], **_row_record(r)} for d in docs for r in d["rows"]]


def write_rows_cache(docs: list[dict]) -> list[dict]:
    """Write `audit/level-scan/.cache/pems_rows.jsonl` and return its records."""
    os.makedirs(CACHE, exist_ok=True)
    recs = rows_cache_records(docs)
    with open(ROWS_CACHE, "w", encoding="utf-8") as fh:
        for rec in recs:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return recs


def build_rows_cache() -> list[dict]:
    """Derive the row cache from the PDF and write nothing else.

    The cache is git-ignored, so a clean clone never has one; a gate that only
    checks the path is red on every fresh checkout. This is the side-effect-free
    build the verifier calls: stage 1's parse and row splits, then the cache —
    no `pems_table.json`, `alignment.json` or `missing-rows.md` is touched, so a
    gate run can never rewrite the artifacts it is judging.
    """
    pages = parse_pdf()
    docs = build_docs(pages)
    splits, _ = _load_row_splits()
    if splits:
        _apply_row_splits(docs, splits)
    return write_rows_cache(docs)


def stage1(verbose: bool = False) -> dict:
    os.makedirs(CACHE, exist_ok=True)
    pages = parse_pdf()
    docs = build_docs(pages)
    splits, _ = _load_row_splits()
    if splits:
        applied = _apply_row_splits(docs, splits)
        if verbose:
            print(f"  row splits: {len(applied)} fused row(s) split")
    os.makedirs(OUTDIR, exist_ok=True)
    write_rows_cache(docs)
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


def _load_badge_overrides() -> tuple[dict, list[str]]:
    """badge-overrides.yaml -> ({(page, ordinal): entry}, problems).

    A human resolution recorded only in an adjudication output is not durable:
    the next C1 regeneration reintroduces the PDF badge and the contradiction
    returns. This file is what the parser reads, so an override lives in the
    canonical table itself.

    Hard errors, same rule as exceptions.yaml: an override with no `reason` or
    no `evidence` is refused at parse time (not merely reported later), and so
    is a duplicate key or a resolved token that is not a level. A missing file
    is an empty override set, never a crash.
    """
    import yaml
    if not os.path.exists(OVERRIDES_YAML):
        return {}, []
    doc = yaml.safe_load(open(OVERRIDES_YAML, encoding="utf-8")) or {}
    raw = doc.get("overrides")
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        raise SystemExit("badge-overrides.yaml: `overrides` must be a list")
    out: dict[tuple[int, int], dict] = {}
    problems: list[str] = []
    for i, ent in enumerate(raw):
        if not isinstance(ent, dict):
            problems.append(f"override #{i}: not a mapping")
            continue
        try:
            key = (int(ent["page"]), int(ent["ordinal"]))
        except (KeyError, TypeError, ValueError):
            problems.append(f"override #{i}: page/ordinal missing or not integers")
            continue
        for fld in ("badge_token_from_pdf", "resolved", "resolved_by"):
            if not str(ent.get(fld) or "").strip():
                problems.append(f"override p.{key[0]} #{key[1]}: `{fld}` is empty")
        for fld in ("reason", "evidence"):
            if not str(ent.get(fld) or "").strip():
                problems.append(f"override p.{key[0]} #{key[1]}: `{fld}` is mandatory")
        resolved = str(ent.get("resolved") or "").strip().strip("[]").upper()
        if resolved and resolved not in list(LEVELS) + ["MC"]:
            problems.append(f"override p.{key[0]} #{key[1]}: resolved {resolved!r} "
                            "is neither a level nor MC")
        if key in out:
            problems.append(f"override p.{key[0]} #{key[1]}: duplicate entry")
        ent = dict(ent)
        ent["resolved"] = resolved
        out[key] = ent
    if problems:
        raise SystemExit("badge-overrides.yaml is invalid:\n  " + "\n  ".join(problems))
    return out, []


def _apply_overrides(rows: list[dict], overrides: dict,
                     applied: list[dict], remaining: set | None = None) -> list[dict]:
    """Apply the human-resolved badge to row records, keeping the PDF token.

    `remaining` is the set of override keys not yet matched; the caller checks it
    is empty once every document has been walked (validating it per document
    would reject an override for a row that lives in the next document).
    """
    if not overrides:
        return rows
    out = []
    unknown = remaining if remaining is not None else set(overrides)
    for rec in rows:
        key = (rec["page"], rec["ordinal"])
        ov = overrides.get(key)
        if not ov:
            out.append(rec)
            continue
        unknown.discard(key)
        rec = dict(rec)
        pdf_token = list(rec.get("badge_tokens") or [])
        rec["badge_token_from_pdf"] = pdf_token
        rec["badge_tokens"] = [ov["resolved"]]
        rec["badge_override_applied"] = True
        rec["badge_override"] = {k: ov.get(k) for k in
                                 ("resolved", "resolved_by", "evidence", "reason")}
        # the badge spread the override implies, for consumers that level rows
        # from the badge rather than from the printed columns
        rec["columns_from_badge"] = _columns([ov["resolved"]])
        applied.append({"page": key[0], "ordinal": key[1],
                        "badge_token_from_pdf": pdf_token,
                        "resolved": ov["resolved"],
                        "resolved_by": ov.get("resolved_by"),
                        "evidence": ov.get("evidence"),
                        "reason": ov.get("reason")})
        out.append(rec)
    return out


def _load_row_splits() -> tuple[dict, list[str]]:
    """row-splits.yaml -> ({(page, ordinal): entry}, problems).

    The parser segments a page's badge column by matching each badge's vertical
    centre to a block of text lines. When two printed cells are only a few points
    apart that partition can put a printed cell's last lines under the *next*
    badge: the extracted row then carries two printed rows and the badge of the
    second. The text is real, the badge is real; only the boundary is wrong, and
    no single badge can correct it.

    A split names such a row and the printed cells it fuses, in order, each with
    the badge PEMS prints on it. The parts must reproduce the extracted text
    exactly — a split may move a boundary the extractor misplaced, never invent or
    drop words. A part marked `merge: next` belongs to the row that follows
    (the printed cell continues there), so it is carried onto that row instead of
    becoming a row of its own.
    """
    import yaml
    if not os.path.exists(SPLITS_YAML):
        return {}, []
    doc = yaml.safe_load(open(SPLITS_YAML, encoding="utf-8")) or {}
    raw = doc.get("splits")
    if raw is None:
        return {}, []
    if not isinstance(raw, list):
        raise SystemExit("row-splits.yaml: `splits` must be a list")
    problems: list[str] = []
    out: dict = {}
    for e in raw:
        if not isinstance(e, dict):
            problems.append(f"entry is not a mapping: {e!r}")
            continue
        page, ordn = e.get("page"), e.get("ordinal")
        label = f"p.{page} #{ordn}"
        if not isinstance(page, int) or not isinstance(ordn, int):
            problems.append(f"entry without an integer page/ordinal: {e!r}")
            continue
        for fld in ("reason", "evidence"):
            if not str(e.get(fld) or "").strip():
                problems.append(f"{label}: `{fld}` is mandatory")
        parts = e.get("parts")
        if not isinstance(parts, list) or len(parts) < 2:
            problems.append(f"{label}: `parts` must list at least two printed cells")
            parts = []
        for i, p in enumerate(parts):
            if not isinstance(p, dict):
                problems.append(f"{label} part {i}: not a mapping")
                continue
            if str(p.get("badge") or "") not in LEVELS:
                problems.append(f"{label} part {i}: badge {p.get('badge')!r} is not one of "
                                + "/".join(LEVELS))
            if not str(p.get("text") or "").strip():
                problems.append(f"{label} part {i}: `text` is mandatory")
            if p.get("merge") not in (None, "next"):
                problems.append(f"{label} part {i}: `merge` may only be \"next\"")
            if p.get("merge") and i != len(parts) - 1:
                problems.append(f"{label} part {i}: only the last part may merge into the "
                                f"next row")
        key = (page, ordn)
        if key in out:
            problems.append(f"{label}: listed twice")
        out[key] = e
    if problems:
        raise SystemExit("row-splits.yaml is invalid:\n  " + "\n  ".join(problems))
    return out, []


def _apply_row_splits(docs: list[dict], splits: dict) -> list[dict]:
    """Split the declared fused rows, then renumber the document's rows.

    `ordinal` is the document-wide index and `section_ordinal` the index within
    the section run; both are recomputed exactly as `build_docs` assigns them, so
    the table keeps the shape every consumer already expects.
    """
    if not splits:
        return []
    applied: list[dict] = []
    remaining = set(splits)
    for d in docs:
        rows = d["rows"]
        if not any((r["page"], r["ordinal"]) in splits for r in rows):
            continue
        out: list[dict] = []
        prepend = ""
        touched = False
        for r in rows:
            if prepend:
                r = dict(r)
                r["verbatim_text"] = re.sub(r"\s+", " ", prepend + " " + r["verbatim_text"]).strip()
                prepend = ""
            sp = splits.get((r["page"], r["ordinal"]))
            if sp is None:
                out.append(r)
                continue
            touched = True
            remaining.discard((r["page"], r["ordinal"]))
            parts = sp["parts"]
            joined = re.sub(r"\s+", " ", " ".join(p["text"] for p in parts)).strip()
            stored = re.sub(r"\s+", " ", r["verbatim_text"]).strip()
            if joined != stored:
                raise SystemExit(
                    f"row-splits.yaml: p.{r['page']} #{r['ordinal']} — the declared parts do "
                    f"not reproduce the extracted row text.\n    declared: {joined}\n    "
                    f"extracted: {stored}")
            emitted = []
            for i, p in enumerate(parts):
                if p.get("merge") == "next":
                    prepend = p["text"]
                    continue
                nr = dict(r)
                nr["verbatim_text"] = p["text"]
                nr["badge_tokens"] = [p["badge"]]
                nr["columns"] = _columns([p["badge"]])
                nr["row_split"] = {"page": r["page"], "ordinal": r["ordinal"],
                                   "part": i, "of": len(parts),
                                   "evidence": sp.get("evidence")}
                emitted.append(nr)
            out.extend(emitted)
            applied.append({"page": r["page"], "ordinal": r["ordinal"],
                            "badges": [p["badge"] for p in parts],
                            "evidence": sp.get("evidence"), "reason": sp.get("reason")})
        if prepend:
            raise SystemExit(f"row-splits.yaml: p.{out[-1]['page']} — a `merge: next` part "
                            f"has no following row to merge into")
        if touched:
            d["rows"] = out
            sec, cnt = None, 0
            for i, r in enumerate(d["rows"]):
                r["ordinal"] = i
                if r["section_heading"] != sec:
                    sec, cnt = r["section_heading"], 0
                r["section_ordinal"] = cnt
                cnt += 1
    if remaining:
        raise SystemExit("row-splits.yaml names PEMS rows the parser did not produce: "
                         f"{sorted(remaining)}")
    return applied


def _write_table(decisions: list[dict], docs: list[dict], pages: dict[int, dict],
                 exc: dict, repairs: dict) -> dict:
    counts: dict[str, int] = {}
    for d in decisions:
        counts[d["decision"]] = counts.get(d["decision"], 0) + 1
    overrides, _ = _load_badge_overrides()
    applied: list[dict] = []
    remaining = set(overrides)
    doc_records = []
    for d in docs:
        recs = _apply_overrides([_row_record(r) for r in d["rows"]], overrides,
                                applied, remaining)
        doc_records.append({"title": d["title"], "pages": d["pages"],
                            "n_rows": len(d["rows"]),
                            "section_continuations": d.get("section_continuations") or [],
                            "rows": recs,
                            "orphans": d["orphans"]})
    if remaining:
        # an override naming a row the parser never produced is otherwise a
        # silent no-op, and the next reader believes the badge was corrected
        raise SystemExit("badge-overrides.yaml names PEMS rows the parser did not "
                         f"produce: {sorted(remaining)}")
    splits, _ = _load_row_splits()
    split_rows = [{"page": r["row_split"]["page"], "ordinal": r["row_split"]["ordinal"],
                   "part": r["row_split"]["part"], "of": r["row_split"]["of"],
                   "badge": (r["badge_tokens"] or [None])[0],
                   "verbatim_text": r["verbatim_text"]}
                  for d in doc_records for r in d["rows"] if r.get("row_split")]
    out = {
        "generated": _dt.datetime.now().isoformat(timespec="seconds"),
        "sources": {"bbox_xml": os.path.relpath(P.CACHE, REPO),
                    "text_layer": "pems_chunks/PEMS2024_full.txt",
                    "pdf_pages_scanned": 280, "pems_pages_with_rows": len(pages)},
        "row_schema": ["page", "section_heading", "ordinal", "section_ordinal",
                       "verbatim_text", "x", "y", "badge_tokens", "columns"],
        "counts": {"site_pages_with_level_table": len(decisions), **counts},
        "page_decisions": decisions,
        "badge_overrides": {"file": os.path.relpath(OVERRIDES_YAML, REPO),
                            "count": len(overrides),
                            "applied": applied},
        "row_splits": {"file": os.path.relpath(SPLITS_YAML, REPO),
                       "count": len(splits),
                       "rows": split_rows},
        "pems_docs": doc_records,
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
    # A section with no single PEMS counterpart is NOT a dead end. Its rows are
    # scored against the whole page, exactly as a divider-less page's rows are:
    # "A: Obtain IV access" is an ordinary intervention with an ordinary PEMS
    # counterpart, and dumping it unexamined is how real gaps get lost. The
    # missing section map is recorded as an ANNOTATION on the row; the row's
    # disposition is still decided on its own evidence below.
    section_fallback: dict[int, str] = {}      # id(site row) -> why the map is absent

    # ---- per site row: every PEMS row in scope, scored
    site_index: list[tuple[str, dict, int, list[int]]] = []   # (section, row, k, scope)
    for si, (sname, srows) in enumerate(s_secs):
        if flat:
            scope = list(range(len(prow)))
        else:
            pi = mapped.get(si)
            if pi is None:
                # page-flat fallback: same scope, same sim(), same ordinal bonus,
                # same floor as the `flat` branch above.
                scope = list(range(len(prow)))
                note = (f"site section '{sname}' has no single PEMS counterpart "
                        f"(PEMS sections: {res['pems_sections']}); rows scored "
                        f"against page-flat scope")
                for r in srows:
                    section_fallback[id(r)] = note
            else:
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
    label_key_map: dict[int, list[str]] = {}
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
        label_key_map[i] = sorted(distinctive(label_keys(site_index[i][1]["action"])))

    # ---- split repair: the site row that OPENS an intervention owns it.
    # A site that splits one PEMS row into consecutive rows can lose that row to
    # its own continuation, because sim() divides the overlap by the SHORTER side
    # and every word of a continuation is inside the PEMS row: "If unsuccessful,
    # check pad placement and repeat at 200 joules" scores 0.841 against p.136 row
    # 6 while "Perform SYNCHRONIZED cardioversion 100 joules initial dose" scores
    # 0.832. Within SPLIT_EPS the two are the same reading of the row, and the
    # site's own order is the evidence that separates them: the earlier row of the
    # same section owns the PEMS row, the later one is the split it is, reported
    # as `shared_pems_row` rather than silently taking the match.
    SPLIT_EPS = 0.02
    owners = [(gi, i, s) for i, (gi, s, _e) in picked.items() if i not in label_fixed]
    for gi, owner, owner_s in owners:
        earlier = []
        for i in range(len(site_index)):
            if i == owner or i in picked or i in ambiguous or i in label_fixed:
                continue
            if site_index[i][0] != site_index[owner][0] or i > owner:
                continue
            for sc, g, e in cands[i]:
                base = sc - (0.04 if e else 0.0)
                if g == gi and base >= 0.40 and abs(base - owner_s) <= SPLIT_EPS:
                    earlier.append((i, base))
                    break
        if not earlier:
            continue
        i, sc = min(earlier)
        picked[i] = (gi, sc, False)
        del picked[owner]
        collided[owner] = gi

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

    # which site row holds each taken PEMS row (for the containment evidence)
    matched_by_gi = {gi: site_index[i][1]["num"] for i, (gi, _s, _e) in picked.items()}

    out_rows = []
    for i, (sname, r, k, scope) in enumerate(site_index):
        base = {"site_row": r["num"], "section": sname,
                "action": P.clean(r["action"])[:200], "cells": [c.strip() for c in r["cells"]]}
        # annotation, not disposition: the row's status is decided below on its own
        # evidence whether or not its section heading could be mapped.
        fallback_note = section_fallback.get(id(r))
        if fallback_note:
            base["section_fallback"] = True
            base["section_note"] = fallback_note
        flat_scope = flat or bool(fallback_note)
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
            # A row with no distinctive label word can still be the other half of
            # a PEMS row the site splits: "A: Obtain IV access" is the head of
            # p.135 row 2, whose fluid-bolus tail the next site row matched.
            contained = None if keys else _contained_in_taken(r["action"], prow, taken)
            if contained:
                ev = {k: v for k, v in contained.items() if k != "pems_gi"}
                base.update(status="ambiguous", reason_kind="shared_pems_row",
                            contained_in_pems=ev,
                            reason=(f"every word of this row "
                                    f"({', '.join(contained['overlap_tokens'])}) occurs in "
                                    f"p.{contained['pems_page']} row {contained['pems_ordinal']} — "
                                    f"{contained['tokens_in_site_row']} of that row's "
                                    f"{contained['tokens_in_pems_row']} significant words — which "
                                    f"site row {matched_by_gi.get(contained['pems_gi'])} already "
                                    f"holds; the site splits one PEMS row into two"))
                out_rows.append(base)
                continue
            base.update(status="ambiguous", reason_kind="no_counterpart",
                        reason=(f"no PEMS row in {'the page grid' if flat_scope else repr(sname)} "
                                f"reaches the text floor and no label word binds it; the site "
                                f"row has no PEMS counterpart (local addition, or a PEMS row "
                                f"worded beyond recognition)"))
            out_rows.append(base)
            continue
        gi, s, exact = picked[i]
        p = prow[gi]
        if i in label_fixed:
            base["label_keys"] = label_key_map.get(i, [])
        base.update(status="matched", pems_section_ordinal=p["section_ordinal"],
                    pems_page=p["page"], pems_ordinal=p["ordinal"],
                    pems_section=p["section_heading"],
                    pems_text=p["verbatim_text"][:240],
                    badges=p["badge_tokens"], similarity=round(s, 3),
                    match_basis=("label+keyword" if i in label_fixed else
                                 ("page-flat+ordinal" if flat_scope and exact else
                                  "section+ordinal" if exact else
                                  "page-flat+text" if flat_scope else "section+text")
                                 + (" +order (near-duplicate rows)" if i in fixed_ids else "")))
        out_rows.append(base)
    res["rows"] = out_rows

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

    # ---- ledger: one entry per PEMS row in scope, with its disposition.
    # Without this, a PEMS row that an ambiguous site row was explaining vanishes
    # from every list (it is neither matched nor absent nor duplicate), and a
    # missing row is exactly what a human can never spot by reading the site.
    amb_claim: dict[int, list] = {}
    for i, gis in claimed_by_ambiguous.items():
        for gi in gis:
            amb_claim.setdefault(gi, []).append(site_index[i][1]["num"])
    disp: dict[tuple[int, int], tuple[str, object]] = {}
    for a in res["absent"]:
        disp[(a["pems_page"], a["ordinal"])] = ("absent", None)
    for d in res.get("duplicates") or []:
        disp[(d["pems_page"], d["ordinal"])] = ("duplicate_in_source",
                                                d.get("duplicate_of_matched_row"))
    for m in res.get("merged_into_site_row") or []:
        disp[(m["pems_page"], m["ordinal"])] = ("merged_into_site_row",
                                                m.get("best_similarity_to_a_site_row"))
    ledger, page_pos = [], {}
    for gi, p in enumerate(prow):
        pos = page_pos.get(p["page"], 0)
        page_pos[p["page"]] = pos + 1
        if gi in matched_by_gi:
            kind, note = "matched", None
        elif gi in amb_claim:
            kind, note = "claimed_by_ambiguous_site_row", None
        else:
            kind, note = disp.get((p["page"], p["ordinal"]), ("unaccounted", None))
        ledger.append({"pems_page": p["page"], "page_ordinal": pos,
                       "ordinal": p["ordinal"], "section": p["section_heading"],
                       "verbatim_text": p["verbatim_text"], "badges": p["badge_tokens"],
                       "disposition": kind, "site_row": matched_by_gi.get(gi),
                       "claimed_by_site_rows": amb_claim.get(gi, []), "note": note})
    res["pems_row_ledger"] = ledger
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
    head = re.sub(r"[*_#]", " ", head)
    # A row can open with the level it applies from ("A: Obtain IV access",
    # "P: Perform SYNCHRONIZED cardioversion"). That prefix is a badge, not the
    # head noun; left in place, the head-noun split below stopped at its colon and
    # the row lost its label key entirely.
    head = re.sub(r"^\s*(?:EMR|EMT|MC|A|I|P)\s*:\s*", "", head)
    head = re.split(r"[:(/]| - ", head, maxsplit=1)[0]       # head noun phrase only
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


def _contained_in_taken(action: str, prow: list[dict], taken: set[int]) -> dict | None:
    """Is this site row one half of a PEMS row another site row already took?

    The site splits a PEMS row it governs into two of its own: "Obtain IV access.
    Consider: ADULT: 0.9% Sodium Chloride up to 1 L IV/IO ..." becomes "A: Obtain
    IV access" and the fluid-bolus row. The first half carries no distinctive
    label word ("access" appears in more than _DISTINCT_MAX PEMS rows), so the
    label binding cannot see it and it reads as "no counterpart" while its other
    half holds the PEMS row.

    The test is CONTAINMENT, not overlap: every significant word of the site row
    must occur in the taken PEMS row, and the PEMS row must say more (proper
    subset), so a row that merely shares a generic word with a taken row cannot
    fire. When more than one taken PEMS row contains it the evidence does not
    name a single source, and nothing is claimed.
    """
    A = _sig(P.clean(action))
    if not A:
        return None
    hits: list[tuple[float, int]] = []
    for gi in sorted(taken):
        B = _sig(P.clean(prow[gi]["verbatim_text"]))
        if A < B:
            hits.append((len(A) / len(B), gi))
    if len(hits) != 1:
        return None
    ratio, gi = hits[0]
    p = prow[gi]
    return {"pems_page": p["page"], "pems_ordinal": p["ordinal"], "pems_gi": gi,
            "pems_text": p["verbatim_text"][:240], "overlap_tokens": sorted(A),
            "tokens_in_site_row": len(A),
            "tokens_in_pems_row": len(_sig(P.clean(p["verbatim_text"]))),
            "containment": round(ratio, 3)}


def stage2(seed: dict) -> dict:
    docs = seed["docs"]
    table = seed["table"]
    _build_df(docs)
    import pems_text_binding as TB      # deferred: it imports this module
    # C1d text-binding pass: the level columns of every PEMS row, so the pass can
    # record what the row it cites actually prints in each provider column.
    cols = {(r["page"], r["ordinal"]): r["columns"]
            for d in docs for r in d["rows"]}
    dec = {d["site_page"]: d for d in table["page_decisions"]}
    results = []
    for pg in site_pages():
        d = dec.get(pg["rel"])
        if not d or d["decision"] != "level_gated":
            continue
        res = align_page(pg, docs, d.get("pems_pages") or [])
        # Structure has had its say; give the leftovers one text pass over the
        # same page scope before the row's disposition is final.
        TB.apply(res, {r["num"]: r["action"] for r in pg["rows"] if not r["divider"]},
                 cols)
        results.append(res)

    tot: dict = {"site_rows": 0, "matched": 0, "ambiguous": 0, "absent_from_site": 0}
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
    # Every PEMS row in scope carries exactly one disposition in the per-page
    # ledger; the census is read from the ledger, never inferred by addition.
    led: collections.Counter = collections.Counter()
    for r in results:
        for e in r.get("pems_row_ledger") or []:
            led[e["disposition"]] += 1
    tot["pems_rows_by_disposition"] = dict(sorted(led.items()))
    tot["pems_rows_in_scope"] = sum(led.values())

    totals = dict(tot)
    totals["ambiguous_by_kind"] = kinds
    totals["text_binding"] = TB.counts(results)
    out = {"generated": _dt.datetime.now().isoformat(timespec="seconds"),
           "method": ("primary key = section heading + ordinal within section, then the "
                      "site row's own intervention label (bold head noun); text similarity "
                      "only breaks ties and never creates a pair on its own"),
           "totals": totals, "pages": results}
    tot = totals
    with open(ALIGN_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    delta = delta_buckets(results, tot, seed["docs"])
    write_missing(results, tot, table, delta)
    write_reconciliation(results, tot, delta)
    write_ambiguous(results, tot)
    TB.write_md(results, os.path.join(OUTDIR, "text-binding.md"))
    return out


PRIOR_ABSENT = 152   # audit/level-scan/2026-11-14-report.md, "PEMS rows with no site counterpart"

UNPAIRED = ("absent", "duplicate_in_source", "merged_into_site_row")

# Human review of every pairing the mechanical screen flags, recorded separately
# from the classification: a verdict here never changes a row's status, it only
# stops a weak pairing from being reported as a quiet win. Each entry was read
# against both texts. `suspect` means the two rows are about DIFFERENT
# interventions and the binding rests on a shared word.
REVIEW_VERDICTS: dict[tuple[str, int, int], tuple[str, str]] = {
    ("protocols/cardiac/04_Chest_Pain_ACS_PROC.md", 107, 5): (
        "correct", "same intervention: site row is Aspirin Administration, PEMS row gives the 324 mg PO dose"),
    ("protocols/cardiac/04_Chest_Pain_ACS_PROC.md", 107, 6): (
        "correct", "same intervention: Nitroglycerin vs Nitroglycerine 0.4 mg SL (dose/spelling only)"),
    ("protocols/medical/07_OB_Emergencies_PROC.md", 141, 3): (
        "suspect", "site row details breech DELIVERY technique; PEMS row only says 'refer to guidance below' — shared word 'breech', different content"),
    ("protocols/neurologic/05_Seizure_PROC.md", 127, 3): (
        "correct", "both are the referral-to-Overdose/Poisoning instruction; wording differs only"),
    ("protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md", 239, 10): (
        "suspect", "site row is BVM ventilation for an apneic patient; PEMS row is paediatric endotracheal intubation — bound on 'apneic' alone"),
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 57, 3): (
        "correct", "both are 'identify and treat potentially reversible causes'"),
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 57, 8): (
        "correct", "PEMS row is explicitly 'regarding Termination of Resuscitation'"),
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 63, 7): (
        "correct", "both are the defibrillation row, same joules and dose split"),
    ("protocols/general/02_Behavioral_Patient_Restraint_PROC.md", 71, 3): (
        "correct", "both assess capacity and treat causes of agitation/altered mental status"),
    ("protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md", 93, 6): (
        "correct", "both are contact medical control for hyperbaric transport destination"),
    ("protocols/medical/07_OB_Emergencies_PROC.md", 147, 4): (
        "correct_partial", "both are medical-control contact in eclampsia; the PEMS row scopes it to continued seizures"),
    ("protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md", 123, 2): (
        "correct", "both are supplemental oxygen to a SpO2 target"),
    ("protocols/respiratory/03_Pediatric_Stridor_PROC.md", 123, 3): (
        "correct", "both are non-invasive (CPAP) ventilatory support"),
    ("protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md", 123, 3): (
        "correct", "both are CPAP for severe respiratory distress"),
    ("protocols/respiratory/03_Respiratory_Arrest_PROC.md", 239, 6): (
        "correct", "PEMS row names 'BLS airway adjuncts (OPA/NPA/SGA)' explicitly"),
    ("protocols/toxicology/06_Overdose_Poisoning_PROC.md", 119, 5): (
        "correct_partial", "site row merges glucose + 12-lead ECG; the PEMS row covers the ECG half"),
    ("protocols/toxicology/06_Overdose_Poisoning_PROC.md", 119, 7): (
        "correct", "both are the naloxone administration row with the same dose ranges"),
    ("protocols/trauma/09_Electrical_Injuries_PROC.md", 96, 11): (
        "correct_partial", "site row merges 12-lead + rhythm monitoring; the PEMS row covers the monitoring half"),
    ("protocols/trauma/09_Trauma_PROC.md", 83, 3): (
        "suspect", "site row is 'assess for shock, refer to Shock protocol'; PEMS row is 'keep the patient warm' — bound on the word 'shock'"),
}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip().lower()


def _prior_absent() -> list[dict]:
    """Parse the 2026-11-14 report's missing list, keeping each row's TEXT.

    The prior scan numbered rows per PAGE; this run numbers them per DOCUMENT and
    splits merged pages differently, so a row number is not an identity. The
    verbatim text is: every prior claim is re-identified by text inside that
    page's own in-scope PEMS rows, never by row number.
    """
    prior = os.path.join(OUTDIR, "2026-11-14-report.md")
    out: list[dict] = []
    if not os.path.exists(prior):
        return out
    md = open(prior, encoding="utf-8").read()
    marker = "## PEMS rows with no site counterpart"
    if marker not in md:
        return out
    for line in md.split(marker, 1)[1].splitlines():
        m = re.match(r"- `([^`]+)` ← p\.(\d+) row (\d+) badge `([^`]*)`: (.*)$", line.strip())
        if m:
            out.append({"site_page": m.group(1), "pems_page": int(m.group(2)),
                        "prior_row": int(m.group(3)), "prior_badges": m.group(4),
                        "prior_text": m.group(5).strip()})
    return out


def _row_overlap(prior_text: str, row_text: str) -> int:
    """Characters of agreement at the START of a PEMS row.

    The old scan emitted a 140-character window per row and cut its rows at
    different boundaries: the window usually opens with the tail of the previous
    row and stops mid-row. So the identifying evidence is "a suffix of the window
    is a prefix of this row". Returns the longest such agreement.
    """
    key, t = _norm(prior_text), _norm(row_text)
    best = 0
    for cut in range(0, min(len(key), 120)):
        k = key[cut:]
        l = 0
        while l < len(k) and l < len(t) and k[l] == t[l]:
            l += 1
        if l > best:
            best = l
    return best


def _find_ledger_row(prior: dict, ledger_by_page: dict[str, list[dict]]) -> dict | None:
    """Locate a prior claim in this run's ledger by page + verbatim text."""
    cands = [e for e in ledger_by_page.get(prior["site_page"], [])
             if e["pems_page"] == prior["pems_page"]]
    key = _norm(prior["prior_text"])
    for e in cands:
        if _norm(e["verbatim_text"]) == key:
            return e
    if len(key) >= 40:
        inside = [e for e in cands
                  if _norm(e["verbatim_text"]) in key or key in _norm(e["verbatim_text"])]
        if len(inside) == 1:
            return inside[0]
    scored = sorted(((_row_overlap(key, e["verbatim_text"]), e) for e in cands),
                    key=lambda x: -x[0])
    if scored and scored[0][0] >= 40:
        if len(scored) == 1 or scored[0][0] - scored[1][0] >= 10:
            return scored[0][1]
    return None


def _site_row_for(results: list[dict], page: str, row_num) -> dict:
    for r in results:
        if r["site_page"] != page:
            continue
        for row in r["rows"]:
            if row["site_row"] == row_num:
                return row
    return {}


def _trust(row: dict) -> str:
    """Did the pairing this run makes hold up on its own evidence?

    A structural basis (section + ordinal) or a label binding on a distinctive
    head noun is evidence in itself. A pure text pairing is only trusted when the
    symmetric score is high; the rest are flagged for a human, never counted as
    a silent win.
    """
    basis = (row.get("match_basis") or "").split(" +order")[0]
    sim = row.get("similarity") or 0.0
    if basis == "section+ordinal":
        return "correct_structural"
    if basis.startswith("text-binding"):
        # The C1d pass never binds on similarity: it binds on a phrase that
        # occurs upstream, or on a cleared coverage floor plus a drug/dose/label
        # anchor. The evidence, not a score, is what makes it trustworthy.
        return "correct_text_binding"
    if basis == "label+keyword":
        # A label binding already required EVERY distinctive label word to appear
        # in the PEMS row. A multi-word key is therefore evidence on its own; a
        # single-word key with a low symmetric score is the weak case that a human
        # should confirm.
        n = len(row.get("label_keys") or [])
        return "correct_label" if (n >= 2 or sim >= 0.30) else "needs_a_human_eye"
    return "correct_text" if sim >= 0.75 else "needs_a_human_eye"


def _where_else(prior: dict, docs: list[dict]) -> dict | None:
    """Where does this PEMS row live, if not in this page's scope?

    A prior claim can name a PEMS row this site page no longer governs (the scope
    comes from exceptions.yaml / title match). Naming the document and page it does
    live on turns "not found" into a checkable statement.
    """
    key = _norm(prior["prior_text"])
    best, best_score = None, 0
    for d in docs:
        for r in d["rows"]:
            score = (40 if _norm(r["verbatim_text"]) == key
                     else _row_overlap(key, r["verbatim_text"]))
            if score > best_score:
                best, best_score = (d, r), score
    if best and best_score >= 40:
        d, r = best
        return {"pems_doc": d["title"], "pems_pages": d["pages"],
                "pems_page": r["page"], "pems_text": r["verbatim_text"][:200]}
    return None


def delta_buckets(results: list[dict], tot: dict, docs: list[dict] | None = None) -> dict:
    """Account for the 152 -> N absent delta BY CAUSE, naming every row.

    Three lists, all derived from this run's per-page PEMS ledger:
      * prior_to_now   — what happened to each of the 152 rows the old scan
                         called gaps (still absent, paired, covered, gone);
      * new_unpaired   — rows this run leaves unpaired that were not on the old
                         list, i.e. the part of the delta that went the other way;
      * absent_arithmetic — the identity that must close.
    """
    prior = _prior_absent()
    ledger_by_page = {r["site_page"]: r.get("pems_row_ledger") or [] for r in results}
    aligned = {r["site_page"] for r in results}
    buckets: dict[str, list[dict]] = collections.defaultdict(list)
    identified_by: dict[tuple[str, int, int], dict] = {}
    for pr in prior:
        if pr["site_page"] not in aligned:
            buckets["page_not_aligned_this_run"].append(pr)
            continue
        e = _find_ledger_row(pr, ledger_by_page)
        if e is None:
            rec = dict(pr)
            rec["elsewhere"] = _where_else(pr, docs or [])
            rec["pems_page_has_rows_now"] = any(
                r["page"] == pr["pems_page"] for d in (docs or []) for r in d["rows"])
            buckets["prior_row_not_in_current_scope"].append(rec)
            continue
        key = (pr["site_page"], e["pems_page"], e["ordinal"])
        if key in identified_by:
            earlier = identified_by[key]
            buckets["prior_claims_collapsed_into_one_current_row"].append(
                {**pr, "pems_page_now": e["pems_page"], "pems_ordinal_now": e["ordinal"],
                 "pems_text_now": e["verbatim_text"],
                 "earlier_claim_text": earlier["prior_text"]})
            continue
        identified_by[key] = pr
        disp = e["disposition"]
        rec = {**pr, "current_disposition": disp,
               "pems_page_now": e["pems_page"], "pems_ordinal_now": e["ordinal"],
               "pems_text_now": e["verbatim_text"]}
        if disp == "matched":
            row = _site_row_for(results, pr["site_page"], e["site_row"])
            rec.update(site_row_now=e["site_row"], site_action=row.get("action"),
                       similarity=row.get("similarity"),
                       match_basis=row.get("match_basis"),
                       label_keys=row.get("label_keys"),
                       section_fallback=bool(row.get("section_fallback")))
            if row.get("section_fallback"):
                buckets["resolved_by_section_fallback"].append(rec)
            elif row.get("match_basis", "").startswith("label+keyword"):
                buckets["paired_to_site_row_label"].append(rec)
            elif row.get("match_basis", "").startswith("text-binding"):
                # C1d: a row the structural pass left in the ambiguous pile and
                # the text pass bound afterwards. Kept in its own bucket so the
                # window of ambiguity this card closed is visible by name.
                buckets["paired_to_site_row_text_binding"].append(rec)
            elif row.get("match_basis", "").startswith("section+ordinal"):
                buckets["paired_to_site_row_section_ordinal"].append(rec)
            else:
                buckets["paired_to_site_row_text"].append(rec)
            rec["verdict"] = _trust(row)
            hv = REVIEW_VERDICTS.get((pr["site_page"], e["pems_page"], e["ordinal"]))
            if hv:
                rec["human_verdict"], rec["human_note"] = hv
        elif disp == "claimed_by_ambiguous_site_row":
            rec["claimed_by_site_rows"] = e.get("claimed_by_site_rows") or []
            buckets["claimed_by_an_ambiguous_site_row"].append(rec)
        elif disp == "duplicate_in_source":
            buckets["duplicate_copy_in_merged_source"].append(rec)
        elif disp == "merged_into_site_row":
            rec["best_similarity_to_a_site_row"] = e.get("note")
            buckets["merged_into_a_site_row"].append(rec)
        else:
            buckets["still_absent"].append(rec)

    new_unpaired: list[dict] = []
    for r in results:
        for e in r.get("pems_row_ledger") or []:
            if e["disposition"] not in UNPAIRED:
                continue
            if (r["site_page"], e["pems_page"], e["ordinal"]) in identified_by:
                continue
            new_unpaired.append({"site_page": r["site_page"], "pems_page": e["pems_page"],
                                 "ordinal": e["ordinal"], "pems_text": e["verbatim_text"],
                                 "section": e["section"], "cause": e["disposition"],
                                 "note": e.get("note")})

    counts = {k: len(v) for k, v in sorted(buckets.items())}
    new_counts = dict(sorted(collections.Counter(x["cause"] for x in new_unpaired).items()))
    absent_after = counts.get("still_absent", 0) + new_counts.get("absent", 0)
    if absent_after != tot["absent_from_site"]:
        raise AssertionError(f"absent arithmetic does not close: {absent_after} != "
                             f"{tot['absent_from_site']}")
    if sum(counts.values()) != len(prior):
        raise AssertionError(f"prior rows not fully accounted: {sum(counts.values())} "
                             f"of {len(prior)}")
    paired_total = (counts.get("paired_to_site_row_section_ordinal", 0)
                    + counts.get("paired_to_site_row_label", 0)
                    + counts.get("paired_to_site_row_text", 0)
                    + counts.get("paired_to_site_row_text_binding", 0)
                    + counts.get("resolved_by_section_fallback", 0))
    left_gap = len(prior) - counts.get("still_absent", 0)
    return {
        "prior_reported": len(prior),
        "prior_pages": len({p["site_page"] for p in prior}),
        "pages_aligned_this_run": len(results),
        "prior_to_now": {"counts": counts, "rows": {k: v for k, v in buckets.items()}},
        "new_unpaired": {"count": len(new_unpaired), "counts": new_counts,
                         "rows": new_unpaired},
        "absent_arithmetic": {
            "prior_absent": len(prior),
            "still_absent_from_prior": counts.get("still_absent", 0),
            "newly_absent_not_on_prior_list": new_counts.get("absent", 0),
            "now_absent": tot["absent_from_site"],
            "identity": (
                f"absent now {tot['absent_from_site']} = "
                f"{counts.get('still_absent', 0)} prior rows still absent + "
                f"{new_counts.get('absent', 0)} newly absent. "
                f"Of the {len(prior)} prior rows, the {left_gap} that left the gap list are: "
                f"{paired_total} paired to a site row "
                f"({counts.get('paired_to_site_row_section_ordinal', 0)} section+ordinal, "
                f"{counts.get('paired_to_site_row_label', 0)} label, "
                f"{counts.get('paired_to_site_row_text', 0)} text, "
                f"{counts.get('paired_to_site_row_text_binding', 0)} text-binding pass, "
                f"{counts.get('resolved_by_section_fallback', 0)} section-fallback), "
                f"{counts.get('claimed_by_an_ambiguous_site_row', 0)} explained by an ambiguous "
                f"site row, {counts.get('merged_into_a_site_row', 0)} merged inside a wider site "
                f"row, {counts.get('duplicate_copy_in_merged_source', 0)} duplicate copies, "
                f"{counts.get('prior_row_not_in_current_scope', 0)} not in this run's scope and "
                f"{counts.get('prior_claims_collapsed_into_one_current_row', 0)} collapsed into a "
                f"single parse row"),
        },
    }


def write_reconciliation(results: list[dict], tot: dict, delta: dict) -> None:
    """Write `reconciliation.json` and the matching section of `missing-rows.md`."""
    counts = delta["prior_to_now"]["counts"]
    new_counts = delta["new_unpaired"]["counts"]
    ident = delta["absent_arithmetic"]["identity"]
    paired = (counts.get("paired_to_site_row_section_ordinal", 0)
              + counts.get("paired_to_site_row_label", 0)
              + counts.get("paired_to_site_row_text", 0)
              + counts.get("paired_to_site_row_text_binding", 0)
              + counts.get("resolved_by_section_fallback", 0))
    verdicts = collections.Counter(r["verdict"]
                                   for k in counts if k.startswith(("paired_to_site_row", "resolved_by"))
                                   for r in delta["prior_to_now"]["rows"][k])
    reviewed = collections.Counter(r["human_verdict"]
                                   for k in counts if k.startswith(("paired_to_site_row", "resolved_by"))
                                   for r in delta["prior_to_now"]["rows"][k] if r.get("human_verdict"))
    delta["prior_to_now"]["verdicts"] = dict(sorted(verdicts.items()))
    delta["prior_to_now"]["human_review"] = dict(sorted(reviewed.items()))
    delta["prior_to_now"]["paired_total"] = paired
    delta["identity"] = ident
    data = {"bridge": {
        "prior_reported": delta["prior_reported"],
        "now_absent": tot["absent_from_site"],
        "still_absent_from_prior": counts.get("still_absent", 0),
        "prior_missing_now_paired": paired,
        "prior_missing_now_paired_reviewed_correct": reviewed.get("correct", 0),
        "prior_missing_now_paired_reviewed_partial": reviewed.get("correct_partial", 0),
        "prior_missing_now_paired_reviewed_suspect": reviewed.get("suspect", 0),
        "prior_missing_now_paired_unreviewed": paired - sum(reviewed.values()),
        "prior_missing_now_duplicate_or_merged":
            counts.get("duplicate_copy_in_merged_source", 0)
            + counts.get("merged_into_a_site_row", 0),
        "prior_missing_now_claimed_by_ambiguous":
            counts.get("claimed_by_an_ambiguous_site_row", 0),
        "prior_rows_not_found_in_current_scope":
            counts.get("prior_row_not_in_current_scope", 0),
        "prior_claims_collapsed_into_one_current_row":
            counts.get("prior_claims_collapsed_into_one_current_row", 0),
        "newly_unpaired_not_in_prior_list": delta["new_unpaired"]["count"],
        "identity": ident,
    }, **delta}
    with open(os.path.join(OUTDIR, "reconciliation.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)

    weak = [r for k in counts if k.startswith(("paired_to_site_row", "resolved_by"))
            for r in delta["prior_to_now"]["rows"][k] if r.get("verdict") == "needs_a_human_eye"]
    section = [
        "## Reconciliation with the previous scan's 152, by cause\n\n",
        f"The 2026-11-14 scan reported **{delta['prior_reported']}** PEMS rows with no site "
        f"row. This run reports **{tot['absent_from_site']}**. The delta is accounted for "
        "below by cause, with every row named in `reconciliation.json` "
        "(`prior_to_now.rows`). Rows are matched by verbatim text, not row number: the two "
        "scans number rows differently.\n\n",
        "| what happened to the prior scan's 152 rows | rows |\n|---|---|\n",
        f"| still `absent_from_site` | {counts.get('still_absent', 0)} |\n",
        f"| paired to a site row on section + ordinal | "
        f"{counts.get('paired_to_site_row_section_ordinal', 0)} |\n",
        f"| paired to a site row on its label | {counts.get('paired_to_site_row_label', 0)} |\n",
        f"| paired to a site row on text evidence | {counts.get('paired_to_site_row_text', 0)} |\n",
        f"| paired to a site row by the C1d text-binding pass (this fix) | "
        f"{counts.get('paired_to_site_row_text_binding', 0)} |\n",
        f"| paired by the section-fallback scoring (this fix) | "
        f"{counts.get('resolved_by_section_fallback', 0)} |\n",
        f"| a duplicate copy inside the merged PEMS source | "
        f"{counts.get('duplicate_copy_in_merged_source', 0)} |\n",
        f"| the site does write it, inside a wider site row | "
        f"{counts.get('merged_into_a_site_row', 0)} |\n",
        f"| explained by an ambiguous site row (not a gap) | "
        f"{counts.get('claimed_by_an_ambiguous_site_row', 0)} |\n",
        f"| not found in this run's scope (needs a look) | "
        f"{counts.get('prior_row_not_in_current_scope', 0)} |\n",
        f"| two prior claims that this run's parse merges into one PEMS row | "
        f"{counts.get('prior_claims_collapsed_into_one_current_row', 0)} |\n",
        f"| page not aligned this run | {counts.get('page_not_aligned_this_run', 0)} |\n",
        f"\nOf the {paired} rows that now pair, the mechanical screen trusts "
        f"{verdicts.get('correct_label', 0) + verdicts.get('correct_text', 0) + verdicts.get('correct_structural', 0) + verdicts.get('correct_text_binding', 0)} "
        f"outright ({verdicts.get('correct_structural', 0)} section+ordinal, "
        f"{verdicts.get('correct_label', 0)} distinctive label, "
        f"{verdicts.get('correct_text', 0)} text evidence, "
        f"{verdicts.get('correct_text_binding', 0)} text-binding pass) and finds "
        f"**{len(weak)} too weak to accept without a human**. All {len(weak)} were read "
        "against both texts and are recorded in `reconciliation.json` under "
        "`prior_to_now.rows[*].human_verdict` / `human_note`:\n\n",
        f"- **{reviewed.get('correct', 0)} correct** — same intervention, wording or dose split "
        "differs.\n",
        f"- **{reviewed.get('correct_partial', 0)} correct but partial** — the site row merges "
        "this PEMS intervention with another, and the PEMS row covers part of it.\n",
        f"- **{reviewed.get('suspect', 0)} suspect** — the two rows are about different "
        "interventions and the binding rests on one shared word: "
        + "; ".join(f"{r['site_page'].split('/')[-1]} p.{r['pems_page_now']}"
                    f"#{r['pems_ordinal_now']}" for k in counts
                    if k.startswith(("paired_to_site_row", "resolved_by"))
                    for r in delta["prior_to_now"]["rows"][k]
                    if r.get("human_verdict") == "suspect")
        + ". These are counted as paired here only because that is what the aligner did; "
        "they are adjudication work for C2, not settled matches.\n\n",
        f"Going the other way, **{delta['new_unpaired']['count']} rows** this run leaves "
        f"unpaired were not on the old list "
        f"({new_counts.get('absent', 0)} absent, "
        f"{new_counts.get('duplicate_in_source', 0)} duplicate, "
        f"{new_counts.get('merged_into_site_row', 0)} merged): the old scan paired them on "
        "text similarity alone, and this one will not pair a row without structural "
        "evidence. They are the rows most worth a human glance and are named in "
        "`reconciliation.json` (`new_unpaired.rows`).\n\n",
        f"**Check:** {ident}.\n",
    ]
    md = open(MISSING_MD, encoding="utf-8").read()
    start = md.find("## Reconciliation with the previous scan's 152")
    end = md.find("\n## `", start)
    if start != -1 and end != -1:
        md = md[:start] + "".join(section) + md[end:]
        open(MISSING_MD, "w", encoding="utf-8").write(md)


def write_missing(results: list[dict], tot: dict, table: dict, delta: dict) -> None:
    n_pages = sum(1 for r in results if r["absent"])
    c = delta["prior_to_now"]["counts"]
    nc = delta["new_unpaired"]["counts"]
    L = ["# PEMS interventions with no site row (`absent_from_site`)\n\n",
         "Every PEMS 2024 intervention that has no counterpart on the Poquoson "
         "protocol page it belongs to. These are content gaps: the site documents "
         "the protocol but not this intervention, and nothing downstream will "
         "notice because the site row it should live on simply is not there.\n\n",
         f"**Total: {tot['absent_from_site']} rows across {n_pages} pages.** "
         f"(matched {tot['matched']}, ambiguous {tot['ambiguous']}, "
         f"site rows {tot['site_rows']})\n",
         "\n## Reconciliation with the previous scan's 152\n",
         f"The 2026-11-14 scan reported **{PRIOR_ABSENT}** PEMS rows with no site row. "
         f"This run reports **{tot['absent_from_site']}**. The difference is accounted for "
         "by cause, and every row in every bucket is named in `reconciliation.json` "
         "(`prior_to_now.rows`, `new_unpaired.rows`).\n",
         f"- **{c.get('still_absent', 0)} of the {PRIOR_ABSENT} are still absent** and are "
         "listed below.\n",
         f"- **{(c.get('paired_to_site_row_section_ordinal', 0) + c.get('paired_to_site_row_label', 0) + c.get('paired_to_site_row_text', 0) + c.get('paired_to_site_row_text_binding', 0) + c.get('resolved_by_section_fallback', 0))} of them now pair to a site row** "
        f"(section+ordinal {c.get('paired_to_site_row_section_ordinal', 0)}, label "
        f"{c.get('paired_to_site_row_label', 0)}, text {c.get('paired_to_site_row_text', 0)}, "
        f"text-binding pass {c.get('paired_to_site_row_text_binding', 0)}, "
        f"section-fallback {c.get('resolved_by_section_fallback', 0)}); each carries its "
        "similarity and basis in `reconciliation.json`, and any pairing below the trust "
        "threshold is flagged there for a human.\n",
        f"- **{c.get('duplicate_copy_in_merged_source', 0)} are duplicate copies inside a "
        f"merged PEMS source and {c.get('merged_into_a_site_row', 0)} sit inside a wider site "
        "row**: the site does write them, the old text-only scan could not see it.\n",
        f"- **{c.get('claimed_by_an_ambiguous_site_row', 0)} are explained by an ambiguous "
        "site row** and are an adjudication item, not a gap.\n",
        f"- **{c.get('prior_row_not_in_current_scope', 0)} could not be re-identified "
        "in this run's scope** and are named there with the document and page they do "
        "live on, and whether that PEMS page yields any level row in this parse (a "
        "non-zero number here is a scope/parse finding, not a rounding difference); "
        f"**{c.get('prior_claims_collapsed_into_one_current_row', 0)}** prior claims map "
        "onto a single PEMS row in this run's parse.\n",
        f"- **{delta['new_unpaired']['count']} rows are unpaired in this run but were not on "
        f"the old list** ({nc.get('absent', 0)} absent, {nc.get('duplicate_in_source', 0)} "
        f"duplicate, {nc.get('merged_into_site_row', 0)} merged) — the other direction of the "
        "delta, named in `reconciliation.json`.\n",
        "\nNo PEMS row in scope is lost between the two runs: every one carries exactly one "
        "disposition in `alignment.json`'s per-page `pems_row_ledger` (matched / claimed by an "
        "ambiguous site row / duplicate / merged / absent), and the ledger totals prove the "
        "sum.\n"]
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
         "- `shared_pems_row` — one PEMS row backs the site's TWO rows. Either the "
         "site row's label names an intervention whose PEMS row already backs a "
         "different site row (CPAP and SGA share p.123 row 3), or the site row has "
         "no distinctive label word and its every word is inside a PEMS row another "
         "site row already holds (\"A: Obtain IV access\" is the head of p.135 row 2, "
         "whose fluid-bolus tail the next row matched). The containment case carries "
         "`contained_in_pems` with the PEMS row, the overlapping words and the ratio.\n",
         "\nRows that carry `section_fallback: true` sit under a site section heading "
         "with no single PEMS counterpart, so they were scored against the whole page "
         "grid instead. That is an annotation on the row, never a disposition: the row "
         "is still `matched`, `ambiguous` or a gap on its own evidence.\n",
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
            tb = a.get("text_binding")
            L.append(f"- row **{a['site_row']}** ({a.get('section') or 'base section'}) "
                     f"[`{a.get('reason_kind', 'other')}`] — {a['action'][:150]}\n"
                     f"  - why: {a['reason']}\n"
                     + (f"  - evidence: `{'`, `'.join(ev)}`\n" if ev else "")
                     + (f"  - text pass: `{tb['verdict']}` / `{tb.get('subtype', tb.get('method'))}`"
                        f" — {tb.get('note') or ('bound: ' + tb.get('matched_phrase', ''))}"
                        f" (best coverage {tb['coverage']:.2f}, p.{tb['pems_page']} row "
                        f"{tb['pems_ordinal']}; see `text-binding.md`)\n"
                        if tb else ""))
    open(AMBIG_MD, "w", encoding="utf-8").write("".join(L))


# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stage", choices=["1", "2", "all"], default="all")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--rows-cache-only", action="store_true",
                    help="build only the git-ignored .cache/pems_rows.jsonl "
                         "(no pems_table.json / alignment.json / missing-rows.md "
                         "is written) — what the verifier runs on a clean checkout")
    args = ap.parse_args(argv)
    if args.rows_cache_only:
        recs = build_rows_cache()
        print(f"rows cache: {len(recs)} rows -> {os.path.relpath(ROWS_CACHE, REPO)}")
        return 0
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
