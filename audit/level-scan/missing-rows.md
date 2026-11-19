# PEMS interventions with no site row (`absent_from_site`)

Every PEMS 2024 intervention that has no counterpart on the Poquoson protocol page it belongs to. These are content gaps: the site documents the protocol but not this intervention, and nothing downstream will notice because the site row it should live on simply is not there.

**Total: 86 rows across 27 pages.** (matched 292, ambiguous 125, site rows 417)

## Reconciliation with the previous scan's 152, by cause

The 2026-11-14 scan reported **152** PEMS rows with no site row. This run reports **86**. The delta is accounted for below by cause, with every row named in `reconciliation.json` (`prior_to_now.rows`). Rows are matched by verbatim text, not row number: the two scans number rows differently.

| what happened to the prior scan's 152 rows | rows |
|---|---|
| still `absent_from_site` | 80 |
| paired to a site row on section + ordinal | 0 |
| paired to a site row on its label | 7 |
| paired to a site row on text evidence | 22 |
| paired to a site row by the C1d text-binding pass (this fix) | 1 |
| paired by the section-fallback scoring (this fix) | 0 |
| a duplicate copy inside the merged PEMS source | 6 |
| the site does write it, inside a wider site row | 21 |
| explained by an ambiguous site row (not a gap) | 13 |
| not found in this run's scope (needs a look) | 1 |
| two prior claims that this run's parse merges into one PEMS row | 1 |
| page not aligned this run | 0 |

Of the 30 rows that now pair, the mechanical screen trusts 12 outright (0 section+ordinal, 3 distinctive label, 8 text evidence, 1 text-binding pass) and finds **18 too weak to accept without a human**. All 18 were read against both texts and are recorded in `reconciliation.json` under `prior_to_now.rows[*].human_verdict` / `human_note`:

- **13 correct** — same intervention, wording or dose split differs.
- **3 correct but partial** — the site row merges this PEMS intervention with another, and the PEMS row covers part of it.
- **3 suspect** — the two rows are about different interventions and the binding rests on one shared word: 07_OB_Emergencies_PROC.md p.141#3; 03_Upper_Airway_Obstruction_PROC.md p.239#10; 09_Trauma_PROC.md p.83#3. These are counted as paired here only because that is what the aligner did; they are adjudication work for C2, not settled matches.

Going the other way, **16 rows** this run leaves unpaired were not on the old list (6 absent, 3 duplicate, 7 merged): the old scan paired them on text similarity alone, and this one will not pair a row without structural evidence. They are the rows most worth a human glance and are named in `reconciliation.json` (`new_unpaired.rows`).

**Check:** absent now 86 = 80 prior rows still absent + 6 newly absent. Of the 152 prior rows, the 72 that left the gap list are: 30 paired to a site row (0 section+ordinal, 7 label, 22 text, 1 text-binding pass, 0 section-fallback), 13 explained by an ambiguous site row, 21 merged inside a wider site row, 6 duplicate copies, 1 not in this run's scope and 1 collapsed into a single parse row.

## `protocols/cardiac/04_Bradycardia_PROC.md` — 4 missing (PEMS p.103, p.104)
- p.103 row 1 [base section #1] badge `EMR` — Ensure adequate oxygenation. Refer to Airway Management and Ventilatory Support procedure.
- p.103 row 2 [base section #2] badge `EMR` — Children/Infants ONLY: If unconscious and hypotensive, with HR less than 60, begin chest compressions . Follow Pediatric Cardiopulmonary Resuscitation (CPR) procedure. If pulselessness develops, follow Cardiac Arrest: Asystole / PEA protocol.
- p.103 row 3 [base section #3] badge `EMR` — Identify and treat potentially reversible causes. See Pearls below.
- p.103 row 4 [base section #4] badge `EMT` — Obtain and transmit a 12-Lead ECG.

## `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md` — 3 missing (PEMS p.57, p.63, p.64)
- p.57 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.
- p.63 row 0 [base section #9] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.
- p.63 row 2 [base section #11] badge `EMR` — Begin chest compression. Follow Adult/Pediatric Cardiopulmonary Resuscitation (CPR) procedure.

## `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md` — 3 missing (PEMS p.61)
- p.61 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.
- p.61 row 2 [base section #2] badge `EMR` — Begin chest compressions. Refer to Cardiopulmonary Resuscitation (CPR) procedure. Consider immediate transport to the closest Emergency Department or Trauma Center.
- p.61 row 6 [base section #6] badge `I` — Secure airway with endotracheal intubation. Refer to Endotracheal Intubation procedure. Note: Intubation of children under 12 years old is a Paramedic “red dot” skill only.

## `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` — 2 missing (PEMS p.107)
- p.107 row 2 [base section #2] badge `EMR` — If hypotensive, refer to Hypotension and Shock protocol.
- p.107 row 7 [base section #7] badge `I` — Monitor cardiac rhythm. Refer to Tachyarrhythmias or Bradycardia protocol, as needed.

## `protocols/cardiac/04_Post_Resuscitation_Care_PROC.md` — 1 missing (PEMS p.59)
- p.59 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.

## `protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md` — 3 missing (PEMS p.63, p.64)
- p.63 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.
- p.63 row 2 [base section #2] badge `EMR` — Begin chest compression. Follow Adult/Pediatric Cardiopulmonary Resuscitation (CPR) procedure.
- p.63 row 3 [base section #3] badge `EMR` — Identify and treat potentially reversible causes. See Pearls below.

## `protocols/front-matter/Universal Patient Care.md` — 5 missing (PEMS p.49, p.50, p.52)
- p.49 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.
- p.52 row 12 [Altered Mental Status Differential Diagnosis (AEIOU TIPS) #0] badge `A` — Alcohol
- p.52 row 13 [Altered Mental Status Differential Diagnosis (AEIOU TIPS) #1] badge `I` — E Endocrine, Encephalopathy, Electrolytes Insulin (hypoglycemia / hyperglycemia) O Oxygen (hypoxia), Opiates (drugs of abuse) U Uremia
- p.52 row 14 [Altered Mental Status Differential Diagnosis (AEIOU TIPS) #2] badge `I` — T Toxins, Trauma, Temperature (hyperthermia / hypothermia)
- p.52 row 15 [Altered Mental Status Differential Diagnosis (AEIOU TIPS) #3] badge `P` — I Infection Psychiatric, Porphyria S Stroke, Shock, Subarachnoid/Intracranial Hemorrhage, Space-occupying CNS Lesion, Seizure

## `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` — 1 missing (PEMS p.71, p.72)
- p.71 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.

## `protocols/general/02_Heat_Exposure_PROC.md` — 1 missing (PEMS p.69)
- p.69 row 0 [base section #0] badge `EMR` — Follow General – Universal Patient Care/Initial Patient Contact protocol.

## `protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md` — 2 missing (PEMS p.55)
- p.55 row 1 [base section #1] badge `EMT` — Confirm and monitor airway placement with continuous SpO2 and box-waveform EtCO2.
- p.55 row 4 [base section #4] badge `MC` — Contact Medical Control for guidance if unable to adequately manage patient agitation or discomfort.

## `protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md` — 4 missing (PEMS p.99, p.100, p.101)
- p.101 row 13 [Anaphylaxis #7] badge `I` — Maintain mean arterial pressure (MAP) above 65 mmHg. If the patient has not responded to repeat IM Epinephrine injections, consider: ADULT: Epinephrine infusion 2 – 10 mcg/min IV/IO (Add 1 mg of Epinephrine [1mg/mL] to 100 mL of 0.9% Sodium chloride = 10 mcg/mL)
- p.101 row 14 [Anaphylaxis #8] badge `[I]` — Maintain age adjusted SBP. If the patient has not responded to repeat IM Epinephrine injections, consider: PEDIATRIC: Epinephrine 0.1 - 1 mcg/kg/min IV/IO infusion. Max dose: 10 mcg/min. Under 1 year old: Titrate to SBP > 70 mmHg Over 1 year old: Titrate to SBP > 90 mmHg (Add 1 mg of Epinephrine [1mg/mL] to 100 mL of 0.9% Sodium chloride = 10 mcg/mL) Note: Infusion via IV pump is preferred is available. Monitor closely for signs of extravasation.
- p.101 row 15 [Anaphylaxis #9] badge `P` — To maintain MAP > 65 until a vasopressor infusion is prepared, consider: ADULT: Push dose Epinephrine 5-10 mcg IV/IO every 2-3 minutes (Add 100 mcg Epinephrine (1mL of 0.1 mg/mL) to 9mL of 0.9% Normal Saline = 10 mcg / mL)
- p.101 row 16 [Anaphylaxis #10] badge `MC` — Contact Medical Control for guidance as needed.

## `protocols/medical/07_OB_Emergencies_PROC.md` — 9 missing (PEMS p.141, p.142, p.147, p.149)
- p.141 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol. Don appropriate PPE including gloves (sterile if available), gown, and eye protection.
- p.141 row 2 [base section #2] badge `EMR` — If significant bleeding, refer to Hemorrhagic Shock protocol.
- p.141 row 7 [base section #7] badge `EMR` — Once delivery is complete, dry and stimulate the neonate. Assess heart rate, respirations, and oxygen saturation. Follow Neonatal Resuscitation protocol.
- p.141 row 8 [base section #8] badge `EMR` — Routine suctioning is no longer recommended. Only perform pharyngeal/tracheal suctioning if thick
- p.141 row 10 [base section #10] badge `EMR` — fundal massage until the placenta delivers and bleeding stops. Transport the placenta with the mother.
- p.141 row 11 [base section #11] badge `EMR` — If possible, allow skin to skin contact for the mother and baby. Apply direct pressure to any visible sites of bleeding. If bleeding continues, refer to Hemorrhagic Shock protocol and initiate transport, preferably to a facility with Obstetric capability if condition allows. PEMS Regional Patient Care Protocols, Policies and Procedures
- p.147 row 1 [base section #13] badge `EMT` — Transport to a facility with labor and delivery capability.
- p.149 row 1 [base section #18] badge `EMR` — Support life threatening problems associated with airway, breathing and circulation.
- p.149 row 2 [base section #19] badge `EMR` — Administer oxygen as needed per patient assessment.

## `protocols/neurologic/05_Seizure_PROC.md` — 1 missing (PEMS p.127)
- p.127 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.

## `protocols/neurologic/05_Stroke_TIA_PROC.md` — 1 missing (PEMS p.131)
- p.131 row 5 [base section #5] badge `MC` — Contact Medical Control for guidance as needed.

## `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` — 5 missing (PEMS p.123, p.124)
- p.123 row 1 [base section #1] badge `EMR` — Perform a focused evaluation including pertinent history and assessment of airway and lung sounds. Refer to Airway Management and Ventilatory Support procedure (includes airway foreign body).
- p.123 row 3 [base section #3] badge `EMT` — Consider non-invasive (CPAP) or invasive (SGA) ventilatory support.
- p.123 row 4 [base section #4] badge `I` — Consider invasive ventilatory support via endotracheal intubation. Refer to Endotracheal Intubation procedure. Note: Intubation of spontaneously breathing patients without rapid sequence induction (RSI) is generally not recommended. RSI is not addressed in PEMS regional protocols – refer to agency specific protocols for guidance.
- p.124 row 10 [Bronchiolitis #0] badge `A` — Provide suctioning as needed and consider: PEDIATRIC: 0.9% Sodium Chloride, 6 mL nebulized. Repeat as needed for increased work of breathing due to secretions.
- p.124 row 11 [Pulmonary Edema #0] badge `A` — Administer: ADULT: Nitroglycerine 0.4 mg SL If SBP remains greater than 100 mmHg (MAP 65 mmHg), may repeat every five minutes as needed, up to three doses.

## `protocols/respiratory/03_Pediatric_Stridor_PROC.md` — 4 missing (PEMS p.123, p.124)
- p.123 row 1 [base section #1] badge `EMR` — Perform a focused evaluation including pertinent history and assessment of airway and lung sounds. Refer to Airway Management and Ventilatory Support procedure (includes airway foreign body).
- p.123 row 4 [base section #4] badge `I` — Consider invasive ventilatory support via endotracheal intubation. Refer to Endotracheal Intubation procedure. Note: Intubation of spontaneously breathing patients without rapid sequence induction (RSI) is generally not recommended. RSI is not addressed in PEMS regional protocols – refer to agency specific protocols for guidance.
- p.124 row 11 [Pulmonary Edema #0] badge `A` — Administer: ADULT: Nitroglycerine 0.4 mg SL If SBP remains greater than 100 mmHg (MAP 65 mmHg), may repeat every five minutes as needed, up to three doses.
- p.124 row 13 [Pulmonary Edema #2] badge `MC` — Contact Medical Control for guidance as needed.

## `protocols/respiratory/03_Pneumothorax_PROC.md` — 1 missing (PEMS p.243)
- p.243 row 0 [base section #0] badge `I` — Administer oxygen at 15 LPM (100% FiO2).

## `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` — 5 missing (PEMS p.123, p.124)
- p.123 row 4 [base section #4] badge `I` — Consider invasive ventilatory support via endotracheal intubation. Refer to Endotracheal Intubation procedure. Note: Intubation of spontaneously breathing patients without rapid sequence induction (RSI) is generally not recommended. RSI is not addressed in PEMS regional protocols – refer to agency specific protocols for guidance.
- p.123 row 5 [Asthma, COPD, Reactive Airway Disease #0] badge `EMT` — Administer: ADULT: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Repeat as necessary. ADULT: Ipratropium Bromide 3 mL of 0.02% solution, nebulized. Once. PEDIATRIC: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Repeat as necessary. PEDIATRIC: Ipratropium Bromide 3 mL of 0.02% solution, nebulized. Once.
- p.124 row 7 [Asthma, COPD, Reactive Airway Disease #2] badge `I` — For severe symptoms, also administer: ADULT: Magnesium Sulfate 2 g IV/IO infusion over 15 minutes PEDIATRIC: Magnesium Sulfate 40 mg/kg IV/IO over 15 minutes. Maximum dose: 2,000 mg (2 g)
- p.124 row 8 [Stridor #0] badge `A` — Administer: ADULT: Epinephrine 3 mg [1 mg/mL] nebulized PEDIATRIC: Epinephrine 3 mg [1 mg/mL] nebulized May repeat once, if needed.
- p.124 row 10 [Bronchiolitis #0] badge `A` — Provide suctioning as needed and consider: PEDIATRIC: 0.9% Sodium Chloride, 6 mL nebulized. Repeat as needed for increased work of breathing due to secretions.

## `protocols/respiratory/03_Respiratory_Arrest_PROC.md` — 2 missing (PEMS p.239)
- p.239 row 1 [base section #1] badge `EMR` — Refer to appropriate protocol (e.g. Respiratory Distress) for condition specific therapy guidelines.
- p.239 row 4 [CONSCIOUS PATIENT #1] badge `EMT` — Provide / titrate supplemental oxygen via NC or NRB to maintain SpO 94 – 98%. 2 Use EtCO2 monitor to guide therapy. Refer to Capnography procedure.

## `protocols/respiratory/03_Respiratory_Distress_PROC.md` — 4 missing (PEMS p.123, p.124)
- p.123 row 4 [base section #4] badge `I` — Consider invasive ventilatory support via endotracheal intubation. Refer to Endotracheal Intubation procedure. Note: Intubation of spontaneously breathing patients without rapid sequence induction (RSI) is generally not recommended. RSI is not addressed in PEMS regional protocols – refer to agency specific protocols for guidance.
- p.123 row 5 [Asthma, COPD, Reactive Airway Disease #0] badge `EMT` — Administer: ADULT: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Repeat as necessary. ADULT: Ipratropium Bromide 3 mL of 0.02% solution, nebulized. Once. PEDIATRIC: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Repeat as necessary. PEDIATRIC: Ipratropium Bromide 3 mL of 0.02% solution, nebulized. Once.
- p.124 row 12 [Pulmonary Edema #1] badge `I` — Administer: ADULT: Furosemide (Lasix) 40 mg IV/IO slow push
- p.124 row 13 [Pulmonary Edema #2] badge `MC` — Contact Medical Control for guidance as needed.

## `protocols/respiratory/03_Smoke_Inhalation_PROC.md` — 10 missing (PEMS p.153, p.239)
- p.153 row 1 [base section #1] badge `EMT` — Consider gross decontamination.
- p.153 row 3 [base section #3] badge `A` — Administer: ADULT: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Repeat as necessary.
- p.153 row 4 [base section #4] badge `A` — PEDIATRIC: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Repeat as necessary. Administer: ADULT: Methylprednisolone (Solu-Medrol) 125 mg IV/IO slow push. PEDIATRIC: Methylprednisolone (Solu-Medrol) 2 mg/kg IV/IO slow push. Maximum dose: 125 mg For suspected Chlorine gas exposure, consider: ADULT: Sodium bicarbonate 2 mL diluted with 2 mL 0.9% Sodium chloride, nebulized. Once. PEDIATRIC: Sodium bicarbonate 2 mL diluted with 2 mL 0.9% Sodium chloride, nebulized. Once.
- p.239 row 1 [base section #7] badge `EMR` — Refer to appropriate protocol (e.g. Respiratory Distress) for condition specific therapy guidelines.
- p.239 row 3 [CONSCIOUS PATIENT #0] badge `EMT` — Foreign body airway obstruction: * ADULT: Perform Heimlich abdominal thrusts. OBESE / PREGNANT: Perform chest thrusts. PEDIATRIC ≥ 1 year: Perform Heimlich abdominal thrusts. PEDIATRIC < 1 year: Alternate 5 back blows/chest thrusts until obstruction clears
- p.239 row 4 [CONSCIOUS PATIENT #1] badge `EMT` — Provide / titrate supplemental oxygen via NC or NRB to maintain SpO 94 – 98%. 2 Use EtCO2 monitor to guide therapy. Refer to Capnography procedure.
- p.239 row 5 [CONSCIOUS PATIENT #2] badge `EMT` — Consider CPAP (PEEP: 5 cmH2O) for respiratory distress. Refer to CPAP procedure. I/P only: Adjust PEEP to support ventilation and work of breathing, up to 10 cmH O.** 2
- p.239 row 6 [UNCONSCIOUS / OBTUNDED PATIENT #0] badge `EMT` — Position the patient and open the airway. Use BLS airway adjuncts (OPA/NPA/SGA) as necessary.
- p.239 row 7 [UNCONSCIOUS / OBTUNDED PATIENT #1] badge `EMT` — Support respirations with BVM. Use in-line EtCO2. Refer to Capnography procedure. Adjust tidal volume, respiratory rate, and/or PEEP (if available) to maintain EtCO 35 – 45mmHg.** 2
- p.239 row 8 [UNCONSCIOUS / OBTUNDED PATIENT #2] badge `I` — Foreign body airway obstruction: If unable to ventilate, perform laryngoscopy. Remove with forceps.

## `protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md` — 4 missing (PEMS p.239)
- p.239 row 1 [base section #1] badge `EMR` — Refer to appropriate protocol (e.g. Respiratory Distress) for condition specific therapy guidelines.
- p.239 row 4 [CONSCIOUS PATIENT #1] badge `EMT` — Provide / titrate supplemental oxygen via NC or NRB to maintain SpO 94 – 98%. 2 Use EtCO2 monitor to guide therapy. Refer to Capnography procedure.
- p.239 row 5 [CONSCIOUS PATIENT #2] badge `EMT` — Consider CPAP (PEEP: 5 cmH2O) for respiratory distress. Refer to CPAP procedure. I/P only: Adjust PEEP to support ventilation and work of breathing, up to 10 cmH O.** 2
- p.239 row 7 [UNCONSCIOUS / OBTUNDED PATIENT #1] badge `EMT` — Support respirations with BVM. Use in-line EtCO2. Refer to Capnography procedure. Adjust tidal volume, respiratory rate, and/or PEEP (if available) to maintain EtCO 35 – 45mmHg.** 2

## `protocols/toxicology/06_Overdose_Poisoning_PROC.md` — 3 missing (PEMS p.119, p.120, p.121)
- p.119 row 3 [base section #3] badge `EMR` — If seizing or a seizure has occurred, refer to Seizure protocol.
- p.121 row 12 [Cyanide #0] badge `I` — For altered mental status, seizures, hypotension, and/or cardiac arrest following exposure to combustion products in an enclosed space or suspected cyanide poisoning, administer (if available): ADULT: Hydroxocobalamin (CYANOKIT) 5 g IV/IO, infuse over 15 minutes PEDIATRIC: Hydroxocobalamin (CYANOKIT) 70 mg/kg IV/IO, infuse over 15 minutes To reconstitute for infusion: Add: 200mL of 0.9% Sodium Chloride to Hydroxocobalamin (CYANOKIT) vial using the transfer spike included in the kit. Fill to the line. Mix: Repeatedly invert or rock the vial for at least 60 seconds. Do not shake.
- p.121 row 13 [Cyanide #1] badge `MC` — Contact Medical Control for guidance as needed.

## `protocols/trauma/09_Burns_Thermal_PROC.md` — 3 missing (PEMS p.87, p.88)
- p.87 row 0 [base section #0] badge `EMR` — Follow Universal Patient Care / Initial Patient Contact protocol.
- p.87 row 6 [base section #6] badge `A` — For an adult patient with SBP less than 90 and TBSA greater than 20%, administer: ADULT: 0.9% Sodium chloride at 500 mL/hr IV/IO PEDIATRIC, 6 to 12 years old: 0.9% Sodium chloride at 250 mL/hr IV/IO PEDIATRIC, 5 years old and younger: 0.9% Sodium chloride at 125 mL/hr IV/IO
- p.88 row 8 [base section #8] badge `I` — For altered mental status, seizures, hypotension, and/or cardiac arrest following exposure to combustion products in an enclosed space or suspected cyanide poisoning, administer (if available): ADULT: Hydroxocobalamin (CYANOKIT) 5 g IV/IO, infuse over 15 minutes PEDIATRIC: Hydroxocobalamin (CYANOKIT) 70 mg/kg IV/IO, infuse over 15 minutes To reconstitute for infusion: Add: 200mL of 0.9% Sodium Chloride to Hydroxocobalamin (CYANOKIT) vial using the transfer spike included in the kit. Fill to the line. Mix: Repeatedly invert or rock the vial for at least 60 seconds. Do not shake.

## `protocols/trauma/09_Electrical_Injuries_PROC.md` — 1 missing (PEMS p.95, p.96)
- p.95 row 0 [base section #0] badge `I` — Consider endotracheal intubation vs immediate transport to the nearest emergency department if any signs of symptoms of airway injury develop: • Singed facial or nasal hairs • Burns or soot on the face, nose, or mouth • Hoarse voice or stridor • Carbonaceous sputum • Difficulty breathing / respiratory distress • Hypoxia • Tachypnea Follow Endotracheal Intubation procedure if proceeding with intubation. Note: Intubation of spontaneously breathing patients without rapid sequence induction (RSI) is generally not recommended. RSI is not addressed in regional protocols – refer to agency specific protocols for guidance. Note: Intubation of children under 12 years old is a Paramedic “red dot” skill only.

## `protocols/trauma/09_Lightning_Injuries_PROC.md` — 1 missing (PEMS p.95, p.96)
- p.96 row 11 [base section #11] badge `I` — Assess and continuously monitor cardiac rhythm.

## `protocols/trauma/09_Trauma_PROC.md` — 3 missing (PEMS p.83, p.84)
- p.83 row 4 [base section #4] badge `EMR` — Immobilize, secure in place, and do not remove any impaled object unless impeding CPR.
- p.83 row 5 [base section #5] badge `EMR` — Acutely deformed /dislocated extremities: • Assess distal perfusion. Contact Medical Control for direction if distal pulse is absent. • Splint or immobilize suspected long bone fractures. • Assess distal perfusion before and after splinting.
- p.83 row 6 [base section #6] badge `EMR` — Complete amputation of any part: • Wrap the amputated part in a dry, sterile dressing • Place the part in a dry, sealed plastic bag • Place the plastic bag with the part in an ice water filled container • Mark the container with date, patient name, and name of the part
