# Batch B2 audit: Stroke/TIA, Seizure, Overdose/Poisoning, Nerve Agents vs PEMS2024

Read-only audit. Parent t_d3600e06. Source: pems_chunks/PEMS2024_full.txt. Machine-readable: batch-B2.json. No files under docs/, the vault, or scripts were edited. No scripts were run.

Totals: 64 discrepancies (21 CRITICAL, 37 MODERATE, 6 MINOR). Per protocol: Stroke 15, Seizure 9, Overdose 25, Nerve Agents 15.

Decode caveat: PEMS levels were decoded from flattened text using the work/00 token rule. The PDF could not be opened (needs OCR). All CRITICAL rows need a human PDF check before the developer edits.

## docs/protocols/neurologic/05_Stroke_TIA_PROC.md

Coverage: PEMS p.131-133 read in full (Stroke/TIA table, pearls, RACE table). All 6 PEMS steps and all 9 site rows checked. Destination rules cross-checked against Stroke Field Triage flowchart (p.37), which is a separate PEMS protocol.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| B2-ST-01 | 1 | Provider Level | "EMR Follow Universal Patient Care" | "Universal Care / Assess BEFAST … • • • •" (EMT+) | MODERATE | EMR cell = • |
| B2-ST-02 | 2 | Provider Level | "EMR Assess probability of large vessel occlusion (LVO) using RACE" | "Assess RACE scale …" (EMT+) | MODERATE | EMR cell = • |
| B2-ST-03 | 3 | Provider Level | "EMR Record time the patient last seen normal" | "Record Time Last Seen Normal…" (EMT+) | MODERATE | EMR cell = • |
| B2-ST-04 | 4 | Provider Level | "EMT Obtain blood glucose level." | "Assess blood glucose (Treat <60…)" (A+) | MODERATE | EMT cell = • |
| B2-ST-05 | 5 | Provider Level | "EMT Initiate transport. Goal scene time < 15 minutes" | "Goal scene time <15 minutes / Initiate rapid transport" (A+) | CRITICAL | EMT cell = • |
| B2-ST-06 | 6 | Provider Level | "EMT … transport to the closest comprehensive stroke center" | "Triage: Symptoms <24 hrs & RACE 5-9 -> … Comprehensive" (A+) | CRITICAL | EMT cell = • |
| B2-ST-07 | 6 | Criteria | "Symptoms less than 24 hours (or unknown) AND suspected LVO" | "Symptoms <24 hrs & RACE 5-9" | CRITICAL | add "or unknown" onset |
| B2-ST-08 | 7 | Provider Level | "EMT Symptoms greater than 24 hours OR low suspicion … closest stroke center" | "Triage: Symptoms >24 hrs OR RACE 0-4 -> … Primary Stroke Center" (A+) | CRITICAL | EMT cell = • |
| B2-ST-09 | 7 | Destination | "Transport to the closest stroke center." | "Transport to closest Primary Stroke Center" | MODERATE | "closest stroke center" |
| B2-ST-10 | absent | Missing Row | "EMT MC Contact Medical Control for guidance as needed. MC" | (absent) | MODERATE | add MC row, MC in all cells |
| B2-ST-11 | absent | Missing Section | RACE table, total 0-9 (p.133) | (absent) — "Calculate RACE scale (0-9)" | MODERATE | add RACE scoring table |
| B2-ST-12 | 8 | Provider Level | pearl: "an 18g IV in the right antecubital (AC) site is preferred" (no level) | "Establish 18g IV in Right AC…" (I+) | MINOR | confirm level or remove |
| B2-ST-13 | 9 | Provider Level | pearl: "Call COR at the receiving facility…" (no level) | "Call Poquoson COR…" (A+) | MINOR | confirm level |
| B2-ST-14 | absent | Pearl | "determine … the time of onset … headache, weakness, slurred speech, dizziness" | (absent) | MODERATE | add onset pearl |
| B2-ST-15 | absent | Pearl | "endovascular therapy (available only at comprehensive/thrombectomy capable…)" | "RACE ≥ 5 indicates high probability of LVO requiring endovascular therapy." | MINOR | add "only at comprehensive" |

## docs/protocols/neurologic/05_Seizure_PROC.md

Coverage: PEMS p.127-128 table fully read. PARTIAL: the last PEARLS bullet (PEMS line 707) is cut off by the tool after "Caution: Both seizures and benzodiazepine…". The remaining text could not be read. verified=false.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| B2-SZ-01 | absent | Missing Row | "EMR Follow Universal Patient Care" | (absent) | MODERATE | add universal row, EMR |
| B2-SZ-02 | 1 | Provider Level | "EMR EMR Prevent the patient from sustaining injury" | "Prevent injury (DO NOT restrain…)" (EMT+) | MODERATE | EMR cell = • |
| B2-SZ-03 | 2 | Provider Level | "EMR EMR Provide supplemental oxygen." | "Provide supplemental O2/protect airway" (EMT+) | MODERATE | EMR cell = • |
| B2-SZ-04 | 4 | Provider Level | "EMR EMR Refer to Overdose / Poisoning / Toxic Ingestion protocol" | "Refer to Overdose/Poisoning protocol if indicated" (EMT+) | MODERATE | EMR cell = • |
| B2-SZ-05 | 3 | Provider Level | "EMR EMT Assess blood glucose level." | "Assess blood glucose (Treat per protocol)" (A+) | MODERATE | EMT cell = • (assessment only) |
| B2-SZ-06 | 5 | Provider Level | "EMT [A] If actively seizing for over 5 minutes, administer: ADULT: Midazolam (Versed) 5 mg IV/IO or 10 mg IM" | "Actively seizing >5 mins: Midazolam 5 mg IV/IO or 10 mg IM …" (I+, A blank) | CRITICAL | A cell = •, bracketed [A] |
| B2-SZ-07 | 6 | Provider Level | "Use half dose Midazolam for frail, hypotensive, underweight, and/or elderly" | "Use HALF dose Midazolam for frail/hypotensive/elderly >65y" (I+, A blank) | CRITICAL | A cell = • |
| B2-SZ-08 | 6 | Criteria | "frail, hypotensive, underweight, and/or elderly ( > 65 years)" | "frail/hypotensive/elderly >65y" | CRITICAL | add "underweight" (monograph p.205: <50 kg) |
| B2-SZ-09 | 7 | Text | "initiate transport to the closest emergency department" | "initiate transport" | MINOR | add "to closest ED" |

## docs/protocols/toxicology/06_Overdose_Poisoning_PROC.md

Coverage: PEMS p.119-121 read in full (p.122 blank). All PEMS rows and all 9 site rows checked, plus the cyanide section and pearls.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| B2-OD-01 | 1 | Provider Level | "EMR Follow Universal Patient Care" | "Follow Universal Patient Care" (EMT+) | MODERATE | EMR = • |
| B2-OD-02 | 2 | Provider Level | "EMR Remove patient from the source of exposure." | "Remove from source / decontaminate patient" (EMT+) | MODERATE | EMR = • |
| B2-OD-03 | 3 | Provider Level | "EMR Ensure adequate ventilation." | "Ensure adequate ventilation / administer supplemental oxygen" (EMT+) | MODERATE | EMR = • |
| B2-OD-04 | 3 | Target | "maintain SpO2 94 – 98%" | (no target) | MODERATE | add SpO2 94-98% |
| B2-OD-05 | absent | Missing Row | "EMR If seizing or a seizure has occurred, refer to Seizure protocol." | (absent) | MODERATE | add EMR row |
| B2-OD-06 | 4 | Provider Level | "EMT Assess blood glucose … EMT Obtain and transmit a 12-Lead ECG." | "Assess blood glucose / 12-lead ECG" (A+) | MODERATE | EMT = • (level inferred) |
| B2-OD-07 | 5 | Provider Level | "EMT If apneic/bradypneic … Naloxone (Narcan) 1 – 2 mg IN" | "Opiate Overdose: Administer Naloxone 1-2 mg IN" (A+) | CRITICAL | EMT = • |
| B2-OD-08 | 5 | Criteria | "If apneic/bradypneic … Repeat at double the initial dose if no response in 5 minutes." | "Administer Naloxone 1-2 mg IN" | MODERATE | add trigger and repeat |
| B2-OD-09 | 6 | Provider Level | "EMT A If apneic/bradypneic … Naloxone 0.5 – 2 mg IV/IO slow push or IM/IN" | "Opiate Overdose (Adult): Administer Naloxone 0.5-2 mg IV/IO/IM/IN" (I+, A blank) | CRITICAL | A = • |
| B2-OD-10 | 6 | Repeat | "Repeat at double the initial dose if no response in 5 minutes." | (absent) | MODERATE | add repeat instruction |
| B2-OD-11 | 7 | Provider Level | "I If hypotensive with signs of poor perfusion, administer: ADULT: Calcium chloride 1 g" | "CCB/BB Overdose (Adult): Calcium Chloride 1g IV/IO AND Glucagon 1mg" (P only) | CRITICAL | I = • |
| B2-OD-12 | 7 | Dose | "PEDIATRIC: Calcium Chloride 20mg/kg (max dose 1g)" | "PEDIATRIC: Calcium Chloride 20 mg/kg" | CRITICAL | add max 1 g and 20 mL NS flush |
| B2-OD-13 | 7 | Dose | "PEDIATRIC (< 25 kg): Glucagon 0.5 mg … PEDIATRIC (≥ 25 kg): Glucagon 1 mg" | "PEDIATRIC: Glucagon 0.5-1 mg IV/IO" | CRITICAL | use the two weight bands |
| B2-OD-14 | 7 | Criteria | "If hypotensive with signs of poor perfusion … If no response, refer to Hypotension and Shock" | (no indication) | MODERATE | add indication and referral |
| B2-OD-15 | 8 | Provider Level | "I For respiratory distress due to bronchorrhea, administer: ADULT: Atropine sulfate 2 mg IV/IO/IM" | "Organophosphate / Cholinergic … Atropine 2 mg IV/IO/IM" (P only) | CRITICAL | I = • |
| B2-OD-16 | 8 | Criteria | "For respiratory distress due to bronchorrhea … Repeat every 5 minutes until respiratory secretions reduce" | (no trigger, no repeat) | MODERATE | add bronchorrhea trigger and q5min repeat |
| B2-OD-17 | 8 | Dose band | "PEDIATRIC (≥ 40 kg): Atropine sulfate 2 mg" | "Adult & Pediatric >40kg: Atropine 2 mg" | MINOR | change ">40kg" to "≥40kg" |
| B2-OD-18 | 9 | Provider Level | "EMR Begin active cooling if temperature is greater than 104F / 40C." | "Anti-Cholinergic / TCA Overdose: Initiate active cooling" (EMT+) | MODERATE | EMR = •; add >104F/40C |
| B2-OD-19 | 10 | Provider Level | "I Assess and monitor cardiac rhythm … ADULT: Sodium bicarbonate 50 mEq IV/IO slow push" | "Anti-Cholinergic / TCA Overdose (Adult): Sodium Bicarbonate 50 mEq IV/IO" (P only) | CRITICAL | I = • |
| B2-OD-20 | 10 | Threshold | "For wide QRS (Adult: > 120 ms, Ped: > 90 ms) or arrhythmia" | pearl: "Wide QRS complexes >100ms" | MODERATE | correct to 120/90 ms and add arrhythmia |
| B2-OD-21 | 10 | Repeat | "Repeat once in 5 – 10 minutes for cardiac arrest or persistent ECG changes." | (absent) | MODERATE | add repeat instruction |
| B2-OD-22 | absent | Missing Row | "I … suspected cyanide poisoning … ADULT: Hydroxocobalamin (CYANOKIT) 5 g IV/IO, infuse over 15 minutes" | (absent) | CRITICAL | add cyanide section, I, with dosing and reconstitution (level inferred) |
| B2-OD-23 | absent | Missing Row | "MC Contact Medical Control for guidance as needed." | (absent) | MODERATE | add MC row to cyanide section |
| B2-OD-24 | absent | Pearl | "Contact the Poison Control Center at 1-800-222-1222" | (absent) | MODERATE | add Poison Control pearl |
| B2-OD-25 | absent | Pearl | "Maintain a low threshold to transport even well-appearing children" | (absent) | MODERATE | add pediatric transport pearl |

## docs/protocols/toxicology/06_Nerve_Agents_PROC.md

Coverage: PEMS p.159-160 read in full. All 7 PEMS rows and all 7 site rows checked, plus pearls.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| B2-NA-01 | 1 | Provider Level | "EMR Follow Universal Patient Care" | (EMT+) | MODERATE | EMR = • |
| B2-NA-02 | 2 | Provider Level | "EMR Don appropriate PPE and decontaminate the patient." | "Don appropriate PPE; decontaminate patient prior to transport" (EMT+) | MODERATE | EMR = • |
| B2-NA-03 | 3 | Provider Level / Procedure | "EMR Follow Airway Management and Ventilatory Support procedure." | "Follow Airway Management (Consider early intubation due to copious secretions)" (EMT+) | CRITICAL | EMR = •; remove or restrict intubation to I |
| B2-NA-04 | 4 | Provider Level | "EMR Refer to Nausea / Vomiting, Seizure, and/or Hypotension…" | "Refer to Nausea/Vomiting, Seizure, and Hypotension protocols as needed" (EMT+) | MODERATE | EMR = • |
| B2-NA-05 | 5 | Provider Level | "EMT If available, administer: ADULT: DuoDote Autoinjector IM" | "DuoDote Autoinjector IM (Adult and Pediatric ≥ 40kg)…" (A+) | CRITICAL | EMT = • |
| B2-NA-06 | 5 | Wording | "If symptoms persist, repeat in 5 minutes up to three doses." | "Repeat in 5 mins up to 3 doses based on symptom severity" | MINOR | use PEMS wording |
| B2-NA-07 | 6 | Provider Level | "I If symptoms persist, or if DuoDote Autoinjector is unavailable, administer: ADULT: Atropine sulfate 2 mg IV/IO/IM" | "Atropine sulfate 2 mg IV/IO/IM …" (P only) | CRITICAL | I = • |
| B2-NA-08 | 6 | Indication | "If symptoms persist, or if DuoDote Autoinjector is unavailable" | "(Use if DuoDote unavailable)" | CRITICAL | restore "if symptoms persist" |
| B2-NA-09 | absent | Pearl | "Nerve agents include … organophosphate/carbamate pesticides … Azinphos-methyl, Malathion … Novichok." | "Examples of nerve agents include Sarin (GB), Soman (GD), Tabun (GA), and VX." | MODERATE | add pesticides and Novichok |
| B2-NA-10 | absent | Dose | "Atropen … Yellow Pen: Less than 7 kg, 0.25 mg … Green pen: Over 41kg, 2mg/dose" | "If using AtroPen autoinjectors for pediatrics, utilize weight-based dosing guidelines." | CRITICAL | insert the four weight bands and doses |
| B2-NA-11 | absent | Pearl / Dose cap | "If symptoms persist, repeat every 5 minutes up to three doses." | "Large and repeated doses may be required to dry secretions." | CRITICAL | delete, or state the three-dose cap |
| B2-NA-12 | absent | Pearl | "…SCBA and chemical protective clothing… do not proceed until it is reasonably safe" | "Decontamination must occur prior to transport." | MODERATE | use PEMS wording; add SCBA/PPE |
| B2-NA-13 | absent | Pearl | "may off-gas (exhale) dangerous vapors, even after skin decontamination is complete." | (absent) | MODERATE | add off-gassing pearl |
| B2-NA-14 | absent | Pearl | "even a very small drop … (1 mL or less) … up to 18 hours later." | (absent) | MODERATE | add delayed-onset pearl |
| B2-NA-15 | absent | Pearl | "non-ambulatory should be placed in the recovery position" | (absent) | MODERATE | add recovery position pearl |

Coverage gap: "Nerve Agents (Pediatric) (Exposure)" is in the CBRNE table of contents (p.151) but no page was found in the flattened text. Pediatric nerve-agent coverage is not claimed. A human must locate it.

## Count reconciliation

- Stroke: 15 (C4 M8 m3)
- Seizure: 9 (C3 M5 m1)
- Overdose: 25 (C8 M16 m1)
- Nerve Agents: 15 (C6 M8 m1)
- Total A (JSON) = 64; table rows in B = 64; fixlist lines in C = 64.
- Severity: CRITICAL 21, MODERATE 37, MINOR 6 (21+37+6=64).
- Inferred levels: 3 (B2-OD-06, B2-OD-22, B2-SZ-05).
- MANUAL: none; Seizure is FIXABLE with verified=false (pearl tail unreadable).
