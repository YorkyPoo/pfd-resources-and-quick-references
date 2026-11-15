#!/usr/bin/env python3
"""Build audit/level-scan/c2-scope.json — the C2 adjudication queue.

WHY THIS SCRIPT EXISTS
----------------------
The C2 scope has been asserted three times by hand and been wrong three times.
The last one ("42 + 1 + 4 + 5 = 52") double-counted Trauma row 7 and
contradicted its own prose two lines later. So the total is never written by
hand again: it is `len(rows)`, computed here, deduped by (file, row).

SOURCES (each row carries `source_bucket` so the split is auditable)
--------------------------------------------------------------------
held_agrees       best_evidence_is_held rows whose published level already
                  contains the PEMS badge -> NOT sent to vision. Cleared by
                  rule; a needs-authoring entry records that site-split vs
                  PEMS-merge is an authoring decision, not a level defect.
held_disagrees    best_evidence_is_held rows whose published level contradicts
                  the PEMS badge -> raster adjudication.
core_ambiguous    the core (11 multiple_candidates + 31 shared_pems_row),
                  read live from ambiguous-rows.md at run time.
extra_named       the named extras still requiring a human.

FAIL-CLOSED RULE
----------------
A held row whose published level is not affirmatively known to contain the
PEMS badge goes to `held_disagrees` (raster), never to `held_agrees`. Silence
is not agreement.

EXCLUDED
--------
06_Overdose_Poisoning row 5 — text-binding settled it (site A+ vs PEMS EMT).
It belongs on the fix list, not in the queue. See text-binding.md.

Run: python3 scripts/build_c2_scope.py [--write] [--verify]
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "audit", "level-scan", "c2-scope.json")
AMBIG = os.path.join(REPO, "audit", "level-scan", "ambiguous-rows.md")

LV = ["EMR", "EMT", "A", "I", "P"]

HELD = [
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 4,  63,  7,  "I",   ["EMT","A","I","P"]),
    ("protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md",     6,  61,  5,  "A",   ["I","P"]),
    ("protocols/cardiac/04_Chest_Pain_ACS_PROC.md",              13,  107, 9,  "MC",  None),
    ("protocols/cardiac/04_Chest_Pain_ACS_PROC.md",               5,  107, 4,  "EMT", None),
    ("protocols/neurologic/05_Stroke_TIA_PROC.md",                6,  131, 4,  "EMT", None),
    ("protocols/neurologic/05_Stroke_TIA_PROC.md",                7,  131, 4,  "EMT", ["A","I","P"]),
    ("protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md", 3, 153, 2, "EMT", None),
    ("protocols/respiratory/03_Pneumothorax_PROC.md",            11,  243, 4,  "I",   None),
    ("protocols/respiratory/03_Respiratory_Arrest_PROC.md",      11,  239, 2,  "EMR", None),
    ("protocols/respiratory/03_Respiratory_Distress_PROC.md",    10,  124, 10, "A",   None),
    ("protocols/respiratory/03_Respiratory_Distress_PROC.md",     8,  123, 1,  "EMR", None),
    ("protocols/respiratory/03_Smoke_Inhalation_PROC.md",        11,  153, 2,  "EMT", None),
    ("protocols/respiratory/03_Smoke_Inhalation_PROC.md",         4,  153, 2,  "EMT", None),
    ("protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md", 3,  239, 3,  "EMT", None),
    ("protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md", 8,  239, 6,  "EMT", None),
    ("protocols/trauma/09_Trauma_PROC.md",                        7,  83,  10, "A",   ["I","P"]),
]

KNOWN_DISAGREE = {
    ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 4),
    ("protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md", 6),
    ("protocols/neurologic/05_Stroke_TIA_PROC.md", 7),
    ("protocols/respiratory/03_Respiratory_Distress_PROC.md", 10),
    ("protocols/trauma/09_Trauma_PROC.md", 7),
}

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


def grants(published, badge):
    if not published:
        return False
    if badge == "MC":
        return False
    if badge not in LV or badge not in published:
        return False
    low = min(LV.index(x) for x in published)
    return LV.index(badge) >= low


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

    def add(f, r, bucket, reason_kind, detail, adjudication):
        key = (f, r)
        if key in seen:
            return
        seen.add(key)
        rows.append({"file": f, "row": r, "source_bucket": bucket,
                     "reason_kind": reason_kind, "detail": detail,
                     "adjudication": adjudication})

    for f, r, page, ordn, badge, published in HELD:
        agrees = grants(published, badge) and (f, r) not in KNOWN_DISAGREE
        if agrees:
            add(f, r, "held_agrees", "shared_pems_row",
                f"published {'/'.join(published)} contains PEMS p.{page}/#{ordn} {badge}",
                "rule_clear")
        else:
            why = ("known disagreement" if (f, r) in KNOWN_DISAGREE
                   else f"published {'/'.join(published) if published else 'unknown'} "
                        f"does not contain PEMS p.{page}/#{ordn} {badge}; fail closed")
            add(f, r, "held_disagrees", "shared_pems_row", why, "raster")

    for f, r, why in EXTRA_NAMED:
        add(f, r, "extra_named", "named_item", why, "raster")

    core, kinds = read_core()
    doc = {
        "note": ("C2 queue. Total is len(rows) + core; nothing here is a hand "
                 "sum. Dedupe is by (file, row). Core ambiguous rows are not "
                 "enumerated individually because ambiguous-rows.md moves; "
                 "they are counted live from that file."),
        "counts": {
            "rows_listed_here": len(rows),
            "held_total": sum(1 for x in rows if x["source_bucket"].startswith("held_")),
            "held_agrees_rule_cleared": sum(1 for x in rows if x["source_bucket"] == "held_agrees"),
            "held_disagrees_raster": sum(1 for x in rows if x["source_bucket"] == "held_disagrees"),
            "extra_named": sum(1 for x in rows if x["source_bucket"] == "extra_named"),
            "core_ambiguous": core,
            "core_ambiguous_by_kind": kinds,
            "derived_total": (len(rows) + core) if core is not None else None,
        },
        "excluded": [{"file": f, "row": r, "why": w} for f, r, w in EXCLUDED],
        "rows": rows,
    }
    return doc


def main():
    doc = build()
    c = doc["counts"]
    print(json.dumps(c, indent=2))
    print()
    print("rows listed here      :", c["rows_listed_here"])
    print("core ambiguous (live) :", c["core_ambiguous"])
    print("DERIVED C2 TOTAL      :", c["derived_total"])
    print("  rule-cleared, no vision:", c["held_agrees_rule_cleared"])
    print("  raster adjudication    :",
          (c["derived_total"] or 0) - c["held_agrees_rule_cleared"])

    if "--verify" in sys.argv:
        keys = [(r["file"], r["row"]) for r in doc["rows"]]
        assert len(keys) == len(set(keys)), "duplicate (file,row) in queue"
        assert c["held_total"] == len(HELD), f"held total {c['held_total']} != {len(HELD)}"
        assert c["held_agrees_rule_cleared"] + c["held_disagrees_raster"] == c["held_total"]
        assert c["derived_total"] == c["rows_listed_here"] + c["core_ambiguous"]
        print("\nverify: OK")

    if "--write" in sys.argv:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1)
        print("\nwrote", OUT)


if __name__ == "__main__":
    main()
