# Batch D1 — PEMS2024 vs published site (read-only audit, parent t_d3600e06)

Scope: 6 protocols, every PEMS step and site row read. PEMS source is the flattened text `pems_chunks/PEMS2024_full.txt`; no PDF raster check (no shell). Level decode per work/00 notes. Totals: 75 discrepancies — CRITICAL 12, MODERATE 50, MINOR 13. Inferred level decodes: 4 (D1-15, D1-25, D1-63, D1-64).

## docs/protocols/general/02_Heat_Exposure_PROC.md
Coverage: PEMS Heat Exposure p.69-70 read in full; rows 1-7 and pearls checked. 9 discrepancies (CRITICAL 2, MODERATE 7).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| D1-01 | 1 | Provider Level | "EMR Place patient in cool environment." | "Place patient in cool environment \| (blank) \| •" (EMT+) | MODERATE | Add EMR bullet |
| D1-02 | absent | Missing Row | "EMR Follow General – Universal Patient Care/Initial Patient Contact protocol." | (absent) | MODERATE | Add EMR+ row |
| D1-03 | 2 | Provider Level | "EMT • Remove excess clothing." | "Remove excess clothing" (A+) | MODERATE | Add EMT bullet |
| D1-04 | 3 | Provider Level | "If skin temperature is normal to touch: o Apply cool compresses." | "Normal skin temp: Apply cool compresses" (A+) | MODERATE | Add EMT bullet |
| D1-05 | 4 | Provider Level | "If skin temperature is hot to touch: o Treat as life-threatening emergency. o Immediately start cooling process" | "Hot skin temp (Heat Stroke): Treat as life-threatening/start rapid cooling" (A+) | CRITICAL | Add EMT bullet (EMT must start rapid cooling) |
| D1-06 | 5 | Provider Level | "If patient begins to shiver, slow cooling process." | "Shivering: Slow the cooling process" (A+) | MODERATE | Add EMT bullet |
| D1-07 | 6 | Provider Level | "A Suspected heat stroke or hypovolemia: 20 mL/kg 0.9% Normal Saline up to 1000 mL bolus" | "Suspected heat stroke/hypovolemia: 0.9% Normal Saline 20 mL/kg up to 1000 mL bolus IV/IO" (I+) | CRITICAL | Add A bullet |
| D1-08 | 7 | Provider Level | "EMT Continuously reassess patient." | "Continuously reassess patient" (A+) | MODERATE | Add EMT bullet |
| D1-09 | absent | Missing Pearl | "Consider cold IV fluids, if available, in heat stroke patient only. Use caution in the conscious patient" | (absent) | MODERATE | Add pearl |

## docs/protocols/general/02_Cold_Exposure_PROC.md
Coverage: PEMS Cold Exposure p.67-68 read; rows 1-9 and pearls checked. PEMS text truncated in the localized-injury DO NOT list and pearl tail ("Attempt to de... [truncated]"); site pearl 5 not found in readable PEMS. verified=false. 8 discrepancies (CRITICAL 0, MODERATE 6, MINOR 2). Row 7 (cardiac arrest, EMR+) and row 9 (bare MC before AED, pearl) match.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| D1-10 | 1 | Provider Level | "EMR Follow General – Universal Patient Care/Initial Patient Contact Protocol." | EMT+ | MODERATE | Add EMR |
| D1-11 | 2 | Provider Level | "EMR Remove all wet clothing and replace with warm blankets." | EMT+ | MODERATE | Add EMR |
| D1-12 | 3 | Provider Level | "EMR Handle the patient gently and avoid excessive movement" | EMT+ | MODERATE | Add EMR |
| D1-13 | 4 | Provider Level | "Use warmed and humidified O2 if available." (EMR universal row) | EMT+ | MODERATE | Add EMR |
| D1-14 | 5 | Provider Level | "EMR Apply loose, sterile dressings to affected part" | EMT+ | MODERATE | Add EMR |
| D1-15 | 6 | Provider Level / Source | PEARLS: "If the patient is alert and responsive, use active external rewarming" (no level token) | "If patient is alert and responsive: Use active external rewarming…" EMT+ | MINOR (inferred) | Confirm level or move to Pearls |
| D1-16 | 8 | Provider Level | "EMT Transport patient immediately with resuscitation efforts continued en route" | EMR+ | MODERATE | Remove EMR |
| D1-17 | absent | Pearl Content | not found in readable PEMS p.67-68 | "During cardiac arrest, medications should be spaced at longer intervals." | MINOR | Verify PDF; remove or source |

## docs/protocols/general/02_Behavioral_Patient_Restraint_PROC.md
Coverage: PEMS Behavioral Emergencies p.71-73 read in full (one truncated de-escalation sub-bullet). Companion PEMS Patient Restraint policy p.31-32 (administrative, not level-gated) read; its CHEMICAL RESTRAINT PROCEDURE text is truncated in the flattened source so that section is not verifiable. TOC title "Behavioral/Patient Restraint" vs body "Behavioral Emergencies". verified=false. 14 discrepancies (CRITICAL 1, MODERATE 9, MINOR 4). Row 8 (bare MC) and all doses in rows 5-7 match PEMS.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| D1-18 | 1 | Provider Level | "EMR EMR Assess decision making capacity." / "EMR Assess and treat potential causes" | EMT+ | MODERATE | Add EMR |
| D1-19 | 2 | Provider Level | "EMR For mild agitation, follow de-escalation guidelines." | EMT+ | MODERATE | Add EMR |
| D1-20 | 3 | Provider Level | "EMR Restrain patient by least restrictive means necessary." | EMT+ | MODERATE | Add EMR |
| D1-21 | absent | Missing Row | "EMT As soon as feasible, assess blood glucose and initiate continuous monitoring … BP every 5 minutes." | (absent) | MODERATE | Add EMT row |
| D1-22 | 4 | Provider Level | "EMT I As soon as feasible, assess and initiate continuous monitoring of cardiac rhythm." | P only | MODERATE | Add I bullet |
| D1-23 | 5 | Provider Level | "I For moderate agitation, consider: ADULT: Haloperidol…" | P only | MODERATE | Add I bullet |
| D1-24 | 6 | Provider Level | "I For severe agitation that does not respond…: ADULT: Midazolam (Versed) 5 mg IV/IO slow push or 10 mg IM" | P only | MODERATE | Add I bullet |
| D1-25 | 7 | Provider Level (omitted) | "I P Only if the patient is severely agitated… ADULT: Ketamine (Ketalar) 4 mg/kg IM" | (no level) | CRITICAL (inferred) | Add P bullet |
| D1-26 | absent | Missing Pearl | "Consider empiric use of high-flow oxygen by mask if unable to monitor SpO2" | (absent) | MODERATE | Add pearl |
| D1-27 | absent | Missing Procedure | Restraint policy p.31: "Place the patient face up on a long backboard – NEVER PRONE… check circulation … every 15 minutes… DO NOT tighten chest straps" | (absent; row 3 refers to policy) | MODERATE | Add steps or explicit link |
| D1-28 | absent | Missing Pearl | "Persons who lack decision-making capacity are assessed and treated with implied consent." | (absent) | MINOR | Add pearl |
| D1-29 | absent | Missing Pearl | "If law-enforcement restraints have been utilized… a law enforcement officer should accompany" | (absent) | MINOR | Add pearl |
| D1-30 | absent | Missing Pearl | "If the patient has decision making capacity and does not wish to be treated… documentation should include…" | (absent) | MINOR | Add pearl |
| D1-31 | absent | Pearl Content | "Consider potential medical or traumatic causes of altered mental status: head injury, hypoxia, delirium…" | "(SMASHED2)" | MINOR | List PEMS causes |

## docs/protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md
Coverage: PEMS Drowning and Diving Injuries p.93-94 read in full; rows 1-7 and all pearls checked. 12 discrepancies (CRITICAL 0, MODERATE 12). Hyperbaric numbers and bare MC row match.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| D1-32 | 1 | Provider Level | "EMR Follow Universal Patient Care…" / "EMR Remove the patient from the water." | EMT+ | MODERATE | Add EMR |
| D1-33 | 2 | Provider Level | "EMR Consider spinal motion restriction." | EMT+ | MODERATE | Add EMR |
| D1-34 | 3 | Provider Level | "EMR Assess airway and ventilation." | EMT+ | MODERATE | Add EMR |
| D1-35 | 4 | Provider Level | "EMR Remove wet clothing and dry the skin. Keep the patient warm." | EMT+ | MODERATE | Add EMR |
| D1-36 | 5 | Provider Level / Wording | "EMR If hypothermia and hemodynamically unstable, focus effort on rewarming as well as resuscitation." | EMT+; "simultaneously" | MODERATE | Add EMR; PEMS wording |
| D1-37 | 6 | Provider Level | "EMR Diving emergencies: Consider pulmonary barotrauma…" | EMT+; "Assess for" | MODERATE | Add EMR; align wording |
| D1-38 | absent | Missing Pearl | "Caution: rewarming the extremities before the trunk may lead to vasodilation…" | (absent) | MODERATE | Add pearl |
| D1-39 | absent | Missing Pearl | "Maintain a high suspicion for blunt trauma, particularly involving the head and spine." | (absent) | MODERATE | Add pearl |
| D1-40 | absent | Missing Pearl | "…Contact Medical Control for guidance regarding continued on-scene resuscitation vs transport…" | (absent) | MODERATE | Add pearl |
| D1-41 | absent | Missing Pearl | "Handle patients with hypothermia gently – rough handling may precipitate arrythmias including lethal VF." | (absent) | MODERATE | Add pearl |
| D1-42 | absent | Missing Pearl | "Pulmonary edema may develop hours after a submersion event. Transport of all … nonfatal drowning…" | (absent) | MODERATE | Add pearl |
| D1-43 | absent | Missing Pearl | "Rapid ascent … barotrauma … the bends … arterial gas emboli…" | (absent) | MODERATE | Add pearl |

## docs/protocols/general/02_Pain_Control_PROC.md
Coverage: PEMS Pain Control p.77-79 read in full; rows 1-8 and pearls checked. 10 discrepancies (CRITICAL 1, MODERATE 9). Row 8 (bare MC), morphine and ketorolac doses, BP minimums and naloxone pearl match.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| D1-44 | 1 | Provider Level | "EMR Follow Universal Patient Care / Initial Patient Contact protocol." | EMT+ | MODERATE | Add EMR |
| D1-45 | 2 | Provider Level | "EMR Assess baseline pain level using scale below." | EMT+ | MODERATE | Add EMR |
| D1-46 | 3 | Provider Level | "EMT Assess and monitor blood pressure." | A+ | MODERATE | Add EMT |
| D1-47 | 4 | Provider Level | "A Consider treatment for nausea prior to administering an opiate: … Ondansetron 4 mg IV/IO slow push, IM, or PO" | I+ | MODERATE | Add A; add 'prior to opiate' and IO |
| D1-48 | 5 | Provider Level | "A For mild to moderate pain (2 - 5), consider: … Ketoralac (Toradol) 15 mg IV/IO or 30 mg IM" | I+ | MODERATE | Add A |
| D1-49 | 6 | Provider Level | "[A] For moderate to severe pain (6 – 10)… Fentanyl 25 – 50 mcg IV/IO over 2 minutes or IN/IM" | I+ (no MC gate) | MODERATE | Add [A] (MC) bullet |
| D1-50 | 6 | Dose (route) | "PEDIATRIC: Fentanyl … 0.5 mcg/kg IV/IO over 2 minutes or 1 mcg/kg IN/IM" | "Pediatric: Fentanyl 0.5-1 mcg/kg IV/IN/IM" | CRITICAL | Split by route |
| D1-51 | 6 | Administration rate | "…25 – 50 mcg IV/IO over 2 minutes" | no rate | MODERATE | Add 'over 2 minutes' |
| D1-52 | 6 | Repeat interval | "May repeat dose as needed every 10 - 15 minutes titrated to pain relief." | (absent rows 6-7) | MODERATE | Add repeat interval |
| D1-53 | 7 | Provider Level | "[A] … OR ADULT: Morphine Sulfate 2.5 – 5 mg IV/IO over 2 minutes or IM" | I+ (no MC gate) | MODERATE | Add [A] (MC) bullet |

## docs/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md
Coverage: PEMS Sedation Post Advanced Airway p.55-56 read in full. Site rows 1-6 and pearls checked against PEMS; site rows 4-5 (ketamine pre/post-intubation) have no source in this PEMS page. Endotracheal Intubation p.248 refers to this protocol for analgesia/sedation; PEMS ketamine card (p.195) lists RSI and behavioral indications only. 22 discrepancies (CRITICAL 8, MODERATE 7, MINOR 7).

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| D1-54 | header | Title | "Sedation Post Advanced Airway" | "Sedation (Non-Paralytic)" | MINOR | Rename |
| D1-55 | front matter | Version | "Version: January 2025" (TOC: 03/2024) | absent | MINOR | Add version |
| D1-56 | absent | Missing Row | "EMT Confirm and monitor airway placement with continuous SpO2 and box-waveform EtCO2." | (absent) | CRITICAL | Add EMT row |
| D1-57 | 1 | Provider Level | "EMR Follow Universal Patient Care / Initial Patient Contact protocol." | EMT+ | MODERATE | Add EMR |
| D1-58 | 1 | Unsourced addition | (not in PEMS page) | "Provide supplemental oxygen and/or ventilatory support." | MINOR | Cross-ref only or source |
| D1-59 | 2 | Unsourced addition | (not in PEMS page) | "Assess and monitor blood pressure…" A+ | MINOR | Source or keep |
| D1-60 | 3 | Unsourced addition | (no IV access row in PEMS) | "Establish IV/IO access." I+ | MINOR | Source or keep |
| D1-61 | 4 | Unsourced high-alert auth | (not in PEMS p.55-56) | Pre-intubation ketamine 1.5-2 mg/kg IV/IO / 4-5 mg/kg IM/IN; midazolam 2.5-5 mg IV/IO; P only | CRITICAL | Remove or source |
| D1-62 | 5 | Unsourced high-alert auth | ketamine card p.195: "Behavioral emergencies… Rapid sequence induction" only | "Post-Intubation Sedation: Ketamine 1 mg/kg IV/IO (max 100 mg)" P only | CRITICAL | Remove or source |
| D1-63 | 6 | Provider Level | "EMT I Administer: … Fentanyl…" / "I If Fentanyl is not sufficient… Midazolam" | P only | CRITICAL (inferred) | Add I bullet; I intubates per p.248 |
| D1-64 | 6 | Sequencing | "I If Fentanyl is not sufficient, administer: … Midazolam" | Midazolam parallel in "AND/OR" block | CRITICAL (inferred) | Make midazolam second-line |
| D1-65 | 6 | Dose | "PEDIATRIC: Midazolam (Versed) 0.1 mg/kg IV/IO over 2 minutes" | "0.05 mg/kg IV/IO" | CRITICAL | Correct to 0.1 mg/kg |
| D1-66 | 6 | Route | "ADULT: Midazolam 2.5 mg IV/IO over 2 minutes or 5 mg IN/IM" | IV/IO only | MODERATE | Add IN/IM |
| D1-67 | 6 | Unsourced dose caps | "Repeat every 10 - 15 minutes… (no total cap)" | total caps 10 mg / 5 mg / 150 mcg / 50 mcg | MODERATE | Source or remove |
| D1-68 | 6 | Dose (per-dose max) | "PEDIATRIC: Fentanyl … Maximum dose 25 mcg." | "(Maximum total dose: 50 mcg)" only | CRITICAL | Add 25 mcg per-dose max |
| D1-69 | 6 | Route | "ADULT: Fentanyl … 25 – 50 mcg IV/IO over 2 minutes or IN/IM" | IV/IO only | MODERATE | Add IN/IM |
| D1-70 | absent | Missing MC row | "I MC Contact Medical Control for guidance if unable to adequately manage patient agitation or discomfort. MC" | (absent) | CRITICAL | Add bare-MC row |
| D1-71 | absent | Missing Pearl | "Adjust ventilation… EtCO2 of 35 – 45 mmHg" | (absent) | MODERATE | Add pearl |
| D1-72 | absent | Missing Pearl | "Closely monitor for hypotension following intubation and sedation." | (absent) | MODERATE | Add pearl |
| D1-73 | absent | Missing Pearl | "Use suction to remove blood, secretions and vomitus as needed." | (absent) | MINOR | Add pearl |
| D1-74 | absent | Pearl Content | "Use lower doses of Fentanyl for opiate naïve, frail, low weight, hypotensive, hemodynamically labile, or elderly" | "lower doses of sedatives in frail, elderly, or opiate/benzodiazepine-naive" | MODERATE | Replace with PEMS wording |
| D1-75 | absent | Unsourced pearls | (not in PEMS p.55-56) | ketamine MI / reactive airway / transport / fentanyl+midazolam pearls | MINOR | Source or remove |

## Count reconciliation
- Discrepancies in JSON (A): 75 (D1-01 … D1-75), by protocol: Heat 9, Cold 8, Behavioral 14, Drowning 12, Pain 10, Sedation 22.
- Table rows in this file (B): 75 (9 + 8 + 14 + 12 + 10 + 22).
- Fixlist lines (C): 75.
- By severity (all three files): CRITICAL 12 (D1-05, 07, 25, 50, 56, 61, 62, 63, 64, 65, 68, 70), MODERATE 50, MINOR 13. Sum 75.
- Inferred level decodes: 4.
- MANUAL protocols: none. Protocols with verified=false (PEMS text truncated in places): Cold Exposure, Behavioral/Patient Restraint.

## Cross-batch notes
- D1-07 is graded CRITICAL (heat-stroke fluid bolus narrowed A→I). The same A-level IV fluid row in batch 07 Allergic Reaction (F-AL-09) was graded MODERATE. The two grades should be reconciled.
- Sedation rows 4-5 and the Behavioral row 7 ketamine finding should be checked against the PDF (ketamine card p.195 and sedation p.55) before editing.
