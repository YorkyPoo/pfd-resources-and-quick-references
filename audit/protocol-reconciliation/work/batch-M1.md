# Batch M1 — PEMS2024 vs site, independent second pass (parent t_d3600e06, task t_de5dc8e6)

READ-ONLY audit. No shell, no PDF raster. All PEMS text read from `pems_chunks/PEMS2024_full.txt` (flattened); level decode per `00_method_and_notes.md`.

Totals: **92 discrepancies** — CRITICAL 24 · MODERATE 53 · MINOR 15.
Protocols: 5 (Allergic, Bradycardia, Chest Pain, Hypertensive Crisis, Hypoglycemia). Status: all 5 FIXABLE. Allergic is verified=false (pearl tail unreadable); the other 4 are verified=true. No MANUAL protocols.
Inferred level reads: 3 (M1-AL-16, M1-BR-12, M1-CP-11). Human PDF check required before the developer edits any of them.

---

## Corrections to the author's draft (work/00_method_and_notes.md)

Draft findings are hypotheses. Result of re-derivation:

- **Allergic:** F-AL-01..13 all CONFIRMED (rows 1-13, doctrine rows 3,4,5,6,10,11,12,13 confirmed I-vs-A). F-AL-14 confirmed but split into four findings (M1-AL-14 adult infusion, -15 pediatric [I] infusion, -16 push-dose P, -17 MC row). Push-dose P is the only inferred one. Draft omitted all PEMS pearl gaps (M1-AL-18..21), added.
- **Bradycardia:** F-BR-01/02/04/05/06/07/09/10/11/12/14/15 CONFIRMED. F-BR-03 RE-RATED MODERATE → CRITICAL (pediatric compressions for unconscious hypotensive bradycardic child is a time-critical life-saving step omitted). F-BR-08 (row 2 monitor I, site I+P) and F-BR-16 (atropine doses) CONFIRMED NO FINDING. Draft omitted pearls/p.105 content (M1-BR-14..18), added.
- **Chest Pain:** draft findings confirmed (rows 1, 2, 4 ECG, 5, 6, 7, 9, 10 level and dose, 11 level and dose, 12, 13, 14, nitrate contraindication). RE-RATED: hypotension referral MINOR → MODERATE (M1-CP-04); "unstable patient to nearest ED" pearl MODERATE → CRITICAL (M1-CP-26). ADDED: mandatory PCI-transport wording softened to "consider" (M1-CP-10, CRITICAL); transmit window 10 min vs PEMS 5 min (M1-CP-06); unsourced EtCO2/SpCO (M1-CP-07); site-only IV/IO row (M1-CP-12, MINOR, previously "ignore"); pearls minimize scene time, HEMS, serial ECG <1 h (M1-CP-21..23). SpO2 target (M1-CP-03) was in the draft and is confirmed.
- **Hypertensive Crisis:** draft rows 1, 2 (site row 3), 3 (site row 4), 4 (site row 5), 5 (site row 6) CONFIRMED as MODERATE. Row 7 MC matches (no finding). RE-RATED: epistaxis pearl MINOR → MODERATE (M1-HT-11). ADDED: unsourced site row 2 Primary Assessment (M1-HT-06, MINOR) and other site-only scope (HT-07..09, MINOR), title naming (HT-13, MINOR).
- **Hypoglycemia:** draft rows 1-5 and pearl findings CONFIRMED. Row 2 CRITICAL, row 3 CRITICAL, row 4 CRITICAL, row 5 MODERATE. ADDED: recurrent-hypoglycemia risk list (M1-HG-10, MODERATE), which the draft missed. D10-over-D50 kept as MINOR (M1-HG-11): the Dextrose monograph (p.177) says only "use appropriate concentration", so no explicit D10 rule exists in PEMS.

## Bracket decode note: PEMS "[ I ]" on the pediatric infusion row (allergic p.101; bradycardia p.104 and hypotension p.114 share the same text)

- The token pattern is `I [ I ] Maintain age adjusted SBP ... PEDIATRIC: Epinephrine 0.1-1 mcg/kg/min`. The adult row's trailing `I` and the pediatric row's leading `[ I ]` are adjacent, so the pediatric row is **[I]**: I must contact MC; P and above standing; EMR/EMT may not perform.
- The following `[ I ] P To maintain MAP > 65 ... Push dose` has the bracket adjacent to the pediatric row's tail and `P` adjacent to the push-dose text. Read as **P (inferred)**. PDF eyeball required (flagged as inferred in M1-AL-16 and M1-BR-12).
- Site effect: bradycardia and allergic sites have no pediatric epinephrine infusion row at all, so the MC bracket is absent (CRITICAL M1-AL-15, M1-BR-11).

## Coverage gap (honest report)

- **Allergic, PEMS p.101 line 584:** the reader truncates the pearl line at "Stop the infusion immedi...". The remainder of that pearl and any later pearls on p.101 could not be read with the available tools (no shell, no PDF raster). Allergic protocol is therefore `verified: false`. Pearl tail check needed from the PDF.
- All other protocols: PEMS pages read completely. Bradycardia p.104-105, chest pain p.107-108, hypertension p.109 and hypoglycemia p.111-112 pearls read in full.

---

## docs/protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md

Coverage: PEMS p.99-101, rows 1-13 + infusion/push/MC rows 14-17 + pearls. Site rows 1-13 compared; rows 14-17 absent. verified=false (pearl tail, see above).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| M1-AL-01 | 1 | Provider Level | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care / Initial Patient Contact protocol." (EMR blank) | MODERATE | Set EMR bullet on row 1. |
| M1-AL-02 | 2 | Provider Level | "EMT Remove stinger if present." | "Remove stinger if present." (EMR, EMT blank) | MODERATE | Set EMT bullet on row 2. |
| M1-AL-03 | 3 | Provider Level | "A Administer: ADULT: Diphenhydramine (Benadryl) 50 mg IV/IO slow push or IM" | "Antihistamine Administration: ADULT Diphenhydramine 50 mg" (I, P only) | MODERATE | A bullet on row 3. Doctrine confirmed. |
| M1-AL-04 | 4 | Provider Level | "A A If wheezing is present, administer: ADULT: Albuterol sulfate (Proventil) 3 mL of 0.083%" | "Bronchodilator (Wheezing): ADULT & PEDIATRIC Albuterol..." (I, P) | MODERATE | A bullet on row 4. |
| M1-AL-05 | 5 | Provider Level | "A A If wheezing is present, administer: ADULT: Ipratropium bromide (Atrovent) 3 mL" | "Anticholinergic (Wheezing): ADULT & PEDIATRIC Ipratropium..." (I, P) | MODERATE | A bullet on row 5. |
| M1-AL-06 | 6 | Provider Level | "A A Consider: ADULT: Methylprednisolone Succinate (Solu-Medrol) 125 mg slow IV push." | "Consider administering: ADULT Methylprednisolone 125 mg slow IV push" (I, P) | MODERATE | A bullet on row 6. |
| M1-AL-07 | 7 | Provider Level | "EMT Administer: ADULT: Epinephrine autoinjector or 0.3 mg [1 mg/mL] IM" | "Administer IM using either dose-specific clearly marked or color-coded syringe." (EMR, EMT blank; A, I, P) | **CRITICAL** | Set EMT bullet on row 7. EMT IM epinephrine is time-critical and PEMS pearl 1 already allows it. |
| M1-AL-08 | 8 | Provider Level | "EMT A Obtain IV/IO access." | "Vascular Access: Obtain IV/IO access." (I, P) | MODERATE | A bullet on row 8. |
| M1-AL-09 | 9 | Provider Level | "A A If the patient is hypotensive, administer: ADULT: 0.9% Sodium chloride up to 1 L" | "Fluid Resuscitation (Hypotension): ... (I, P)" | MODERATE | A bullet on row 9. |
| M1-AL-10 | 10 | Provider Level | "A A Administer: ADULT: Diphenhydramine (Benadryl) 50 mg IV/IO slow push or IM" | "Antihistamine Administration: ADULT Diphenhydramine 50 mg..." (I, P) | MODERATE | A bullet on row 10. |
| M1-AL-11 | 11 | Provider Level | "A A If wheezing is present, administer: ADULT: Albuterol sulfate ... May repeat as needed." | "Bronchodilator (Wheezing)..." (I, P) | MODERATE | A bullet on row 11. |
| M1-AL-12 | 12 | Provider Level | "A A If wheezing is present, administer: ADULT: Ipratropium bromide ... once." | "Anticholinergic (Wheezing)..." (I, P) | MODERATE | A bullet on row 12. |
| M1-AL-13 | 13 | Provider Level | "A A Administer: ADULT: Methylprednisolone succinate (Solu-Medrol) 125 mg IV/IO slow push" | "Corticosteroid Administration: ADULT ..." (I, P) | MODERATE | A bullet on row 13. |
| M1-AL-14 | absent | Missing row (adult epi infusion) | "I Maintain mean arterial pressure (MAP) above 65 mmHg. ... ADULT: Epinephrine infusion 2 – 10 mcg/min IV/IO" | (absent) | **CRITICAL** | Add I-level adult epinephrine infusion row (MAP > 65 after non-response to repeat IM epi). |
| M1-AL-15 | absent | Missing row (peds epi infusion, [I]) | "[ I ] Maintain age adjusted SBP. ... PEDIATRIC: Epinephrine 0.1 - 1 mcg/kg/min IV/IO infusion. Max dose: 10 mcg/min." | (absent) | **CRITICAL** | Add [I] pediatric infusion row: MC contact at I; SBP <1 yr >70, >1 yr >90. |
| M1-AL-16 | absent | Missing row (adult push-dose epi) | "[ I ] P To maintain MAP > 65 until a vasopressor infusion is prepared, consider: ADULT: Push dose Epinephrine 5-10 mcg IV/IO every 2-3 minutes" | (absent) | **CRITICAL** (level inferred: P) | Add P-level push-dose row (5-10 mcg IV/IO q2-3 min; 100 mcg in 9 mL NS). PDF check bracket placement. |
| M1-AL-17 | absent | Missing row (MC) | "P MC Contact Medical Control for guidance as needed. MC" | (absent) | **CRITICAL** | Add MC row with MC in all five cells. |
| M1-AL-18 | pearl | Pearl (sequencing) | "administer IM epinephrine before any other medications." | "Epinephrine is the definitive treatment ... administered immediately." | MODERATE | Add PEMS sequencing pearl verbatim. |
| M1-AL-19 | pearl | Pearl (trigger removal) | "Remove, decontaminate, or separate the patient from the allergic trigger whenever possible." | (absent) | MODERATE | Add pearl. |
| M1-AL-20 | pearl | Pearl (post-epi monitoring / ECG) | "Obtain an ECG immediately for any patient who develops chest discomfort ... following ... IM Epinephrine or during an Epinephrine infusion." | (absent) | MODERATE | Add pearl. |
| M1-AL-21 | pearl | Pearl (infusion route / extravasation) | "through the largest, most proximal IV access site ... Monitor closely for signs of extravasation" | (absent) | MODERATE | Add pearl; finish the tail from PDF (see coverage gap). |

Counts: 21 (CRITICAL 5, MODERATE 16, MINOR 0).

---

## docs/protocols/cardiac/04_Bradycardia_PROC.md

Coverage: PEMS p.103-105, PEMS rows 1-14 (site rows 1-8 compared; PEMS rows 2-7 absent from site) + pearls + p.105 pearls. verified=true.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| M1-BR-01 | 1 | Provider Level | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care / Initial Patient Contact protocol" (EMR blank, EMT+) | MODERATE | Set EMR bullet on row 1. |
| M1-BR-02 | absent | Missing row (oxygenation) | "EMR Ensure adequate oxygenation. Refer to Airway Management and Ventilatory Support procedure." | (absent) | MODERATE | Add EMR row. |
| M1-BR-03 | absent | Missing row (peds compressions) | "EMR Children/Infants ONLY: If unconscious and hypotensive, with HR less than 60, begin chest compressions." | (absent) | **CRITICAL** | Add EMR row with pediatric CPR and asystole/PEA cross-references. Re-rated from draft MODERATE. |
| M1-BR-04 | absent | Missing row (reversible causes) | "EMR Identify and treat potentially reversible causes. See Pearls below." | (absent) | MODERATE | Add EMR row. |
| M1-BR-05 | absent | Missing row (12-lead ECG) | "EMR EMT Obtain and transmit a 12-Lead ECG." | (absent) | MODERATE | Add EMT row. |
| M1-BR-06 | absent | Missing row (IV/IO) | "EMT A Obtain IV/IO access." | (absent) | MODERATE | Add A row. |
| M1-BR-07 | absent | Missing row (peds epi 0.01 mg/kg) | "A A Children/Infants ONLY: ... PEDIATRIC: Epinephrine 0.01 mg/kg IV/IO [0.1 mg/mL] every 3 – 5 minutes" | (absent) | **CRITICAL** | Add A-level pediatric epinephrine row. |
| M1-BR-08 | 3 | Provider Level (atropine) | "I I Consider: ADULT: Atropine sulfate 1 mg IV/IO ... Maximum dose: 0.5 mg May repeat once after 5 minutes" | "ADULT: 1 mg IV/IO ... May repeat once after 5 minutes" (no level) | **CRITICAL** | Set I bullet (and P) on row 3. Doses match. |
| M1-BR-09 | 4 | Provider Level (pacing) | "I If hypotensive or in shock, initiate transcutaneous pacing." | "If hypotensive or in shock, initiate transcutaneous pacing." (P only) | **CRITICAL** | Set I bullet on row 4. |
| M1-BR-10 | 5 | Provider Level (adult epi infusion) | "I I Maintain mean arterial pressure (MAP) above 65 mmHg ... ADULT: Epinephrine infusion 2 – 10 mcg/min" | same text (no level) | **CRITICAL** | Set I bullet on row 5. |
| M1-BR-11 | 6 | Provider Level / MC bracket (peds epi infusion) | "I [ I ] Maintain age adjusted SBP ... PEDIATRIC: Epinephrine 0.1 - 1 mcg/kg/min IV/IO infusion." | same text (no level) | **CRITICAL** | Add [I] bracket (MC at I). |
| M1-BR-12 | 7 | Provider Level (push-dose) | "[ I ] P To maintain MAP > 65 ... ADULT: Push dose Epinephrine 5-10 mcg IV/IO every 2-3 minutes" | same text (no level) | **CRITICAL** (level inferred: P) | Set P bullet on row 7. PDF check. |
| M1-BR-13 | 8 | MC requirement | "P MC Contact Medical Control for guidance as needed. ... MC" (bare MC) | "[A] at A; bullet at I, P; EMR/EMT blank" | MODERATE | Set MC in all five cells on row 8. Draft F-BR-14 confirmed. |
| M1-BR-14 | pearl | Pearl (pacing not delayed) | "Do not delay pacing to obtain IV/IO access if the patient is hemodynamically unstable." | (absent) | MODERATE | Add pearl. |
| M1-BR-15 | pearl | Pearl (pad placement) | "Refer to manufacturer recommendations for device specific optimal pad placement." | (absent) | MINOR | Add pearl. |
| M1-BR-16 | pearl | Pearl (vasopressor IV site) | "Administer vasopressors through the largest, most proximal IV site available ... monitor closely for extravasation." | (absent) | MODERATE | Add pearl. |
| M1-BR-17 | pearl | Pearl block p.105 (compressions / EtCO2 / airway) | "Push hard and fast: rate 100 – 120 bpm ... EtCO2 ... target above 10 mmHg during CPR and 35-45 mmHg" | (absent) | MODERATE | Add p.105 pearls or cross-reference the CPR procedure. |
| M1-BR-18 | pearl | Pearl (reversible causes list p.105) | "Hypoxia; Hyperkalemia or Hypokalemia; ... Tablets (Overdose)" | (absent) | MODERATE | Add list under reversible-causes row. |
| M1-BR-19 | pearl | Pearl unsourced | (no PEMS text) | "Atropine may be ineffective in high-degree AV blocks..." | MINOR | Source or remove. |
| M1-BR-20 | pearl | Contact numbers | "Children's Hospital of the King's Daughters, COR: (757) 668 – 8000 ... (804) 828 – 3989" | (absent) | MINOR | Add both numbers under row 8. |

Doses on site row 3 (atropine 1 mg; 0.02 mg/kg; min 0.1; max 0.5; repeat once after 5 min) match PEMS: no finding. Row 2 monitor (I, P) matches PEMS I row: no finding.

Counts: 20 (CRITICAL 7, MODERATE 10, MINOR 3).

---

## docs/protocols/cardiac/04_Chest_Pain_ACS_PROC.md

Coverage: PEMS p.107-108, 10 PEMS rows + 9 pearls. Site 14 rows + 9 pearls compared. Site row mapping: 5 = STEMI interpretation pearl; 6 = PEMS row 5 (STEMI transport/alert); 7 = MC serial-ECG text; 8 and 14 site-only. verified=true.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| M1-CP-01 | 1 | Provider Level | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care / Initial Patient Contact protocol." (EMR blank) | MODERATE | Set EMR bullet on row 1. |
| M1-CP-02 | 2 | Provider Level | "EMR EMR Maintain SpO2 94 – 98%. Refer to Airway Management..." | "Airway / Respiratory Management: ... Assess SpO2." (EMR blank) | MODERATE | Set EMR bullet on row 2. |
| M1-CP-03 | 2 | Target | "Maintain SpO2 94 – 98%." | "Assess SpO2." | MODERATE | Add the 94-98% target. |
| M1-CP-04 | absent | Missing referral row | "EMR EMR If hypotensive, refer to Hypotension and Shock protocol." | (absent) | MODERATE | Add EMR referral row. Re-rated from draft MINOR. |
| M1-CP-05 | 4 | Provider Level (12-lead ECG) | "EMR EMT Obtain and transmit 12 – Lead ECG within 5 minutes of patient contact." | "12-Lead ECG Acquisition (EMT): Acquire 12-Lead ECG within 5 minutes" (EMR, EMT blank; A, I, P) | **CRITICAL** | Set EMT bullet on row 4. |
| M1-CP-06 | 4 | Threshold | "Obtain and transmit 12 – Lead ECG within 5 minutes of patient contact." | "Transmit to receiving facility within 10 minutes of patient contact." | MODERATE | Change transmit window to 5 min. |
| M1-CP-07 | 4 | Unsourced | (no EtCO2/SpCO in PEMS) | "Consider assessing EtCO2 and/or SpCO as indicated." | MINOR | Source or remove. |
| M1-CP-08 | 5 | Provider Level (STEMI interpretation, pearl) | "Intermediate and Paramedic providers may interpret a 12-Lead ECG as STEMI if diagnostic criteria is met" | "Intermediate and Paramedic providers may interpret as STEMI if..." (P only) | MODERATE | Set I bullet on row 5. |
| M1-CP-09 | 6 | Provider Level (STEMI alert / transport) | "EMT EMT If 12-Lead ECG reads “STEMI” or “ACUTE MI”, initiate transport ... Notify the receiving facility of a “Pre-Hospital STEMI Alert.”" | "STEMI Alert / Notification: Contact receiving facility via COR ..." (P only) | **CRITICAL** | Set EMT bullet on row 6. |
| M1-CP-10 | 6 | Mandatory action softened | "initiate transport to the nearest PCI capable hospital." | "Consider destination per Administrative Policy - STEMI Field Triage if indicated." | **CRITICAL** | Restore mandatory PCI-capable transport wording. Not in draft; added. |
| M1-CP-11 | 7 | MC requirement (serial ECG; level inferred) | "If 12-Lead ECG is indeterminate ... obtain serial ECGs at 10-minute intervals and contact Medical Control for guidance. MC" | "Extended ECG Assessment: ... Contact Poquoson OMD for guidance." ([I] at I; P bullet) | MODERATE (inferred) | Set MC in all levels (or source a level). PDF check. |
| M1-CP-12 | 8 | Unsourced row | (no IV/IO row in PEMS chest pain p.107-108) | "Establish IV / IO access when indicated" (I, P) | MINOR | Verify against IO/IV procedure, or remove. |
| M1-CP-13 | 9 | Provider Level (monitoring) | "I Monitor cardiac rhythm. Refer to Tachyarrhythmias or Bradycardia protocol, as needed." | "Consider continuous cardiac monitoring." (P only) | MODERATE | Set I bullet on row 9. |
| M1-CP-14 | 10 | Provider Level (aspirin) | "EMT EMT Administer: ADULT: Aspirin 324 mg PO chewed" | "Aspirin Administration (for ACS/STEMI)" (I, P) | **CRITICAL** | Set EMT bullet on row 10. |
| M1-CP-15 | 10 | Dose / route | "ADULT: Aspirin 324 mg PO chewed" | (no dose or route) | **CRITICAL** | Add 324 mg PO chewed. |
| M1-CP-16 | 11 | Provider Level (NTG) | "EMT EMT If systolic blood pressure remains above 100 mmHg and MAP ≥ 65, consider: ADULT: Nitroglycerine 0.4 mg SL." | "Administer per Pain Control Poquoson Protocol" (P only) | **CRITICAL** | Set EMT bullet on row 11. |
| M1-CP-17 | 11 | Dose / repeat / max / gate | "ADULT: Nitroglycerine 0.4 mg SL. May repeat every 5 minutes ... up to three doses." | (no dose, interval, maximum, or SBP/MAP gate) | **CRITICAL** | Add dose, repeat, maximum, and gate. Pain Control cross-reference not verified here. |
| M1-CP-18 | 12 | Provider Level (analgesia) | "I I Consider analgesia." | "Consider analgesia (refer to Pain Control ...)" (P only) | MODERATE | Set I bullet on row 12. |
| M1-CP-19 | 13 | MC requirement | "I MC Contact Medical Control for guidance as needed. ... MC" (bare MC) | "[A] at A; bullet at I, P; EMR/EMT blank" | MODERATE | Set MC in all five cells on row 13. |
| M1-CP-20 | 14 | Bracket on pearl | Pearl: "Consider right-sided 12-Lead or 15-Lead ECG." (no level) | "[I] at I; bullet at P" | MINOR | Remove [I] bracket or source a level. |
| M1-CP-21 | pearl | Scene time | "Minimize scene time. Goal ≤ 15 minutes." | (absent) | MODERATE | Add pearl. |
| M1-CP-22 | pearl | HEMS | "If transport to a PCI capable hospital will not be possible within 30 minutes, consider HEMS." | (absent) | MODERATE | Add pearl. |
| M1-CP-23 | pearl | Serial ECG <1 h | "obtain serial ECGs to assess symptoms with recent onset (< 1 hour)." | (absent) | MODERATE | Add pearl. |
| M1-CP-24 | pearl | Contraindication | "Do not administer Nitroglycerine (Nitrostat) to patients who have taken any long-acting nitrate-based medications within the past 48 hours. ... Sildenafil ... Vardenafil ... Tadalafil" | (absent) | **CRITICAL** | Add contraindication. |
| M1-CP-25 | pearl | ECG before NTG | "Record 12-Lead ECG prior to nitroglycerine administration." | (absent) | MODERATE | Add pearl. |
| M1-CP-26 | pearl | Unstable → nearest ED | "Any unstable patient not expected to survive transport to a PCI capable hospital should be transported immediately to the nearest Emergency Department." | (absent) | **CRITICAL** | Add pearl. Re-rated from draft MODERATE. |
| M1-CP-27 | pearls / row 10 | Unsourced content | (not on PEMS chest pain p.107-108) | site pearls 2, 3, 6, 7, 8, 9; row 10 contraindications/precautions | MINOR | Verify source or remove. |

Counts: 27 (CRITICAL 9, MODERATE 14, MINOR 4).

---

## docs/protocols/cardiac/04_Hypertensive_Crisis_PROC.md

Coverage: PEMS p.109 (titled "Hypertension"), 6 PEMS rows + 2 pearls + criteria. Site 7 rows compared: row 2 site-only; rows 3-6 = PEMS rows 2-5; row 7 = PEMS MC row (MATCH). verified=true.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| M1-HT-01 | 1 | Provider Level | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care / Initial Patient Contact / Poquoson Protocol." (EMR blank) | MODERATE | Set EMR bullet on row 1. |
| M1-HT-02 | 3 | Provider Level (stroke referral) | "EMR EMR If stroke is suspected, refer to Stroke / TIA protocol." | "refer to Stroke / TIA Poquoson Protocol immediately" (EMR blank, EMT+) | MODERATE | Set EMR bullet on row 3. |
| M1-HT-03 | 4 | Provider Level (chest pain referral) | "EMR EMR If the patient is experiencing chest pain / discomfort ... refer to Chest Pain (Cardiac) protocol." | "refer to Chest Pain (Cardiac) Poquoson Protocol immediately" (A, I, P) | MODERATE | Set EMR bullet on row 4. |
| M1-HT-04 | 5 | Provider Level (respiratory referral) | "EMR EMR If the patient is experiencing respiratory distress, refer to ..." | "refer to Respiratory Distress ... Airway Management ..." (EMR blank, EMT+) | MODERATE | Set EMR bullet on row 5. |
| M1-HT-05 | 6 | Provider Level (glucose) | "EMR EMR Check blood glucose level. Refer to Hyperglycemia / Hypoglycemia protocol." | "Check blood glucose level." (A, I, P) | MODERATE | Set EMR bullet on row 6. |
| M1-HT-06 | 2 | Unsourced row (scope) | (no PEMS primary-assessment row) | "Perform Primary and Secondary Survey. Obtain complete set of vital signs" (EMT+) | MINOR | Source or remove leveled row. |
| M1-HT-07 | 4 | Unsourced scope (12-lead ECG at A+) | (no ECG in PEMS p.109; EMT in chest pain p.107) | "Obtain 12-lead ECG if available." (A, I, P) | MINOR | Remove or align with M1-CP-05. |
| M1-HT-08 | 5 | Unsourced scope (oxygen) | (no pulse-ox/O2 instruction in PEMS p.109) | "Apply pulse oximetry and administer oxygen as indicated." | MINOR | Source or remove. |
| M1-HT-09 | 3 | Unsourced instruction | (no scale named in PEMS p.109) | "Cincinnati Prehospital Stroke Scale or equivalent" | MINOR | Source or remove. |
| M1-HT-10 | pearl | Missing pearl | "Generally, prehospital treatment of hypertension is unnecessary. Monitor for deterioration in patient condition." | (statement absent; pearl 1 gives OMD-target language) | MODERATE | Add PEMS statement. |
| M1-HT-11 | pearl | Missing pearl | "Patients with extremely high blood pressure may experience epistaxis ... manage with direct pressure with the patient leaning forward." | (absent) | MODERATE | Add pearl. Re-rated from draft MINOR. |
| M1-HT-12 | pearls / row 7 | Unsourced content | (not in PEMS p.109) | site pearls 2-5 (aortic dissection, permissive HTN); row 7 "Do NOT attempt to aggressively lower blood pressure" | MINOR | Verify with medical director or remove. |
| M1-HT-13 | title | Header naming | "Hypertension" | "Hypertensive Crisis" | MINOR | Align title or add alias. |

Row 7 MC: site MC in all five cells matches PEMS bare MC: no finding.

Counts: 13 (CRITICAL 0, MODERATE 7, MINOR 6).

---

## docs/protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.md

Coverage: PEMS p.111-112, 5 PEMS rows + criteria + pearls. Site 5 rows + 2 pearls compared. verified=true.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| M1-HG-01 | 1 | Provider Level | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care / Initial Patient Contact protocol / Check blood glucose" (EMR blank) | MODERATE | Set EMR bullet on row 1. |
| M1-HG-02 | 2 | Provider Level (oral glucose) | "EMT If the patient is conscious, and able to swallow, administer: ADULT: Oral glucose, 1 tube, PO" | "Administer Oral glucose 1 tube PO" (A, I, P; EMT blank) | **CRITICAL** | Set EMT bullet on row 2. |
| M1-HG-03 | 3 | Provider Level (IV/IO dextrose) | "EMT A Administer: ADULT: Dextrose 10% 125 mL (12.5 g) IV/IO" | "Administer ADULT: Dextrose 10% 125 mL (12.5 g) IV/IO" (I, P) | **CRITICAL** | Set A bullet on row 3. Dose matches. |
| M1-HG-04 | 4 | Provider Level (IM glucagon) | "A A If unable to obtain IV/IO access, administer*: ADULT: Glucagon 1 mg IM" | "Hypoglycemia (No IV/IO access): ADULT: Glucagon 1 mg IM" (I, P) | **CRITICAL** | Set A bullet on row 4. Dose matches. |
| M1-HG-05 | 5 | Provider Level (saline, hyperglycemia) | "A Hyperglycemia A Consider: ADULT: 0.9% Sodium chloride up to 1 L IV/IO" | "Consider ADULT: 0.9% Sodium chloride up to 1 L IV/IO" (I, P) | MODERATE | Set A bullet on row 5. |
| M1-HG-06 | 1 | Pearl (AMS trigger) | "Blood glucose must be assessed for any patient with altered mental status." | "Check blood glucose" (unconditional, EMT+) | MINOR | Optional: add AMS trigger wording. Site is broader. |
| M1-HG-07 | pearl | Missing pearl | "Response to Glucagon requires adequate stores of glycogen ... obtain IO access and administer Dextrose as above." | (absent) | MODERATE | Add pearl. |
| M1-HG-08 | pearl | Missing pearl | "Asymptomatic hyperglycemia does not require prehospital intervention." | (absent) | MODERATE | Add pearl. |
| M1-HG-09 | pearl | Missing pearl | "Use caution when administering IV fluids to patients with congestive heart failure, ESRD or pulmonary edema." | (absent) | MODERATE | Add pearl to row 5. |
| M1-HG-10 | pearl | Missing pearl (recurrence risk; not in draft) | "The risk of recurrent hypoglycemia ... No clear explanation ... Nausea or vomiting ... Sulfonylureas and SGLT2 inhibitors ... left alone ... altered mental status." | (absent) | MODERATE | Add list verbatim. |
| M1-HG-11 | pearl 2 | Unsourced | (no D10-over-D50 in PEMS; monograph says "Use appropriate concentration") | "Dextrose 10% is preferred over D50 to reduce tissue necrosis risk" | MINOR | Source or remove. |

Criteria (BG >300; <60; newborn <72 h and <40) match: no finding.

Counts: 11 (CRITICAL 3, MODERATE 6, MINOR 2).

---

## Count reconciliation

| Protocol | JSON entries | MD table rows | Fixlist lines | CRIT | MOD | MINOR |
|---|---|---|---|---|---|---|
| Allergic | 21 | 21 | 21 | 5 | 16 | 0 |
| Bradycardia | 20 | 20 | 20 | 7 | 10 | 3 |
| Chest Pain | 27 | 27 | 27 | 9 | 14 | 4 |
| Hypertensive Crisis | 13 | 13 | 13 | 0 | 7 | 6 |
| Hypoglycemia | 11 | 11 | 11 | 3 | 6 | 2 |
| **Total** | **92** | **92** | **92** | **24** | **53** | **15** |

`count_reconciled: true`.
