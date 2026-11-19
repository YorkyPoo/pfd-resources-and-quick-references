# VERIFICATION — level scanner output (card t_adc807a8)

Reviewer: `reviewer` profile. Scope: `scripts/pems_level_scan.py` on branch `level-scan`, its outputs in `audit/level-scan/`, and the 216 rewritten rows.

## 0. Execution limits (read first)

The reviewer profile has **no shell**. Nothing below was executed by me. Every item that needs a command is marked **NOT EXECUTED — needs developer** with the exact command to run.

- Could not run: `pems_level_scan.py --apply` / `--report` / `--dry-run`, `git diff`, `git status`, `mkdocs build --strict`, `pdftotext`, or any Python.
- Could not raster the PEMS PDF. No PDF-to-image tool is available, so the two PDF-only decodes are **UNVERIFIED**.
- Hand-checks used the PEMS text layer in `pems_chunks/PEMS2024_full.txt` (a different extraction from the tool's `pdftotext -bbox-layout` cache), plus the cache's row/badge pairing where needed for cross-reference. Page and row citations below are to the PEMS 2024 PDF page numbers as printed in the flattened text's `--- PAGE n ---` markers.
- I changed no site files and no code. The only file I wrote is this one.

## 1. Verdict

**FAIL — sign-off blocked.**

Reasons, in order of weight:

1. **Published wrong rows remain, and the report's headline hides them.** "0 fixable mismatches" is true only for the tool's own definition (matched rows with a confident PEMS source). The scanner correctly left 154 UNMATCHED and 37 INFERRED rows alone. I hand-checked 12 of those rows and all 12 are still wrong against PEMS. Several are clinically significant: EMT-level aspirin and nitroglycerin are blocked; EMT-level AED use is restricted to A; A-level IV access is blocked; EMR-level CPR and EMR-level oxygen are blocked; and the Respiratory Distress CPAP row still carries an MC bracket at A and I. The audit (t_d3600e06) missed several of these entirely. The owner must not read "0 fixable mismatches" as "levels correct".
2. **One false-confidence match was applied.** Non-Traumatic Cardiac Arrest row 9 was paired to the wrong PEMS row (p.64 row 1, 150 mg amiodarone) at strong confidence (score 0.672). The correct source is p.64 row 0 (300 mg amiodarone). The level happens to be the same (I), so the cell is right by coincidence, not by evidence.
3. **One applied row rests on an ambiguous decode.** Crush Syndrome row 5 (sodium bicarbonate) was written as `[I]` at I from a single badge token. The PEMS line carries two bracket badges, `[A] [I]`, and the cell was not flagged. Needs a PDF check before it stands.
4. **Correct fixes were refused.** Pediatric Stridor row 4 (oxygen, A→EMR/EMT) and Non-Traumatic Cardiac Arrest row 2 (CPR, EMT→EMR) have clear PEMS matches. Both were held as INFERRED on a text-similarity threshold that the text does not justify. Stridor row 4 is a CRITICAL audit item.
5. **Gating checks are not executed.** Idempotency, the prose/scope diff, the strict build, and the cache-vs-PDF check cannot be claimed without the commands in §7.
6. **Exception list has honesty gaps.** See §5. The biggest is that 99 rows are exempted under an "owner ruling 2026-11-11" that the audit's own reports describe as open and contradictory.

What is good, and should be said plainly: of the 27 applied rows in §2a, 26 have the correct level against PEMS (one of those cites the wrong PEMS row, F1) and 1 is unverified (Crush row 5). The Allergic Reaction over-restriction is fixed (§4 item 7). Completeness at the file-count level holds (59 pages on disk, 59 in the report). The apply path touches only level cells and no rewritten line contains an escaped pipe (`\|` count in `docs/protocols` = 0). The rewrite engine is sound for what it applies. The problem is what it leaves behind, and what the owner is being told about it.

## 2. Hand-check table

Legend: **OK** = current cell matches PEMS as I read it. **WRONG** = current cell does not match PEMS. "Applied" = changed by the tool (changelog.md). "Residual" = not changed by the tool.

### 2a. Rows the tool applied (26 hand-checked)

| # | Site file (docs/protocols/…) | Row | Current cells (EMR·EMT·A·I·P) | PEMS source (p., row, badge) | Result |
|---|---|---|---|---|---|
| 1 | medical/07_Allergic_Reaction | 1 Universal care | •••• • | p.99 row 0, EMR "Follow Universal Patient Care" | OK |
| 2 | medical/07_Allergic_Reaction | 3 Diphenhydramine | · · • • • | p.99 row 2, **A** "Administer: Diphenhydramine" (was I) | OK (I→A) |
| 3 | medical/07_Allergic_Reaction | 7 Epinephrine IM | · • • • • | p.100 row 0, **EMT** "Administer: Epinephrine autoinjector" | OK |
| 4 | medical/07_Allergic_Reaction | 10 Diphenhydramine | · · • • • | p.100 row 3, **A** (was I) | OK (I→A) |
| 5 | medical/07_Allergic_Reaction | 13 Methylpred | · · • • • | p.100 row 6, **A** (was I) | OK (I→A) |
| 6 | cardiac/04_Bradycardia | 3 Atropine | · · · • • | p.103 row 8, **I** "Consider: Atropine" | OK |
| 7 | cardiac/04_Bradycardia | 6 Ped. epi infusion SBP | · · · [I] • | p.104 row 2, **[I]** "Maintain age adjusted SBP" | OK (bracket: I contacts MC, P standing) |
| 8 | cardiac/04_Bradycardia | 7 Push-dose epi | · · · · • | p.104 row 3, **P** | OK |
| 9 | cardiac/04_Bradycardia | 8 Contact MC | MC×5 | p.104 row 4, **MC** | OK |
| 10 | cardiac/04_Cardiac_Arrest_Non_Traumatic (merge p.57/63/64) | 8 Epinephrine | · · • • • | p.63 row 8, **A** "Administer: Epinephrine 1 mg" (was I) | OK (I→A) |
| 11 | cardiac/04_Cardiac_Arrest_Non_Traumatic (merge) | 9 Amiodarone (V-Fib only) | · · · • • | **Level** p.64 row 1, I. **Evidence wrong:** the matching text is p.64 row 0 (300 mg, I). | **F1: level OK, evidence WRONG** |
| 12 | cardiac/04_Cardiac_Arrest_Non_Traumatic (merge) | 11 CaCl / NaHCO₃ | · · · • • | p.64 row 3, **I** "For cardiac arrest in renal dialysis…" | OK |
| 13 | cardiac/04_Cardiac_Arrest_Non_Traumatic (merge) | 13 TOR | MC×5 | p.64 row 5, **MC** "Termination of Resuscitation" | OK |
| 14 | cardiac/04_Cardiac_Arrest_Traumatic | 2 Open airway | · • • • • | p.61 row 3, **EMT** "Open the airway" (was A) | OK |
| 15 | cardiac/04_Cardiac_Arrest_Traumatic | 4 Withhold CPR on asystole | · • • • • | p.61 row 4, **EMT** (same PEMS row as AED, see residual R1) | OK (level) |
| 16 | cardiac/04_Cardiac_Arrest_Traumatic | 7 NS 1 L | · · • • • | p.61 row 5, **A** "Obtain IV/IO access… 0.9% NaCl" (was I) | OK (I→A). See R2 for row 6. |
| 17 | trauma/09_Crush_Syndrome | 4 Continuous albuterol | · · [A] • • | p.91 row 4, **[A]** "Continuous Albuterol" | OK (bracket) |
| 18 | trauma/09_Crush_Syndrome | 5 NaHCO₃ | · · · [I] • | Tool read p.91 row 5, **[I]**. The PEMS line shows `[A] [I]` for this block. | **F11: UNVERIFIED** (PDF) |
| 19 | cardiac/04_Chest_Pain_ACS | 4 12-lead ECG | · • • • • | p.107 row 3, **EMT** "Obtain and transmit 12-Lead ECG" | OK |
| 20 | cardiac/04_Chest_Pain_ACS | 12 Analgesia | · · · • • | p.107 row 8, **I** "Consider analgesia" | OK |
| 21 | cardiac/04_Chest_Pain_ACS | 13 Contact MC (serial ECG) | MC×5 | p.107 row 9, **MC** | OK (was [A]) |
| 22 | general/02_Pain_Control | 3 Monitor BP | · • • • • | p.77 row 2, **EMT** "Assess and monitor blood pressure" | OK |
| 23 | general/02_Pain_Control | 4 Nausea (ondansetron) | · · • • • | p.77 row 3, **A** "Consider treatment for nausea" | OK |
| 24 | respiratory/03_Pulmonary_Edema | 2 Focused assessment | • • • • • | p.123 row 1, **EMR** "Perform a focused evaluation" | OK (C2-02 #4, resolved) |
| 25 | respiratory/03_Pulmonary_Edema | 11 Nitroglycerin 0.4 mg | · · • • • | p.124 row 4, **A** "Administer: Nitroglycerine 0.4 mg SL" (was I) | OK (I→A) |
| 26 | respiratory/03_Respiratory_Distress | 11 Epinephrine nebulized | · · • • • | p.124 row 1, **A** "Administer: Epinephrine 3 mg nebulized" (MC bracket removed) | OK |
| 27 | respiratory/03_Airway_Inhalation_Irritants | 5 Airway management | · • • • • | p.153 row 2, **EMT** "Follow Airway Management and Ventilatory Support" (was A) | OK (C2-02 #2, resolved) |

Applied-row result: **27 applied rows checked. 26 level-correct** (row 11 is level-correct but cites the wrong PEMS row, F1). **1 unverified** (row 18, Crush NaHCO₃, F11). Pass rate on applied rows: 26/27 = 96% on level, with one evidence failure. The Pediatric Stridor and Non-trauma row 2 cases are residual (§2b).

### 2b. Rows the tool did NOT apply, still wrong (12 hand-checked)

| ID | Site file | Row | Current cells | PEMS source | Why it is wrong | Tool status |
|---|---|---|---|---|---|---|
| R1 | cardiac/04_Cardiac_Arrest_Traumatic | 3 Apply AED / monitor | · · • • • (**A**) | p.61 row 4, **EMT** "Apply AED or cardiac monitor. Assess rhythm…" | EMT-level AED blocked to A. Matched PEMS row went to site row 4 (withholding line). | UNMATCHED |
| R2 | cardiac/04_Cardiac_Arrest_Traumatic | 6 IV/IO ×2 | · · · • • (**I, P**) | p.61 row 5, **A** "Obtain IV/IO access" | A-level IV access blocked, while row 7 now gives A-level IV fluids. Internally inconsistent. | UNMATCHED (PEMS row 5 went to row 7) |
| R3 | cardiac/04_Chest_Pain_ACS | 10 Aspirin 324 mg | · · · • • (**I, P**) | p.107 row 5, **EMT** "Administer: Aspirin 324 mg PO chewed" | EMT and A blocked from aspirin for ACS. Audit AUD-0049 fixed the dose and missed the level. | UNMATCHED |
| R4 | cardiac/04_Chest_Pain_ACS | 11 Nitroglycerin | · · · · • (**P**) | p.107 row 6, **EMT** "consider Nitroglycerine 0.4 mg SL" | EMT, A, I blocked from NTG. Audit AUD-0051 fixed the dose and missed the level. | UNMATCHED |
| R5 | cardiac/04_Chest_Pain_ACS | 6 STEMI alert | · · · · • (**P**) | p.107 row 3–4, **EMT** "If 12-Lead reads STEMI… Pre-Hospital STEMI Alert" | EMT blocked from STEMI alert. | INFERRED, not applied |
| R6 | cardiac/04_Chest_Pain_ACS | 7 Serial ECG | · · · [I] • | p.107 row 9, **MC** "…serial ECGs at 10-minute intervals… contact Medical Control" | Should be MC in all five cells. | UNMATCHED |
| R7 | cardiac/04_Cardiac_Arrest_Non_Traumatic | 2 Begin high-quality CPR | · • • • • (**EMT+**) | p.63 row 2 and p.57 row 2, **EMR** "Begin chest compression(s)" | EMR-level CPR blocked. Text match is clear. | INFERRED, not applied (score 0.455) |
| R8 | cardiac/04_Cardiac_Arrest_Non_Traumatic | 5 Defibrillation (V-Fib only) | · • • • • (**EMT+**) | p.63 row 7, **I** "If VF/VT present… immediately defibrillate" (AED for EMR inline) | Manual defibrillation over-authorized at EMT. | UNMATCHED |
| R9 | respiratory/03_Pediatric_Stridor | 4 "High-flow" oxygen | · · • • • (**A**) | p.123 row 2, **EMR** "Provide supplemental oxygen to maintain SpO2 > 94%" | EMR/EMT blocked from oxygen. **CRITICAL** (C2-02). Match is clear. | INFERRED, not applied (score 0.538) |
| R10 | general/02_Pain_Control | 2 Baseline pain assessment | · • • • • (**EMT+**) | p.77 row 1, **EMR** "Assess baseline pain level using scale below" | EMR blocked from baseline pain assessment. | INFERRED, not applied |
| R11 | respiratory/03_Respiratory_Distress | 6 CPAP | · · MC MC · (**MC at A, I; blank EMT, P**) | p.123 row 3, **EMT** "Consider non-invasive (CPAP)…" | Standing EMT+ per PEMS; site has MC at A/I and blocks EMT. **CRITICAL** (AUD-0148). | UNMATCHED |
| R12 | respiratory/03_Smoke_Inhalation | 3 Airway assessment | · • • • • (**EMT+**) | p.87 row 2, **EMR** "Assess airway and respiratory effort" (Burns page, not in Smoke's forced sources) | EMR blocked. Correct PEMS source is outside the page's declared sources. | UNMATCHED |

Residual result: **12 of 12 still wrong.** The tool did not write a wrong cell in these cases, but the tool did not fix them either.

### 2c. Pass rate

- Applied rows hand-checked: 27. Level-correct: 26 (includes F1, whose cited evidence is wrong). Unverified: 1 (F11). Level pass rate 26/27 = 96%.
- Residual rows hand-checked: 12. Still wrong: 12/12.

## 3. Conservative matching (task 3)

**Refused correctly, spot-checked:** Crush row 6 (CaCl, P-only) UNMATCHED; Pain Control row 6 UNMATCHED because the one PEMS `[A]` block was split across two site rows and the tool paired it to row 7; Cold Exposure row 8 (transport EMR) held INFERRED with "expected cells REMOVE a currently authorized level"; Cardiac Arrest Non-Trauma row 5 UNMATCHED. The removal guard (line 698) and the many-to-one behaviour are working as designed.

**Refused where it should have accepted (false negatives):** R7 Non-trauma row 2 (score 0.455), R9 Stridor row 4 (score 0.538), R10 Pain row 2 (score 0.45). The text similarity is low because the site rows are long bullet lists. The PEMS row text is short and the verb is the same. A threshold change is not the fix. An explicit pems_row declaration in exceptions.yaml, reviewed by a human, is.

**False-confidence matches (applied at strong confidence, evidence wrong or doubtful):**
- **F1** Non-trauma row 9 → p.64 row 1 (150 mg) instead of p.64 row 0 (300 mg). Score 0.672, strong. Level I matches both, so no level is wrong today. But the citation is wrong, and the cause is structural: the monotonic alignment assumes site row order equals PEMS row order. On this merged page the site order (epi → amiodarone → fluids → CaCl) does not follow PEMS order (p.57 CaCl is earlier than p.63/64 amiodarone). The same risk applies to any merged page.
- **F11** Crush row 5 → single badge `[I]` from a two-badge PEMS line. Not flagged, and the `expected_cells` multi-badge guard did not fire because the tool read one token. Needs PDF check.

Count of applied rows with score < 0.6 that I could not individually check: not enumerated. Score list in findings.json shows 65 rows in the 0.55–0.74 band (lines 2029–15280). A developer should list every applied row under 0.65 and check its PEMS page.

## 4. Known Allergic Reaction over-restriction (task 7)

**Resolved and correct.** Changelog.md lists rows 3, 4, 5, 6, 10, 11, 12, 13 on `07_Allergic_Reaction_Anaphylaxis_PROC.md` moved from `· · · • •` (I) to `· · • • •` (A). I read the file and PEMS p.99–100:

- Rows 3, 4, 5, 6 → p.99 rows 2–5, badge A. OK.
- Rows 10, 11, 12, 13 → p.100 rows 3–6, badge A. OK.
- Row 7 (epi IM) → EMT (p.100 row 0). OK.
- Row 8 (IV access) → A (p.100 row 1). OK.
- The `[I]` and `P` epinephrine-infusion and push-dose rows on p.101 are not on the site page at all. The tool reports them as "PEMS rows with no site counterpart" and did not create them. That is correct behaviour, but the Anaphylaxis severe half is still missing I and P content (AUD-0088–0091, CRITICAL). The owner should know the page is incomplete, not just mis-levelled.

## 5. Exceptions honesty (task 4)

Read line by line against `exceptions.yaml` (144 lines). Assessment:

| Entry | Assessment |
|---|---|
| 14 `kind: administrative` pages + `front-matter/01 - How to Read` (99 rows) | **Honest in form, unresolved in substance.** The reason cites "owner ruling 2026-11-11". The audit's own `RECONCILIATION_REPORT.md` (line ~25) and `NARRATIVE.md` (lines 25, 43) say that ruling is **open**: one reading is "not level-gated", the other is "applies to all levels", and the site's 88 blank admin cells contradict the second. The scanner has picked the first reading without stating that the audit flagged it as undecided. These 99 rows are now unverified by anything. **Owner must confirm the ruling in writing before the exemption stands.** |
| Cardiac Arrest Non-Traumatic `pems_pages: [57, 63]` "deliberate MERGE" | Legitimate declaration, but the page exposes the alignment problem in F1. Should carry an explicit `rows:` pems_row map for rows 8, 9, 11, 13 instead of relying on order. |
| Pneumothorax `pems_pages: [243]` | **Misleading.** p.243 has no level badges, so the forced source yields zero rows and all 15 rows are UNMATCHED. The exception reads as if a source exists. Should be declared as "no regional level grid". Residual: row 13 (advanced airway, P-only; audit says I) remains wrong. |
| Aortic Dissection 04b | **Undeclared.** No exception entry, so the 11 rows are simply UNMATCHED with no PEMS source. The four EMR+ rows (1–4) are local content with no regional source and should be declared `local`. |
| Lightning Injuries → p.96 (Electrical) | Acceptable with a note. There is no PEMS lightning protocol; the page's 9 rows are checked against the electrical page, which is the closest governing source. "9 of 9 ok" here means "matches electrical injuries", not "matches a lightning protocol". |
| Stridor, Asthma, Respiratory Distress, Pulmonary Edema → p.123–124 | Plausible. Each reason states the regional section that carries the content. Note R9 (Stridor row 4) is refused under this declaration, which makes the declaration hide a clear CRITICAL miss rather than document a deliberate one. |
| SVT row 16 `kind: skip` | **Weak reason, hides a bare-MC row.** The reason is "flattening that to MC in all five cells would restate the whole ladder". That is a tooling convenience, not a clinical reason. The cell is `[P]` only, so EMR–I cannot contact OMD for a failed-cardioversion escalation at all. This is an owner decision and should be recorded as one, not as a silent skip. |
| Row-level declarations for SVT rows 3, 11 (dividers) and Allergic dividers | Legitimate. Divider rows authorize nothing; I confirmed the labels. |

## 6. Completeness and build (tasks 5–6)

**Completeness (partly verified):**
- `docs/protocols` contains 59 `.md` files. The report's "pages on disk: 59" matches.
- The report says 57 pages carry a level table. The two without a table, by file name, are `front-matter/00 - Introduction.md` and `front-matter/00 - AI Formatting Guidelines.md`. These are not protocols. The report does not name them. Minor.
- My grep cross-check for the exact header `| EMR |` returned 55 files, not 57. The two I could not reconcile are `Universal Patient Care.md` and `01 - How to Read the Protocols.md`, which the tool reports as having tables. Developer should confirm the header parse for those two.

**Build:** **NOT EXECUTED — needs developer.** The builder's card reports `mkdocs build --strict` exit 0 with 6.58 s and a pre-existing MkDocs-2 deprecation notice. That is a summary, not evidence I can cite.

## 7. Commands the developer must run to close this review

Run from `/root/projects/pfd-resources-and-quick-references`, on branch `level-scan`, with `git status --porcelain` empty first:

```
# A. Idempotency (task 2)
git status --porcelain --untracked-files=no          # expect empty
python3 scripts/pems_level_scan.py --apply; echo EXIT=$?
git diff --stat                                      # expect: no output (0 changes)
python3 scripts/pems_level_scan.py --apply; echo EXIT=$?
git diff --stat                                      # expect: no output
# (if the first --apply changes the tree, the tree was not idempotent: FAIL)

# B. Scope: every changed line must differ only in level cells (task 2 of the addendum)
git diff ef540f9^ ef540f9 -- docs/protocols | grep '^[-+]' | grep -v '^+++\|^---' > /tmp/changed.txt
#   Then check: every -/+ pair has identical text in column 1 (#) and column 2 (action), differing only in cols 3–7.
#   A single prose-line change is a FAIL on scope.

# C. Strict build (task 5)
/root/pfd-ssg-env/bin/mkdocs build --strict; echo EXIT=$?

# D. Report vs changelog (task 3 / count)
python3 scripts/pems_level_scan.py --report; echo EXIT=$?   # expect 1 (residual UNMATCHED)
wc -l audit/level-scan/changelog.md                          # expect 216 data rows (+header)

# E. Fixlist ID collisions (addendum item 3)
grep -n 'C2-02' audit/protocol-reconciliation/work/batch-C2.fixlist.md   # expect 4 lines, not 3
grep -n 'C2-02' audit/protocol-reconciliation/work/batch-C2.fixlist.md | cut -d: -f1 | wc -l

# F. PEMS cache vs PDF (addendum item 1)
pdftotext -bbox-layout "/root/System/mindpalace/40 - areas/Paramedic/PEMS2024.pdf" /tmp/pems_fresh.xml
cmp /tmp/pems_fresh.xml audit/level-scan/.cache/pems_bbox.xml; echo EXIT=$?
pdftoppm -r 200 -f 124 -l 125 -png "/root/System/mindpalace/40 - areas/Paramedic/PEMS2024.pdf" /root/.hermes/profiles/reviewer/cache/scratch/pems
#   then send the PNGs to a vision-capable reviewer to decode: p.125 pearl tail (Respiratory Distress); p.124 CPAP/PEEP range (Pulmonary Edema, "9%-15mmHg" — confirm the real upper bound).
```

Not executed by me: A, B, C, D, E, F. The pdftoppm render in F is needed to close the two UNVERIFIED decodes; I could not do it.

## 8. Remaining work (ordered by clinical weight)

Blocking before sign-off:

1. **Hand-correct the EMT-level blocks with PEMS citations (R1, R3, R4, R7, R9, R11).** Aspirin and NTG at EMT (Chest Pain rows 10–11); AED at EMT (Trauma Cardiac Arrest row 3); CPR at EMR (Non-trauma row 2); oxygen at EMR (Stridor row 4, CRITICAL); CPAP standing EMT+ (Respiratory Distress row 6, CRITICAL). These are changes the scanner refused and the audit missed or mis-levelled. A human must make and cite them.
2. **Resolve F1 (Non-trauma row 9 evidence) and F11 (Crush row 5 two-badge line).** Declare pems_row explicitly in exceptions.yaml for merged pages, and PDF-check the Crush line. Revert F11 if the PDF shows `[A] [I]`.
3. **Resolve the admin-ruling scope** (99 rows, 88 blank admin cells). Owner must state in writing whether "not level-gated" or "all levels" governs admin rows.
4. **Decide SVT row 16 as an owner matter**, not a skip. Record the decision either way.
5. **Fix the exception entries** for Pneumothorax (no level grid, not a forced source) and Aortic Dissection (undeclared local content).
6. **Run §7 A–F.** Idempotency, scope diff, strict build, fixlist collision count, and the cache-vs-PDF check are not proven.
7. **Render and decode the two PDF items** (RD p.125 pearl tail; CPAP PEEP range on p.124). Until then, mark them UNVERIFIED in any published content.

Non-blocking:

8. `needs-authoring.md` header says it holds "clinical-prose, dose, contraindication, destination" items only. It holds dozens of level items too (e.g. AUD-0016, AUD-0030, AUD-0148). Correct the header, or the owner will think level work is all done.
9. `C2-02` appears four times in `batch-C2.fixlist.md` (lines 4, 14, 23, 34), not three. The four targets are Smoke row 3 (EMR, sourced to Burns p.87), Airway Irritants row 5 (EMT, correct and applied), Stridor row 4 (EMR, refused, R9), and Pulmonary Edema row 2 (EMR, correct and applied). The scanner keys by PEMS row, not by ID, so no edit was misapplied. But anywhere the audit keys by ID, these four must be disambiguated by (file, row).
10. The report's Pages table silently omits the two table-less front-matter pages. Name them.
11. Confirm no `\n` / trailing-whitespace normalization on rewritten lines (§7-B covers this).

## 9. What I did not verify, stated plainly

- Idempotency (task 2): **not executed**.
- Strict build (task 5): **not executed**.
- Prose/scope diff against the git base (addendum 2): **not executed**. I confirmed the changelog lists only level cells and that no escaped-pipe lines exist, but I cannot exclude whitespace or newline changes without the diff.
- Full inferred-row cross-check (addendum 2, last bullet): 37 INFERRED rows are reported. I confirmed three of them (Cold row 8, Pain row 2, V-Fib row 5) are absent from the changelog, so they were not applied. I did not check all 37.
- PDF raster decodes (addendum 1): **UNVERIFIED**.
- Score-band check (task 3): 65 applied-candidate scores in the 0.55–0.74 band were not individually checked.
