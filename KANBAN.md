# PEMS Protocol Audit — Kanban Board

> Auto-maintained by Hermes Agent. Each protocol card moves through:
> **Backlog → In Progress → Review → Done**

---

## How This Board Works

- **Backlog**: PENDING — not yet audited (list is ordered by priority)
- **In Progress**: currently being audited by Hermes
- **Review**: audited but needs a second pass or a human eye on discrepancies
- **Done**: VERIFIED — matches PEMS source, no discrepancies
- **Blocked**: protocol has an issue preventing audit (missing file, ambiguous source)

### Per-Audit Workflow
1. Pick the **first PENDING protocol** from Backlog
2. Move it to **In Progress**
3. Read PEMS chunk + converted protocol → compare for discrepancies
4. If **VERIFIED** → move to **Done**
5. If **FIXABLE** (minor discrepancies) → move to **Review**, add discrepancy notes
6. If **MANUAL** (significant discrepancies) → move to **Blocked**, add detailed notes

---

## Backlog

### Administrative (14)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 1 | Abuse Recognition | pems_chunks/Abuse_Recognition.txt | |
| 2 | ALS Release to BLS | pems_chunks/ALS_Release_to_BLS.txt | |
| 3 | Behavioral Health Transport | pems_chunks/Behavioral_Health_Transportation.txt | |
| 4 | Communications | pems_chunks/Communications.txt | |
| 5 | Death Criteria | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 6 | Helicopter EMS | pems_chunks/Helicopter_EMS.txt | |
| 7 | Infant Abandonment | pems_chunks/Infant_Abandonment.txt | |
| 8 | Patient Refusal | pems_chunks/Patient_Refusal.txt | |
| 9 | Patient Restraint | pems_chunks/Patient_Restraint.txt | |
| 10 | Transport of Pediatric | pems_chunks/Safe_Transport_of_Pediatric.txt | |
| 11 | STEMI Field Triage | pems_chunks/STEMI_Field_Triage.txt | |
| 12 | Stroke Field Triage | pems_chunks/Stroke_Field_Triage.txt | |
| 13 | Transport and Destination | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 14 | Trauma Field Triage | pems_chunks/Trauma_Field_Triage.txt | |

### General (6)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 15 | Behavioral Pt Restraint | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 16 | Cold Exposure | pems_chunks/Cold_Exposure.txt | |
| 17 | Diving and Drowning | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 18 | Heat Exposure | pems_chunks/Heat_Exposure.txt | |
| 19 | Pain Control | pems_chunks/Pain_Control.txt | |
| 20 | Sedation | pems_chunks/Sedation.txt | |

### Respiratory (9)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 21 | Airway Inhalation | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 22 | Asthma/COPD | pems_chunks/Asthma.txt | |
| 23 | Pediatric Stridor | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 24 | Pneumothorax | pems_chunks/Pneumothorax.txt | |
| 25 | Pulmonary Edema | pems_chunks/Pulmonary_Edema.txt | |
| 26 | Respiratory Arrest | pems_chunks/Respiratory_Arrest.txt | |
| 27 | Respiratory Distress | pems_chunks/Respiratory_Distress.txt | |
| 28 | Smoke Inhalation | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 29 | Upper Airway Obstruction | pems_chunks/Upper_Airway_Obstruction.txt | |

### Cardiac (10)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 30 | Aortic Dissection | pems_chunks/Aortic_Dissection.txt | MISSING - needs creation from PEMS chunk |
| 31 | Asystole/PEA | pems_chunks/Asystole.txt | |
| 32 | Bradycardia | pems_chunks/Bradycardia.txt | |
| 33 | Cardiac Arrest Non-Trauma | pems_chunks/Cardiac_Arrest.txt | |
| 34 | Cardiac Arrest Traumatic | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 35 | Chest Pain/ACS | pems_chunks/Chest_Pain.txt | |
| 36 | Hypertensive Crisis | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 37 | Post-Resuscitation Care | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 38 | SVT | pems_chunks/Supraventricular_Tachycardia.txt | |
| 39 | V-Fib/V-Tach | pems_chunks/V-Fib.txt | |

### Neurologic (3)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 40 | Hypoglycemia | pems_chunks/Hypoglycemia.txt | |
| 41 | Seizure | pems_chunks/Seizure.txt | |
| 42 | Stroke/TIA | pems_chunks/Stroke.txt | |

### Toxicology (3)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 43 | Nausea/Vomiting | pems_chunks/Nausea.txt | |
| 44 | Nerve Agents | pems_chunks/Nerve_Agents.txt | |
| 45 | Overdose/Poisoning | pems_chunks/Overdose.txt | |

### Medical (4)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 46 | Allergic Reaction | pems_chunks/Allergic_Reaction.txt | |
| 47 | Hypotension/Shock | pems_chunks/Hypotension.txt | |
| 48 | OB Emergencies | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 49 | Sepsis | pems_chunks/Sepsis.txt | |

### Trauma (6)

| # | Protocol | PEMS Chunk | Notes |
|:--:|:---|---:|:---|
| 50 | Burns Thermal | pems_chunks/Burns.txt | |
| 51 | Crush Syndrome | pems_chunks/Crush_Syndrome.txt | |
| 52 | Electrical Injuries | pems_chunks/Electrical_Injuries.txt | |
| 53 | Hemorrhage Control | pems_chunks/Hemorrhage_Control.txt | |
| 54 | Lightning Injuries | pems_chunks/PEMS2024_full.txt | No standalone chunk; search full text |
| 55 | Trauma | pems_chunks/Trauma.txt | |

---

## In Progress

Empty

---

## Review

Empty

---

## Done

Empty

---

## Blocked

| # | Protocol | Reason |
|:--:|:---|---:|
| 30 | Aortic Dissection | Converted .md file needs to be created from PEMS chunk first |

---

## Post-Audit Pipeline

| # | Task | Description | Status |
|:--:|:---|:---|:---:|
| P1 | Apply FIXABLE corrections | Fix all minor discrepancies found during audit | PENDING |
| P2 | Create Aortic Dissection protocol | Generate docs/protocols/cardiac/04_Aortic_Dissection_PROC.md from PEMS chunk | PENDING |
| P3 | Run link_drugs.py | python link_drugs.py - rebuild medication cross-references | PENDING |
| P4 | MkDocs build | mkdocs build - verify site compiles cleanly | PENDING |
| P5 | Deploy | mkdocs gh-deploy - publish the updated site | PENDING |

---

## Progress Summary

| Status | Count |
|:---|---:|
| Total | 55 |
| Done | 0 |
| Review | 0 |
| In Progress | 0 |
| Backlog | 54 |
| Blocked | 1 (Aortic Dissection) |
| Completion | 0% |

---

## Local AI Run Instructions

When starting an overnight audit session with a local model:

1. Load the skill: skill_view(name="pems-protocol-audit")
2. Read this Kanban - find first Backlog item
3. Move to In Progress by updating this file
4. Audit: read PEMS chunk + converted .md, compare for discrepancies
5. Report findings in JSON format (see skill instructions)
6. Update both this Kanban AND master_tracker.md
7. Repeat for next Backlog item

### Audit Priority Order
Batch by category: Administrative -> General -> Respiratory -> Cardiac -> Neurologic -> Toxicology -> Medical -> Trauma

Categories without standalone chunks (search full text) should be done later in each category.
