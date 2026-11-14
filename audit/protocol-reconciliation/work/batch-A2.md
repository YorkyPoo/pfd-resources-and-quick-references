# Batch A2 — PEMS2024 vs published site (parent t_d3600e06, task t_3024221a)

Read-only audit. No files under docs/, the vault, or scripts were edited. No scripts were run (no shell). PEMS source: `pems_chunks/PEMS2024_full.txt` (page markers used as PEMS page numbers). The PEMS PDF could not be opened (NeedsOcrError, pages 47 and 151), so every CRITICAL item needs a human check of the PDF before developer edits.

Totals: 40 discrepancies (14 CRITICAL, 26 MODERATE, 0 MINOR) across 3 protocols. 1 protocol MANUAL (Aortic Dissection) — no PEMS source. 9 inferred levels.

---

## docs/protocols/cardiac/04_Post_Resuscitation_Care_PROC.md

Coverage: PEMS p.59-60 read in full (no truncation). All 8 site rows and all 5 site pearls compared. No MC row exists in PEMS, and none was invented. Status FIXABLE; 12 discrepancies (3 CRITICAL, 9 MODERATE).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| A2-01 | absent | Missing row: Universal Patient Care (EMR) | "EMR Follow Universal Patient Care / Initial Patient Contact protocol." | (absent) | MODERATE | Add Universal row with EMR • |
| A2-02 | 1 | Provider Level (EMR) | "EMR Follow Airway Management and Ventilatory Support procedure." | "Airway management / Ventilatory support" — EMR blank, EMT • | MODERATE | Set EMR • on row 1 |
| A2-03 | 2 | Provider Level (EMT) | "EMT Assess blood glucose. If less than 60 mg/dL, refer to Hypoglycemia protocol." | "Assess Blood Glucose (treat < 60 mg/dL per protocol)" — A • | MODERATE | Set EMT • on row 2 |
| A2-04 | 3 | Provider Level (EMT) | "EMT Obtain and transmit a 12-Lead ECG." | "Obtain / transmit 12-lead ECG (STEMI Triage if indicated)" — A • | MODERATE | Set EMT • on row 3 |
| A2-05 | 4 | Provider Level (A) | "A Obtain IV/IO access (humeral IO preferred if IV unavailable)." | "Obtain IV/IO (Humeral IO preferred if IV unavailable)" — I • | MODERATE | Set A • on row 4 |
| A2-06 | 5 | Provider Level (A) | "A A Consider: ADULT: 0.9% Sodium chloride up to 1 L IV/IO in 250 – 500 mL boluses" | "Fluid Bolus: ADULT: 0.9% Sodium Chloride up to 1 L…" — I • | MODERATE | Set A • on row 5 |
| A2-07 | 6 | Provider Level (I) — vasopressor infusion | "A I Maintain mean arterial pressure (MAP) above 65 mmHg. Consider: ADULT: Norepinephrine (Levophed) infusion 5 – 20 mcg/min IV/IO … OR ADULT: Epinephrine infusion 2 – 10 mcg/min IV/IO" | "Maintain MAP > 65 mmHg: ADULT: Norepinephrine infusion 5 - 20 mcg/min IV/IO OR … Epinephrine infusion 2 - 10 mcg/min IV/IO" — P only | CRITICAL | Set I • on row 6 (P stays •) |
| A2-08 | 6 | Concentration omitted | "(Add 4 mg of Norepinephrine to 250 mL 0.9% Sodium chloride = 16 mcg/mL) … (Add 1 mg of Epinephrine [1mg/mL] to 100 mL of 0.9% Sodium chloride = 10 mcg/mL)" | (no concentration in row 6) | MODERATE | Add both PEMS concentrations |
| A2-09 | 7 | Provider Level (I) + MC bracket | "[ I ] Maintain age adjusted SBP. Consider: PEDIATRIC: Epinephrine 0.1 - 1 mcg/kg/min IV/IO infusion. Max dose: 10 mcg/min." | "Pediatric SBP Support: PEDIATRIC: Epinephrine infusion 0.1-1 mcg/kg/min IV/IO" — P only, no MC | CRITICAL | Set [I] at I on row 7 (MC required) |
| A2-10 | 7 | Concentration omitted | "(Add 1 mg of Epinephrine [1mg/mL] to 100 mL of 0.9% Sodium chloride = 10 mcg/mL)" | (no concentration in row 7) | MODERATE | Add pediatric concentration |
| A2-11 | 8 | Provider Level (P) — push-dose epinephrine absent | "[ I ] P To maintain MAP > 65 until a vasopressor infusion is prepared, consider: ADULT: Push dose Epinephrine 5-10 mcg IV/IO every 2-3 minutes" | "Bridge Therapy: ADULT: Push dose Epinephrine 5 - 10 mcg IV/IO every 2-3 minutes" — no level cell | CRITICAL | Set P • on row 8 |
| A2-12 | 8 | Concentration omitted | "Add 100 mcg Epinephrine (1mL of 0.1 mg/mL) to 9mL of 0.9% Normal Saline = 10 mcg / mL" | (no concentration in row 8) | MODERATE | Add push-dose preparation |

Count: 12 discrepancies — CRITICAL 3 (A2-07, A2-09, A2-11); MODERATE 9.
Verified against PEMS: NS 1 L / 250–500 mL; 20 mL/kg peds, max 60 mL/kg; NE 5–20 mcg/min; epi 2–10 mcg/min; peds epi 0.1–1 mcg/kg/min, max 10 mcg/min; SBP targets; push-dose 5–10 mcg q2–3 min. PEMS concentration arithmetic verified (4 mg/250 mL = 16 mcg/mL; 1 mg/100 mL = 10 mcg/mL; 100 mcg/10 mL = 10 mcg/mL). Pearls 1–5 match.

---

## docs/protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md

Coverage: PEMS p.61-62. PEMS p.61 final line ("If transporting and the patient is in cardiac arrest, ... ") is truncated in the reader output; its remainder is unreadable. p.62 PEARLS read in full. Verified = false. Status FIXABLE; 14 discrepancies (6 CRITICAL, 8 MODERATE).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| A2-13 | 1 | Provider Level (EMR) — bleeding control and CPR | "EMR EMR Control sites of major active external bleeding … EMR EMR Begin chest compressions." | "Control major active external bleeding / Begin CPR" — EMR blank, EMT • | CRITICAL | Set EMR • on row 1 |
| A2-14 | 2 | Provider Level (EMT) | "EMT EMT Open the airway. Refer to Airway Management and Ventilatory Support procedure." | "Open the airway / Ventilate" — A • | MODERATE | Set EMT • on row 2 |
| A2-15 | 3 | Provider Level (EMT) — AED/monitor | "EMT EMT Apply AED or cardiac monitor. Assess rhythm (I / P):" | "Apply AED / Monitor (Assess rhythm before CPR if possible)" — A • | CRITICAL | Set EMT • on row 3 |
| A2-16 | 4 | Provider Level (EMT) — withholding (inline) | "For Asystole at the time of EMS arrival: Consider withholding / terminating resuscitation." | "Asystole on arrival: Consider withholding CPR" — A • | MODERATE (inferred) | Set EMT • on row 4 or cross-reference the Withholding protocol |
| A2-17 | 5 | Provider Level (EMT) — continue CPR / defibrillate (inline) | "For PEA/Witnessed Asystole: Continue CPR. For VF/VT: Continue CPR and defibrillate." | "PEA / VF / VT: Continue CPR / Defibrillate if indicated" — A • | CRITICAL (inferred) | Set EMT • on row 5 |
| A2-18 | 6 | Provider Level (A) — IV/IO | "EMT A Obtain IV/IO access. Establish secondary IV/IO access if possible." | "Obtain IV/IO access (x2 preferred)" — I • | MODERATE | Set A • on row 6 |
| A2-19 | 7 | Provider Level (A) — saline (inline) | "If blood products are not available, administer: ADULT: 0.9% Sodium chloride up to 1 L IV/IO in 250 – 500 mL boluses" | "If blood unavailable: 0.9% Sodium Chloride up to 1 L IV/IO (Adult)…" — I • | MODERATE (inferred) | Set A • on row 7 |
| A2-20 | 8 | Provider Level (I) — shock index (cross-protocol, PEMS Trauma p.84) | "I If considering intubation, assess Shock Index (Heart Rate / Systolic Blood Pressure).* If Shock Index is greater than 1, consider resuscitation prior to intubation." | "Assess Shock Index > 1 / Resuscitate prior to intubation" — P only | MODERATE | Remove from this protocol, or set I • to match PEMS Trauma p.84 |
| A2-21 | absent | Missing row: Endotracheal intubation (I) | "A I Secure airway with endotracheal intubation. … Intubation of children under 12 years old is a Paramedic 'red dot' skill only." | (absent) | CRITICAL | Add ETI row: I+ (12+), P only under 12 |
| A2-22 | 9 | Provider Level (I) and indication — chest decompression | "I If signs or suspicion of thoracoabdominal trauma are present (blunt or penetrating), perform bilateral chest decompression." | "Perform bilateral chest decompression for tension pneumo" — P only | CRITICAL | Set I • on row 9; broaden indication to PEMS wording |
| A2-23 | absent | Missing row: Epinephrine for PEA (A) | "A If ROSC is not achieved, and rhythm remains PEA, administer: ADULT: 1 mg Epinephrine 0.1 mg/mL IV/IO PEDIATRIC: 0.01 mg/kg Epinephrine IV/IO Single dose only." | (absent) | CRITICAL | Add epinephrine row A+ with doses and single-dose limit |
| A2-24 | 10 | Provider Level (EMR) and destination — transport (inline) | "Consider immediate transport to the closest Emergency Department or Trauma Center." | "Rapid transport to Level I/II Trauma Center (Goal < 10 mins)" — EMR blank | MODERATE (inferred) | Set EMR • on row 10; use "closest Emergency Department or Trauma Center" (Level I/II text is from PEMS Trauma p.84) |
| A2-25 | 11 | MC trigger omitted | "MC If there are no signs of life after 15-20 minutes of resuscitation, or at any time … contact Medical Control." | "Contact Poquoson Medical Control for guidance / destination" — MC all levels | MODERATE | Add the 15–20 minute trigger |
| A2-26 | absent | Missing PEARLS/notes | "Note: CPR should NOT impede procedural interventions …" and "Providers must weigh the risks of resuscitation and transport …" | (absent) | MODERATE | Add both statements |

Count: 14 discrepancies — CRITICAL 6 (A2-13, A2-15, A2-17, A2-21, A2-22, A2-23); MODERATE 8.
Inferred levels: A2-16, A2-17, A2-19, A2-24.
Severity note for reviewer: A2-13 rates EMR narrowing of CPR/bleeding control as CRITICAL. Batch A1 rated the missing EMR pediatric-compressions row (F-BR-03) MODERATE. These should be harmonised.

---

## docs/protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md

Coverage: PEMS p.135 read in full. PEMS p.136 PEARLS are truncated after "…Confirm agency dosing for cardioversion and de..." — the rest is unreadable. Site pearls 4 and 5 are not verifiable and are not counted. Dividers (site rows 3 and 11) not flagged, per the batch instruction. Verified = false. Status FIXABLE; 14 discrepancies (5 CRITICAL, 9 MODERATE).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| A2-27 | 1 | Provider Level (EMR) — Universal | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care / Initial Patient Contact" — EMR blank, EMT • | MODERATE | Set EMR • on row 1 |
| A2-28 | 4 | Provider Level (EMT) — 12-lead ECG | "EMT Obtain and transmit a 12-Lead ECG." | "EMT: Obtain and transmit 12-Lead ECG" — A • | MODERATE | Set EMT • on row 4 |
| A2-29 | 5 | Provider Level (A) — IV access | "A Obtain IV access." | "A: Obtain IV access" — I • | MODERATE | Set A • on row 5 |
| A2-30 | 6 | Provider Level (A) — saline (inline) | "Consider: ADULT: 0.9% Sodium chloride up to 1 L IV/IO in 250 – 500 mL boluses" | "A: 0.9% Sodium chloride up to 1 L IV/IO…" — I • | MODERATE (inferred) | Set A • on row 6 |
| A2-31 | 7 | Provider Level (I) — adenosine 6 mg | "A I If the rhythm is regular, consider: ADULT: Adenosine (Adenocard) 6 mg IV/IO followed by a 20 mL 0.9% Sodium chloride flush." | "I: If rhythm regular, Adenosine (Adenocard) 6 mg IV/IO…" — P only | CRITICAL | Set I • on row 7 |
| A2-32 | 8 | Provider Level (I) and "one time" limit — adenosine repeat (inline) | "If no conversion within 2 minutes, consider repeating one time at double the initial dose." | "I: If no conversion after 2 minutes, repeat Adenosine at DOUBLE initial dose" — P only, no limit | CRITICAL (inferred) | Set I • on row 8; add "one time only" |
| A2-33 | 9 | Provider Level (I) — irregular/AF transport and monitor | "I If the rhythm is irregular/atrial fibrillation, initiate transport to an appropriate facility. Monitor for signs of poor perfusion." | "I: If rhythm irregular/atrial fibrillation, initiate transport…" — P only | MODERATE | Set I • on row 9 |
| A2-34 | 10 | Bracket vs bare MC | "I MC Contact Medical Control if uncertain regarding rhythm… MC" (bare MC) | "MC: Contact Poquoson OMD for guidance…" — [I] at I, • at P, EMR/EMT/A blank | MODERATE | MC in all five cells |
| A2-35 | 12 | Provider Level (I) — midazolam sedation; P-only MC | "I For light sedation, if time and patient condition permit, consider: ADULT: Midazolam (Versed) 2.5 mg IV/IO or 5 mg IN/IM…" | "I: For light sedation, consider Midazolam (Versed)…" — I blank, P = MC | CRITICAL | Set I • on row 12; remove P MC |
| A2-36 | 13 | Provider Level (I) — monitoring (inline) | "Monitor SpO2 and EtCO2." (within the I midazolam row) | "I: Monitor SpO₂ and EtCO₂ during sedation" — no level | MODERATE (inferred) | Set I • on row 13 |
| A2-37 | 14 | Provider Level (I) — synchronized cardioversion 100 J | "I Perform synchronized cardioversion. ADULT: 100 joules initial dose … PEDIATRIC: 1 joule/kg initial dose" | "P: Perform SYNCHRONIZED cardioversion 100 joules…" — P only | CRITICAL | Set I • on row 14 |
| A2-38 | 15 | Provider Level (I) — repeat cardioversion (inline) | "If cardioversion is unsuccessful, check pad placement and repeat at 200 joules. … repeat at 2 joules/kg." | "P: If unsuccessful, check pad placement and repeat at 200 joules…" — P only | CRITICAL (inferred) | Set I • on row 15 |
| A2-39 | 16 | Bracket / level — MC after two attempts (inline) | "If cardioversion is unsuccessful after two attempts, contact Medical Control for guidance." | "P: If unsuccessful after two attempts, MC: Contact Poquoson OMD" — [P] at P, I blank | MODERATE (inferred) | Set I • on row 16; no P-only bracket |
| A2-40 | absent | Missing criteria/PEARLS | "For wide complex tachycardias, refer to Ventricular Tachycardia with a Pulse." · "Unstable vs stable: Unstable patients are those with signs/symptoms consistent with poor or inadequate perfusion…" · "There are many potential causes for tachyarrhythmias…" | (absent) | MODERATE | Add the three statements |

Count: 14 discrepancies — CRITICAL 5 (A2-31, A2-32, A2-35, A2-37, A2-38); MODERATE 9.
Inferred levels: A2-30, A2-32, A2-36, A2-38, A2-39.

---

## docs/protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md

Coverage: MANUAL — verified = false — 0 discrepancies. No findings were invented.

Reason:
- No "Aortic Dissection" protocol exists in `pems_chunks/PEMS2024_full.txt`. The only case-insensitive hit for aortic/aneurysm is the Hypotension & Shock pearl at line 645 (p.114: "Pipe problem: … such as aortic dissection or pulmonary embolism").
- `pems_chunks/Aortic_Dissection.txt` is a mis-chunk. It contains the PEMS Hypotension & Shock text (p.114–115).
- `protocol_index.json` and `mapping.json` point "Aortic Dissection" at that same pearl and mis-chunked file.
- `pems_chunks/ODEMSA_Aortic_Dissection.txt` (and `.pdf`) is the legacy ODEMSA Protocol 2-5, "REVISED: 06/2015". It is not PEMS 2024. The site's own source line cites this ODEMSA document.
- The PEMS PDF cannot be read (NeedsOcrError).

Needed from a human: confirm whether PEMS 2024 contains an Aortic Dissection protocol. If it does, supply its text. If it does not, the site's provenance (ODEMSA 2015) must be re-sourced.

Non-PEMS observations, not counted:
- Site pearl 6 ("DO NOT administer Aspirin if aortic dissection or AAA is suspected") is broader than the ODEMSA 2015 row 4 wording ("DO NOT administer ASA if acute MI is present in conjunction with suspected AAA or aortic dissection").
- Site pearls 5, 7, 8, 9 and the row 11 [A] MC requirement have no counterpart in the ODEMSA 2015 text.
- The Norepinephrine chart matches the ODEMSA 2015 chart (spot-check: 45–50 kg 4.50–25.00 mcg/min; 126–130 kg 12.60–65.00).

---

## Count reconciliation

| Protocol | Discrepancies (A, JSON) | Table rows (B, this file) | Fixlist lines (C) | CRITICAL | MODERATE | MINOR |
|---|---|---|---|---|---|---|
| Post ROSC | 12 | 12 | 12 | 3 | 9 | 0 |
| Traumatic | 14 | 14 | 14 | 6 | 8 | 0 |
| SVT | 14 | 14 | 14 | 5 | 9 | 0 |
| Aortic (MANUAL) | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **40** | **40** | **40** | **14** | **26** | **0** |

count_reconciled: true. inferred_level_count: 9 (A2-16, A2-17, A2-19, A2-24, A2-30, A2-32, A2-36, A2-38, A2-39).
