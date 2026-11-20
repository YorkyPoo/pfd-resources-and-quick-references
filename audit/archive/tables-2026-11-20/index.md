# Level tables as published on 2026-11-20

Snapshot taken from the `main` build (commit `d5fd03c`)
before the five-pip strip rollout. Each file holds that page's rendered
`lv-wrap` table markup **verbatim** — the chip table where every level
appears once per row. Filenames mirror the site path. Every page that
carries an `lv-wrap` table is here, including the 15 whose tables publish
no provider level (`policy` / `pending`) and are therefore not converted.

- pages snapshotted: **69**
- pages the rollout converts: **52**
- action rows over all snapshotted tables: **621**
- pages skipped (no provider level in any table): **17**

## To restore a page

Either set `extra.pip_strip.enabled: false` in `mkdocs.yml` and rebuild
(one-commit switch, restores every page), or paste the markup from the
page's file back into the page's markdown in place of the strip.

## Pages

| page | tables | rows | rollout | chips (row:chip) |
|---|---|---|---|---|
| `procedures/CPAP.html` | 1 | 6 | converted (1 of 1) | 1:EMT, 2:EMT, 3:EMT, 4:EMT, 5:EMT, 6:I |
| `procedures/Capnography.html` | 1 | 7 | converted (1 of 1) | 1:EMT, 2:EMT, 3:EMT, 4:EMT, 5:EMT, 6:EMT, 7:EMT |
| `procedures/Chest_Decompression.html` | 1 | 7 | converted (1 of 1) | 1:I, 2:I, 3:I, 4:I, 5:I, 6:I, 7:I |
| `procedures/Endotracheal_Intubation.html` | 1 | 12 | converted (1 of 1) | 0:EMR, 1:EMT, 2:EMT, 3:I, 4:I, 5:P, 6:I, 7:P, 8:I, 9:I, 10:I, 11:EMT |
| `procedures/Intraosseous_Access.html` | 1 | 8 | converted (1 of 1) | 1:A, 2:A, 3:A, 4:A, 5:A, 6:A, 7:A, 8:A |
| `procedures/Medication_Administration.html` | 1 | 6 | converted (1 of 1) | 1:EMT, 2:EMT, 3:A, 4:A, 5:EMT, 6:EMT |
| `procedures/Nasogastric_Tube.html` | 1 | 6 | converted (1 of 1) | 1:I, 2:I, 3:I, 4:I, 5:I, 6:I |
| `procedures/Neonatal_Resuscitation.html` | 1 | 6 | converted (1 of 1) | 1:EMR, 2:EMR, 3:I, 4:EMR, 5:A, 5a:I |
| `procedures/Spinal_Motion_Restriction.html` | 1 | 4 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR |
| `procedures/Surgical_Airway.html` | 1 | 5 | converted (1 of 1) | 1:P, 2:P, 3:P, 4:P, 5:MC |
| `procedures/Taser_Barb_Removal.html` | 1 | 6 | converted (1 of 1) | 1:EMT, 2:EMT, 3:EMT, 4:EMT, 5:EMT, 6:EMT |
| `procedures/Tourniquet_Application.html` | 1 | 6 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMR, 6:EMR |
| `procedures/Transcutaneous_Pacing.html` | 1 | 5 | converted (1 of 1) | 1:I, 2:I, 3:I, 4:I, 5:I |
| `protocols/administrative/01_ALS_Release_to_BLS_PROC.html` | 1 | 8 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:POLICY, 8:POLICY |
| `protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.html` | 1 | 7 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:POLICY |
| `protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.html` | 1 | 5 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY |
| `protocols/administrative/01_Communications_PROC.html` | 1 | 6 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY |
| `protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.html` | 1 | 5 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY |
| `protocols/administrative/01_Helicopter_EMS_HEMS_PROC.html` | 1 | 6 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY |
| `protocols/administrative/01_Infant_Abandonment_PROC.html` | 1 | 4 | skipped — policy table | 1:POLICY, 2:PENDING, 3:POLICY, 4:POLICY |
| `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.html` | 1 | 7 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:POLICY |
| `protocols/administrative/01_Patient_Restraint_PROC.html` | 1 | 8 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:POLICY, 8:POLICY |
| `protocols/administrative/01_STEMI_Field_Triage_PROC.html` | 1 | 7 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:MC |
| `protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.html` | 1 | 7 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:POLICY |
| `protocols/administrative/01_Stroke_Field_Triage_PROC.html` | 1 | 7 | skipped — policy table | 1:EMT, 2:POLICY, 3:POLICY, 5:POLICY, 6:POLICY, 7:POLICY, 8:POLICY |
| `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.html` | 1 | 7 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:POLICY |
| `protocols/administrative/01_Trauma_Field_Triage_PROC.html` | 1 | 8 | skipped — policy table | 1:POLICY, 2:POLICY, 3:POLICY, 4:POLICY, 5:POLICY, 6:POLICY, 7:POLICY, 8:POLICY |
| `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.html` | 1 | 14 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMT, 6:A, 7:EMT, 8:EMR, 8a:I †, 8b:I, 9:A, 10:I, 11:I, 12:MC |
| `protocols/cardiac/04_Bradycardia_PROC.html` | 1 | 8 | converted (1 of 1) | 1:EMR, 2:I, 3:I, 4:I, 5:I, 6:I *, 7:P, 8:MC |
| `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.html` | 1 | 16 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMT, 4:EMR, 4a:I †, 5:I, 5a:EMR, 6:EMT, 7:A, 8:A, 9:I, 10:A, 11:I, 12:EMR, 13:MC, 14:EMR |
| `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.html` | 1 | 12 | converted (1 of 1) | 1:EMR, 2:EMT, 3:EMT, 4:I, 5:EMT, 5a:I, 6:A, 7:A, 8:I, 9:I, 10:EMT, 11:MC |
| `protocols/cardiac/04_Chest_Pain_ACS_PROC.html` | 1 | 14 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMT, 5:I, 6:EMT, 7:MC, 8:A, 9:I, 10:EMT, 11:EMT, 12:I, 13:MC, 14:I +MC |
| `protocols/cardiac/04_Hypertensive_Crisis_PROC.html` | 1 | 7 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMR, 6:EMR, 7:MC |
| `protocols/cardiac/04_Post_Resuscitation_Care_PROC.html` | 1 | 8 | converted (1 of 1) | 1:EMR, 2:EMT, 3:EMT, 4:A, 5:A, 6:I, 7:I *, 8:P |
| `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.html` | 3 | 14 | converted (3 of 3) | 1:EMR, 2:EMR / 4:EMT, 5:A, 6:A, 7:I, 8:I, 9:I, 10:MC / 12:I, 13:I, 14:I, 15:I, 16:I |
| `protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.html` | 1 | 13 | converted (1 of 1) | 1:EMR, 2:EMT, 3:A, 4:A, 5:EMR, 5a:I, 6:A, 7:I, 8:I, 9:I, 10:I, 11:EMR, 12:MC |
| `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.html` | 1 | 11 | skipped — pending table | 1:PENDING, 2:PENDING, 3:PENDING, 4:PENDING, 5:PENDING, 6:PENDING, 7:PENDING, 8:PENDING, 9:PENDING, 10:PENDING, 11:PENDING |
| `protocols/front-matter/Universal Patient Care.html` | 1 | 11 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMT, 6:EMT, 7:EMT, 8:A, 9:I, 10:EMT, 11:EMR |
| `protocols/general/02_Behavioral_Patient_Restraint_PROC.html` | 1 | 8 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:I, 5:I, 6:I, 7:P, 8:MC |
| `protocols/general/02_Cold_Exposure_PROC.html` | 1 | 7 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMR, 7:EMR, 8:EMT |
| `protocols/general/02_Diving_and_Drowning_Emergencies_PROC.html` | 1 | 7 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMR, 6:EMR, 7:MC |
| `protocols/general/02_Heat_Exposure_PROC.html` | 1 | 7 | converted (1 of 1) | 1:EMR, 2:EMT, 3:EMT, 4:EMT, 5:EMT, 6:A, 7:EMT |
| `protocols/general/02_Pain_Control_PROC.html` | 1 | 8 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMT, 4:A, 5:A, 6:A *, 7:A *, 8:MC |
| `protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.html` | 1 | 7 | converted (1 of 1) | 1:EMR, 2:EMT, 3:I, 4:I, 5:I, 6:I, 7:MC |
| `protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.html` | 3 | 13 | converted (3 of 3) | 1:EMR, 2:EMT / 3:A, 4:A, 5:A, 6:A / 7:EMT, 8:A, 9:A, 10:A, 11:A, 12:A, 13:A |
| `protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.html` | 1 | 10 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMT, 5:A, 6:I, 7:I, 8:I *, 9:P, 10:MC |
| `protocols/medical/07_OB_Emergencies_PROC.html` | 1 | 10 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMR, 6:I, 7:I, 8:EMR, 9:A, 10:MC |
| `protocols/medical/07_Sepsis_PROC.html` | 1 | 6 | converted (1 of 1) | 1:EMR, 2:A, 3:I, 4:I *, 5:P, 6:MC |
| `protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.html` | 1 | 5 | converted (1 of 1) | 1:EMR, 2:EMT, 3:A, 4:A, 5:A |
| `protocols/neurologic/05_Seizure_PROC.html` | 1 | 7 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMT, 4:EMR, 5:A *, 6:A *, 7:MC |
| `protocols/neurologic/05_Stroke_TIA_PROC.html` | 1 | 9 | skipped — PENDING row in the table | 1:EMR, 2:EMR, 3:EMR, 4:EMT, 5:EMT, 6:EMT, 7:EMT, 8:PENDING, 9:PENDING |
| `protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.html` | 1 | 13 | converted (1 of 1) | 1:EMR, 2:EMT, 3:EMT, 4:EMT, 5:EMT, 6:A, 7:A, 8:A, 9:I, 10:I, 10a:P, 11:EMR, 12:MC |
| `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.html` | 1 | 13 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMT, 4:EMT, 5:A, 6:I, 7:EMT, 8:EMT, 8a:I, 9:A, 10:A, 11:EMR, 11a:EMT |
| `protocols/respiratory/03_Pediatric_Stridor_PROC.html` | 1 | 12 | converted (1 of 1) | 1:EMR, 3:EMR, 4:EMR, 5:EMT, 5a:I, 6:EMT, 7:EMT, 8:A, 9:A, 10:A, 11:P +MC, 12:EMT |
| `protocols/respiratory/03_Pneumothorax_PROC.html` | 1 | 20 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMT, 4:EMR, 4a:A, 4b:I, 6:I, 7:I, 8:I, 9:I, 10:I, 11:I, 12:A, 12a:I, 13:I, 13a:P, 13b:P, 14:EMT, 15:EMR, 15a:I |
| `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.html` | 1 | 10 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMT, 5:EMT, 9:I, 10:A, 11:A, 12:I, 13:MC |
| `protocols/respiratory/03_Respiratory_Arrest_PROC.html` | 1 | 15 | converted (1 of 1) | 1:EMR, 2:EMT, 3:EMT, 4:EMT, 5:EMR, 6:EMT, 7:EMT, 8:I, 9:P, 10:I, 11:P, 12:I, 13:EMT, 14:I, 15:I |
| `protocols/respiratory/03_Respiratory_Distress_PROC.html` | 1 | 20 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMT, 3a:I, 4:EMR, 5:EMR, 6:EMT, 6a:I, 7:EMT, 8:I, 9:A, 10:A, 11:A, 12:A, 13:A, 14:I, 15:EMT, 16:EMT, 16a:I, 16b:P |
| `protocols/respiratory/03_Smoke_Inhalation_PROC.html` | 1 | 16 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMT, 4:EMT, 5:I, 6:I +MC, 7:I +MC, 8:I, 9:I +MC, 10:EMT, 11:A, 12:MC, 13:EMR, 13a:EMT, 13b:I, 14:EMT |
| `protocols/respiratory/03_Upper_Airway_Obstruction_PROC.html` | 1 | 13 | converted (1 of 1) | 1:EMR, 3:EMT, 4:EMT, 5:EMT, 6:EMT, 7:EMT, 8:EMT, 9:EMR, 10:EMT, 11:I, 12:I, 13:I +MC, 14:P |
| `protocols/toxicology/06_Nausea_Vomiting_PROC.html` | 1 | 6 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMT, 5:A, 6:MC |
| `protocols/toxicology/06_Nerve_Agents_PROC.html` | 1 | 7 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMT, 6:I, 7:MC |
| `protocols/toxicology/06_Overdose_Poisoning_PROC.html` | 1 | 10 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMT, 5:EMT, 6:A, 7:I, 8:I, 9:EMR, 10:I |
| `protocols/trauma/09_Burns_Thermal_PROC.html` | 1 | 7 | skipped — PENDING row in the table | 1:EMR, 2:EMR, 3:EMT, 4:EMT, 5:A, 6:PENDING, 7:MC |
| `protocols/trauma/09_Crush_Syndrome_PROC.html` | 1 | 9 | converted (1 of 1) | 1:EMR, 2:EMT, 3:A, 4:A +MC *, 5:I +MC *, 6:I *, 7:I, 8:EMT, 9:MC |
| `protocols/trauma/09_Electrical_Injuries_PROC.html` | 1 | 10 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMT, 6:EMT, 7:EMT, 7a:I, 8:A, 9:A |
| `protocols/trauma/09_Hemorrhage_Control_PROC.html` | 1 | 9 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMR, 6:EMR, 7:EMR, 8:EMR, 9:MC |
| `protocols/trauma/09_Lightning_Injuries_PROC.html` | 1 | 10 | converted (1 of 1) | 1:EMR, 2:EMR, 3:EMR, 4:EMR, 5:EMT, 6:EMT, 7:EMT, 7a:I, 8:A, 9:A |
| `protocols/trauma/09_Trauma_PROC.html` | 1 | 13 | converted (1 of 1) | 1:EMR, 2:EMR, 2a:EMT, 3:EMR, 4:EMT, 5:EMR, 7:A, 8:A, 9:I, 10:I, 11:I, 12:EMT, 13:MC |

## Skipped — no provider level, not touched by the rollout

- `protocols/administrative/01_ALS_Release_to_BLS_PROC.html` — policy table
- `protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.html` — policy table
- `protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.html` — policy table
- `protocols/administrative/01_Communications_PROC.html` — policy table
- `protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.html` — policy table
- `protocols/administrative/01_Helicopter_EMS_HEMS_PROC.html` — policy table
- `protocols/administrative/01_Infant_Abandonment_PROC.html` — policy table
- `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.html` — policy table
- `protocols/administrative/01_Patient_Restraint_PROC.html` — policy table
- `protocols/administrative/01_STEMI_Field_Triage_PROC.html` — policy table
- `protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.html` — policy table
- `protocols/administrative/01_Stroke_Field_Triage_PROC.html` — policy table
- `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.html` — policy table
- `protocols/administrative/01_Trauma_Field_Triage_PROC.html` — policy table
- `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.html` — pending table
- `protocols/neurologic/05_Stroke_TIA_PROC.html` — PENDING row in the table
- `protocols/trauma/09_Burns_Thermal_PROC.html` — PENDING row in the table
