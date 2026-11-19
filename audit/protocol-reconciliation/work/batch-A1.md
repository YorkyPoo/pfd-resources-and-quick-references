# Batch A1 audit - PEMS2024 vs published site (t_073f5877, parent t_d3600e06)

Scope: 04_Cardiac_Arrest_Non_Traumatic (deliberate merge of PEMS Asystole/PEA p.57-58 and V-Fib/pVT p.63-66), 04_Asystole_and_Pulseless_Electrical_Activity (p.57-58), 04_V_Fib_Pulseless_V_Tach (p.63-66). Read-only audit. No scripts run (no shell). PEMS source: pems_chunks/PEMS2024_full.txt (flattened). Full structured record: batch-A1.json. Counts reconciled: JSON 64 = table rows 64 = fixlist lines 64.

Totals: 64 discrepancies. CRITICAL 20, MODERATE 39, MINOR 5. Level decode inferred: 16 (flag CRITICAL inferred items for PDF eyeball: A1-06, A1-10, A1-33, A1-34, A1-35, A1-47, A1-49, A1-50 and the other inferred rows listed in the JSON).

Cross-file drift (the same drugs disagree across the three files): magnesium absent in merged, P-only in VF standalone; CaCl/NaHCO3 at I in merged but P-only in both standalones; amiodarone at I in merged but P-only in VF standalone; fluid at I in merged and VF standalone (PEMS A).

## 04_Cardiac_Arrest_Non_Traumatic_PROC.md (merged)

Coverage: PEMS Asystole/PEA steps 1-9 and pearls p.58; VF/pVT steps 1-15, pearls p.65, TOR p.66 against site rows 1-14 and pearls. Site rows 3, 4 are not PEMS rows (see notes in JSON).

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| A1-01 | 1 | Provider Level (Universal) | EMR Follow Universal Patient Care / Initial Patient Contact protocol. | Scene Safety / Initial Contact: Ensure scene safety and appropriate PPE. (EMR blank) | MODERATE | Fill EMR |
| A1-02 | 1 | Provider Level (DNR) | EMR Determine DNR status. Refer to Death and Criteria for Withholding Resuscitation protocol. | Determine DNR status (refer to Death and Criteria for Withholding Resuscitation protocol). (EMR blank) | MODERATE | Fill EMR |
| A1-03 | 1 | Exclusions | Patients with a valid durable DNR, rigor mortis, lividity, decomposition, or injuries inconsistent with survival are excluded. | Patients with valid durable DNR or injuries inconsistent with survival are excluded. | MODERATE | Add rigor mortis, lividity, decomposition |
| A1-04 | 2 | Provider Level (CPR) | EMR Begin chest compressions. Refer to Adult / Pediatric Cardiopulmonary Resuscitation (CPR) procedure. | Begin High-Quality CPR (EMR blank; EMT and above) | CRITICAL | Fill EMR |
| A1-05 | 3 | Pearls (airway/EtCO2) | Avoid excessive ventilation. Maximize preload. Continually monitor EtCO2 with target above 10 mmHg during CPR and 35-45 mmHg once ROSC is achieved. | Absent from pearls | MODERATE | Add PEMS airway/EtCO2 pearls |
| A1-06 | 5 | Provider Level (defib, AED) | If VF or VT is present, or AED is advising to shock [EMR], immediately defibrillate: | Defibrillation - VF/VT Only (EMR blank; EMT and above) | CRITICAL (inferred) | Fill EMR AED-only; PDF eyeball first |
| A1-07 | 6 | Provider Level (SMR) | EMR EMT Consider spinal motion restriction. | Consider spinal motion restriction if indicated (A and above) | MODERATE (inferred) | Fill EMT |
| A1-08 | 7 | Provider Level (IV/IO) | EMT A Obtain IV/IO access (humeral IO preferred if IV unavailable). | Obtain IV/IO access (I and above) | MODERATE (inferred) | Set A |
| A1-09 | 8 | Provider Level (Epinephrine adult) | A A Administer: ADULT: Epinephrine 1 mg IV/IO [0.1 mg/mL concentration] | ADULT: 1 mg IV/IO [0.1 mg/mL concentration] (I and above) | CRITICAL | Set A |
| A1-10 | 9 | Lidocaine alternative | OR, if Amiodarone is unavailable, administer: ADULT: Lidocaine (Xylocaine) 1 mg/kg IV/IO slow push. Maximum dose 100 mg. | Alternative if Amiodarone unavailable: Contact Medical Control for guidance | CRITICAL (inferred) | Add lidocaine at I |
| A1-11 | absent | Second antiarrhythmic | I If VF / VT persists, ensure optimal defibrillator pad placement, then administer: ADULT: Amiodarone (Cordarone) 150 mg IV/IO slow push | (absent) | CRITICAL | Add second-line row at I |
| A1-12 | 9 | MC gate (amiodarone P) | I If VF / VT persists, administer: ADULT: Amiodarone (Cordarone) 300 mg IV/IO slow push | P = MC | MODERATE (inferred) | P filled, standing |
| A1-13 | 10 | Fluid level/scope | A A Administer: ADULT: 0.9% Sodium Chloride IV/IO up to 1 L in 250 - 500 mL boluses (VF p.63) | Fluid Administration - Asystole/PEA Only (I and above) | MODERATE | Set A; remove Asystole-only label |
| A1-14 | 11 | MC gate (CaCl/NaHCO3 P) | I For cardiac arrest in renal dialysis patients ... also administer | P = MC | MODERATE | P filled |
| A1-15 | absent | Magnesium sulfate | I If VF / VT persists, administer: ADULT: Magnesium Sulfate 2 g IV/IO slow push | (absent) | CRITICAL | Add magnesium row at I |
| A1-16 | 11 | Separate lines | (preferably via separate lines) | (absent) | MINOR | Add the phrase |
| A1-17 | 12 | Provider Level (reversible causes) | EMR EMR Identify and treat potentially reversible causes. See Pearls below. | EMR blank; EMT and above | MODERATE | Fill EMR |
| A1-18 | 13 | TOR I standing | Termination of resuscitative efforts is a Medical Control decision only. | I filled | CRITICAL | I to MC |
| A1-19 | 13 | TOR EMR/EMT/A | MC (bare MC: every level must contact MC) | EMR, EMT, A blank | MODERATE | Set MC in EMR, EMT, A |
| A1-20 | absent | Bare MC guidance row | MC Contact Medical Control for guidance as needed. See Pearls below regarding Termination of Resuscitation. MC | (absent) | MODERATE | Add MC row |
| A1-21 | 14 | Provider Level (ROSC referral) | EMR If return of spontaneous circulation (ROSC) is achieved, refer to Cardiac Arrest: Post ROSC Care. | If ROSC achieved, refer to Post Cardiac Arrest Care (EMT and above) | MODERATE (inferred) | Fill EMR |
| A1-22 | absent | Reversible-cause list | Ensure IV/IO patency. ... Hyperthermia or Hypothermia | H's and T's list: no hyperthermia/hypothermia; no IV patency | MODERATE | Add both |
| A1-23 | absent | Pearl: magnesium | Magnesium Sulfate should be considered for: Torsades de pointes, long QT, digitalis toxicity, or suspected hypomagnesemia. | (absent) | MODERATE | Add pearl |
| A1-24 | absent | Pearl: epi dilution | If there is no Epinephrine 0.1 mg/mL preloaded syringe, combine 1 mg of Epinephrine 1 mg/mL with 9 mL of 0.9% sodium chloride in a 10 mL syrine. | (absent) | MODERATE | Add dilution pearl |
| A1-25 | absent | Criteria: two leads / AED | (check two leads), or AED advising not to shock | V-Fib/V-Tach or Asystole/PEA on monitor | MINOR | Add two-lead and AED criterion |

## 04_Asystole_and_Pulseless_Electrical_Activity_PROC.md

Coverage: PEMS p.57 steps 1-9 and pearls p.58 against site rows 1-12 and pearls. Site rows 4, 5, 7 (oxygenation, 12-lead ECG at A, EtCO2 at A) have no PEMS Asystole step; not scored.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| A1-26 | 1 | Provider Level (Universal) | EMR Follow Universal Patient Care / Initial Patient Contact protocol. | Follow Universal Patient Care / Initial Patient Contact protocol. (EMR blank) | MODERATE | Fill EMR |
| A1-27 | 1 | Provider Level (DNR) | EMR Determine DNR status. Refer to Death and Criteria for Withholding Resuscitation protocol. | Determine DNR status. Refer to Death and Criteria for Withholding Resuscitation protocol. (EMR blank) | MODERATE | Fill EMR |
| A1-28 | 2 | Provider Level (CPR) | EMR Begin chest compressions. Refer to Adult / Pediatric Cardiopulmonary Resuscitation (CPR) procedure. | Begin chest compressions. Refer to Adult / Pediatric CPR procedure. (EMR blank) | CRITICAL | Fill EMR |
| A1-29 | 3 | Provider Level (reversible causes) | EMR Identify and treat potentially reversible causes. See Pearls below. | Identify and treat potentially reversible causes. See Pearls below. (EMR blank) | MODERATE | Fill EMR |
| A1-30 | 6 | Provider Level (IV/IO) | EMT A Obtain IV/IO access (humeral IO preferred if IV unavailable). | Obtain IV/IO access (I and above) | MODERATE (inferred) | Set A |
| A1-31 | absent | Adult epinephrine | A Administer: ADULT: Epinephrine 1 mg IV/IO [0.1 mg/mL concentration] | (absent; adult half missing) | CRITICAL | Add adult row at A |
| A1-32 | 9 | Pediatric epinephrine level/scope | A Administer: ... PEDIATRIC: Epinephrine 0.01 mg/kg IV/IO [0.1 mg/mL concentration] Repeat every 3-5 minutes during cardiac arrest. | Children/Infants ONLY: If unconscious and hypotensive, with HR less than 60 ... every 3 - 5 minutes, as needed. (I and P) | CRITICAL | Set A; drop bradycardia qualifier |
| A1-33 | 10 | CaCl/NaHCO3 adult level | I For cardiac arrest in renal dialysis patients ... ADULT: Calcium Chloride 1 g IV/IO slow push | ADULT: Calcium Chloride 1 g IV/IO slow push ... (P only) | CRITICAL (inferred) | Set I |
| A1-34 | 11 | CaCl/NaHCO3 peds level | PEDIATRIC: Calcium Chloride 20mg/kg (max dose 1g) IV/IO slow push | PEDIATRIC: Calcium Chloride 20 mg/kg (max dose 1 g) IV/IO slow push (P only) | CRITICAL (inferred) | Set I |
| A1-35 | 8 | AED by EMR and energies | If VF or VT is present, or AED is advising to shock [EMR], immediately defibrillate: ADULT: 200 joules Biphasic / 360 joules Monophasic | defibrillate at maximum joules (or 2 J/kg for pediatrics) (EMR blank; rhythm ID by EMT-I or P) | CRITICAL (inferred) | EMR AED; PEMS energies; drop EMT-I/P restriction |
| A1-36 | absent | Reversible-cause pearls | Ensure IV/IO patency. ... Hyperthermia or Hypothermia ... Tablets (Overdose) | Row 3 says See Pearls below; pearls have no list | MODERATE | Add list and IV patency |
| A1-37 | absent | TOR criteria pearl | Consider contacting Medical Control to request TOR if the arrest was not witnessed by EMS and after 20 minutes of continuous CPR | Termination ... is a Poquoson Medical Control decision only. (no criteria) | MODERATE | Add criteria |
| A1-38 | 7 | EtCO2 pearls | If sudden increase in EtCO2 is noted (above 30-40 mmHg), check pulse and rhythm for ROSC. | Monitor ETCO2. If ETCO2 < 10 or dropping, reassess | MODERATE | Add ROSC check, 35-45 target, avoid excessive ventilation |

## 04_V_Fib_Pulseless_V_Tach_PROC.md

Coverage: PEMS p.63 steps 1-8, p.64 steps 9-15, pearls p.65, TOR p.66 against site rows 1-12 and pearls. Site row 12 (MC) matches PEMS bare MC.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| A1-39 | 1 | Provider Level (CPR) | EMR EMR Begin chest compression. Follow Adult/Pediatric Cardiopulmonary Resuscitation (CPR) procedure. | Begin high-quality CPR / determine DNR status (EMR blank) | CRITICAL | Split CPR; fill EMR |
| A1-40 | absent | Universal care row | EMR Follow Universal Patient Care / Initial Patient Contact protocol. | (absent) | MODERATE | Add row at EMR |
| A1-41 | 1 | Provider Level (DNR) | EMR Determine DNR status. Refer to Death and Criteria for Withholding Resuscitation protocol. | Begin high-quality CPR / determine DNR status (EMR blank) | MODERATE | Fill EMR for DNR |
| A1-42 | absent | Reversible causes row | EMR Identify and treat potentially reversible causes. See Pearls below. | (pearl label only) | MODERATE | Add row at EMR |
| A1-43 | 2 | Provider Level (SMR) | EMR EMT Consider spinal motion restriction. | Consider spinal motion restriction if indicated (A and above) | MODERATE (inferred) | Fill EMT |
| A1-44 | 3 | Provider Level (IV/IO) | EMT A Obtain IV/IO access (humeral IO preferred is IV unavailable). | Establish IV/IO (Humeral IO preferred) (I and above) | MODERATE (inferred) | Set A |
| A1-45 | 4 | Provider Level (fluid) | A A Administer: ADULT: 0.9% Sodium Chloride IV/IO up to 1 L in 250 - 500 mL boluses | Fluid Resuscitation: 0.9% Sodium Chloride up to 1 L (I and above) | MODERATE | Set A |
| A1-46 | 4 | Fluid dose limits | Repeat as needed to maintain adequate perfusion, up to 60 mL/kg total. | (absent: no bolus size, no 60 mL/kg cap) | MODERATE | Add bolus size and cap |
| A1-47 | 5 | Provider Level (AED by EMR) | If VF or VT is present, or AED is advising to shock [EMR], immediately defibrillate: | Defibrillation ... (AED for EMR/EMT, Manual for I/P) with EMR blank | CRITICAL (inferred) | Fill EMR AED; PDF eyeball first |
| A1-48 | 5 | Post-shock instruction | After each defibrillation, perform 2 minutes of CPR, followed by rhythm assessment. | (absent) | MODERATE | Add 2-minute CPR and re-shock instruction |
| A1-49 | 6 | Provider Level (epinephrine) | I A Administer: ADULT: Epinephrine 1 mg IV/IO [0.1 mg/mL concentration] | Epinephrine 1 mg (0.1mg/mL) IV/IO (I and P) | CRITICAL (inferred) | Set A |
| A1-50 | 7 | Provider Level (first antiarrhythmic) | I If VF / VT persists, administer: ADULT: Amiodarone (Cordarone) 300 mg IV/IO slow push | First Antiarrhythmic: Amiodarone 300 mg IV/IO (P only) | CRITICAL (inferred) | Set I |
| A1-51 | 7-10 | Slow push | Amiodarone 300 mg IV/IO slow push; Magnesium Sulfate 2 g IV/IO slow push; Calcium Chloride 1 g IV/IO slow push | Amiodarone 300 mg IV/IO; Magnesium Sulfate 2 g IV/IO (no slow push) | MODERATE | Add slow push |
| A1-52 | 8 | Second antiarrhythmic level | I If VF / VT persists, ensure optimal defibrillator pad placement, then administer: ADULT: Amiodarone (Cordarone) 150 mg IV/IO slow push | Second Antiarrhythmic: Amiodarone 150 mg IV/IO (P only) | CRITICAL | Set I |
| A1-53 | 9 | Magnesium level | I If VF / VT persists, administer: ADULT: Magnesium Sulfate 2 g IV/IO slow push | Persistent VF/VT: Magnesium Sulfate 2 g IV/IO (P only) | CRITICAL | Set I |
| A1-54 | 10 | CaCl/NaHCO3 level | I For cardiac arrest in renal dialysis patients ... also administer (preferably via separate lines) | Dialysis/Crush/Hyperkalemia: Calcium Chloride 1 g IV/IO ... (P only) | CRITICAL | Set I |
| A1-55 | 10 | Repeat instruction | Repeat in 5 minutes if no change. | (absent) | MODERATE | Add |
| A1-56 | 10 | Flush volume/separate lines | Followed by 20 mL 0.9% sodium chloride flush (preferably via separate lines) | THEN flush | MINOR | Add 20 mL and separate lines |
| A1-57 | 11 | Provider Level (ROSC) | EMR If return of spontaneous circulation (ROSC) is achieved, refer to Cardiac Arrest: Post ROSC Care. | Proceed to Post ROSC Care if pulses return (EMT and above) | MODERATE (inferred) | Fill EMR |
| A1-58 | absent | Pearl: magnesium | Magnesium Sulfate should be considered for: Torsades de pointes, long QT, digitalis toxicity, or suspected hypomagnesemia. | (absent) | MODERATE | Add pearl |
| A1-59 | absent | Pearl: epi dilution | If there is no Epinephrine 0.1 mg/mL preloaded syringe, combine 1 mg of Epinephrine 1 mg/mL with 9 mL of 0.9% sodium chloride | (absent) | MODERATE | Add pearl |
| A1-60 | absent | Pearls: airway/EtCO2 | Avoid excessive ventilation. Maximize preload. ... Use quantitative EtCO2 monitoring with BVM | (absent) | MODERATE | Add pearls |
| A1-61 | absent | Pearl: TOR criteria | Consider contacting Medical Control to request TOR if the arrest was not witnessed by EMS and after 20 minutes of continuous CPR | (absent) | MODERATE | Add criteria |
| A1-62 | absent | Pearl: reversible causes list | Identify and treat per appropriate protocol and scope of practice: Hypoxia; ... Hyperthermia or Hypothermia; ... | Reversible causes (H's and T's). (label only) | MODERATE | Add list |
| A1-63 | absent | Pearl: pad adjustment | consider adjustment is multiple shocks are delivered without a change in rhythm | Ensure optimal defibrillator pad placement. | MINOR | Add sentence |
| A1-64 | absent | Criteria: two leads | apparent on the cardiac monitor (check 2 leads), or AED advising to shock. | VF/VT on monitor or AED advise shock | MINOR | Add check 2 leads |

## Notes for the orchestrator / developer

- No protocol is VERIFIED. All three are FIXABLE. No MANUAL protocols (all PEMS sections were located and read).
- Blocking inferred CRITICAL items (A1-06, A1-10, A1-33, A1-34, A1-35, A1-47, A1-49, A1-50) depend on the flattened-text decode. Have a human eyeball PEMS2024.pdf p.57, p.63 and p.64 before editing. The [EMR] AED bracket on p.63 is the key one.
- The three files must be fixed together. The merged file and the standalones disagree on magnesium, amiodarone level, and CaCl/NaHCO3 level (see drift note above).
- Not scored (site content with no PEMS Asystole/VF step): merged row 3 airway level, merged row 4 AED row, Asystole rows 4, 5, 7, Asystole row 2 bradycardia text. Flagged for orchestrator decision.
- PEMS typos preserved in quotes: 'syrine' (VF p.65); PEMS spells Amiodarone as 'Cordarone' in the drug name only.
