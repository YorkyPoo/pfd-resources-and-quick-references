# C2 — adjudicated cells

Generated 2026-11-15T03:40:48Z from the rasters in `audit/level-scan/evidence/` and `pems_table.json`.

## Decision vocabulary

| decision | meaning |
|---|---|
| `set_cells` | level cells must change to resolved_cells (C3 applies) |
| `confirm` | site cells already equal the PEMS row's columns; nothing changes |
| `site_split_of_pems` | one PEMS row split across site rows; cells correct as authored, recorded for the split review |
| `no_pems_counterpart` | no PEMS row of its own; cells authored; no change, review with the named parent |
| `ownership` | another site row owns the PEMS row; this row is authored detail; no change |
| `add_from_pems` | site prints no level where PEMS prints one; C3 adds resolved_cells |
| `held_split_review` | level already correct; split review list (do NOT set to matched) |
| `info` | named item with no cell decision |
| `UNRESOLVED` | could not be settled from the source |

## Counts

```
{
 "records": 63,
 "queue_rows_covered": 61,
 "by_decision": {
  "site_split_of_pems": 3,
  "set_cells": 26,
  "held_split_review": 7,
  "ownership": 1,
  "add_from_pems": 1,
  "no_pems_counterpart": 7,
  "info": 2,
  "confirm": 15,
  "UNRESOLVED": 1
 },
 "by_disposition": {
  "ownership_adjudication": 8,
  "held_level_correct": 7,
  "site_gap_add": 1,
  "named_item": 5,
  "ambiguous_adjudication": 42
 },
 "raster_verified": 31,
 "unresolved": [
  "protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md rNone p.245#4"
 ],
 "no_badge_overrides_written": true
}
```

## Rulings

| file | row | PEMS | disposition | decision | cells (EMR EMT A I P) | conf | basis |
|---|---:|---|---|---|---|---|---|
| `04_Cardiac_Arrest_Non_Traumatic_PROC.md` | 4 | p.63#7 | ownership_adjudication | `site_split_of_pems` | — | medium | raster |
| `04_Cardiac_Arrest_Traumatic_PROC.md` | 6 | p.61#5 | ownership_adjudication | `set_cells` | . . • • • | high | raster |
| `04_Chest_Pain_ACS_PROC.md` | 13 | p.107#9 | held_level_correct | `held_split_review` | — | high | text layer |
| `04_Chest_Pain_ACS_PROC.md` | 5 | p.107#4 | ownership_adjudication | `ownership` | — | medium | text layer |
| `05_Stroke_TIA_PROC.md` | 6 | p.131#4 | held_level_correct | `held_split_review` | — | high | text layer |
| `05_Stroke_TIA_PROC.md` | 7 | p.131#4 | ownership_adjudication | `site_split_of_pems` | — | high | text layer |
| `03_Airway_Inhalation_Irritants_PROC.md` | 3 | p.153#2 | held_level_correct | `held_split_review` | — | high | text layer |
| `03_Pneumothorax_PROC.md` | 11 | p.243#4 | held_level_correct | `held_split_review` | — | high | text layer |
| `03_Respiratory_Arrest_PROC.md` | 11 | p.269#0 | site_gap_add | `add_from_pems` | . . . . • | high | raster |
| `03_Respiratory_Distress_PROC.md` | 10 | p.124#10 | ownership_adjudication | `no_pems_counterpart` | — | medium | text layer |
| `03_Respiratory_Distress_PROC.md` | 8 | p.123#4 | ownership_adjudication | `set_cells` | . . . • • | high | raster |
| `03_Smoke_Inhalation_PROC.md` | 11 | p.153#2 | ownership_adjudication | `no_pems_counterpart` | — | medium | text layer |
| `03_Smoke_Inhalation_PROC.md` | 4 | p.153#2 | held_level_correct | `held_split_review` | — | high | text layer |
| `03_Upper_Airway_Obstruction_PROC.md` | 3 | p.239#3 | held_level_correct | `held_split_review` | — | high | raster |
| `03_Upper_Airway_Obstruction_PROC.md` | 8 | p.239#6 | held_level_correct | `held_split_review` | — | high | raster |
| `09_Trauma_PROC.md` | 7 | p.83#10 | ownership_adjudication | `set_cells` | . . • • • | high | text layer |
| `04_V_Fib_Pulseless_V_Tach_PROC.md` | 5 | p.63#7 | named_item | `site_split_of_pems` | — | high | raster |
| `03_Respiratory_Distress_PROC.md` | — | p.125 | named_item | `info` | — | high | raster |
| `04_Cardiac_Arrest_Non_Traumatic_PROC.md` | — | p.64#9 | named_item | `info` | — | high | raster |
| `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | 1 | p.57#1 | ambiguous_adjudication | `confirm` | — | high | text layer |
| `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | 12 | p.57#8 | ambiguous_adjudication | `confirm` | — | medium | text layer |
| `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | 11 | p.57#7 | ambiguous_adjudication | `confirm` | — | high | text layer |
| `04_Cardiac_Arrest_Non_Traumatic_PROC.md` | 14 | p.64#13 | ambiguous_adjudication | `set_cells` | • • • • • | high | raster |
| `04_Cardiac_Arrest_Non_Traumatic_PROC.md` | 9 | p.64#9 | ambiguous_adjudication | `confirm` | — | high | raster |
| `04_Cardiac_Arrest_Traumatic_PROC.md` | 3 | p.61#4 | ambiguous_adjudication | `set_cells` | . • • • • | high | raster |
| `04_Cardiac_Arrest_Traumatic_PROC.md` | 4 | p.61#4 | ambiguous_adjudication | `set_cells` | . . . • • | medium | raster |
| `04_Supraventricular_Tachycardia_PROC.md` | 13 | p.135#5 | ambiguous_adjudication | `set_cells` | . . . • • | high | text layer |
| `04_Supraventricular_Tachycardia_PROC.md` | 15 | p.136#6 | ambiguous_adjudication | `confirm` | — | high | text layer |
| `04_Supraventricular_Tachycardia_PROC.md` | 16 | p.136#6 | ambiguous_adjudication | `set_cells` | . . . • • | medium | text layer |
| `04_Supraventricular_Tachycardia_PROC.md` | 5 | p.135#2 | ambiguous_adjudication | `set_cells` | . . • • • | high | text layer |
| `04_Supraventricular_Tachycardia_PROC.md` | 8 | p.135#3 | ambiguous_adjudication | `set_cells` | . . . • • | high | text layer |
| `02_Cold_Exposure_PROC.md` | 3 | p.67#1 | ambiguous_adjudication | `confirm` | — | high | text layer |
| `02_Heat_Exposure_PROC.md` | 3 | p.69#2 | ambiguous_adjudication | `set_cells` | . • • • • | high | text layer |
| `02_Heat_Exposure_PROC.md` | 4 | p.69#2 | ambiguous_adjudication | `set_cells` | . • • • • | high | text layer |
| `02_Heat_Exposure_PROC.md` | 5 | p.69#2 | ambiguous_adjudication | `set_cells` | . • • • • | high | text layer |
| `02_Pain_Control_PROC.md` | 7 | p.77#5 | ambiguous_adjudication | `set_cells` | . . [A] • • | high | raster |
| `02_Sedation_Assisted_Non_Paralytic_PROC.md` | 5 | p.55#2 | ambiguous_adjudication | `set_cells` | . . . • • | medium | text layer |
| `02_Sedation_Assisted_Non_Paralytic_PROC.md` | 6 | p.55#3 | ambiguous_adjudication | `set_cells` | . . . • • | high | text layer |
| `07_OB_Emergencies_PROC.md` | 1 | p.147#0 | ambiguous_adjudication | `confirm` | — | high | text layer |
| `07_OB_Emergencies_PROC.md` | 4 | p.141#3 | ambiguous_adjudication | `set_cells` | • • • • • | high | text layer |
| `05_Seizure_PROC.md` | 6 | p.127#5 | ambiguous_adjudication | `set_cells` | . . [A] • • | high | raster |
| `05_Stroke_TIA_PROC.md` | 9 | p.131#2 | ambiguous_adjudication | `set_cells` | • • • • • | high | text layer |
| `03_Airway_Inhalation_Irritants_PROC.md` | 7 | p.153#4 | ambiguous_adjudication | `confirm` | — | high | text layer |
| `03_Asthma_COPD_Reactive_Airway_PROC.md` | 4 | p.123#5 | ambiguous_adjudication | `confirm` | — | high | raster |
| `03_Pneumothorax_PROC.md` | 12 | p.243#4 | ambiguous_adjudication | `no_pems_counterpart` | — | medium | text layer |
| `03_Pulmonary_Edema_Congestion_PROC.md` | 10 | p.124#11 | ambiguous_adjudication | `set_cells` | . . • • • | high | text layer |
| `03_Pulmonary_Edema_Congestion_PROC.md` | 5 | p.123#3 | ambiguous_adjudication | `set_cells` | . • • • • | high | raster |
| `03_Pulmonary_Edema_Congestion_PROC.md` | 6 | p.245#2 | ambiguous_adjudication | `no_pems_counterpart` | — | medium | raster |
| `03_Pulmonary_Edema_Congestion_PROC.md` | 7 | p.245#2 | ambiguous_adjudication | `no_pems_counterpart` | — | medium | raster |
| `03_Pulmonary_Edema_Congestion_PROC.md` | 8 | p.245#2 | ambiguous_adjudication | `no_pems_counterpart` | — | medium | raster |
| `03_Pulmonary_Edema_Congestion_PROC.md` | 9 | p.239#5 | ambiguous_adjudication | `set_cells` | . . . • • | high | raster |
| `03_Respiratory_Arrest_PROC.md` | 2 | p.239#6 | ambiguous_adjudication | `confirm` | — | high | raster |
| `03_Respiratory_Distress_PROC.md` | 6 | p.123#3 | ambiguous_adjudication | `set_cells` | . • • • • | high | raster |
| `03_Respiratory_Distress_PROC.md` | 7 | p.123#3 | ambiguous_adjudication | `set_cells` | . • • • • | high | raster |
| `03_Smoke_Inhalation_PROC.md` | 5 | p.123#4 | ambiguous_adjudication | `set_cells` | . . . • • | medium | raster |
| `03_Upper_Airway_Obstruction_PROC.md` | 5 | p.239#3 | ambiguous_adjudication | `confirm` | — | high | raster |
| `03_Upper_Airway_Obstruction_PROC.md` | 6 | p.239#3 | ambiguous_adjudication | `confirm` | — | high | raster |
| `09_Crush_Syndrome_PROC.md` | 1 | p.91#1 | ambiguous_adjudication | `confirm` | — | high | raster |
| `09_Crush_Syndrome_PROC.md` | 5 | p.91#5 | named_item | `confirm` | — | high | raster |
| `09_Crush_Syndrome_PROC.md` | 6 | p.91#5 | ambiguous_adjudication | `set_cells` | . . . [I] • | high | raster |
| `09_Hemorrhage_Control_PROC.md` | 1 | p.75#0 | ambiguous_adjudication | `confirm` | — | high | text layer |
| `09_Hemorrhage_Control_PROC.md` | 9 | p.75#3 | ambiguous_adjudication | `no_pems_counterpart` | — | high | text layer |
| `03_Pulmonary_Edema_Congestion_PROC.md` | — | p.245#4 | named_item | `UNRESOLVED` | — | high that the print is broken; UNRESOLVED on the intended number | raster |

## Verdicts

### 1. `04_Cardiac_Arrest_Non_Traumatic_PROC.md` r4 — p.63#7

**site_split_of_pems** (medium; raster read with vision)

Compound row. Badge I is printed once for the whole defibrillation row; the inline '[EMR]' puts the AED in the EMR's hands ('or AED is advising to shock [EMR]'). Site rows 4 (AED application) and 5 (defibrillation) split this one PEMS row. r4's EMT/A cells are supported by that inline annotation, not by the badge, so no cell change and the provisional site_broader flag is withdrawn as an authoring difference.

- evidence: `audit/level-scan/evidence/vfib_p63-063.png`

### 2. `04_Cardiac_Arrest_Traumatic_PROC.md` r6 — p.61#5

**set_cells** (high; raster read with vision)

PEMS p.61#5 badge A opens with 'Obtain IV/IO access. Establish secondary IV/IO access if possible.' Access is authorised at A; corroborated by p.57#5, p.63#5 and p.135#2, all badge A on an access row. Site prints I/P (narrower by A).

- resolved cells: `. . • • •`

- evidence: `audit/level-scan/evidence/cardiacarresttraumatic_p61-061.png`

### 3. `04_Chest_Pain_ACS_PROC.md` r13 — p.107#9

**held_split_review** (high; PDF text layer (pems_table.json))

PEMS MC in every column; site MC in every column. Level already correct; goes to the split review list. Do not set to matched.

- evidence: `audit/level-scan/evidence/page_107-107.png`

### 4. `04_Chest_Pain_ACS_PROC.md` r5 — p.107#4

**ownership** (medium; PDF text layer (pems_table.json))

p.107#4 is owned by site r6 (STEMI alert / notification). r5 is a site-authored interpretation step with no PEMS row of its own; PEMS badges the EMT for acting on the 12-lead, so the site's P-only gate is narrower than the source. Authoring question, no cell change.

- evidence: `audit/level-scan/evidence/page_107-107.png`

### 5. `05_Stroke_TIA_PROC.md` r6 — p.131#4

**held_split_review** (high; PDF text layer (pems_table.json))

PEMS EMT/A/I/P; site EMT/A/I/P. Level correct; split review list. Do not set to matched.

- evidence: `audit/level-scan/evidence/page_131-131.png`

### 6. `05_Stroke_TIA_PROC.md` r7 — p.131#4

**site_split_of_pems** (high; PDF text layer (pems_table.json))

One PEMS transport row with two triage branches, badge EMT. r6 (comprehensive centre, EMT..P) plus r7 (primary centre, A/I/P) union to EMT/A/I/P = the badge spread, so the split invariant holds and r7's cells are correct as authored.

- evidence: `audit/level-scan/evidence/page_131-131.png`

### 7. `03_Airway_Inhalation_Irritants_PROC.md` r3 — p.153#2

**held_split_review** (high; PDF text layer (pems_table.json))

PEMS EMT/A/I/P; site EMT/A/I/P. Split review list.

- evidence: `audit/level-scan/evidence/page_153-153.png`

### 8. `03_Pneumothorax_PROC.md` r11 — p.243#4

**held_split_review** (high; PDF text layer (pems_table.json))

PEMS I/P; site I/P. Split review list.

- evidence: `audit/level-scan/evidence/page_243-243.png`

### 9. `03_Respiratory_Arrest_PROC.md` r11 — p.269#0

**add_from_pems** (high; raster read with vision)

C1 bound this row to p.239#2 (suctioning, EMR, all five columns) on text overlap — that binding is wrong. The true source is the Surgical Airway procedure, p.269, where every cricothyrotomy step prints badge P (raster confirms). ADD P only; adding all five columns would be a clinical defect.

- resolved cells: `. . . . •`

- evidence: `audit/level-scan/evidence/page_269-269.png`

### 10. `03_Respiratory_Distress_PROC.md` r10 — p.124#10

**no_pems_counterpart** (medium; PDF text layer (pems_table.json))

p.124#10 is pediatric nebulised saline. No crystalloid bolus row exists on pp.123-125, so 'Fluid Administration' has no PEMS counterpart; its MC/MC cells are site-authored. No change, authoring flag.

- evidence: `audit/level-scan/evidence/page_124-124.png`

### 11. `03_Respiratory_Distress_PROC.md` r8 — p.123#4

**set_cells** (high; raster read with vision)

C1 bound this row to p.123#1 (focused evaluation, EMR). The text match is p.123#4 'Consider invasive ventilatory support via endotracheal intubation', badge I -> I/P. Site prints P only.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_123-123.png`

### 12. `03_Smoke_Inhalation_PROC.md` r11 — p.153#2

**no_pems_counterpart** (medium; PDF text layer (pems_table.json))

No burn-fluid row on the inhalation/irritants page. Site prints I/P (blocks EMT/A) with no PEMS row behind it. Authoring flag, no change.

- evidence: `audit/level-scan/evidence/page_153-153.png`

### 13. `03_Smoke_Inhalation_PROC.md` r4 — p.153#2

**held_split_review** (high; PDF text layer (pems_table.json))

PEMS EMT/A/I/P; site EMT/A/I/P. Split review list.

- evidence: `audit/level-scan/evidence/page_153-153.png`

### 14. `03_Upper_Airway_Obstruction_PROC.md` r3 — p.239#3

**held_split_review** (high; raster read with vision)

PEMS EMT/A/I/P; site EMT/A/I/P. Split review list.

- evidence: `audit/level-scan/evidence/page_239-239.png`

### 15. `03_Upper_Airway_Obstruction_PROC.md` r8 — p.239#6

**held_split_review** (high; raster read with vision)

PEMS EMT/A/I/P; site EMT/A/I/P. Split review list.

- evidence: `audit/level-scan/evidence/page_239-239.png`

### 16. `09_Trauma_PROC.md` r7 — p.83#10

**set_cells** (high; PDF text layer (pems_table.json))

p.83#10 (hypovolemia / crystalloid) is badge A; IV/IO access is an A-level act in every PEMS protocol that badges it. Site prints I/P. Note: site r8 (Fluid Resuscitation, currently 'matched', out of this queue) prints I/P for the same A-badged row — same defect.

- resolved cells: `. . • • •`

- evidence: `audit/level-scan/evidence/page_83-083.png`

### 17. `04_V_Fib_Pulseless_V_Tach_PROC.md` r5 — p.63#7

**site_split_of_pems** (high; raster read with vision)

Raster: one row, one badge (I), text 'If VF or VT is present, or AED is advising to shock [EMR], immediately defibrillate'. Two triggers, one action: the defibrillation is I; the AED may be applied/read by an EMR, which is what the bracketed token says. Site's own annotation '(AED for EMR/EMT, Manual for I/P)' matches the source. No cell change; provisional site_broader withdrawn as an authoring difference, not a level defect.

- evidence: `audit/level-scan/evidence/vfib_p63-063.png`

### 18. `03_Respiratory_Distress_PROC.md` r— — p.125

**info** (high; raster read with vision)

Named item (pearl tail). Raster of p.125 shows the page ends cleanly after six pearls; nothing is cut off. Recovered tail: 'Note: these medications are routinely prescribed to both men and women for a variety of conditions.'

- evidence: `audit/level-scan/evidence/respdist_p125-125.png`

### 19. `04_Cardiac_Arrest_Non_Traumatic_PROC.md` r— — p.64#9

**info** (high; raster read with vision)

Named item (amiodarone 300 vs 150). Raster of p.64: p.64#9 = 'Amiodarone 300 mg IV/IO slow push' (plus lidocaine alternative), badge I; p.64#10 = 'Amiodarone 150 mg ... ensure optimal defibrillator pad placement', badge I. Two separate rows, both I. Site CNT r9 (300 mg) is the first dose and correctly prints I/P once re-bound to p.64#9. Site V-Fib r8 (150 mg) prints P only -> narrower than I (out of this queue, flagged).

- evidence: `audit/level-scan/evidence/vfib_p64-064.png`

### 20. `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` r1 — p.57#1

**confirm** (high; PDF text layer (pems_table.json))

Site row merges p.57#0 and p.57#1, both badge EMR (all five columns); site prints all five. Confirm.

- evidence: `audit/level-scan/evidence/page_57-057.png`

### 21. `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` r12 — p.57#8

**confirm** (medium; PDF text layer (pems_table.json))

Site prints MC in every cell, matching p.57#8 (MC). The row also contains the ROSC / withholding referral, which PEMS badges EMR (p.57#0-#3, p.64#13), so all-MC under-grants that half. Matches the row it is bound to; authoring flag only.

- evidence: `audit/level-scan/evidence/page_57-057.png`

### 22. `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` r11 — p.57#7

**confirm** (high; PDF text layer (pems_table.json))

PEMS p.57#7 badge I -> I/P; site I/P. Confirm. Note: site r10 (adult half, 'matched', out of queue) prints A/I/P where the same I-badged row authorises I/P — broader than the badge.

- evidence: `audit/level-scan/evidence/page_57-057.png`

### 23. `04_Cardiac_Arrest_Non_Traumatic_PROC.md` r14 — p.64#13

**set_cells** (high; raster read with vision)

p.64#13 'If ROSC is achieved, refer to Post ROSC Care' is badge EMR = every column; the no-ROSC half is p.57#1, also EMR. Site prints EMT..P (narrower by EMR).

- resolved cells: `• • • • •`

- evidence: `audit/level-scan/evidence/vfib_p64-064.png`

### 24. `04_Cardiac_Arrest_Non_Traumatic_PROC.md` r9 — p.64#9

**confirm** (high; raster read with vision)

C1 bound this row to p.64#11 (magnesium). The 300 mg amiodarone text is p.64#9, badge I -> I/P, which is exactly what the site prints. Confirm on the corrected key.

- evidence: `audit/level-scan/evidence/vfib_p64-064.png`

### 25. `04_Cardiac_Arrest_Traumatic_PROC.md` r3 — p.61#4

**set_cells** (high; raster read with vision)

C1 bound this row to p.61#8 (epinephrine). 'Apply AED or cardiac monitor' is p.61#4, badge EMT -> EMT/A/I/P. Site prints A/I/P (narrower by EMT).

- resolved cells: `. • • • •`

- evidence: `audit/level-scan/evidence/cardiacarresttraumatic_p61-061.png`

### 26. `04_Cardiac_Arrest_Traumatic_PROC.md` r4 — p.61#4

**set_cells** (medium; raster read with vision)

Raster: the row is 'Apply AED or cardiac monitor. Assess rhythm (I / P): For Asystole at the time of EMS arrival: Consider withholding / terminating resuscitation...'. The (I / P) token governs the rhythm assessment and the withhold/continue clauses, which is exactly what this site row states. Site prints EMT/A/I/P -> should be I/P.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/cardiacarresttraumatic_p61-061.png`

### 27. `04_Supraventricular_Tachycardia_PROC.md` r13 — p.135#5

**set_cells** (high; PDF text layer (pems_table.json))

p.135#5 (light sedation) ends 'Monitor SpO2 and EtCO2', inside the same badge-I row. Site row prints no level at all -> I/P.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_135-135.png`

### 28. `04_Supraventricular_Tachycardia_PROC.md` r15 — p.136#6

**confirm** (high; PDF text layer (pems_table.json))

Repeat-cardioversion half of p.136#6 (badge I); site I/P. Confirm.

- evidence: `audit/level-scan/evidence/page_136-136.png`

### 29. `04_Supraventricular_Tachycardia_PROC.md` r16 — p.136#6

**set_cells** (medium; PDF text layer (pems_table.json))

'If cardioversion is unsuccessful after two attempts, contact Medical Control' is the last clause of p.136#6, badge I. Site prints [P] only: under-grants I, and the bracket is not in the source. SVT's own MC row is p.136#7 (all MC).

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_136-136.png`

### 30. `04_Supraventricular_Tachycardia_PROC.md` r5 — p.135#2

**set_cells** (high; PDF text layer (pems_table.json))

Site label says 'A: Obtain IV access'; p.135#2 badge A. Site prints I/P (narrower by A).

- resolved cells: `. . • • •`

- evidence: `audit/level-scan/evidence/page_135-135.png`

### 31. `04_Supraventricular_Tachycardia_PROC.md` r8 — p.135#3

**set_cells** (high; PDF text layer (pems_table.json))

Repeat-adenosine clause is inside p.135#3, badge I. Site label says 'I:' but prints P only.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_135-135.png`

### 32. `02_Cold_Exposure_PROC.md` r3 — p.67#1

**confirm** (high; PDF text layer (pems_table.json))

'Handle the patient gently' is inside p.67#1, badge EMR (all five). Site all five. Confirm.

- evidence: `audit/level-scan/evidence/page_67-067.png`

### 33. `02_Heat_Exposure_PROC.md` r3 — p.69#2

**set_cells** (high; PDF text layer (pems_table.json))

Cool compresses for normal skin temperature are inside p.69#2, badge EMT. Site prints A/I/P (narrower by EMT).

- resolved cells: `. • • • •`

- evidence: `audit/level-scan/evidence/page_69-069.png`

### 34. `02_Heat_Exposure_PROC.md` r4 — p.69#2

**set_cells** (high; PDF text layer (pems_table.json))

Rapid cooling for hot skin / heat stroke is inside p.69#2, badge EMT. Site prints A/I/P.

- resolved cells: `. • • • •`

- evidence: `audit/level-scan/evidence/page_69-069.png`

### 35. `02_Heat_Exposure_PROC.md` r5 — p.69#2

**set_cells** (high; PDF text layer (pems_table.json))

'If patient begins to shiver, slow cooling process' is inside p.69#2, badge EMT. Site A/I/P.

- resolved cells: `. • • • •`

- evidence: `audit/level-scan/evidence/page_69-069.png`

### 36. `02_Pain_Control_PROC.md` r7 — p.77#5

**set_cells** (high; raster read with vision)

C1 bound this row to p.77#4 (ketorolac, A). Raster of p.77: ONE row carries the bracketed badge [A] and contains both Fentanyl and 'OR: Morphine Sulfate 2.5 - 5 mg'. Morphine is p.77#5, badge [A] -> A/I/P with the bracket preserved. Site prints I/P.

- resolved cells: `. . [A] • •`

- evidence: `audit/level-scan/evidence/page_77-077.png`

### 37. `02_Sedation_Assisted_Non_Paralytic_PROC.md` r5 — p.55#2

**set_cells** (medium; PDF text layer (pems_table.json))

No ketamine row exists on p.55; post-intubation sedation is an I-level act there (fentanyl p.55#2 and midazolam p.55#3 are both badge I). Site prints P only. Medium: inferred from the page's sedation badges, not from an identical row.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_55-055.png`

### 38. `02_Sedation_Assisted_Non_Paralytic_PROC.md` r6 — p.55#3

**set_cells** (high; PDF text layer (pems_table.json))

This row names Midazolam and Fentanyl, i.e. p.55#3 and p.55#2, both badge I -> I/P. Site prints P only.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_55-055.png`

### 39. `07_OB_Emergencies_PROC.md` r1 — p.147#0

**confirm** (high; PDF text layer (pems_table.json))

Universal patient care row, badge EMR (all five); site all five. Confirm.

- evidence: `audit/level-scan/evidence/page_147-147.png`

### 40. `07_OB_Emergencies_PROC.md` r4 — p.141#3

**set_cells** (high; PDF text layer (pems_table.json))

'If breech presentation or cord prolapse, refer to guidance below' is badge EMR = every column. Site prints EMT..P (narrower by EMR).

- resolved cells: `• • • • •`

- evidence: `audit/level-scan/evidence/page_141-141.png`

### 41. `05_Seizure_PROC.md` r6 — p.127#5

**set_cells** (high; raster read with vision)

Raster: the midazolam row prints a single bracketed badge [A]. The half-dose line is the last sentence of that row, so it is [A]/I/P. Site prints I/P (narrower by A, and drops the bracket).

- resolved cells: `. . [A] • •`

- evidence: `audit/level-scan/evidence/page_127-127.png`

### 42. `05_Stroke_TIA_PROC.md` r9 — p.131#2

**set_cells** (high; PDF text layer (pems_table.json))

'Record time last seen normal ... provide to the receiving facility' is badge EMR = all five. Site prints A/I/P.

- resolved cells: `• • • • •`

- evidence: `audit/level-scan/evidence/page_131-131.png`

### 43. `03_Airway_Inhalation_Irritants_PROC.md` r7 — p.153#4

**confirm** (high; PDF text layer (pems_table.json))

Methylprednisolone is inside p.153#4, badge A -> A/I/P; site A/I/P. Confirm.

- evidence: `audit/level-scan/evidence/page_153-153.png`

### 44. `03_Asthma_COPD_Reactive_Airway_PROC.md` r4 — p.123#5

**confirm** (high; raster read with vision)

Ipratropium is inside p.123#5, badge EMT -> EMT/A/I/P; site matches. Confirm.

- evidence: `audit/level-scan/evidence/page_123-123.png`

### 45. `03_Pneumothorax_PROC.md` r12 — p.243#4

**no_pems_counterpart** (medium; PDF text layer (pems_table.json))

'Hemodynamic Support: fluid bolus / vasopressors' has no PEMS row on p.243 (decompression only); p.243#4 is reassessment. Site I/P is authored and happens to equal that row's columns. No change; authoring flag.

- evidence: `audit/level-scan/evidence/page_243-243.png`

### 46. `03_Pulmonary_Edema_Congestion_PROC.md` r10 — p.124#11

**set_cells** (high; PDF text layer (pems_table.json))

Nitroglycerine 0.4 mg SL is p.124#11, badge A -> A/I/P. Site prints I/P (narrower by A).

- resolved cells: `. . • • •`

- evidence: `audit/level-scan/evidence/page_124-124.png`

### 47. `03_Pulmonary_Edema_Congestion_PROC.md` r5 — p.123#3

**set_cells** (high; raster read with vision)

'Consider non-invasive (CPAP) or invasive (SGA) ventilatory support' is p.123#3, badge EMT (raster). Site prints A/I/P (narrower by EMT).

- resolved cells: `. • • • •`

- evidence: `audit/level-scan/evidence/page_123-123.png`

### 48. `03_Pulmonary_Edema_Congestion_PROC.md` r6 — p.245#2

**no_pems_counterpart** (medium; raster read with vision)

CPAP contraindications are procedure text from the CPAP/BiPAP/PEEP page (p.245), not a level-gated PEMS grid row. No cell change; the site's A/I/P is a downstream consequence of the parent CPAP row and should be reviewed with it.

- evidence: `audit/level-scan/evidence/cpap_p245-245.png`

### 49. `03_Pulmonary_Edema_Congestion_PROC.md` r7 — p.245#2

**no_pems_counterpart** (medium; raster read with vision)

CPAP contraindications, as row 6. No cell change; authoring review with the parent CPAP row.

- evidence: `audit/level-scan/evidence/cpap_p245-245.png`

### 50. `03_Pulmonary_Edema_Congestion_PROC.md` r8 — p.245#2

**no_pems_counterpart** (medium; raster read with vision)

CPAP contraindications, as row 6. No cell change; authoring review with the parent CPAP row.

- evidence: `audit/level-scan/evidence/cpap_p245-245.png`

### 51. `03_Pulmonary_Edema_Congestion_PROC.md` r9 — p.239#5

**set_cells** (high; raster read with vision)

PEEP titration is explicitly restricted in the source: p.239#5 'I/P only: Adjust PEEP to support ventilation and work of breathing, up to 10 cmH2O' (raster). Site prints P only -> I/P. Upper bound confirmed as 10 cmH2O, not 15.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_239-239.png`

### 52. `03_Respiratory_Arrest_PROC.md` r2 — p.239#6

**confirm** (high; raster read with vision)

Position/open airway with BLS adjuncts is p.239#6, badge EMT -> EMT/A/I/P; site matches. Confirm.

- evidence: `audit/level-scan/evidence/page_239-239.png`

### 53. `03_Respiratory_Distress_PROC.md` r6 — p.123#3

**set_cells** (high; raster read with vision)

CPAP block: starting CPAP at PEEP 5 is EMT (p.239#5, p.123#3), titration to 10 is I/P only. Union = EMT/A/I/P. Site prints MC/MC, far narrower than the source.

- resolved cells: `. • • • •`

- evidence: `audit/level-scan/evidence/page_123-123.png`

### 54. `03_Respiratory_Distress_PROC.md` r7 — p.123#3

**set_cells** (high; raster read with vision)

SGA placement is EMT: p.239#6 'Use BLS airway adjuncts (OPA/NPA/SGA)' badge EMT, and p.123#3 groups SGA with CPAP at badge EMT. Site row prints no level -> EMT/A/I/P.

- resolved cells: `. • • • •`

- evidence: `audit/level-scan/evidence/page_123-123.png`

### 55. `03_Smoke_Inhalation_PROC.md` r5 — p.123#4

**set_cells** (medium; raster read with vision)

'Consider endotracheal intubation versus immediate transport' is the intubation decision, which PEMS badges I (p.123#4, p.239#9). Site prints P only. Medium: no identical sentence in the source.

- resolved cells: `. . . • •`

- evidence: `audit/level-scan/evidence/page_123-123.png`

### 56. `03_Upper_Airway_Obstruction_PROC.md` r5 — p.239#3

**confirm** (high; raster read with vision)

Pediatric abdominal thrusts are inside p.239#3, badge EMT -> EMT/A/I/P; site matches. Confirm.

- evidence: `audit/level-scan/evidence/page_239-239.png`

### 57. `03_Upper_Airway_Obstruction_PROC.md` r6 — p.239#3

**confirm** (high; raster read with vision)

Infant back blows / chest thrusts are inside p.239#3, badge EMT; site matches. Confirm.

- evidence: `audit/level-scan/evidence/page_239-239.png`

### 58. `09_Crush_Syndrome_PROC.md` r1 — p.91#1

**confirm** (high; raster read with vision)

Site row merges p.91#0 and p.91#1, both badge EMR (all five); site all five. Confirm.

- evidence: `audit/level-scan/evidence/crush_p91-091.png`

### 59. `09_Crush_Syndrome_PROC.md` r5 — p.91#5

**confirm** (high; raster read with vision)

Known item (NaHCO3). The card body said this row was written from one badge token while the PEMS line carried '[A] [I]'. The raster refutes that: the sodium bicarbonate / calcium chloride row carries ONE bracketed badge, [I]; the [A] belongs to the row above (continuous albuterol). The site prints [I]/• , which is exactly p.91#5's spread. Confirm — no defect on this row.

- evidence: `audit/level-scan/evidence/crush_p91-091.png`

### 60. `09_Crush_Syndrome_PROC.md` r6 — p.91#5

**set_cells** (high; raster read with vision)

Same PEMS row as site r5 (p.91#5, badge [I], spread {I,P}). The site splits the row's two drugs and prints P only for calcium chloride, which is narrower: PEMS badges the calcium at [I] too. Note the split-map union rule passes this pair only because r5 carries the I — do not let the union check hide the deficit on this half.

- resolved cells: `. . . [I] •`

- evidence: `audit/level-scan/evidence/crush_p91-091.png`

### 61. `09_Hemorrhage_Control_PROC.md` r1 — p.75#0

**confirm** (high; PDF text layer (pems_table.json))

Universal patient care / reassess, badge EMR (all five); site all five. Confirm.

- evidence: `audit/level-scan/evidence/page_75-075.png`

### 62. `09_Hemorrhage_Control_PROC.md` r9 — p.75#3

**no_pems_counterpart** (high; PDF text layer (pems_table.json))

No Medical Control row exists on p.75 (all EMR regional-pressure rows). A 'contact Medical Control' step is inherently all-MC, which is what the site prints. No change.

- evidence: `audit/level-scan/evidence/page_75-075.png`

### 63. `03_Pulmonary_Edema_Congestion_PROC.md` r— — p.245#4

**UNRESOLVED** (high that the print is broken; UNRESOLVED on the intended number; raster read with vision (4x zoom on the row))

The CPAP procedure row prints, verbatim and at 4x zoom, 'Consider titratingPEEP9%-15mmHg) as needed to improve ventilation/work of breathing.' The concatenation is broken in the source itself ('titratingPEEP9%-15mmHg)'), so the range cannot be read as a number without guessing. It is not encoded anywhere: the titration bound that IS legible is p.239#5 'up to 10 cmH2O' (I/P only), which is what the site publishes.

- evidence: `audit/level-scan/evidence/cpap_p245-245.png`

## Could not resolve

- `p.245#4` — The CPAP procedure row prints, verbatim and at 4x zoom, 'Consider titratingPEEP9%-15mmHg) as needed to improve ventilation/work of breathing.' The concatenation is broken in the source itself ('titratingPEEP9%-15mmHg)'), so the range cannot be read as a number without guessing. It is not encoded anywhere: the titration bound that IS legible is p.239#5 'up to 10 cmH2O' (I/P only), which is what the site publishes.
  evidence: `audit/level-scan/evidence/cpap_p245-245.png`

## The four provisional rows

`c2-scope.json` flags four rows `provisional` because the PEMS badge they join still carries an inline token. Every one of them now has a final ruling:

| row | was | now |
|---|---|---|
| `04_Cardiac_Arrest_Non_Traumatic_PROC.md` r4 | provisional, site_broader | final: keep cells — the EMT/A grant rests on the inline `[EMR]` AED annotation, not on the badge |
| `04_V_Fib_Pulseless_V_Tach_PROC.md` r5 | provisional, site_broader | final: keep cells — same compound row, defibrillation is I, AED is EMR/EMT |
| `04_Cardiac_Arrest_Traumatic_PROC.md` r3 | provisional, ambiguous | final: set to EMT/A/I/P (apply AED is the EMT half of p.61#4) |
| `04_Cardiac_Arrest_Traumatic_PROC.md` r4 | provisional, agrees | final: set to I/P (the `(I / P)` half of p.61#4) |

The `provisional` flags stay set in `c2-scope.json` because they are derived from the table and no badge override was written — see below. The rulings above are what the site should do.

## Why no badge override was written

Both contradictory badges are printed correctly: p.61#4 really is `EMT` and p.63#7 really is `I`. What constrains them is a clause-scoped inline token (`(I / P)` on 'Assess rhythm', `[EMR]` on 'AED is advising to shock'), not a second badge. Overriding the badge would replace a correct source value with a surrogate and would make the record unfaithful to the PDF. The corrections belong on the site cells, which is where they are recorded here. Consequently `badge-overrides.yaml` stays empty, and `scripts/recheck_ambiguous_badges.py` still reports the same two at-risk `matched` rows: `04_Cardiac_Arrest_Non_Traumatic_PROC.md` r5 (p.63#7) and `04_Cardiac_Arrest_Traumatic_PROC.md` r5 (p.61#4). Both print EMT/A/I/P on rows whose badge is `I` / `EMT`; the wider cells are the AED annotation again, and **0 rows flip to a new defect** as a result of this adjudication.

## Out-of-queue defects seen while adjudicating (not fixed here)

- `04_Cardiac_Arrest_Non_Traumatic_PROC.md` r5 and `04_Cardiac_Arrest_Traumatic_PROC.md` r5 are `matched` but print EMT/A/I/P on rows whose badge is I (p.63#7) / EMT (p.61#4). The at-risk re-check names them; the wider cells are explained by the inline AED annotations and should be left alone unless the OMD says otherwise.
- `04_Asystole_..._PROC.md` r10 prints A/I/P on p.57#7 (badge I).
- `04_Supraventricular_Tachycardia_PROC.md` r14 (initial cardioversion) prints no level while p.136#6 is badge I.
- `04_V_Fib_..._PROC.md` r7 (300 mg amiodarone) and r8 (150 mg) print P only while p.64#9/#10 are badge I.
- `03_Respiratory_Distress_PROC.md` r9 (IV/IO access) prints I/P where access is an A-level act.
- `03_Pulmonary_Edema_Congestion_PROC.md` r5-r9 and `03_Respiratory_Distress_PROC.md` r6-r7: the CPAP/SGA block is EMT with I/P titration; every one of these rows must move together.
