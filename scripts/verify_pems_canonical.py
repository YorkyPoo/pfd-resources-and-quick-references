#!/usr/bin/env python3
"""Invariant checks for the level-scan rebuild artifacts (stages 1+2).

Run after `pems_canonical.py --stage all`. Exits non-zero and prints the failed
invariant when something does not add up. This exists because the previous
pipeline's report was believed without checking: "0 fixable mismatches" was true
by its own definition while 154 rows were wrong.

    python scripts/verify_pems_canonical.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "audit", "level-scan")
sys.path.insert(0, os.path.join(REPO, "scripts"))
import pems_canonical as C  # noqa: E402  (for the human-review table)
fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


def main() -> int:
    table = json.load(open(os.path.join(OUT, "pems_table.json"), encoding="utf-8"))
    align = json.load(open(os.path.join(OUT, "alignment.json"), encoding="utf-8"))

    print("stage 1 — canonical PEMS table")
    dec = table["page_decisions"]
    check(len(dec) == 57, f"57 site pages carry a decision (found {len(dec)})")
    check(len({d["site_page"] for d in dec}) == 57, "every decision is a distinct page")
    check(all(d.get("decision") in ("level_gated", "administrative", "skipped") for d in dec),
          "every decision is level_gated / administrative / skipped")
    check(all(d.get("reason") or d.get("ruling") or d.get("source_declared") for d in dec),
          "every decision carries a reason, ruling or declared source")
    admins = [d for d in dec if d["decision"] == "administrative"]
    check(all(d.get("ruling_status") == "contested" for d in admins),
          f"all {len(admins)} administrative pages record the ruling as contested")
    check(all("level_grid_present" in d for d in admins),
          "all administrative pages report whether the page still carries a level grid")
    check(all(d.get("decision") != "skipped" or d.get("reason") for d in dec),
          "no skipped page without a stated reason")

    rows = [r for d in table["pems_docs"] for r in d["rows"]]
    need = {"page", "section_heading", "ordinal", "section_ordinal", "verbatim_text",
            "x", "y", "badge_tokens", "columns"}
    check(bool(rows) and all(need <= set(r) for r in rows),
          f"every PEMS row carries the required fields ({len(rows)} rows)")
    check(all(r["badge_tokens"] for r in rows), "every PEMS row carries a badge token")
    check(all(r["verbatim_text"] for r in rows), "every PEMS row has verbatim text")
    # A badge word may legitimately appear INSIDE an instruction ("...shock [EMR],
    # immediately defibrillate"); what must never happen is the margin column
    # being rendered at the start or end of the row text.
    # Known-good exceptions: p.7 is the level key ("EMR Emergency Medical
    # Responder EMT ...") and p.52 carries the AEIOU mnemonic ("I Infection"),
    # both of which legitimately begin a row with a level word.
    LEGEND = {7, 52}
    leaks = [r for r in rows
             if r["page"] not in LEGEND
             and ((r["verbatim_text"].split() and r["verbatim_text"].split()[0]
                   in ("EMR", "EMT", "MC", "A", "I", "P"))
                  or r["verbatim_text"].split()[-1] in ("EMR", "EMT", "MC"))]
    check(len(leaks) <= 2, f"badge column does not bleed into row text ({len(leaks)} leaks)")
    for r in leaks:
        print("        leak:", r["page"], r["ordinal"], "|", r["verbatim_text"][:90])
    # ordinals restart at every section run, and a heading can recur on a page
    # (p.123 has an empty base section again after "Asthma..."), so runs are what
    # must be contiguous, not (page, heading) groups.
    # a section continues across pages (p.123 -> p.124 keeps counting), so the run
    # key is the heading alone; a repeat of the same heading restarts at 0.
    runs, prev_head = [], None
    for r in rows:
        if prev_head == r["section_heading"] and r["section_ordinal"] != 0:
            runs[-1].append(r["section_ordinal"])
        else:
            runs.append([r["section_ordinal"]])
        prev_head = r["section_heading"]
    check(all(v == list(range(len(v))) for v in runs),
          "section ordinals are contiguous from 0 within every section run")

    print("stage 2 — alignment")
    tot = align["totals"]
    check(tot["matched"] + tot["ambiguous"] == tot["site_rows"],
          f"matched {tot['matched']} + ambiguous {tot['ambiguous']} = "
          f"site rows {tot['site_rows']}")
    check(tot["matched"] + tot["ambiguous"] + tot["absent_from_site"] == tot["total_accounted"],
          f"matched + ambiguous + absent = {tot['total_accounted']} accounted")
    check(tot["absent_from_site"] == sum(len(p["absent"]) for p in align["pages"]),
          f"absent total {tot['absent_from_site']} equals the sum of the page lists")
    amb = [r for p in align["pages"] for r in p["rows"] if r["status"] == "ambiguous"]
    check(len(amb) == tot["ambiguous"], f"{len(amb)} ambiguous rows are all listed")
    check(all(r.get("reason") for r in amb), "every ambiguous row states why")
    check(all(r.get("reason_kind") in ("multiple_candidates", "no_counterpart",
                                      "shared_pems_row", "other") for r in amb),
          "every ambiguous row carries a classification reason_kind")
    check(not [r for p in align["pages"] for r in p["rows"]
               if r.get("reason_kind") == "unresolved_section"],
          "unresolved_section is never a terminal disposition")
    fb = [r for p in align["pages"] for r in p["rows"] if r.get("section_fallback")]
    check(all(r.get("section_note") and r["status"] in ("matched", "ambiguous") for r in fb),
          f"every section-fallback row ({len(fb)}) is classified and carries its note")
    matched = [r for p in align["pages"] for r in p["rows"] if r["status"] == "matched"]
    check(all(r.get("pems_page") and r.get("badges") for r in matched),
          "every matched row cites a PEMS page and badge")
    # within one page a PEMS row may back only one site row (two site pages may
    # legitimately share a source: Electrical Injuries and Lightning Injuries both
    # cite p.96)
    clashes = []
    for p in align["pages"]:
        seen = set()
        for r in p["rows"]:
            if r["status"] != "matched":
                continue
            key = (r["pems_page"], r["pems_ordinal"])
            if key in seen:
                clashes.append((p["site_page"], key))
            seen.add(key)
    check(not clashes, f"no PEMS row backs two site rows on the same page ({len(clashes)} clashes)")
    for c in clashes[:10]:
        print("        clash:", c)

    print("deliverables")
    for name in ("missing-rows.md", "ambiguous-rows.md", "alignment.json",
                 "pems_table.json", ".cache/pems_rows.jsonl"):
        check(os.path.exists(os.path.join(OUT, name)), f"{name} exists")
    md = open(os.path.join(OUT, "missing-rows.md"), encoding="utf-8").read()
    check(f"**Total: {tot['absent_from_site']} rows" in md,
          f"missing-rows.md states the same total ({tot['absent_from_site']})")
    check("**152**" in md, "missing-rows.md reconciles with the prior scan's 152")
    rec_path = os.path.join(OUT, "reconciliation.json")
    check(os.path.exists(rec_path), "reconciliation.json exists")
    if os.path.exists(rec_path):
        rec = json.load(open(rec_path, encoding="utf-8"))
        b = rec["bridge"]
        c = rec["prior_to_now"]["counts"]
        nc = rec["new_unpaired"]["counts"]
        check(b["prior_reported"] == 152, f"prior reported total is 152 ({b['prior_reported']})")
        check(sum(c.values()) == 152, f"every prior row lands in exactly one cause bucket "
                                      f"({sum(c.values())} of 152)")
        paired = (c.get("paired_to_site_row_section_ordinal", 0)
                  + c.get("paired_to_site_row_label", 0)
                  + c.get("paired_to_site_row_text", 0)
                  + c.get("resolved_by_section_fallback", 0))
        check(paired == b["prior_missing_now_paired"],
              f"paired count {paired} equals the bridge's paired count")
        check(c.get("still_absent", 0) + nc.get("absent", 0) == tot["absent_from_site"],
              f"absent {tot['absent_from_site']} = still absent {c.get('still_absent', 0)} + "
              f"newly absent {nc.get('absent', 0)}")
        check(rec["new_unpaired"]["count"] == b["newly_unpaired_not_in_prior_list"],
              "newly unpaired total matches its bridge entry")
        check(len(rec["prior_to_now"]["rows"].get("still_absent", [])) == c.get("still_absent", 0),
              "the still-absent bucket names every row it counts")
        for k, v in rec["prior_to_now"]["rows"].items():
            check(len(v) == c[k], f"bucket '{k}' names {len(v)} rows and counts {c[k]}")
        check(len(rec["new_unpaired"]["rows"]) == rec["new_unpaired"]["count"],
              "newly unpaired bucket names every row it counts")
        check(rec["prior_to_now"]["verdicts"] and
              sum(rec["prior_to_now"]["verdicts"].values()) == paired,
              "every paired row carries a trust verdict")
        hr = rec["prior_to_now"].get("human_review") or {}
        check(sum(hr.values()) + b["prior_missing_now_paired_unreviewed"] == paired,
              "reviewed pairings + unreviewed pairings = all pairings")
        stale = set(C.REVIEW_VERDICTS) - {
            (r["site_page"], r["pems_page_now"], r["pems_ordinal_now"])
            for k in rec["prior_to_now"]["rows"] if k.startswith(("paired_to_site_row", "resolved_by"))
            for r in rec["prior_to_now"]["rows"][k]}
        check(not stale, f"every recorded human review still maps to a pairing ({len(stale)} stale)")
        check(b["prior_missing_now_paired_reviewed_suspect"] == hr.get("suspect", 0),
              f"{hr.get('suspect', 0)} pairings are recorded as suspect, not as settled")
        # a pairing counted as a win must show its evidence
        weak = [r for k, v in rec["prior_to_now"]["rows"].items()
                if k.startswith(("paired_to_site_row", "resolved_by"))
                for r in v if r.get("verdict") == "needs_a_human_eye"]
        check(all(r.get("similarity") is not None and r.get("pems_text_now") for r in weak),
              f"the {len(weak)} flagged pairings show similarity and PEMS text")
        led = align["totals"]["pems_rows_by_disposition"]
        check(align["totals"]["pems_rows_in_scope"] == sum(
            len(p.get("pems_row_ledger") or []) for p in align["pages"]),
              "the ledger covers every in-scope PEMS row")
        check(led.get("unaccounted", 0) == 0,
              f"no PEMS row in scope is unaccounted for ({led.get('unaccounted', 0)})")
    amd = open(os.path.join(OUT, "ambiguous-rows.md"), encoding="utf-8").read()
    check(f"**Total: {tot['ambiguous']} rows**" in amd,
          f"ambiguous-rows.md states the same total ({tot['ambiguous']})")

    print("no protocol pages touched")
    st = subprocess.run(["git", "status", "--porcelain", "--", "docs/"], cwd=REPO,
                        capture_output=True, text=True).stdout.strip()
    check(st == "", "git status shows no modified files under docs/")

    print()
    if fails:
        print(f"{len(fails)} INVARIANT(S) FAILED")
        return 1
    print("all invariants hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
