#!/usr/bin/env python3
"""Invariant checks for the level-scan rebuild artifacts (stages 1+2).

Run after `pems_canonical.py --stage all`. Exits non-zero and prints the failed
invariant when something does not add up.

It is also runnable on a clean clone: the one input it cannot get from git is
the derived `.cache/pems_rows.jsonl` (git-ignored), so when it is absent the
script builds it from the PDF itself — writing the cache and nothing else, never
`pems_table.json` / `alignment.json` / `missing-rows.md`.

This exists because the previous pipeline's report was believed without
checking: "0 fixable mismatches" was true by its own definition while 154 rows
were wrong.

    python scripts/verify_pems_canonical.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "audit", "level-scan")
sys.path.insert(0, os.path.join(REPO, "scripts"))
import pems_canonical as C  # noqa: E402  (for the human-review table)
import pems_level_scan as P  # noqa: E402  (text cleaning, same tokeniser as the aligner)
fails: list[str] = []

LV = ["EMR", "EMT", "A", "I", "P"]

# Manifest of the checks this verifier runs. Every entry must be reached by a
# section() call during main(), and the last check asserts exactly that, so a
# check cannot be dropped from the run without the run failing.
MANIFEST = [
    ("stage1.pems_table",
     "PEMS table integrity: page decisions, row fields, badges, ordinals, "
     "page-break continuations"),
    ("stage2.alignment",
     "alignment integrity: totals, ambiguity classifications, containment "
     "evidence, 0.40 floor, text-binding verdicts"),
    ("c2.split_map",
     "split-map invariant: the union of the levels published by the site rows "
     "that split a PEMS row equals the PEMS badge level and every level above "
     "it, each listed row still exists (in either table format), and each row's "
     "chip is the level the conversion ledger records for it"),
    ("c2.row_splits",
     "row-splits.yaml: every declared fused-row split is applied by "
     "pems_table.json, no applied split is undeclared, and the declared parts "
     "reproduce a row a fresh parse of the page produces (no word added or "
     "dropped)"),
    ("c2.badge_overrides",
     "badge-overrides.yaml: every override names an existing PEMS row, keeps a "
     "reason and evidence, cannot drift from the PDF token, and is actually "
     "applied by pems_table.json (original token retained)"),
    ("c2.recheck",
     "badge re-check: at_risk matched rows in c2-scope.json equal the recheck "
     "script's output, both p.61#4/p.63#7 mapped rows are named, provisional "
     "flags are derived, and the adjudicator note is present"),
    ("deliverables",
     "deliverables exist and state the same totals as the artifacts"),
    ("docs_clean", "no protocol page under docs/ is modified"),
]
_ran: set[str] = set()


def section(cid: str) -> None:
    assert cid in dict(MANIFEST), f"unlisted check section {cid}"
    _ran.add(cid)


def check(cond: bool, msg: str) -> None:
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


def load_verifier_exceptions() -> dict[tuple[int, int], str]:
    """Documented badge-bleed leaks: {(page, ordinal): reason}.

    `verifier-exceptions.yaml` is the only place a leak may be tolerated. An entry
    without a reason (or without page/ordinal) is itself a failure — an exception
    nobody can explain is not an exception.
    """
    path = os.path.join(OUT, "verifier-exceptions.yaml")
    check(os.path.exists(path), "verifier-exceptions.yaml exists")
    if not os.path.exists(path):
        return {}
    doc = yaml.safe_load(open(path, encoding="utf-8")) or {}
    entries = doc.get("leaks") or []
    out: dict[tuple[int, int], str] = {}
    problems = []
    for e in entries:
        page, ordinal, reason = e.get("page"), e.get("ordinal"), (e.get("reason") or "").strip()
        if not isinstance(page, int) or not isinstance(ordinal, int):
            problems.append(f"entry without an integer page/ordinal: {e!r}")
        elif not reason:
            problems.append(f"p.{page} #{ordinal} has no reason")
        else:
            out[(page, ordinal)] = reason
    check(not problems, "every documented badge-bleed exception carries a page, an "
                        "ordinal and a reason" + (f" ({'; '.join(problems)})" if problems else ""))
    return out


def levels(cells) -> set[str]:
    """The levels a site row authorises.

    A non-blank cell at level X grants X and every level above it (the same
    spread `pems_table.json` records in `columns{}`). `MC` in every cell means
    all levels contact Medical Control, i.e. the full set. A blank cell grants
    nothing.
    """
    cells = [(c or "").strip() for c in cells]
    if len(cells) != len(LV):
        raise ValueError(f"expected {len(LV)} level cells, got {len(cells)}: {cells}")
    if all(c and "MC" in c.upper() for c in cells):
        return set(LV)
    got: set[str] = set()
    for i, c in enumerate(cells):
        if c:
            got |= set(LV[i:])
    return got


def expected_levels(badge: str) -> set[str]:
    """The PEMS badge level and every level above it (`MC` = the full set)."""
    badge = (badge or "").strip().strip("[]").upper()
    if badge == "MC":
        return set(LV)
    if badge not in LV:
        raise ValueError(f"badge {badge!r} is neither a level nor MC")
    return set(LV[LV.index(badge):])


def fmt_levels(s: set[str]) -> str:
    return "/".join(L for L in LV if L in s) or "·"


def ledger_level_index() -> dict:
    """(file, row) -> level_published, from audit/level-scan/level-rule-ledger.json.

    The ledger is the join key back to the conversion: it records, per action row,
    which provider level the page publishes now and why. Re-deriving a site row's
    level from the page alone cannot tell a renumbered row from a merged one; the
    ledger can, because it is keyed on the action row the conversion wrote.
    """
    path = os.path.join(OUT, "level-rule-ledger.json")
    if not os.path.exists(path):
        return {}
    doc = json.load(open(path, encoding="utf-8"))
    return {(e["file"], str(e["row"])): e for e in doc.get("rows") or []}


def check_split_map(pems_row: dict) -> None:
    """Re-derive the split invariant from the site pages.

    A `held_level_correct` row is a site row that splits a PEMS row the region
    merges. Its levels are right only while every site row that splits the PEMS
    row still publishes exactly the PEMS badge spread. `audit/level-scan/
    split-map.yaml` records those pairings (derived by scripts/build_split_map.py);
    this check re-parses each named row on every run and FAILS when the union
    stops equalling the expected set, when a named row no longer exists (renumbered
    or merged away — the change the OMD must be told about), when the row's chip
    disagrees with the level the ledger records for it, or when the yaml's badge
    has drifted from `pems_table.json`.

    Rows are read through `pems_level_scan.read_action_rows`, which understands BOTH
    the legacy 7-column matrix and the collapsed one-chip table. Reading only the
    matrix is what made a converted page look like a page whose rows had been
    deleted: the rows were there, in a format the reader did not parse.
    """
    path = os.path.join(OUT, "split-map.yaml")
    check(os.path.exists(path), "split-map.yaml exists")
    if not os.path.exists(path):
        return
    doc = yaml.safe_load(open(path, encoding="utf-8")) or {}
    splits = doc.get("splits") or []
    # The count is a "did the derivation shrink silently" guard, not a target: it was 7
    # when the map was first written, and the 2026-11-20 row-structure pass took it to 11.
    # Four more held rows now agree with their PEMS row exactly under the one-chip layout
    # (CT r6, Stroke r7, Respiratory Distress r10, Trauma r7), so they are recorded as
    # splits too, and Pneumothorax r12 left the p.243#4 split because it now cites p.113#4
    # for its own half. Every entry below is still checked against the pages; the count
    # only has to match what the derivation produces.
    from build_split_map import build as _derive_splits
    check(len(splits) == len(_derive_splits()),
          f"split-map.yaml records every split the derivation produces "
          f"({len(splits)} listed, {len(_derive_splits())} derived)")
    ids = [s.get("id") for s in splits]
    check(len(ids) == len(set(ids)) and all(ids), "every split carries a unique id")
    led = ledger_level_index()

    for s in splits:
        sid = s.get("id")
        pems = s.get("pems") or {}
        key = (int(str(pems.get("page"))), int(str(pems.get("ordinal"))))
        badge = pems.get("badge")
        src = pems_row.get(key)
        # 6. the yaml must not drift from the table
        if src is None:
            check(False, f"split {sid}: PEMS p.{key[0]} #{key[1]} is not in pems_table.json")
            continue
        tbl_badge = (src.get("badge_tokens") or [None])[0]
        check(badge == tbl_badge,
              f"split {sid}: badge {badge!r} matches pems_table.json for "
              f"p.{key[0]} #{key[1]} ({tbl_badge!r})")

        site_rows = s.get("site_rows") or []
        check(bool(site_rows), f"split {sid}: names at least one site row")
        # 1. read every named row with the scanner's own parser, either format
        union, producers, missing, drifted = set(), [], [], []
        for sr in site_rows:
            rel, num = sr.get("file"), sr.get("row")
            page = P.read_action_rows(os.path.join(REPO, "docs", rel))
            hits = [r for r in page.get("rows") or []
                    if str(r.get("num", "")).strip() == str(num)]
            if len(hits) != 1:
                missing.append((rel, num, len(hits)))
                continue
            got = levels(hits[0]["cells"])
            union |= got
            producers.append(f"{os.path.basename(rel)} r{num} → {fmt_levels(got)}")
            # 2. the ledger is the join key: the row's chip must be the level the
            # conversion recorded for that (file, row), not merely a level that
            # happens to make the union add up
            entry = led.get((rel, str(num)))
            if entry and hits[0].get("chip") and hits[0]["chip"] != entry["level_published"]:
                drifted.append(f"{os.path.basename(rel)} r{num}: chip {hits[0]['chip']} "
                               f"but the ledger records {entry['level_published']}")
        # 3. a row that vanished is a failure, not silence
        for rel, num, n in missing:
            where = ""
            page = P.read_action_rows(os.path.join(REPO, "docs", rel))
            if page.get("format") is None:
                where = " (the page carries no level table in either format)"
            check(False,
                  f"split {sid}: site row {rel} r{num} no longer exists on the page "
                  f"({n} rows carry that number){where} — renumbered or merged away; "
                  f"update split-map.yaml and tell the OMD")
        if missing:
            continue
        check(not drifted, f"split {sid}: every named row's chip is the level the ledger "
                           f"records" + (f" ({'; '.join(drifted)})" if drifted else ""))
        # 4-5. the union must be exactly the PEMS badge spread
        exp = expected_levels(str(badge or ""))
        check(union == exp,
              f"split {sid}: PEMS p.{key[0]} #{key[1]} badge {badge} expects "
              f"{{{fmt_levels(exp)}}}; site rows publish {{{fmt_levels(union)}}} "
              f"({'; '.join(producers)})")



def check_row_splits(table: dict) -> None:
    """row-splits.yaml is the durable home of a fused-row repair.

    The extractor can hand a printed cell's last lines to the next printed badge;
    one extracted row then carries two badges' worth of text. A split moves that
    boundary and nothing else, so it is checked the way an override is: the file
    must parse strictly, every declared split must be applied by pems_table.json,
    no applied split may be missing from the file, and — the check that makes the
    claim about the source rather than about our own output — the declared parts,
    concatenated, must reproduce the row the PDF parser produces on a fresh parse
    of that page.
    """
    import re as _re
    path = os.path.join(OUT, "row-splits.yaml")
    check(os.path.exists(path), "row-splits.yaml exists")
    if not os.path.exists(path):
        return
    splits, _ = C._load_row_splits()
    norm = lambda s: _re.sub(r"\s+", " ", str(s or "")).strip()
    stored = (table.get("row_splits") or {}).get("rows") or []
    check((table.get("row_splits") or {}).get("count") == len(splits),
          f"pems_table.json records the {len(splits)} declared row split(s) "
          f"({(table.get('row_splits') or {}).get('count')} recorded)")

    xml = P._read_pdf_xml(False)
    fresh: dict[int, dict] = {}
    for pno, m in enumerate(P.PAGE_RE.finditer(xml), 1):
        if pno in {int(p) for p, _o in splits}:
            body = m.group(3)
            fresh[pno] = C.parse_page(pno, body, C.page_title(body))

    applied_keys = {(r["page"], r["ordinal"]) for r in stored}
    stale = applied_keys - set(splits)
    check(not stale, f"no split row in pems_table.json lacks a row-splits.yaml entry "
                     f"({sorted(stale)} undeclared)")
    for (page, ordn), sp in sorted(splits.items()):
        label = f"p.{page} #{ordn}"
        parts = sp["parts"]
        declared = [p for p in parts if p.get("merge") != "next"]
        got = [r for r in stored if (r["page"], r["ordinal"]) == (page, ordn)]
        check(len(got) == len(declared),
              f"split {label}: pems_table.json carries {len(got)} row(s) for the "
              f"{len(declared)} named printed cell(s)")
        if [r["part"] for r in got] != sorted(r["part"] for r in got):
            check(False, f"split {label}: the stored parts are out of printed order")
        check([r["badge"] for r in sorted(got, key=lambda r: r["part"])]
              == [p["badge"] for p in declared],
              f"split {label}: the stored badges are the declared ones "
              f"({[p['badge'] for p in declared]})")
        check([norm(r["verbatim_text"]) for r in sorted(got, key=lambda r: r["part"])]
              == [norm(p["text"]) for p in declared],
              f"split {label}: the stored text is the declared text")
        # the claim is about the source: the parts must rebuild a row the PDF
        # parser produces from the page right now
        joined = norm(" ".join(p["text"] for p in parts))
        fresh_texts = [norm(r["verbatim_text"]) for r in (fresh.get(page) or {}).get("rows") or []]
        check(joined in fresh_texts,
              f"split {label}: the declared parts reproduce a row a fresh parse of "
              f"p.{page} produces (no word added or dropped)")
        # a merged part must survive on the row that follows, not vanish
        mids = [p["text"] for p in parts if p.get("merge") == "next"]
        if mids:
            following = " ".join(norm(r["verbatim_text"]) for d in table["pems_docs"]
                                 for r in d["rows"]
                                 if r["page"] == page and r["ordinal"] > ordn)
            check(all(norm(t) in following for t in mids),
                  f"split {label}: the {len(mids)} merged part(s) are carried onto a later "
                  f"row of p.{page} (not dropped)")


def check_badge_overrides(table: dict, pems_row: dict) -> None:
    """badge-overrides.yaml is the durable home of a badge resolution.

    A resolution written only into an adjudication output is not durable: the
    next C1 regeneration reintroduces the PDF badge and the contradiction
    returns. So the file is checked as strictly as exceptions.yaml: reason and
    evidence are mandatory, a row that does not exist is a failure, an override
    that the table did not apply is a failure, and `badge_token_from_pdf` must
    agree with the token the table parsed — an override may correct the badge,
    never drift from the source it is correcting.
    """
    path = os.path.join(OUT, "badge-overrides.yaml")
    check(os.path.exists(path), "badge-overrides.yaml exists")
    if not os.path.exists(path):
        return
    doc = yaml.safe_load(open(path, encoding="utf-8")) or {}
    ovs = doc.get("overrides")
    check(isinstance(ovs, list), "badge-overrides.yaml carries an `overrides` list")
    ovs = ovs or []
    bad = []
    applied_rows = {}
    for d in table["pems_docs"]:
        for r in d["rows"]:
            if r.get("badge_override_applied"):
                applied_rows[(r["page"], r["ordinal"])] = r
    for ov in ovs:
        key = (int(ov.get("page")), int(ov.get("ordinal")))
        label = f"p.{key[0]} #{key[1]}"
        for fld in ("reason", "evidence"):
            if not str(ov.get(fld) or "").strip():
                bad.append(f"{label}: `{fld}` is mandatory")
        src = pems_row.get(key)
        if src is None:
            bad.append(f"{label}: no such PEMS row in pems_table.json")
            continue
        if not src.get("badge_override_applied"):
            bad.append(f"{label}: override is not applied by pems_table.json")
            continue
        pdf = src.get("badge_token_from_pdf") or []
        if not pdf or pdf[0] != ov.get("badge_token_from_pdf"):
            bad.append(f"{label}: badge_token_from_pdf {ov.get('badge_token_from_pdf')!r} "
                       f"disagrees with the parsed token {pdf[:1]}")
        resolved = str(ov.get("resolved") or "").strip().strip("[]").upper()
        if src.get("badge_tokens") != [resolved]:
            bad.append(f"{label}: resolved badge {resolved!r} is not the table's badge")
        if not str(ov.get("resolved_by") or "").strip():
            bad.append(f"{label}: `resolved_by` is mandatory")
    check(not bad, f"the {len(ovs)} badge overrides are complete and applied "
                   f"({len(bad)} problems)")
    for b in bad[:10]:
        print("        bad override:", b)
    # the other direction: a table row cannot claim an override nobody declared
    declared = {(int(o.get("page")), int(o.get("ordinal"))) for o in ovs}
    undeclared = sorted(set(applied_rows) - declared)
    check(not undeclared,
          f"every row the table marks badge_override_applied is declared in the yaml "
          f"({len(undeclared)} undeclared)")
    # the retained token is what makes a resolution reversible
    check(all(r.get("badge_token_from_pdf") for r in applied_rows.values()),
          "every overridden row retains the PDF token in badge_token_from_pdf")
    check(table.get("badge_overrides", {}).get("count", -1) == len(ovs),
          f"pems_table.json records {table.get('badge_overrides', {}).get('count')} "
          f"applied overrides, the yaml declares {len(ovs)}")


def check_recheck(table: dict, pems_row: dict, align: dict) -> None:
    """The re-check must cover every row mapped to the ambiguous badges.

    Only one of the three site rows mapped to p.61#4 / p.63#7 is in the C2 queue;
    the other two carry `matched` and are flagged nowhere. c2-scope.json records
    them as `at_risk_matched_rows`, and the value is checked against the recheck
    script's own output rather than trusted.
    """
    import recheck_ambiguous_badges as RC  # noqa: E402
    scope_path = os.path.join(OUT, "c2-scope.json")
    check(os.path.exists(scope_path), "c2-scope.json exists")
    if not os.path.exists(scope_path):
        return
    scope = json.load(open(scope_path, encoding="utf-8"))
    counts = scope.get("counts") or {}
    rows = scope.get("rows") or []
    queued = {(r["file"], r["row"]) for r in rows}

    ar = RC.at_risk_rows(exclude=queued)

    # provisional flags are derived from the table, not hand-set: a row is
    # provisional when it is joined to a badge that is still contradictory
    unresolved = set()
    for d in table["pems_docs"]:
        for r in d["rows"]:
            # an applied override resolves the contradiction; still-contradictory
            # rows are the ones that make a verdict provisional
            if not r.get("badge_override_applied") and row_badge_conflict(r):
                unresolved.add((r["page"], r["ordinal"]))

    listed = counts.get("at_risk_matched_rows")
    check(isinstance(listed, list), "c2-scope.json carries counts.at_risk_matched_rows")
    check(listed == ar, "at_risk_matched_rows equals the recheck script's output "
                        f"({len(listed or [])} listed, {len(ar)} derived)")
    check(counts.get("at_risk_matched_rows_count") == len(ar),
          "at_risk_matched_rows_count matches the list length")
    named = {(os.path.basename(a["file"]), a["row"]) for a in ar}
    for want, pkey in ((("04_Cardiac_Arrest_Non_Traumatic_PROC.md", 5), (63, 7)),
                       (("04_Cardiac_Arrest_Traumatic_PROC.md", 5), (61, 4))):
        if pkey in unresolved:
            check(want in named,
                  f"at-risk list names {want[0]} r{want[1]} (mapped to an ambiguous badge)")
        else:
            check(want not in named,
                  f"{want[0]} r{want[1]}: p.{pkey[0]}#{pkey[1]} is resolved, so it is "
                  "a settled flip, not an at-risk row")

    # provisional flags are derived from the table, not hand-set
    expect = set()
    import build_c2_scope as B  # noqa: E402
    align_idx = {(p["site_page"], int(r["site_row"])): r
                 for p in align["pages"] for r in p["rows"]}
    for r in rows:
        if r.get("row") is None:
            continue
        keys = set(B.pems_keys_of(r, align_idx))
        if keys & unresolved:
            expect.add((r["file"], r["row"]))
    flagged = {(r["file"], r["row"]) for r in rows if r.get("provisional")}
    check(flagged == expect,
          f"provisional flags equal the rows joined to a still-contradictory badge "
          f"({len(flagged)} flagged, {len(expect)} derived)")
    check(counts.get("provisional_count") == len(flagged),
          f"counts.provisional_count {counts.get('provisional_count')} matches the "
          f"{len(flagged)} flagged rows")
    check([(p["file"], p["row"]) for p in counts.get("provisional") or []] ==
          [(r["file"], r["row"]) for r in rows if r.get("provisional")],
          "counts.provisional enumerates exactly the provisional rows")
    broad = ("protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md", 4)
    if (63, 7) in unresolved:
        check(broad in flagged,
              "the single site_broader row is provisional (its direction rests on p.63#7)")
    else:
        check(broad not in flagged,
              "p.63#7 is resolved, so no row is provisional on it any more")

    notes = scope.get("notes_for_adjudicator") or []
    check(bool(notes), "c2-scope.json carries notes_for_adjudicator")
    check(any("one row or two" in n for n in notes),
          "notes_for_adjudicator carries the 'one row or two' test")
    check(any("authoring decision, not a level fix" in n for n in notes),
          "notes_for_adjudicator says the compound case is an authoring decision")


def row_badge_conflict(row: dict) -> bool:
    """Does this PEMS row's inline level token still contradict its badge?

    Delegates to the scope builder's detector, which knows all three marker
    shapes ([X], (X / Y), "X/Y only"). An applied override changes the row's
    badge, so a resolved row stops conflicting on its own.
    """
    import build_c2_scope as B  # noqa: E402
    flag, _reason = B.badge_ambiguity(row)
    return flag


def main() -> int:
    print(f"verifier manifest — {len(MANIFEST)} checks")
    for cid, desc in MANIFEST:
        print(f"  [{cid}] {desc}")
    print()
    section("stage1.pems_table")
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
    # A page carrying >=1 level badge group is a grid page and must yield rows.
    # p.78 (Pain Control continuation, one MC row) used to be classed "narrative"
    # by a `len(badges) >= 2` test and its row discarded, which made the ledger's
    # "PEMS prints this nowhere" claim for Pain Control r8 false. The guard parses
    # the PDF itself rather than trusting pems_table.json, so a table regenerated
    # by broken code cannot hide the defect.
    xml = P._read_pdf_xml(False)
    zero_row_badge_pages = []
    for pno, m in enumerate(P.PAGE_RE.finditer(xml), 1):
        body = m.group(3)
        rec = C.parse_page(pno, body, C.page_title(body))
        if rec.get("n_badges", 0) >= 1 and not rec["rows"]:
            zero_row_badge_pages.append(
                (pno, rec.get("kind"), rec.get("n_badges"), rec.get("title")))
    check(not zero_row_badge_pages,
          "no page carrying >=1 level badge contributes zero rows"
          + (f" (offenders: {zero_row_badge_pages})" if zero_row_badge_pages else ""))
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
    # Tolerance is an explicit, documented list — not a count. Every leak the
    # canonical table carries is named in `verifier-exceptions.yaml` with its
    # reason; a leak that is NOT listed fails, and a listed leak that has stopped
    # leaking also fails, so an exception can neither cover a new defect nor go
    # stale. (The previous form was `len(leaks) <= 2`, a bare count that tolerated
    # any two leaks; it predates the level-rule conversion, from d21aa3d.)
    known = load_verifier_exceptions()
    unexplained = [r for r in leaks if (r["page"], r["ordinal"]) not in known]
    stale = [k for k in known if k not in {(r["page"], r["ordinal"]) for r in leaks}]
    check(not unexplained,
          "badge column does not bleed into row text: every leak is documented "
          f"({len(leaks)} leak(s), {len(unexplained)} unexplained)")
    check(not stale,
          "every documented badge-bleed exception still leaks (no stale exception)")
    for r in leaks:
        why = known.get((r["page"], r["ordinal"]))
        print(f"        leak: p.{r['page']} #{r['ordinal']} | {r['verbatim_text'][:80]}"
              + (f"\n        documented: {why}" if why else "   <-- UNDOCUMENTED"))
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

    section("stage2.alignment")
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

    # ---- C2d: the split map. The 7 held rows split a PEMS row the region
    # merges; the pairing is data in split-map.yaml, not a word in a handoff
    # note, and the union invariant is re-derived from the site pages here.
    section("c2.split_map")
    check_split_map(pems_row)

    # ---- C2e: durable badge overrides + the widened re-check.
    # A badge resolution that lives only in an adjudication output is not
    # durable; it must live where the parser reads it.
    section("c2.row_splits")
    check_row_splits(table)

    section("c2.badge_overrides")
    check_badge_overrides(table, pems_row)

    section("c2.recheck")
    check_recheck(table, pems_row, align)

    section("deliverables")
    print("deliverables")
    for name in ("missing-rows.md", "ambiguous-rows.md", "alignment.json",
                 "pems_table.json", "pems_prose.json"):
        check(os.path.exists(os.path.join(OUT, name)), f"{name} exists")
    # `.cache/pems_rows.jsonl` is a *derived* artifact inside a git-ignored
    # directory, so a clean clone never has one; testing `os.path.exists` made
    # this gate red on every fresh checkout (and green on a stale cache, which
    # nothing read). Build it here when it is missing — the cache is the only
    # thing written, never the table/alignment/markdown the gate audits — and
    # then require it to be the canonical table's rows, row for row, so the
    # check still fails on a cache that has drifted from the table.
    cache_path = os.path.join(OUT, ".cache", "pems_rows.jsonl")
    cache_rows: list[dict] = []
    built = False
    have_cache = os.path.exists(cache_path)
    if have_cache:
        with open(cache_path, encoding="utf-8") as fh:
            cache_rows = [json.loads(line) for line in fh if line.strip()]
    else:
        print("  note  .cache/pems_rows.jsonl is derived and git-ignored: a clean\n"
              "        checkout has none, so it is built from the PDF now (cache only)")
        try:
            cache_rows = C.build_rows_cache()
            built = True
        except SystemExit as exc:            # pems_level_scan exits if the PDF is gone
            check(False, f"rows cache could not be built: {exc}")
    if have_cache or built:
        print(f"        rows cache: {len(cache_rows)} rows"
              + (" (built for this run)" if built else " (existing)"))
        tbl = {(r["page"], r["ordinal"]): r for r in rows}
        got = {(r["page"], r["ordinal"]): r for r in cache_rows}
        absent = sorted(set(tbl) - set(got))
        surplus = sorted(set(got) - set(tbl))
        drifted = sorted(k for k in set(tbl) & set(got)
                         if (got[k].get("section_heading"), got[k].get("verbatim_text"))
                         != (tbl[k].get("section_heading"), tbl[k].get("verbatim_text")))
        check(not absent and not surplus and not drifted,
              f"the rows cache is the canonical table's row set "
              f"({len(cache_rows)} rows; {len(absent)} absent, {len(surplus)} surplus, "
              f"{len(drifted)} drifted)")
        for label, keys in (("absent from cache", absent[:3]),
                            ("not in the table", surplus[:3]),
                            ("drifted (heading/text)", drifted[:3])):
            for k in keys:
                print(f"        {label}: p.{k[0]} #{k[1]}")
    # The prose index is the only place the unbadged PEARLS / NOTES /
    # CONTRAINDICATIONS text lives (pems_table.json stores grid rows only), so a
    # stale index silently re-opens the "PEMS prints this nowhere" defect. Compare
    # it with a fresh build: same pages, same entries, byte-for-byte.
    import build_pems_prose as BP
    fresh, n_pearls, _methods, prose_failures = BP.build()
    committed = json.load(open(os.path.join(OUT, "pems_prose.json"), encoding="utf-8"))
    check(len(committed.get("pages", {})) == 280,
          f"pems_prose.json indexes all 280 pages ({len(committed.get('pages', {}))})")
    check(not prose_failures,
          f"every prose entry verifies against the flattened text layer "
          f"({len(prose_failures)} failure(s))")
    check(committed == fresh,
          "pems_prose.json is up to date with scripts/build_pems_prose.py "
          "(pages and entries identical)")
    check(bool(n_pearls) and any(e["heading"] == "PEARLS"
                                 for v in committed.get("pages", {}).values() for e in v),
          f"the prose index carries PEARLS entries ({n_pearls} PEARLS headings)")
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

    section("docs_clean")
    print("no protocol pages touched")
    st = subprocess.run(["git", "status", "--porcelain", "--", "docs/"], cwd=REPO,
                        capture_output=True, text=True).stdout.strip()
    check(st == "", "git status shows no modified files under docs/")

    # The manifest is the contract: every listed check ran, and nothing ran
    # that is not listed.
    print()
    check(_ran == {cid for cid, _ in MANIFEST},
          f"verifier manifest covers the run ({len(_ran)} of {len(MANIFEST)} checks reached: "
          + ", ".join(cid for cid, _ in MANIFEST if cid not in _ran) + ")")

    print()
    if fails:
        print(f"{len(fails)} INVARIANT(S) FAILED")
        return 1
    print("all invariants hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
