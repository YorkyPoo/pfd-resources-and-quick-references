# Agency names in clinical prose — sweep report

Owner ruling 2026-11-20: *"Don't put Poquoson OMD in Perrls."* The earlier MC sweep
(`t_c53e62ff`, `scripts/mc_wording.py`) covered protocol **table rows** only. This card
closes the prose half.

Guard: `scripts/agency_names.py`. Two independent bans, each with its own allowlist, so a
line cannot slip through by matching the other ban's exemption:

| ban | terms |
|---|---|
| OFFICE | `OMD`, `Operational Medical Director`, `Medical Director`, `medical director` |
| AGENCY | `Poquoson` |

A line is a violation if **either** ban has an unallowed hit — so `Poquoson Fire and Rescue
OMD` is still a violation: the agency phrase is exempt, the office term is not.

## Counts

| | lines naming the office/agency | clinical-prose violations |
|---|---:|---:|
| before (`main` @ 02c467a) | 741 | **27** |
| after (this branch) | 715 | **0** |

## The 27 replaced lines

| file | line | before | after |
|---|---:|---|---|
| `station-info.md` | 19 | pre-fills the page name. Submissions go to the OMD; nothing changes without their approval. | Submissions go to **Medical Control**; nothing changes without their approval. |
| `station-info.md` | 33 | your medical director govern.** | **your local protocols and Medical Control govern.** |
| `quick-refs/apgar-scoring.md` | 14 | compressions. Follow your neonatal/resuscitation protocol and the OMD's direction. | Follow your neonatal/resuscitation protocol and **Medical Control's** direction. |
| `quick-refs/burn-tbsa-estimation.md` | 14 | and transfer thresholds come from your burn protocol and the OMD** — confirm them before | come from your burn protocol and **Medical Control** |
| `quick-refs/glasgow-coma-scale.md` | 9 | depressed; disposition and airway decisions come from your protocol and your medical director. | disposition and airway decisions come from your protocol and **Medical Control**. |
| `quick-refs/glasgow-coma-scale.md` | 14 | the OMD**, not by this page. | are governed by **Poquoson Fire & Rescue protocols and Medical Control**, not by this page. |
| `protocols/administrative/01_ALS_Release_to_BLS_PROC.md` | 42 | 3. **Medical Control**: Always consult Medical Control (**Poquoson OMD**) for edge cases or when there is any concern about the appropriateness of the | Always consult **Medical Control** for edge cases … |
| `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` | 49 | • ⚠ **Medical ECOs:** For medical emergencies, issuance of an emergency custody order (ECO) for medical evaluation requires a licensed physician to pe | Early discussion with **Medical Control** … |
| `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md` | 43 | 4. **Alternate Destinations:** If approved by the Poquoson OMD / Emergency Physician, alternate destinations may be established. | If approved by **Medical Control** / Emergency Physician, alternate destinations may be established. |
| `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | 42 | • ⚠ Termination of resuscitative efforts is a **Poquoson Medical Control** decision only. | Termination of resuscitative efforts is a **Medical Control** decision only. |
| `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` | 52 | 1. ⚠ **Cautious Blood Pressure Management:** In most hypertensive emergencies, the goal is NOT to normalize blood pressure rapidly. Aggressive reducti | … should be determined by **Medical Control** based on the underlying cause. |
| `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` | 56 | 3. ⚠ **Aortic Dissection Suspicion:** If acute aortic dissection is suspected (tearing chest/back pain, pulse deficits, new neurologic deficits), imme | immediate **Medical Control** notification is critical. |
| `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` | 60 | 5. **Ischemic Stroke Consideration:** In patients with suspected acute ischemic stroke, permissive hypertension may be appropriate to maintain cerebra | Do NOT lower blood pressure without specific **Medical Control** direction. |
| `protocols/front-matter/00 - AI Formatting Guidelines.md` | 14 | * `PEMS Medical Advisory Committee`, `Regional Medical Director` ➔ **Poquoson OMD** | `PEMS Medical Advisory Committee`, `Regional Medical Director` ➔ **Medical Control** |
| `protocols/front-matter/01 - How to Read the Protocols.md` | 45 | * **Cumulative by level:** A bullet (•) at any tier implies the same standing order at every HIGHER tier (EMR→EMT→A→I→P). `MC` is never implied — each | … report it through the chain of command for **Medical Control** review. |
| `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` | 52 | 1. ⚠ **[Ipratropium](../../pharmacology/Ipratropium Bromide.md) Bromide is ONCE ONLY.** Do not administer repeat doses without consulting Poquoson OMD | Do not administer repeat doses without consulting **Medical Control**. |
| `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` | 54 | 2. **[Albuterol](../../pharmacology/Albuterol.md) is Repeat-As-Necessary.** EMTs may administer multiple treatments based on clinical response. Contin | Continuous nebulized Albuterol may be initiated for severe cases with **Medical Control** direction. |
| `protocols/respiratory/03_Respiratory_Distress_PROC.md` | 89 | - PEMS Medical Advisory Committee / Regional Medical Director ➔ Poquoson OMD | `PEMS Medical Advisory Committee / Regional Medical Director` ➔ **Medical Control** |
| `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` | 21 | - Patients less than 25 kg who cannot be safely managed with de-escalation require Poquoson Medical Control guidance | … require **Medical Control** guidance |
| `pediatric-dosing/index.md` | 3 | !!! danger "OMD Review Required" | !!! danger "**Medical Control** Review Required" |
| `pediatric-dosing/index.md` | 4 | This pediatric dosing reference is a **calculational aid only**. All doses must be verified against current Poquoson Fire & Rescue Patient Care Protoc | … approved by **Medical Control** before clinical use. |
| `procedures/Vaccination.md` | 8 | *   **OMD:** Manages vaccine handling/training, acts as supervising physician, implements quality management. | **Medical Control:** Manages vaccine handling/training, acts as supervising physician, implements quality management. |
| `procedures/Vaccination.md` | 10 | *   **Provider:** Must hold valid, unrestricted ALS certification and be individually approved by the OMD. | … individually approved by **Medical Control**. |
| `pharmacology/Ketorolac.md` | 21 | - Contact Poquoson Medical Control before administering to patients with multisystem trauma | Contact **Medical Control** before administering to patients with multisystem trauma |
| `pharmacology/Ketorolac.md` | 49 | - ⚠ **Warning:** Contact Poquoson Medical Control before administering to patients with multisystem trauma. | Contact **Medical Control** before administering to patients with multisystem trauma. |
| `training/index.md` | 80 | opens the intake form with the page name already filled in. The submission goes to the OMD; | The submission goes to **Medical Control**; |
| `training/index.md` | 97 | timed scenario drills and CE tracking need real content ownership and OMD sign-off before | … real content ownership and **Medical Control** sign-off before |

## Disposition of every remaining hit

Every line that still names the office or the agency is an explicit exemption in the
guard, with the reason recorded next to it. Grouped by reason:

| reason | lines |
|---|---:|
| department's own personnel policy manual | 299 |
| department's own administrative SOP | 254 |
| page H1 header: the document's own name | 72 |
| department's own administrative SOP: the OMD is a role in its chain of command, not a clinical attribution | 25 |
| decisions log: PENDING_OMD is a defined status label, not a clinical attribution | 13 |
| cross-reference to the document's own name ('Poquoson Protocol(s)') | 11 |
| the agency's own name in a non-clinical-attribution context | 9 |
| title page / acknowledgements / scope statement / footer | 7 |
| PENDING_OMD status label (defined in audit/level-scan/pending-protocols.yaml) | 6 |
| external link labels | 4 |
| title page / acknowledgements / scope statement / footer: the document's own attribution, not clinical prose; title page / acknowledgements / scope statement / footer | 3 |
| department's own administrative SOP: the OMD is a role in its chain of command, not a clinical attribution; department's own administrative SOP | 3 |
| provenance note naming the source agency | 2 |
| site title | 1 |
| document title | 1 |
| title page / acknowledgements / scope statement / footer: the document's own attribution, not clinical prose | 1 |
| quoted regional requirement about any EMS agency's OMD, not this agency's office | 1 |
| document footer | 1 |
| document version line | 1 |
| page title | 1 |

### Why the department's own SOPs and personnel policies are exempt

`docs/sops/**` and `docs/personnel-policies/**` are the department's own administrative
documents. There the OMD is a **role in its chain of command** — "The Fire Chief, Deputy
Fire Chief, EMS Officer and OMD will review each incident", "the OMD will be contacted and
a training plan will be approved". That is not a clinical attribution and replacing it with
"Medical Control" would be factually wrong: Medical Control is the receiving physician, the
OMD is the department's own medical director who signs certifications and sits on the QA/QI
committee. Left unchanged. If the owner wants those swept too, it is one line in the
guard's `ALLOW_OFFICE` / `ALLOW_AGENCY` tables.

### Why the front-matter Introduction is exempt

`protocols/front-matter/00 - Introduction.md` is the document's title page: agency name,
address, "Pending approval by: Poquoson Fire and Rescue Operational Medical Director (OMD)",
acknowledgements, scope statement, footer. That is the document's own identity, the same
category the card told us to leave alone.

### Why `PENDING_OMD` is exempt

`Pending OMD authorization` is a **defined status label** (`audit/level-scan/pending-protocols.yaml`),
rendered as the `PENDING` chip on rows with no PEMS citation. It is a system term, not a
clinical attribution, and it appears on the decisions log and in the `lv-note` blocks.

## Non-`.md` files

The guard scans `.md` only — the prose surface a provider reads. These non-prose files also
contain the words, and are left alone:

| file | content | disposition |
|---|---|---|
| `docs/manifest.webmanifest` | app name / description | site identity |
| `docs/robots.txt` | header comment | site identity |
| `docs/stylesheets/extra.css` | header comment, `PENDING_OMD` comment | site identity / status label |
| `docs/protocols/**/*_report.json` | conversion audit reports | internal audit artifacts, not published prose |

## Gates

Run on this branch's committed tip. See `gates.txt` for the raw output.

| gate | exit |
|---|---|
| `scripts/verify_pems_canonical.py` | 0 |
| `scripts/level_rule.py --check` | 0 |
| `scripts/mc_wording.py --check` | 0 |
| `scripts/agency_names.py --check` | 0 |
| `mkdocs build --strict` | 0 |
| `scripts/build_outstanding_decisions.py --check` | **1 — pre-existing on `main`, not caused by this branch** |

The last one fails identically on a clean worktree of `main` @ 02c467a; the two outputs are
byte-identical (`diff` empty). It is the known stale `p.247#3/#5` → `#4/#6` ETT citation in
`docs/protocols/outstanding-decisions.md`, inherited from the row-split work.

## Planted-defect check

Six defects planted in a throwaway copy of `docs/`, one per defect class; the guard caught
all six (`EXIT=1`):

| planted defect | guard |
|---|---|
| Pearl prose names the office (`consulting Poquoson OMD`) | CAUGHT |
| Pearl prose names the local Medical Control (`Poquoson Medical Control`) | CAUGHT |
| bare `OMD` in a quick-reference card | CAUGHT |
| `the OMD` in a procedure step | CAUGHT |
| agency name as a clinical attribution | CAUGHT |
| a replacement-mapping line that maps **to** the local office | CAUGHT |
