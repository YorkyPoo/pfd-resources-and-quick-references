---
title: "'Prints nowhere' audit — the 17 flags against the PEMS text layer"
description: Read-only re-verification of every "PEMS prints this nowhere" flag, measured in code.
---

# AUDIT — "PEMS prints this nowhere" flags vs the PEMS text layer

**Task:** t_c7aa7e6e · **Profile:** developer · **Date:** 2026-11-17
**Source of record:** `/root/System/mindpalace/40 - areas/Paramedic/PEMS2024.pdf` (280 pages,
`pdfinfo` verified), read through its own text layer `pems_chunks/PEMS2024_full.txt`
(the file `audit/level-scan/pems_table.json` names as its `sources.text_layer`).
**Mode:** read-only. No protocol page, ledger, binding, `pending-protocols.yaml` or digest
was modified (`git status --porcelain` empty at end; digest md5 unchanged — see §6).

---

## Verdict in one paragraph

All **9** owner findings are **CONFIRMED**. The defect is wider than 9 rows: of the **17**
flags the digest publishes under "PEMS prints this nowhere", **1 is falsified by a badged
row the extractor dropped, 12 are falsified by unbadged prose, and only 4 are genuinely
absent**. The same defect reaches into the PENDING family: of the **5** PENDING entries that
claim the source is silent, **1 is falsified by a badged row and 3 by prose**; only the
Aortic Dissection whole-protocol claim holds. Site-wide that is **22 "PEMS prints nothing
here" claims, 17 of them false**. Two separate extraction defects produce this, both
reproduced below: prose is not in the extraction at all, and a page carrying exactly one
badged row is classified as narrative and its row discarded (p.78 — the only page in the
whole 280-page PDF with that shape).

---

## 1. The nine owner findings, verified independently

Each was checked against the PDF page, not against `pems_table.json`. Page numbers are PDF
page indices, which match the ledger's numbering exactly (280 markers in the text layer,
280 PDF pages). Bullet numbers are counted from the printed bullet list on the page.

### 1. Pain Control r8, shown `MC` — **CONFIRMED** (falsified by a badged row)

**p.78** is a continuation of the Pain Control protocol and carries exactly one row, with a
red **`MC`** badge in *both* margin columns:

> "If unable to adequately control pain or safely and humanely extricate/transport a stable
> patient, contact medical control for guidance."

This is a **level-badged table row**, not prose. The owner's citation `p.78#0 (MC)` is
exactly right: it is row 7 of the protocol (p.77 prints rows 1–6) and ordinal 0 of p.78.

Why the pipeline missed it: p.78 is **absent from `pems_pages_parsed`** in
`pems_table.json`. The ledger's reason — *"p.77 carries no Medical Control row at all (its
six rows are #0–#5, all interventions)"* — is true of p.77 and was never checked against
p.78. Root cause in §3.2.

### 2. Chest Pain r5, shown `P` — **CONFIRMED** (falsified by prose)

- **p.108 PEARLS b1** — the owner's citation is exact:
  > "Intermediate and Paramedic providers may interpret a 12-Lead ECG as STEMI if
  > diagnostic criteria is met: … Symptoms consistent with an acute coronary syndrome or
  > myocardial ischemia **AND** … ≥ 1 mm ST segment elevation in two or more contiguous
  > leads"
- **p.232 PEARLS** — the same sentence verbatim. **Index correction:** it is the **7th**
  top-level bullet, not the 6th (verified visually on the rendered page: 9 top-level
  bullets, of which #7 is the interpretation sentence, #8 the "EMT-I and Paramedic" scope,
  #9 the 15-Lead definition). The substance of the finding is unaffected.
- **p.231#4**, badge **EMT** — the owner's citation is exact, and it is a badged row:
  > "If no EMT-I or Paramedic is available to assess the ECG, or if it is interpreted by an
  > EMT-I or Paramedic to represent an acute cardiac emergency (e.g. acute dysrhythmia),
  > transmit the ECG …"

Flag false. PEMS prints the instruction three times, once in a badged row and twice in
unbadged Pearls.

### 3. Chest Pain r14, shown `I` — **CONFIRMED** (falsified by prose)

- **p.108 PEARLS b3** — exact: > "Consider right-sided 12-Lead or 15-Lead ECG."
- **p.232 PEARLS b8** — > "**EMT-I and Paramedic:** If there is >1 mm ST elevation in leads
  II, III, and/or V1 … consider obtaining a right-sided (V4R) ECG."
- **p.232 PEARLS b9** — > "A Right-sided 12-Lead ECG (V4R) & Posterior 12-Lead ECG (V8 & V9)
  together constitute a 15-Lead ECG:"

**Index correction:** the owner wrote "b7–8"; the scope sentence is **b8** and the 15-Lead
definition is **b9** (b7 is the STEMI-interpretation bullet). Substance unaffected. The
digest's claim — *"No PEMS 2024 row anywhere prints a right-sided or 15-lead ECG"* — is
false as a statement about PEMS; it is only true as a statement about *badged rows*.

### 4. Cold Exposure r6, shown `EMT` — **CONFIRMED** (falsified by prose, unbadged)

**p.67 PEARLS b5** — exact:
> "If the patient is alert and responsive, use active external rewarming with heat packs,
> warm blankets, etc"

The Pearls carry **no badge at all** — the rendered page shows a plain bullet list with no
level column and no level token (verified visually). **One addition the reason omits:
p.67 PEARLS b2 prints the opposite caution —**
> "DO NOT place heat packs, hot water bottles, IV bags, or other heat-retaining devices
> directly on skin"

so the source endorses heat packs (b5) and forbids direct skin contact (b2). The site row
("Use active external rewarming with heat packs, warm blankets, etc.") matches b5 and would
breach b2 if applied directly to skin. That is a clinical-wording question for the owner
alongside the level question.

### 5. Cold Exposure r9, shown `MC` — **CONFIRMED** (falsified by prose, unbadged)

**p.67 PEARLS b3** — exact: > "Contact Medical Control prior to use of AED" (no badge).

The digest's claim *"PEMS prints an AED Medical Control gate nowhere in the Cold Exposure
protocol"* is false as written: the protocol prints it in its own Pearls on its own page.
What is true is narrower — p.67's six *badged rows* (#0–#5) contain no AED row, and no
badged row anywhere gates AED on MC. Both halves stand; the "nowhere" framing does not.

### 6. Inhalation Irritants r11, shown `P` — **CONFIRMED** (falsified by prose, unbadged)

- **p.154 PEARLS** (CBRNE: Airway / Inhalation Irritants, final bullet) — verbatim:
  > "Contact the Poison Control Center at 1-800-222-1222 with any questions. Note: Although
  > Poison Control can provide invaluable expert guidance, it is not online medical control.
  > If recommendations fall outside of protocols, contact medical control for guidance."
- **p.121 PEARLS b1** (Overdose / Poisoning / Toxic Ingestion) — the identical sentence.
- **p.19** (Communications) lists `Poison Control (800) 222-1222` in the regional contact
  table — confirmed in the text layer.

Unbadged in all three places. The digest's *"the referral is agency authoring; PEMS routes
questions to Medical Control instead"* is contradicted by the Pearl itself: PEMS prints both
routes and says explicitly that Poison Control is *not* online medical control. No level is
assigned here (owner's ruling).

### 7–9. Pulmonary Edema / Congestion r6, r7, r8, shown `A` — **ALL THREE CONFIRMED**

**p.245** (Procedure: CPAP/BiPAP/PEEP) prints an explicit **`CONTRAINDICATIONS`** section
whose eight bullets cover all three site rows word-for-word:

> "Apnea / agonal respirations · Decreased level of consciousness (GCS ≤ 13) · Pneumothorax ·
> Facial trauma, burns, or recent surgery · Penetrating neck and/or chest trauma · Active
> vomiting / severe nausea · Hypotension (SBP < 90 mmHg, MAP < 65) · Inability to tolerate
> tight fitting mask"

Mapping to the site rows: r6 = bullets 1–3, r7 = bullets 4–6, r8 = bullets 7–8.

**Placement and badges (as asked):** the CONTRAINDICATIONS section sits **above and outside**
the procedure table — it is headed prose, not grid rows — and **carries no level badge in
any form**. The `PROCEDURE` table immediately below it has five rows, each badged **EMT in
both margin columns**, and the page footer adds "CPAP, BiPAP, and PEEP are RED DOT
procedures at all EMS Certification Levels". Verified visually on the rendered page, so: the
words are printed (flag false), the words carry no badge (badge question live), and the
procedure they govern is badged EMT (the page's `A` is out of sync with that, as the owner
says).

The digest's parenthetical *"(p.245 is the CPAP procedure's steps)"* is the tell: p.245 was
looked at, but only its **rows** were read. The contraindication block was on the same page
and invisible to the search.

---

## 2. Full extent, derived in code

Script: `nowhere_scan.py` (Appendix A; run from the repo root, exit 0). It takes the 17
flags straight out of the ledger using the same two lines as
`scripts/build_outstanding_decisions.py` (`status == OWNER_REQUIRED` and the reason not
matching that script's `CONFLICT` regex — so the "17" is the digest's own definition, not
mine), asserts `len(flags) == 17`, verifies **every** quoted page/needle against the text
layer before counting, and then asserts the three counts sum to the flag count.

Enumeration, for the record (`level-rule-ledger.json`):

| shape | count | note |
|---|---|---|
| `OWNER_REQUIRED`, reason matches the digest's CONFLICT regex | 21 | "two levels", "one chip cannot carry both" — a *different* defect (bundled rows), not a silence claim |
| `OWNER_REQUIRED`, reason does **not** match → published as "PEMS prints this nowhere" | **17** | the flags this audit is about |
| `pending_omd` rows (rows of a protocol with no PEMS equivalent) | 11 | all on `04b_Aortic_Dissection_AAA_PROC.md` |
| `pending_row_omd` rows | 8 | see §4 |

`row-bindings.yaml` (274 entries) carries the same claims as its evidence: 39 `owner_required`
entries (22 of them worded as a silence claim — the same 17 plus 5 of the conflict set) and
37 *positive* bindings that carry a supporting note of the form "Cross-page: p.N prints no
… row". Those 37 are the same genre of assertion and were **not** re-verified row by row
here (§7).

### The three counts

```
flags examined          : 17
falsified by badged row : 1  -> ['Pain Control r8 (MC escalation for uncontrolled pain)']
falsified by prose      : 12  -> ['Chest Pain r5 (12-lead STEMI interpretation)', 'Chest Pain r14
                               (right-sided / 15-lead ECG)', 'Inhalation Irritants r3 (airway-injury
                               assessment)', 'Inhalation Irritants r11 (Poison Control consultation)',
                               'Pulmonary Edema r6 (CPAP contraindication list 1)', 'Pulmonary Edema r7
                               (CPAP contraindication list 2)', 'Pulmonary Edema r8 (CPAP
                               contraindication list 3)', 'Smoke Inhalation r3 (airway-injury
                               assessment)', 'Trauma r6 (assess for shock)', 'Cold Exposure r6 (active
                               external rewarming)', 'Cold Exposure r9 (MC before AED)', 'Sedation r4
                               (pre-intubation sedation, ketamine)']
genuinely absent        : 4  -> ['Pediatric Stridor r2 (scene mgmt / keep child calm)', 'Pneumothorax
                               r5 (suction/airway equipment readiness)', 'Upper Airway Obstruction r2
                               (recognition)', 'Sedation r5 (post-intubation sedation, ketamine)']
ASSERT 1+12+4 == 17 AND every declared quote verified against the text layer -> ALL TRUE
```

**Per-row evidence** (abridged; the script prints all of it):

| # | Row | Shown | Class | Where PEMS prints it |
|---|---|---|---|---|
| 1 | Chest Pain r5 | `P` | prose | p.108 PEARLS b1; p.232 PEARLS b7; p.231#4 (badged EMT) |
| 2 | Chest Pain r14 | `I` | prose | p.108 PEARLS b3; p.232 PEARLS b8, b9 |
| 3 | Inhalation Irritants r3 | `EMT` | prose | p.88 PEARLS b1 "Assess for airway / inhalation injury…" (+ p.87 badged-I row prints the sign list as intubation indications) |
| 4 | Inhalation Irritants r11 | `P` | prose | p.154 PEARLS; p.121 PEARLS b1 |
| 5 | Pediatric Stridor r2 | `EMT` | **absent** | pp.123–125: "calm" occurs only in Behavioral Emergencies de-escalation guidance (p.72–73), nothing about keeping a child calm |
| 6 | Pneumothorax r5 | `A` | **absent** | pp.61, 84, 239–240, 243: no "prepare suction" / "be prepared for rapid airway" anywhere |
| 7 | Pulmonary Edema r6 | `A` | prose | p.245 CONTRAINDICATIONS bullets 1–3 |
| 8 | Pulmonary Edema r7 | `A` | prose | p.245 CONTRAINDICATIONS bullets 4–6 |
| 9 | Pulmonary Edema r8 | `A` | prose | p.245 CONTRAINDICATIONS bullets 7–8 |
| 10 | Smoke Inhalation r3 | `EMT` | prose | p.88 PEARLS b1 (+ p.87 badged-I row) |
| 11 | Upper Airway Obstruction r2 | `EMT` | **absent** | pp.239–240: no recognition language, no "choking sign", no complete-vs-partial wording |
| 12 | Trauma r6 | `A` | prose *(partial)* | p.84 PEARLS b3 "Any patient who is cool/diaphoretic and tachycardic is considered to be in shock until proven otherwise." — recognition is printed; the *referral* half ("refer to the Shock protocol") is not |
| 13 | Cold Exposure r6 | `EMT` | prose | p.67 PEARLS b5 (+ b2 caution) |
| 14 | Cold Exposure r9 | `MC` | prose | p.67 PEARLS b3 |
| 15 | Pain Control r8 | `MC` | **badged row** | p.78, MC in both margins |
| 16 | Sedation r4 | `I` | prose *(partial)* | p.248 ET-intubation PEARLS "If performing RSI: Etomidate … Ketamine may increase the risk of post-intubation hypotension…"; p.195 ketamine monograph INDICATIONS "… Rapid sequence induction". No dose and no level are printed |
| 17 | Sedation r5 | `P` | **absent** | pp.55, 195, 248: nothing prints post-intubation *ketamine* sedation (p.55 Pearls name fentanyl only; p.195 indications are behavioral emergencies and RSI) |

Two of the twelve prose hits (#12, #16) are **partial**: the prose prints part of the action,
not all of it. They are counted as false **rationales** because both reasons say some form of
"printed nowhere" / "no PEMS row", and both are demonstrably wrong about the protocol they
belong to. The owner should read #12 and #16 as "the reason is false, the level question is
still open", not as "the chip should be re-derived from these quotes".

**On the operator's "only 8 of the 17 remain unflagged":** four of those eight (Inhalation
Irritants r3, Smoke Inhalation r3, Trauma r6, Sedation r4) are also printed in the source,
in prose. Only **4** of the 17 are genuinely silent: Pediatric Stridor r2, Pneumothorax r5,
Upper Airway Obstruction r2, Sedation r5.

---

## 3. Structural defects (reproduced, not inferred)

### 3.1 Prose is not in the extraction — there is no prose capability at all

- `audit/level-scan/pems_table.json` row schema is
  `[page, section_heading, ordinal, section_ordinal, verbatim_text, x, y, badge_tokens, columns]`.
  `verbatim_text` exists only for grid rows. **`pems_table.json` records no prose.**
- In `scripts/pems_canonical.py`, `PEARLS`, `NOTES`, `REFERENCES`, `CRITERIA` are
  **stop tokens** — `GRID_STOP` (line 85) ends the grid at them, and
  `scripts/pems_level_scan.py:105` (`SEC`) splits sections on them. The prose below those
  headings is deliberately not parsed into anything.
- **No script extracts Pearls / Notes / Key Points.** `grep -rn "PEARL" scripts/*.py` finds
  only those two stop-token definitions (plus two prose mentions inside
  `scripts/level_rule.py` comments). There is no prose index, no prose search, no
  prose-to-page lookup.
- The prose **is** available and always was: `pems_chunks/PEMS2024_full.txt` is the PDF text
  layer with `--- PAGE n ---` markers, and 12 of the 45 per-topic chunk files contain
  `PEARLS`. It is the file `pems_table.json` itself cites as `sources.text_layer`. The
  verifier never read it.
- Corroboration that the adjudications were row-only: `audit/level-scan/adjudicated.json`
  records carry `"evidence_basis": "PDF text layer (pems_table.json)"` — the text layer was
  consulted **through the table**, which carries only rows.

**Consequence:** the fix is not a data correction. It is a **new extraction/index pass for
prose** (page → section-heading → text), plus a verifier rule that a "the source is silent"
conclusion is only admissible after a prose search. Until then no silence claim in this
project is safe, including the four that happen to be true.

### 3.2 The p.77 → p.78 boundary defect — one page, exact cause

`scripts/pems_canonical.py:294`:

```python
kind = "protocol" if caps else ("continuation" if len(badges) >= 2 else "narrative")
if kind == "narrative":
    return {..., "rows": [], "orphans": []}
```

A page is treated as a table continuation only if it carries **at least two badge groups**.
p.78 carries exactly **one** (the single MC row), so it is classed `narrative` and its row is
returned as `rows: []` — silently discarded, not reported as an error or an orphan.

Reproduced by calling the parser directly:

```
page 77 kind protocol n_badges 6 rows 6 orphans 0
page 78 kind narrative n_badges 1 rows 0 orphans 0
page 79 kind narrative n_badges 0 rows 0 orphans 0
```

**How widespread is it?** I ran `parse_page` over all 280 pages and counted every page that
carries ≥1 badge but contributes zero rows:

```
Pages carrying >=1 level badge but contributing ZERO rows to pems_table.json: 1
   p.78  kind=narrative  n_badges=1  title='Pain Control'
```

**p.78 is the only page in the whole PDF with that shape.** So the boundary defect has
exactly one casualty — but that casualty is a badged row, and it is the row behind one of the
17 flags.

### 3.3 Continuation-row audit across every multi-page protocol table

Same script (`multipage.py`, Appendix C output), grouping consecutive pages by their printed
protocol title and testing each page of each run against `pems_pages_parsed`:

| measure | count |
|---|---|
| consecutive same-title page runs of length ≥ 2 that carry an extracted table | **50** |
| …where at least one later page contributes **no rows** | **44** |
| …where a row-less later page also **carries a level badge** (a row was dropped) | **1** (p.78, Pain Control) |

So: **50 multi-page protocol/procedure tables span a page break; 44 have at least one page
after the break that contributes no rows; exactly one of those pages carries a level badge.**
The other 43 are PEARLS / NOTES / CRITERIA pages, which legitimately have no rows. The
p.77→p.78 case is the only lost *badged* continuation row in the source — the boundary defect
is real but bounded, and it is **not** the cause of the other falsifications (those are §3.1).

Note: this measures rows **missing from a page entirely**. Rows that are present but **fused**
across a page break are a different defect, measured separately in
`audit/level-scan/fusion-impact.md` (17 fused rows on 12 pages, 4 with a wrong badge).

---

## 4. The PENDING family — same blind spot, measured

`pending-protocols.yaml` holds 1 whole-page entry and 8 row-level entries; the ledger mirrors
them as 11 `pending_omd` rows and 8 `pending_row_omd` rows. Three of the eight row-level
reasons are **prose-aware** — they already name the Pearls/guideline page they saw, so they
are not silence claims. The other five are:

```
PENDING entries examined       : 8
  prose-aware (already correct): 3  -> ['Burns r6 (HF calcium chloride)', 'Behavioral Health
                                       Transport r6 (LE custody)', 'Behavioral Health Transport r7
                                       (LE restraints)']
  silence claims               : 5
    falsified by badged row    : 1  -> ['Stroke Field Triage r1 (15-minute scene time)']
    falsified by prose         : 3  -> ['Stroke/TIA r8 (18g right AC for rapid imaging)',
                                        'Stroke/TIA r9 (call COR with Name/DOB)',
                                        'Stroke Field Triage r4 (life threats to nearest ED)']
    accurate                   : 1  -> ['Aortic Dissection/AAA (whole protocol absent)']
ASSERT 1+3+1 == 5 (silence claims) AND 3 prose-aware AND every quote verified -> ALL TRUE
```

Detail:

- **Stroke/TIA r8** (`Establish 18g IV in Right AC`) — reason: *"PEMS 2024 p.131 publishes no
  such action."* **False.** p.132 PEARLS b4: *"To facilitate rapid imaging, an 18g IV in the
  right antecubital (AC) site is preferred."*
- **Stroke/TIA r9** (`Call COR … Name/DOB for rapid registration`) — reason: *"no other PEMS
  2024 row on p.131 does."* Narrowly true about p.131 rows; **but p.132 PEARLS b7 prints it
  verbatim**: *"Call COR at the receiving facility to inform of the patient's name and date
  of birth for rapid registration."*
- **Stroke Field Triage r1** (`goal scene time < 15 minutes`) — reason: *"PEMS prints a
  scene-time goal only in the Trauma Field Triage policy (p.44, 10 minutes), which does not
  govern stroke."* **False, and falsified by a badged row:** p.131 (Stroke / TIA) prints
  *"Initiate transport. Goal scene time < 15 minutes"* at badge **EMT**.
- **Stroke Field Triage r4** (`life threats → nearest ED`) — reason: *"…no 'life threats go to
  the nearest ED' branch. That branch is the agency page's own addition."* **False.** p.132
  PEARLS b6: *"Any patient with an immediate life-threat (e.g. uncontrolled airway, cardiac
  arrest) that cannot be addressed during transport should be transported to the nearest
  emergency department."*
- **Burns r6** (HF calcium) — the reason *already* says PEMS prints it only in the Burns
  Pearls, and it is right: p.88 PEARLS, *"Hydrofluoric Acid (HF) – … Treat hypotension with
  1 g Calcium Chloride IV/IO over 3 minutes."* **Accurate and honest.** The operator's note
  that this reasoning is "now suspect" does not hold: it is the model the other reasons
  should have followed.
- **Behavioral Health Transport r6 / r7** — both quote p.73 correctly (verified verbatim).
  **Accurate and honest.**
- **Aortic Dissection / AAA (page-level)** — *"PEMS 2024 publishes no Aortic Dissection or AAA
  protocol."* **Accurate.** "Aortic dissection" occurs in the whole text layer only at p.114,
  as an example of a "pipe problem" inside the Hypotension/Shock Pearls. No protocol, no rows.

**Site-wide total:**

```
SITE-WIDE: 17 'prints nowhere' flags + 5 PENDING silence claims = 22 'PEMS prints nothing here' claims
           17 false, 5 accurate
ASSERT 17+5 == 22 -> TRUE
```

The 38-row `OWNER_REQUIRED` count is therefore **not** a workload figure (the operator is
right): 13 of its 17 published "prints nowhere" rows are pipeline misses, and the 21 conflict
rows are a different question again.

---

## 5. Unbadged-prose inventory — for the owner's ruling, no levels assigned

Everything PEMS prints that falsifies a flag, with the page and the heading it sits under.
**No level is proposed, inferred, or defaulted anywhere in this section.**

| # | Page | Section | Text | Site row it matches (shown level) |
|---|---|---|---|---|
| 1 | p.108 | PEARLS b1 | "Intermediate and Paramedic providers may interpret a 12-Lead ECG as STEMI if diagnostic criteria is met…" | Chest Pain r5 (`P`) |
| 2 | p.232 | PEARLS b7 | same sentence, verbatim | Chest Pain r5 (`P`) |
| 3 | p.108 | PEARLS b3 | "Consider right-sided 12-Lead or 15-Lead ECG." | Chest Pain r14 (`I`) |
| 4 | p.232 | PEARLS b8 | "EMT-I and Paramedic: … consider obtaining a right-sided (V4R) ECG." | Chest Pain r14 (`I`) |
| 5 | p.232 | PEARLS b9 | "A Right-sided 12-Lead ECG (V4R) & Posterior 12-Lead ECG (V8 & V9) together constitute a 15-Lead ECG" | Chest Pain r14 (`I`) |
| 6 | p.88 | PEARLS b1 | "Assess for airway / inhalation injury. Consider early definitive airway management for patients with respiratory distress, hoarse voice or stridor, carbonaceous sputum and/or facial burns." | Inhalation Irritants r3, Smoke Inhalation r3 (`EMT`) |
| 7 | p.154 | PEARLS (last bullet) | "Contact the Poison Control Center at 1-800-222-1222 with any questions. Note: Although Poison Control can provide invaluable expert guidance, it is not online medical control…" | Inhalation Irritants r11 (`P`) |
| 8 | p.121 | PEARLS b1 | the identical sentence | Inhalation Irritants r11 (`P`) |
| 9 | p.67 | PEARLS b3 | "Contact Medical Control prior to use of AED" | Cold Exposure r9 (`MC`) |
| 10 | p.67 | PEARLS b5 | "If the patient is alert and responsive, use active external rewarming with heat packs, warm blankets, etc" | Cold Exposure r6 (`EMT`) |
| 11 | p.67 | PEARLS b2 | "DO NOT place heat packs, hot water bottles, IV bags, or other heat-retaining devices directly on skin" | constrains #10 — not a flag, a wording conflict |
| 12 | p.245 | **CONTRAINDICATIONS** (headings block, not Pearls) | the 8 contraindication bullets | Pulmonary Edema r6, r7, r8 (`A`) |
| 13 | p.84 | PEARLS b3 | "Any patient who is cool/diaphoretic and tachycardic is considered to be in shock until proven otherwise." | Trauma r6 (`A`) |
| 14 | p.248 | PEARLS (RSI bullet) | "If performing RSI: Etomidate … is the preferred induction agent in most cases. Ketamine may increase the risk of post-intubation hypotension…" | Sedation r4 (`I`) |
| 15 | p.195 | Ketamine monograph, INDICATIONS | "Behavioral emergencies …; Rapid sequence induction" | Sedation r4 (`I`) |
| 16 | p.132 | PEARLS b4 | "To facilitate rapid imaging, an 18g IV in the right antecubital (AC) site is preferred." | Stroke/TIA r8 (`PENDING`) |
| 17 | p.132 | PEARLS b7 | "Call COR at the receiving facility to inform of the patient's name and date of birth for rapid registration." | Stroke/TIA r9 (`PENDING`) |
| 18 | p.132 | PEARLS b6 | "Any patient with an immediate life-threat … should be transported to the nearest emergency department." | Stroke Field Triage r4 (`PENDING`) |
| 19 | p.73 | guideline bullets | "Patients in law enforcement custody … must have a law enforcement officer present at all times." / "If law-enforcement restraints have been utilized … a law enforcement officer should accompany the patient." | Behavioral Health Transport r6/r7 (already prose-aware) |
| 20 | p.88 | PEARLS (HF bullet) | "Treat hypotension with 1 g Calcium Chloride IV/IO over 3 minutes." | Burns r6 (already prose-aware) |

Shape of the evidence, for the policy decision:

- **17 of the 20 sit under a `PEARLS` heading** — a heading, a bullet list, no badge column
  anywhere on the page.
- **1 is a different prose block**: the p.245 `CONTRAINDICATIONS` list. Same problem (no
  badge), different heading — a prose policy that recognises only `PEARLS` will miss it.
- **2 are drug-monograph / guideline prose** (p.195 ketamine monograph, p.73 restraint
  guidelines) — administrative/prose sections again.
- **1 is a caution that contradicts another bullet** (p.67 b2 vs b5) and needs a wording
  decision, not a level decision.
- In every case the surrounding **badged** rows print a *narrower or different* action, which
  is why a row-only search could conclude "silent" with a straight face.

---

## 6. The digest — untouched, and a path correction

`audit/level-scan/outstanding-decisions-digest.md` **does not exist**. The file the owner is
reading is **`docs/protocols/outstanding-decisions.md`** (743 lines), generated by
`scripts/build_outstanding_decisions.py`. I have not modified it:

```
md5 docs/protocols/outstanding-decisions.md
7d5e85e78c6c15d97429b221fe3ac731   (before the audit; unchanged after)
```

`git status --porcelain` is empty apart from this new report file. The digest's own count
("PEMS prints this nowhere — 17 rows") is **correct** — 17 is exactly what the ledger's
classifier yields. What is wrong is not the count but the verdicts underneath it: 13 of those
17 rows are printed in the source. The digest also mislabels its own evidence base: the
`od-chip-nowhere` help text says *"No PEMS 2024 row prints the action at all"*, which is
literally what the pipeline checked — but it presents that as "the source is silent".

---

## 7. What I did not do

- **No level assigned, proposed or defaulted** for any unbadged prose case (§5) — owner's
  ruling. Nothing converted to PENDING, nothing bound, nothing chipped.
- **No file under `docs/`, `audit/level-scan/*.json|yaml|md` modified.** The only new file is
  this report.
- **The 21 conflict-class flag reasons were not re-verified.** They claim a *bundle* problem
  ("two rows, two levels"), not silence; that is a separate question and a separate task.
- **The 37 "Cross-page: p.N prints no … row" notes inside positive bindings in
  `row-bindings.yaml` were not re-verified one by one.** They are the same genre of assertion
  and carry the same risk; the four PENDING falsifications above show the risk is real. I
  recommend they be swept with the same prose index once it exists.
- **Not touched: the fused-row defect** (17 fused rows / 4 wrong badges) — measured
  separately in `audit/level-scan/fusion-impact.md`.
- **Not verified: any clinical judgement** about whether an unbadged Pearl should carry a
  level at all, or which. That is the policy gap (§5).

---

## Appendix A — `nowhere_scan.py` (the measurement)

Reproduce with `python3 nowhere_scan.py` from the repo root. Not placed in `scripts/`
because acceptance for this task requires `git status` clean apart from this report; lift it
into `scripts/` when the owner rules.

```python
"""Audit: do the 17 'PEMS prints this nowhere' flags survive the FULL text layer?

Read-only. Writes nothing but stdout.

Each flag's reason says "No PEMS 2024 row prints this action" / "Nothing to cite". The
audit that produced those reasons searched audit/level-scan/pems_table.json, which holds
level-badged grid rows ONLY. PEMS also prints clinical instruction as unbadged prose
(PEARLS, NOTES, CONTRAINDICATIONS blocks, drug monographs) and the row parser deliberately
stops the grid at those headings.

Method: take the 17 OWNER_REQUIRED reasons the digest labels "PEMS prints this nowhere"
(same classifier as scripts/build_outstanding_decisions.py); declare, per row, the evidence
found by reading pems_chunks/PEMS2024_full.txt; VERIFY every declared page+needle against
that text layer (abort otherwise); classify each hit as badged row / prose by testing
whether the phrase sits inside a row pems_table.json extracted for that page; assert the
three counts sum to 17; then do the same for the PENDING silence claims.

Matching is whitespace-insensitive: the procedure pages' text layer prints with no spaces
between words, so haystack and needle are whitespace-stripped and lower-cased first.
"""
import json, re

REPO = "/root/projects/pfd-resources-and-quick-references"
FULL = f"{REPO}/pems_chunks/PEMS2024_full.txt"
LEDGER = f"{REPO}/audit/level-scan/level-rule-ledger.json"
TABLE = f"{REPO}/audit/level-scan/pems_table.json"
CONFLICT = re.compile(r'contradict|conflict|two levels|three levels|multiple levels|'
                      r'single badge|one chip cannot|two rows|three rows|at one level', re.I)


def norm(s):
    return re.sub(r"\s+", "", s).lower()


pages = {}
parts = re.split(r"--- PAGE (\d+) ---", open(FULL, encoding="utf-8", errors="replace").read())
for i in range(1, len(parts), 2):
    pages[int(parts[i])] = parts[i + 1]

tbl = json.load(open(TABLE))
_badged = {}
for doc in tbl["pems_docs"]:
    for r in doc["rows"]:
        _badged.setdefault(r["page"], []).append(r["verbatim_text"])
BADGED_TEXT = {p: norm(" ".join(v)) for p, v in _badged.items()}
PARSED = set(tbl["pems_pages_parsed"])

# label, ledger(file,row) marker, search pages, class, [(page, needle, kind, quote)]
# kind: "row" = inside a badged row pems_table.json already has; "prose" = only in unbadged
# prose; "unparsed_row" = badged row on a page pems_table.json never parsed.
CASES = [ ... 17 entries ... ]        # full list in the run that produced this report
PENDING_CASES = [ ... 8 entries ... ]


def main():
    ledger = json.load(open(LEDGER))
    nowhere = [r for r in ledger["rows"] if r["status"] == "OWNER_REQUIRED"
               and not CONFLICT.search(r.get("reason") or "")]
    assert len(nowhere) == 17, len(nowhere)
    keys = {(r["file"].rsplit("/", 1)[-1], r["row"]) for r in nowhere}
    for c in CASES:
        assert (c["file"], c["row"]) in keys, ("not a 'nowhere' ledger row", c["label"])
    assert len(CASES) == len(keys) == 17, (len(CASES), len(keys))

    problems = []
    for c in CASES:
        for (p, nd, kind, quote) in c["ev"]:
            hay = norm(pages.get(p, ""))
            if not re.search(nd, hay):
                problems.append(f"{c['label']}: needle /{nd}/ NOT FOUND on p.{p}")
                continue
            in_row = bool(re.search(nd, BADGED_TEXT.get(p, "")))
            if kind == "prose" and in_row:
                problems.append(f"{c['label']}: p.{p} hit is inside a badged row, not prose")
            if kind == "row" and not in_row:
                problems.append(f"{c['label']}: p.{p} hit is NOT inside a badged row")
            if kind == "unparsed_row" and p in PARSED:
                problems.append(f"{c['label']}: p.{p} expected an unparsed badged row")
    assert not problems, "\n".join(problems)

    for c in CASES:
        kinds = {e[2] for e in c["ev"]}
        if c["cls"] == "absent":
            assert not c["ev"]
        elif c["cls"] == "badged_row":
            assert "unparsed_row" in kinds or "row" in kinds, c["label"]
            assert "prose" not in kinds, c["label"]
        else:
            assert "prose" in kinds, c["label"]

    badged = [c for c in CASES if c["cls"] == "badged_row"]
    prose = [c for c in CASES if c["cls"] == "unbadged_prose"]
    absent = [c for c in CASES if c["cls"] == "absent"]
    assert len(badged) + len(prose) + len(absent) == len(nowhere) == 17
    print(f"ASSERT {len(badged)}+{len(prose)}+{len(absent)} == {len(nowhere)} "
          f"AND every declared quote verified -> ALL TRUE")
    # ... PENDING block, same pattern, asserted 1+3+1 == 5 with 3 prose-aware, 17+5 == 22
```

## Appendix B — per-page badge check (the p.78 defect, all 280 pages)

```python
import sys, re
sys.path.insert(0, "scripts")
import pems_canonical as PC
xml = PC.P._read_pdf_xml(False)
narr1 = []
for pno, m in enumerate(PC.P.PAGE_RE.finditer(xml), 1):
    body = m.group(3)
    rec = PC.parse_page(pno, body, PC.page_title(body))
    if rec["kind"] == "narrative" and rec.get("n_badges") == 1:
        narr1.append(pno)
print("narrative pages with exactly 1 badge:", len(narr1), narr1)
```

```
Pages carrying >=1 level badge but contributing ZERO rows to pems_table.json: 1
   p.78  kind=narrative  n_badges=1  title='Pain Control'
```

## Appendix C — multi-page continuation audit output

```
Consecutive same-title page runs of length >=2 that carry an extracted table: 50
  'How to Read the Protocols' pages=[7, 8] with_rows=[7] NO_ROWS=[8]
  'Communications' pages=[17, 18, 19, 20] with_rows=[17, 18] NO_ROWS=[19, 20]
  'Patient Refusal of Treatment/Transport' pages=[27, 28, 29] with_rows=[27, 28] NO_ROWS=[29]
  'Trauma Field Triage' pages=[43, 44, 45] with_rows=[43] NO_ROWS=[44, 45]
  'Universal Patient Care / Initial Patient Contact' pages=[49, 50, 51, 52, 53] with_rows=[49, 50, 52] NO_ROWS=[51, 53]
  'Cardiac Arrest: Asystole / PEA' pages=[57, 58] with_rows=[57] NO_ROWS=[58]
  'Cardiac Arrest: Post ROSC Care' pages=[59, 60] with_rows=[59] NO_ROWS=[60]
  'Cardiac Arrest: Traumatic' pages=[61, 62] with_rows=[61] NO_ROWS=[62]
  'Cardiac Arrest: V-fib / Pulseless V-Tach' pages=[63, 64, 65] with_rows=[63, 64] NO_ROWS=[65]
  'Behavioral Emergencies' pages=[71, 72, 73] with_rows=[71, 72] NO_ROWS=[73]
  'Hemorrhage Control' pages=[75, 76] with_rows=[75] NO_ROWS=[76]
  'Pain Control' pages=[77, 78, 79] with_rows=[77] NO_ROWS=[78, 79] (badge-carrying: [78])
  'Trauma' pages=[83, 84, 85, 86] with_rows=[83, 84] NO_ROWS=[85, 86]
  'Burn Injuries' pages=[87, 88, 89] with_rows=[87, 88] NO_ROWS=[89]
  'Crush Injuries' pages=[91, 92] with_rows=[91] NO_ROWS=[92]
  'Drowning and Diving Injuries' pages=[93, 94] with_rows=[93] NO_ROWS=[94]
  'Electrical Injuries' pages=[95, 96, 97] with_rows=[95, 96] NO_ROWS=[97]
  'Symptomatic Bradycardia' pages=[103, 104, 105] with_rows=[103, 104] NO_ROWS=[105]
  'Chest Pain (Cardiac)' pages=[107, 108] with_rows=[107] NO_ROWS=[108]
  'Hypoglycemia / Hyperglycemia' pages=[111, 112] with_rows=[111] NO_ROWS=[112]
  'Hypotension and Shock' pages=[113, 114, 115, 116] with_rows=[113, 114] NO_ROWS=[115, 116]
  'Respiratory Distress' pages=[123, 124, 125] with_rows=[123, 124] NO_ROWS=[125]
  'Stroke / TIA' pages=[131, 132, 133] with_rows=[131] NO_ROWS=[132, 133]
  'Ventricular Tachycardia with a Pulse' pages=[137, 138, 139] with_rows=[137, 138] NO_ROWS=[139]
  'Childbirth / Labor / Delivery' pages=[141, 142, 143, 144, 145] with_rows=[141, 142] NO_ROWS=[143, 144, 145]
  'Airway / Inhalation Irritants' pages=[153, 154] with_rows=[153] NO_ROWS=[154]
  'CBRNE: Biological / Infectious' pages=[155, 156] with_rows=[155] NO_ROWS=[156]
  'CBRNE: Blistering Agents' pages=[157, 158] with_rows=[157] NO_ROWS=[158]
  'Nerve Agents' pages=[159, 160] with_rows=[159] NO_ROWS=[160]
  'CBRNE: Radiologic Agents' pages=[161, 162] with_rows=[161] NO_ROWS=[162]
  '12-Lead Electrocardiogram (ECG)' pages=[231, 232, 233, 234] with_rows=[231] NO_ROWS=[232, 233, 234]
  'ADULT Cardiopulmonary Resuscitation (CPR)' pages=[235, 236, 237] with_rows=[235] NO_ROWS=[236, 237]
  'Airway Management and Ventilatory Support' pages=[239, 240] with_rows=[239] NO_ROWS=[240]
  'Capnography' pages=[241, 242] with_rows=[241] NO_ROWS=[242]
  'CPAP/BiPAP/PEEP' pages=[245, 246] with_rows=[245] NO_ROWS=[246]
  'EndotrachealIntubation' pages=[247, 248] with_rows=[247] NO_ROWS=[248]
  'Intraosseous(IO)Access' pages=[249, 250] with_rows=[249] NO_ROWS=[250]
  'MedicalDevicesandPumps' pages=[251, 252, 253, 254, 255, 256] with_rows=[251, 252] NO_ROWS=[253, 254, 255, 256]
  'Neonatal Resuscitation' pages=[261, 262] with_rows=[261] NO_ROWS=[262]
  'PEDIATRICCardiopulmonaryResuscitation(CPR)' pages=[263, 264, 265] with_rows=[263] NO_ROWS=[264, 265]
  'SpinalMotionRestriction' pages=[267, 268] with_rows=[267] NO_ROWS=[268]
  'SurgicalAirway' pages=[269, 270] with_rows=[269] NO_ROWS=[270]
  'TaserBarbRemoval' pages=[271, 272] with_rows=[271] NO_ROWS=[272]
  'Vaccination Administration by EMS Providers' pages=[277, 278, 279] with_rows=[278] NO_ROWS=[277, 279]

runs where at least one page contributed no rows: 44
runs where a row-less page also carries a level badge (row silently dropped): 1
   -> Pain Control [78]
```
