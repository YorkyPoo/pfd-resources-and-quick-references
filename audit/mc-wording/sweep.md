# MC wording sweep — "Contact Medical Control", never a local office

Derived by `scripts/mc_wording.py --list` over the whole `docs/` tree. An **MC row** is
a row whose level is `MC`: either a `<span class="lvl lvl-mc">MC</span>` chip, or a legacy
5-column row whose every filled level cell is `MC`.

- pages with MC rows: **28**
- MC rows total: **30**
- MC rows rewritten: **20**
- MC rows already correct before the sweep: **10**
- MC rows still bad: **0**

## Before → after (every rewritten row)

### `protocols/toxicology/06_Nerve_Agents_PROC.md` row 7

- before: `Contact Poquoson Medical Control for additional guidance and dosing instructions`
- after:  `Contact Medical Control for additional guidance and dosing instructions`

### `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` row 6

- before: `Contact **Poquoson Medical Control** regarding issuance of a Medical ECO for acute medical emergencies lacking capacity.`
- after:  `Contact **Medical Control** regarding issuance of a Medical ECO for acute medical emergencies lacking capacity.`

### `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` row 7

- before: `Contact **Poquoson Medical Control** for assistance if unsure of capacity, surrogate validity, or if patient refuses despite severe risk.`
- after:  `Contact **Medical Control** for assistance if unsure of capacity, surrogate validity, or if patient refuses despite severe risk.`

### `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` row 12

- before: `If ROSC is achieved, refer to Post Cardiac Arrest Care (ROSC) protocol.<br><br>If ROSC is not achieved, refer to Death and Criteria for Withholding Resuscitation protocol. Contact **Poquoson Medical Control** for guidance as needed. Note: Once initiated, termination of resuscitative efforts is a **Poquoson Medical Control** decision only.`
- after:  `If ROSC is achieved, refer to Post Cardiac Arrest Care (ROSC) protocol.<br><br>If ROSC is not achieved, refer to Death and Criteria for Withholding Resuscitation protocol. Contact **Medical Control** for guidance as needed. Note: Once initiated, termination of resuscitative efforts is a **Medical Control** decision only.`

### `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md` row 11

- before: `Contact Poquoson Medical Control for guidance / destination`
- after:  `Contact Medical Control for guidance / destination`

### `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` row 13

- before: `**Medical Control Contact:**<br>• Contact Poquoson OMD for guidance as needed.`
- after:  `**Medical Control Contact:**<br>• Contact Medical Control for guidance as needed.`

### `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` row 7

- before: `**Medical Control Consultation:**<br>• Contact **Poquoson Medical Control** for guidance on blood pressure management as needed.<br>• Do NOT attempt to aggressively lower blood pressure in the field without specific orders.<br>• Report all associated symptoms, vital signs, and suspected target organ involvement.`
- after:  `**Medical Control Consultation:**<br>• Contact **Medical Control** for guidance on blood pressure management as needed.<br>• Do NOT attempt to aggressively lower blood pressure in the field without specific orders.<br>• Report all associated symptoms, vital signs, and suspected target organ involvement.`

### `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md` row 10

- before: `Contact Poquoson OMD for guidance<br>Ensure 12-Lead ECG transmitted`
- after:  `Contact Medical Control for guidance<br>Ensure 12-Lead ECG transmitted`

### `protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md` row 12

- before: `Contact Poquoson Medical Control for guidance / termination of resuscitation`
- after:  `Contact Medical Control for guidance / termination of resuscitation`

### `protocols/trauma/09_Burns_Thermal_PROC.md` row 7

- before: `Contact Poquoson Medical Control if the most appropriate transport destination is unclear based on criteria.`
- after:  `Contact Medical Control if the most appropriate transport destination is unclear based on criteria.`

### `protocols/trauma/09_Crush_Syndrome_PROC.md` row 9

- before: `If it is anticipated the patient will not be able to be promptly and safely extricated, contact Poquoson Medical Control at a regional trauma center for additional resources.`
- after:  `If it is anticipated the patient will not be able to be promptly and safely extricated, contact Medical Control at a regional trauma center for additional resources.`

### `protocols/trauma/09_Hemorrhage_Control_PROC.md` row 9

- before: `Contact Poquoson Medical Control if hemorrhage cannot be controlled and transport immediately.`
- after:  `Contact Medical Control if hemorrhage cannot be controlled and transport immediately.`

### `protocols/trauma/09_Trauma_PROC.md` row 13

- before: `Contact Poquoson Medical Control for guidance and/or optimal destination determination as needed.`
- after:  `Contact Medical Control for guidance and/or optimal destination determination as needed.`

### `protocols/medical/07_Sepsis_PROC.md` row 6

- before: `Contact Poquoson Medical Control / Prehospital Sepsis Alert`
- after:  `Contact Medical Control / Prehospital Sepsis Alert`

### `protocols/neurologic/05_Seizure_PROC.md` row 7

- before: `Contact Poquoson Medical Control and initiate transport if seizing >5 mins after 2nd dose of **[Midazolam](../../pharmacology/Midazolam.md)**`
- after:  `Contact Medical Control and initiate transport if seizing >5 mins after 2nd dose of **[Midazolam](../../pharmacology/Midazolam.md)**`

### `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` row 13

- before: `Contact Poquoson Medical Control for guidance as needed`
- after:  `Contact Medical Control for guidance as needed`

### `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` row 8

- before: `Contact Poquoson Medical Control for guidance if unable to safely restrain or transport the patient.`
- after:  `Contact Medical Control for guidance if unable to safely restrain or transport the patient.`

### `protocols/general/02_Cold_Exposure_PROC.md` row 9

- before: `Contact Poquoson Medical Control prior to use of AED.`
- after:  `Contact Medical Control prior to use of AED.`

### `protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md` row 7

- before: `Contact Poquoson Medical Control for hyperbaric transport destination guidance if decompression injury is suspected.`
- after:  `Contact Medical Control for hyperbaric transport destination guidance if decompression injury is suspected.`

### `protocols/general/02_Pain_Control_PROC.md` row 8

- before: `If unable to adequately control pain or safely and humanely extricate/transport a stable patient, contact Poquoson Medical Control for guidance.`
- after:  `If unable to adequately control pain or safely and humanely extricate/transport a stable patient, contact Medical Control for guidance.`

## MC rows after the sweep (all 30, unchanged or rewritten)

- `protocols/toxicology/06_Nerve_Agents_PROC.md` row 7: Contact Medical Control for additional guidance and dosing instructions
- `protocols/administrative/01_ALS_Release_to_BLS_PROC.md` row 5: Medical Control: Contact Medical Control when there is a concern of the appropriateness of the release.
- `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` row 6: Contact Medical Control regarding issuance of a Medical ECO for acute medical emergencies lacking capacity.
- `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` row 7: Contact Medical Control for assistance if unsure of capacity, surrogate validity, or if patient refuses despite severe risk.
- `protocols/administrative/01_Trauma_Field_Triage_PROC.md` row 5: Mechanism-Only Routing: If patient meets mechanism criteria but NOT physiologic/anatomic criteria, contact Medical Control to determine destination.
- `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` row 12: If ROSC is achieved, refer to Post Cardiac Arrest Care (ROSC) protocol. /  / If ROSC is not achieved, refer to Death and Criteria for Withholding Resuscitation 
- `protocols/cardiac/04_Bradycardia_PROC.md` row 8: Contact Medical Control for guidance as needed / Consider contacting Medical Control at a pediatric specialty center (VCU CHoR or CHKD) for children and infants
- `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md` row 13: Termination of Resuscitation (TOR): / Contact Medical Control to request TOR if ALL criteria met: / • Arrest was not witnessed by EMS / • After 20 minutes of co
- `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md` row 11: Contact Medical Control for guidance / destination
- `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` row 13: Medical Control Contact: / • Contact Medical Control for guidance as needed.
- `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` row 7: Medical Control Consultation: / • Contact Medical Control for guidance on blood pressure management as needed. / • Do NOT attempt to aggressively lower blood pr
- `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md` row 10: Contact Medical Control for guidance / Ensure 12-Lead ECG transmitted
- `protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md` row 12: Contact Medical Control for guidance / termination of resuscitation
- `protocols/trauma/09_Burns_Thermal_PROC.md` row 7: Contact Medical Control if the most appropriate transport destination is unclear based on criteria.
- `protocols/trauma/09_Crush_Syndrome_PROC.md` row 9: If it is anticipated the patient will not be able to be promptly and safely extricated, contact Medical Control at a regional trauma center for additional resou
- `protocols/trauma/09_Hemorrhage_Control_PROC.md` row 9: Contact Medical Control if hemorrhage cannot be controlled and transport immediately.
- `protocols/trauma/09_Trauma_PROC.md` row 13: Contact Medical Control for guidance and/or optimal destination determination as needed.
- `protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md` row 10: Contact Medical Control for guidance as needed.
- `protocols/medical/07_OB_Emergencies_PROC.md` row 10: Contact Medical Control for guidance, especially for complications, eclampsia seizures, or difficult deliveries.
- `protocols/medical/07_Sepsis_PROC.md` row 6: Contact Medical Control / Prehospital Sepsis Alert
- `protocols/neurologic/05_Seizure_PROC.md` row 7: Contact Medical Control and initiate transport if seizing >5 mins after 2nd dose of Midazolam
- `protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md` row 8: Sodium Bicarbonate - Chlorine Gas Exposure Only: / • Adult: 2 mL diluted with 2 mL 0.9% Sodium chloride, nebulized (ONCE only) / • Pediatric: 2 mL diluted with 
- `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` row 13: Contact Medical Control for guidance as needed
- `protocols/respiratory/03_Respiratory_Distress_PROC.md` row 6: CPAP (Continuous Positive Airway Pressure): / • Indications: Adults with respiratory distress due to pulmonary edema, infection, or near-drowning / • Initial Se
- `protocols/respiratory/03_Respiratory_Distress_PROC.md` row 10: Fluid Administration: / • 0.9% Sodium Chloride or appropriate fluid as clinically indicated / • Monitor for signs of fluid overload in CHF patients
- `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` row 8: Contact Medical Control for guidance if unable to safely restrain or transport the patient.
- `protocols/general/02_Cold_Exposure_PROC.md` row 9: Contact Medical Control prior to use of AED.
- `protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md` row 7: Contact Medical Control for hyperbaric transport destination guidance if decompression injury is suspected.
- `protocols/general/02_Pain_Control_PROC.md` row 8: If unable to adequately control pain or safely and humanely extricate/transport a stable patient, contact Medical Control for guidance.
- `procedures/Surgical_Airway.md` row 5: Contact Medical Control and transport to closest ED.

## Non-MC rows that mention the OMD — REPORTED, NOT TOUCHED

9 row(s). The level shown is the row's own level; the owner decides
whether these should also be reworded.

- `protocols/toxicology/06_Nausea_Vomiting_PROC.md` row 6 — level **A** — Contact Poquoson Medical Control for additional doses or orders
- `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` row 7 — level **I** — Extended ECG Assessment: / • If 12-Lead ECG is indeterminate or high suspicion for cardiac ischemia, obtain serial ECGs at 10-minute intervals. / • Contact Poquoson OMD for guidance.
- `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md` row 16 — level **I** — If unsuccessful after two attempts, contact Poquoson OMD
- `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md` row 11 — level **A** — Medical Control Contact: / • Contact Poquoson OMD for guidance as needed.
- `protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md` row 12 — level **I** — Medical Control Contact: / • Contact Poquoson OMD for guidance as needed. / • Report agent exposure, interventions performed, and patient status.
- `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` row 3 — level **EMT** — Albuterol Sulfate (Beta-Agonist): / • Adult & Pediatric: 3 mL of 0.083% solution via nebulizer. / • Repeat as necessary based on clinical response. / • May be administered continuously in severe cases
- `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` row 4 — level **EMT** — Ipratropium Bromide (Anticholinergic): / • Adult & Pediatric: 3 mL of 0.02% solution via nebulizer. / • ⚠ ONCE ONLY – Do NOT repeat without Poquoson OMD consultation.
- `protocols/respiratory/03_Smoke_Inhalation_PROC.md` row 9 — level **I** — Hydroxocobalamin Administration: / • Administer per Poquoson OMD guidance / • Monitor for increase in blood pressure / • Inform receiving facility of administration / • Prepare for possible red/purple
- `protocols/respiratory/03_Smoke_Inhalation_PROC.md` row 12 — level **I** — Medical Control Contact: / • Contact Poquoson OMD for cyanide poisoning confirmation and specific Hydroxocobalamin dosing guidance / • Contact Regional Burn Center for significant burn injuries requir

## Prose (non-table) mentions of the OMD — REPORTED, NOT TOUCHED

57 line(s). Clinical prose is not edited without the owner's nod.

- `station-info.md:19` — pre-fills the page name. Submissions go to the OMD; nothing changes without their approval.
- `station-info.md:33` — your medical director govern.**
- `quick-refs/apgar-scoring.md:14` — compressions. Follow your neonatal/resuscitation protocol and the OMD's direction.
- `quick-refs/burn-tbsa-estimation.md:14` — and transfer thresholds come from your burn protocol and the OMD** — confirm them before
- `quick-refs/glasgow-coma-scale.md:9` — depressed; disposition and airway decisions come from your protocol and your medical director.
- `quick-refs/glasgow-coma-scale.md:14` — the OMD**, not by this page.
- `protocols/administrative/01_ALS_Release_to_BLS_PROC.md:40` — 3. **Medical Control**: Always consult Medical Control (**Poquoson OMD**) for edge cases or when there is any concern about the appropriateness of the release to BLS.
- `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md:41` — 4. **Alternate Destinations:** If approved by the Poquoson OMD / Emergency Physician, alternate destinations may be established.
- `protocols/cardiac/04_Hypertensive_Crisis_PROC.md:52` — 1. ⚠ **Cautious Blood Pressure Management:** In most hypertensive emergencies, the goal is NOT to normalize blood pressure rapidly. Aggressive reduction can precipitate cerebral, coronary, or renal hy
- `protocols/cardiac/04_Hypertensive_Crisis_PROC.md:56` — 3. ⚠ **Aortic Dissection Suspicion:** If acute aortic dissection is suspected (tearing chest/back pain, pulse deficits, new neurologic deficits), immediate **Poquoson OMD** notification is critical. T
- `protocols/cardiac/04_Hypertensive_Crisis_PROC.md:60` — 5. **Ischemic Stroke Consideration:** In patients with suspected acute ischemic stroke, permissive hypertension may be appropriate to maintain cerebral perfusion. Do NOT lower blood pressure without s
- `protocols/cardiac/04_Post_Resuscitation_Care_PROC.md:35` — <p class="lv-note">* <strong>[ ] badge in PEMS 2024</strong> — the source prints this level in brackets: agency post-affiliation training documentation on file, plus the OMD's written authorization fo
- `protocols/front-matter/00 - AI Formatting Guidelines.md:14` — * `PEMS Medical Advisory Committee`, `Regional Medical Director` ➔ **Poquoson OMD**
- `protocols/front-matter/00 - Introduction.md:6` — **Approved by:** Poquoson Fire and Rescue Operational Medical Director (OMD)
- `protocols/front-matter/00 - Introduction.md:24` — These protocols have been adopted, adapted, and approved by the Poquoson Fire and Rescue Operational Medical Director to serve the specific operational and clinical needs of our agency and the citizen
- `protocols/front-matter/00 - Introduction.md:37` — - To ensure an accountability structure for our Operational Medical Director, EMS leadership, and field providers.
- `protocols/front-matter/00 - Introduction.md:42` — These protocols apply exclusively to EMS providers operating under the medical direction of the Poquoson Fire and Rescue OMD. Providers are expected to utilize these protocols in conjunction with thei
- `protocols/front-matter/00 - Introduction.md:46` — *Document maintained by Poquoson Fire and Rescue. For questions or clarifications, contact the OMD.*
- `protocols/front-matter/01 - How to Read the Protocols.md:19` — > 2. EMS agency Operational Medical Director must provide specific written authorization, to include and/or limit, these specific skills and medications, in the provider's scope of practice. Written a
- `protocols/front-matter/01 - How to Read the Protocols.md:45` — * **Cumulative by level:** A bullet (•) at any tier implies the same standing order at every HIGHER tier (EMR→EMT→A→I→P). `MC` is never implied — each tier that requires Medical Control for a step car
- `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md:50` — 1. ⚠ **[Ipratropium](../../pharmacology/Ipratropium Bromide.md) Bromide is ONCE ONLY.** Do not administer repeat doses without consulting Poquoson OMD. Excessive anticholinergic dosing may worsen outc
- `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md:52` — 2. **[Albuterol](../../pharmacology/Albuterol.md) is Repeat-As-Necessary.** EMTs may administer multiple treatments based on clinical response. Continuous nebulized [Albuterol](../../pharmacology/Albu
- `protocols/respiratory/03_Respiratory_Distress_PROC.md:87` — - PEMS Medical Advisory Committee / Regional Medical Director ➔ Poquoson OMD
- `pediatric-dosing/index.md:3` — !!! danger "OMD Review Required"
- `pediatric-dosing/index.md:4` — This pediatric dosing reference is a **calculational aid only**. All doses must be verified against current Poquoson Fire & Rescue Patient Care Protocols and approved by the Operational Medical Direct
- `procedures/Vaccination.md:8` — *   **OMD:** Manages vaccine handling/training, acts as supervising physician, implements quality management.
- `procedures/Vaccination.md:10` — *   **Provider:** Must hold valid, unrestricted ALS certification and be individually approved by the OMD.
- `sops/special-operations/so-1300-rescue-task-force-administration.md:408` — e BPE for Fire and EMS will include, at a minimum: o Ballistic Vests — minimum rating of IIIA o Individual First Aid Kit (IFAK) o Personal Protection Equipment (PPE) Gloves o EMS equipment approved by
- `sops/ems/EMS-100-General-EMS-Guidelines.md:28` — Department basic and advanced life Revised Date: ______________ | support providers to follow the protocols to the level of their certification and training as established and approved by Avy Uurt, th
- `sops/ems/EMS-1100-QA-QI.md:36` — The QA/QI Committee shall consist of 6 members. The Operational Medical Director, the EMS Officer, and a Chief Officer shall maintain permanent positions on this committee. The 3 remaining positions s
- `sops/ems/EMS-1100-QA-QI.md:38` — The Committee shall meet every other month (January, March, May, July, September, and November) at a minimum. Additional meetings may be scheduled at the discretion of the OMD, EMS Officer, or a Chief
- `sops/ems/EMS-1300-EMS-Certifications.md:70` — - National Registry Certifications — These are optional certifications and are not required by the City of Poquoson Fire Department. They can be recertified with the same hours required for the state 
- `sops/ems/EMS-1300-EMS-Certifications.md:72` — After receiving the recertification forms from the providers, the EMS Officer will contact the OMD to have the recertification forms signed. After being signed, the forms will be kept at Fire Administ
- `sops/ems/EMS-191-Hemostatic-Agents.md:50` — Each provider must be trained to use the hemostatic agent approved by the medical director. Documentation of this training will be placed in each provider’s training file.
- `sops/ems/EMS-2000-Medication-Management-and-Pharmacy.md:24` — Purchase of routine pharmaceuticals is made through ordering from an established pharmaceutical vendor. The Department’s Supervising Practitioner (Medical Director) shall provide a copy of their curre
- `sops/ems/EMS-2000-Medication-Management-and-Pharmacy.md:31` — Items purchased from vendors are shipped to Station 1 as the Registered Location on the department’s Controlled Substance Registry (CSR) issued by the Virginia Board of Pharmacy. Employees listed on t
- `sops/ems/EMS-2100-Controlled-Substances.md:16` — Purchase of controlled substances will be completed by the EMS Chief using the Drug Enforcement Agency (DEA) Form 22° or through an established online vendor using the DEA’s Controlled Substance Order
- `sops/ems/EMS-2100-Controlled-Substances.md:22` — Items purchased from vendors are shipped to Station 1 as the Registered Location on the department’s Controlled Substance Registry (CSR) issued by the Virginia Board of Pharmacy. Employees listed on t
- `sops/ems/EMS-2100-Controlled-Substances.md:86` — If a medication is unaccounted for at any time, all narcotics pouches and storage areas must be checked to see if the item was misplaced. Check for ePCR numbers on the Medication Tracking Form to matc
- `sops/ems/EMS-400-Advanced-Life-Support-Preceptorship.md:89` — required to meet the minimum competencies and will not have a minimum time requirement for this phase. Volunteer members must still complete all precepting steps prior to 1 year. During Phase Three, t
- `sops/ems/EMS-400-Advanced-Life-Support-Preceptorship.md:119` — - During the course of the preceptorship, the trainee medic shall interact with the Preceptor, who will interact with the EMS Officer, who will interact with the Operational Medical Director. At no ti
- `sops/ems/EMS-400-Advanced-Life-Support-Preceptorship.md:129` — The Trainee shall meet with the EMS Officer to review and finalize any details of the preceptorship. At this time, the EMS Officer shall make the decision whether to allow the trainee medic to continu
- `sops/ems/EMS-400-Advanced-Life-Support-Preceptorship.md:131` — The EMS Officer shall then meet with the Operational Medical Director and make the decision whether to release the trainee medic completely or to extend the preceptorship. The Operational Medical Dire
- `sops/ems/EMS-400-Advanced-Life-Support-Preceptorship.md:137` — A Poquoson Fire/Rescue member who is a released medic or equivalent in another ALS agency may apply for reciprocal privileges as a released medic in Poquoson. This should be done in the form of a writ
- `sops/ems/EMS-400-Advanced-Life-Support-Preceptorship.md:145` — When returning to full duty from an extended absence of longer than 90 days (this includes light duty assignments) the employee must be observed in the clinical setting to ensure they remain competent
- `sops/ems/EMS-700-Failure-to-Comply-with-Regional-Protocols.md:31` — al Medical Director
- `sops/ems/EMS-700-Failure-to-Comply-with-Regional-Protocols.md:41` — The EMS Officer will notify the OMD as soon as all the report and the written incident reports have been received.
- `sops/ems/EMS-700-Failure-to-Comply-with-Regional-Protocols.md:47` — The Fire Chief, Deputy Fire Chief, EMS Officer and OMD will review each incident and may require a re-evaluation period, during which the involved personnel will not practice as the Attendant in Charg
- `sops/ems/EMS-700-Failure-to-Comply-with-Regional-Protocols.md:51` — These progress reports will be reviewed by the Fire Chief, Deputy Fire Chief, EMS Officer and the OMD and a decision will be made to continue the re-evaluation or release the employee to practice. The
- `sops/ems/EMS-700-Failure-to-Comply-with-Regional-Protocols.md:55` — Prior to disciplinary action, the employee may request, in writing, to meet with the Fire Chief, the Deputy Chief, the OMD and the EMS Officer for a formal review.
- `sops/ems/EMS-800-BLS-Preceptorship-Program.md:38` — Phase 3 (Team Leader/Probationary Release): The OMD has granted the EMS Officer the authority to release a trainee under “Probationary” status after specific minimum requirements are
- `sops/ems/EMS-800-BLS-Preceptorship-Program.md:64` — During the course of the preceptorship, the EMT shall interact with the Preceptor, who will interact with the EMS Officer, who will interact with the Operational Medical Director. At no time during th
- `sops/ems/EMS-800-BLS-Preceptorship-Program.md:68` — The EMS Officer shall meet with the Operational Medical Director and make the decision whether to release the EMT or to extend the preceptorship. The Operational Medical Director, the EMS Officer and 
- `sops/ems/EMS-800-BLS-Preceptorship-Program.md:72` — A Poquoson Fire/Rescue member who is a released EMT or equivalent in another agency may apply for reciprocal privileges as a released EMT in Poquoson. This should be done in the form of a written requ
- `sops/ems/EMS-800-BLS-Preceptorship-Program.md:82` — determined that the employee needs continuing training, the OMD will be contacted and a training plan will be approved.
- `training/index.md:80` — opens the intake form with the page name already filled in. The submission goes to the OMD;
- `training/index.md:97` — timed scenario drills and CE tracking need real content ownership and OMD sign-off before

