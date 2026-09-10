# Pharmacology Correction Review Plan

**Status:** Review only. This document changes no clinical pages and is not a publishing authorization.

## Objective
Correct incomplete pharmacology reference pages without inferring clinical content. Each field must trace to the locality-approved Poquoson/PEMS source.

## Authority hierarchy
1. Original locality-approved Poquoson and/or PEMS protocol source.
2. Exact treatment statements in the matching approved PEMS protocol.
3. No generic drug-reference values may be added as Poquoson protocol content without explicit OMD/department approval.

## Verified source locations

| Source                             | Location                                                                                                              | Use                                   |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Original PEMS PDF                  | `D:\mindpalace\40 - areas\Paramedic\PEMS2024.pdf`                                                                     | Primary March 2024 source             |
| Searchable PEMS extraction         | `pems_chunks\PEMS2024_full.txt`                                                                                       | Evidence search and page traceability |
| Raw converted pharmacology records | `D:\mindpalace\30 - projects\Active\EMS Protocols\Poquoson Fire and Rescue Patient Care Protocols\08 - Pharmacology\` | Existing incomplete conversion source |
| Published pharmacology pages       | `docs\pharmacology\`                                                                                                  | Edit targets after approval           |

## Audit result

- 30 pharmacology pages contain placeholders.
- 107 occurrences of `Not specified in protocol` were found.
- Missing fields are primarily adult dosage, pediatric dosage, pharmacokinetics, and interactions.

## Mandatory clinical-review gates

- [ ] Capture exact supporting evidence, document title, and page number.
- [ ] Preserve route, patient group, scope/medical-control requirement, maximum dose, repeat interval, and timing exactly.
- [ ] Compare draft wording with the matching SSG treatment protocol.
- [ ] Preserve unresolved content as **Not listed in reviewed PEMS protocol source.**
- [ ] YorkyPoo reviews the proposed file diff.
- [ ] Obtain OMD/designated reviewer approval if required by department process.
- [ ] Run `mkdocs build` before any approved deployment.

---

# Phase 1A: Review Drafts Only

## Lidocaine 2% (Xylocaine)

**Target:** `docs\pharmacology\Lidocaine.md`

**Current missing fields:** Adult dosage, pediatric dosage, onset/duration, interactions.

### Verified PEMS evidence

| Source | Evidence |
| --- | --- |
| *Cardiac Arrest: V-Fib / Pulseless V-Tach*, January 2024, pages 64-65 | If amiodarone is unavailable: adult Lidocaine 1 mg/kg IV/IO slow push, maximum 100 mg; pediatric Lidocaine 1 mg/kg IV/IO slow push, maximum 50 mg. |
| *Cardiac Arrest: V-Fib / Pulseless V-Tach*, January 2024, pages 64-65 | Subsequent alternative dose: adult Lidocaine 0.5 mg/kg IV/IO slow push, maximum 100 mg; pediatric Lidocaine 1 mg/kg IV/IO slow push, maximum 50 mg. |
| *Procedures: Intraosseous Access*, March 2024, page 249 | Conscious IO pain control: adult 2% Lidocaine 1 mg/kg IO slow push, maximum 40 mg; pediatric 0.5 mg/kg IO slow push, maximum 20 mg. Allow dwell one minute, flush, and may repeat once as necessary. |

### Proposed disposition for review

| Field | Draft disposition |
| --- | --- |
| Adult dosage | Separate labeled indications: **Cardiac Arrest** and **Conscious-Patient IO Pain Control**. Preserve each exact route, maximum, and timing statement. |
| Pediatric dosage | Same indication-based structure using the exact PEMS values above. |
| Onset / duration | `Not listed in reviewed PEMS protocol source.` |
| Interactions | `Not listed in reviewed PEMS protocol source.` |

**Decision requested:** Use two indication-based subsections. **Recommended: yes.**

## Ondansetron (Zofran)

**Target:** `docs\pharmacology\Ondansetron.md`

**Current missing fields:** Adult dosage, pediatric dosage, onset/duration, interactions.

### Verified PEMS evidence

| Source | Evidence |
| --- | --- |
| *Pain Control*, January 2024, page 77 | Adult: 4 mg IV/IO slow push, IM, or PO. Pediatric patients over one year: 0.15 mg/kg IV/IO slow push, IM, or PO; maximum 4 mg. |
| *Nausea / Vomiting*, January 2024, page 117 | EMT adult option: 4 mg ODT; may repeat in 10-15 minutes as needed. ALS adult option: 4 mg IV/IO slow push, IM, or PO. Pediatric: 0.15 mg/kg IV/IO slow push, IM, or PO; maximum 4 mg; may repeat in 10-15 minutes as needed. |
| *Nausea / Vomiting*, January 2024, page 117 | IV administration is slow push: at least 30 seconds, preferably 2 minutes. Maximum total dose: adult 8 mg; pediatric 0.3 mg/kg. |
| *Nausea / Vomiting*, January 2024, page 117 | Assess QT risk with other QT-prolonging drugs, including amiodarone and haloperidol, and with prolonged QTc greater than 500 ms. |

### Proposed disposition for review

| Field | Draft disposition |
| --- | --- |
| Adult dosage | Separate **EMT** ODT and **ALS** IV/IO/IM/PO entries to preserve scope clarity; include repeat, maximum-total, and slow-push wording. |
| Pediatric dosage | 0.15 mg/kg IV/IO slow push, IM, or PO; maximum 4 mg per dose; retain repeat and total-dose constraints exactly as sourced. |
| Onset / duration | `Not listed in reviewed PEMS protocol source.` |
| Interactions | Include only the cited PEMS QT-prolongation caution and examples. |

**Decision requested:** Display EMT and ALS routes as separate entries. **Recommended: yes.**

---

# Remaining review queue

## High-acuity / first batch
Aspirin; Atropine Sulfate; Calcium Chloride; Dextrose; Diphenhydramine; Epinephrine; Etomidate; Fentanyl; Glucagon; Ipratropium Bromide; Ketamine; Ketorolac; Magnesium Sulfate; Methylprednisolone; Midazolam; Morphine Sulfate; Naloxone; Nitroglycerin; Norepinephrine; Rocuronium; Sodium Bicarbonate; Succinylcholine; Vecuronium.

## Medium-priority batch
Furosemide; Haloperidol; Hydroxocobalamin; Ziprasidone.

## Required naming check
Resolve the `Nitroglycerin.md` / `Nitroglycerine.md` duplicate naming issue before changing that drug's content or links.

# Controlled execution sequence

1. Produce side-by-side diffs for Lidocaine and Ondansetron only.
2. YorkyPoo reviews and approves each draft.
3. Apply approved edits only to those two pages.
4. Run `mkdocs build`; inspect rendering and links.
5. Commit clinical edits with a specific message.
6. Deploy only after explicit approval.
7. Continue in small review batches and finish with a final placeholder/duplicate audit.

# Completion criteria

- [ ] Every added clinical field has a cited approved source.
- [ ] Unavailable source data stays visibly unresolved; it is never guessed.
- [ ] No conflicting duplicate drug pages or broken links remain.
- [ ] Final review and department approval occur before publishing.
