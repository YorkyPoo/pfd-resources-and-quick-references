# Working notes — PEMS2024 vs site audit (t_d3600e06)

## Decoding rule for PEMS level codes (PEMS2024_full.txt is flattened PDF text)
- Every PEMS step/row = `<level-token> <text>`; the level token(s) immediately BEFORE a row's text is that row's level.
  Between two rows, the tokens are `trailing(prev) leading(next)`; the leading token of the NEXT row is the one adjacent to its text.
- `[ X ]` before a row text = bracketed level X (must contact MC; levels below may not perform).
- Bare `MC` before a row text = every level must contact MC.
- Rows with NO token before the text in PEMS = no level listed (header/criteria/pearls).
- Confidence: high where the token is a bare level code; flattened text cannot confirm column position of multi-level rows. Anything decoded this way that is a blocking finding must be eyeballed in the PDF (`/root/System/mindpalace/40 - areas/Paramedic/PEMS2024.pdf`) by a human before the developer edits — no shell here, so PDF raster view was not performed.

## Severity judgement applied (state in report)
- CRITICAL: (a) level omitted/narrowed for a time-critical life-saving intervention PEMS grants at that level (epinephrine IM for EMT, vasopressor/epi infusion, pacing, pediatric epi, naloxone-level etc.), (b) site over-authorizes a level PEMS does not grant for a high-alert drug/procedure, (c) wrong drug dose/route/concentration that could injure, (d) PEMS-required MC omitted for high-alert drug, (e) omitted high-alert drug row entirely.
- MODERATE: level-only mismatch on lower-harm rows (universal-care gating, monitoring, ECG, oral/adjunct meds, bracket-shape), missing level cell on existing row for non-high-alert intervention, threshold drift that does not change action.
- MINOR: text/format/phone numbers/header differences that do not change clinical action.

## Site file list (55 protocol .md; front-matter excluded). Task brief says "41" — actual count is 55.
General(6), Respiratory(9), Neurologic(3), Trauma(6), Toxicology(3), Administrative(14), Medical(4), Cardiac(10).

## Per-protocol progress
- [x] 07 Allergic Reaction / Anaphylaxis (PEMS p.99-101)
- [x] 04 Bradycardia (PEMS p.103-105)
- [x] 04 Chest Pain ACS (PEMS p.107-108)
- [x] 04 Hypertensive Crisis (PEMS p.109)
- [x] 05 Hypoglycemia (PEMS p.111-112)
- [~] 07 Hypotension (PEMS p.113-116) — PEMS read, site not yet compared
- [~] 07 Nausea (PEMS p.117) — PEMS read, site not yet compared
- [~] 06 Overdose (PEMS p.119-122) — PEMS read, site not yet compared
- [ ] remaining 45 files

## Findings so far (provisional, to be serialized)
### 07_Allergic_Reaction_Anaphylaxis_PROC.md
F-AL-01 row1 Universal Patient Care: PEMS EMR; site EMR blank (EMT+). MODERATE (universal-care gating).
F-AL-02 row2 Stinger removal: PEMS EMT ("EMT Remove stinger if present"); site blank EMT (A,I,P). MODERATE.
F-AL-03..06 rows 3,4,5,6 (Diphenhydramine, Albuterol, Ipratropium, Methylprednisolone acute): PEMS A; site I. Ruling-confirmed still present. MODERATE.
F-AL-07 row7 Epinephrine IM anaphylaxis: PEMS EMT ("EMT Administer: ADULT: Epinephrine autoinjector..."; Pearls: "EMTs may administer intramuscular epinephrine... via color-coded or clearly marked syringe"). Site blank EMT, A+. CRITICAL (EMT blocked from epi IM).
F-AL-08 row8 IV/IO access: PEMS A ("A Obtain IV/IO access"); site I. NOT in ruling list. MODERATE.
F-AL-09 row9 fluid bolus: PEMS A ("A If the patient is hypotensive"); site I. NOT in ruling list. MODERATE.
F-AL-10..13 rows 10-13 (diphen, albuterol, ipratropium, methylpred IV): PEMS A; site I. Ruling-confirmed. MODERATE.
F-AL-14 MISSING ROWS: Epinephrine IV infusion adult (PEMS I, "I Maintain MAP above 65 mmHg... Epinephrine infusion 2–10 mcg/min"); pediatric epi infusion ([I] = MC required, "[ I ] Maintain age adjusted SBP ... 0.1–1 mcg/kg/min"); push-dose epinephrine adult (PEMS P, "[ I ] P ... Push dose Epinephrine 5-10 mcg IV/IO every 2-3 minutes"); MC row (PEMS MC). Site has none. CRITICAL.

### 04_Bradycardia_PROC.md
F-BR-01 row1 Universal: PEMS EMR; site EMT+. MODERATE.
F-BR-02 MISSING row "Ensure adequate oxygenation / Refer to Airway" (PEMS EMR). MODERATE.
F-BR-03 MISSING row Children/Infants unconscious+hypotensive HR<60 begin compressions (PEMS EMR). MODERATE.
F-BR-04 MISSING row "Identify and treat potentially reversible causes" (PEMS EMR). MODERATE.
F-BR-05 row (ECG) MISSING in site: PEMS "EMR EMT Obtain and transmit a 12-Lead ECG." → EMT. Site has no ECG row. MODERATE.
F-BR-06 row IV/IO access MISSING: PEMS A "Obtain IV/IO access". Site none. MODERATE.
F-BR-07 MISSING pediatric epinephrine 0.01 mg/kg IV/IO [0.1 mg/mL] q3-5min for unconscious hypotensive HR<60 kids (PEMS A). CRITICAL (life-saving drug omitted, A level).
F-BR-08 row2 monitor rhythm: PEMS I; site I,P (I ✓). NO finding — site row 2 = I (matches).
F-BR-09 row3 Atropine: PEMS I; site NO LEVEL at all (blank). MODERATE → treat as CRITICAL? Atropine is time-critical; I'd rate CRITICAL (I cannot give atropine per site). CRITICAL.
F-BR-10 row4 transcutaneous pacing: PEMS I ("I If hypotensive or in shock, initiate transcutaneous pacing"); site P only. CRITICAL (I blocked from pacing).
F-BR-11 row5 Epinephrine adult infusion: PEMS I; site blank. CRITICAL.
F-BR-12 row6 Pediatric epi infusion: PEMS [I] (MC-bracket); site blank. CRITICAL.
F-BR-13 row7 Push-dose epinephrine adult: PEMS P; site blank. CRITICAL.
F-BR-14 row8 MC: PEMS bare MC (every level must contact MC; "P MC Contact Medical Control"); site [A] at A, • at I and P; EMR/EMT blank. MODERATE (doctrine bare-MC violation; I/P standing).
F-BR-15 MINOR: pediatric MC phone numbers (CHKD COR (757) 668-8000; VCU Communications Room (804) 828-3989) absent from site.
F-BR-16 site row 3 atropine doses: ADULT 1 mg, PEDS 0.02 mg/kg, min 0.1 mg, max 0.5 mg, repeat once after 5 min — matches PEMS ✓.

### 04_Chest_Pain_ACS_PROC.md (PEMS p.107-108)
PEMS levels: Universal EMR; SpO2 maintain 94-98% EMR (refer airway); hypotensive → Hypotension EMR; 12-lead ECG within 5 min EMT; STEMI → transport EMT; Aspirin 324 mg PO chewed EMT (ADULT); Nitroglycerine 0.4 mg SL q5min up to 3 (SBP>100, MAP≥65) EMT; Monitor cardiac rhythm I; Consider analgesia I; MC contact MC (bare).
Site: Universal EMT+ (EMR blank); row2 airway/resp EMT+ (PEMS EMR); row3 glucose EMT+; row4 ECG: site A+ (PEMS EMT) → CRITICAL? (EMT blocked from 12-lead ECG — yes, must be EMT); row5 STEMI interpretation P only (PEMS: not a row in PEMS — PEARLS; no level) — ok as pearl; site row 5 "P" is a site-level authority not in PEMS table (Intermediate/Paramedic may interpret STEMI per PEMS pearl; site P-only excludes I) → MODERATE (site_narrower: PEMS Pearl says Intermediate AND Paramedic).
Site row 6 STEMI alert P only (PEMS: STEMI alert under EMT: "EMT EMT If 12-Lead ECG reads STEMI... initiate transport... Notify the receiving facility of a Pre-Hospital STEMI Alert" → EMT). Site P-only → CRITICAL? EMT denied STEMI alert/transport authority — (MODERATE→ treat as CRITICAL: time critical STEMI transport). CRITICAL.
Site row 7 serial ECG [I]: PEMS "If 12-lead indeterminate ... obtain serial ECGs ... contact MC" — PEMS puts this under MC row (bare MC). Site [I] + P. Site I bracket vs PEMS MC → bracket_shape/site_broader. MODERATE.
Site row 8 IV: I,P (PEMS: not listed in Chest Pain PEMS page) — N/A; ignore unless PEMS lists it. PEMS pearls don't list IV. → site adds scope not in PEMS: MINOR/“unverified”.
Site row 9 cardiac monitoring: P only; PEMS row I "Monitor cardiac rhythm" → site_narrower MODERATE (I blocked).
Site row 10 Aspirin: I,P (A-level? site I ✓? PEMS EMT) → site_narrower: EMT excluded from aspirin → CRITICAL (EMT is PEMS-authorized aspirin; site I+). Dose: site has NO dose (PEMS ADULT 324 mg PO chewed) → CRITICAL (missing dose).
Site row 11 Nitroglycerin: P only; PEMS EMT (SBP>100, MAP≥65, 0.4 mg SL q5min up to 3 doses) → site_narrower CRITICAL; site lacks dose (0.4 mg SL, repeat q5min up to 3) → CRITICAL dose omission.
Site row 12 analgesia P; PEMS I "Consider analgesia" → site_narrower MODERATE.
Site row 13 MC [A] + I/P •; PEMS bare MC → MODERATE.
Site row 14 right-sided ECG [I]: PEMS pearl. MINOR.
Pearls: nitro contraindication: PEMS "Do not administer Nitroglycerine to patients who have taken sildenafil/vardenafil/tadalafil within 48 h" — site MISSING. CRITICAL (contraindication omission).
PEMS STEMI pearl: "Any unstable patient not expected to survive transport to a PCI capable hospital should be transported to the nearest ED" — site missing: MODERATE.
PEMS ECG pearl "Record 12-Lead ECG prior to nitroglycerine" — site missing: MINOR/MODERATE.
PEMS "Maintain SpO2 94-98%" — site "Assess SpO2" (no target) — MODERATE.
PEMS Chest pain hypotension → Hypotension protocol; site omitted? site row 2 refers to respiratory; hypotension referral missing. MINOR.
PEMS "Aspirin 324 mg" and nitro "0.4 mg" — exact dose absent. CRITICAL (see above).

### 04_Hypertensive_Crisis (PEMS p.109)
PEMS: criteria SBP>240 and/or DBP>120; chronic HTN sudden increase. Universal EMR; stroke→Stroke EMR; chest pain → Chest pain EMR; resp distress → airway/respiratory EMR; glucose → Hypo/Hyper EMR; MC contact (MC bare). Pearls: generally unnecessary to treat; epistaxis pressure.
Site: row 1-6 levels EMT+ / A+ (site uses EMT for universal, resp etc.). Site row 2 'Primary Assessment' EMT. PEMS: EMR for the referral rows (stroke/chest pain/resp/glucose) → site_narrower for EMR (MODERATE). Site row 3 stroke: EMT+ (PEMS EMR) same. Site row 4 Cardiac assessment ECG: A+ (site) — PEMS has no ECG row here; fine (site adds scope—'obtain 12-lead ECG if available' by A+ — no PEMS basis; MINOR/verify).
Site row 7 MC: MC in all five cells ✓ (matches bare MC).
Site Pearl 1: "Specific BP targets and medications determined by Poquoson OMD" — PEMS says "generally, prehospital treatment unnecessary; monitor for deterioration". Site lacks "generally unnecessary" statement — MINOR/MODERATE.
Site lacks the epistaxis pearl — MINOR.
Site row 6 glucose — EMR blank? site: `| 6 | Glucose | | | • | • | •` -> A+; PEMS EMR → MODERATE.
Site row 5 Respiratory: EMT+ (PEMS EMR referral) → MODERATE.
Site Pearl 5 'permissive hypertension' — not in PEMS (site adds clinical advice not sourced): MINOR (unsourced clinical content) — flag for verification.

### 05_Hypoglycemia (PEMS p.111-112)
PEMS: Universal EMR; oral glucose 1 tube PO (ADULT & PEDS >1 yr) EMT; Dextrose 10% 125 mL (12.5 g) IV/IO adult; peds 5 mL/kg max 125 mL; repeat 5 min, level A; Glucagon 1 mg IM adult, peds <25 kg 0.2 mg/kg max 1 mg, repeat 10 min, level A (if unable IV); Hyperglycemia NS 1 L 250-500 mL boluses / peds 20 mL/kg up to 60 mL/kg, level A (Consider).
Site: row1 EMT+ (EMR blank) → MODERATE. Row2 oral glucose: site A+ → PEMS EMT → CRITICAL (EMT blocked from oral glucose hypoglycemia; hypoglycemia time-critical) — CRITICAL.
Row3 dextrose: site I+ → PEMS A → site_narrower (A blocked from IV dextrose) CRITICAL.
Row4 glucagon: site I+ → PEMS A → MODERATE/CRITICAL? A cannot give IM glucagon — CRITICAL (time-critical hypoglycemia).
Row5 saline hyperglycemia: site I+ → PEMS A → MODERATE.
Pearls: PEMS "Blood glucose must be assessed for any patient with AMS" — site: row1 "check blood glucose" (EMT+) ✓ minor. PEMS "If IV cannot be obtained and no response within 5-10 min, obtain IO and give dextrose" — site MISSING. MODERATE. PEMS "asymptomatic hyperglycemia does not require intervention" — site MISSING. MODERATE. PEMS CHF/ESRD caution — missing in site Pearls? Site pearls only 2 items; missing. MODERATE (fluid caution).
Glucose thresholds: site criteria: 'Symptomatic hyperglycemia greater than 300 ✓; hypoglycemia <60 ✓; newborn <72h <40 ✓. Site does not state Adult/peds criteria explicitly; OK.
Site Dextrose pearl: "Dextrose 10% is preferred over D50" — not in PEMS. Unsourced MINOR.
Site row 4 glucagon: "IM" — PEMS "IM" ✓. Site row 4 peds: "PEDIATRIC (< 25 kg): 0.2 mg/kg IM. Maximum 1 mg" ✓. Repeat 10 min — site says "Repeat dose in 10 minutes" ✓.
PEMS glucagon: "If unable to obtain IV/IO access" ✓.

## Pending from PEMS pages already read (no site compare yet)
- Hypotension (PEMS p.113-116): criteria <90 / <70 under 1 yr; levels: Universal EMR; obtain history/focused EMR; SpO2 EMR; 12-lead ECG EMT; IV access + NS 1 L / peds 20 mL/kg (A); monitor rhythm (A - "A I Assess and continuously monitor cardiac rhythm" → token before = I? Careful: "A I Assess" → leading token I → I); Norepinephrine/epi infusion (I) ; [I] ped epi; P push dose; MC.
   Note: "EMR EMT Obtain and transmit a 12-Lead ECG. EMT A Obtain IV/IO access. Administer: ... A I Assess..." — IV/fluid row leading A; ECG EMT.
- Nausea (PEMS p.117): Universal EMR; positioning/suction EMR; Hypotension ref EMR; Ondansetron 4 mg ODT EMT; IV/IM/PO 4 mg / peds 0.15 mg/kg max 4 mg EMT→A (token "EMT A Consider: ADULT: Ondansetron 4 mg IV/IO slow push... " → A); MC contact (bare MC).
   Note: site likely ok; check.
- Overdose (PEMS p.119-122): Universal EMR; remove from exposure EMR; ventilation/O2 94-98% EMR; seizure → Seizure EMR; glucose → EMT; 12-lead ECG EMT; Opiate: apneic/bradypneic Naloxone 1-2 mg IN (EMT) ; naloxone IV/IO/IM/IN 0.5–2 mg (A). Ca channel/beta blocker: CaCl 1 g IV (I); peds 20 mg/kg max 1 g; glucagon 1 mg (I); peds <25 kg glucagon 0.5 mg; peds ≥25 kg 1 mg. Organophosphate: atropine 2 mg IV/IO/IM (I); peds <40 kg 1 mg; ≥40 kg 2 mg; repeat q5min. Anticholinergic/TCA: EMR active cooling >104F; sodium bicarb 50 mEq (I), peds 1 mEq/kg max 50; repeat once 5–10 min. Cyanide: hydroxocobalamin 5 g IV over 15 min (I), peds 70 mg/kg; MC (I bare MC?): "I MC Contact Medical Control" → MC bare.
   Note PEMS typo "Atroprine".
