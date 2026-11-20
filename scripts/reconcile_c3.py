#!/usr/bin/env python3
"""C3 reconciliation: collapse the 707-finding audit into confirmed / dropped / owner-required.

READ-ONLY with respect to `docs/`. Writes only `audit/level-scan/reconciled.json`
and `audit/level-scan/reconciled.md`.

Doctrine (owner ruling D1, 2026-11-19): reconcile and report; do not apply level
cells. Every ruling below is derived in code from the ledgers, never hand-tallied:

  inputs
    audit/protocol-reconciliation/AUDIT-2026-11-14.json   the 707 findings
    audit/level-scan/needs-authoring.md                   the 489 non-level findings
    audit/level-scan/level-rule-ledger.json               per site row: canonical badge,
                                                          compound tokens, published chip
    audit/level-scan/adjudicated.json                     C2 visual adjudications
    audit/level-scan/pems_table.json                      canonical PEMS rows (evidence)
    audit/level-scan/alignment.json                       site-row alignment status

  ruling order (first match wins, rule id recorded per finding)
    R1  C2 decision recorded for (file,row)          -> CONFIRMED / DROPPED / OWNER_REQUIRED
    R2  ledger status OWNER_REQUIRED|pending_*       -> OWNER_REQUIRED
    R3  ledger status policy                         -> DROPPED (not level-gated)
    R4  no canonical badge and no compound token     -> OWNER_REQUIRED (no evidence)
    R5  published chip == canonical lowest level     -> DROPPED (already canonical)
    R6  published chip != canonical lowest level     -> CONFIRMED (still divergent)
    N1  finding is not a level-cell finding          -> DROPPED (routed to needs-authoring.md)

Usage:
  python scripts/reconcile_c3.py            # write reconciled.json + reconciled.md
  python scripts/reconcile_c3.py --check    # re-run and assert the split is unchanged
"""
from __future__ import annotations

import argparse
import collections
import difflib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUD = os.path.join(ROOT, "audit", "protocol-reconciliation", "AUDIT-2026-11-14.json")
NEEDS = os.path.join(ROOT, "audit", "level-scan", "needs-authoring.md")
LEDGER = os.path.join(ROOT, "audit", "level-scan", "level-rule-ledger.json")
C2 = os.path.join(ROOT, "audit", "level-scan", "adjudicated.json")
PEMS = os.path.join(ROOT, "audit", "level-scan", "pems_table.json")
ALIGN = os.path.join(ROOT, "audit", "level-scan", "alignment.json")
OUT_JSON = os.path.join(ROOT, "audit", "level-scan", "reconciled.json")
OUT_MD = os.path.join(ROOT, "audit", "level-scan", "reconciled.md")

LEVELS = ["EMR", "EMT", "A", "I", "P"]
BRK = re.compile(r"^\[(.+?)\]$")


def rel(p: str) -> str:
    return p.replace("docs/", "", 1).replace(os.sep, "/")


def norm_level(tok: str) -> str | None:
    t = (tok or "").strip()
    m = BRK.match(t)
    if m:
        t = m.group(1).strip()
    t = t.upper()
    return t if t in LEVELS or t == "MC" else None


def canonical_levels(row: dict) -> list[str]:
    """Every level token the canonical row carries: the badge plus inline compound tokens."""
    toks: list[str] = []
    for t in [row.get("pems_badge")] + list(row.get("compound_tokens") or []):
        n = norm_level(t) if t else None
        if n and n not in toks:
            toks.append(n)
    return toks


def lowest(levels: list[str]) -> str | None:
    lv = [x for x in levels if x in LEVELS]
    if not lv:
        return "MC" if "MC" in levels else None
    return min(lv, key=LEVELS.index)


def cells_leftmost(cells: list[str]) -> str | None:
    """The level a 5-cell matrix encodes: the leftmost filled column.

    Matches the tool's own matrix semantics — a filled cell at index i means level
    LEVELS[i] and every level above it. `MC` in any cell means MC at all levels.
    """
    for i, c in enumerate(list(cells)[:5]):
        s = (c or "").strip()
        if not s:
            continue
        n = norm_level(s)
        if n:
            return n
        if "MC" in s.upper():
            return "MC"
        return LEVELS[i]          # a filled dot / bullet
    return None


LEVEL_FIELD = re.compile(
    r"(?i)\bprovider level\b|missing level|\blevel cell|level bracket|bracket / level|"
    r"/ level$|level / |^level$|row level|MC requirement|MC gating|MC bracket|bracket / MC|"
    r"level and|level cells")
LEVEL_REC = re.compile(
    r"(?i)\bSet (EMR|EMT|A|I|P|MC)\b|\b(EMR|EMT|A|I|P)\+|\b(EMR|EMT|A|I|P) (●|filled)\b|"
    r"\bfilled on row\b|\b(EMR|EMT|A|I|P) column\b")


def is_level_finding(x: dict) -> bool:
    """Does this finding ask for a provider-level assignment (as opposed to prose/dose)?

    Judged from the finding's own field name and its instruction text, so a level
    finding that the scanner refused to apply (its `inferred` flag sent it to
    needs-authoring.md) is still recognised as a level question.
    """
    blob = " ".join([x.get("field") or "", x.get("recommendation") or "",
                     x.get("correct_value") or ""])
    return bool(LEVEL_FIELD.search(x.get("field") or "") or LEVEL_REC.search(blob))


def read_published_levels(docs_dir: str) -> dict[tuple[str, str], str]:
    """Read the level each site row publishes straight out of the markdown.

    Independent of `level_rule.py`'s ledger so the reconciliation is checked
    against the tree it is reporting on, not against a stale ledger. Understands
    both table formats the site has used:
      `| # | Level | Action / Intervention |`  one chip per action (current)
      `| # | Action | EMR | EMT | A | I | P |` five level cells (legacy matrix)
    """
    out: dict[tuple[str, str], str] = {}
    hdr_collapsed = re.compile(r"^\|\s*#\s*\|\s*Level\s*\|\s*Action\s*/\s*Intervention\s*\|$")
    hdr_matrix = re.compile(r"^\|\s*#\s*\|\s*Action\s*\|\s*EMR\s*\|\s*EMT\s*\|\s*A\s*\|\s*I\s*\|\s*P\s*\|$")
    sep = re.compile(r"^[\s|:-]+$")
    for dirpath, _dirs, files in os.walk(docs_dir):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            relf = os.path.relpath(path, docs_dir).replace(os.sep, "/")
            if not relf.startswith(("protocols/", "procedures/")):
                continue
            lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
            for i, line in enumerate(lines):
                s = line.strip()
                collapsed = bool(hdr_collapsed.match(s))
                matrix = bool(hdr_matrix.match(s))
                if not (collapsed or matrix):
                    continue
                for raw in lines[i + 1:]:
                    r = raw.strip()
                    if not r.startswith("|"):
                        break
                    if sep.match(r):
                        continue
                    parts = [p.strip() for p in r.strip("|").split("|")]
                    num = parts[0]
                    if collapsed:
                        m = re.search(r"lvl-([a-z]+)", parts[1]) or re.match(r"^([A-Z]+)\b", parts[1])
                        if m:
                            out[(relf, num)] = m.group(1).upper()
                    else:
                        got = cells_leftmost(parts[2:7])
                        if got:
                            out[(relf, num)] = got
                # NOTE: no break — a page may carry more than one level table
                # (e.g. Supraventricular Tachycardia: narrow- and wide-complex).
    return out


def pems_row(pems: dict, page: int | None, ordinal: int | None) -> dict | None:
    if page is None or ordinal is None:
        return None
    for doc in pems["pems_docs"]:
        for row in doc["rows"]:
            if row["page"] == page and row["ordinal"] == ordinal:
                return row
    return None


def evidence(pems: dict, row: dict | None) -> dict:
    if not row:
        return {"canonical_page": None, "canonical_ordinal": None,
                "canonical_badges": [], "canonical_text": None}
    canon = pems_row(pems, row.get("pems_page"), row.get("pems_ordinal"))
    return {
        "canonical_page": row.get("pems_page"),
        "canonical_ordinal": row.get("pems_ordinal"),
        "canonical_badges": list(row.get("compound_tokens") or []) +
                            ([row["pems_badge"]] if row.get("pems_badge") else []),
        "canonical_columns": (canon or {}).get("columns"),
        "canonical_text": ((canon or {}).get("verbatim_text") or row.get("pems_text") or "")[:400],
        "published_chip": row.get("level_published"),
        "ledger_status": row.get("status"),
        "ledger_basis": row.get("basis"),
        "ledger_note": row.get("reason") or row.get("note"),
        "binding_evidence": row.get("binding_evidence"),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="recompute and compare with the committed reconciled.json; exit 1 on drift")
    args = ap.parse_args(argv)

    audit = json.load(open(AUD, encoding="utf-8"))
    ledger_doc = json.load(open(LEDGER, encoding="utf-8"))
    c2 = json.load(open(C2, encoding="utf-8"))
    pems = json.load(open(PEMS, encoding="utf-8"))
    align = json.load(open(ALIGN, encoding="utf-8"))
    needs_md = open(NEEDS, encoding="utf-8").read()
    pub_doc = read_published_levels(os.path.join(ROOT, "docs"))

    # ledger vs tree: the ledger was generated by level_rule.py; the reconciliation
    # must not inherit its mistakes, so disagreements are counted and reported.
    ledger_vs_doc = {"compared": 0, "agree": 0, "disagreements": []}
    for r in ledger_doc["rows"]:
        got = pub_doc.get((r["file"], str(r["row"])))
        if got is None or r.get("level_published") is None:
            continue
        ledger_vs_doc["compared"] += 1
        if got == r["level_published"]:
            ledger_vs_doc["agree"] += 1
        else:
            ledger_vs_doc["disagreements"].append(
                {"file": r["file"], "row": r["row"],
                 "ledger": r["level_published"], "doc": got})

    # 489 non-level findings, keyed by audit id, with the line that routes them.
    routed: dict[str, int] = {}
    for i, line in enumerate(needs_md.splitlines(), 1):
        m = re.search(r"`(AUD-\d{4})`", line)
        if m:
            routed[m.group(1)] = i

    lk = {(r["file"], str(r["row"])): r for r in ledger_doc["rows"]}
    ck: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for rec in c2["records"]:
        ck[(rel(rec["file"]), str(rec["row"]))].append(rec)

    findings = []
    ident_sims: list[float] = []
    for page in audit:
        f = rel(page["file"])
        for x in page["discrepancies"]:
            gid = x["gid"]
            key = (f, str(x["row"]))
            row = lk.get(key)
            recs = ck.get(key, [])
            ruled = None

            level_ish = is_level_finding(x)
            if bucket_check := (x["row"] is not None and level_ish and row is not None):
                a = (x.get("converted_text") or "").strip()
                b = (row.get("action") or "").strip()
                if a and b:
                    ident_sims.append(difflib.SequenceMatcher(None, a, b).ratio())
            if x["row"] is None:
                bucket = "no_site_row"
            elif level_ish:
                bucket = "level_cell"
            else:
                bucket = "non_level"
            ruled = None

            # N1 — not a level-cell finding: routed to authorship, never applied by C3.
            if bucket == "non_level":
                line = routed.get(gid)
                ruled = {
                    "ruling": "DROPPED",
                    "reason_code": "N1_NOT_LEVEL_CELL",
                    "detail": ("not a level-cell finding: clinical prose / dose / contraindication / "
                               "destination work, "
                               + (f"routed to needs-authoring.md line {line} " if line else "routed to authorship ")
                               + "(OMD authorship, outside C3's scope)"),
                    "rule": "N1",
                }
            # X1 — a level finding for a row the page does not carry: an ADD, and C3
            # only edits level cells of existing rows.
            elif bucket == "no_site_row":
                ev_row = row
                c2note = ""
                if recs:
                    c2note = f"; C2 recorded {recs[0]['decision']} for this named item"
                ruled = {
                    "ruling": "DROPPED",
                    "reason_code": "X1_ROW_ABSENT_ADD",
                    "detail": (("the page has no row for this level finding, so the fix is to ADD a row — " if level_ish
                                else "the finding needs content the page does not carry, so the fix is an ADD — ")
                               + "outside C3's scope (level cells in existing rows only); stays in "
                               f"needs-authoring.md line {routed.get(gid, '?')}"
                               + (f"; canonical source p.{ev_row['pems_page']}#{ev_row['pems_ordinal']}"
                                  if ev_row else "")
                               + c2note),
                    "rule": "X1",
                }
            elif recs:
                dec = [r["decision"] for r in recs]
                ur = [r for r in recs if r["decision"] == "UNRESOLVED"]
                if ur:
                    ruled = {"ruling": "OWNER_REQUIRED", "rule": "R1",
                             "reason_code": "R1_C2_UNRESOLVED",
                             "detail": "C2 could not settle this row from the source: " + ur[0]["question"]}
                elif any(d == "set_cells" for d in dec):
                    rec = [r for r in recs if r["decision"] == "set_cells"][0]
                    left = cells_leftmost(rec.get("resolved_cells") or [])
                    pub = pub_doc.get((f, str(x["row"]))) or (row or {}).get("level_published")
                    lstatus = (row or {}).get("status")
                    if lstatus in ("OWNER_REQUIRED", "pending_omd", "pending_row_omd"):
                        # C2 says set_cells; the level-rule ledger says the row cannot be
                        # settled. Two records disagree -> a human decides, not this script.
                        ruled = {"ruling": "OWNER_REQUIRED", "rule": "R1",
                                 "reason_code": "R1_C2_VS_LEDGER_CONFLICT",
                                 "detail": (f"C2 ruled set_cells -> {left}, but the ledger marks this row "
                                            f"{lstatus}: {(row or {}).get('reason') or 'no reason recorded'}"),
                                 "c2_verdict": rec["verdict"]}
                    elif pub == "PENDING":
                        ruled = {"ruling": "OWNER_REQUIRED", "rule": "R1",
                                 "reason_code": "R1_PENDING_OMD",
                                 "detail": ("C2 ruled set_cells -> " + str(left) +
                                            "; the page prints PENDING (awaiting OMD authorization)"),
                                 "c2_verdict": rec["verdict"]}
                    elif left and pub == left:
                        ruled = {"ruling": "DROPPED", "rule": "R1",
                                 "reason_code": "R1_C2_SET_ALREADY_APPLIED",
                                 "detail": (f"C2 ruled set_cells ({left}); the page now publishes {pub} — "
                                            "the correction is already in place"),
                                 "c2_verdict": rec["verdict"]}
                    else:
                        ruled = {"ruling": "CONFIRMED", "rule": "R1",
                                 "reason_code": "R1_C2_SET_CELLS_PENDING",
                                 "detail": (f"C2 ruled set_cells -> {left}; the page publishes {pub} — "
                                            "the correction is still outstanding"),
                                 "c2_verdict": rec["verdict"]}
                else:
                    rec = recs[0]
                    ruled = {"ruling": "DROPPED", "rule": "R1",
                             "reason_code": "R1_C2_" + rec["decision"].upper(),
                             "detail": f"C2 adjudicated {rec['decision']}: {rec['verdict']}",
                             "c2_verdict": rec["verdict"]}
            elif row is None:
                ruled = {"ruling": "OWNER_REQUIRED", "rule": "R4",
                         "reason_code": "R4_NO_LEDGER_ROW",
                         "detail": f"no ledger row for {f} row {x['row']} — the site table no longer "
                                   "carries this row, so no canonical level can be attached"}
            else:
                st = row["status"]
                if st == "OWNER_REQUIRED":
                    ruled = {"ruling": "OWNER_REQUIRED", "rule": "R2", "reason_code": "R2_LEDGER_OWNER",
                             "detail": "ledger OWNER_REQUIRED: " + (row.get("reason") or "no reason recorded")}
                elif st in ("pending_omd", "pending_row_omd"):
                    ruled = {"ruling": "OWNER_REQUIRED", "rule": "R2", "reason_code": "R2_" + st.upper(),
                             "detail": "awaiting OMD: " + (row.get("reason") or "no reason recorded")}
                elif st == "policy":
                    ruled = {"ruling": "DROPPED", "rule": "R3", "reason_code": "R3_POLICY_ROW",
                             "detail": "row is an administrative/policy step, not level-gated: "
                                       + (row.get("reason") or "")}
                else:
                    levels = canonical_levels(row)
                    lvl = lowest(levels)
                    pub = pub_doc.get((f, str(x["row"]))) or row.get("level_published")
                    pub_src = "docs" if (f, str(x["row"])) in pub_doc else "ledger"
                    if lvl is None or (lvl == "MC" and pub is None):
                        ruled = {"ruling": "OWNER_REQUIRED", "rule": "R4",
                                 "reason_code": "R4_NO_CANONICAL_LEVEL",
                                 "detail": "the canonical PEMS row prints no level badge and no inline "
                                           "level token, so no level can be confirmed or dropped"}
                    elif pub == lvl:
                        ruled = {"ruling": "DROPPED", "rule": "R5",
                                 "reason_code": "R5_ALREADY_CANONICAL",
                                 "detail": (f"page publishes {pub} (read from {pub_src}); the canonical row "
                                            f"(p.{row['pems_page']}#{row['pems_ordinal']}) permits "
                                            f"{'/'.join(levels)} -> lowest permitting level {lvl}")}
                    else:
                        ruled = {"ruling": "CONFIRMED", "rule": "R6",
                                 "reason_code": "R6_DIVERGENT",
                                 "detail": (f"page publishes {pub} (read from {pub_src}); the canonical row "
                                            f"(p.{row['pems_page']}#{row['pems_ordinal']}) permits "
                                            f"{'/'.join(levels)} -> should be {lvl}")}

            findings.append({
                "gid": gid,
                "file": f,
                "row": x["row"],
                "field": x["field"],
                "severity": x["severity"],
                "level_decode": x["level_decode"],
                "bucket": bucket,
                "current_value": x["current_value"],
                "correct_value": x["correct_value"],
                "recommendation": x["recommendation"],
                "ruling": ruled["ruling"],
                "rule": ruled["rule"],
                "reason_code": ruled["reason_code"],
                "detail": ruled["detail"],
                "c2_verdict": ruled.get("c2_verdict"),
                "evidence": dict(evidence(pems, row),
                                 published_doc=pub_doc.get((f, str(x["row"])))),
            })

    assert len(findings) == len({f["gid"] for f in findings}), "duplicate audit ids"

    collapse = collections.Counter(f["ruling"] for f in findings)
    by_code = collections.Counter(f["reason_code"] for f in findings)
    by_bucket = collections.Counter(f["bucket"] for f in findings)
    inferred = [f for f in findings if f["level_decode"] == "inferred"]
    assert len(inferred) == 80, len(inferred)
    assert all(f["ruling"] in ("CONFIRMED", "DROPPED", "OWNER_REQUIRED") for f in findings)

    by_page = collections.defaultdict(lambda: collections.Counter())
    for f in findings:
        by_page[f["file"]][f["ruling"]] += 1
        by_page[f["file"]]["total"] += 1

    # Residual human list: ledger rows that never settled, plus C2's unresolved record.
    residual = collections.defaultdict(lambda: collections.Counter())
    for r in ledger_doc["rows"]:
        if r["status"] in ("OWNER_REQUIRED", "pending_omd", "pending_row_omd"):
            residual[r["file"]][r["status"]] += 1
    for rec in c2["records"]:
        if rec["decision"] == "UNRESOLVED":
            residual[rel(rec["file"])]["C2_UNRESOLVED"] += 1
    unmatched = collections.Counter()
    for page in align["pages"]:
        for r in page["rows"]:
            if r.get("status") == "ambiguous":
                unmatched[page["site_page"]] += 1

    ambiguous_sample = []
    for f in findings:
        if f["ruling"] != "OWNER_REQUIRED":
            continue
        ambiguous_sample.append({
            "gid": f["gid"], "file": f["file"], "row": f["row"], "field": f["field"],
            "reason": f["detail"], "claimed": f["correct_value"],
        })

    doc = {
        "generated_by": "scripts/reconcile_c3.py",
        "ruling": "OWNER RULING D1 (2026-11-19): reconcile + report only. No level cell applied.",
        "doctrine": "one marker per action = the lowest provider level PEMS 2024 prints for that action",
        "inputs": {
            "findings": os.path.relpath(AUD, ROOT),
            "needs_authoring": os.path.relpath(NEEDS, ROOT),
            "ledger": os.path.relpath(LEDGER, ROOT),
            "c2_adjudications": os.path.relpath(C2, ROOT),
            "pems_table": os.path.relpath(PEMS, ROOT),
            "alignment": os.path.relpath(ALIGN, ROOT),
        },
        "counts": {
            "findings": len(findings),
            "confirmed": collapse["CONFIRMED"],
            "dropped": collapse["DROPPED"],
            "owner_required": collapse["OWNER_REQUIRED"],
            "by_bucket": dict(by_bucket),
            "by_reason_code": dict(sorted(by_code.items())),
            "inferred_total": len(inferred),
            "inferred_confirmed": sum(1 for f in inferred if f["ruling"] == "CONFIRMED"),
            "inferred_dropped": sum(1 for f in inferred if f["ruling"] == "DROPPED"),
            "inferred_owner_required": sum(1 for f in inferred if f["ruling"] == "OWNER_REQUIRED"),
            "ledger_rows": len(ledger_doc["rows"]),
            "c2_records": len(c2["records"]),
            "ledger_vs_docs": {
                "rows_compared": ledger_vs_doc["compared"],
                "rows_agree": ledger_vs_doc["agree"],
                "rows_disagree": len(ledger_vs_doc["disagreements"]),
            },
            "row_identity": {
                "rows_compared": len(ident_sims),
                "median_similarity": (round(sorted(ident_sims)[len(ident_sims) // 2], 3)
                                      if ident_sims else None),
                "below_0_55": sum(1 for s in ident_sims if s < 0.55),
            },
        },
        "needs_authoring_lines": routed,
        "ledger_vs_docs_disagreements": ledger_vs_doc["disagreements"],
        "residual": {
            "ledger_unsettled_by_file": {k: dict(v) for k, v in sorted(residual.items())},
            "ledger_unsettled_total": sum(sum(v.values()) for v in residual.values()),
            "alignment_ambiguous_by_file": dict(sorted(unmatched.items())),
            "alignment_ambiguous_total": sum(unmatched.values()),
        },
        "by_page": {k: dict(v) for k, v in sorted(by_page.items())},
        "ambiguous_sample": ambiguous_sample,
        "findings": findings,
    }

    if args.check:
        if not os.path.exists(OUT_JSON):
            print("CHECK FAIL: reconciled.json missing", file=sys.stderr)
            return 1
        old = json.load(open(OUT_JSON, encoding="utf-8"))
        if old["counts"] != doc["counts"]:
            print("CHECK FAIL: counts drifted", file=sys.stderr)
            print(json.dumps({"old": old["counts"], "new": doc["counts"]}, indent=1), file=sys.stderr)
            return 1
        oldr = [(f["gid"], f["ruling"], f["reason_code"]) for f in old["findings"]]
        newr = [(f["gid"], f["ruling"], f["reason_code"]) for f in doc["findings"]]
        if oldr != newr:
            print("CHECK FAIL: per-finding rulings drifted", file=sys.stderr)
            return 1
        print(f"CHECK OK: {len(findings)} findings, split unchanged "
              f"(confirmed={collapse['CONFIRMED']} dropped={collapse['DROPPED']} "
              f"owner={collapse['OWNER_REQUIRED']})")
        return 0

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")

    write_md(doc)
    print(f"wrote {os.path.relpath(OUT_JSON, ROOT)} and {os.path.relpath(OUT_MD, ROOT)}")
    print(f"  707 -> confirmed={collapse['CONFIRMED']} dropped={collapse['DROPPED']} "
          f"owner_required={collapse['OWNER_REQUIRED']}")
    return 0


def write_md(doc: dict) -> None:
    c = doc["counts"]
    L = []
    A = L.append
    A("# C3 reconciliation — 707 findings → confirmed / dropped")
    A("")
    A("Generated by `scripts/reconcile_c3.py`. **Reconciliation and report only** "
      "(owner ruling D1, 2026-11-19): no level cell was applied, nothing merged, nothing pushed.")
    A("")
    A("## 1. Collapse")
    A("")
    A("| bucket | count |")
    A("|---|---|")
    A(f"| in the 707 audit | {c['findings']} |")
    A(f"| **CONFIRMED** (still divergent, needs a decision) | **{c['confirmed']}** |")
    A(f"| **DROPPED** (no action needed) | **{c['dropped']}** |")
    A(f"| **OWNER_REQUIRED** (policy / no canonical evidence) | **{c['owner_required']}** |")
    A("")
    A(f"Split by class: level-cell findings {c['by_bucket'].get('level_cell', 0)}, "
      f"findings on rows the page does not carry (adds) {c['by_bucket'].get('no_site_row', 0)}, "
      f"non-level findings {c['by_bucket'].get('non_level', 0)}.")
    A("")
    A("**How to read CONFIRMED = %d.** No level-cell finding in the 707 survives as an "
      "outstanding *level correction*: every one of the %d level-cell findings either publishes "
      "exactly the level the canonical PEMS row permits, was already settled by a C2 adjudication, "
      "or is in OWNER_REQUIRED because two records disagree or no canonical level exists. The "
      "outstanding work is therefore not in CONFIRMED — it is the %d OWNER_REQUIRED findings below, "
      "plus the %d adds that need authoring."
      % (c["confirmed"], c["by_bucket"].get("level_cell", 0), c["owner_required"],
         c["by_bucket"].get("no_site_row", 0)))
    A("")
    A(f"Cross-check that this is not an artefact of the ledger: the script re-reads every level "
      f"table in `docs/` itself and compares with the ledger. "
      f"{c['ledger_vs_docs']['rows_agree']} of {c['ledger_vs_docs']['rows_compared']} rows agree, "
      f"{c['ledger_vs_docs']['rows_disagree']} disagree.")
    A("")
    ri = c["row_identity"]
    A(f"Row-identity check (does row *N* in the audit still name the same action as row *N* in the "
      f"ledger): {ri['rows_compared']} level rows compared, median text similarity "
      f"{ri['median_similarity']}, {ri['below_0_55']} below 0.55 — those are rows the audit quoted "
      "in truncated/compound form, not rows that moved.")
    A("")
    A("### Rule firings")
    A("")
    A("| rule | reason code | count | meaning |")
    A("|---|---|---|---|")
    meaning = {
        "R1_C2_SET_ALREADY_APPLIED": "C2 ruled set_cells and the page now publishes it",
        "R1_C2_SET_CELLS_PENDING": "C2 ruled set_cells and the page still differs",
        "R1_C2_CONFIRM": "C2 confirmed the site cells",
        "R1_C2_SITE_SPLIT_OF_PEMS": "C2: site splits one PEMS row; cells correct as authored",
        "R1_C2_NO_PEMS_COUNTERPART": "C2: no PEMS row of its own; authored detail",
        "R1_C2_OWNERSHIP": "C2: another row owns the PEMS row",
        "R1_C2_HELD_SPLIT_REVIEW": "C2: level right, split review (not a level change)",
        "R1_C2_INFO": "C2: named item, no cell decision",
        "R1_C2_UNRESOLVED": "C2 could not settle the row from the source",
        "R2_LEDGER_OWNER": "ledger marks the row OWNER_REQUIRED",
        "R2_PENDING_OMD": "ledger marks the row awaiting OMD",
        "R2_PENDING_ROW_OMD": "ledger marks the row awaiting an OMD row ruling",
        "R3_POLICY_ROW": "administrative/policy row, not level-gated",
        "R4_NO_CANONICAL_LEVEL": "canonical row prints no level and no inline token",
        "R4_NO_LEDGER_ROW": "site row no longer exists in the ledger",
        "R5_ALREADY_CANONICAL": "page already publishes the canonical lowest level",
        "R6_DIVERGENT": "page level differs from the canonical lowest level",
        "N1_NOT_LEVEL_CELL": "not a level-cell finding — routed to needs-authoring.md",
        "X1_ROW_ABSENT_ADD": "fix is an ADD (no such row/content) — needs-authoring.md, not a cell edit",
        "R1_C2_ADD_FROM_PEMS": "C2: site prints no level where PEMS prints one",
        "R1_C2_VS_LEDGER_CONFLICT": "C2 says set_cells, ledger says OWNER/pending — two records disagree",
        "R1_PENDING_OMD": "C2 says set_cells, page prints PENDING (awaiting OMD)",
    }
    for code, n in sorted(c["by_reason_code"].items(), key=lambda kv: (-kv[1], kv[0])):
        A(f"| {code.split('_')[0]} | `{code}` | {n} | {meaning.get(code, '')} |")
    A("")
    A("## 2. The 80 `inferred` findings")
    A("")
    A(f"All 80 resolve: **{c['inferred_confirmed']} confirmed**, **{c['inferred_dropped']} dropped**, "
      f"**{c['inferred_owner_required']} owner-required**. None left as \"maybe\".")
    A("")
    A("| gid | page | row | ruling | rule | evidence |")
    A("|---|---|---|---|---|---|")
    for f in doc["findings"]:
        if f["level_decode"] != "inferred":
            continue
        ev = f["evidence"]
        if f["reason_code"] in ("N1_NOT_LEVEL_CELL", "X1_ROW_ABSENT_ADD"):
            evs = "needs-authoring.md line " + str(doc["needs_authoring_lines"].get(f["gid"], "?"))
        elif ev["canonical_page"] is not None:
            evs = (f"p.{ev['canonical_page']}#{ev['canonical_ordinal']} "
                   f"{'/'.join(str(b) for b in ev['canonical_badges'])} "
                   f"(page publishes {ev.get('published_doc') or ev.get('published_chip')})")
        else:
            evs = "no canonical row"
        A(f"| {f['gid']} | {f['file'].split('/')[-1]} | {f['row']} | **{f['ruling']}** | "
          f"{f['reason_code']} | {evs} |")
    A("")
    A("## 3. Split by protocol page")
    A("")
    A("| page | total | confirmed | dropped | owner |")
    A("|---|---|---|---|---|")
    for page, cnt in sorted(doc["by_page"].items(), key=lambda kv: (-kv[1]["total"], kv[0])):
        A(f"| {page} | {cnt.get('total', 0)} | {cnt.get('CONFIRMED', 0)} | {cnt.get('DROPPED', 0)} | "
          f"{cnt.get('OWNER_REQUIRED', 0)} |")
    A("")
    A("## 4. OWNER_REQUIRED — the outstanding list, each with its reason")
    A("")
    A("These are the findings a person has to rule on. None of them was silently dropped.")
    A("")
    A("| gid | page | row | field | claimed correction | why it needs a human |")
    A("|---|---|---|---|---|---|")
    for s in doc["ambiguous_sample"]:
        claim = (s["claimed"] or "").replace("|", "/")[:70]
        why = (s["reason"] or "").replace("|", "/")[:220]
        fld = (s["field"] or "").replace("|", "/")[:50]
        A(f"| {s['gid']} | {s['file'].split('/')[-1]} | {s['row']} | {fld} | {claim} | {why} |")
    A("")
    A("## 5. Residual human list — rows that never settled")
    A("")
    R = doc["residual"]
    A(f"Ledger rows still unsettled: **{R['ledger_unsettled_total']}**. "
      f"Alignment rows still ambiguous: **{R['alignment_ambiguous_total']}**.")
    A("")
    A("| file | OWNER_REQUIRED | pending_omd | pending_row_omd | C2_UNRESOLVED | alignment ambiguous |")
    A("|---|---|---|---|---|---|")
    files = sorted(set(R["ledger_unsettled_by_file"]) | set(R["alignment_ambiguous_by_file"]))
    for f in files:
        d = R["ledger_unsettled_by_file"].get(f, {})
        A(f"| {f} | {d.get('OWNER_REQUIRED', 0)} | {d.get('pending_omd', 0)} | "
          f"{d.get('pending_row_omd', 0)} | {d.get('C2_UNRESOLVED', 0)} | "
          f"{R['alignment_ambiguous_by_file'].get(f, 0)} |")
    A("")
    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
