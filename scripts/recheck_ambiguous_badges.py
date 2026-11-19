#!/usr/bin/env python3
"""Re-check every site row the alignment maps to a badge-contradiction PEMS row.

WHY THIS EXISTS
---------------
Only 2 of the 535 PEMS rows print an inline level token that contradicts their
own badge:

    p.61 #4  badge EMT, line prints "(I / P)"
    p.63 #7  badge I,   line prints "[EMR]"

Three site rows map to those two PEMS rows (`04_Cardiac_Arrest_Traumatic` r5,
`04_Cardiac_Arrest_Non_Traumatic` r5, `04_V_Fib_Pulseless_V_Tach` r5). Only one
of them is in the C2 queue; the other two carry `matched` and are flagged
nowhere. A raster that settles p.63 #7 = `EMR` would make the site row that
grants EMT/A/I/P narrower than PEMS — a defect that currently has no card and
no line in any report.

So this script re-runs the join over EVERY site row linked to those PEMS rows,
not just queue members, and reports:

    at_risk   rows currently `matched` and absent from c2-scope.json whose
              verdict flips to a defect under one of the admissible badge
              resolutions for their PEMS row
    flips     rows that DO flip once an override in badge-overrides.yaml is
              applied (definitive: the human settled the badge)
    in_queue  linked rows already enumerated by c2-scope.json (reported, not
              re-queued)

The PEMS level set for a resolution comes from the badge itself
(`pems_canonical._columns`), never from the contradictory printed columns: the
printed columns are the thing the resolution is correcting.

    python3 scripts/recheck_ambiguous_badges.py            # human report
    python3 scripts/recheck_ambiguous_badges.py --json     # machine payload
    python3 scripts/recheck_ambiguous_badges.py --write    # audit/level-scan/badge-recheck.json
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

import yaml  # noqa: E402
import build_c2_scope as B  # noqa: E402  (same join: compare/site_cells_for/LV)
import pems_canonical as C  # noqa: E402  (badge -> columns)

OUT = os.path.join(REPO, "audit", "level-scan")
TABLE = os.path.join(OUT, "pems_table.json")
ALIGN = os.path.join(OUT, "alignment.json")
SCOPE = os.path.join(OUT, "c2-scope.json")
OVERRIDES = os.path.join(OUT, "badge-overrides.yaml")
REPORT = os.path.join(OUT, "badge-recheck.json")

LV = B.LV
# The two rows the operator named. Kept explicit so the re-check still covers
# them when badge-overrides.yaml is empty (which it is until rasters land).
NAMED_PEMS_ROWS = [(61, 4), (63, 7)]
LEVEL_TOKEN = re.compile(r"\[\s*(EMR|EMT|A|I|P)\s*\]")
LEVEL_PAIR = re.compile(r"\(\s*(EMR|EMT|A|I|P)(?:\s*/\s*(EMR|EMT|A|I|P))+\s*\)")
LEVEL_ONLY = re.compile(r"\b((?:EMR|EMT|A|I|P)(?:\s*/\s*(?:EMR|EMT|A|I|P))+)\s+only\b")


def load_overrides() -> dict:
    """{(page, ordinal): entry} from badge-overrides.yaml (empty file -> {})."""
    if not os.path.exists(OVERRIDES):
        return {}
    doc = yaml.safe_load(open(OVERRIDES, encoding="utf-8")) or {}
    out = {}
    for ent in doc.get("overrides") or []:
        out[(int(ent["page"]), int(ent["ordinal"]))] = ent
    return out


def load_table():
    doc = json.load(open(TABLE, encoding="utf-8"))
    idx = {}
    for d in doc["pems_docs"]:
        for r in d["rows"]:
            idx[(r["page"], r["ordinal"])] = r
    return doc, idx


def watch_keys(pems_idx) -> list:
    """PEMS rows to re-check: the named two plus everything in the override file."""
    keys = []
    for k in NAMED_PEMS_ROWS:
        if k not in pems_idx:
            raise SystemExit(f"pems_table.json has no row p.{k[0]} #{k[1]}")
        keys.append(k)
    for k in load_overrides():
        if k not in pems_idx:
            raise SystemExit(f"badge-overrides.yaml names p.{k[0]} #{k[1]}, "
                             "which is not in pems_table.json")
        if k not in keys:
            keys.append(k)
    return keys


def inline_markers(text: str) -> list[tuple[str, list[str]]]:
    """Level tokens printed inside a PEMS row's text, with the levels each names."""
    out = []
    for m in LEVEL_TOKEN.finditer(text or ""):
        out.append((m.group(0), [m.group(1)]))
    for m in LEVEL_PAIR.finditer(text or ""):
        out.append((m.group(0), [x for x in m.group(1).split("/") if x]))
    for m in LEVEL_ONLY.finditer(text or ""):
        out.append((m.group(0), [x.strip() for x in m.group(1).split("/") if x.strip()]))
    return out


def resolutions_for(key, pems_row, overrides) -> tuple[list[str], str]:
    """The badge values this row can settle to, and why.

    An applied override is definitive: exactly one resolution. Otherwise the
    PDF badge and every inline marker are admissible, because that is precisely
    what the raster is meant to arbitrate.
    """
    ov = overrides.get(key)
    if ov:
        return [str(ov["resolved"]).strip().strip("[]").upper()], "override"
    badge = str((pems_row.get("badge_tokens") or [""])[0]).strip().strip("[]").upper()
    levels = []
    if badge:
        levels.append(badge)
    for _raw, lv in inline_markers(pems_row.get("verbatim_text")):
        for L in lv:
            if L not in levels:
                levels.append(L)
    return levels, "unresolved"


def linked_rows(align_doc, keys) -> list[dict]:
    """Every site row the alignment links to one of `keys`.

    Link shapes: a `matched` row's own (pems_page, pems_ordinal), a
    `shared_pems_row`'s `contained_in_pems`, a `multiple_candidates` row's
    `pems_candidates`, and a text-binding verdict's named PEMS row.
    """
    out = []
    keyset = set(keys)
    for page in align_doc["pages"]:
        rel = page["site_page"]
        for r in page["rows"]:
            refs = []

            def add(pp, oo, basis):
                if pp is None or oo is None:
                    return
                k = (int(pp), int(oo))
                if k in keyset:
                    refs.append((k, basis))

            if r.get("status") == "matched":
                add(r.get("pems_page"), r.get("pems_ordinal"), "matched")
            ci = r.get("contained_in_pems")
            if ci:
                add(ci.get("pems_page"), ci.get("pems_ordinal"), "shared_pems_row")
            for cand in r.get("pems_candidates") or []:
                add(cand.get("pems_page"), cand.get("pems_ordinal"), "candidate")
            tb = r.get("text_binding")
            if tb:
                add(tb.get("pems_page"), tb.get("pems_ordinal"), "text_binding")
            # `multiple_candidates` rows name their candidates in the aligner's
            # reason string (c2-scope derives them from there), not as fields
            for pp, oo in re.findall(r"p\.(\d+) row (\d+)", r.get("reason") or ""):
                add(pp, oo, "named_in_reason")
            for k, basis in refs:
                out.append({"file": rel, "row": int(r["site_row"]), "pems": k,
                            "basis": basis, "status": r.get("status"),
                            "reason_kind": r.get("reason_kind"),
                            "old_verdict": ("matched" if r.get("status") == "matched"
                                            else f"{r.get('status')}:{r.get('reason_kind')}")})
    return out


def queue_keys() -> set:
    if not os.path.exists(SCOPE):
        return set()
    doc = json.load(open(SCOPE, encoding="utf-8"))
    return {(r["file"], r["row"]) for r in doc.get("rows") or []}


def recheck(exclude=None) -> dict:
    _table, pems_idx = load_table()
    align = json.load(open(ALIGN, encoding="utf-8"))
    overrides = load_overrides()
    keys = watch_keys(pems_idx)
    in_queue = queue_keys() | set(exclude or ())

    rows = linked_rows(align, keys)
    # one entry per (site row, watched PEMS row)
    seen = set()
    at_risk, flips, queued = [], [], []
    for ent in rows:
        k = (ent["file"], ent["row"], ent["pems"])
        if k in seen:
            continue
        seen.add(k)
        pems_row = pems_idx[ent["pems"]]
        try:
            cells, _action = B.site_cells_for(ent["file"], ent["row"])
        except SystemExit as exc:  # a row that vanished is reported, not crashed on
            ent["error"] = str(exc)
            continue
        levels, basis = resolutions_for(ent["pems"], pems_row, overrides)
        outcomes = []
        for badge in levels:
            cols = C._columns([badge])
            verdict, direction, detail = B.compare(cols, cells)
            outcomes.append({"resolved_badge": badge, "verdict": verdict,
                             "direction": direction, "detail": detail})
        ent = {**ent,
               "resolution_basis": basis,
               "site_cells": cells,
               "pdf_badge": ((pems_row.get("badge_token_from_pdf")
                              or pems_row.get("badge_tokens") or [None])[0]),
               "outcomes": outcomes}
        ent["flips"] = [o for o in outcomes if o["verdict"] == "disagrees"]
        if basis == "override":
            if ent["flips"]:
                flips.append(ent)
            elif ent["old_verdict"] == "matched":
                pass  # settled and still agrees: no longer at risk
        elif (ent["file"], ent["row"]) in in_queue:
            queued.append(ent)
        elif ent["old_verdict"] == "matched" and ent["flips"]:
            at_risk.append(ent)
    return {
        "generated": _dt.datetime.now().isoformat(timespec="seconds"),
        "watched_pems_rows": [{"page": p, "ordinal": o} for p, o in keys],
        "named_pems_rows": [{"page": p, "ordinal": o} for p, o in NAMED_PEMS_ROWS],
        "overrides": [{"page": k[0], "ordinal": k[1], "resolved": v.get("resolved")}
                      for k, v in sorted(overrides.items())],
        "counts": {"linked_rows": len({(e["file"], e["row"]) for e in rows}),
                   "at_risk": len(at_risk), "flips": len(flips),
                   "in_queue": len({(e["file"], e["row"]) for e in queued})},
        "at_risk": at_risk,
        "flips": flips,
        "in_queue": queued,
    }


def at_risk_rows(exclude=None) -> list[dict]:
    """Compact at_risk list for c2-scope.json (`counts.at_risk_matched_rows`)."""
    return [{"file": e["file"], "row": e["row"],
             "old_verdict": e["old_verdict"],
             "pems_page": e["pems"][0], "pems_ordinal": e["pems"][1],
             "pdf_badge": e["pdf_badge"],
             "flips_if_badge": sorted({o["resolved_badge"] for o in e["flips"]}),
             "directions": sorted({o["direction"] for o in e["flips"]})}
            for e in recheck(exclude=exclude)["at_risk"]]


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    doc = recheck()
    if "--write" in argv:
        with open(REPORT, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1)
        print("wrote", os.path.relpath(REPORT, REPO))
    if "--json" in argv:
        print(json.dumps(doc, indent=1))
        return 0
    print("re-check of site rows mapped to ambiguous PEMS badges")
    print("  watched PEMS rows :", ", ".join(f"p.{r['page']} #{r['ordinal']}"
                                             for r in doc["watched_pems_rows"]))
    print("  overrides applied :", doc["overrides"] or "none (rasters not run)")
    print("  linked site rows  :", doc["counts"]["linked_rows"],
          f"(at_risk {doc['counts']['at_risk']}, in_queue {doc['counts']['in_queue']}, "
          f"flips {doc['counts']['flips']})")
    print()
    print("AT_RISK — matched, not in c2-scope.json, flips under an admissible badge")
    if not doc["at_risk"]:
        print("  none")
    for e in doc["at_risk"]:
        print(f"  - {os.path.basename(e['file'])} r{e['row']} "
              f"(PEMS p.{e['pems'][0]} #{e['pems'][1]}, {e['resolution_basis']}) "
              f"{e['old_verdict']} -> " + "; ".join(
                  f"{o['resolved_badge']}: {o['verdict']}/{o['direction'] or ''}"
                  for o in e["flips"]))
        print(f"      site cells {'/'.join(c or '·' for c in e['site_cells'])}")
    print()
    print("IN_QUEUE — linked rows c2-scope.json already enumerates")
    for e in doc["in_queue"]:
        print(f"  - {os.path.basename(e['file'])} r{e['row']} "
              f"(PEMS p.{e['pems'][0]} #{e['pems'][1]}, {e['basis']}) "
              f"{e['old_verdict']}")
    print()
    print("FLIPS — settled by an override, now a defect")
    if not doc["flips"]:
        print("  none")
    for e in doc["flips"]:
        print(f"  - {os.path.basename(e['file'])} r{e['row']} "
              f"matched -> {e['flips'][0]['verdict']}/{e['flips'][0]['direction']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())