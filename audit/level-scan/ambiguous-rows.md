# Rows needing adjudication (`ambiguous`)
Input to C2. A row is ambiguous when the structure cannot settle it. `reason_kind` says which of the four shapes it is:
- `multiple_candidates` — two or more different PEMS rows explain the site row about equally well (the site row merges them, or a dose/badge differs only in the PEMS row it was pulled from).
- `no_counterpart` — no PEMS row in the mapped source reaches the text floor and no label word binds it: a local addition, or (for pages whose PEMS counterpart is a policy page rather than a grid) a row with no upstream at all.
- `shared_pems_row` — one PEMS row backs the site's TWO rows. Either the site row's label names an intervention whose PEMS row already backs a different site row (CPAP and SGA share p.123 row 3), or the site row has no distinctive label word and its every word is inside a PEMS row another site row already holds ("A: Obtain IV access" is the head of p.135 row 2, whose fluid-bolus tail the next row matched). The containment case carries `contained_in_pems` with the PEMS row, the overlapping words and the ratio.

Rows that carry `section_fallback: true` sit under a site section heading with no single PEMS counterpart, so they were scored against the whole page grid instead. That is an annotation on the row, never a disposition: the row is still `matched`, `ambiguous` or a gap on its own evidence.
**Total: 125 rows** (multiple_candidates 12, no_counterpart 82, shared_pems_row 31) across 27 pages.

Raster crops already exist in `audit/level-scan/evidence/` for the six known hard cases (`vfib_p63`, `vfib_p64`, `crush_p91`, `crush_p92`, `cpap_p245`, `respdist_p125`); where an entry below names one, look at the crop instead of re-rastering.

## `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` — 7 ambiguous
- row **1** (base section) [`multiple_candidates`] — Follow Universal Patient Care / Initial Patient Contact protocol. Determine DNR status. Refer to Death and Criteria for Withholding Resuscitation prot
  - why: 2 different PEMS rows explain this row about equally well: p.57 row 1 (0.88), p.57 row 0 (0.79); the site row may merge them
- row **12** (base section) [`multiple_candidates`] — If ROSC is achieved, refer to Post Cardiac Arrest Care (ROSC) protocol. If ROSC is not achieved, refer to Death and Criteria for Withholding Resuscita
  - why: 2 different PEMS rows explain this row about equally well: p.57 row 8 (0.61), p.57 row 1 (0.60); the site row may merge them
- row **4** (base section) [`no_counterpart`] — Ensure adequate oxygenation. Refer to Airway Management and Ventilatory Support procedure.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.57 row 1) (best coverage 0.00, p.57 row 1; see `text-binding.md`)
- row **5** (base section) [`no_counterpart`] — Obtain and transmit a 12-Lead ECG.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.57 row 1) (best coverage 0.00, p.57 row 1; see `text-binding.md`)
- row **7** (base section) [`no_counterpart`] — Monitor ETCO2. If ETCO2 < 10 or dropping, reassess and optimize compression rate, depth, and recoil.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.57 row 4) (best coverage 0.00, p.57 row 4; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — Apply AED / Assess cardiac rhythm every 2 minutes. If AED is advising to shock or rhythm is VF or VT (as determined by EMT-I or P), defibrillate at ma
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.57 row 1) (best coverage 0.00, p.57 row 1; see `text-binding.md`)
- row **11** (base section) [`shared_pems_row`] — For cardiac arrest in renal dialysis patients, patients with crush injuries, suspected calcium channel blocker overdose, or suspected hyperkalemia onl
  - why: site row label names an intervention that p.57 row 7 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
  - evidence: `crush_p91-091.png`, `crush_p92-092.png`

## `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md` — 4 ambiguous
- row **14** (base section) [`multiple_candidates`] — Post-Resuscitation: • If ROSC achieved, refer to Post Cardiac Arrest Care (ROSC) protocol. • If ROSC not achieved, refer to Death and Criteria for Wit
  - why: 3 different PEMS rows explain this row about equally well: p.64 row 13 (0.65), p.57 row 1 (0.64), p.63 row 1 (0.64); the site row may merge them
- row **9** (base section) [`multiple_candidates`] — Amiodarone - V-Fib/V-Tach Only (if persists after defibrillation and Epinephrine): • ADULT: 300 mg IV/IO slow push • PEDIATRIC: 5 mg/kg IV/IO slow pus
  - why: 3 different PEMS rows explain this row about equally well: p.64 row 11 (0.67), p.64 row 10 (0.64), p.64 row 9 (0.61); the site row may merge them
- row **3** (base section) [`no_counterpart`] — Airway Management: • Apply BVM with high-flow O₂. • Use quantitative EtCO₂ monitoring with BVM: - If EtCO₂ < 10 mmHg, improve compressions - If sudden
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.06 against p.64 row 13) (best coverage 0.06, p.64 row 13; see `text-binding.md`)
- row **4** (base section) [`no_counterpart`] — AED / Rhythm Assessment: • Apply AED and assess cardiac rhythm every 2 minutes. • Identify rhythm: V-Fib/V-Tach (shockable) or Asystole/PEA (non-shock
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.63 row 7 (coverage 1.00, badge I), which site row 5 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 1.00, p.63 row 7; see `text-binding.md`)

## `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md` — 5 ambiguous
- row **3** (base section) [`multiple_candidates`] — Apply AED / Monitor (Assess rhythm before CPR if possible)
  - why: 3 different PEMS rows explain this row about equally well: p.61 row 8 (0.40), p.61 row 4 (0.38), p.61 row 5 (0.38); the site row may merge them
- row **10** (base section) [`no_counterpart`] — Rapid transport to Level I/II Trauma Center (Goal < 10 mins)
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `no_anchor` — coverage 0.50 (whole row 0.38) clears the 0.40 floor, but the row shares no drug name, no dose and no whole label head with that PEMS row, so the binding would rest on an ordinary word: Begin chest compressions. Refer to Cardiopulmonary Resuscitation (CPR) procedure. Consider immediate transport to the closest Emergency Department or Trauma Cen (best coverage 0.50, p.61 row 2; see `text-binding.md`)
- row **6** (base section) [`no_counterpart`] — Obtain IV/IO access (x2 preferred)
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.61 row 5 (coverage 1.00, badge A), which site row 7 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 1.00, p.61 row 5; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — Assess Shock Index > 1 / Resuscitate prior to intubation
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.20 against p.61 row 6) (best coverage 0.20, p.61 row 6; see `text-binding.md`)
- row **4** (base section) [`shared_pems_row`] — Asystole on arrival: Consider withholding CPR
  - why: site row label names an intervention that p.61 row 4 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` — 6 ambiguous
- row **14** (base section) [`no_counterpart`] — Right-Sided / 15-Lead ECG: • Consider right-sided 12-Lead or 15-Lead ECG for additional assessment.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.107 row 2) (best coverage 0.00, p.107 row 2; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Glucose Assessment: • Check blood glucose level. • Refer to the Hyperglycemia / Hypoglycemia protocol if indicated.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.107 row 2) (best coverage 0.00, p.107 row 2; see `text-binding.md`)
- row **5** (base section) [`no_counterpart`] — 12-Lead ECG Interpretation - STEMI Criteria: • Intermediate and Paramedic providers may interpret as STEMI if: - Symptoms consistent with ACS/myocardi
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.107 row 4 (coverage 0.60, badge EMT), which site row 6 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.60, p.107 row 4; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — IV/IO Access: • Establish IV / IO access when indicated (refer to Intraosseous Access procedure).
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.107 row 2) (best coverage 0.00, p.107 row 2; see `text-binding.md`)
- row **9** (base section) [`no_counterpart`] — Cardiac Monitoring: • Consider continuous cardiac monitoring.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `no_anchor` — coverage 1.00 (whole row 0.50) clears the 0.40 floor, but the row shares no drug name, no dose and no whole label head with that PEMS row, so the binding would rest on an ordinary word: Monitor cardiac rhythm. Refer to Tachyarrhythmias or Bradycardia protocol, as needed. (best coverage 1.00, p.107 row 7; see `text-binding.md`)
- row **13** (base section) [`shared_pems_row`] — Medical Control Contact: • Contact Medical Control for guidance as needed.
  - why: every word of this row (contact, control, guidance, medical) occurs in p.107 row 9 — 4 of that row's 17 significant words — which site row 7 already holds; the site splits one PEMS row into two

## `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` — 1 ambiguous
- row **2** (base section) [`no_counterpart`] — Primary Assessment: • Perform Primary and Secondary Survey. • Obtain complete set of vital signs including bilateral BP if possible. • Assess for sign
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.06 against p.109 row 2) (best coverage 0.06, p.109 row 2; see `text-binding.md`)

## `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md` — 6 ambiguous
- row **2** (base section) [`no_counterpart`] — Assess patient stability (chest pain, dyspnea, AMS, shock)
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.135 row 1) (best coverage 0.00, p.135 row 1; see `text-binding.md`)
- row **13** (base section) [`shared_pems_row`] — Monitor SpO₂ and EtCO₂ during sedation
  - why: site row label names an intervention that p.135 row 5 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
- row **15** (base section) [`shared_pems_row`] — If unsuccessful, check pad placement and repeat at 200 joules (Adult) or 2 joules/kg (Pediatric)
  - why: two site rows name this same PEMS intervention; p.136 row 6 merges what the site splits — adjudicate which site row's cells that PEMS badge governs
- row **16** (base section) [`shared_pems_row`] — If unsuccessful after two attempts, contact Medical Control
  - why: site row label names an intervention that p.136 row 6 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
- row **5** (base section) [`shared_pems_row`] — Obtain IV access
  - why: every word of this row (access) occurs in p.135 row 2 — 1 of that row's 15 significant words — which site row 6 already holds; the site splits one PEMS row into two
- row **8** (base section) [`shared_pems_row`] — If no conversion after 2 minutes, repeat Adenosine at DOUBLE initial dose
  - why: site row label names an intervention that p.135 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` — 1 ambiguous
- row **2** (base section) [`no_counterpart`] — Apply de-escalation techniques. Remain calm, maintain soothing tone, allow space, do not reinforce delusions, set boundaries.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.71 row 0) (best coverage 0.00, p.71 row 0; see `text-binding.md`)

## `protocols/general/02_Cold_Exposure_PROC.md` — 3 ambiguous
- row **6** (base section) [`no_counterpart`] — If patient is alert and responsive: Use active external rewarming with heat packs, warm blankets, etc.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.38 against p.67 row 1) (best coverage 0.38, p.67 row 1; see `text-binding.md`)
- row **9** (base section) [`no_counterpart`] — Contact Medical Control prior to use of AED.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.20 against p.67 row 4) (best coverage 0.20, p.67 row 4; see `text-binding.md`)
- row **3** (base section) [`shared_pems_row`] — Handle the patient gently and avoid excessive movement (risk of cardiac arrest/VF).
  - why: site row label names an intervention that p.67 row 1 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/general/02_Heat_Exposure_PROC.md` — 3 ambiguous
- row **3** (base section) [`shared_pems_row`] — Normal skin temp: Apply cool compresses
  - why: site row label names an intervention that p.69 row 2 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
- row **4** (base section) [`shared_pems_row`] — Hot skin temp (Heat Stroke): Treat as life-threatening/start rapid cooling (cool mist, ice packs to armpits/groin/neck, wet sheet)
  - why: site row label names an intervention that p.69 row 2 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
- row **5** (base section) [`shared_pems_row`] — Shivering: Slow the cooling process
  - why: site row label names an intervention that p.69 row 2 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/general/02_Pain_Control_PROC.md` — 1 ambiguous
- row **7** (base section) [`shared_pems_row`] — OR Moderate to Severe Pain (6 - 10): • Adult: Morphine Sulfate 2.5-5 mg IV/IM (Max total dose: 10 mg) • Pediatric: Morphine Sulfate 0.1 mg/kg IV/IM (M
  - why: site row label names an intervention that p.77 row 4 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md` — 4 ambiguous
- row **5** (base section) [`multiple_candidates`] — Post-Intubation Sedation, consider ONE of the following: • ADULT: Ketamine (Ketalar) 1 mg/kg IV/IO (Maximum single dose: 100 mg). May repeat every 10-
  - why: 2 different PEMS rows explain this row about equally well: p.55 row 2 (0.48), p.55 row 3 (0.43); the site row may merge them
- row **6** (base section) [`multiple_candidates`] — OR Post-Intubation Sedation (Midazolam / Fentanyl): • ADULT: Midazolam (Versed) 2.5 mg IV/IO. May repeat every 10-15 minutes as needed. (Maximum total
  - why: 2 different PEMS rows explain this row about equally well: p.55 row 2 (0.69), p.55 row 3 (0.61); the site row may merge them
- row **2** (base section) [`no_counterpart`] — Assess and monitor blood pressure. Ensure patient is not hypotensive.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.55 row 1) (best coverage 0.00, p.55 row 1; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Establish IV/IO access.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.33 against p.55 row 2) (best coverage 0.33, p.55 row 2; see `text-binding.md`)

## `protocols/medical/07_OB_Emergencies_PROC.md` — 2 ambiguous
- row **1** (base section) [`multiple_candidates`] — Follow Universal Patient Care, don appropriate PPE, and visualize perineum for crowning or presenting part.
  - why: 2 different PEMS rows explain this row about equally well: p.147 row 0 (0.67), p.141 row 1 (0.65); the site row may merge them
- row **4** (base section) [`shared_pems_row`] — Umbilical Cord Prolapse: Wrap exposed cord in saline-moistened gauze. Elevate mother's hips or place in Trendelenburg position. Insert gloved hand to 
  - why: site row label names an intervention that p.141 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/neurologic/05_Seizure_PROC.md` — 1 ambiguous
- row **6** (base section) [`shared_pems_row`] — Use HALF dose Midazolam for frail/hypotensive/elderly >65y
  - why: site row label names an intervention that p.127 row 5 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/neurologic/05_Stroke_TIA_PROC.md` — 4 ambiguous
- row **6** (base section) [`no_counterpart`] — Triage: Symptoms <24 hrs & RACE 5-9 -> Transport to closest Comprehensive Stroke Center (if <30 min delay)
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.131 row 4 (coverage 0.64, badge EMT), which site row 5 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.64, p.131 row 4; see `text-binding.md`)
- row **7** (base section) [`no_counterpart`] — Triage: Symptoms >24 hrs OR RACE 0-4 -> Transport to closest stroke center
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.131 row 4 (coverage 0.75, badge EMT), which site row 5 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.75, p.131 row 4; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — Establish 18g IV in Right AC (preferred for rapid imaging)
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.131 row 5) (best coverage 0.00, p.131 row 5; see `text-binding.md`)
- row **9** (base section) [`shared_pems_row`] — Call COR at the receiving facility with Name/DOB for rapid registration
  - why: site row label names an intervention that p.131 row 2 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md` — 6 ambiguous
- row **10** (base section) [`no_counterpart`] — Endotracheal Intubation: • Follow Endotracheal Intubation procedure. • ⚠ Intubation of spontaneously breathing patients without rapid sequence inducti
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.09 against p.153 row 2) (best coverage 0.09, p.153 row 2; see `text-binding.md`)
- row **11** (base section) [`no_counterpart`] — Poison Control Consultation: • Contact Poison Control Center at 1-800-222-1222 with any questions. (Note: Poison Control is not online medical control
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.33 against p.153 row 5) (best coverage 0.33, p.153 row 5; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Airway Assessment: • Assess for signs of airway injury (singed hairs, facial burns, hoarseness, stridor, soot). • Monitor for progressive respiratory 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.153 row 2 (coverage 0.50, badge EMT), which site row 5 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.50, p.153 row 2; see `text-binding.md`)
- row **4** (base section) [`no_counterpart`] — Oxygen Administration: • Apply high-flow oxygen via NRB or BVM as indicated. • Target SpO₂ > 94%.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.153 row 1) (best coverage 0.00, p.153 row 1; see `text-binding.md`)
- row **9** (base section) [`no_counterpart`] — Advanced Airway Assessment: • Consider endotracheal intubation if signs of airway injury develop. • Assess for impending airway compromise (worsening 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.33 against p.153 row 2) (best coverage 0.33, p.153 row 2; see `text-binding.md`)
- row **7** (base section) [`shared_pems_row`] — Methylprednisolone (Solu-Medrol): • Adult: 125 mg IV/IO slow push • Pediatric: 2 mg/kg IV/IO slow push (Maximum dose: 125 mg)
  - why: site row label names an intervention that p.153 row 4 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` — 4 ambiguous
- row **4** (base section) [`multiple_candidates`] — Ipratropium Bromide (Anticholinergic): • Adult & Pediatric: 3 mL of 0.02% solution via nebulizer. • ⚠ ONCE ONLY – Do NOT repeat without Medical Contro
  - why: 2 different PEMS rows explain this row about equally well: p.123 row 5 (0.50), p.124 row 13 (0.46); the site row may merge them
- row **11** (base section) [`no_counterpart`] — Reassessment and Transport: • Continuously monitor respiratory status, auscultation, and SpO₂. • Reassess after each bronchodilator treatment. • Exped
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.124 row 11) (best coverage 0.00, p.124 row 11; see `text-binding.md`)
- row **7** (base section) [`no_counterpart`] — Assist Ventilations / Airway Management: • Prepare for assisted ventilation if respiratory failure develops. • Bag-valve-mask with PEEP valve as indic
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `no_anchor` — coverage 0.50 (whole row 0.11) clears the 0.40 floor, but the row shares no drug name, no dose and no whole label head with that PEMS row, so the binding would rest on an ordinary word: Perform a focused evaluation including pertinent history and assessment of airway and lung sounds. Refer to Airway Management and Ventilatory Support procedure  (best coverage 0.50, p.123 row 1; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — Continuous Positive Airway Pressure (CPAP): • Consider for COPD exacerbation or severe bronchospasm with adequate mentation. • Initiate 5-10 cm H₂O, t
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - evidence: `cpap_p245-245.png`
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.25 against p.123 row 1) (best coverage 0.25, p.123 row 1; see `text-binding.md`)

## `protocols/respiratory/03_Pediatric_Stridor_PROC.md` — 6 ambiguous
- row **11** (base section) [`no_counterpart`] — Airway Protection - Advanced Airway • Prepare for advanced airway if impending respiratory failure • Have appropriate sized equipment ready • ⚠ Intuba
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.33 against p.123 row 1) (best coverage 0.33, p.123 row 1; see `text-binding.md`)
- row **12** (base section) [`no_counterpart`] — Transport Considerations • Transport to pediatric-capable facility • Alert receiving facility early • Consider ALS intercept if BLS only • Rapid trans
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.08 against p.124 row 9) (best coverage 0.08, p.124 row 9; see `text-binding.md`)
- row **2** (base section) [`no_counterpart`] — Scene Management & Calm Environment • Keep child calm - agitation worsens obstruction • Allow parent/caregiver to hold child • Avoid unnecessary proce
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.25 against p.123 row 1) (best coverage 0.25, p.123 row 1; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Position of Comfort • Allow child to assume position of choice (usually upright or with parent) • Do not force supine positioning • Head-down position
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.12 against p.123 row 1) (best coverage 0.12, p.123 row 1; see `text-binding.md`)
- row **5** (base section) [`no_counterpart`] — Continuous Monitoring • Cardiac monitor • Pulse oximetry • EtCO2 when available
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.124 row 11) (best coverage 0.00, p.124 row 11; see `text-binding.md`)
- row **9** (base section) [`no_counterpart`] — IV/IO Access • Obtain IV or IO access for medication administration • Use largest appropriate catheter • Do NOT delay Epinephrine for IV/IO placement
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `no_anchor` — coverage 0.50 (whole row 0.11) clears the 0.40 floor, but the row shares no drug name, no dose and no whole label head with that PEMS row, so the binding would rest on an ordinary word: For moderate to severe symptoms, also administer: ADULT: Methylprednisolone (Solu-Medrol) 125 mg IV/IO slow push. PEDIATRIC: Methylprednisolone (Solu-Medrol) 2  (best coverage 0.50, p.124 row 9; see `text-binding.md`)

## `protocols/respiratory/03_Pneumothorax_PROC.md` — 11 ambiguous
- row **1** (base section) [`no_counterpart`] — Universal Patient Care / Scene Safety: • Ensure scene safety and appropriate PPE. • Bring all necessary equipment to patient side.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **11** (base section) [`no_counterpart`] — Repeat Decompression if Needed: • Consider repeating procedure for continued or recurrent hemodynamic instability or absent breath sounds.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.243 row 4 (coverage 0.57, badge I), which site row 10 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.57, p.243 row 4; see `text-binding.md`)
- row **13** (base section) [`no_counterpart`] — Advanced Airway Management (if indicated): • Prepare for or perform endotracheal intubation if respiratory failure. • ⚠ Positive pressure ventilation 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - evidence: `cpap_p245-245.png`
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **14** (base section) [`no_counterpart`] — Transport Considerations: • Transport to appropriate trauma center if traumatic etiology. • Alert receiving facility of needle decompression performed
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **15** (base section) [`no_counterpart`] — Close Monitoring En Route: • Continuous reassessment en route. • Monitor for recurrent tension pneumothorax. • Secure catheter to prevent dislodgement
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **2** (base section) [`no_counterpart`] — Primary Assessment: • Assess airway, breathing, circulation, and disability. • Assess vital signs and SpO2. • Identify life threats immediately.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Oxygen Administration: • Administer Oxygen via nasal cannula or mask as needed to maintain SpO2 > 94%. • Titrate to patient condition.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `no_anchor` — coverage 0.50 (whole row 0.10) clears the 0.40 floor, but the row shares no drug name, no dose and no whole label head with that PEMS row, so the binding would rest on an ordinary word: Administer oxygen at 15 LPM (100% FiO2). (best coverage 0.50, p.243 row 0; see `text-binding.md`)
- row **4** (base section) [`no_counterpart`] — Positioning and Monitoring: • Position patient for comfort (typically supine or semi-Fowler's). • Establish IV/IO access. • Continuous cardiac and pul
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **5** (base section) [`no_counterpart`] — Suction and Airway Management: • Prepare suction and airway equipment. • Be prepared for rapid airway intervention if decompensation occurs.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **9** (base section) [`no_counterpart`] — Bilateral Chest Decompression (Traumatic Cardiac Arrest): • For traumatic cardiac arrest with suspicion of thoracoabdominal trauma, perform bilateral 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.243 row 0) (best coverage 0.00, p.243 row 0; see `text-binding.md`)
- row **12** (base section) [`shared_pems_row`] — Hemodynamic Support: • 0.9% Sodium Chloride fluid bolus if hypotensive (SBP < 90 mmHg or MAP < 65). • Consider vasopressor support if cardiogenic shoc
  - why: site row label names an intervention that p.243 row 4 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` — 6 ambiguous
- row **10** (base section) [`shared_pems_row`] — Nitroglycerin Adult: 0.4 mg SL
  - why: site row label names an intervention that p.124 row 11 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
- row **5** (base section) [`shared_pems_row`] — CPAP Initial Settings: PEEP 5 cmH2O
  - why: site row label names an intervention that p.123 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
  - evidence: `cpap_p245-245.png`
- row **6** (base section) [`shared_pems_row`] — CPAP CONTRAINDICATIONS (⚠️): • Apnea/agonal respirations • GCS ≤ 13 • Pneumothorax
  - why: site row label names an intervention that p.123 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
  - evidence: `cpap_p245-245.png`
- row **7** (base section) [`shared_pems_row`] — CPAP CONTRAINDICATIONS (⚠️): • Facial trauma/burns/recent surgery • Penetrating neck/chest trauma • Active vomiting/severe nausea
  - why: site row label names an intervention that p.123 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
  - evidence: `cpap_p245-245.png`
- row **8** (base section) [`shared_pems_row`] — CPAP CONTRAINDICATIONS (⚠️): • Hypotension (SBP < 90 mmHg, MAP < 65) • Inability to tolerate tight fitting mask
  - why: site row label names an intervention that p.123 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
  - evidence: `cpap_p245-245.png`
- row **9** (base section) [`shared_pems_row`] — CPAP Titration: Adjust PEEP up to 10 cmH2O to support ventilation and work of breathing
  - why: site row label names an intervention that p.123 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
  - evidence: `cpap_p245-245.png`

## `protocols/respiratory/03_Respiratory_Arrest_PROC.md` — 8 ambiguous
- row **11** (base section) [`no_counterpart`] — Surgical Airway (Cricothyrotomy): • If unable to intubate and unable to oxygenate, proceed immediately to Surgical Airway. • Use 14G, 3.25" catheter o
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.239 row 2 (coverage 0.50, badge EMR), which site row 5 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.50, p.239 row 2; see `text-binding.md`)
- row **12** (base section) [`no_counterpart`] — Post-Intubation Airway Management: • Verify tube placement with continuous box-waveform capnography AND auscultation (bilateral lung sounds, absence o
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.05 against p.239 row 4) (best coverage 0.05, p.239 row 4; see `text-binding.md`)
- row **13** (base section) [`no_counterpart`] — Ongoing Ventilation Monitoring: • Monitor ET tube placement and ventilation continuously with SpO2 and EtCO2. • Reassess lung sounds and gastric sound
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.09 against p.239 row 4) (best coverage 0.09, p.239 row 4; see `text-binding.md`)
- row **14** (base section) [`no_counterpart`] — Post-Advanced Airway Analgesia – Fentanyl (Sublimaze): • ADULT: 25–50 mcg IV/IO over 2 minutes or IN/IM. • PEDIATRIC: 0.5–1 mcg/kg IV/IO over 2 minute
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.239 row 4) (best coverage 0.00, p.239 row 4; see `text-binding.md`)
- row **15** (base section) [`no_counterpart`] — Post-Advanced Airway Sedation – Midazolam (Versed): • ADULT: 2.5 mg IV/IO over 2 minutes or 5 mg IN/IM. • PEDIATRIC: 0.1 mg/kg IV/IO over 2 minutes or
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.239 row 4) (best coverage 0.00, p.239 row 4; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Continuous Monitoring: • Apply continuous pulse oximetry (SpO2). • Apply continuous box-waveform capnography (EtCO2) once airway placed.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.22 against p.239 row 4) (best coverage 0.22, p.239 row 4; see `text-binding.md`)
- row **6** (base section) [`no_counterpart`] — BVM Ventilation (Two-Person Technique): • Support respirations with bag-valve-mask using two-person technique preferred. • Deliver appropriate tidal v
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.239 row 4) (best coverage 0.00, p.239 row 4; see `text-binding.md`)
- row **2** (base section) [`shared_pems_row`] — Position Patient and Open Airway: • Position the patient appropriately (supine for intubation, recovery position if vomiting). • Open the airway using
  - why: site row label names an intervention that p.239 row 6 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/respiratory/03_Respiratory_Distress_PROC.md` — 10 ambiguous
- row **10** (base section) [`no_counterpart`] — Fluid Administration: • 0.9% Sodium Chloride or appropriate fluid as clinically indicated • Monitor for signs of fluid overload in CHF patients
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.124 row 10 (coverage 0.44, badge A), which site row 12 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.44, p.124 row 10; see `text-binding.md`)
- row **14** (base section) [`no_counterpart`] — Severe Asthma/COPD: • Refer to Asthma specific protocol for comprehensive treatment • Magnesium Sulfate per Asthma protocol ⚠ Positive pressure may wo
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.08 against p.123 row 5, shared words: sulfate) (best coverage 0.08, p.123 row 5; see `text-binding.md`)
- row **15** (base section) [`no_counterpart`] — Cardiac Ischemia Management: • Evaluate for cardiac origin • Consider 12-lead ECG • Refer to Chest Pain/ACS protocol if indicated
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.123 row 5) (best coverage 0.00, p.123 row 5; see `text-binding.md`)
- row **16** (base section) [`no_counterpart`] — Respiratory Failure Management: • If apnea/agonal respirations or GCS ≤13: • Prepare for immediate airway control • Bag-valve-mask ventilation • Consi
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.07 against p.124 row 13) (best coverage 0.07, p.124 row 13; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Continuous Monitoring: • Continuous EtCO2 monitoring to guide therapy • Continuous pulse oximetry • Cardiac monitoring
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.124 row 13) (best coverage 0.00, p.124 row 13; see `text-binding.md`)
- row **5** (base section) [`no_counterpart`] — Positioning: • Patient position of comfort (sitting upright preferred) • Consider reverse Trendelenburg if tolerated
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.124 row 13) (best coverage 0.00, p.124 row 13; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — Advanced Airway Management (ETI): • Endotracheal intubation reserved for I-level providers per protocol
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.123 row 1 (coverage 0.67, badge EMR), which site row 2 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.67, p.123 row 1; see `text-binding.md`)
- row **9** (base section) [`no_counterpart`] — IV/IO Access: • Establish vascular access for medication administration and fluid therapy • IO if IV unobtainable
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `no_anchor` — coverage 0.50 (whole row 0.11) clears the 0.40 floor, but the row shares no drug name, no dose and no whole label head with that PEMS row, so the binding would rest on an ordinary word: Administer: ADULT: Furosemide (Lasix) 40 mg IV/IO slow push (best coverage 0.50, p.124 row 12; see `text-binding.md`)
- row **6** (base section) [`shared_pems_row`] — CPAP (Continuous Positive Airway Pressure): • Indications: Adults with respiratory distress due to pulmonary edema, infection, or near-drowning • Init
  - why: two site rows name this same PEMS intervention; p.123 row 3 merges what the site splits — adjudicate which site row's cells that PEMS badge governs
  - evidence: `cpap_p245-245.png`
- row **7** (base section) [`shared_pems_row`] — Supraglottic Airways (SGA): • Consider if patient continues to deteriorate and cannot tolerate CPAP • Maintains airway patency while avoiding invasive
  - why: two site rows name this same PEMS intervention; p.123 row 3 merges what the site splits — adjudicate which site row's cells that PEMS badge governs
  - evidence: `cpap_p245-245.png`

## `protocols/respiratory/03_Smoke_Inhalation_PROC.md` — 11 ambiguous
- row **5** (base section) [`multiple_candidates`] — Advanced Airway Considerations: • Consider endotracheal intubation versus immediate transport to the nearest emergency department if any signs or symp
  - why: 2 different PEMS rows explain this row about equally well: p.153 row 2 (0.43), p.239 row 10 (0.34); the site row may merge them
- row **10** (base section) [`no_counterpart`] — Burn Assessment: • Assess for concomitant thermal burn injuries • Estimate total body surface area (TBSA) involved • Evaluate burn depth and critical 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.05 against p.239 row 8) (best coverage 0.05, p.239 row 8; see `text-binding.md`)
- row **11** (base section) [`no_counterpart`] — Fluid Management (If Burns Present): • Initiate fluid resuscitation per Burn Injuries Protocol • Titrate fluid administration to hemodynamic response 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.153 row 2 (coverage 0.50, badge EMT), which site row 5 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.50, p.153 row 2; see `text-binding.md`)
- row **13** (base section) [`no_counterpart`] — Monitoring and Reassessment: • Monitor SpO2, EtCO2, and respiratory rate continuously • Reassess airway patency frequently; edema may progress rapidly
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.17 against p.239 row 7) (best coverage 0.17, p.239 row 7; see `text-binding.md`)
- row **14** (base section) [`no_counterpart`] — Transport Considerations: • Expedited transport given risk of rapid airway compromise • Transport to facility capable of managing combined trauma/burn
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.05 against p.153 row 2) (best coverage 0.05, p.153 row 2; see `text-binding.md`)
- row **2** (base section) [`no_counterpart`] — Scene Safety and Scene Time Considerations: • Assess scene for ongoing hazard exposure • Limit scene time; prepare for rapid transport • Coordinate wi
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.08 against p.153 row 4) (best coverage 0.08, p.153 row 4; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Airway Assessment: • Inspect for singed facial/nasal hairs • Examine face, nose, and mouth for burns or soot • Auscultate for stridor, hoarseness, or 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `no_anchor` — coverage 0.50 (whole row 0.04) clears the 0.40 floor, but the row shares no drug name, no dose and no whole label head with that PEMS row, so the binding would rest on an ordinary word: Follow Airway Management and Ventilatory Support procedure. (best coverage 0.50, p.153 row 2; see `text-binding.md`)
- row **4** (base section) [`no_counterpart`] — Initial Airway Management: • Position patient to optimize ventilation • Suction oropharynx as needed for soot/secretions • Apply high-flow oxygen via 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.153 row 2 (coverage 1.00, badge EMT), which site row 5 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 1.00, p.153 row 2; see `text-binding.md`)
- row **7** (base section) [`no_counterpart`] — Hydroxocobalamin (Cyanide Antidote) - Indication Assessment: • Assess for exposure to combustion products/fire in an enclosed space with ANY of the fo
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.08 against p.153 row 4) (best coverage 0.08, p.153 row 4; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — Hydroxocobalamin Preparation: • Reconstitute with 200 mL 0.9% Sodium Chloride • Use vented IV tubing for administration • Verify solution clarity and 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.33 against p.153 row 4, shared words: 0.9 %, chloride, sodium) (best coverage 0.33, p.153 row 4; see `text-binding.md`)
- row **9** (base section) [`no_counterpart`] — Hydroxocobalamin Administration: • Administer per Medical Control guidance • Monitor for increase in blood pressure • Inform receiving facility of adm
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.239 row 4) (best coverage 0.00, p.239 row 4; see `text-binding.md`)

## `protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md` — 7 ambiguous
- row **13** (base section) [`no_counterpart`] — Post-Obstruction Advanced Airway - Sedation: • If endotracheal intubation performed, refer to Sedation Post Advanced Airway protocol. • Fentanyl (25 m
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.06 against p.239 row 1) (best coverage 0.06, p.239 row 1; see `text-binding.md`)
- row **14** (base section) [`no_counterpart`] — Expanding Hematoma / Edema - Advanced Airway: • Early airway intervention before complete obstruction. • Consider difficult airway algorithm; prepare 
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.239 row 1) (best coverage 0.00, p.239 row 1; see `text-binding.md`)
- row **2** (base section) [`no_counterpart`] — Scene Safety / Recognition: • Rapidly identify complete vs partial obstruction. • Recognize universal choking sign (hands to throat). • Determine cons
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.239 row 7) (best coverage 0.00, p.239 row 7; see `text-binding.md`)
- row **3** (base section) [`no_counterpart`] — Conscious Adult (≥12 years) - Abdominal Thrusts: • Stand behind patient, wrap arms around waist. • Make fist with one hand; thumb side against patient
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.239 row 3 (coverage 0.50, badge EMT), which site row 4 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.50, p.239 row 3; see `text-binding.md`)
- row **8** (base section) [`no_counterpart`] — Unconscious Patient - BLS Airway Adjuncts: • Insert OPA or NPA as indicated by patient tolerance and level of consciousness. • Insert SGA (i-gel or Ki
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.239 row 6 (coverage 0.75, badge EMT), which site row 7 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.75, p.239 row 6; see `text-binding.md`)
- row **5** (base section) [`shared_pems_row`] — Conscious Pediatric ≥1 year - Abdominal Thrusts: • Kneel behind child, wrap arms around waist. • Make fist; thumb side against child's abdomen. • Posi
  - why: site row label names an intervention that p.239 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
- row **6** (base section) [`shared_pems_row`] — Conscious Pediatric <1 year - Back Blows and Chest Thrusts: • Position infant prone, head down, below level of chest. • Support head and neck with han
  - why: site row label names an intervention that p.239 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/trauma/09_Burns_Thermal_PROC.md` — 1 ambiguous
- row **6** (base section) [`no_counterpart`] — Hydrofluoric Acid (HF) Burns with Hypotension: Administer Calcium Chloride 1 g IV/IO over 3 mins (Repeat in 5 mins PRN).
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.33 against p.88 row 8, shared words: chloride) (best coverage 0.33, p.88 row 8; see `text-binding.md`)

## `protocols/trauma/09_Crush_Syndrome_PROC.md` — 2 ambiguous
- row **1** (base section) [`multiple_candidates`] — Follow Universal Patient Care / Initial Patient Contact protocol. Refer to Trauma, Hemorrhage Control, and Pain Control protocols as needed.
  - why: 2 different PEMS rows explain this row about equally well: p.91 row 1 (0.90), p.91 row 0 (0.86); the site row may merge them
  - evidence: `crush_p91-091.png`, `crush_p92-092.png`
- row **6** (base section) [`shared_pems_row`] — Administer, preferably via separate lines (when able, initiate prior to release): - ADULT: Calcium Chloride 1 g IV/IO over 3 minutes. - PEDIATRIC: Cal
  - why: site row label names an intervention that p.91 row 5 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs
  - evidence: `crush_p91-091.png`, `crush_p92-092.png`

## `protocols/trauma/09_Hemorrhage_Control_PROC.md` — 3 ambiguous
- row **1** (base section) [`multiple_candidates`] — Follow Universal Care / Reassess bleeding after treatments performed.
  - why: 2 different PEMS rows explain this row about equally well: p.75 row 0 (0.65), p.75 row 7 (0.68); the site row may merge them
- row **8** (base section) [`no_counterpart`] — Consider pain control per the Pain Control protocol.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.75 row 0) (best coverage 0.00, p.75 row 0; see `text-binding.md`)
- row **9** (base section) [`shared_pems_row`] — Contact Medical Control if hemorrhage cannot be controlled and transport immediately.
  - why: site row label names an intervention that p.75 row 3 already backs with another site row; PEMS merges what the site splits (or the labels collide) — adjudicate which cell source governs

## `protocols/trauma/09_Trauma_PROC.md` — 2 ambiguous
- row **2** (base section) [`no_counterpart`] — Ensure scene safety. Extricate/move patient to safety if necessary.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `below_floor` — no free PEMS row in scope reaches the 0.40 floor for this row (best 0.00 against p.83 row 6) (best coverage 0.00, p.83 row 6; see `text-binding.md`)
- row **7** (base section) [`no_counterpart`] — Obtain IV/IO access.
  - why: no PEMS row in the page grid reaches the text floor and no label word binds it; the site row has no PEMS counterpart (local addition, or a PEMS row worded beyond recognition)
  - text pass: `no_evidence_local` / `best_evidence_is_held` — this row's best text evidence is p.83 row 10 (coverage 0.50, badge A), which site row 8 already holds: the row is not a local addition, it is a second site row on an already-attributed PEMS row — a shared-row adjudication, not a level fix (best coverage 0.50, p.83 row 10; see `text-binding.md`)
