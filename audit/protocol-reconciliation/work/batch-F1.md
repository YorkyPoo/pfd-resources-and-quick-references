# Batch F1 — Administrative triage/transport policies vs PEMS2024 (read-only audit)

Parent: t_d3600e06 · Task: t_d207d8a0 · Reviewer audit, no files under `docs/`, the vault or scripts were edited.
Administrative protocols are not level-gated (doctrine). Level-gating differences are not counted, because the PEMS pages here assign no levels.
Quotes are verbatim excerpts from the flattened PEMS text (`pems_chunks/PEMS2024_full.txt`) or the site Markdown; "…" marks an omitted middle. Full verbatim quotes are in `batch-F1.json`.
Tool limitation: the read tool cuts each long PEMS line at about 2,000 characters. Lost text is marked below. The PDF cannot be text-extracted (pages 47 and 151 need OCR), and file URLs are blocked for web_extract. Three protocols are therefore MANUAL with `verified=false`.

## Totals

| Protocol | Status | Verified | CRITICAL | MODERATE | MINOR | Total |
|---|---|---|---|---|---|---|
| Stroke Field Triage | FIXABLE | true | 0 | 1 | 4 | 5 |
| Transportation & Destination Determination | MANUAL | false | 2 | 1 | 2 | 5 |
| Behavioral Health Transportation Decision | FIXABLE | true | 5 | 2 | 0 | 7 |
| STEMI Field Triage | FIXABLE | true | 0 | 2 | 2 | 4 |
| Patient Refusal of Treatment/Transport | MANUAL | false | 1 | 4 | 1 | 6 |
| Helicopter EMS (HEMS) | FIXABLE | true | 0 | 1 | 1 | 2 |
| Abuse Recognition & Mandated Reporting | MANUAL | false | 0 | 5 | 1 | 6 |
| **Batch total** | | | **8** | **16** | **11** | **35** |

Count reconciliation: 35 discrepancies in JSON = 35 table rows in this file = 35 lines in `batch-F1.fixlist.md`. Severity totals 8 + 16 + 11 = 35. Inferred-level items: 2 (F1-15, F1-34), both flowchart or bullet-structure readings of flattened text.

---

## 01_Stroke_Field_Triage_PROC.md
Coverage: PEMS p.37 read in full (lines 219–231). Site Rows 1–8 and Pearls 1–3 checked. Routing branches decoded from the flattened flowchart; site Rows 5–6 match that reading.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F1-01 | 2 | Threshold (glucose) | "Assess blood glucose. Is glucose greater than 60?" | "**Diagnostics:** Assess blood glucose. If < 60 mg/dL, treat per Hypoglycemia protocol." | MODERATE | Change to "If 60 mg/dL or less, treat per Hypoglycemia protocol" (matches the site's own Differential "Must be > 60"). |
| F1-02 | 1 | Site-only directive (scene time) | (absent from p.37) | "**Time Management:** Maintain a goal scene time of less than 15 minutes." | MINOR | Remove, or footnote as an agency target. |
| F1-03 | 3 | Site-only tool (BEFAST) | "evaluate the patient using the RACE exam" | "Evaluate patient using **BEFAST** criteria and **RACE** scale." | MINOR | Keep RACE as the trigger; label BEFAST as an adjunct. |
| F1-04 | Pearl 2 | Site-only pearl (family contact) | (absent from p.37) | "Gather family contact info and provide it to the receiving facility for immediate consent and history needs." | MINOR | Remove, or source to agency policy. |
| F1-05 | 8 | Missing MC instruction | "If you have questions contact local medical control." | "Early notification to Medical Control and/or Stroke Center. During transport, call COR with Name and DOB for rapid registration." | MINOR | Add "If you have questions, contact local Medical Control." |

No discrepancies in: RACE ≥ 1 alert (Row 7), COR Name/DOB call (Row 8), 5-hour routing logic (Rows 5–6), 30-minute PSC fallback.

## 01_Transportation_and_Destination_Determination_PROC.md
Coverage: **PEMS p.39 is a single flattened line (line 240) that the tool cut off** after step 3 ("…documented on the Pati…"). Items 1.a–1.e, step 2, and the start of step 3 were readable. Not readable: the rest of step 3, everything after it on p.39, and the "*" footnote. Site Rows 6–7 and Pearls 3–5 (HEMS > 10-min rule, Poquoson OMD alternate destinations, internal agency policy) cannot be checked. **MANUAL, verified=false.**

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F1-06 | absent | Missing row (1.e emergent to closest) | "e. The patient requires EMERGENT transport to the closest hospital when, in the judgment of the AIC, the patient is unstable due to one or more of the following conditions: i. Inability to establish or maintain a protected airway … viii. Any other life-threatening condition the AIC believes to be time critical" | "(absent)" | CRITICAL | Add a row: unstable patient (i–viii) → EMERGENT transport to the CLOSEST hospital. |
| F1-07 | Pearl 2 | Meaning changed (routing) | "e. … EMERGENT transport to the closest hospital …" | "**Time-Critical Exceptions:** STEMI, Stroke/CVA, and other life-threatening conditions the AIC believes to be time critical override patient hospital preference to ensure specialized care." | CRITICAL | Split the pearl: unstable (1.e) → closest hospital; STEMI/stroke/trauma/burn → specialized destination. |
| F1-08 | absent | Missing rows (trauma, burn) | "c. Th patient exhibiting … i.e. a trauma center d. The patient exhibiting … should be transported to a burn center." | "(absent) — rows 2–3 cover STEMI and stroke only" | MODERATE | Add trauma-center and burn-center exception rows, cross-referenced to Trauma Field Triage. |
| F1-09 | 2 | Plan name | "the patient destination should be consistent with the PEMS Regional STEMI Plan, i.e. a STEMI Receiving Center." | "Transport to STEMI Receiving Center per Poquoson Regional STEMI Plan" | MINOR | "PEMS Regional STEMI Plan". |
| F1-10 | 3 | Plan name | "the patient destination should be consistent with the PEMS Stroke Triage Plan, to a designated stroke center." | "Transport to designated stroke center per Poquoson Stroke Triage Plan" | MINOR | "PEMS Stroke Triage Plan". |

Matches: Row 1 (patient choice), Row 4 (closest most appropriate hospital if no preference), Row 5 (document reason for change).

## 01_Behavioral_Health_Transportation_Decision_PROC.md
Coverage: PEMS p.41 read in full (lines 246–261). The page has no running header in the flattened text, so it was identified by title and content. Algorithm Yes/No columns are not aligned in the flattened text; branch order is inferred (F1-15).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F1-11 | absent | Missing Physical Exam gate | "Physical Exam Temp greater than 100.4 HR less than 50 or greater than 120 BP less than 90 or greater than 180 RR less than 12 or greater than 28 Glucose less than 70 mg/dL or greater than 350 Loss of Consciousness Any Stroke or TIA Symptoms? Does the patient require supplemental oxygen or airway support?" | "(absent)" | CRITICAL | Add the physical-exam criteria block verbatim before the direct-transport step. |
| F1-12 | absent | Missing exclusion (trauma/strangulation) | "No significant Trauma? No strangulation injury?" | "(absent)" | CRITICAL | Add both criteria. |
| F1-13 | absent | Missing exclusion (sedation) | "Has the patient been chemically sedated?" | "(absent)" | CRITICAL | Add the criterion. |
| F1-14 | absent | Missing eligibility (age 5–60) | "Is the patient between ages of 5 and 60?" | "(absent)" | CRITICAL | Add the age criterion; outside range → appropriate ED. |
| F1-15 | absent | Missing pregnancy branch (**inferred**) | "Is the patient pregnant? Contact RMHRC Med Control Provide the following information: Gestational age Presence or absence of prenatal care Presence or absence of abdominal pain Presence or absence of bleeding" | "(absent)" | CRITICAL | Add the pregnancy branch; eyeball the PDF flowchart first. |
| F1-16 | 2 | Destination not named | "Consider Direct Transport to BH Center -Contact RMHRC or CHKD" | "**Direct Transport:** Once identified, consider direct transport to a Mental Health Facility." | MODERATE | Name RMHRC and CHKD as contacts (CHKD (757) 668-8000 per PEMS Communications; no RMHRC number in readable text). |
| F1-17 | absent | Missing default disposition | "Transport to appropriate ED" | "(absent)" | MODERATE | Add: "If any criterion is not met, transport to the appropriate ED." |

Not counted: Rows 4–7 (ECO, medical ECO, LE custody, LE accompaniment) are sourced from PEMS Refusal p.28–29 and Restraint, not p.41. Row 6 ("MUST have LE present") and Row 7 ("SHOULD accompany") could not be checked against readable text.

## 01_STEMI_Field_Triage_PROC.md
Coverage: PEMS p.35 read in full (lines 202–212). Decision tree decoded from the Yes/Yes/No/No ordering. All 11 receiving-center phone numbers and the surgical column match the PEMS lists except the Mary Washington second number.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F1-18 | 2 | Criteria (machine ACUTE MI omitted from row) | "Cardiac symptoms AND • 12-lead ECG criteria of 1 mm (or more) ST elevation in 2 (or more) contiguous leads OR • 12-lead ECG interpretation with an “ACUTE MI” statement" | "Identify STEMI based on cardiac symptoms AND 1mm+ ST elevation in 2+ contiguous leads." | MINOR | Add the OR machine "ACUTE MI" branch (the Decision Scheme section already has it). |
| F1-19 | 3 | Threshold boundary (gap at exactly 30) | "PCI Capable hospital within 30 minutes EMS transport Time?" / "…closest PCI center within 30 minutes EMS transport time." | "Transport to the closest PCI capable facility if EMS ground transport time is < 30 minutes." | MODERATE | Use "<= 30" for row 3 and "> 30" for row 4. |
| F1-20 | 4 | Action verb (evaluate vs activate) | "Activate Helicopter EMS (HEMS) Transport to Closest Listed PCI Capable Hospital w/ Surgical Capabilities" | "If ground transport to a PCI facility is > 30 minutes, evaluate Helicopter EMS (HEMS) transport within 30 minutes." | MODERATE | "Activate" HEMS when within 30 min; destination = closest listed PCI with surgical capability. |
| F1-21 | table | Secondary phone omitted | "Mary Washington Hospital (REMS) @ (540) 373-0348 Or (540) 741-4768" | "| Mary Washington Hospital (REMS) | (540) 373-0348 |" | MINOR | Add (540) 741-4768. |

Not counted: "Pre-Hospital STEMI Alert" wording and the Name/DOB pearl are sourced from PEMS Chest Pain (out-of-batch line 615). Row 7 (serial ECG q10 min) and Pearl 3 (printed ECG copy) are not on p.35 and could not be checked in-batch. The site's P-only Row 2 is level-gated and not counted (PEMS p.35 assigns no levels).

## 01_Patient_Refusal_of_Treatment_Transport_PROC.md
Coverage: PEMS p.27–29 (lines 163–175) read through the DNR section and the pearls. **Two tool-truncated tails:** line 170 after "contact law enforcement regardi…" (end of the psychiatric-ECO sentence), and line 175 after the minor-treatment clause "…no authorized person …" (the 14+ consent step). Site Row 7 and Pearl 4 are not verifiable. **MANUAL, verified=false.**

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F1-22 | absent | Missing DNR / cardiac-arrest section | "For patients in cardiac arrest: • A DNR/DDNR/DNAR (Do Not Resuscitate) is applicable ONLY if the patient is in cardiac arrest. … If there is any doubt as to the applicability or validity of a DNR or other advanced directive belonging to a patient in cardiac arrest, begin CPR and contact Medical Control immediately for guidance." | "(absent — no DNR, DDNR, POST/POLST/MOLST, living-will or revocation content)" | CRITICAL | Add the PEMS DNR block verbatim, including "begin CPR and contact Medical Control immediately". Cross-reference Death & Criteria. |
| F1-23 | 2 | Criterion meaning (consider vs exclude) | "Assess for and take into consideration any condition which may impair decision making capacity such as acute or chronic psychiatric illness, acute drug or alcohol intoxication, CVA, hypotension, hypoglycemia, hypoxia, head trauma…" | "No condition present which may impair decision-making capacity" | MODERATE | Reword to "Assess for and consider any condition that may impair capacity". |
| F1-24 | 3 | Missing required step (surrogate capacity) | "Ensure the surrogate decision maker has clinical decision-making capacity (see above)" | "Identify appropriate surrogate decision maker (in descending order) if the patient lacks capacity or competence." | MODERATE | Add the surrogate-capacity check. |
| F1-25 | 4 | Qualifier dropped | "obtain signatures from the patient or authorized surrogate decision maker and at least one adult witness, when possible." | "obtain signatures for refusal from patient or surrogate and at least 1 adult witness." | MINOR | Add "when possible". |
| F1-26 | absent | Missing pearl (in loco parentis) | "In the absence of available parents, an adult in whose care a minor has been entrusted, such as a teacher or caregiver, may act as a surrogate decision maker in the place of a parent (“in loco parentis”)." | "(absent)" | MODERATE | Add the pearl verbatim. |
| F1-27 | Pearl 3 | Minor-consent rule narrowed/misstated | "A minor shall be deemed an adult for the purpose of consenting to: … venereal disease … birth control, pregnancy or family planning … outpatient … substance abuse … outpatient … mental or emotional disturbance • A pregnant minor shall be deemed an adult for the sole purpose of giving consent for herself and her child…" | "**Minor Exceptions:** A minor may be deemed an adult for the purpose of giving consent to surgical and medical treatment for her child." | MODERATE | Replace with the PEMS deemed-adult list and pregnant-minor rule verbatim. |

## 01_Helicopter_EMS_HEMS_PROC.md
Coverage: PEMS p.23 read in full (lines 145–146). Site Rows 1–6 and Pearls 1–2 checked; all matched except the two findings below.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F1-28 | absent | Indications presented as closed list | "Patients meeting specialty care criteria including but not limited to:" | "=== \"History of Present Illness\" - STEMI - Stroke - Trauma - Burns - Critical Pediatrics - Ventricular Assist Device (LVAD/BiVAD/VAD)" | MODERATE | Restore "including but not limited to". |
| F1-29 | 4 | Site-only qualifier | "Trauma patients should be fully immobilized. IV/IO access should be established as time allows." | "**Prepare Patient:** … **IV/IO** access should be established as time allows (within provider scope)." | MINOR | Remove "(within provider scope)" or footnote it. |

## 01_Abuse_Recognition_and_Mandated_Reporting_PROC.md
Coverage: PEMS p.11–13 (lines 87–98) read. **Two tool-truncated tails:** line 88 after "Emotional/mental injury - the infliction of anguis…" and line 93 after "…must report the situation immediately to the local department of social services in t…". Site steps 1–3 are generic assessment content, not counted. **MANUAL, verified=false.**

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F1-30 | 5 | Timing and locality (child report) | "Mandated reporters must report the situation immediately to the local department of social services in the locality where the child resides or where the abuse is believed to have occurred or make reports to the 24-hour, toll-free Virginia Department of Social Services (VDSS) Child Protective Services (CPS) hotline." | "**Report Child Abuse:** Notify local DSS or Child Protective Services (CPS)…" | MODERATE | Add "immediately" and the locality rule or the 24-hour hotline. |
| F1-31 | Pearl 2 | Phone (CPS hotline missing) | "Child abuse and/or neglect 800-552-7096 § 63.2-1509" | "Pearl 2: APS 888-832-3858; DGIF 804-367-1258 or 804-367-2251. (no CPS number)" | MINOR | Add 800-552-7096. Rated MINOR per the phone rule, but it is the only child-abuse reporting line. |
| F1-32 | 4 | Required recipient (LE omitted for elder abuse) | "Mandated reporters must report the following to Adult Protective Services and law enforcement:" | "**Report Elder Abuse:** Notify local DSS or Adult Protective Services (APS). If imminent danger … report to medical examiner and law enforcement." | MODERATE | Report to APS and law enforcement. Rated MODERATE under the batch rule (non-clinical). A human may escalate for legal exposure. |
| F1-33 | 4 | Timing (elder report) | "Mandated reporters must report the situation immediately to the local department of social services in t…" | (same as F1-32, row 4) | MODERATE | Add "immediately". |
| F1-34 | 4 | Trigger scope (**inferred**) | "Suspected sexual abuse, death, serious bodily injury or disease believed to be the result of abuse or neglect; applies to an adult 60 years of age or older…" | "**Report Elder Abuse:** … If imminent danger of death/serious injury or death occurred…" | MODERATE | Match the PEMS trigger list (no "imminent" qualifier; add suspected sexual abuse). The bullet placement is inferred, so eyeball the PDF. |
| F1-35 | 6 | Timing (hunting) | "…shall immediately give notice of the incident to the Department of Game and Inland Fisheries." and "EMS providers are required to report the event to the Department of Game and Inland Fisheries within five days of the incident" | "**Hunting Reporting:** Must report within 5 days to Dept of Game and Inland Fisheries (DGIF)." | MODERATE | Add the statutory "immediately" notice alongside the 5-day report. |

Matches: APS 888-832-3858; DGIF 804-367-1258 / 804-367-2251; statute citations; Class 4 misdemeanor; child-penalty pearl; PCR "made notification to Dr." documentation; attending-physician reporting when transporting; elder age criteria.

---

## Cross-cutting notes
1. **Existing report contradicts this audit.** `docs/protocols/administrative/transport_destination_report.json` says `"status": "VERIFIED"` with zero discrepancies for Transportation & Destination Determination. The PEMS text supports two CRITICAL and one MODERATE routing discrepancies in the readable part. Treat that report as superseded.
2. **Chunk files are unusable.** `pems_chunks/Stroke.txt`, `Patient_Refusal.txt`, `Abuse_Recognition.txt` and the other per-protocol chunk files contain only the Table of Contents page. Use `PEMS2024_full.txt`.
3. **PEMS lines truncated by the read tool:** p.11 (line 88), p.12 (line 93), p.28 (line 170), p.29 (line 175), p.39 (line 240). A human must eyeball PDF pages 11–13, 28–29 and 39 before the MANUAL protocols are edited. PDF text extraction fails (pages 47 and 151 need OCR).
4. Level-gated site cells in these administrative protocols were not counted (doctrine). The one level-based observation (STEMI row 2, P-only interpretation vs PEMS Chest Pain I+P) belongs to the cardiac batch.
