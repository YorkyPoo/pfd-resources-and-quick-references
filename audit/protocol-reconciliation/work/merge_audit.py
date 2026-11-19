#!/usr/bin/env python3
"""Mechanical merge of the 11 batch audit outputs into the three deliverables.

Re-runnable:
    python3 audit/protocol-reconciliation/work/merge_audit.py            # rebuild
    python3 audit/protocol-reconciliation/work/merge_audit.py --verify   # rebuild + verify

Inputs  (read only): audit/protocol-reconciliation/work/batch-{A1..M1}.{json,md,fixlist.md}
Outputs (write only):
    audit/protocol-reconciliation/AUDIT-2026-11-14.json
    audit/protocol-reconciliation/AUDIT-2026-11-14.md
    audit/protocol-reconciliation/FIXLIST.md

No clinical judgement beyond the parent rulings R-1..R-6, which are applied through the explicit
match table RULES/OWNER below (one reviewed rule per gid, asserted unique).
Does not touch docs/, scripts/, or pre-existing audit artifacts.
"""
import collections
import glob
import json
import os
import re
import sys

REPO = "/root/projects/pfd-resources-and-quick-references"
WORK = os.path.join(REPO, "audit/protocol-reconciliation/work")
OUT = os.path.join(REPO, "audit/protocol-reconciliation")
BATCHES = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "F1", "F2", "M1"]
EXPECT = {"A1": 64, "A2": 40, "B1": 74, "B2": 64, "C1": 65, "C2": 42,
          "D1": 75, "D2": 101, "F1": 35, "F2": 55, "M1": 92}
EXPECT_TOTAL = 707
EXPECT_SEV = {"CRITICAL": 201, "MODERATE": 416, "MINOR": 90}
SEV_RANK = {"CRITICAL": 0, "MODERATE": 1, "MINOR": 2}
DATE = "2026-11-14"

JSON_OUT = os.path.join(OUT, "AUDIT-2026-11-14.json")
MD_OUT = os.path.join(OUT, "AUDIT-2026-11-14.md")
FIX_OUT = os.path.join(OUT, "FIXLIST.md")


# --------------------------------------------------------------------------- inputs
def load_batches():
    protos = []
    per_batch = {}
    for b in BATCHES:
        with open(os.path.join(WORK, "batch-%s.json" % b), encoding="utf-8") as fh:
            data = json.load(fh)
        n = sum(len(p["discrepancies"]) for p in data)
        if n != EXPECT[b]:
            sys.exit("COUNT MISMATCH batch %s: got %d expected %d" % (b, n, EXPECT[b]))
        per_batch[b] = n
        for p in data:
            p["_batch"] = b
            for d in p["discrepancies"]:
                d["_batch"] = b
                d["_file"] = p["file"]
                d["_protocol"] = p["protocol"]
            protos.append(p)
    total = sum(per_batch.values())
    if total != EXPECT_TOTAL:
        sys.exit("TOTAL MISMATCH: got %d expected %d" % (total, EXPECT_TOTAL))
    return protos, per_batch


def norm_row(v):
    if v is None:
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if s.lower() in ("", "none", "null", "absent", "-"):
        return None
    m = re.match(r"^-?\d+", s)
    return int(m.group()) if m else None


# --------------------------------------------------------------------------- rulings
# (ruling, batch, batch_id, file substring, row, field substring, basis)
RULES = [
    ("R-1", "A1", "A1-13", "04_Cardiac_Arrest_Non_Traumatic", 10, "Fluid Administration",
     'PEMS "A A Administer: ADULT: 0.9% Sodium Chloride IV/IO up to 1 L in 250 - 500 mL boluses"; '
     "site narrows the NS bolus to I. Arrest/post-ROSC fluid is listed in R-1."),
    ("R-1", "A1", "A1-45", "04_V_Fib_Pulseless_V_Tach", 4, "Fluid resuscitation",
     'PEMS "A A Administer: ADULT: 0.9% Sodium Chloride IV/IO up to 1 L in 250 - 500 mL boluses"; '
     "site narrows the NS bolus to I."),
    ("R-1", "A2", "A2-06", "04_Post_Resuscitation_Care", 5, "Provider Level (A)",
     'PEMS "A A Consider: ADULT: 0.9% Sodium chloride up to 1 L IV/IO in 250 - 500 mL boluses"; '
     "post-ROSC volume for hypotension (listed in R-1); site narrows to I."),
    ("R-1", "A2", "A2-19", "04_Cardiac_Arrest_Traumatic", 7, "saline bolus",
     'PEMS "If blood products are not available, administer: ADULT: 0.9% Sodium chloride up to 1 L '
     'IV/IO in 250 - 500 mL boluses"; trauma/haemorrhage is listed in R-1; site narrows to I.'),
    ("R-1", "C2", "C2-08", "03_Smoke_Inhalation", 11, "IV fluid",
     'PEMS "A For an adult patient with SBP less than 90 and TBSA greater than 20%, administer: '
     'ADULT: 0.9% Sodium chloride at 500 mL/hr"; hypotension + burns, both listed in R-1; site I+.'),
    ("R-1", "M1", "M1-AL-09", "07_Allergic_Reaction_Anaphylaxis", 9, "Provider Level",
     'PEMS "A A If the patient is hypotensive, administer: ADULT: 0.9% Sodium Chloride up to 1 L '
     'IV/IO in 250 - 500 mL boluses"; the allergic fluid bolus named in the card; site I+.'),
    ("R-2", "B1", "HYP-04", "07_Hypotension_Shock_Non_Trauma", 4, "12-lead ECG",
     'PEMS "EMR EMT Obtain and transmit a 12-Lead ECG"; site A/I/P only. Named in the card.'),
    ("R-2", "A2", "A2-04", "04_Post_Resuscitation_Care", 3, "Provider Level (EMT)",
     'PEMS "EMT Obtain and transmit a 12-Lead ECG"; site A+ only.'),
    ("R-2", "A2", "A2-28", "04_Supraventricular_Tachycardia", 4, "12-lead ECG",
     'PEMS "EMT Obtain and transmit a 12-Lead ECG"; site A+ only.'),
    ("R-2", "B2", "B2-OD-06", "06_Overdose_Poisoning", 4, "Provider Level",
     'PEMS "EMT Obtain and transmit a 12-Lead ECG" (glucose + ECG row); site A+ only.'),
    ("R-2", "D2", "D2-EL-07", "09_Electrical_Injuries", 7, "Provider Level",
     'PEMS "EMT Obtain and transmit a 12-Lead ECG"; site A+ only.'),
    ("R-2", "D2", "D2-LT-07", "09_Lightning_Injuries", 7, "Provider Level",
     'PEMS "EMT Obtain and transmit a 12-Lead ECG"; site A+ only.'),
    ("R-2", "M1", "M1-BR-05", "04_Bradycardia", None, "12-lead ECG",
     'PEMS "EMR EMT Obtain and transmit a 12-Lead ECG"; the row is missing from the site entirely.'),
    ("R-3", "D2", "D2-HC-07", "09_Hemorrhage_Control", 4, "Missing step",
     'PEMS "If tourniquet(s) are not controlling bleeding continuously maintain direct pressure to '
     'wound over packing" - an EMR bleeding-control step missing from the site.'),
]

# R-6 owner-decision items named in the card: (batch, batch_id, file substring or None)
OWNER = [
    ("C1", "C1-05", None), ("C1", "C1-06", None),                        # RD row 6 CPAP MC
    ("C1", "C1-27", None), ("C1", "C1-28", None), ("C1", "C1-29", None),  # asthma row 8 CPAP MC
    ("C1", "C1-04", None),                                              # COPD O2 88-92% target
    ("C1", "C1-15", None),                                              # nitro PDE-5 (respiratory)
    ("C2", "C2-08", "03_Pulmonary_Edema_Congestion"),                    # nitro PDE-5 (pulm edema)
    ("M1", "M1-CP-24", None),                                           # nitro PDE-5 (chest pain)
]


# Reviewed recommendation text overrides keyed by (batch, batch id, file substring).
# AUD-0092 (HYP-04) carried stale pre-ruling text ("Rated MODERATE ... parent to reconcile");
# the published recommendation must state the R-2 outcome only.
REC_OVERRIDES = {
    ("B1", "HYP-04", "07_Hypotension_Shock_Non_Trauma"):
        "Set EMT cell to • on row 4 (EMT 12-lead ECG, ruling R-2).",
}


def recommendation(d):
    """Return the reviewed recommendation text for a finding (override or batch text)."""
    for (batch, bid, fsub), text in REC_OVERRIDES.items():
        if d["_batch"] == batch and d["id"] == bid and fsub in d["_file"]:
            return text
    return d.get("recommendation")


def classify(protos):
    """Attach gid, ruling upgrade and owner flag. Returns flat list + changes."""
    flat = [d for p in protos for d in p["discrepancies"]]
    for d in flat:
        d["row"] = norm_row(d.get("row"))
        if d["severity"] not in SEV_RANK:
            sys.exit("BAD SEVERITY %r in %s %s" % (d["severity"], d["_file"], d["id"]))
        d["_ruling"] = None
        d["_owner"] = False

    for (ruling, batch, bid, fsub, row, fsub2, basis) in RULES:
        hits = [d for d in flat
                if d["_batch"] == batch and d["id"] == bid and fsub in d["_file"]
                and d["row"] == row and fsub2 in (d.get("field") or "")]
        if len(hits) != 1:
            sys.exit("RULE %s/%s/%s/%s matched %d records (need exactly 1)"
                     % (ruling, batch, bid, fsub, len(hits)))
        hits[0]["_ruling"] = ruling
        hits[0]["_basis"] = basis

    for (batch, bid, fsub) in OWNER:
        hits = [d for d in flat if d["_batch"] == batch and d["id"] == bid
                and (fsub is None or fsub in d["_file"])]
        if len(hits) != 1:
            sys.exit("OWNER %s/%s matched %d records" % (batch, bid, len(hits)))
        hits[0]["_owner"] = True

    def key(d):
        return (SEV_RANK[d["severity"]], d["_file"], d["row"] is None, d["row"] or 0,
                d["_batch"], d["id"], d.get("field") or "")

    flat.sort(key=key)
    for i, d in enumerate(flat, 1):
        d["gid"] = "AUD-%04d" % i
    pre = {id(d): d["gid"] for d in flat}

    changes = []
    for d in flat:
        if d["_ruling"] and d["severity"] != "CRITICAL":
            changes.append({"gid": d["gid"], "batch_id": d["id"], "batch": d["_batch"],
                            "file": d["_file"], "row": d["row"], "field": d.get("field"),
                            "ruling": d["_ruling"], "before": d["severity"], "after": "CRITICAL",
                            "basis": d["_basis"]})
            d["severity"] = "CRITICAL"
    # severity changed -> ordering can change; re-sort + renumber so that the published id
    # sequence really is (final severity, file, row).
    flat.sort(key=key)
    for i, d in enumerate(flat, 1):
        d["gid"] = "AUD-%04d" % i
    for c in changes:
        for d in flat:
            if (d["_batch"] == c["batch"] and d["id"] == c["batch_id"]
                    and d["_file"] == c["file"]):
                c["gid"] = d["gid"]
                break
    return flat, changes


# --------------------------------------------------------------------------- emit helpers
def clean(text, limit=None):
    """One-line pipe-safe cell text. Quotes themselves are untouched."""
    s = "" if text is None else str(text)
    s = re.sub(r"\s+", " ", s.replace("\r", " ").replace("\n", " ")).strip()
    s = s.replace("|", "\\|")
    if limit and len(s) > limit:
        s = s[: limit - 1].rstrip() + "..."
    return s


def q(text):
    """Quoted value for the FIXLIST: verbatim except pipes/newlines (kept one line)."""
    s = "" if text is None else str(text)
    s = re.sub(r"\s+", " ", s.replace("\r", " ").replace("\n", " ")).strip()
    return s.replace("|", "/")


def disk_pages():
    return sorted(os.path.relpath(p, REPO) for p in
                  glob.glob(os.path.join(REPO, "docs/protocols/**/*.md"), recursive=True))


# --------------------------------------------------------------------------- outputs
def build_json(flat, protos):
    by_file = collections.OrderedDict()
    for p in protos:
        if p["file"] in by_file:
            sys.exit("file audited by two batches: %s" % p["file"])
        by_file[p["file"]] = {"protocol": p["protocol"], "pems_pages": p["pems_pages"],
                              "status": p["status"],
                              "missing_sections": list(p.get("missing_sections") or []),
                              "verified": p.get("verified"), "notes": p.get("notes") or ""}
    per_file = collections.defaultdict(list)
    for d in flat:
        per_file[d["_file"]].append({
            "gid": d["gid"], "batch_id": d["id"], "row": d["row"],
            "field": d.get("field"), "pems_original": d.get("pems_original"),
            "converted_text": d.get("converted_text"), "current_value": d.get("current_value"),
            "correct_value": d.get("correct_value"), "level_decode": d.get("level_decode"),
            "severity": d["severity"], "recommendation": recommendation(d),
            "owner_question": bool(d["_owner"]),
        })
    out = []
    for f in sorted(by_file):
        e = by_file[f]
        out.append({"protocol": e["protocol"], "file": f, "pems_pages": e["pems_pages"],
                    "status": e["status"], "discrepancies": per_file.get(f, []),
                    "missing_sections": e["missing_sections"], "verified": e["verified"],
                    "notes": e["notes"]})
    have = {e["file"] for e in out}
    for f in disk_pages():
        if f in have:
            continue
        out.append({"protocol": None, "file": f, "pems_pages": None, "status": "MANUAL",
                    "discrepancies": [], "missing_sections": [], "verified": False,
                    "notes": "NOT AUDITED - front-matter page with no PEMS protocol equivalent; "
                             "not assigned to any audit batch and contains no level-gated "
                             "protocol rows."})
    with open(JSON_OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return out


def build_md(flat, changes, objects, per_batch):
    sev = collections.Counter(d["severity"] for d in flat)
    by_file = collections.defaultdict(list)
    for d in flat:
        by_file[d["_file"]].append(d)
    obj_by_file = {o["file"]: o for o in objects}
    inf = sum(1 for d in flat if d.get("level_decode") == "inferred")
    own = sum(1 for d in flat if d["_owner"])
    pages = disk_pages()
    names_on_disk = set(pages)

    L = []
    A = L.append
    A("# AUDIT-2026-11-14 — PEMS2024 Regional Patient Care Protocols vs published site")
    A("")
    A("**Generated:** %s · **Generator:** `audit/protocol-reconciliation/work/merge_audit.py` "
      "(re-runnable) · **Method:** `audit/protocol-reconciliation/work/00_method_and_notes.md`" % DATE)
    A("")
    A("## Scope and method")
    A("")
    A("Every protocol page under `docs/protocols/**/*.md` (%d pages found by "
      "`find docs/protocols -name '*.md'`) was audited row by row against the flattened PEMS2024 "
      "text (`pems_chunks/PEMS2024_full.txt`) in 11 batches (A1, A2, B1, B2, C1, C2, D1, D2, F1, "
      "F2, M1). This document is a mechanical consolidation of those batch outputs: quotes are "
      "copied verbatim from the batch JSON/MD, no protocol was edited, and no clinical judgement "
      "was added beyond the binding severity rulings R-1..R-6 below. PEMS level codes were decoded "
      "from flattened PDF text per the method note; findings marked `inferred` must be confirmed "
      "against `PEMS2024.pdf` before any edit." % len(pages))
    A("")
    A("## Totals by severity (AFTER rulings R-1..R-3)")
    A("")
    A("| Severity | Findings |")
    A("|---|---:|")
    for s in ("CRITICAL", "MODERATE", "MINOR"):
        A("| %s | %d |" % (s, sev[s]))
    A("| **Total** | **%d** |" % len(flat))
    A("")
    A("Batch totals as delivered: " + ", ".join("%s %d" % (b, per_batch[b]) for b in BATCHES) +
      " = %d. Before rulings the batches carried CRITICAL %d / MODERATE %d / MINOR %d; "
      "R-1..R-3 moved **%d** findings from MODERATE to CRITICAL, giving CRITICAL %d / MODERATE %d "
      "/ MINOR %d." % (EXPECT_TOTAL, EXPECT_SEV["CRITICAL"], EXPECT_SEV["MODERATE"],
                       EXPECT_SEV["MINOR"], len(changes), sev["CRITICAL"], sev["MODERATE"],
                       sev["MINOR"]))
    A("")
    A("Flagged but not re-rated: %d findings carry `level_decode: inferred` (level decoded from "
      "split level tokens in the flattened text) and need a human PDF check before the edit; %d "
      "findings carry an `[OWNER]` decision marker (R-6)." % (inf, own))
    A("")
    A("## Severity rulings applied (parent decision, task t_d3600e06)")
    A("")
    A("| Rule | Ruling | Findings changed |")
    A("|---|---|---:|")
    A("| R-1 | IV/IO fluid bolus for hypotension/shock: any NS/LR fluid-bolus row whose PEMS "
      "indication is hypotension/shock (anaphylaxis, sepsis, burns, heat, haemorrhage, trauma, "
      "electrical, lightning, crush, cardiac arrest/post-ROSC) and whose site level is narrower "
      "than PEMS → CRITICAL. IV/IO access-only rows keep their batch rating. | %d |"
      % sum(1 for c in changes if c["ruling"] == "R-1"))
    A("| R-2 | 12-lead ECG at EMT: any site row for a PEMS EMT-level 12-lead ECG that is narrowed "
      "(A/I/P or blank) or missing → CRITICAL in every protocol. | %d |"
      % sum(1 for c in changes if c["ruling"] == "R-2"))
    A("| R-3 | EMR-level life-saving steps: CPR / chest compressions (adult and paediatric), "
      "AED / defibrillation pad application and bleeding control for PEMS EMR rows that are "
      "narrowed or missing → CRITICAL. | %d |"
      % sum(1 for c in changes if c["ruling"] == "R-3"))
    A("| R-4 | Everything else keeps the batch-assigned severity — nothing outside R-1..R-3 was "
      "re-rated. | 0 |")
    A("| R-5 | `level_decode: inferred` findings keep their batch severity — flagged, not "
      "downgraded. | 0 |")
    A("| R-6 | Owner-decision items keep their batch severity and get `[OWNER]` in FIXLIST.md. | "
      "0 (flag only) |")
    A("")
    A("### Every gid changed by R-1..R-3 (before → after)")
    A("")
    A("| batch id | gid | file | row | field | change | rule | basis (PEMS indication) |")
    A("|---|---|---|---:|---|---|---|---|")
    for c in sorted(changes, key=lambda c: (c["ruling"], c["gid"])):
        A("| %s | `%s` | `%s` | %s | %s | %s → **%s** | %s | %s |"
          % (c["batch_id"], c["gid"], c["file"], "absent" if c["row"] is None else c["row"],
             clean(c["field"], 60), c["before"], c["after"], c["ruling"], clean(c["basis"])))
    A("")
    A("Items named in the card that were **already CRITICAL** in their batch (no change needed): "
      "`M1-BR-03` (EMR paediatric compressions — the card's F-BR-03), `M1-CP-05` (chest-pain "
      "12-lead ECG), `F2-46` (Universal Patient Care 12-lead ECG), `C1-15` / `C2-08` (pulmonary "
      "edema) / `M1-CP-24` (nitroglycerin PDE-5 contraindication), `M1-AL-07` (EMT IM "
      "epinephrine). Fluid-bolus rows whose PEMS indication is not hypotension/shock (SVT "
      "`A2-30`, hyperglycaemia `M1-HG-05`) and IV/IO access-only rows (`D2-TR-06`) were left at "
      "their batch severity, per R-1.")
    A("")
    A("## Coverage table")
    A("")
    A("| # | Protocol page | Status | Findings | Audited | Coverage note |")
    A("|---:|---|---|---:|---|---|")
    for i, f in enumerate(pages, 1):
        o = obj_by_file.get(f)
        n = len(by_file.get(f, []))
        if o is None:
            A("| %d | `%s` | MANUAL | 0 | no | not covered by any batch |" % (i, f))
            continue
        audited = "yes" if o["status"] in ("VERIFIED", "FIXABLE") else "partial (MANUAL)"
        A("| %d | `%s` | %s | %d | %s | %s |" % (i, f, o["status"], n, audited,
                                                 clean(o["notes"], 220)))
    A("")
    unaudited = [f for f in pages
                 if f not in obj_by_file
                 or str(obj_by_file[f].get("notes") or "").startswith("NOT AUDITED")]
    A("Pages on disk but not audited by any batch (marked MANUAL above; reason: front-matter "
      "pages with no PEMS protocol equivalent and no level-gated rows): " +
      ", ".join("`%s`" % f for f in unaudited) + ".")
    A("")
    A("MANUAL protocol pages (audited against adjacent PEMS procedure text only — not a full "
      "protocol comparison; see each `notes` field): " +
      ", ".join("`%s`" % o["file"] for o in objects
                if o["status"] == "MANUAL" and o["file"] in by_file) + ".")
    A("")
    A("## Findings by protocol")
    A("")
    for f in pages:
        o = obj_by_file.get(f)
        A("## %s" % f)
        A("")
        if o is None:
            A("Not audited — not assigned to any batch. Reason: front-matter page with no PEMS "
              "protocol equivalent and no level-gated protocol rows.")
            A("")
            continue
        rows = by_file.get(f, [])
        A("PEMS: %s · status **%s** · verified `%s` · %d findings."
          % (o["pems_pages"], o["status"], str(o["verified"]).lower(), len(rows)))
        A("")
        if o["notes"]:
            A("Coverage note: %s" % clean(o["notes"]))
            A("")
        if o["missing_sections"]:
            A("Missing sections: " +
              "; ".join("`%s`" % clean(m, 300) for m in o["missing_sections"]))
            A("")
        if not rows:
            if o["status"] == "MANUAL":
                A("No discrepancies recorded — status **MANUAL**: this page was not compared "
                  "against a full PEMS protocol (see coverage note), so it is NOT verified.")
            else:
                A("No discrepancies — VERIFIED.")
            A("")
            continue
        A("| ID | Batch | Row | Field | PEMS source (exact quote) | Converted (exact quote) "
          "| Severity | Required fix |")
        A("|---|---|---:|---|---|---|---|---|")
        for d in rows:
            A("| %s | %s | %s | %s | %s | %s | %s | %s |"
              % (d["gid"], d["id"],
                 "absent" if d["row"] is None else d["row"], clean(d.get("field")),
                 clean(d.get("pems_original")), clean(d.get("converted_text")),
                 d["severity"], clean(recommendation(d))))
        A("")
    A("## Count reconciliation")
    A("")
    md_rows = sum(1 for line in L if line.startswith("| AUD-"))
    A("| Quantity | Count |")
    A("|---|---:|")
    A("| Findings in AUDIT-2026-11-14.json (sum of `discrepancies`) | %d |" % len(flat))
    A("| Finding table rows in this document (`^| AUD-`) | %d |" % md_rows)
    A("| Lines in FIXLIST.md (`^- [`) | %d |" % len(flat))
    A("| Protocol objects in the JSON = pages found on disk | %d |" % len(pages))
    A("| CRITICAL + MODERATE + MINOR | %d |" % sum(sev.values()))
    A("")
    A("All three deliverable counts are **%d**, the severity breakdown sums to the same number, "
      "and `merge_audit.py --verify` re-checks this after every run." % len(flat))
    A("")
    with open(MD_OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def build_fixlist(flat, changes):
    # Resolve "see <batch-id>" cross-references in the edit text to the global gid so that every
    # line is traceable inside this file alone (batch ids are not unique across the 11 batches).
    by_bid = collections.defaultdict(list)
    by_gid = {}
    for d in flat:
        by_bid[d["id"]].append(d)
        by_gid[d["gid"]] = d
    ref_re = re.compile(r"\b((?:A1|A2|B1|B2|C1|C2|D1|D2|F1|F2|M1)-[A-Za-z]*-?\d+)\b")
    gid_ref_re = re.compile(r"see (AUD-\d{4})")

    def fix_gid_refs(text):
        """Replace 'see AUD-####' with the target row and file so each line stands alone."""
        if not text:
            return text

        def sub(m):
            target = by_gid.get(m.group(1))
            if target is None:
                return m.group(0)
            row = "absent" if target["row"] is None else target["row"]
            return "see row %s, %s" % (row, target["_file"])

        return gid_ref_re.sub(sub, str(text))

    def fix_refs(text, d):
        if not text:
            return text
        def sub(m):
            bid = m.group(1)
            cands = by_bid.get(bid)
            if not cands:
                return bid
            same = [c for c in cands if c["_file"] == d["_file"]]
            pick = same[0] if len(same) == 1 else (cands[0] if len(cands) == 1 else None)
            return pick["gid"] if pick else bid
        return ref_re.sub(sub, str(text))

    L = ["# FIXLIST — PEMS2024 vs site (%s)" % DATE, "",
         "Mechanical fix list generated by `audit/protocol-reconciliation/work/merge_audit.py` "
         "from the 11 batch outputs. One self-contained line per finding, grouped by severity "
         "AFTER rulings R-1..R-3; no \"see above\" references. The OWNER marker (R-6) means an "
         "owner/medical-director decision is required. The closing `inferred` marker means the "
         "PEMS level was decoded from flattened text and must be verified in `PEMS2024.pdf` "
         "before the edit.",
         ""]
    for s in ("CRITICAL", "MODERATE", "MINOR"):
        L.append("## %s" % s)
        L.append("")
        for d in [x for x in flat if x["severity"] == s]:
            line = ('- [%s] %s | %s | row %s | current: "%s" | correct: "%s" | %s'
                    % (s, d["gid"], d["_file"], "absent" if d["row"] is None else d["row"],
                       q(d.get("current_value")), q(d.get("correct_value")),
                       q(fix_gid_refs(fix_refs(recommendation(d), d)))))
            if d["_owner"]:
                line += " | [OWNER]"
            if d.get("level_decode") == "inferred":
                line += " | inferred: confirm in PDF before edit"
            L.append(line)
        L.append("")
    L.append("_Totals: CRITICAL %d · MODERATE %d · MINOR %d · %d findings · %d upgraded by "
             "R-1..R-3._"
             % (sum(1 for d in flat if d["severity"] == "CRITICAL"),
                sum(1 for d in flat if d["severity"] == "MODERATE"),
                sum(1 for d in flat if d["severity"] == "MINOR"), len(flat), len(changes)))
    L.append("")
    with open(FIX_OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


# --------------------------------------------------------------------------- verify
def verify(flat, changes):
    ok = True
    pages = disk_pages()
    data = json.load(open(JSON_OUT, encoding="utf-8"))
    n_json = sum(len(o["discrepancies"]) for o in data)
    md_rows = sum(1 for line in open(MD_OUT, encoding="utf-8") if line.startswith("| AUD-"))
    fix_lines = sum(1 for line in open(FIX_OUT, encoding="utf-8") if line.startswith("- ["))
    sev = collections.Counter(d["severity"] for d in flat)
    dup = [g for g, c in collections.Counter(d["gid"] for d in flat).items() if c > 1]
    in_json = {o["file"] for o in data}
    missing = [f for f in pages if f not in in_json]

    print("find docs/protocols -name '*.md' | wc -l   =", len(pages))
    print("protocol objects in JSON                 =", len(data))
    print("json discrepancies                       =", n_json)
    print("md table rows (^| AUD-)                  =", md_rows)
    print("fixlist lines (^- [)                     =", fix_lines)
    print("severity CRIT/MOD/MIN                    =", sev["CRITICAL"], sev["MODERATE"],
          sev["MINOR"], "| sum", sum(sev.values()))
    print("ruling changes                           =", len(changes),
          dict(collections.Counter(c["ruling"] for c in changes)))
    print("owner flags / inferred                   =",
          sum(1 for d in flat if d["_owner"]), "/",
          sum(1 for d in flat if d.get("level_decode") == "inferred"))
    print("duplicate gids                           =", dup or "none")
    print("pages on disk missing from JSON          =", missing or "none")
    if not (n_json == md_rows == fix_lines == len(flat) == EXPECT_TOTAL):
        print("FAIL: counts do not reconcile")
        ok = False
    if dup:
        print("FAIL: duplicate gid")
        ok = False
    if len(data) != len(pages):
        print("FAIL: protocol objects != pages on disk")
        ok = False
    if sum(sev.values()) != EXPECT_TOTAL:
        print("FAIL: severity sum != %d" % EXPECT_TOTAL)
        ok = False
    print("VERIFY:", "OK" if ok else "FAILED")
    return ok


def main():
    protos, per_batch = load_batches()
    flat, changes = classify(protos)
    objects = build_json(flat, protos)
    build_md(flat, changes, objects, per_batch)
    build_fixlist(flat, changes)
    print("wrote", JSON_OUT)
    print("wrote", MD_OUT)
    print("wrote", FIX_OUT)
    if "--verify" in sys.argv:
        return 0 if verify(flat, changes) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
