#!/usr/bin/env python3
"""Build audit/level-scan/c2-scope.json — the C2 adjudication queue.

WHY THIS SCRIPT EXISTS
----------------------
The C2 scope has been asserted by hand and been wrong. The total is never
written by hand: it is `len(rows) + core_ambiguous`, computed here, deduped by
(file, row).

THE HELD-ROW SPLIT IS A JOIN, NOT A GUESS
-----------------------------------------
An earlier revision carried a hand list (`KNOWN_DISAGREE`) of rows believed to
contradict PEMS, plus a hand `published` level per row. The two mechanisms
contradicted each other: the hand list vetoed the rule even when the rule said
the badge was contained, so every held row went to vision — inverting the
operator's instruction not to spend vision on rows whose level is already
correct.

That is gone. For each held row this script now:

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

Every held row in the artifact carries pems_page, pems_ordinal, pems_columns,
site_cells, badge_tokens, verdict and (when disagreeing) direction, so the
split is reproducible from the artifact alone.

SOURCES
-------
held_*            the 16 best_evidence_is_held rows, split by the join above.
core_ambiguous    the core (multiple_candidates + shared_pems_row), read live
                  from ambiguous-rows.md at run time.
extra_named       the named extras still requiring a human.

EXCLUDED
--------
06_Overdose_Poisoning row 5 — text-binding settled it (site A+ vs PEMS EMT).
It belongs on the fix list, not in the queue. See text-binding.md.

Run: python3 scripts/build_c2_scope.py [--write] [--verify]
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import pems_level_scan as PLS  # noqa: E402  (read_page / cells are the parser of record)

OUT = os.path.join(REPO, "audit", "level-scan", "c2-scope.json")
AMBIG = os.path.join(REPO, "audit", "level-scan", "ambiguous-rows.md")
TABLE = os.path.join(REPO, "audit", "level-scan", "pems_table.json")
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

EXTRA_NAMED = [
    ("protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md", 5,
     "PEMS p.63 badge I but the line says 'AED is advising to shock [EMR]' inline"),
    ("protocols/respiratory/03_Respiratory_Distress_PROC.md", None,
     "PEMS p.125 pearl tail truncated in every text extraction"),
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", None,
     "amiodarone 300 mg vs 150 mg row pairing (C1 false-confidence case)"),
]

EXCLUDED = [
    ("protocols/toxicology/06_Overdose_Poisoning_PROC.md", 5,
     "text-binding settled: site A+ vs PEMS EMT -> fix list, not queue"),
]


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
    five level cells. Missing or duplicated row numbers are hard errors."""
    path = os.path.join(DOCS, rel)
    page = PLS.read_page(path)
    if not page.get("has_table"):
        raise SystemExit(f"{rel}: no EMR|EMT|A|I|P table")
    hits = [r for r in page["rows"] if r["num"].strip() == str(row_num)]
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


def read_core():
    if not os.path.exists(AMBIG):
        return None, None
    txt = open(AMBIG, encoding="utf-8").read()
    m = re.search(r"multiple_candidates (\d+), no_counterpart (\d+), shared_pems_row (\d+)", txt)
    if not m:
        return None, None
    mc, _, shared = (int(x) for x in m.groups())
    return mc + shared, {"multiple_candidates": mc, "shared_pems_row": shared}


def build():
    rows, seen = [], set()
    pems_idx = load_pems_index()

    def add(f, r, bucket, reason_kind, detail, adjudication, **extra):
        key = (f, r)
        if key in seen:
            return
        seen.add(key)
        rec = {"file": f, "row": r, "source_bucket": bucket,
               "reason_kind": reason_kind, "detail": detail,
               "adjudication": adjudication}
        rec.update(extra)
        rows.append(rec)

    for f, r, page, ordn in HELD:
        key = (page, ordn)
        if key not in pems_idx:
            raise SystemExit(f"join failed: PEMS key {key} for {f} row {r} "
                             f"is not in pems_table.json")
        pems = pems_idx[key]
        pems_columns = {L: (pems["columns"].get(L) or "") for L in LV}
        badge_tokens = list(pems.get("badge_tokens") or [])
        cells, action = site_cells_for(f, r)
        verdict, direction, why = compare(pems_columns, cells)

        rec_extra = {
            "pems_page": page,
            "pems_ordinal": ordn,
            "pems_columns": pems_columns,
            "site_cells": cells,
            "badge_tokens": badge_tokens,
            "verdict": verdict,
            "site_action": action[:160],
        }
        if verdict == "agrees":
            add(f, r, "held_agrees", "shared_pems_row", why, "rule_clear", **rec_extra)
        else:
            rec_extra["direction"] = direction
            add(f, r, "held_disagrees", "shared_pems_row", why, "raster", **rec_extra)

    for f, r, why in EXTRA_NAMED:
        add(f, r, "extra_named", "named_item", why, "raster")

    core, kinds = read_core()
    held = [x for x in rows if x["source_bucket"].startswith("held_")]
    agrees = [x for x in held if x["verdict"] == "agrees"]
    disagrees = [x for x in held if x["verdict"] == "disagrees"]
    hist = {}
    for x in disagrees:
        hist[x["direction"]] = hist.get(x["direction"], 0) + 1

    derived_total = (len(rows) + core) if core is not None else None
    doc = {
        "note": ("C2 queue. Total is len(rows) + core; nothing here is a hand "
                 "sum. Dedupe is by (file, row). The held-row split is a join "
                 "against pems_table.json by (pems_page, pems_ordinal) — no "
                 "hand verdicts, no hand published levels. Core ambiguous rows "
                 "are counted live from ambiguous-rows.md."),
        "counts": {
            "rows_listed_here": len(rows),
            "held_total": len(held),
            "held_agrees_rule_cleared": len(agrees),
            "held_disagrees_raster": len(disagrees),
            "held_direction_histogram": hist,
            "site_broader": [{"file": x["file"], "row": x["row"],
                              "pems_columns": x["pems_columns"],
                              "site_cells": x["site_cells"]}
                             for x in disagrees if x["direction"] == "site_broader"],
            "extra_named": sum(1 for x in rows if x["source_bucket"] == "extra_named"),
            "core_ambiguous": core,
            "core_ambiguous_by_kind": kinds,
            "derived_total": derived_total,
            "rule_cleared": len(agrees),
            "needs_adjudication": (derived_total - len(agrees)) if derived_total is not None else None,
        },
        "excluded": [{"file": f, "row": r, "why": w} for f, r, w in EXCLUDED],
        "rows": rows,
    }
    return doc


def main():
    doc = build()
    c = doc["counts"]
    print(json.dumps({k: v for k, v in c.items() if k != "site_broader"}, indent=2))
    print()
    print("rows listed here      :", c["rows_listed_here"])
    print("core ambiguous (live) :", c["core_ambiguous"])
    print("DERIVED C2 TOTAL      :", c["derived_total"])
    print("  rule-cleared, no vision:", c["rule_cleared"])
    print("  needs adjudication     :", c["needs_adjudication"])
    print("  direction histogram    :", c["held_direction_histogram"])
    print("  site_broader (liability):", len(c["site_broader"]))

    if "--table" in sys.argv:
        print("\n| file | row | PEMS p/# | PEMS cols (EMR/EMT/A/I/P) | site cells | verdict | direction |")
        print("|---|---|---|---|---|---|---|")
        for r in doc["rows"]:
            if not r["source_bucket"].startswith("held_"):
                continue
            pc = "/".join(r["pems_columns"][L] or "·" for L in LV)
            sc = "/".join(c or "·" for c in r["site_cells"])
            print(f"| {os.path.basename(r['file'])} | {r['row']} | "
                  f"{r['pems_page']}/{r['pems_ordinal']} | {pc} | {sc} | "
                  f"{r['verdict']} | {r.get('direction') or ''} |")

    if "--verify" in sys.argv:
        keys = [(r["file"], r["row"]) for r in doc["rows"]]
        assert len(keys) == len(set(keys)), "duplicate (file,row) in queue"
        assert c["held_total"] == len(HELD), f"held total {c['held_total']} != {len(HELD)}"
        assert c["held_agrees_rule_cleared"] + c["held_disagrees_raster"] == c["held_total"]
        assert c["derived_total"] == c["rows_listed_here"] + c["core_ambiguous"]
        assert c["rule_cleared"] + c["needs_adjudication"] == c["derived_total"]
        # every held row's verdict must be reproducible from the artifact alone
        for r in doc["rows"]:
            if not r["source_bucket"].startswith("held_"):
                continue
            for fld in ("pems_page", "pems_ordinal", "pems_columns", "site_cells",
                        "badge_tokens", "verdict"):
                assert fld in r, f"{r['file']} row {r['row']} missing {fld}"
            v, d, _ = compare(r["pems_columns"], r["site_cells"])
            assert v == r["verdict"], f"{r['file']} row {r['row']}: verdict not reproducible"
            if r["verdict"] == "disagrees":
                assert r.get("direction") == d, f"{r['file']} row {r['row']}: direction mismatch"
                assert d in ("site_broader", "site_narrower", "site_gap")
            else:
                assert "direction" not in r
        # the join key must exist for all 16
        idx = load_pems_index()
        for f, r, page, ordn in HELD:
            assert (page, ordn) in idx, f"missing PEMS key {(page, ordn)}"
        print("\nverify: OK")

    if "--write" in sys.argv:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1)
        print("\nwrote", OUT)


if __name__ == "__main__":
    main()
