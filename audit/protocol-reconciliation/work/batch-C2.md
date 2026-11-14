# Batch C2 — PEMS2024 vs published site (respiratory) — parent t_d3600e06, task t_fa9af832

READ-ONLY audit. No file under docs/, the vault, or scripts was edited. No scripts were run (reviewer has no shell).

**Verification caveat (applies to every finding below):** PEMS text was read from `pems_chunks/PEMS2024_full.txt` (flattened PDF text). Level codes were decoded with the rule in `work/00_method_and_notes.md`. No PDF raster view was performed. Two tool limits: (a) the read tool cuts long lines, so the tail of the Respiratory Distress pearls (p.125, after "Note: these medication…") could not be read; (b) the CPAP titration range prints as "9%-15mmHg". Before the developer edits any row, a human should eyeball pp.87-88, 121, 153-154, 185, 191, 211, 123-125, 245-248 in `/root/System/mindpalace/40 - areas/Paramedic/PEMS2024.pdf`.

**Site-table structure check (requested):** all four site tables are well-formed. Every table line in the four files matched `^\|([^|]*\|){7}$` (7 cells = the 7-column header); none matched 8+ cells. The malformed table the parent flagged is in the **vault** copy, `…/Poquoson Fire and Rescue Patient Care Protocols/03 - Respiratory/03_Pediatric_Stridor_PROC.md`: rows 6–11 have 8 cells. It is not in the site copy.

---

## docs/protocols/respiratory/03_Smoke_Inhalation_PROC.md

Coverage: **MANUAL, verified=false.** No PEMS section is titled "Smoke Inhalation". Covered PEMS text: Burn Injuries (p.87-88: airway-injury ETI, hydroxocobalamin, burn-center criteria, fluids, IV access), Overdose/Cyanide (p.121), Hydroxocobalamin drug sheet (p.191), ETI procedure (p.247-248). No PEMS carbon-monoxide section was found. All 14 site rows were compared.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| C2-01 | 1 | Provider level (EMR) | "EMR Follow Universal Patient Care / Initial Patient Contact protocol." (p.87) | "• Follow Poquoson Protocols for Universal Patient Care" (EMR blank) | MODERATE | Set EMR = • |
| C2-02 | 3 | Provider level (EMR) | "EMR Assess airway and respiratory effort." (p.87) | "**Airway Assessment:**" (EMR blank, EMT •) | MODERATE | Set EMR = • |
| C2-03 | 5 | Provider level (I) | "I Consider endotracheal intubation vs immediate transport to the nearest emergency department if any signs of symptoms of airway injury develop:" (p.87) | "Consider endotracheal intubation versus immediate transport to the nearest emergency department if any signs or symptoms of airway injury develop" (P only) | MODERATE | Add I to the consider-ETI-vs-transport row. Net I-level ETI is available via row 6 with MC; see C2-04. |
| C2-04 | 6 | Bracket / MC | "I Consider endotracheal intubation…" (no MC requirement). "Note: Intubation of children under 12 years old is a Paramedic “red dot” skill only." (p.87) | "Perform endotracheal intubation per procedure" with [I] at I | MODERATE | [I] → • at I (no MC bracket); keep <12 red-dot warning |
| C2-05 | 7 | Indication / bracket | "I For altered mental status, seizures, hypotension, and/or cardiac arrest following exposure to combustion products in an enclosed space or suspected cyanide poisoning, administer (if available):" (p.88, p.121) | "Assess for exposure to combustion products/fire in an enclosed space with ANY of the following" (+ [I]) | MODERATE | Add "suspected cyanide poisoning" trigger; remove [I] unless MD directs |
| C2-06 | 8 | Preparation | "To reconstitute for infusion: Add… using the transfer spike… Fill to the line. Mix: Repeatedly invert or rock the vial for at least 60 seconds. Do not shake." (p.88) | "**Reconstitute with 200 mL 0.9% Sodium Chloride**; **Use vented IV tubing for administration**" | MODERATE | Add transfer-spike, fill-to-line, invert/rock ≥60 s, do-not-shake |
| C2-07 | 9 | Dose | "ADULT: Hydroxocobalamin (CYANOKIT) 5 g IV/IO, infuse over 15 minutes PEDIATRIC: Hydroxocobalamin (CYANOKIT) 70 mg/kg IV/IO, infuse over 15 minutes" (p.88, p.121) | "**Administer per Poquoson OMD guidance**" | **CRITICAL** | Insert adult 5 g IV/IO over 15 min; peds 70 mg/kg IV/IO over 15 min; "(if available)" |
| C2-08 | 11 | Level + dose | "A For an adult patient with SBP less than 90 and TBSA greater than 20%, administer: ADULT: 0.9% Sodium chloride at 500 mL/hr… PEDIATRIC, 6 to 12 years old: … 250 mL/hr… 5 years old and younger: … 125 mL/hr" (p.88) | "Initiate fluid resuscitation per Burn Injuries Protocol; Titrate fluid administration to hemodynamic response" (I •, P •) | MODERATE | Move to A+; add trigger and rates, or confirm referenced Burn protocol carries them |
| C2-09 | absent | IV/IO access | "A Establish IV/IO access on a non-burned extremity, if possible" (p.87); pearl: "Only if necessary … obtain IV/IO access through a burned area." (p.88) | (absent) | MODERATE | Add IV/IO row at A+ (non-burned first) |
| C2-10 | 12 | Bracket vs bare MC | "MC Contact Medical Control if most appropriate transport destination is unclear:…" (bare MC, p.88) | "**Medical Control Contact:**" [I] at I, • at P | MODERATE | MC in all five level cells (bare MC = all levels) |
| C2-11 | pearl 7; rows 12/14 | Destination priority | "Cardiac arrest, impending arrest, or airway compromise → Closest emergency department… None of the above AND any of the following → Consider transport to a Burn Center" and "airway compromise … takes priority over direct transport to a burn center. Do not bypass a trauma center…" (p.88) | Pearl 7: "Contact the Regional Burn Center early for patients with significant burn injuries, especially those involving the airway…" Row 14: "Transport to facility capable of managing combined trauma/burns if indicated" | **CRITICAL** | Airway compromise → closest ED; burn center only when none apply; state airway priority. MD to confirm |
| C2-12 | 12 | Burn-center criteria | "Consider transport to a Burn Center: … Inhalation injuries • Burns to the face…" (p.88) | "Contact **Regional Burn Center** for significant burn injuries requiring specialized care" | MODERATE | Replace with PEMS criteria list (inhalation injury listed) |
| C2-13 | pearl 2 | RSI scope | "RSI is a Paramedic only skill and not addressed in PEMS regional protocols" (p.87); "qualified RSI paramedic… is preferred" (p.88) | Pearl 2 has no RSI scope statement | MODERATE | Add PEMS RSI scope statement |

**Verified-consistent (no finding):** hydroxocobalamin 200 mL NS reconstitution and vented tubing (PEMS precautions p.191); caution on severe HTN and red/purple urine (PEMS side effects); <12 intubation red-dot / I may not intubate <12 (pearl 3, matches ETI p.247); row 7 trigger list otherwise matches.

**Un-sourced (no PEMS text found; not counted):** row 2 scene time; row 4 positioning/suction/high-flow O2 at EMT (PEMS RD p.123 grants supplemental O2 at EMR for respiratory distress; cross-protocol, MD to decide); row 13 monitoring; row 14 aeromedical; pearls 4-6.

**Totals: 13 (CRITICAL 2, MODERATE 11).**

---

## docs/protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md

Coverage: **FIXABLE, verified=true.** PEMS "Airway / Inhalation Irritants" p.153-154 read in full. All 12 site rows and the pearls were compared. ETI (p.247) was used for row 10.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| C2-01 | 1 | Provider level (EMR) | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." (p.153) | "Follow Universal Patient Care / Initial Patient Contact protocol." (EMR blank, EMT •) | MODERATE | Set EMR = • |
| C2-02 | 5 | Provider level (EMT) | "EMT Follow Airway Management and Ventilatory Support procedure." (p.153) | "**Airway Management - Basic:** • Follow Airway Management and Ventilatory Support procedure." (A+) | **CRITICAL** | Set EMT = • (time-critical airway management narrowed to A) |
| C2-03 | 6 | Provider level (A) | "EMT A Administer: ADULT: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Repeat as necessary." (p.153) | "**Adult:** **3 mL of 0.083% solution**, nebulized; repeat as necessary" (I+) | MODERATE | Set A = • (dose and repeat wording already match) |
| C2-04 | 7 | Provider level (A) | "A A Administer: ADULT: Methylprednisolone (Solu-Medrol) 125 mg IV/IO slow push." (p.153) | "**Adult:** **125 mg IV/IO** slow push" (I+) | MODERATE | Set A = • (dose matches) |
| C2-05 | 8 | Provider level (A) — **inferred** | "A For suspected Chlorine gas exposure, consider: ADULT: Sodium bicarbonate 2 mL diluted with 2 mL 0.9% Sodium chloride, nebulized. Once." (p.153) | "**Sodium Bicarbonate - Chlorine Gas Exposure Only:**" (I+) | MODERATE | Set A = •. Verify level on PDF p.153 (inferred from flattened text) |
| C2-06 | 8 | Indication wording | "For suspected Chlorine gas exposure, consider:" (p.153) | "Chlorine Gas Exposure Only" | MINOR | "Suspected chlorine gas exposure" |
| C2-07 | 10 | Provider level (I) — ETI | "I Orally intubate. Patients 12 years and older." / "P Orally intubate. Patients <12 years old." (p.247) | "**Endotracheal Intubation:** • Follow Endotracheal Intubation procedure." (P only; row 9 also P only) | **CRITICAL** | Set I = • for ETI ≥12 (rows 9 and 10); keep P-only <12 |
| C2-08 | 12 | Bracket vs bare MC | "MC Contact Medical Control for guidance as needed. MC" (p.153) | "**Medical Control Contact:** Contact Poquoson OMD for guidance as needed." ([I] at I, • at P) | MODERATE | MC in all five level cells |
| C2-09 | absent | Cross-reference | "For respiratory distress due to nerve agents / organophosphates, refer to Nerve Agents protocol." (p.153) | (absent) | MODERATE | Add referral to Nerve Agents protocol |

**Un-sourced, not counted:** pearls 5-8 (phosgene delayed edema, H2S knockdown/SCBA, ammonia vs chlorine, pneumonitis/ARDS) are not in the PEMS text read. Flag for content review.

**Totals: 9 (CRITICAL 2, MODERATE 6, MINOR 1).**

---

## docs/protocols/respiratory/03_Pediatric_Stridor_PROC.md

Coverage: **FIXABLE, verified=false.** "Pediatric Stridor" is not a PEMS title. Source = "Stridor" subsection of Respiratory Distress (p.124), with general RD rows (p.123), CPAP (p.245-246) and ETI (p.247-248). The RD pearl tail (p.125) is truncated in the read tool.

**Site structure: well-formed** (14 table lines, all 7 cells; see top). The vault copy has the malformation (rows 6–11, 8 cells).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| C2-01 | 1 | Provider level (EMR) | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." (p.123) | "Follow Universal Patient Care Poquoson Protocol for all patients." (EMR blank, EMT •) | MODERATE | Set EMR = • |
| C2-02 | 4 | Provider level (EMR) — O2 | "EMR Provide supplemental oxygen to maintain SpO2 > 94%." (p.123) | "**High-Flow Oxygen** … Titrate to maintain SpO2 >94%" (EMR, EMT blank; A •) | **CRITICAL** | Set EMR and EMT = •; device wording is MD decision |
| C2-03 | 6 | Provider level (EMT) — CPAP | "EMT Consider non-invasive (CPAP) or invasive (SGA) ventilatory support." (p.123); "CPAP, BiPAP, and PEEP are RED DOT procedures at all EMS Certification levels." (p.245) | "**CPAP for Upper Airway Support** … Consider CPAP for upper airway support if indicated" (P only) | **CRITICAL** | **MD decision first.** PEMS CPAP indication = respiratory distress from pulmonary edema/infection/near-drowning; upper-airway obstruction is not listed. If intended: EMT+. If not: remove the row, don't re-level it. |
| C2-04 | 8 | Provider level (A) — steroid | "A For moderate to severe symptoms, also administer: ADULT: Methylprednisolone (Solu-Medrol) 125 mg IV/IO slow push." (p.124) | "per dosing table below" (P only; table absent) | MODERATE | Set A = • with moderate-to-severe condition; fix dangling "dosing table" reference |
| C2-05 | 9 | Provider level (A) — IV/IO — **inferred** | Inferred need for IV/IO at A for A-level IV methylprednisolone (p.124) | "**IV/IO Access** …" (P only) | MODERATE | Set A = •; verify scope on PDF |
| C2-06 | 10 | Provider level (A) — nebulized epi | "A Administer: ADULT: Epinephrine 3 mg [1 mg/mL] nebulized PEDIATRIC: Epinephrine 3 mg [1 mg/mL] nebulized May repeat once, if needed." (p.124) | "**Nebulized Epinephrine for Moderate to Severe Stridor**" (all level cells blank) | **CRITICAL** | Set A = • and above. Keep "moderate to severe" only if MD approves; PEMS has no qualifier here. |
| C2-07 | 11 | Provider level / bracket / age scope — ETI | "I Consider invasive ventilatory support via endotracheal intubation." (p.123); "I Orally intubate. Patients 12 years and older." / "P Orally intubate. Patients <12 years old." (p.247) | "Intubation of children <12 requires Paramedic skill" ([P] at P) | MODERATE (escalate to CRITICAL if ≥12 in scope) | <12: P only, remove MC bracket unless MD adds it. ≥12: add I. Scope decision needed. |
| C2-08 | pearl 1 | Over-authorization — pediatric ETI at I | "IP Orally Intubate. Patients <12 years old." (p.247; P only; I not granted for <12) | "Intermediate providers must contact Medical Control prior to attempting intubation in pediatric patients." | **CRITICAL** | Delete the I/MC permission; state <12 ETI is Paramedic-only (red dot). Aligns with row 11. |
| C2-09 | absent | Missing RSI note | "Note: Intubation of spontaneously breathing patients without rapid sequence induction (RSI) is generally not recommended. RSI is not addressed in PEMS regional protocols – refer to agency specific protocols." (p.123) | (absent) | MODERATE | Add RSI note |

**Un-sourced, not counted:** row 2 calm environment, row 3 position, row 5 monitoring (A+), row 7 albuterol (site adds albuterol at P; PEMS Asthma grants EMT, the stridor section has none; verify intent), pearls 2-8 (croup/epiglottitis, steroid onset, rebound stridor, do-not-examine-oropharynx, Magill forceps).

**Dose checks:** epinephrine 3 mg [1 mg/mL] neb adult/peds, repeat once ✓. Methylprednisolone 125 mg / 2 mg/kg max 125 mg ✓.

**Totals: 9 (CRITICAL 4, MODERATE 5).** Vault malformation: separate item, see top.

---

## docs/protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md

Coverage: **FIXABLE, verified=false.** Source = "Pulmonary Edema" subsection of Respiratory Distress (p.124), CPAP (p.245-246), Nitroglycerin sheet (p.211), Furosemide sheet (p.185), RD pearls (p.125, tail truncated in read tool).

Dose and level checks requested: **CPAP PEEP 5** ✓ (units cmH2O vs PEMS mmHg, MINOR, in C2-04). **CPAP titration** → C2-05 (cap 10 vs 9–15). **Nitroglycerin 0.4 mg SL** dose ✓ (level and threshold → C2-06/07). **Furosemide 40 mg IV/IO slow push** dose ✓ (level → C2-09; contraindications → C2-10). **MC row (bare MC)** → site has MC in all five cells ✓.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| C2-01 | 1 | Provider level (EMR) | "EMR Follow Universal Patient Care / Initial Patient Contact protocol." (p.123) | "Follow Universal Patient Care / Initial Patient Contact protocol" (EMT •) | MODERATE | Set EMR = • |
| C2-02 | 2 | Provider level (EMR) | "EMR Perform a focused evaluation including pertinent history and assessment of airway and lung sounds." (p.123) | "Perform focused evaluation including assessment of airway and lung sounds" (EMT •) | MODERATE | Set EMR = • |
| C2-03 | 3 | Provider level (EMR) — O2 | "EMR Provide supplemental oxygen to maintain SpO2 > 94%." (p.123) | "Provide supplemental oxygen to maintain SpO2 > 94%" (EMT •) | **CRITICAL** | Set EMR = • |
| C2-04 | 4 (+5) | Provider level (EMT) — CPAP; qualifier | "EMT Consider non-invasive (CPAP) or invasive (SGA) ventilatory support." (p.123); "EMT Set positive and expiratory pressure (PEEP) to 5 mmHg" and "CPAP, BiPAP, and PEEP are RED DOT procedures at all EMS Certification levels." (p.245) | Row 4: "Consider non-invasive positive pressure ventilation (**CPAP**) for severe respiratory distress" (A+). Row 5: "**CPAP Initial Settings:** PEEP 5 cmH2O" (A+) | **CRITICAL** | Set EMT = • for CPAP and initial settings; drop "for severe respiratory distress" unless MD approves; PEEP unit to mmHg (MINOR) |
| C2-05 | 9 | Provider level (P) and cap | "EMT Consider titrating PEEP 9%-15mmHg as needed to improve ventilation/work of breathing." (p.245; "%" glyph — verify on PDF) | "**CPAP Titration:** Adjust PEEP up to 10 cmH2O…" (P only) | MODERATE | Set EMT = •; cap at PEMS range (confirm 15 on PDF) |
| C2-06 | 10 | Provider level (A) — nitro | "A Administer: ADULT: Nitroglycerine 0.4 mg SL" (p.124) | "**Nitroglycerin** Adult: **0.4 mg SL**" (I •, P •) | **CRITICAL** | Set A = • |
| C2-07 | 11 | Provider level (A) and threshold — nitro repeat | "If SBP remains greater than 100 mmHg (MAP 65 mmHg), may repeat every five minutes as needed, up to three doses." (p.124); pre-check "SBP ≥ 100 mmHg and MAP ≥ 65" (p.125) | "May repeat every 5 minutes as needed if SBP remains > 100 mmHg / MAP > 65 mmHg (maximum 3 doses)" (I •, P •) | **CRITICAL** | Set A = •; MAP "> 65" → "≥ 65" |
| C2-08 | 10 | Contraindications / pre-checks omitted — nitro | Nitro sheet (p.211): "CONTRAINDICTATIONS: Hypotension: SBP <100mmHg or MAP <65 Use of PDE inhibitors (eg. Sildenafil, Vardenafil, Tadalafil) … Children less than 12". RD p.125: "obtain IV access, ensure blood pressure is acceptable (SBP ≥ 100 mmHg and MAP ≥ 65), and assess for the recent use of PDE inhibitors" | No contraindication or pre-check text in row 10 or pearls | **CRITICAL** | Add nitro contraindications and pre-checks (PDE-5 inhibitor exclusion is high-risk) |
| C2-09 | 12 | Provider level (I) — furosemide | "A I Administer: ADULT: Furosemide (Lasix) 40 mg IV/IO slow push" (p.124) | "**Furosemide (Lasix)** Adult: **40 mg IV/IO slow push**" (P only) | MODERATE | Set I = • (dose matches) |
| C2-10 | 12 | Contraindications omitted — furosemide | "CONTRAINDICTATIONS: Pregnancy Hypovolemia / dehydration Hypotension: SBP <110, MAP<65" (p.185) | Pearl 5 caution only: "Exercise cautious diuresis…" | **CRITICAL** | Add furosemide contraindications (SBP<110 / MAP<65 is stricter than nitro) |
| C2-11 | pearls | CPAP pearl content missing | "Caution: Avoid aspiration when using CPAP. Use only on conscious and alert patients. Remove the mask immediately if the patient begins to vomit. Consider RSI, if available." and "Assess for pneumothorax and perform needle thoracostomy if indicated." (p.246) | Pearls 2-3 cover hypotension/pneumothorax monitoring only | MODERATE | Add the CPAP pearl content |

**Verified-consistent:** CPAP contraindications rows 6–8 match PEMS all ten items. Furosemide and nitro doses ✓. MC row 13 ✓ (bare MC, all cells). Pearl 4 (epinephrine caution in RAD + CHF) ✓.

**Un-sourced, not counted:** pearl 6 (cardiac asthma), pearl 7 GCS wording (consistent with GCS ≤13).

**Totals: 11 (CRITICAL 6, MODERATE 5).**

---

## Batch totals

| Protocol | File | Status | Verified | CRITICAL | MODERATE | MINOR | Total |
|---|---|---|---|---|---|---|---|
| Smoke Inhalation | 03_Smoke_Inhalation_PROC.md | MANUAL | false | 2 | 11 | 0 | 13 |
| Airway / Inhalation Irritants | 03_Airway_Inhalation_Irritants_PROC.md | FIXABLE | true | 2 | 6 | 1 | 9 |
| Pediatric Stridor | 03_Pediatric_Stridor_PROC.md | FIXABLE | false | 4 | 5 | 0 | 9 |
| Pulmonary Edema & Congestion | 03_Pulmonary_Edema_Congestion_PROC.md | FIXABLE | false | 6 | 5 | 0 | 11 |
| **Total** | | | | **14** | **27** | **1** | **42** |

Inferred level decodes: 2 (C2-05 Irritants row 8; C2-05 Stridor row 9). Manual protocols: Smoke Inhalation.

**Severity judgements to confirm:** (1) Oxygen blocked at EMR (PE C2-03, Stridor C2-02) is rated CRITICAL as a time-critical life-saving intervention. (2) Airway management blocked at EMT (Irritants C2-02) is CRITICAL on the same basis. (3) Stridor CPAP (C2-03) is CRITICAL on level, but the indication is not in PEMS, so the medical director must decide first. (4) Smoke destination (C2-11) is CRITICAL because PEMS routes airway compromise to the closest ED.
