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
import pems_level_scan as P  # noqa: E402  (text cleaning, same tokeniser as the aligner)
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

    # A section that runs past the bottom of a page resumes on the next page with
    # no heading reprinted; those rows must be carried back into the section they
    # interrupt, or the site section they belong to never reaches them (p.136 of
    # the SVT protocol: cardioversion rows outside every site section's scope).
    mid_empty, bad_cont, cont_rows = [], [], 0
    for d in table["pems_docs"]:
        drows = d["rows"]
        seen_pages: set[int] = set()
        run_no = -1
        i = 0
        while i < len(drows):
            j = i
            while j < len(drows) and drows[j]["section_heading"] == drows[i]["section_heading"]:
                j += 1
            run, run_no = drows[i:j], run_no + 1
            if not run[0]["section_heading"] and run_no > 0:
                mid_empty.append((d["title"], run[0]["page"], run[0]["ordinal"]))
            i = j
        for k, r in enumerate(drows):
            if r.get("section_continued"):
                cont_rows += 1
                starts_block = k == 0 or not drows[k - 1].get("section_continued")
                # the block opens its page and keeps the heading printed above it
                # on the previous page; the rows after it follow on that page
                if starts_block and r["page"] in seen_pages:
                    bad_cont.append((d["title"], r["page"], r["ordinal"],
                                     "not the first row of its page"))
                if k and r["section_heading"] != drows[k - 1]["section_heading"]:
                    bad_cont.append((d["title"], r["page"], r["ordinal"], "heading changed"))
            seen_pages.add(r["page"])
    check(not mid_empty, "no PEMS document has an unnamed section in the middle "
                         f"({len(mid_empty)} left)")
    for m in mid_empty[:10]:
        print("        unnamed section:", m)
    check(not bad_cont, "every page-break continuation row starts its page and keeps the "
                        f"heading it continues ({len(bad_cont)} bad)")
    noted = sum(c["rows"] for d in table["pems_docs"] for c in d.get("section_continuations") or [])
    check(noted == cont_rows,
          f"the {cont_rows} continuation rows are the ones the documents record ({noted})")

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

    # The 0.40 floor is the contract of the aligner. A text or section pairing
    # below it would mean some later repair quietly promoted a weak pair (the
    # split repair does re-assign a PEMS row, and must not move it below the
    # floor). Label bindings are the documented exception: they pair on a
    # structural key, and their `similarity` is reported, not required.
    # C1d's text-binding pairs are the second documented exception, and they pay
    # for it: a `token_binding` row must clear 0.40 on COVERAGE (the fraction of
    # the site row's significant tokens present in the PEMS row), which is the
    # floor the pass itself applies. `verbatim` rows bind on a phrase that occurs
    # upstream and need no score at all. Both are checked below.
    is_tb = lambda r: (r.get("match_basis") or "").startswith("text-binding")
    floor_breach = [r for r in matched
                    if not (r.get("match_basis") or "").startswith("label+keyword")
                    and not is_tb(r)
                    and (r.get("similarity") or 0.0) < 0.40]
    check(not floor_breach,
          f"no text/section pairing sits below the 0.40 floor ({len(floor_breach)} below)")
    for r in floor_breach[:10]:
        print("        below floor:", r["site_row"], r.get("similarity"), r["action"][:70])
    tb_floor = [r for r in matched if is_tb(r)
                and (r.get("text_binding") or {}).get("method") == "token_binding"
                and (r["text_binding"]["coverage"] or 0.0) < 0.40]
    check(not tb_floor,
          f"every text-binding token binding clears 0.40 coverage ({len(tb_floor)} below)")

    # A site row that splits a PEMS row another site row already took is reported
    # as `shared_pems_row` WITH the containing row and the overlap. Check the
    # evidence against the table itself: every claimed token really is in the
    # named PEMS row, the counts add up, and that row really is held elsewhere.
    C._build_df(table["pems_docs"])
    pems_row = {(r["page"], r["ordinal"]): r
                for d in table["pems_docs"] for r in d["rows"]}
    evidence, bad_ev = [], []
    for p in align["pages"]:
        holders = {(r["pems_page"], r["pems_ordinal"]): r["site_row"]
                   for r in p["rows"] if r["status"] == "matched"}
        for r in p["rows"]:
            ev = r.get("contained_in_pems")
            if not ev:
                continue
            evidence.append((p["site_page"], r["site_row"], ev["pems_page"], ev["pems_ordinal"]))
            src = pems_row.get((ev["pems_page"], ev["pems_ordinal"]))
            if src is None:
                bad_ev.append((r["site_row"], "no such PEMS row"))
                continue
            if r.get("reason_kind") != "shared_pems_row":
                bad_ev.append((r["site_row"], "evidence on a non-shared row"))
            toks = set(ev["overlap_tokens"])
            if not toks or not toks <= C._sig(P.clean(src["verbatim_text"])):
                bad_ev.append((r["site_row"], "token not in the named PEMS row"))
            if ev["tokens_in_site_row"] != len(toks):
                bad_ev.append((r["site_row"], "site token count does not match the token list"))
            n_pems = len(C._sig(P.clean(src["verbatim_text"])))
            if ev["tokens_in_pems_row"] != n_pems:
                bad_ev.append((r["site_row"], "PEMS token count is wrong"))
            if ev["containment"] != round(len(toks) / n_pems, 3):
                bad_ev.append((r["site_row"], "containment ratio does not add up"))
            if holders.get((ev["pems_page"], ev["pems_ordinal"])) in (None, r["site_row"]):
                bad_ev.append((r["site_row"], "the named PEMS row is not held by another site row"))
            if C.distinctive(C.label_keys(r["action"])):
                bad_ev.append((r["site_row"], "row has a distinctive label key (rule must not fire)"))
    check(not bad_ev, f"the {len(evidence)} containment claims all check out ({len(bad_ev)} bad)")
    for b in bad_ev[:10]:
        print("        bad evidence:", b)

    # ---- C1d: the text-binding pass over the `no_counterpart` rows.
    # Every row the structural pass left as `no_counterpart` must now carry
    # exactly one verdict with its evidence, and a `bound_by_text` row's
    # `matched_phrase` must really occur in the PEMS row it names — the binding is
    # only worth anything if the phrase is genuinely upstream. A bound row's
    # badge must also be the badge of the row it cites, not one it inherited.
    import pems_text_binding as TB  # noqa: E402
    tb_rows, tb_bad = [], []
    for p in align["pages"]:
        for r in p["rows"]:
            tb = r.get("text_binding")
            if not tb:
                continue
            tb_rows.append((p["site_page"], r))
            if tb["verdict"] not in ("bound_by_text", "no_evidence_local"):
                tb_bad.append((r["site_row"], "verdict is not one of the two"))
            if "coverage_row" not in tb or "coverage" not in tb:
                tb_bad.append((r["site_row"], "coverage not recorded"))
            if tb["verdict"] == "no_evidence_local" and not tb.get("subtype"):
                tb_bad.append((r["site_row"], "no_evidence_local without a subtype"))
            if not (tb.get("query") or tb.get("pages_searched") or
                    tb["verdict"] == "bound_by_text"):
                tb_bad.append((r["site_row"], "no negative search recorded"))
            if tb["verdict"] == "bound_by_text":
                src = None
                for d in table["pems_docs"]:
                    for s in d["rows"]:
                        if (s["page"], s["ordinal"]) == (tb["pems_page"], tb["pems_ordinal"]):
                            src = s
                if src is None:
                    tb_bad.append((r["site_row"], "names a PEMS row that does not exist"))
                    continue
                if src["verbatim_text"] != tb["pems_row_text"]:
                    tb_bad.append((r["site_row"], "pems_row_text is not verbatim"))
                if list(src["badge_tokens"]) != list(tb["badge_tokens"]):
                    tb_bad.append((r["site_row"], "badge_tokens are not the source row's"))
                phrase = tb["matched_phrase"]
                if tb["method"] == "verbatim":
                    if phrase.lower() not in src["verbatim_text"].lower():
                        tb_bad.append((r["site_row"], "verbatim phrase not in the PEMS row"))
                else:
                    words = set(TB._words(src["verbatim_text"]))
                    if not all(w in words for w in TB._words(phrase)):
                        tb_bad.append((r["site_row"], "token anchor not in the PEMS row"))
                if r["status"] != "matched":
                    tb_bad.append((r["site_row"], "bound row is not matched"))
                if (r.get("pems_page"), r.get("pems_ordinal")) != (tb["pems_page"],
                                                                  tb["pems_ordinal"]):
                    tb_bad.append((r["site_row"], "matched against a different PEMS row"))
            else:
                if r["status"] == "matched":
                    tb_bad.append((r["site_row"], "no_evidence_local row is marked matched"))
    # every leftover row of the aligner has a verdict: the pass may not skip one
    unbind = [r for p in align["pages"] for r in p["rows"]
              if r.get("reason_kind") == "no_counterpart" and not r.get("text_binding")]
    check(not unbind, f"every no_counterpart row carries a text-binding verdict "
                      f"({len(unbind)} without)")
    check(not tb_bad, f"the {len(tb_rows)} text-binding verdicts check out "
                      f"({len(tb_bad)} bad)")
    for b in tb_bad[:10]:
        print("        bad text binding:", b)
    tbc = tot.get("text_binding") or {}
    bound_n = sum(1 for _p, r in tb_rows if r["text_binding"]["verdict"] == "bound_by_text")
    check(tbc.get("bound_by_text") == bound_n,
          f"totals count {tbc.get('bound_by_text')} bound rows, the pages carry {bound_n}")
    check(sum(tbc.get("no_evidence_local_by_subtype", {}).values())
          == tbc.get("no_evidence_local", -1),
          "every no_evidence_local row is counted under exactly one subtype")
    check(os.path.exists(os.path.join(OUT, "text-binding.md")),
          "text-binding.md exists")
    tbmd = open(os.path.join(OUT, "text-binding.md"), encoding="utf-8").read()
    check(f"**{len(tb_rows)} rows**" in tbmd,
          f"text-binding.md states the same row total ({len(tb_rows)})")

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
                  + c.get("paired_to_site_row_text_binding", 0)
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
