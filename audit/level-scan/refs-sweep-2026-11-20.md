# Refs sweep — 2026-11-20 (card t_07d23947)

Owner standing rule: guidance that is published as a numbered action row is relocated to
that page's **References & Good Practice** block, never escalated. This file is the record
of the sweep that applied it to every published page.

## Method

- Every page under `docs/protocols/**` (59) and `docs/procedures/*.md` (16) was read at the
  level-table level; the row count below is counted from the rendered markdown, not from
  the ledger, so a row the ledger never saw would still appear here.
- Each row's chip was classified from `level-rule-ledger.json`: `OK` / `owner_ruled` /
  `policy` rows carry a PEMS-printed badge or a recorded ruling (a real level — relocating
  them would drop it); `OWNER_REQUIRED` rows are actions awaiting a level decision;
  `pending_omd` / `pending_row_omd` rows have no printed badge at all and were each read by
  hand and judged action vs. guidance.

## Pages checked

| page | table rows | chipped PEMS badge | policy | owner_ruled | OWNER_REQUIRED | PENDING | relocated |
|---|---:|---:|---:|---:|---:|---:|---:|
| `procedures/CPAP.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Capnography.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Chest_Decompression.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Endotracheal_Intubation.md` | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Intraosseous_Access.md` | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Medical_Devices_Pumps.md` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Medication_Administration.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Nasogastric_Tube.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Neonatal_Resuscitation.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Spinal_Motion_Restriction.md` | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Surgical_Airway.md` | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Taser_Barb_Removal.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Tourniquet_Application.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Transcutaneous_Pacing.md` | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| `procedures/Vaccination.md` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_ALS_Release_to_BLS_PROC.md` | 8 | 0 | 8 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.md` | 7 | 0 | 7 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md` | 5 | 0 | 5 | 0 | 0 | 0 | 2 |
| `protocols/administrative/01_Communications_PROC.md` | 6 | 0 | 6 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md` | 5 | 0 | 5 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Helicopter_EMS_HEMS_PROC.md` | 6 | 0 | 6 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Infant_Abandonment_PROC.md` | 4 | 0 | 3 | 0 | 0 | 1 | 0 |
| `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` | 7 | 0 | 7 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Patient_Restraint_PROC.md` | 8 | 0 | 8 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_STEMI_Field_Triage_PROC.md` | 7 | 1 | 6 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.md` | 7 | 0 | 7 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Stroke_Field_Triage_PROC.md` | 7 | 1 | 6 | 0 | 0 | 0 | 1 |
| `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md` | 7 | 0 | 7 | 0 | 0 | 0 | 0 |
| `protocols/administrative/01_Trauma_Field_Triage_PROC.md` | 8 | 0 | 8 | 0 | 0 | 0 | 0 |
| `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | 14 | 13 | 0 | 0 | 1 | 0 | 0 |
| `protocols/cardiac/04_Bradycardia_PROC.md` | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md` | 16 | 15 | 0 | 0 | 1 | 0 | 0 |
| `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md` | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` | 14 | 12 | 0 | 2 | 0 | 0 | 0 |
| `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `protocols/cardiac/04_Post_Resuscitation_Care_PROC.md` | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md` | 14 | 13 | 0 | 1 | 0 | 0 | 0 |
| `protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md` | 13 | 13 | 0 | 0 | 0 | 0 | 0 |
| `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md` | 11 | 0 | 0 | 0 | 0 | 11 | 0 |
| `protocols/front-matter/00 - AI Formatting Guidelines.md` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `protocols/front-matter/00 - Introduction.md` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `protocols/front-matter/01 - How to Read the Protocols.md` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `protocols/front-matter/Universal Patient Care.md` | 11 | 11 | 0 | 0 | 0 | 0 | 0 |
| `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| `protocols/general/02_Cold_Exposure_PROC.md` | 7 | 7 | 0 | 0 | 0 | 0 | 2 |
| `protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `protocols/general/02_Heat_Exposure_PROC.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `protocols/general/02_Pain_Control_PROC.md` | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| `protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md` | 13 | 13 | 0 | 0 | 0 | 0 | 0 |
| `protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md` | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| `protocols/medical/07_OB_Emergencies_PROC.md` | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| `protocols/medical/07_Sepsis_PROC.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.md` | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| `protocols/neurologic/05_Seizure_PROC.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `protocols/neurologic/05_Stroke_TIA_PROC.md` | 9 | 7 | 0 | 0 | 0 | 2 | 0 |
| `protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md` | 13 | 11 | 0 | 2 | 0 | 0 | 0 |
| `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` | 13 | 12 | 0 | 0 | 1 | 0 | 0 |
| `protocols/respiratory/03_Pediatric_Stridor_PROC.md` | 12 | 12 | 0 | 0 | 0 | 0 | 1 |
| `protocols/respiratory/03_Pneumothorax_PROC.md` | 20 | 20 | 0 | 0 | 0 | 0 | 1 |
| `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` | 10 | 9 | 0 | 0 | 1 | 0 | 3 |
| `protocols/respiratory/03_Respiratory_Arrest_PROC.md` | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| `protocols/respiratory/03_Respiratory_Distress_PROC.md` | 19 | 19 | 0 | 0 | 0 | 0 | 0 |
| `protocols/respiratory/03_Smoke_Inhalation_PROC.md` | 16 | 15 | 0 | 1 | 0 | 0 | 0 |
| `protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md` | 13 | 13 | 0 | 0 | 0 | 0 | 1 |
| `protocols/toxicology/06_Nausea_Vomiting_PROC.md` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| `protocols/toxicology/06_Nerve_Agents_PROC.md` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| `protocols/toxicology/06_Overdose_Poisoning_PROC.md` | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| `protocols/trauma/09_Burns_Thermal_PROC.md` | 7 | 6 | 0 | 0 | 0 | 1 | 0 |
| `protocols/trauma/09_Crush_Syndrome_PROC.md` | 9 | 9 | 0 | 0 | 0 | 0 | 0 |
| `protocols/trauma/09_Electrical_Injuries_PROC.md` | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| `protocols/trauma/09_Hemorrhage_Control_PROC.md` | 9 | 9 | 0 | 0 | 0 | 0 | 0 |
| `protocols/trauma/09_Lightning_Injuries_PROC.md` | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| `protocols/trauma/09_Trauma_PROC.md` | 13 | 13 | 0 | 0 | 0 | 0 | 1 |
| **total (74 pages)** | **620** | **506** | **89** | **6** | **4** | **15** | **12** |


## Every unbadged row, and what was done with it

A row with no PEMS-printed badge is the only kind the standing rule can move: a chipped row
carries a level, and relocating it would drop that level. Rows below are grouped by status.

| page | row | level now | what it says | disposition |
|---|---|---|---|---|
| `04_Supraventricular_Tachycardia_PROC.md` | 2 | EMR | Assess patient stability (chest pain, dyspnea, AMS, shock) | kept — prose-shaped but the owner set its level by ruling (EMR); relocating it would drop a level the owner decided — kept, boundary of the standing rule |
| `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | 8a | I | Interpret the rhythm: VF or VT (shockable), or asystole or PEA (non-shockable). | kept — action — rhythm interpretation is a provider skill; OWNER_REQUIRED because PEMS badges the AED row EMR and scopes the classification to I in the same sentence |
| `04_Cardiac_Arrest_Non_Traumatic_PROC.md` | 4a | I | • Interpret the rhythm: V-Fib/V-Tach (shockable) or Asystole/PEA (non-shockable). | kept — action — same shape as Asystole 8a |
| `04_Chest_Pain_ACS_PROC.md` | 5 | I | 12-Lead ECG Interpretation - STEMI Criteria: • Intermediate and Paramedic providers may interpret as STEMI if:   - Symptoms consistent with ACS/myocar | kept — owner_ruled I — 12-lead interpretation; keeping the level is the point of the ruling |
| `04_Chest_Pain_ACS_PROC.md` | 14 | I | Right-Sided / 15-Lead ECG: • Consider right-sided 12-Lead or 15-Lead ECG for additional assessment. | kept — owner_ruled I — "consider right-sided/15-lead"; would be a relocation candidate if it had no level, but the owner ruled I and the standing rule forbids dropping a level |
| `05_Stroke_TIA_PROC.md` | 8 | PENDING | Establish 18g IV in Right AC (preferred for rapid imaging) | kept — action — establishes IV access; agency addition awaiting the OMD's level, not prose |
| `05_Stroke_TIA_PROC.md` | 9 | PENDING | Call COR at the receiving facility with Name/DOB for rapid registration | kept — action — a call to the receiving facility; agency addition awaiting the OMD's level |
| `03_Airway_Inhalation_Irritants_PROC.md` | 3 | EMT | Airway Assessment: • Assess for signs of airway injury (singed hairs, facial burns, hoarseness, stridor, soot). • Monitor for progressive respiratory  | kept — owner_ruled EMT — airway assessment; level set by the owner's Pearl ruling |
| `03_Airway_Inhalation_Irritants_PROC.md` | 11 | EMR | Poison Control Consultation: • Contact Poison Control Center at 1-800-222-1222 with any questions. (Note: Poison Control is not online medical control | kept — owner_ruled EMR — Poison Control referral; level set by the owner's Pearl ruling |
| `03_Asthma_COPD_Reactive_Airway_PROC.md` | 8a | I | • Titrate PEEP up to 10 cm H₂O to support ventilation and work of breathing. | kept — action — PEEP titration above 5 cmH2O; OWNER_REQUIRED because the printed rows disagree |
| `03_Pulmonary_Edema_Congestion_PROC.md` | 9 | P | CPAP Titration: Adjust PEEP up to 10 cmH2O to support ventilation and work of breathing | kept — action — PEEP titration; owner ruled 2026-11-20 that an Intermediate may titrate |
| `03_Smoke_Inhalation_PROC.md` | 3 | EMT | Airway Assessment: • Inspect for singed facial/nasal hairs • Examine face, nose, and mouth for burns or soot • Auscultate for stridor, hoarseness, or  | kept — owner_ruled EMT — airway assessment; level set by the owner's Pearl ruling |
| `09_Burns_Thermal_PROC.md` | 6 | PENDING | Hydrofluoric Acid (HF) Burns with Hypotension: Administer Calcium Chloride 1 g IV/IO over 3 mins (Repeat in 5 mins PRN). | kept — action — a drug dose (HF burns); PEMS prints it in prose only, so it has no printed level and stays PENDING for the OMD (relocating it would delete a treatment) |
| `01_Infant_Abandonment_PROC.md` | 2 | PENDING | Assess infant and provide medical care per these Protocols | kept — action — the care step in an ordered receive/assess/report/transport sequence; it directs treatment, so it is not guidance |
| `04b_Aortic_Dissection_AAA_PROC.md` | 1 | PENDING | Scene Safety / Initial Assessment: • Follow the Universal Patient Care / Initial Patient Contact protocol. • Perform general patient management. | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 2 | PENDING | Airway / Respiratory Management: • Support life-threatening problems associated with airway, breathing, and circulation. • If respiratory distress, re | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 3 | PENDING | Oxygen Administration: • Administer oxygen to maintain SpO2 94-99%. | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 4 | PENDING | Vital Signs / 12-Lead ECG: • Obtain VS in both arms and assess distal pulses. • Place patient on monitor and obtain (BLS) / interpret (ALS) 12-lead EC | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 5 | PENDING | Glucose Assessment: • Check blood glucose level. • Refer to the Hyperglycemia / Hypoglycemia protocol if indicated. | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 6 | PENDING | IV/IO Access: • Establish two IV of normal saline and titrate to a systolic B/P > 90 mmHg. • Do not delay transport to establish second IV. • Refer to | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 7 | PENDING | Pain Management: • Administer Fentanyl 1 mcg/kg IN/IV/IM or Morphine Sulfate 2.5-5.0 mg IV/IM as needed, per the Pain Control protocol. • Confirm all  | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 8 | PENDING | Nausea Management: • Administer Ondansetron (Zofran) 0.1 mg/kg slow IVP as needed per the Nausea and Vomiting protocol. | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 9 | PENDING | Hypotension Management - Vasopressors: • Consider Norepinephrine (Levophed) Infusion 0.1-0.5 mcg/kg/minute for hypotension. • Titrate to systolic B/P  | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 10 | PENDING | Transport: • Transport and perform ongoing assessment as indicated. • Do not delay transport for any reason if possible; interventions should be done  | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |
| `04b_Aortic_Dissection_AAA_PROC.md` | 11 | PENDING | Medical Control Contact: • Contact Medical Control for guidance as needed. | kept — action (whole page is outside PEMS 2024: Aortic Dissection/AAA awaits OMD authorization on every row) |

**25 rows judged**: 3 relocated, 22 kept, each with the reason recorded above.

