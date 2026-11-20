# Pip-strip rollout — reconciliation evidence (developer)

Derived in code from the markdown under `docs/protocols/` and `docs/procedures/` at branch tip `working tree`. Generator: `scripts/reconcile_rollout.py` (committed), which calls the verifier's own `page_tables()` classifier. Nothing in this table is hand-written.

## 1. Page-by-page reconciliation

| page | has lv-wrap table? | converted? | if not, why |
|---|---|---|---|
| `procedures/CPAP.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Capnography.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Chest_Decompression.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Endotracheal_Intubation.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Intraosseous_Access.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Medical_Devices_Pumps.md` | no | no | no table, nothing to convert |
| `procedures/Medication_Administration.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Nasogastric_Tube.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Neonatal_Resuscitation.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Spinal_Motion_Restriction.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Surgical_Airway.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Taser_Barb_Removal.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Tourniquet_Application.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Transcutaneous_Pacing.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Vaccination.md` | no | no | no table, nothing to convert |
| `protocols/administrative/01_ALS_Release_to_BLS_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Communications_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Helicopter_EMS_HEMS_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Infant_Abandonment_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Patient_Restraint_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_STEMI_Field_Triage_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Stroke_Field_Triage_PROC.md` | yes | no | policy (Basis) table (1 table): no `Level` column; one row names a provider level as its basis, so it is not a level table |
| `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/administrative/01_Trauma_Field_Triage_PROC.md` | yes | no | policy table (1 table): no `Level` column (header is `# | Basis | Action`) |
| `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Bradycardia_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Post_Resuscitation_Care_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md` | yes | yes | 3 of 3 table(s) |
| `protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md` | yes | no | PENDING table (1 table): every row is PENDING — no provider level published |
| `protocols/front-matter/00 - AI Formatting Guidelines.md` | no | no | no table, nothing to convert |
| `protocols/front-matter/00 - Introduction.md` | no | no | no table, nothing to convert |
| `protocols/front-matter/01 - How to Read the Protocols.md` | no | no | no table, nothing to convert |
| `protocols/front-matter/Universal Patient Care.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Cold_Exposure_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Heat_Exposure_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Pain_Control_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md` | yes | yes | 3 of 3 table(s) |
| `protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/medical/07_OB_Emergencies_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/medical/07_Sepsis_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/neurologic/05_Seizure_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/neurologic/05_Stroke_TIA_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/outstanding-decisions.md` | no | no | no table, nothing to convert |
| `protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Pediatric_Stridor_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Pneumothorax_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Respiratory_Arrest_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Respiratory_Distress_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Smoke_Inhalation_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/toxicology/06_Nausea_Vomiting_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/toxicology/06_Nerve_Agents_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/toxicology/06_Overdose_Poisoning_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Burns_Thermal_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Crush_Syndrome_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Electrical_Injuries_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Hemorrhage_Control_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Lightning_Injuries_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Trauma_PROC.md` | yes | yes | 1 of 1 table(s) |

## 2. Arithmetic

```
total pages under docs/protocols + docs/procedures: 75
  carry an lv-wrap table: 69
    converted: 54  (58 tables, 518 action rows, 3 of them PENDING)
    skipped: 15  (no level table to convert — see section 3)
  no lv-wrap table: 6
check: 54 + 15 + 6 = 75 -> True
```

## 3. The skip set, by class

Classified from the table, not the page: a **policy table** is one whose second header cell is not `Level` (`| # | Basis | Action / Intervention |`); a **PENDING table** is one where every row's level cell is `<span class="lvl lvl-pending">PENDING</span>`. A level table with only *some* PENDING rows is converted — its PENDING rows render as dashed pips with the tag `PENDING — no published level`, never as a level.

- **policy table — no `Level` column** — 13 page(s): `protocols/administrative/01_ALS_Release_to_BLS_PROC.md`, `protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.md`, `protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md`, `protocols/administrative/01_Communications_PROC.md`, `protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md`, `protocols/administrative/01_Helicopter_EMS_HEMS_PROC.md`, `protocols/administrative/01_Infant_Abandonment_PROC.md`, `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md`, `protocols/administrative/01_Patient_Restraint_PROC.md`, `protocols/administrative/01_STEMI_Field_Triage_PROC.md`, `protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.md`, `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md`, `protocols/administrative/01_Trauma_Field_Triage_PROC.md`
- **policy (Basis) table naming a level as its basis — not a level table, not converted** — 1 page(s): `protocols/administrative/01_Stroke_Field_Triage_PROC.md`
- **PENDING table — every row is PENDING, no level is published** — 1 page(s): `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md`
- **no table, nothing to convert** — 6 page(s): `procedures/Medical_Devices_Pumps.md`, `procedures/Vaccination.md`, `protocols/front-matter/00 - AI Formatting Guidelines.md`, `protocols/front-matter/00 - Introduction.md`, `protocols/front-matter/01 - How to Read the Protocols.md`, `protocols/outstanding-decisions.md`

The classifier fails the build (`ValueError`, so `mkdocs build --strict` fails) if a table has provider-level chips but no `Level` column, if a `policy`-wrapped table has a `Level` column with level chips, or if a row publishes neither a level nor PENDING. Two level tables were wrongly skipped before that guard existed; it is the rule that stops a repeat.

## 4. Row parity (verifier output, quoted verbatim)

```
518 rows in markdown / 518 rows in HTML / 518 compared / 0 mismatches
```

`scripts/verify_pip_strip.py` reads the chips out of the markdown with its own reader and compares them with the `data-states` of every rendered row, so that line is a machine comparison of every converted row, not a count.

