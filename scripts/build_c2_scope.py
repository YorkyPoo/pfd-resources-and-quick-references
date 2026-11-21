#!/usr/bin/env python3
"""Build audit/level-scan/c2-scope.json — the C2 adjudication queue.

WHY THIS SCRIPT EXISTS
----------------------
The C2 scope has been asserted by hand and been wrong. The total is never
written by hand: it is derived from the three sources, deduped by (file, row),
and asserted against `len(rows)`.

THE WORKLIST MUST HOLD EVERY ROW THE TOTAL COUNTS
-------------------------------------------------
An earlier revision published `core_ambiguous: 42` in `counts` while `rows`
held only the 19 held/named rows. The artifact then said 61 and the worklist
said 19 — a C2 worker would do 19 rows and report done. Every row the total
counts is now enumerated here: the 42 core rows are parsed live out of
ambiguous-rows.md and appended with the same field shape as the held rows.
`--verify` asserts len(rows) == derived_total explicitly.

THE HELD-ROW SPLIT IS A JOIN, NOT A GUESS
-----------------------------------------
An earlier revision carried a hand list (`KNOWN_DISAGREE`) of rows believed to
contradict PEMS, plus a hand `published` level per row. The two mechanisms
contradicted each other: the hand list vetoed the rule even when the rule said
the badge was contained, so every held row went to vision — inverting the
operator's instruction not to spend vision on rows whose level is already
correct. That is gone. For each row this script:

  1. loads the PEMS row by exact key (pems_page, pems_ordinal) from
     audit/level-scan/pems_table.json and FAILS LOUDLY if the key is missing;
  2. parses the site row's five level cells from the protocol page with
     pems_level_scan.read_page() — the same parser the scanner uses, never a
     hand transcription;
  3. compares column by column under the standing doctrine:
       - a badge at level X authorises X and above (the table's `columns{}`
         already encodes that spread);
       - bare `MC` in every cell = all levels must contact Medical Control;
       - a blank site cell where PEMS prints a level = the site does not
         authorise it.

Verdicts:
  agrees        site grants the PEMS level or a superset -> rule_clear, no vision
  site_broader  site authorises a level PEMS does not     -> LIABILITY CASE
  site_narrower site blocks a level PEMS authorises
  site_gap      site prints no level at all where PEMS prints one
  ambiguous     (multiple_candidates only) the candidate PEMS rows do not agree
                on the verdict, so the join cannot settle the row by itself

DISPOSITIONS ARE AN OPERATOR RULING, NOT AN INFERENCE
-----------------------------------------------------
  held_level_correct       7 held rows where the join says `agrees`. Their level
                           is right; the open question is which SITE row owns the
                           PEMS row (the site splits what PEMS merges). They go
                           to the split-review list, must NOT enter `matched`
                           (that would put two site rows on one PEMS row), and
                           are EXCLUDED from C3's apply set — no cells change.
  ownership_adjudication   8 held rows where the join disagrees, minus the
                           site_gap row. Ownership calls: choosing the owner
                           determines the level.
  site_gap_add             03_Respiratory_Arrest_PROC.md row 11. No owner to
                           choose and no level printed on the page: carry the
                           PEMS columns through to C3 as an ADD.
  ambiguous_adjudication   42 core rows (multiple_candidates + shared_pems_row),
                           reason_kind preserved.
  named_item               3 named extras still needing a human.

SOURCES
-------
held_*             the 16 best_evidence_is_held rows, split by the join above.
core_ambiguous     parsed live from ambiguous-rows.md at run time (42 rows:
                   11 multiple_candidates + 31 shared_pems_row).
extra_named        the named extras still requiring a human.

VISION BUDGET
-------------
Vision is spent ONLY where `badge_tokens` is itself ambiguous — two badges on
one line, a bracket/parenthetical level conflict, or margins that contradict the
badge. The join already answered every level, so no raster is ever needed to
re-derive one. `needs_vision` is computed per row by re-reading the referenced
PEMS row's verbatim_text; it is not a hand flag.

EXCLUDED
--------
06_Overdose_Poisoning row 5 — text-binding settled it (site A+ vs PEMS EMT).
It belongs on the fix list, not in the queue. See text-binding.md.

Run: python3 scripts/build_c2_scope.py [--write] [--verify] [--table]
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import pems_level_scan as PLS  # noqa: E402  (read_page / cells are the parser of record)

OUT = os.path.join(REPO, "audit", "level-scan", "c2-scope.json")
AMBIG = os.path.join(REPO, "audit", "level-scan", "ambiguous-rows.md")
TABLE = os.path.join(REPO, "audit", "level-scan", "pems_table.json")
ALIGN = os.path.join(REPO, "audit", "level-scan", "alignment.json")
DOCS = os.path.join(REPO, "docs")

LV = ["EMR", "EMT", "A", "I", "P"]

# (site file, site row number, PEMS page, PEMS ordinal). No badge, no published
# level, no verdict: all three are derived from the join.
HELD = [
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 4,  63,  7),
    ("protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md",     6,  61,  5),
    ("protocols/cardiac/04_Chest_Pain_ACS_PROC.md",              13,  107, 9),
    ("protocols/cardiac/04_Chest_Pain_ACS_PROC.md",               5,  107, 4),
    ("protocols/neurologic/05_Stroke_TIA_PROC.md",                6,  131, 4),
    ("protocols/neurologic/05_Stroke_TIA_PROC.md",                7,  131, 4),
    ("protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md", 3, 153, 2),
    ("protocols/respiratory/03_Pneumothorax_PROC.md",            11,  243, 4),
    ("protocols/respiratory/03_Respiratory_Arrest_PROC.md",      11,  239, 2),
    ("protocols/respiratory/03_Respiratory_Distress_PROC.md",    10,  124, 10),
    ("protocols/respiratory/03_Respiratory_Distress_PROC.md",     8,  123, 1),
    ("protocols/respiratory/03_Smoke_Inhalation_PROC.md",        11,  153, 2),
    ("protocols/respiratory/03_Smoke_Inhalation_PROC.md",         4,  153, 2),
    ("protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md", 3,  239, 3),
    ("protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md", 8,  239, 6),
    ("protocols/trauma/09_Trauma_PROC.md",                        7,  83,  10),
]

# The site_gap held row: no owner to choose, no level printed -> C3 ADD.
SITE_GAP_ADD = ("protocols/respiratory/03_Respiratory_Arrest_PROC.md", 11)

# (site file, site row, why, PEMS page, PEMS ordinal or None)
EXTRA_NAMED = [
    ("protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md", 5, 63, 7,
     "PEMS p.63 badge I but the line says 'AED is advising to shock [EMR]' inline"),
    ("protocols/respiratory/03_Respiratory_Distress_PROC.md", None, None, None,
     "PEMS p.125 pearl tail truncated in every text extraction"),
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", None, None, None,
     "amiodarone 300 mg vs 150 mg row pairing (C1 false-confidence case)"),
]

EXCLUDED = [
    ("protocols/toxicology/06_Overdose_Poisoning_PROC.md", 5,
     "text-binding settled: site A+ vs PEMS EMT -> fix list, not queue"),
]

# The operator ruling, in code. The histogram is asserted against this.
EXPECTED_DISPOSITIONS = {
    "held_level_correct": 7,
    "ownership_adjudication": 8,
    "site_gap_add": 1,
    "ambiguous_adjudication": 42,
    "named_item": 3,
}

# Instruction recorded for whoever adjudicates the two badge contradictions.
# Verbatim in substance, because it decides WHICH question is being asked: if a
# contradiction text is compound, the row is a PEMS row the site split (the
# `held_level_correct` class) and the fix is an authoring decision, not a level.
NOTES_FOR_ADJUDICATOR = [
    "**Test \"one row or two\" before choosing a level.** Both contradiction "
    "texts look compound:",
    "- `Apply AED or cardiac monitor. Assess rhythm (I / P)` may mean EMT applies "
    "the AED while I/P assess rhythm.",
    "- `or AED is advising to shock [EMR], immediately defibrillate` may mean EMR "
    "may use the AED, with the badge covering the advanced step.",
    "If either is compound, these are **PEMS rows the site split**, not "
    "mis-decoded badges — which puts them in the `held_level_correct` class and "
    "makes the fix an **authoring decision, not a level fix**. Settle the shape "
    "before the number. Do not write a level until you know whether you are "
    "writing one row or two.",
]

DISPOSITION_LEGEND = {
    "held_level_correct": ("level is right; the open question is which site row "
                           "owns the PEMS row. Split-review list. NOT matched, "
                           "NOT in C3's apply set, no cells change."),
    "ownership_adjudication": ("ownership call — choosing the owner determines "
                               "the level. Not a level question."),
    "site_gap_add": ("no owner to choose and no level printed on the page; carry "
                     "the PEMS columns through to C3 as an ADD."),
    "ambiguous_adjudication": ("structure could not settle the row; reason_kind "
                               "says which shape of ambiguity."),
    "named_item": "named extra still requiring a human.",
}

CORE_KINDS = ("multiple_candidates", "shared_pems_row")
KEY_RE = re.compile(r"p\.(\d+) row (\d+)")


# --------------------------------------------------------------------------
# join
# --------------------------------------------------------------------------
def load_pems_index():
    """(page, ordinal) -> PEMS row record. Duplicate keys are a hard error."""
    doc = json.load(open(TABLE, encoding="utf-8"))
    idx = {}
    for section in doc["pems_docs"]:
        for row in section["rows"]:
            key = (row["page"], row["ordinal"])
            if key in idx:
                raise SystemExit(f"pems_table.json: duplicate key {key}")
            idx[key] = row
    return idx


def site_cells_for(rel, row_num):
    """Parse the site page with the scanner's own parser and return the row's
    five level cells. Missing or duplicated row numbers are hard errors.

    The page may be in the legacy 7-column matrix or in the collapsed one-chip
    format scripts/level_rule.py writes. Both are read: one chip at level X is
    the same statement as filling X and the columns above it, which is the shape
    `compare()` below compares column-by-column. Reading only the matrix made a
    converted page raise "no EMR|EMT|A|I|P table", and the re-check silently
    dropped every such row from its at-risk list — a parse gap reported as a
    clean result, which is the one thing this re-check exists to prevent.
    """
    path = os.path.join(DOCS, rel)
    page = PLS.read_action_rows(path)
    if page.get("format") is None:
        raise SystemExit(f"{rel}: no EMR|EMT|A|I|P table and no collapsed level table")
    hits = [r for r in page["rows"] if str(r["num"]).strip() == str(row_num)]
    if len(hits) != 1:
        raise SystemExit(f"{rel}: row {row_num} matched {len(hits)} site rows")
    return [c.strip() for c in hits[0]["cells"]], hits[0]["action"]


def compare(pems_columns, site_cells):
    """Column-by-column comparison. Returns (verdict, direction, detail)."""
    pems_levels = [L for L in LV if (pems_columns.get(L) or "").strip()]
    site_levels = [L for L in LV if site_cells[LV.index(L)].strip()]
    pems_all_mc = all((pems_columns.get(L) or "").strip().upper() == "MC" for L in LV)
    site_all_mc = all("MC" in c.upper() for c in site_cells)

    if pems_all_mc:
        if site_all_mc:
            return "agrees", None, "PEMS MC in every column; site MC in every column"
        if not site_levels:
            return "disagrees", "site_gap", "PEMS MC in every column; site prints no level"
        return ("disagrees", "site_broader",
                f"PEMS requires MC at every level; site grants {'/'.join(site_levels)}")

    broader = [L for L in site_levels if L not in pems_levels]
    narrower = [L for L in pems_levels if L not in site_levels]

    if not site_levels:
        return ("disagrees", "site_gap",
                f"PEMS grants {'/'.join(pems_levels)}; site prints no level")
    if broader:
        return ("disagrees", "site_broader",
                f"site grants {'/'.join(broader)} which PEMS does not "
                f"(PEMS {'/'.join(pems_levels)})")
    if narrower:
        return ("disagrees", "site_narrower",
                f"site blocks {'/'.join(narrower)} which PEMS grants "
                f"(PEMS {'/'.join(pems_levels)})")
    return "agrees", None, f"site grants {'/'.join(site_levels)}; PEMS {'/'.join(pems_levels)}"


def aggregate_verdict(candidate_verdicts):
    """One row-level verdict from the per-candidate joins.

    All candidates agreeing -> that verdict. Candidates disagreeing -> the join
    has not settled the row, so the verdict says so instead of picking one.
    """
    shapes = {(v, d) for v, d in candidate_verdicts}
    if len(shapes) == 1:
        return candidate_verdicts[0]
    return "ambiguous", None


# --------------------------------------------------------------------------
# badge ambiguity -> needs_vision
# --------------------------------------------------------------------------
BRACKET_RE = re.compile(r"\[(EMR|EMT|A|I|P)\]")
PAREN_RE = re.compile(r"\((EMR|EMT|A|I|P)(?:\s*/\s*(EMR|EMT|A|I|P))+\)")
ONLY_RE = re.compile(r"\b((?:EMR|EMT|A|I|P)(?:\s*/\s*(?:EMR|EMT|A|I|P))+)\s+only\b")


def badge_ambiguity(pems_row):
    """Is the PEMS row's badge itself ambiguous? Returns (bool, reason|None).

    Only three shapes count, per the operator's vision budget:
      - two badges on one line (two bracket markers naming different levels);
      - a bracket/parenthetical level that contradicts the badge;
      - margins that contradict the badge (first printed column is not the
        badge's own level).

    A marker that merely restates the badge (the table records `[A]` and `A` for
    the same line) is not a conflict, and a level that the badge already settles
    is never ambiguous — so this never re-derives a level from a raster.
    """
    text = pems_row.get("verbatim_text") or ""
    raw_badge = (pems_row.get("badge_tokens") or [None])[0]
    # the table records both `A` and `[A]` for a bracketed source badge
    badge = (raw_badge or "").strip().strip("[]").strip().upper()
    if badge == "MC":
        # every column is Medical Control; any level marker contradicts that
        spread = []
    elif badge in LV:
        spread = LV[LV.index(badge):]
    else:
        return True, f"badge token {raw_badge!r} is neither a level nor MC"

    markers = []
    for m in BRACKET_RE.finditer(text):
        markers.append((m.group(0), [m.group(1)]))
    for m in PAREN_RE.finditer(text):
        markers.append((m.group(0), [x for x in m.group(1).split("/") if x]))
    for m in ONLY_RE.finditer(text):
        markers.append((m.group(0), [x.strip() for x in m.group(1).split("/") if x.strip()]))

    # a marker that just restates the badge is the badge, not a second opinion
    markers = [(raw, lv) for raw, lv in markers
               if not (len(lv) == 1 and lv[0] == badge)]

    if markers:
        for raw, levels in markers:
            if levels != spread:
                return (True,
                        f"PEMS p.{pems_row['page']} #{pems_row['ordinal']}: badge "
                        f"{badge} authorises "
                        f"{'/'.join(spread) if spread else 'MC in every column'} but "
                        f"the line prints {raw!r}")
        if len({tuple(lv) for _, lv in markers}) > 1:
            return (True,
                    f"PEMS p.{pems_row['page']} #{pems_row['ordinal']}: two different "
                    f"level markers on one line: "
                    + ", ".join(sorted({raw for raw, _ in markers})))

    cols = [L for L in LV if (pems_row["columns"].get(L) or "").strip()]
    if badge in LV and cols and cols[0] != badge:
        return (True,
                f"PEMS p.{pems_row['page']} #{pems_row['ordinal']}: badge {badge} but "
                f"the first printed column is {cols[0]} (contradictory margins)")
    return False, None


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------
SEC_RE = re.compile(r"^## `([^`]+)` — (\d+) ambiguous\s*$")
ROW_RE = re.compile(r"^- row \*\*(\d+[a-z]?)\*\* \(([^)]*)\) \[`([a-z_]+)`\] — (.*)$")
TOTAL_RE = re.compile(
    r"^\*\*Total: (\d+) rows\*\* \(multiple_candidates (\d+), no_counterpart (\d+), "
    r"shared_pems_row (\d+)\)", re.M)


def read_ambiguous_md():
    """Parse ambiguous-rows.md into row records. Hard-fails when the file's own
    totals and per-section counts do not match what was parsed."""
    txt = open(AMBIG, encoding="utf-8").read()
    lines = txt.splitlines()

    m = TOTAL_RE.search(txt)
    if not m:
        raise SystemExit("ambiguous-rows.md: total line not found")
    stated_total, stated_mc, stated_nc, stated_sh = (int(x) for x in m.groups())

    recs, cur, section_expected, section_seen = [], None, {}, {}
    for ln in lines:
        ms = SEC_RE.match(ln)
        if ms:
            cur = ms.group(1)
            section_expected[cur] = int(ms.group(2))
            continue
        mr = ROW_RE.match(ln)
        if mr and cur:
            recs.append({"file": cur, "row": row_key(mr.group(1)),
                         "section": mr.group(2), "reason_kind": mr.group(3),
                         "action_head": mr.group(4)})
            section_seen[cur] = section_seen.get(cur, 0) + 1
        elif ln.startswith("  - why: ") and recs and "why" not in recs[-1]:
            recs[-1]["why"] = ln[len("  - why: "):]
        elif ln.startswith("  - evidence: ") and recs:
            recs[-1]["evidence"] = ln[len("  - evidence: "):]

    if len(recs) != stated_total:
        raise SystemExit(f"ambiguous-rows.md: parsed {len(recs)} rows, header says {stated_total}")
    kinds = {}
    for r in recs:
        kinds[r["reason_kind"]] = kinds.get(r["reason_kind"], 0) + 1
    stated_kinds = {"multiple_candidates": stated_mc,
                    "no_counterpart": stated_nc,
                    "shared_pems_row": stated_sh}
    if kinds != stated_kinds:
        raise SystemExit(f"ambiguous-rows.md: kind counts {kinds} != header {stated_kinds}")
    bad = {f: (section_expected[f], section_seen.get(f, 0))
           for f in section_expected if section_expected[f] != section_seen.get(f, 0)}
    if bad:
        raise SystemExit(f"ambiguous-rows.md: per-section count mismatch {bad}")
    missing_why = [(r["file"], r["row"]) for r in recs if "why" not in r]
    if missing_why:
        raise SystemExit(f"ambiguous-rows.md: rows with no 'why' line: {missing_why}")
    return recs, stated_kinds


def row_key(value):
    """A site row label as a lookup key: ints stay ints, split labels stay str.

    `row_splits.yaml` names split rows `4a`/`5a`; `int()` on those raised
    ValueError and crashed the re-check the first time a regenerated alignment
    carried one.
    """
    s = str(value).strip()
    return int(s) if s.isdigit() else s


def load_alignment_index():
    doc = json.load(open(ALIGN, encoding="utf-8"))
    return {(p["site_page"], row_key(r["site_row"])): r
            for p in doc["pages"] for r in p["rows"]}


def core_pems_refs(rec, align_idx):
    """PEMS (page, ordinal) references for a core_ambiguous row.

    shared_pems_row  -> the `contained_in_pems` row when the aligner recorded
                        one, else the single row named in the why line.
    multiple_candidates -> every candidate named in the why line, in rank order
                        (first = best similarity).
    """
    a = align_idx.get((rec["file"], rec["row"]))
    if a is None:
        raise SystemExit(f"alignment.json has no record for {rec['file']} row {rec['row']}")
    if a.get("reason") != rec["why"]:
        raise SystemExit(
            f"{rec['file']} row {rec['row']}: why line differs between "
            f"ambiguous-rows.md and alignment.json\n  md : {rec['why']}\n  al : {a.get('reason')}")

    if rec["reason_kind"] == "shared_pems_row":
        ci = a.get("contained_in_pems")
        if ci:
            return [(ci["pems_page"], ci["pems_ordinal"])], "contained_in_pems"
        keys = [(int(p), int(o)) for p, o in KEY_RE.findall(rec["why"])]
        if len(keys) != 1:
            raise SystemExit(f"{rec['file']} row {rec['row']}: shared_pems_row names "
                             f"{len(keys)} PEMS rows, expected exactly 1")
        return keys, "named_row"

    keys = [(int(p), int(o)) for p, o in KEY_RE.findall(rec["why"])]
    seen, ordered = set(), []
    for k in keys:
        if k not in seen:
            seen.add(k)
            ordered.append(k)
    if len(ordered) < 2:
        raise SystemExit(f"{rec['file']} row {rec['row']}: multiple_candidates names "
                         f"{len(ordered)} distinct PEMS rows, expected >= 2")
    return ordered, "candidates"


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------
def disposition_for(bucket, verdict, direction, file, row):
    """The operator ruling, applied. No inference."""
    if bucket == "held_agrees":
        return "held_level_correct"
    if bucket == "held_disagrees":
        if (file, row) == SITE_GAP_ADD and direction == "site_gap":
            return "site_gap_add"
        return "ownership_adjudication"
    if bucket == "core_ambiguous":
        return "ambiguous_adjudication"
    if bucket == "extra_named":
        return "named_item"
    raise SystemExit(f"no disposition rule for bucket {bucket}")


ADJUDICATION = {
    "held_level_correct": "split_review",
    "ownership_adjudication": "ownership",
    "site_gap_add": "add",
    "ambiguous_adjudication": "adjudicate",
    "named_item": "named_item",
}


def pems_keys_of(rec: dict, align_idx: dict) -> list[tuple[int, int]]:
    """Every PEMS (page, ordinal) a queue row is joined to.

    pems_page/pems_ordinal is the primary key; a `multiple_candidates` row also
    names alternates; the aligner's record adds the container of a
    `shared_pems_row` and the row a text binding cites. Used to decide which rows
    depend on an unresolved badge — a row is provisional if ANY of its keys is.
    """
    keys: list[tuple[int, int]] = []

    def push(p, o):
        if p is None or o is None:
            return
        k = (int(p), int(o))
        if k not in keys:
            keys.append(k)

    push(rec.get("pems_page"), rec.get("pems_ordinal"))
    for c in rec.get("pems_candidates") or []:
        push(c.get("pems_page"), c.get("pems_ordinal"))
    if rec.get("row") is not None:
        a = align_idx.get((rec["file"], rec["row"])) or {}
        ci = a.get("contained_in_pems") or {}
        push(ci.get("pems_page"), ci.get("pems_ordinal"))
        tb = a.get("text_binding") or {}
        push(tb.get("pems_page"), tb.get("pems_ordinal"))
        for pp, oo in KEY_RE.findall(a.get("reason") or ""):
            push(pp, oo)
    return keys


def build():
    rows, seen, dropped = [], set(), []
    pems_idx = load_pems_index()
    align_idx = load_alignment_index()

    def add(rec):
        key = (rec["file"], rec["row"])
        if key in seen:
            # Keep the richer record: held/named rows carry the join already.
            dropped.append({"file": rec["file"], "row": rec["row"],
                            "dropped_bucket": rec["source_bucket"],
                            "kept_bucket": next(r["source_bucket"] for r in rows
                                                if (r["file"], r["row"]) == key)})
            return False
        seen.add(key)
        rows.append(rec)
        return True

    # ---- held rows: the split is the join -------------------------------
    held_split = []
    for f, r, page, ordn in HELD:
        key = (page, ordn)
        if key not in pems_idx:
            raise SystemExit(f"join failed: PEMS key {key} for {f} row {r} "
                             f"is not in pems_table.json")
        pems = pems_idx[key]
        pems_columns = {L: (pems["columns"].get(L) or "") for L in LV}
        cells, action = site_cells_for(f, r)
        verdict, direction, why = compare(pems_columns, cells)
        nv, nv_reason = badge_ambiguity(pems)
        bucket = "held_agrees" if verdict == "agrees" else "held_disagrees"
        held_split.append(bucket)
        rec = {
            "file": f, "row": r,
            "source_bucket": bucket,
            "reason_kind": "shared_pems_row",
            "detail": why,
            "disposition": disposition_for(bucket, verdict, direction, f, r),
            "adjudication": None,  # filled below from disposition
            "decision": "",
            "needs_vision": nv,
            "needs_vision_reason": nv_reason,
            "pems_page": page,
            "pems_ordinal": ordn,
            "pems_columns_basis": "named_row",
            "pems_columns": pems_columns,
            "badge_tokens": list(pems.get("badge_tokens") or []),
            "site_cells": cells,
            "site_action": action[:160],
            "verdict": verdict,
        }
        if verdict == "disagrees":
            rec["direction"] = direction
        rec["adjudication"] = ADJUDICATION[rec["disposition"]]
        add(rec)

    # ---- named extras ----------------------------------------------------
    for f, r, page, ordn, why in EXTRA_NAMED:
        rec = {
            "file": f, "row": r,
            "source_bucket": "extra_named",
            "reason_kind": "named_item",
            "detail": why,
            "disposition": "named_item",
            "adjudication": ADJUDICATION["named_item"],
            "decision": "",
        }
        if page is not None and ordn is not None:
            key = (page, ordn)
            if key not in pems_idx:
                raise SystemExit(f"join failed: PEMS key {key} for named item {f} row {r}")
            pems = pems_idx[key]
            rec["pems_page"] = page
            rec["pems_ordinal"] = ordn
            rec["pems_columns_basis"] = "named_row"
            rec["pems_columns"] = {L: (pems["columns"].get(L) or "") for L in LV}
            rec["badge_tokens"] = list(pems.get("badge_tokens") or [])
            nv, nv_reason = badge_ambiguity(pems)
            rec["needs_vision"] = nv
            rec["needs_vision_reason"] = nv_reason
            if r is not None:
                cells, action = site_cells_for(f, r)
                rec["site_cells"] = cells
                rec["site_action"] = action[:160]
                verdict, direction, det = compare(rec["pems_columns"], cells)
                rec["verdict"] = verdict
                if verdict == "disagrees":
                    rec["direction"] = direction
                rec["detail"] = why
        else:
            rec["pems_page"] = None
            rec["pems_ordinal"] = None
            rec["pems_columns"] = None
            rec["pems_columns_null_reason"] = (
                "no single PEMS row: the item is a page-level defect, not a "
                "row-level pairing (see text-binding.md / extra-named list)")
            rec["badge_tokens"] = []
            rec["needs_vision"] = False
            rec["needs_vision_reason"] = None
            rec["site_cells"] = None
            rec["site_cells_null_reason"] = (
                "named item names no site row number")
        add(rec)

    # ---- core ambiguous: every row, parsed live --------------------------
    all_ambig, kinds = read_ambiguous_md()
    core = [r for r in all_ambig if r["reason_kind"] in CORE_KINDS]
    if len(core) != sum(kinds[k] for k in CORE_KINDS):
        raise SystemExit("core_ambiguous row count does not match the md's kind totals")

    for c in core:
        refs, basis = core_pems_refs(c, align_idx)
        candidates = []
        for page, ordn in refs:
            key = (page, ordn)
            if key not in pems_idx:
                raise SystemExit(f"join failed: PEMS key {key} for {c['file']} "
                                 f"row {c['row']} is not in pems_table.json")
            pems = pems_idx[key]
            cols = {L: (pems["columns"].get(L) or "") for L in LV}
            cells, action = site_cells_for(c["file"], c["row"])
            verdict, direction, det = compare(cols, cells)
            nv, nv_reason = badge_ambiguity(pems)
            cand = {"pems_page": page, "pems_ordinal": ordn,
                    "pems_columns": cols,
                    "badge_tokens": list(pems.get("badge_tokens") or []),
                    "verdict": verdict,
                    "detail": det,
                    "needs_vision": nv}
            if direction:
                cand["direction"] = direction
            if nv_reason:
                cand["needs_vision_reason"] = nv_reason
            candidates.append(cand)

        cells, action = site_cells_for(c["file"], c["row"])
        verdict, direction = aggregate_verdict([(x["verdict"], x.get("direction"))
                                                for x in candidates])
        primary = candidates[0]
        rec = {
            "file": c["file"], "row": c["row"],
            "source_bucket": "core_ambiguous",
            "reason_kind": c["reason_kind"],
            "detail": c["why"],
            "disposition": "ambiguous_adjudication",
            "adjudication": ADJUDICATION["ambiguous_adjudication"],
            "decision": "",
            "needs_vision": any(x["needs_vision"] for x in candidates),
            "needs_vision_reason": next((x["needs_vision_reason"] for x in candidates
                                         if x.get("needs_vision_reason")), None),
            "pems_page": primary["pems_page"],
            "pems_ordinal": primary["pems_ordinal"],
            "pems_columns_basis": basis,
            "pems_columns": primary["pems_columns"],
            "badge_tokens": primary["badge_tokens"],
            "site_cells": cells,
            "site_action": action[:160],
            "verdict": verdict,
        }
        if c["reason_kind"] == "multiple_candidates":
            rec["pems_candidates"] = candidates
        if c.get("evidence"):
            rec["evidence"] = c["evidence"]
        if verdict == "disagrees":
            rec["direction"] = direction
        add(rec)

    # ---- provisional direction, at-risk rows, adjudicator notes -----------
    # A verdict that turns on an unresolved badge is PROVISIONAL: p.63 #7 prints
    # `[EMR]` inline but carries badge `I`, so `04_Cardiac_Arrest_Non_Traumatic`
    # r4 reads `site_broader` today and would read `site_narrower` if the raster
    # settles EMR. C3 and the handoff must be able to filter those out instead of
    # applying a direction that is about to invert.
    import recheck_ambiguous_badges as RC  # lazy: RC imports this module

    resolved_keys = set(RC.load_overrides())
    unresolved = {k for k, pems in pems_idx.items()
                  if k not in resolved_keys and badge_ambiguity(pems)[0]}
    for x in rows:
        hit = [k for k in pems_keys_of(x, align_idx) if k in unresolved]
        if hit:
            x["provisional"] = True
            x["provisional_reason"] = ("depends on unresolved badge for PEMS "
                                       + ", ".join(f"p.{p}#{o}" for p, o in hit))
    provisional = [{"file": x["file"], "row": x["row"],
                    "pems_keys": [f"p.{p}#{o}" for p, o in
                                  pems_keys_of(x, align_idx) if (p, o) in unresolved],
                    "verdict": x.get("verdict"),
                    "direction": x.get("direction"),
                    "provisional_reason": x["provisional_reason"]}
                   for x in rows if x.get("provisional")]
    # every site row mapped to p.61#4 / p.63#7 that is NOT already in this queue:
    # after a raster lands these are the rows that can silently flip
    at_risk = RC.at_risk_rows(exclude={(x["file"], x["row"]) for x in rows})

    # ---- derived totals --------------------------------------------------
    held = [x for x in rows if x["source_bucket"].startswith("held_")]
    agrees = [x for x in held if x["verdict"] == "agrees"]
    disagrees = [x for x in held if x["verdict"] == "disagrees"]
    hist = {}
    for x in disagrees:
        hist[x["direction"]] = hist.get(x["direction"], 0) + 1

    disp_hist = {}
    for x in rows:
        disp_hist[x["disposition"]] = disp_hist.get(x["disposition"], 0) + 1

    derived_total = len(HELD) + len(core) + len(EXTRA_NAMED) - len(dropped)
    needs_vision = [{"file": x["file"], "row": x["row"],
                     "pems_page": x.get("pems_page"),
                     "pems_ordinal": x.get("pems_ordinal"),
                     "why": x["needs_vision_reason"]}
                    for x in rows if x["needs_vision"]]
    split_review = [{"file": x["file"], "row": x["row"],
                     "pems_page": x["pems_page"], "pems_ordinal": x["pems_ordinal"],
                     "site_cells": x["site_cells"],
                     "pems_columns": x["pems_columns"]}
                    for x in rows if x["disposition"] == "held_level_correct"]

    doc = {
        "note": ("C2 queue. Every row the total counts is enumerated in `rows`; "
                 "the total is derived from the three sources minus dedupe, never "
                 "hand-summed. Dedupe is by (file, row). The held-row split and "
                 "every verdict are a join against pems_table.json by "
                 "(pems_page, pems_ordinal) — no hand verdicts, no hand published "
                 "levels. Core ambiguous rows are parsed live from "
                 "ambiguous-rows.md. Dispositions encode an operator ruling, not an "
                 "inference; see disposition_legend."),
        "disposition_legend": DISPOSITION_LEGEND,
        "counts": {
            "rows_listed_here": len(rows),
            "derived_total": derived_total,
            "source_derivation": {
                "held_rows": len(HELD),
                "core_ambiguous_from_md": len(core),
                "core_ambiguous_by_kind": {k: kinds[k] for k in CORE_KINDS},
                "extra_named": len(EXTRA_NAMED),
                "dedupe_dropped": len(dropped),
            },
            "disposition_histogram": disp_hist,
            "disposition_expected": EXPECTED_DISPOSITIONS,
            "held_total": len(held),
            # bucket counts: the ruling (not a hand rule) turns `held_agrees`
            # into held_level_correct below; these are the join's own counts
            "held_agrees": len(agrees),
            "held_disagrees": len(disagrees),
            "held_direction_histogram": hist,
            "site_broader": [{"file": x["file"], "row": x["row"],
                              "pems_columns": x["pems_columns"],
                              "site_cells": x["site_cells"]}
                             for x in disagrees if x["direction"] == "site_broader"],
            "split_review_list": split_review,
            "c3_apply_excluded": [{"file": x["file"], "row": x["row"]}
                                  for x in rows
                                  if x["disposition"] == "held_level_correct"],
            "c3_apply_candidates": len(rows) - len(split_review),
            "needs_vision_count": len(needs_vision),
            "needs_vision": needs_vision,
            # rows whose verdict/direction turns on a badge that is still
            # internally contradictory — C3 and the handoff filter on this
            "provisional_count": len(provisional),
            "provisional": provisional,
            # every site row mapped to p.61#4 / p.63#7 that is NOT in this queue;
            # currently `matched`, invisible today, defect if the badge settles
            "at_risk_matched_rows_count": len(at_risk),
            "at_risk_matched_rows": at_risk,
            "dedupe_dropped": dropped,
        },
        "notes_for_adjudicator": NOTES_FOR_ADJUDICATOR,
        "excluded": [{"file": f, "row": r, "why": w} for f, r, w in EXCLUDED],
        "rows": rows,
    }
    return doc


def main():
    doc = build()
    c = doc["counts"]
    print(json.dumps({k: v for k, v in c.items()
                      if k not in ("site_broader", "split_review_list",
                                   "c3_apply_excluded", "needs_vision",
                                   "provisional", "at_risk_matched_rows",
                                   "dedupe_dropped", "disposition_legend")}, indent=2))
    print()
    print("rows enumerated       :", c["rows_listed_here"])
    print("DERIVED C2 TOTAL      :", c["derived_total"])
    print("  held                  :", c["held_total"],
          f"(agrees {c['held_agrees']}, disagrees {c['held_disagrees']})")
    print("  core ambiguous        :", c["source_derivation"]["core_ambiguous_from_md"],
          c["source_derivation"]["core_ambiguous_by_kind"])
    print("  extra named           :", c["source_derivation"]["extra_named"])
    print("  dedupe dropped        :", c["source_derivation"]["dedupe_dropped"])
    print("  direction histogram   :", c["held_direction_histogram"])
    print("  site_broader (liability):", len(c["site_broader"]))
    print()
    print("DISPOSITION HISTOGRAM")
    for k in ("held_level_correct", "ownership_adjudication", "site_gap_add",
              "ambiguous_adjudication", "named_item"):
        print(f"  {k:24s} {c['disposition_histogram'].get(k, 0):3d}"
              f"   (expected {EXPECTED_DISPOSITIONS[k]})")
    print(f"  {'TOTAL':24s} {sum(c['disposition_histogram'].values()):3d}"
          f"   (rows {c['rows_listed_here']})")
    print()
    print(f"NEEDS_VISION : {c['needs_vision_count']}")
    for n in c["needs_vision"]:
        print(f"  - {os.path.basename(n['file'])} row {n['row']} "
              f"(PEMS p.{n['pems_page']} #{n['pems_ordinal']}): {n['why']}")
    print()
    print(f"PROVISIONAL  : {c['provisional_count']} (verdict/direction depends on "
          "an unresolved badge)")
    for n in c["provisional"]:
        print(f"  - {os.path.basename(n['file'])} row {n['row']} "
              f"{n['verdict'] or ''} {n['direction'] or ''} — {n['provisional_reason']}")
    print()
    print(f"AT_RISK (matched, not queued): {c['at_risk_matched_rows_count']}")
    for n in c["at_risk_matched_rows"]:
        print(f"  - {os.path.basename(n['file'])} row {n['row']} "
              f"(PEMS p.{n['pems_page']} #{n['pems_ordinal']}) flips to "
              f"{'/'.join(n['directions']) or '—'} if badge settles "
              f"{'/'.join(n['flips_if_badge'])}")
    print()
    print("DEDUPE       :", "none — no (file, row) appears in two buckets"
          if not c["dedupe_dropped"] else c["dedupe_dropped"])
    print()
    print("SPLIT-REVIEW LIST (held_level_correct — no cells change, not in matched)")
    for s in c["split_review_list"]:
        pc = "/".join(s["pems_columns"][L] or "·" for L in LV)
        sc = "/".join(x or "·" for x in s["site_cells"])
        print(f"  - {os.path.basename(s['file'])} row {s['row']} "
              f"(PEMS p.{s['pems_page']} #{s['pems_ordinal']}) PEMS {pc} | site {sc}")

    if "--table" in sys.argv:
        print("\n| file | row | bucket | disposition | PEMS p/# | PEMS cols "
              "(EMR/EMT/A/I/P) | site cells | verdict | direction | vision |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for r in doc["rows"]:
            pc = ("/".join(r["pems_columns"][L] or "·" for L in LV)
                  if r.get("pems_columns") else "—")
            sc = ("/".join(x or "·" for x in r["site_cells"])
                  if r.get("site_cells") else "—")
            pp = (f"{r['pems_page']}/{r['pems_ordinal']}"
                  if r.get("pems_page") is not None else "—")
            print(f"| {os.path.basename(r['file'])} | {r['row']} | "
                  f"{r['source_bucket']} | {r['disposition']} | {pp} | {pc} | {sc} | "
                  f"{r.get('verdict', '—')} | {r.get('direction') or ''} | "
                  f"{'YES' if r['needs_vision'] else ''} |")

    if "--verify" in sys.argv:
        verify(doc)
        print("\nverify: OK")

    if "--write" in sys.argv:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1)
        print("\nwrote", OUT)


def verify(doc):
    rows, c = doc["rows"], doc["counts"]

    # 1. every counted row is enumerated, and the total is derivable
    assert len(rows) == c["derived_total"], (
        f"rows {len(rows)} != derived_total {c['derived_total']}")
    src = c["source_derivation"]
    recomputed = (src["held_rows"] + src["core_ambiguous_from_md"]
                  + src["extra_named"] - src["dedupe_dropped"])
    assert recomputed == c["derived_total"], (
        f"derived_total {c['derived_total']} != sources {recomputed}")
    assert c["derived_total"] == 61, f"derived total {c['derived_total']} != 61"
    assert src["core_ambiguous_from_md"] == sum(src["core_ambiguous_by_kind"].values())

    # 2. no duplicate (file, row), and any dedupe is named
    keys = [(r["file"], r["row"]) for r in rows]
    assert len(keys) == len(set(keys)), "duplicate (file,row) in queue"
    assert len(rows) + len(c["dedupe_dropped"]) == (
        src["held_rows"] + src["core_ambiguous_from_md"] + src["extra_named"]), (
        "rows + dedupe drops != the three sources")
    for d in c["dedupe_dropped"]:
        assert (d["file"], d["row"]) not in set(keys), (
            f"dedupe dropped {(d['file'], d['row'])} but it is still listed")

    # 3. disposition histogram matches the ruling and covers every row
    assert c["disposition_histogram"] == EXPECTED_DISPOSITIONS, (
        f"disposition histogram {c['disposition_histogram']} != ruling "
        f"{EXPECTED_DISPOSITIONS}")
    assert sum(c["disposition_histogram"].values()) == len(rows)

    # 4. every row: disposition, verdict, direction reproducible from the artifact
    align_idx = load_alignment_index()
    pems_idx = load_pems_index()
    for r in rows:
        d = disposition_for(r["source_bucket"], r.get("verdict"),
                            r.get("direction"), r["file"], r["row"])
        assert r["disposition"] == d, (
            f"{r['file']} row {r['row']}: disposition {r['disposition']} != rule {d}")
        assert r["adjudication"] == ADJUDICATION[d]
        assert r["decision"] == "", "decision must be an empty placeholder"
        assert isinstance(r["needs_vision"], bool)

        if r.get("pems_columns") is None:
            assert r.get("pems_columns_null_reason"), (
                f"{r['file']} row {r['row']}: null pems_columns with no reason")
            assert r.get("pems_page") is None, (
                f"{r['file']} row {r['row']}: null pems_columns but a pems_page")
            continue

        # the join key must exist and the columns must be that row's columns
        key = (r["pems_page"], r["pems_ordinal"])
        assert key in pems_idx, f"{r['file']} row {r['row']}: missing PEMS key {key}"
        pems = pems_idx[key]
        for L in LV:
            assert r["pems_columns"][L] == (pems["columns"].get(L) or ""), (
                f"{r['file']} row {r['row']}: pems_columns[{L}] not from pems_table")
        assert r["badge_tokens"] == list(pems.get("badge_tokens") or [])

        # site cells re-parsed from the page, not trusted from the artifact
        if r["row"] is not None:
            cells, _ = site_cells_for(r["file"], r["row"])
            assert cells == r["site_cells"], (
                f"{r['file']} row {r['row']}: site_cells not reproducible")

        # verdict / direction recomputed from the join
        if r["reason_kind"] == "multiple_candidates":
            cands = r["pems_candidates"]
            assert len(cands) >= 2
            for cd in cands:
                v, dirn, _ = compare(cd["pems_columns"], r["site_cells"])
                assert v == cd["verdict"], (
                    f"{r['file']} row {r['row']}: candidate verdict not reproducible")
                assert cd.get("direction") == dirn
            v, dirn = aggregate_verdict([(cd["verdict"], cd.get("direction"))
                                         for cd in cands])
            assert r["verdict"] == v, (
                f"{r['file']} row {r['row']}: aggregate verdict {r['verdict']} != {v}")
            assert r.get("direction") == dirn
        elif "verdict" in r:
            v, dirn, _ = compare(r["pems_columns"], r["site_cells"])
            assert v == r["verdict"], (
                f"{r['file']} row {r['row']}: verdict not reproducible")
            if v == "disagrees":
                assert r.get("direction") == dirn, (
                    f"{r['file']} row {r['row']}: direction mismatch")
                assert dirn in ("site_broader", "site_narrower", "site_gap")
            else:
                assert "direction" not in r

        # needs_vision recomputed from the badge itself
        if r["reason_kind"] == "multiple_candidates":
            flags = []
            for cd in r["pems_candidates"]:
                k = (cd["pems_page"], cd["pems_ordinal"])
                nv, nv_reason = badge_ambiguity(pems_idx[k])
                assert cd["needs_vision"] == nv, (
                    f"{r['file']} row {r['row']}: candidate {k} needs_vision "
                    f"not reproducible")
                flags.append(nv)
                if nv:
                    assert cd.get("needs_vision_reason") == nv_reason
            assert r["needs_vision"] == any(flags), (
                f"{r['file']} row {r['row']}: needs_vision not reproducible "
                f"from its candidates")
        else:
            nv, nv_reason = badge_ambiguity(pems)
            assert r["needs_vision"] == nv, (
                f"{r['file']} row {r['row']}: needs_vision not reproducible")
            if nv:
                assert r["needs_vision_reason"] == nv_reason
        if r["needs_vision"]:
            assert r["needs_vision_reason"], (
                f"{r['file']} row {r['row']}: needs_vision with no reason")

    # 5. held rows: the split is the join, and the site_gap row is the ADD
    held = [r for r in rows if r["source_bucket"].startswith("held_")]
    assert len(held) == len(HELD), f"held {len(held)} != {len(HELD)}"
    for r in held:
        assert r["verdict"] == ("agrees" if r["source_bucket"] == "held_agrees"
                                else "disagrees")
    gap = [r for r in held if r.get("direction") == "site_gap"]
    assert len(gap) == 1 and (gap[0]["file"], gap[0]["row"]) == SITE_GAP_ADD
    assert gap[0]["disposition"] == "site_gap_add"
    assert c["c3_apply_excluded"] == [{"file": r["file"], "row": r["row"]}
                                      for r in rows
                                      if r["disposition"] == "held_level_correct"]
    assert len(c["c3_apply_excluded"]) == EXPECTED_DISPOSITIONS["held_level_correct"]
    assert c["needs_vision_count"] == len([r for r in rows if r["needs_vision"]])

    # 6. core rows: every one of the md's 42 is here
    core = [r for r in rows if r["source_bucket"] == "core_ambiguous"]
    assert len(core) == src["core_ambiguous_from_md"]
    for r in core:
        a = align_idx[(r["file"], r["row"])]
        assert a["reason_kind"] in CORE_KINDS
        assert r["reason_kind"] == a["reason_kind"]
        assert r["detail"] == a["reason"], (
            f"{r['file']} row {r['row']}: detail is not the md's why line")

    # 7. provisional flags, at-risk matched rows, adjudicator notes ---------
    # A provisional verdict is one whose direction inverts if an unresolved
    # badge settles the other way (Non_Traumatic r4 reads site_broader today and
    # site_narrower under EMR). It is derived from the table, never hand-set.
    import recheck_ambiguous_badges as RC  # lazy: RC imports this module
    resolved_keys = set(RC.load_overrides())
    unresolved = {k for k, p in pems_idx.items()
                  if k not in resolved_keys and badge_ambiguity(p)[0]}
    expect_flags = [(r["file"], r["row"]) for r in rows
                    if any(k in unresolved for k in pems_keys_of(r, align_idx))]
    flagged = [(r["file"], r["row"]) for r in rows if r.get("provisional")]
    assert flagged == expect_flags, (
        f"provisional flags {flagged} != rows joined to an unresolved badge {expect_flags}")
    assert c["provisional_count"] == len(flagged)
    assert [(p["file"], p["row"]) for p in c["provisional"]] == flagged
    for r in rows:
        assert ("provisional" in r) == ("provisional_reason" in r), (
            f"{r['file']} row {r['row']}: provisional without a reason")
        if r.get("provisional"):
            assert r["provisional_reason"].startswith("depends on unresolved badge")
    if (63, 7) in unresolved:
        assert ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 4) in flagged, (
            "the single site_broader row must be provisional — its direction rests on "
            "the unresolved p.63#7 badge")
    else:
        assert ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 4) not in flagged, (
            "p.63#7 is resolved; the row must not still be flagged provisional")

    # the at-risk list is the recheck script's own output, not a hand list
    ar = RC.at_risk_rows(exclude={(r["file"], r["row"]) for r in rows})
    assert c["at_risk_matched_rows"] == ar, "counts.at_risk_matched_rows != recheck output"
    assert c["at_risk_matched_rows_count"] == len(ar)
    ar_keys = {(os.path.basename(a["file"]), a["row"]) for a in ar}
    for named, pkey in ((("04_Cardiac_Arrest_Non_Traumatic_PROC.md", 5), (63, 7)),
                        (("04_Cardiac_Arrest_Traumatic_PROC.md", 5), (61, 4))):
        if pkey in unresolved:
            assert named in ar_keys, f"{named} is mapped to an ambiguous badge but not at risk"
        else:
            assert named not in ar_keys, (
                f"{named}: its badge is resolved, so it is a settled flip, not at risk")
    for a in ar:
        assert a["old_verdict"] == "matched", (
            f"{a['file']} row {a['row']}: at-risk rows must be currently matched")
        assert a["flips_if_badge"], f"{a['file']} row {a['row']}: at risk but never flips"

    notes = doc.get("notes_for_adjudicator") or []
    assert notes, "notes_for_adjudicator is missing"
    assert any('one row or two' in n for n in notes), (
        "notes_for_adjudicator must carry the 'one row or two' test")
    assert any("authoring decision, not a level fix" in n for n in notes)


if __name__ == "__main__":
    main()
