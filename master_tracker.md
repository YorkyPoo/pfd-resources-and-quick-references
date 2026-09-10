# PEMS Protocol Audit Tracker

> Use this tracker with Hermes Agent + qwen3.6:27b to verify accuracy of every converted protocol.

## Status Codes
- `PENDING` â€” Not yet audited
- `VERIFIED` â€” Matches PEMS source, no discrepancies
- `FIXABLE` â€” Minor discrepancies found, auto-fixable
- `MANUAL` â€” Significant discrepancies requiring human review

---

## Administrative Policies

| # | Protocol | PEMS Chunk | Converted File | Status | Discrepancies | Notes |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | Abuse Recognition | pems_chunks/Abuse_Recognition.txt | docs/protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.md | MANUAL | 1 | Re-structure as administrative policy; missing detail. |
| 2 | ALS Release to BLS | pems_chunks/ALS_Release_to_BLS.txt | docs/protocols/administrative/01_ALS_Release_to_BLS_PROC.md | FIXED | 0 | Governance language updated to Officer/Acting Officer review. | 2 | Terminology replacement in committee name; formatting. |
| 3 | Behavioral Health Transport | pems_chunks/Behavioral_Health_Transportation.txt | docs/protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md | MANUAL | 1 | Significant addition of non-PEMS procedural material. |
| 4 | Communications | pems_chunks/Communications.txt | docs/protocols/administrative/01_Communications_PROC.md | FIXED | 0 | Regional Resources & Telephone Numbers section added. | 1 | Missing regional resources and contact list. |
| 5 | Death Criteria | pems_chunks/Death_Criteria.txt | docs/protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md | FIXED | 0 | Facility-specific DNR instructions added. | 2 | Missing detailed facility-specific DNR instructions. |
| 6 | Helicopter EMS | pems_chunks/Helicopter_EMS.txt | docs/protocols/administrative/01_Helicopter_EMS_HEMS_PROC.md | VERIFIED | 0 | None. |
| 7 | Infant Abandonment | pems_chunks/Infant_Abandonment.txt | docs/protocols/administrative/01_Infant_Abandonment_PROC.md | VERIFIED | 0 | None. |
| 8 | Patient Refusal | pems_chunks/Patient_Refusal.txt | docs/protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md | VERIFIED | 0 | None. |
| 9 | Patient Restraint | pems_chunks/Patient_Restraint.txt | docs/protocols/administrative/01_Patient_Restraint_PROC.md | VERIFIED | 0 | None. |
| 10 | Transport of Pediatric | pems_chunks/Safe_Transport_of_Pediatric.txt | docs/protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.md | VERIFIED | 0 | None. |
| 11 | STEMI Field Triage | pems_chunks/STEMI_Field_Triage.txt | docs/protocols/administrative/01_STEMI_Field_Triage_PROC.md | FIXED | 0 | Complete PCI hospital list with surgical capability added. | 1 | Missing list of specific regional PCI hospitals. |
| 12 | Stroke Field Triage | pems_chunks/Stroke_Field_Triage.txt | docs/protocols/administrative/01_Stroke_Field_Triage_PROC.md | VERIFIED | 0 | None. |
| 13 | Transport & Destination | PEMS2024_full.txt | docs/protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md | VERIFIED | 0 | None. |
| 14 | Trauma Field Triage | pems_chunks/Trauma_Field_Triage.txt | docs/protocols/administrative/01_Trauma_Field_Triage_PROC.md | VERIFIED | 0 | None. |

## General

| # | Protocol | PEMS Chunk | Converted File | Status |
| :---: | :--- | :--- | :--- | :--- |
| 15 | Behavioral Pt Restraint | PEMS2024_full.txt | docs/protocols/general/02_Behavioral_Patient_Restraint_PROC.md | MANUAL | 1 | Extensive addition of chemical restraint dosages. |
| 16 | Cold Exposure | pems_chunks/Cold_Exposure.txt | docs/protocols/general/02_Cold_Exposure_PROC.md | FIXED | 0 | Transport authority corrected for all provider levels. | 1 | Incorrectly restricted transport authority in table. |
| 17 | Diving & Drowning | PEMS2024_full.txt | docs/protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md | VERIFIED | 0 | None. |
| 18 | Heat Exposure | pems_chunks/Heat_Exposure.txt | docs/protocols/general/02_Heat_Exposure_PROC.md | VERIFIED | 0 | None. |
| 19 | Pain Control | pems_chunks/Pain_Control.txt | docs/protocols/general/02_Pain_Control_PROC.md | VERIFIED | 0 | None. |
| 20 | Sedation | pems_chunks/Sedation.txt | docs/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md | VERIFIED | 0 | None. |

## Respiratory

|  #  | Protocol                 | PEMS Chunk                               | Converted File                                                    |  Status  | Discrepancies | Notes |
| :-: | :----------------------- | :--------------------------------------- | :---------------------------------------------------------------- | :------: | :---: | ------------------------------------------------------- |
| 21  | Airway Inhalation        | PEMS2024_full.txt                        | docs/protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md | VERIFIED | 0   | None.                                                   |
| 22  | Asthma/COPD              | pems_chunks/Asthma.txt                   | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | FIXABLE  | 1   | Verify Pediatric MgSO4 dosage against OMD orders.       |
| 23  | Pediatric Stridor        | PEMS2024_full.txt                        | docs/protocols/respiratory/03_Pediatric_Stridor_PROC.md           | VERIFIED | 0   | None.                                                   |
| 24  | Pneumothorax             | pems_chunks/Pneumothorax.txt             | docs/protocols/respiratory/03_Pneumothorax_PROC.md                | VERIFIED | 0   | None.                                                   |
| 25  | Pulmonary Edema          | pems_chunks/Pulmonary_Edema.txt          | docs/protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md  | VERIFIED | 0   | None.                                                   |
| 26  | Respiratory Arrest       | pems_chunks/Respiratory_Arrest.txt       | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md          | VERIFIED | 0   | None.                                                   |
| 27  | Respiratory Distress     | pems_chunks/Respiratory_Distress.txt     | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md        | VERIFIED | 0   | None.                                                   |
| 28  | Smoke Inhalation         | PEMS2024_full.txt                        | docs/protocols/respiratory/03_Smoke_Inhalation_PROC.md            | VERIFIED | 0   | None.                                                   |
| 29  | Upper Airway Obstruction | pems_chunks/Upper_Airway_Obstruction.txt | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md    | VERIFIED | 0   | None.                                                   |

## Cardiac

| # | Protocol | PEMS Chunk | Converted File | Status | Discrepancies | Notes |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 30 | Aortic Dissection | pems_chunks/Aortic_Dissection.txt | docs/protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md | CREATED | - | Created from ODEMSA source 2025-06-11. |
| 31 | Asystole/PEA | pems_chunks/Asystole.txt | docs/protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md | VERIFIED | 0 | None. |
| 32 | Bradycardia | pems_chunks/Bradycardia.txt | docs/protocols/cardiac/04_Bradycardia_PROC.md | VERIFIED | 0 | None. |
| 33 | Cardiac Arrest Non-Trauma | pems_chunks/Cardiac_Arrest.txt | docs/protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md | VERIFIED | 0 | None. |
| 34 | Cardiac Arrest Traumatic | PEMS2024_full.txt | docs/protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md | VERIFIED | 0 | None. |
| 35 | Chest Pain/ACS | pems_chunks/Chest_Pain.txt | docs/protocols/cardiac/04_Chest_Pain_ACS_PROC.md | VERIFIED | 0 | None. |
| 36 | Hypertensive Crisis | PEMS2024_full.txt | docs/protocols/cardiac/04_Hypertensive_Crisis_PROC.md | VERIFIED | 0 | None. |
| 37 | Post-Resuscitation Care | PEMS2024_full.txt | docs/protocols/cardiac/04_Post_Resuscitation_Care_PROC.md | VERIFIED | 0 | None. |
| 38 | SVT | pems_chunks/Supraventricular_Tachycardia.txt | docs/protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md | VERIFIED | 0 | None. |
| 39 | V-Fib/V-Tach | pems_chunks/V-Fib.txt | docs/protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md | VERIFIED | 0 | None. |

## Neurologic

| # | Protocol | PEMS Chunk | Converted File | Status | Discrepancies | Notes |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 40 | Hypoglycemia | pems_chunks/Hypoglycemia.txt | docs/protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.md | VERIFIED | 0 | None. |
| 41 | Seizure | pems_chunks/Seizure.txt | docs/protocols/neurologic/05_Seizure_PROC.md | VERIFIED | 0 | None. |
| 42 | Stroke/TIA | pems_chunks/Stroke.txt | docs/protocols/neurologic/05_Stroke_TIA_PROC.md | VERIFIED | 0 | None. |

## Toxicology

| # | Protocol | PEMS Chunk | Converted File | Status | Discrepancies | Notes |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 43 | Nausea/Vomiting | pems_chunks/Nausea.txt | docs/protocols/toxicology/06_Nausea_Vomiting_PROC.md | VERIFIED | 0 | None. |
| 44 | Nerve Agents | pems_chunks/Nerve_Agents.txt | docs/protocols/toxicology/06_Nerve_Agents_PROC.md | VERIFIED | 0 | None. |
| 45 | Overdose/Poisoning | pems_chunks/Overdose.txt | docs/protocols/toxicology/06_Overdose_Poisoning_PROC.md | VERIFIED | 0 | None. |

## Medical

|  #  | Protocol          | PEMS Chunk                        | Converted File                                                  |  Status  | Discrepancies | Notes |
| :-: | :---------------- | :-------------------------------- | :-------------------------------------------------------------- | :------: | :---: | ------------------------------------------ |
| 46  | Allergic Reaction | pems_chunks/Allergic_Reaction.txt | docs/protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md | VERIFIED | 0   | None.                                      |
| 47  | Hypotension/Shock | pems_chunks/Hypotension.txt       | docs/protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md  | VERIFIED | 0   | None.                                      |
| 48  | OB Emergencies    | PEMS2024_full.txt                 | docs/protocols/medical/07_OB_Emergencies_PROC.md                | FIXABLE  | 1   | Combined multiple PEMS protocols into one. |
| 49  | Sepsis            | pems_chunks/Sepsis.txt            | docs/protocols/medical/07_Sepsis_PROC.md                        | VERIFIED | 0   | None.                                      |

## Trauma

| # | Protocol | PEMS Chunk | Converted File | Status | Discrepancies | Notes |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 50 | Burns Thermal | pems_chunks/Burns.txt | docs/protocols/trauma/09_Burns_Thermal_PROC.md | VERIFIED | 0 | None. |
| 51 | Crush Syndrome | pems_chunks/Crush_Syndrome.txt | docs/protocols/trauma/09_Crush_Syndrome_PROC.md | VERIFIED | 0 | None. |
| 52 | Electrical Injuries | pems_chunks/Electrical_Injuries.txt | docs/protocols/trauma/09_Electrical_Injuries_PROC.md | VERIFIED | 0 | None. |
| 53 | Hemorrhage Control | pems_chunks/Hemorrhage_Control.txt | docs/protocols/trauma/09_Hemorrhage_Control_PROC.md | VERIFIED | 0 | None. |
| 54 | Lightning Injuries | PEMS2024_full.txt | docs/protocols/trauma/09_Lightning_Injuries_PROC.md | VERIFIED | 0 | None. |
| 55 | Trauma | pems_chunks/Trauma.txt | docs/protocols/trauma/09_Trauma_PROC.md | VERIFIED | 0 | None. |

---

**Total: 55 protocols** | **Audited: 55** | **Verified: 44** | **Missing: 0** | **FIXABLE: 0** | **MANUAL: 3** | **CREATED: 1**
