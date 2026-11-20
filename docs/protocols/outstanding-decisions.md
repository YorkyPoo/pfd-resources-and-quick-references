---
title: Outstanding Decisions
description: Every protocol row and open question still waiting on the owner.
search:
  boost: 4
---

# Outstanding Decisions

<div class="od-intro" markdown="1">
Every row below is a decision **still waiting on you** — except the last section, which records rulings you have already made. Nothing here changes a protocol: the pages keep working exactly as they do today, and answering is optional row by row.

This page is generated from the conversion ledger (`audit/level-scan/level-rule-ledger.json`) — the reasons are copied verbatim, and the counts are computed from the lists, not typed in.

| what | how many |
|---|---:|
| Rows that need your level decision (`OWNER_REQUIRED`, marked &#9873; on the page) | **25** |
| Rows pending authorization (`PENDING`) | **18** (11 whole-page + 7 single-row) |
| Open questions on how the rules themselves should read | **33** |
| Rulings already recorded — decided, no action needed | **2** |

</div>

<h2 id="what-each-decision-means">What each decision means</h2>

<div class="od-preamble" markdown="1">
- **&#9873; `OWNER_REQUIRED`** — the protocol shows a provider level, but no PEMS 2024 row authorises that level for that action. The level you see is **kept from the page as it was published, not taken from the source**. It is marked so nobody mistakes it for a verified regional citation. Your answer decides which level the row should carry.
- **`PENDING`** — no provider level is published at all yet. Either the whole protocol is not in PEMS 2024 (Aortic Dissection & AAA comes from ODEMSA), or the agency added the row and PEMS prints no such action. The row stays `PENDING` until the operational medical director authorises a level.
- **`POLICY`** — the row is an administrative rule that PEMS prints as policy prose, not as a level-badged protocol row. Policy rows publish no provider level, so there is nothing here for you to level.
- **`+MC`** — the original page printed that level in brackets (`[A]`), meaning "at this level only with Medical Control". The chip carries the level and a second marker carries the bracket, so the notation survives.
- **`*` (asterisk)** — PEMS itself brackets that badge (`[A]` in the regional table). The asterisk means the bracket comes from the source, not from our page.
- **Why the level is "kept from the page, not the source"** — the site pages predate the conversion. Where the source does not settle a level, the conversion refuses to invent one: it keeps what the page already published and raises a flag so the uncertainty is visible instead of being silently wiped out.

</div>

<h2 id="two-kinds">Two kinds of flagged row</h2>

<div class="od-legend" markdown="1">
- <span class="od-chip od-chip-nowhere">PEMS prints this nowhere</span> — **4 rows**. No PEMS 2024 row prints the action at all (or prints it only in pieces that no single row covers). Your answer is a level of our own, or `PENDING`.
- <span class="od-chip od-chip-conflict">PEMS prints it, but the badge contradicts the row's own words</span> — **21 rows**. A PEMS row prints the action, but its printed badge conflicts with the text of that same row, or the action is spread over rows at different levels. Your answer is which one wins (and whether the row should be split).

Jump to: [PEMS prints this nowhere](#pems-prints-this-nowhere) · [PEMS prints it, badge contradicts](#pems-prints-it-badge-contradicts)

</div>

<h2 id="owner-required">1. Needs your level decision — 25 rows</h2>

Grouped by protocol page, in the order they appear in the site navigation. Each card shows the page, the row number, the level the page shows today with the &#9873; flag, the row text word for word, and the full reason it is flagged.

<h3 id="pems-prints-this-nowhere">PEMS prints this nowhere — 4 rows</h3>

#### [Pediatric Stridor](respiratory/03_Pediatric_Stridor_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-nowhere">
<p class="od-head"><span class="od-row">Row 2</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Scene Management &amp; Calm Environment / • Keep child calm - agitation worsens obstruction / • Allow parent/caregiver to hold child / • Avoid unnecessary procedures / • Minimize stimulation and stranger anxiety</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row anywhere prints scene management or keeping a child calm. The nearest rows are the universal-care steps, which do not print this action; the page&#x27;s EMT is kept and flagged.</p>

</div>
</div>

#### [Pneumothorax](respiratory/03_Pneumothorax_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-nowhere">
<p class="od-head"><span class="od-row">Row 5</span> <span class="lvl lvl-a">A</span> &#9873;</p>
<p class="od-action">Suction and Airway Management: / • Prepare suction and airway equipment. / • Be prepared for rapid airway intervention if decompensation occurs.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints equipment readiness. p.239#2 (badge EMR) prints &#x27;Provide suctioning as needed to maintain patent airway&#x27; — the act, not the preparation this row describes — so citing it would chip an action the row does not name. The page&#x27;s A is kept and flagged.</p>

</div>
</div>

#### [Upper Airway Obstruction](respiratory/03_Upper_Airway_Obstruction_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-nowhere">
<p class="od-head"><span class="od-row">Row 2</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Scene Safety / Recognition: / • Rapidly identify complete vs partial obstruction. / • Recognize universal choking sign (hands to throat). / • Determine conscious vs unconscious status.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints recognition. p.239#3 and p.239#8 print the obstruction-relief actions, not &#x27;rapidly identify complete vs partial obstruction&#x27;; citing either would chip a level for an action the row does not name. The page&#x27;s EMT is kept and flagged.</p>

</div>
</div>

#### [Trauma](trauma/09_Trauma_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-nowhere">
<p class="od-head"><span class="od-row">Row 6</span> <span class="lvl lvl-a">A</span> &#9873;</p>
<p class="od-action">Assess for shock. Refer to Shock (Hypoperfusion) protocol.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints &#x27;assess for shock and refer to the Shock protocol&#x27;. p.83#3 prints &#x27;If shock or potential for shock is present, keep the patient warm&#x27; (badge EMR) — the intervention, not the assessment/referral this row names. The page&#x27;s A is kept and flagged.</p>
<p class="od-near">Nearest PEMS row: <strong>p.83#3</strong> &mdash; <em>not cited as authority</em></p>
</div>
</div>

<h3 id="pems-prints-it-badge-contradicts">PEMS prints it, but the badge contradicts the row&#x27;s words — 21 rows</h3>

#### [Asystole / PEA](cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 8</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Apply AED / Assess cardiac rhythm every 2 minutes. If AED is advising to shock or rhythm is VF or VT (as determined by EMT-I or P), defibrillate at maximum joules (or 2 J/kg for pediatrics), then refer to Cardiac Arrest: Ventricular Fibrillation / Pulseless Ventricular Tachycardia protocol. If AED is advising no shock or rhythm is asystole or PEA (as determined by EMT-I or P), continue CPR then refer to Cardiac Arrest: Asystole / Pulseless Electrical Activity protocol.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints this bundled AED-application + rhythm-determination + defibrillation step at one level. The rows that print it split the badge from the words: p.235#4 and p.263#4 carry badge EMR while scoping rhythm determination to &#x27;EMT-I or P&#x27; in the same row, and p.63#7 badges defibrillation I while bracketing its AED clause &#x27;[EMR]&#x27;. Citing any of them would chip a level the row&#x27;s own text contradicts. The page&#x27;s EMT is kept and flagged.</p>

</div>
</div>

#### [Cardiac Arrest (Non-Traumatic)](cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md) — 2 rows

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 4</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">AED / Rhythm Assessment: / • Apply AED and assess cardiac rhythm every 2 minutes. / • Identify rhythm: V-Fib/V-Tach (shockable) or Asystole/PEA (non-shockable).</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints AED application + rhythm assessment + defibrillation at one level. p.263#4 and p.235#4 print &#x27;Apply AED / Assess cardiac rhythm every 2 minutes&#x27; at badge EMR but scope rhythm determination to &#x27;EMT-I or P&#x27; in the same row&#x27;s text; p.63#7 badges defibrillation I and brackets its AED clause &#x27;[EMR]&#x27;. The page&#x27;s EMT is kept and flagged rather than chipped off a badge the row&#x27;s own words contradict.</p>
<p class="od-near">Nearest PEMS row: <strong>p.63#7</strong> &mdash; <em>not cited as authority</em></p>
</div>
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 5</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Defibrillation - V-Fib/V-Tach Only: / • ADULT: 200 joules Biphasic / 360 joules Monophasic, or manufacturer&#x27;s recommendation / • PEDIATRIC: 2 joules/kg initial, 4 joules/kg subsequent / • After each defibrillation, perform 2 minutes of CPR, then reassess rhythm. / • Ensure optimal pad placement; consider adjustment if multiple shocks delivered without rhythm change.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> Same conflict: the only PEMS row printing defibrillation is p.63#7 (badge I, inline &#x27;[EMR]&#x27; on the AED clause). A chip of I would contradict the [EMR] token, a chip of EMT would contradict the printed badge; p.235#4/p.263#4 badge the AED step EMR but scope rhythm determination to EMT-I/P. The page&#x27;s EMT is kept and flagged.</p>
<p class="od-near">Nearest PEMS row: <strong>p.63#7</strong> &mdash; <em>not cited as authority</em></p>
</div>
</div>

#### [Cardiac Arrest (Traumatic)](cardiac/04_Cardiac_Arrest_Traumatic_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 5</span> <span class="lvl lvl-a">A</span> &#9873;</p>
<p class="od-action">PEA / VF / VT: Continue CPR / Defibrillate if indicated</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints &#x27;continue CPR / defibrillate if indicated&#x27; at one level: p.61#4 badges EMT while scoping the rhythm decision &#x27;(I / P)&#x27; in the same row, and p.63#7 badges defibrillation I with an inline &#x27;[EMR]&#x27; AED token. Both candidates contradict their own text. The page&#x27;s A is kept and flagged.</p>
<p class="od-near">Nearest PEMS row: <strong>p.61#4</strong> &mdash; <em>not cited as authority</em></p>
</div>
</div>

#### [V-Fib / Pulseless V-Tach](cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 5</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Defibrillation: 200 J Biphasic / 360 J Monophasic (Adult) / 2 J/kg initial, 4 J/kg subsequent (Ped) (AED for EMR/EMT, Manual for I/P)</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints defibrillation with an unambiguous single badge. p.63#7 badges it I but brackets its own AED clause &#x27;[EMR]&#x27; and this page&#x27;s row states &#x27;(AED for EMR/EMT, Manual for I/P)&#x27;; p.235#4/p.263#4 badge the AED/rhythm step EMR but scope rhythm determination to EMT-I/P. The page&#x27;s EMT is kept and flagged.</p>
<p class="od-near">Nearest PEMS row: <strong>p.63#7</strong> &mdash; <em>not cited as authority</em></p>
</div>
</div>

#### [Airway / Inhalation Irritants](respiratory/03_Airway_Inhalation_Irritants_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 10</span> <span class="lvl lvl-p">P</span> &#9873;</p>
<p class="od-action">Endotracheal Intubation: / • Follow Endotracheal Intubation procedure. / • ⚠ Intubation of spontaneously breathing patients without rapid sequence induction (RSI) is generally not recommended.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> PEMS prints endotracheal intubation as two age-split rows: p.247#4 (badge I) for patients 12 and older and p.247#6 (badge P) for patients under 12. This site row invokes the procedure without an age limit, so no single badge is correct; the page&#x27;s P is kept and flagged.</p>

</div>
</div>

#### [Asthma / COPD / Reactive Airway](respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md) — 2 rows

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 8</span> <span class="lvl lvl-i">I</span> &#9873;</p>
<p class="od-action">Continuous Positive Airway Pressure (CPAP): / • Consider for COPD exacerbation or severe bronchospasm with adequate mentation. / • Initiate 5-10 cm H₂O, titrate to effect. / • Contraindicated if altered mental status, vomiting, or respiratory arrest imminent.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> Conflict, recorded: the CPAP rows are p.123#3 (badge EMT) and p.239#5 (badge EMT, &#x27;Consider CPAP (PEEP: 5 cmH2O)... I/P only: Adjust PEEP to support ventilation and work of breathing, up to 10 cmH2O&#x27;). This row is the PEEP-titration row, and p.239#5&#x27;s own text reserves that titration to I/P, so an EMT chip would contradict the cited row&#x27;s words while an I chip would contradict its printed badge. The page&#x27;s I is kept and flagged.</p>

</div>
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 11</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Reassessment and Transport: / • Continuously monitor respiratory status, auscultation, and SpO₂. / • Reassess after each bronchodilator treatment. / • Expedite transport for severe or deteriorating patients.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this reassessment-and-transport bundle: reassessment is p.49#4 (badge EMR, reassess vitals every 15/5 minutes) and the transport step is p.50#11 (badge EMT). One chip cannot carry both, so the page&#x27;s EMT is kept and flagged.</p>

</div>
</div>

#### [Pediatric Stridor](respiratory/03_Pediatric_Stridor_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 5</span> <span class="lvl lvl-a">A</span> &#9873;</p>
<p class="od-action">Continuous Monitoring / • Cardiac monitor / • Pulse oximetry / • EtCO2 when available</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this monitoring bundle: continuous cardiac monitoring is p.50#10 (badge I) and SpO2/EtCO2 assessment is p.49#6 (badge EMT), while continuous ETCO2 waveform belongs to p.241#3 (badge EMT). Two levels, so the page&#x27;s A is kept and flagged.</p>

</div>
</div>

#### [Pneumothorax](respiratory/03_Pneumothorax_PROC.md) — 4 rows

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 4</span> <span class="lvl lvl-a">A</span> &#9873;</p>
<p class="od-action">Positioning and Monitoring: / • Position patient for comfort (typically supine or semi-Fowler&#x27;s). / • Establish IV/IO access. / • Continuous cardiac and pulse oximetry monitoring.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this positioning-plus-access-plus-monitoring bundle: position of comfort is p.117#1 (badge EMR), IV/IO access is p.50#9 (badge A) and continuous cardiac monitoring is p.50#10 (badge I). Three levels, so the page&#x27;s A is kept and flagged.</p>

</div>
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 12</span> <span class="lvl lvl-i">I</span> &#9873;</p>
<p class="od-action">Hemodynamic Support: / • 0.9% Sodium Chloride fluid bolus if hypotensive (SBP &lt; 90 mmHg or MAP &lt; 65). / • Consider vasopressor support if cardiogenic shock present. / • Titrate fluids to perfusion.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this haemodynamic bundle: the fluid bolus is p.113#4 (badge A) and vasopressor support is p.113#6 (badge I). Two levels, so the page&#x27;s I is kept and flagged.</p>
<p class="od-near">Nearest PEMS row: <strong>p.243#4</strong> &mdash; <em>not cited as authority</em></p>
</div>
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 13</span> <span class="lvl lvl-p">P</span> &#9873;</p>
<p class="od-action">Advanced Airway Management (if indicated): / • Prepare for or perform endotracheal intubation if respiratory failure. / • ⚠ Positive pressure ventilation (BVM/CPAP) may worsen or induce pneumothorax.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this advanced-airway bundle: adult intubation is p.247#4 (badge I), paediatric is p.247#6 (badge P) and surgical airway is p.269#0 (badge P). Three rows, two levels, so the page&#x27;s P is kept and flagged.</p>

</div>
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 15</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Close Monitoring En Route: / • Continuous reassessment en route. / • Monitor for recurrent tension pneumothorax. / • Secure catheter to prevent dislodgement.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints this en-route monitoring bundle. Reassessment after decompression is p.243#4 (badge I) while routine reassessment is p.49#4 (badge EMR); two levels, so the page&#x27;s EMT is kept and flagged.</p>

</div>
</div>

#### [Pulmonary Edema / Congestion](respiratory/03_Pulmonary_Edema_Congestion_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 9</span> <span class="lvl lvl-p">P</span> &#9873;</p>
<p class="od-action">CPAP Titration: Adjust PEEP up to 10 cmH2O to support ventilation and work of breathing</p>
<p class="od-reason"><strong>Why it is flagged:</strong> Conflict, recorded: p.239#5 prints &#x27;Consider CPAP (PEEP: 5 cmH2O) ... I/P only: Adjust PEEP to support ventilation and work of breathing, up to 10 cmH2O&#x27; at badge EMT, and p.245#4 adds &#x27;Consider titrating PEEP ... CPAP, BiPAP, and PEEP are RED DOT procedures at all EMS Certification Levels&#x27;. This row is the titration step the source&#x27;s own text reserves to I/P, so an EMT chip would contradict the cited row&#x27;s words. The page&#x27;s P is kept and flagged.</p>
<p class="od-near">Nearest PEMS row: <strong>p.239#5</strong> &mdash; <em>not cited as authority</em></p>
</div>
</div>

#### [Respiratory Distress](respiratory/03_Respiratory_Distress_PROC.md) — 2 rows

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 3</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Continuous Monitoring: / • Continuous EtCO2 monitoring to guide therapy / • Continuous pulse oximetry / • Cardiac monitoring</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this monitoring bundle: continuous cardiac monitoring is p.50#10 (badge I) and SpO2/EtCO2 assessment is p.49#6 (badge EMT). Two levels, so the page&#x27;s EMT is kept and flagged.</p>

</div>
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 16</span> <span class="lvl lvl-p">P</span> &#9873;</p>
<p class="od-action">Respiratory Failure Management: / • If apnea/agonal respirations or GCS ≤13: / • Prepare for immediate airway control / • Bag-valve-mask ventilation / • Consider advanced airway per provider level / • Transport without delay</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this respiratory-failure bundle: BVM support is p.239#7 (badge EMT), adult intubation p.239#9 (badge I) and paediatric p.239#10 (badge P). Three rows, three levels, so the page&#x27;s P is kept and flagged.</p>

</div>
</div>

#### [Smoke Inhalation](respiratory/03_Smoke_Inhalation_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 13</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Monitoring and Reassessment: / • Monitor SpO2, EtCO2, and respiratory rate continuously / • Reassess airway patency frequently; edema may progress rapidly / • Observe for signs of respiratory failure requiring immediate airway intervention</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this monitoring bundle: routine reassessment is p.49#4 (badge EMR), continuous cardiac monitoring p.50#10 (badge I) and continuous ETCO2 waveform p.241#3 (badge EMT). Multiple levels, so the page&#x27;s EMT is kept and flagged.</p>

</div>
</div>

#### [Electrical Injuries](trauma/09_Electrical_Injuries_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 7</span> <span class="lvl lvl-a">A</span> &#9873;</p>
<p class="od-action">Obtain 12-Lead ECG / Monitor rhythm continuously</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this 12-lead-plus-continuous-monitoring bundle: p.96#8 badges &#x27;Obtain and transmit a 12-Lead ECG&#x27; EMT and p.96#11 badges &#x27;Assess and continuously monitor cardiac rhythm&#x27; I. Two levels, so the page&#x27;s A is kept and flagged rather than chipped off one row that would contradict the other.</p>
<p class="od-near">Nearest PEMS row: <strong>p.96#11</strong> &mdash; <em>not cited as authority</em></p>
</div>
</div>

#### [Lightning Injuries](trauma/09_Lightning_Injuries_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 7</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Obtain and transmit a 12-Lead ECG / Monitor rhythm.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No single PEMS 2024 row prints this 12-lead-plus-monitoring bundle: p.96#8 badges &#x27;Obtain and transmit a 12-Lead ECG&#x27; EMT and p.96#11 badges &#x27;Assess and continuously monitor cardiac rhythm&#x27; I. Two levels, so the page&#x27;s EMT is kept and flagged.</p>
<p class="od-near">Nearest PEMS row: <strong>p.96#8</strong> &mdash; <em>not cited as authority</em></p>
</div>
</div>

#### [Trauma](trauma/09_Trauma_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 2</span> <span class="lvl lvl-emt">EMT</span> &#9873;</p>
<p class="od-action">Ensure scene safety. Extricate/move patient to safety if necessary.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> No PEMS 2024 row prints scene safety plus extrication/movement to safety. p.49#1 prints scene safety/PPE (badge EMR) but not extrication; p.91#7 prints extrication from entrapment (badge EMT) but not scene safety. Two rows, two levels, so the page&#x27;s EMT is kept and flagged.</p>

</div>
</div>

#### [Neonatal Resuscitation](../procedures/Neonatal_Resuscitation.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-conflict">
<p class="od-head"><span class="od-row">Row 5</span> <span class="lvl lvl-p">P</span> &#9873;</p>
<p class="od-action">Obtain IV/IO access, administer Epinephrine 0.01 mg/kg (0.1 mg/mL). Repeat q3-5 mins.</p>
<p class="od-reason"><strong>Why it is flagged:</strong> The row bundles two actions printed on two PEMS rows at two different levels: &quot;Obtain IV/IO access if not already obtained.&quot; (p.261#10, badge A) and &quot;Administer: Epinephrine (Adrenaline) 0.01mg/kg (0.1mg/mL) IV/IO&quot; (p.261#12, badge I). One chip cannot carry both; the level this page published (P) is kept and flagged.</p>

</div>
</div>

<h2 id="pending">2. Pending authorization — 18 rows</h2>

**11 whole-page rows** — a protocol that is not in PEMS 2024 at all. **3 clinical agency additions** — a row the agency wrote on a page that is otherwise PEMS-cited. **4 administrative rules** — a policy row no PEMS administrative policy prints.

<p class="od-pagenote">The brief for this page said "14 PENDING rows" (11 + 3). The ledger records 7 single-row PENDING entries: 3 clinical agency additions plus 4 administrative rules. Both are listed below, so the number you see here is 18 — derived from the ledger, not from the brief. The 4 administrative rules are decided together with the Batch 6 administrative ruling (see the open questions).</p>

<h3 id="pending-whole-page">Whole page not in PEMS 2024 — 11 rows</h3>

#### [Aortic Dissection & AAA](cardiac/04b_Aortic_Dissection_AAA_PROC.md) — 11 rows

<div class="od-page-block">
<p class="od-pagenote"><strong>Note you will see on the page:</strong> Pending OMD Authorization — this protocol is sourced from ODEMSA Regional Patient Care Protocols, Section 2.5, Revised 06/2015. PEMS 2024 does not publish this protocol. Levels below are carried from the agency&#x27;s existing page and are not verified against a regional source.</p>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 1</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Scene Safety / Initial Assessment: / • Follow the Universal Patient Care / Initial Patient Contact protocol. / • Perform general patient management.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>EMR</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 2</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Airway / Respiratory Management: / • Support life-threatening problems associated with airway, breathing, and circulation. / • If respiratory distress, refer to Airway Management and Ventilatory Support procedure and the Respiratory Distress protocol. / • Assess SpO2.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>EMR</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 3</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Oxygen Administration: / • Administer oxygen to maintain SpO2 94-99%.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>EMR</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 4</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Vital Signs / 12-Lead ECG: / • Obtain VS in both arms and assess distal pulses. / • Place patient on monitor and obtain (BLS) / interpret (ALS) 12-lead ECG. / • Refer to the Chest Pain / ACS protocol as needed. / • DO NOT administer Aspirin if acute MI is present in conjunction with suspected AAA or aortic dissection.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>EMR</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 5</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Glucose Assessment: / • Check blood glucose level. / • Refer to the Hyperglycemia / Hypoglycemia protocol if indicated.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>EMT</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 6</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">IV/IO Access: / • Establish two IV of normal saline and titrate to a systolic B/P &gt; 90 mmHg. / • Do not delay transport to establish second IV. / • Refer to Intraosseous Access procedure if IV access is difficult.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>A</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 7</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Pain Management: / • Administer Fentanyl 1 mcg/kg IN/IV/IM or Morphine Sulfate 2.5-5.0 mg IV/IM as needed, per the Pain Control protocol. / • Confirm all &quot;Rights&quot; prior to administration (Right patient, medication, dose, route, time).</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>I</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 8</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Nausea Management: / • Administer Ondansetron (Zofran) 0.1 mg/kg slow IVP as needed per the Nausea and Vomiting protocol.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>I</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 9</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Hypotension Management - Vasopressors: / • Consider Norepinephrine (Levophed) Infusion 0.1-0.5 mcg/kg/minute for hypotension. / • Titrate to systolic B/P &gt; 90 mmHg. / • Refer to Levophed Dosing Chart below. / • Administer vasopressors through the largest, most proximal IV site available (AC or higher preferable) or IO. Verify patency prior to initiating infusion and monitor closely for signs of extravasation.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>I</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 10</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Transport: / • Transport and perform ongoing assessment as indicated. / • Do not delay transport for any reason if possible; interventions should be done enroute to appropriate facility.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>EMR</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 11</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Medical Control Contact: / • Contact Medical Control for guidance as needed.</p>
<p class="od-reason"><strong>Why:</strong> this protocol is not published in PEMS 2024; its source prints no PEMS row to cite, so the level is not verified against a regional source</p>

<p class="od-near">Was carried from the page as <strong>A</strong> &mdash; provenance only, not a citation.</p>
</div>
</div>

<h3 id="pending-agency">Clinical agency additions — 3 rows</h3>

#### [Burns (Thermal)](trauma/09_Burns_Thermal_PROC.md) — 1 row

<div class="od-page-block">
<p class="od-pagenote"><strong>Note you will see on the page:</strong> PENDING — row 6: PEMS 2024 prints the HF calcium treatment only in the Burns protocol&#x27;s PEARLS (p.87-88 prose), not as a level-badged row, so no provider level is published for it. Pending OMD authorization — no provider level applies until the OMD authorizes it. See audit/level-scan/pending-protocols.yaml and audit/level-scan/level-rule-ledger.md.</p>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 6</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Hydrofluoric Acid (HF) Burns with Hypotension: Administer Calcium Chloride 1 g IV/IO over 3 mins (Repeat in 5 mins PRN).</p>
<p class="od-reason"><strong>Why:</strong> Agency addition. PEMS 2024 prints &#x27;Treat hypotension with 1 g Calcium Chloride IV/IO over 3 minutes&#x27; for hydrofluoric acid burns only in the Burns protocol&#x27;s PEARLS (p.87-88 prose), not as a level-badged table row; the only table rows printing calcium chloride 1 g IV/IO over 3 minutes are p.91#5 (crush syndrome, badge [I]) and p.120#8 (CCB/BB overdose, badge I), whose indications differ. No PEMS row authorises this action&#x27;s provider level, and the page published none. Pending OMD authorization.</p>

<p class="od-near">Was carried from the page as <strong>NONE</strong> &mdash; provenance only, not a citation.</p>
</div>
</div>

#### [Stroke / TIA](neurologic/05_Stroke_TIA_PROC.md) — 2 rows

<div class="od-page-block">
<p class="od-pagenote"><strong>Note you will see on the page:</strong> PENDING — rows 8, 9: this action has no counterpart in PEMS 2024. It is an agency addition, so the level it used to show was never verified against the regional source and is not published as a level now. Every other row on this page is cited to its PEMS 2024 row. This is not the same case as a whole protocol sourced outside PEMS (e.g. Aortic Dissection, which comes from ODEMSA and is PENDING on every row): here only the row(s) named are pending, and the rest of the protocol stands on PEMS. Pending OMD authorization — no provider level applies until the OMD authorizes it. See audit/level-scan/pending-protocols.yaml and audit/level-scan/level-rule-ledger.md.</p>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 8</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Establish 18g IV in Right AC (preferred for rapid imaging)</p>
<p class="od-reason"><strong>Why:</strong> Agency addition; PEMS 2024 p.131 publishes no such action. Pending OMD authorization.</p>

<p class="od-near">Was carried from the page as <strong>I</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 9</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Call COR at the receiving facility with Name/DOB for rapid registration</p>
<p class="od-reason"><strong>Why:</strong> Agency addition; PEMS 2024 p.131 publishes no such action. Pending OMD authorization.</p>

<p class="od-near">Was carried from the page as <strong>A</strong> &mdash; provenance only, not a citation.</p>
</div>
</div>

<h3 id="pending-admin">Administrative rules PEMS does not print — 4 rows</h3>

#### [Behavioral Health Transportation](administrative/01_Behavioral_Health_Transportation_Decision_PROC.md) — 2 rows

<div class="od-page-block">
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 6</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Law Enforcement Custody: Patients in LE custody (including ECOs) or under arrest MUST have a law enforcement officer present at all times.</p>
<p class="od-reason"><strong>Why:</strong> PEMS 2024 prints this rule only as prose in the Behavioral Emergencies protocol restraint guidelines (p.73: &quot;Patients in law enforcement custody (including emergency custody orders) or under arrest must have a law enforcement officer present at all times&quot;), not as an administrative policy and not as a level-badged row. No policy and no level is published; the wording on this page is the agency policy.</p>
<p class="od-pagenote"><strong>Note on the page:</strong> PENDING — row 6: PEMS 2024 does not print this rule in any administrative policy; it appears only as prose in the Behavioral Emergencies restraint guidelines (p.73), which carries no level-badged row. No policy and no provider level is published for it. Pending OMD authorization — no provider level applies until the OMD authorizes it. See audit/level-scan/level-rule-ledger.md.</p>
<p class="od-near">Was carried from the page as <strong>EMT</strong> &mdash; provenance only, not a citation.</p>
</div>
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 7</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Restraints: If LE restraints utilized (handcuffs, flex-cuffs), LE officer SHOULD accompany the patient.</p>
<p class="od-reason"><strong>Why:</strong> PEMS 2024 prints this rule only as prose in the Behavioral Emergencies protocol restraint guidelines (p.73: &quot;If law-enforcement restraints have been utilized (for example handcuffs or flex-cuffs), a law enforcement officer should accompany the patient&quot;), not as an administrative policy and not as a level-badged row. No policy and no level is published; the wording on this page is the agency policy.</p>
<p class="od-pagenote"><strong>Note on the page:</strong> PENDING — row 7: PEMS 2024 does not print this rule in any administrative policy; it appears only as prose in the Behavioral Emergencies restraint guidelines (p.73), which carries no level-badged row. No policy and no provider level is published for it. Pending OMD authorization — no provider level applies until the OMD authorizes it. See audit/level-scan/level-rule-ledger.md.</p>
<p class="od-near">Was carried from the page as <strong>EMT</strong> &mdash; provenance only, not a citation.</p>
</div>
</div>

#### [Infant Abandonment](administrative/01_Infant_Abandonment_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 2</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Assess infant and provide medical care per these Protocols</p>
<p class="od-reason"><strong>Why:</strong> The Infant Abandonment policy (p.25) prints what to do with a surrendered infant (contact CPS or law enforcement, and transport if indicated) but no assessment or treatment step. &quot;Assess the infant and provide medical care per these Protocols&quot; is the agency page&#x27;s own instruction and is not printed in any PEMS administrative policy.</p>
<p class="od-pagenote"><strong>Note on the page:</strong> PENDING — row 2: PEMS 2024 prints no assessment or treatment step in the Infant Abandonment policy (p.25), so this instruction is the agency&#x27;s own. No policy and no provider level is published for it. Pending OMD authorization — no provider level applies until the OMD authorizes it. See audit/level-scan/level-rule-ledger.md.</p>
<p class="od-near">Was carried from the page as <strong>EMT</strong> &mdash; provenance only, not a citation.</p>
</div>
</div>

#### [Stroke Field Triage](administrative/01_Stroke_Field_Triage_PROC.md) — 1 row

<div class="od-page-block">
<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row 4</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">Immediate Life-Threats: If uncontrolled airway, cardiac arrest, etc. cannot be addressed during transport, route to the nearest ED.</p>
<p class="od-reason"><strong>Why:</strong> The Stroke Field Triage policy (p.37) prints the RACE/glucose/destination algorithm and no &quot;life threats go to the nearest ED&quot; branch. That branch is the agency page&#x27;s own addition.</p>
<p class="od-pagenote"><strong>Note on the page:</strong> PENDING — row 4: the Stroke Field Triage policy (p.37) prints no life-threat routing branch, so this one is the agency&#x27;s own. No policy and no provider level is published for it. Pending OMD authorization — no provider level applies until the OMD authorizes it. See audit/level-scan/level-rule-ledger.md.</p>
<p class="od-near">Was carried from the page as <strong>EMT</strong> &mdash; provenance only, not a citation.</p>
</div>
</div>

<h2 id="open-questions">3. Open questions about the rules — 33</h2>

These are not row-level decisions. Each one is a question about how the rule itself should read, recorded in the conversion ledger and grouped here by the batch that raised it — the batch is the topic of work, and every card opens with the ledger's own heading naming its subject.

<h3>No batch recorded <span class="od-count">9</span></h3>

<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>Post-ROSC has no row for PEMS p.59#0</strong> (&quot;Follow Universal Patient Care…&quot;, badge EMR) — missing row, not a level defect.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>p.61#4 and p.63#7 are compound rows</strong> (one badge, plus an inline level token scoping a clause). Every site row bound to them without a C2 <code>resolved_cells</code> decision is flagged OWNER_REQUIRED rather than given a chip.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>Aortic Dissection &amp; AAA (<code>04b</code>) has no PEMS 2024 protocol</strong>: its source is ODEMSA Section 2.5 (Revised 06/2015). It is converted to the 3-column chassis with every row chipped <code>PENDING</code> (Pending OMD Authorization); see PENDING_OMD above. The page must not be given a PEMS citation by any later pass.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>Aortic Dissection row 11 (Medical Control contact) is chipped <code>PENDING</code>, not <code>MC</code></strong>, because this project&#x27;s rule is one <code>PENDING</code> chip on every action row of a page with no PEMS protocol. Owner ruling needed: is <code>PENDING</code> alone correct on such a page, or should a Medical-Control row read <code>MC</code> + <code>PENDING</code> (both chips)? Nothing on the page changes until the owner rules.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong><code>05_Stroke_TIA</code> rows 8 and 9 are agency additions</strong> — PEMS 2024 p.131 prints 6 Stroke / TIA rows and neither &quot;Establish 18g IV in Right AC&quot; nor &quot;Call COR at the receiving hospital&quot; is one of them. Owner ruling 2026-11-15: they are chipped <code>PENDING</code> (Pending OMD Authorization), not given a level, and the ⚑ OWNER_REQUIRED marker is removed because PENDING supersedes it. <code>carried_from_page</code> keeps the level the page used to publish (row 8 <code>I</code>, row 9 <code>A</code>) as provenance only; see PENDING_OMD — row-level above. This is NOT the whole-page case: the rest of the Stroke page is PEMS-cited.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>Whether every OWNER_REQUIRED row should become PENDING is UNANSWERED.</strong> The owner was asked and did not rule, so the other 25 OWNER_REQUIRED rows keep their level + ⚑ flag exactly as they were. Do not convert them without a ruling.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>Respiratory pages — the OWNER_REQUIRED rows that remain after the cross-page pass.</strong> PEMS 2024 prints one respiratory protocol (p.123-124) and one inhalation-irritant protocol (p.153); the rest of these pages&#x27; content is printed in procedures (p.239, p.241, p.243, p.245, p.247, p.269) and other protocols (Burns p.87-88, Sedation p.55). Where such a procedure prints the action it is now cited (see *Cross-page citations*); where it does not, or prints it only across rows of different levels, the row keeps the level the page published with its reason in <code>row-bindings.yaml</code>.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>Site-side <code>[X]</code> brackets — RESOLVED (owner ruling 2026-11-16).</strong> The owner ruled *&quot;Add a second marker so [X] survives in the chassis&quot;*. Bracketed rows now carry the level chip plus a distinct <code>+MC</code> marker (see the <code>+MC</code> section above); <code>row-bindings.yaml</code> is the source of truth and <code>--check</code> re-derives the bracketed rows from the pre-conversion pages. A bracketed cell whose level is not the level the row now publishes, or a row that is itself a Medical Control contact, cannot carry <code>+MC</code> without changing its meaning — those rows say so explicitly under *Bracketed rows whose bracket cannot be carried* above.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">No batch recorded</span></p>
<p class="od-question"><strong>Pearl ruling 2026-11-17 — two rows still say &quot;PEMS prints this nowhere&quot;, and the reason is only half true.</strong> The BLS/ALS scope ruling cleared 11 of the 13 false &quot;prints nowhere&quot; flags, so that bucket now holds 6 rows, not the 4 the task card expected: the 4 genuinely absent rows (Pediatric Stridor r2, Pneumothorax r5, Upper Airway Obstruction r2, Sedation r5) plus Trauma r6 and Sedation r4, which that card put explicitly out of scope. Trauma r6 (&quot;assess for shock&quot;) is worth a review: p.84 PEARLS #3 prints the recognition half (&quot;Any patient who is cool/diaphoretic and tachycardic is considered to be in shock until proven otherwise&quot;) but not the &quot;refer to the Shock protocol&quot; half, so the reason&#x27;s silence claim is false while the level question stays open. Sedation r4 prints only prose (p.248 PEARLS RSI bullet, p.195 ketamine INDICATIONS) with no dose and no level. Both stay flagged until the owner rules; the number the owner reads is 6 by design, not by omission.</p>
</div>

<h3>Batch 3 <span class="od-count">2</span></h3>

<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 3</span></p>
<p class="od-question"><strong>Batch 3 — 3 row(s) lost a Medical-Control requirement the page printed.</strong> Each is now chipped at the level PEMS prints: <code>03_Airway_Inhalation_Irritants_PROC.md</code> row 8 was <code>MC</code>, now <code>A</code> (p.153#4). <code>03_Respiratory_Distress_PROC.md</code> row 6 was <code>MC</code>, now <code>EMT</code> (p.123#3). <code>03_Respiratory_Distress_PROC.md</code> row 10 was <code>MC</code>, now <code>A</code> (p.113#4). The rule is &quot;chip = the level PEMS prints&quot;, and the source grants these actions on standing order, but the owner should confirm that dropping a page-printed MC requirement is intended. Row(s) in the converted set that moved *to* MC, now matching the source&#x27;s MC row: <code>04_Chest_Pain_ACS_PROC.md</code> row 7 <code>I</code> -&gt; <code>MC</code> (p.107#9); <code>03_Airway_Inhalation_Irritants_PROC.md</code> row 12 <code>I</code> -&gt; <code>MC</code> (p.153#5); <code>03_Smoke_Inhalation_PROC.md</code> row 12 <code>I</code> -&gt; <code>MC</code> (p.153#5); <code>06_Nausea_Vomiting_PROC.md</code> row 6 <code>A</code> -&gt; <code>MC</code> (p.117#5); <code>01_STEMI_Field_Triage_PROC.md</code> row 7 <code>EMT</code> -&gt; <code>MC</code> (p.107#9). Already <code>MC</code> on the page and matching the source, so not moved (converted set, whole list): <code>04_Supraventricular_Tachycardia_PROC.md</code> row 10 (p.136#7); <code>04_Asystole_and_Pulseless_Electrical_Activity_PROC.md</code> row 12 (p.57#8); <code>04_Bradycardia_PROC.md</code> row 8 (p.104#13); <code>04_Cardiac_Arrest_Non_Traumatic_PROC.md</code> row 13 (p.57#8); <code>04_Cardiac_Arrest_Traumatic_PROC.md</code> row 11 (p.61#9); <code>04_Chest_Pain_ACS_PROC.md</code> row 13 (p.107#9); <code>04_Hypertensive_Crisis_PROC.md</code> row 7 (p.109#5); <code>04_V_Fib_Pulseless_V_Tach_PROC.md</code> row 12 (p.64#14); <code>07_Sepsis_PROC.md</code> row 6 (p.130#5); <code>07_OB_Emergencies_PROC.md</code> row 10 (p.147#4); <code>07_Hypotension_Shock_Non_Trauma_PROC.md</code> row 10 (p.114#9); <code>05_Seizure_PROC.md</code> row 7 (p.127#6); <code>03_Pulmonary_Edema_Congestion_PROC.md</code> row 13 (p.124#13); <code>09_Burns_Thermal_PROC.md</code> row 7 (p.88#9); <code>09_Crush_Syndrome_PROC.md</code> row 9 (p.91#8); <code>09_Hemorrhage_Control_PROC.md</code> row 9 (p.273#7); <code>09_Trauma_PROC.md</code> row 13 (p.84#15); <code>06_Nerve_Agents_PROC.md</code> row 7 (p.159#6); <code>02_Behavioral_Patient_Restraint_PROC.md</code> row 8 (p.72#10); <code>02_Diving_and_Drowning_Emergencies_PROC.md</code> row 7 (p.93#6); <code>02_Pain_Control_PROC.md</code> row 8 (p.78#6); <code>02_Sedation_Assisted_Non_Paralytic_PROC.md</code> row 7 (p.55#4); <code>Surgical_Airway.md</code> row 5 (p.269#6).</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 3</span></p>
<p class="od-question"><strong>Batch 3 — four rows published no level at all</strong> (Respiratory Arrest r11, r14, r15; Smoke Inhalation r8). There was nothing to keep, so each is bound to the row that prints the action: p.269#0 (Surgical Airway, already a C2 ruling), p.55#2 (Fentanyl), p.55#3 (Midazolam), p.88#8 (Hydroxocobalamin). Confirm that binding a level-less row is preferred over chipping it PENDING.</p>
</div>

<h3>Batch 4 <span class="od-count">5</span></h3>

<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 4</span></p>
<p class="od-question"><strong>Batch 4 — Burns row 6 (HF-burn calcium) is PENDING, not OWNER_REQUIRED.</strong> The page published no level at all, so there is no level to keep and flag. PEMS 2024 prints the HF calcium treatment only in the Burns protocol&#x27;s PEARLS (p.87-88 prose), not as a level-badged row; the only table rows printing calcium chloride 1 g IV/IO over 3 minutes are p.91#5 (crush syndrome, badge [I]) and p.120#8 (CCB/BB overdose, badge I), whose indications differ. Confirm PENDING is preferred over citing one of those rows across indications.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 4</span></p>
<p class="od-question"><strong>Batch 4 — Electrical row 7 and Lightning row 7 are OWNER_REQUIRED bundles.</strong> Each row prints a 12-lead ECG (p.96#8, badge EMT) and continuous rhythm monitoring (p.96#11, badge I) as one action. One chip cannot carry both without over- or under-granting one half; the page levels (A and EMT) are kept and flagged. Owner to decide whether to split the rows or accept one level.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 4</span></p>
<p class="od-question"><strong>Batch 4 — Trauma row 2 (scene safety + extrication) and row 6 (assess shock / refer to Shock protocol) are OWNER_REQUIRED.</strong> No PEMS row prints either bundle: scene safety is p.49#1 (EMR) and extrication is p.91#7 (EMT); the shock row p.83#3 prints &quot;keep the patient warm&quot; (EMR), not the assessment/referral the page names. The page levels (EMT and A) are kept and flagged.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 4</span></p>
<p class="od-question"><strong>Batch 4 — Crush rows 4-5 carry <code>+MC</code> from brackets added on the level-scan branch.</strong> The [A]/[I] notation was added by ef540f9 after the branch base 768ad68, so this page&#x27;s pre-conversion bracket set is recorded as <code>base_rev: cf8af7a</code> in <code>exceptions.yaml</code>. Confirm the branch-added brackets are the owner&#x27;s intended notation and not a scanner artifact.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 4</span></p>
<p class="od-question"><strong>Batch 4 — three cross-page citations reach procedures.</strong> Hemorrhage rows 8-9 cite the Tourniquet Application procedure (p.273#6 EMR, p.273#7 MC) and Trauma row 7 cites Universal Patient Care (p.50#9 A). Each cited row prints the action verbatim; confirm citing a procedure for a protocol-page row is intended.</p>
</div>

<h3>Batch 5 <span class="od-count">5</span></h3>

<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 5</span></p>
<p class="od-question"><strong>Batch 5 — four card premises were wrong, and the tree/source were followed.</strong> (a) <code>07_Hypotension_Shock_Non_Trauma</code> was already converted in Batch 2; its two remaining <code>sc-wrap</code> blocks are the Norepinephrine and Epinephrine DRIP CHARTS (columns: Dose | Drops per minute) — dose tables, not level matrices, with no action row to chip. They keep <code>sc-wrap</code> and are excluded from <code>TARGETS</code>. Confirm a drip chart should never be converted. (b) <code>02_Diving_and_Drowning</code> did NOT need OWNER_REQUIRED: PEMS p.93#6 prints &quot;Contact Medical Control for transport destination guidance if decompression injury is suspected&quot; badged MC, so row 7 is cited, not flagged. (c) <code>02_Behavioral_Patient_Restraint</code> is not admin-policy-only: PEMS p.71#2 prints &quot;Restrain patient by least restrictive means necessary. Refer to administrative policy Patient Restraint.&quot; at EMR and p.71#4 prints de-escalation at EMR, so both are cited from the protocol row. (d) the general/ scope is 6 pages, not 6-plus-medical: <code>grep</code> is the source.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 5</span></p>
<p class="od-question"><strong>Batch 5 — Pain Control rows 6 and 7 now print <code>A</code> + <code>*</code> (PEMS <code>[A]</code> bracket), down from the <code>I</code> the page published.</strong> p.77#5 is the only row that prints fentanyl/morphine and PEMS brackets its badge: AEMT, with agency training documentation and Medical Control written authorisation. The one-chip chassis cannot reproduce a bracket, so the asterisk note carries it. Owner to confirm that the analgesia ladder is A+MC in PEMS and not I.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 5</span></p>
<p class="od-question"><strong>Batch 5 — Sedation: pre-intubation sedation has no PEMS row (OWNER_REQUIRED, row 4).</strong> p.55 is &quot;Sedation Post Advanced Airway&quot;; p.123#4 states outright that &quot;RSI is not addressed in PEMS regional protocols – refer to agency specific protocols for guidance&quot;. The alignment had bound the row to the post-airway midazolam row; the binding now overrides that. Owner to say whether pre-intubation ketamine/midazolam is agency-specific (and should be PENDING like other agency additions) rather than I.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 5</span></p>
<p class="od-question"><strong>Batch 5 — Sedation row 5 (post-intubation KETAMINE) keeps <code>P</code>, flagged OWNER_REQUIRED.</strong> Post-intubation sedation is printed at I (p.55#2 fentanyl, p.55#3 midazolam) but ketamine is printed in exactly one PEMS 2024 row — p.72#9, behavioural restraint, badge P — so no row authorises ketamine *as a sedative*. The C2 adjudication would have levelled it I (the class level, on a row that does not name the drug); the page level P is kept and flagged instead. Owner to rule: I on the class rows, or P/agency-specific.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 5</span></p>
<p class="od-question"><strong>Batch 5 — two cross-page citations reach other protocols.</strong> Sedation row 2 cites Pain Control p.77#2 (&quot;Assess and monitor blood pressure. Ensure patient is not hypotensive.&quot;, badge EMT) and row 3 cites Universal Patient Care p.50#9 (&quot;Establish IV / IO access when indicated.&quot;, badge A). Both print the site row verbatim; chip moves A -&gt; EMT (row 2) and I -&gt; A (row 3) as the source prints.</p>
</div>

<h3>Batch 6 <span class="od-count">8</span></h3>

<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — administrative pages are chipped POLICY / PENDING, not levelled.</strong> Owner ruling 2026-11-16: *&quot;Treat admin pages as policy.&quot;* All 14 administrative pages are now 3-column tables whose marker column says <code>POLICY</code> (the rule is printed in one of the 14 PEMS 2024 administrative policies) or <code>PENDING</code> (no PEMS policy prints it). No provider level is published on those pages, so the levels they used to show (mostly the cumulative EMR-through-P dot grid, which was the same re-encoding defect the conversion removed elsewhere) are gone. Every removed level is still recorded per row as <code>before.leftmost</code> above.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — three of the 14 administrative policies ARE printed with provider badges, and those badges are not republished.</strong> PEMS prints Death &amp; Criteria for Withholding Resuscitation (p.21-22), Patient Refusal (p.27-28) and Trauma Field Triage (p.43) as level-badged policy tables, not only as prose. Under the ruling those rows are chipped <code>POLICY</code> like the rest, so the badge a reader could have seen (EMT/I/MC on the Death and Refusal rows) is not on the site page. If the owner wants those three pages levelled from the policy&#x27;s own badges, that is a second ruling and a small change: the badges are in pems_table.json and every row prints its policy id here.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — the 4 administrative PENDING row(s), for the owner&#x27;s one-pass ruling.</strong> Each row below is an administrative rule that no PEMS 2024 administrative policy prints: Behavioral Health rows 6-7 (law-enforcement custody; handcuffed transport): PEMS prints the rule only as prose in the Behavioral Emergencies restraint guidelines (p.73), not in any administrative policy and not as a level-badged row. Infant Abandonment row 2 (&quot;assess infant and provide medical care&quot;): the policy prints no assessment/treatment step. Stroke Field Triage row 4 (life-threats route to nearest ED): the Stroke policy prints it nowhere. Stroke Field Triage row 1 is no longer in this set: the Pearl ruling levelled it <code>EMT</code> (p.131#4), so the administrative PENDING count is 4. Each row keeps its reason in <code>pending-protocols.yaml</code> and on the page.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — the STEMI page has one PEMS level, cited where printed.</strong> STEMI row 7 (serial ECGs every 10 minutes) is not in the STEMI Field Triage policy; it is printed verbatim as row p.107#9 of the Chest Pain protocol, badge MC, and is cited there (<code>cross_page: true</code>). It is the only level chip left on an administrative page, and the page note says why. Owner to confirm a protocol-row citation on a policy page is preferable to a PENDING chip on a rule PEMS does print.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — <code>07_Hypotension_Shock_Non_Trauma</code> needs no further conversion.</strong> The card inherited it for two remaining <code>sc-wrap</code> blocks; both are the Norepinephrine/Epinephrine DRIP CHARTS (columns: Dose | Drops per minute with a 60-drop set). They are dose tables with no action row and no provider-level column, so there is nothing to chip. The card premise (sc-wrap == unconverted level matrix) is wrong here, exactly as Batch 5 reported.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — &quot;grep -rn sc-wrap docs/ returns nothing&quot; cannot be the criterion.</strong> <code>sc-wrap</code> is the shared stylesheet wrapper for any wide table, used by ~80 non-level tables (pediatric dosing grids, COR phone lists, GCS tables, the SOP pages). Converting or deleting them would edit clinical content the task forbids touching. The check this batch enforces and reports instead: <strong>zero level matrices remain on <code>sc-wrap</code> anywhere under docs/</strong> — i.e. no table whose header is <code>| # | Action / Intervention | EMR | EMT | A | I | P |</code> still sits inside an <code>sc-wrap</code>. At Batch 6 that count was not 0: 13 <code>docs/procedures/</code> pages still carried the matrix, outside every batch&#x27;s scope and only REPORTED. Batch 7 converted those 13, so the count is 0 now and <code>--check</code> gates every one of them; the only page left outside the gate is the front-matter legend that defines the level columns and is correct as it stands.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — <code>rows_mc_required</code> = 8 is correct; the two &quot;bracketed&quot; Batch 5 rows are a DIFFERENT bracket.</strong> The 8 are page-cell brackets (<code>[X]</code> in the pre-conversion site page) carrying the <code>+MC</code> marker. Pain Control rows 6-7 carry an asterisk instead because the bracket is PEMS&#x27;s, not the page&#x27;s: pems_table.json records p.77#5 <code>badge_tokens: [&quot;[A]&quot;]</code>, so the chip is <code>A</code> plus the <code>*</code> source-bracket marker, and <code>+MC</code> (which means &quot;this page printed the level cell in brackets&quot;) would be a false statement about that row. Both conventions are derived from data, not typed: <code>*</code> from the PEMS badge token, <code>+MC</code> from row-bindings.yaml <code>mc_required</code> re-checked against the page&#x27;s base revision. No marker failed to apply.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 6</span></p>
<p class="od-question"><strong>Batch 6 — Universal Patient Care row 11 moves EMT -&gt; EMR.</strong> The page printed EMT-and-above for &quot;Refer to relevant protocols / consider contacting Medical Control&quot;; PEMS p.49#5 badges the same sentence EMR. Chip follows the source, and the move is listed under *Level moved by the source*. Its 11 row numbers are unchanged, so the 34 inbound references from other pages (none of which point at a row number or anchor) cannot break.</p>
</div>

<h3>Batch 7 <span class="od-count">4</span></h3>

<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 7</span></p>
<p class="od-question"><strong>Batch 7 — the 13 <code>docs/procedures/</code> pages are bound to the PEMS 2024 PROCEDURES section.</strong> The card listed p.231, 235, 239, 241, 243, 245, 247, 249, 263, 269, 273 as the available rows; <code>pems_table.json</code> actually carries the whole procedure section (p.231-275), and the page -&gt; PEMS page binding was derived from it (each page&#x27;s <code>pems_pages</code> in <code>exceptions.yaml</code>, title-matched, plus the row citations in <code>row-bindings.yaml</code>): CPAP p.245, Capnography p.241, Chest Decompression p.243, Endotracheal Intubation p.247, Intraosseous p.249, Medication Administration p.257-258, Nasogastric Tube p.259, Neonatal Resuscitation p.261, Spinal Motion Restriction p.267, Surgical Airway p.269, Taser Barb Removal p.271, Tourniquet p.273, Transcutaneous Pacing p.275. <code>Medical_Devices_Pumps.md</code> (2-column Device | Action) and <code>Vaccination.md</code> (prose list, no table) carry no level matrix and were left byte-identical.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 7</span></p>
<p class="od-question"><strong>Batch 7 — 15 rows move to the level PEMS prints.</strong> The rule is &quot;chip = the level PEMS prints&quot;, so the chip follows the source. 14 of these print a LOWER level (more permissive) than the page published, and owner should confirm each ladder: CPAP r6 <code>P -&gt; EMT</code> (PEEP titration); Endotracheal Intubation r4 and r10 <code>P -&gt; I</code> (adult oral intubation, analgesia/sedation: PEMS prints both inside p.247#3 and p.247#9 at badge I); Intraosseous r8 <code>P -&gt; A</code> (IO lidocaine); Medication Administration r3 and r4 <code>I -&gt; A</code> (IV and IO administration, p.257#3/#5 badge A); Nasogastric Tube r1-r6 <code>P -&gt; I</code> (the whole procedure is badge I on p.259); Neonatal Resuscitation r2 and r4 <code>EMT -&gt; EMR</code> (BVM and chest compressions, p.261#5/#9 badge EMR). The 15th moves the other way: Endotracheal Intubation r2 <code>EMT -&gt; I</code>, because the row bundles a sentence PEMS prints at I (see the bundled-row rule below) and an EMT chip would over-grant it. No row keeps a cumulative dot grid.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 7</span></p>
<p class="od-question"><strong>Batch 7 — a row that bundles more than one PEMS level takes the HIGHEST level.</strong> One rule for every bundled row: the chip is the highest (most restrictive) of the source levels the row prints, and the evidence names each sub-step level, so a lower-level sentence can never be published under a lower chip. Applied to the three bundled rows: ETT r2 <code>I</code> (C-spine sentence p.247#3 badge I, position step p.247#2 badge EMT) — the EMT over-grant the earlier draft only disclosed is now REMOVED from the page, since the chip is the higher level; ETT r6 <code>P</code> (escalation p.247#7 badge P, re-oxygenate sentence p.247#6 badge I); Neonatal r3 <code>I</code> (ECG p.261#7 badge I, EtCO2 sub-step p.261#6 badge EMT). All three are CITED rows, not OWNER_REQUIRED; each row&#x27;s <code>evidence</code> in <code>row-bindings.yaml</code> states the rule and both levels.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Batch 7</span></p>
<p class="od-question"><strong>Batch 7 — CPAP units disagree with the source, and the action text was not edited.</strong> The page reads PEEP &quot;5 cmH2O&quot; (r3) and &quot;5-15 cmH2O&quot; (r6); PEMS p.245#1 prints &quot;5 mmHg&quot; and p.245#4 extracts as &quot;titratingPEEP9%-15mmHg)&quot;. Reconciliation (mmHg vs cmH2O, and 5-15 vs 9%-15) is a clinical-text decision outside this conversion, so only the chip was bound; owner to reconcile the page wording.</p>
</div>

<h2 id="ruled">4. Already ruled — recorded decisions — 2</h2>

The owner has already answered these, so they are not waiting on you. They are published as a record: the page states the level that was decided, and the answer and the PEMS citation stay in the audit trail (`audit/level-scan/level-rulings.yaml`, `audit/level-scan/relocated-rows.yaml`).

<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Decided</span></p>
<p class="od-question"><strong>Pilot 2026-11-20 — Cold Exposure rows 6 and 9 were moved out of the action table into the page&#x27;s &quot;References &amp; Good Practice&quot; block.</strong> Both are unbadged PEMS p.67 PEARLS prose; the owner&#x27;s presentation ruling puts unbadged prose below the table instead of chipping it. The levels this page records for them (row 6 <code>EMR</code> (p.67 PEARLS #5), row 9 <code>MC</code> (p.67 PEARLS #3), Pearl ruling 2026-11-17) are stated in that block and stay in <code>level-rulings.yaml</code>; they are no longer chips, so they are no longer in this ledger.</p>
</div>
<div class="od-card od-cat-question">
<p class="od-head"><span class="od-batch">Decided</span></p>
<p class="od-question"><strong>Cold Exposure row 6 — the BLS-floor question was ASKED and ANSWERED (owner ruling 2026-11-20): <code>EMR</code>.</strong> The question recorded here on 2026-11-17 was whether the rewarming item keeps <code>EMT</code> although the page&#x27;s own BLS floor is lower: the ruling&#x27;s test reads &quot;BLS-scope -&gt; the page&#x27;s BLS floor&quot;, heat packs are a BLS skill, and the page chips a floor of <code>EMR</code> (derived from the page&#x27;s 7 level chips, in file order: EMR, EMR, EMR, EMR, EMR, EMR, EMT). The owner answered on 2026-11-20: <strong>EMR</strong> — &quot;Anyone can warm a patient, EMR. Might want to move below the table.&quot;. The item stays below the action table in the page&#x27;s &quot;References &amp; Good Practice&quot; block, and that block now states <code>EMR</code>, the page&#x27;s own derived floor. The history is kept in <code>level-rulings.yaml</code>; no open question remains for this row.</p>
</div>

<p class="od-foot">Generated from the conversion ledger by `scripts/build_outstanding_decisions.py`. Row text and reasons are the ledger's own words; this page adds no clinical content and edits no protocol page.</p>
