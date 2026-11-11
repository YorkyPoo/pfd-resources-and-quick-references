---
title: Training & Drills
---

# Training

<div class="trainbar" markdown="1">

**TRAINING REFERENCE ONLY — USE EMS PROTOCOLS TAB ON ACTIVE CALLS**

</div>

Tap a card to reveal the answer. Every answer points at the **ratified page** that carries
the authority — if this card and the protocol ever disagree, the protocol wins and the card
is a bug: [report it](../index.md#submit-an-update-or-correction).

!!! danger "Not a field reference"
    Nothing on this page is an authorization, a dose, or a decision rule. It exists for
    station drills and recertification study. On a call, use
    [EMS Resources](../resources/ems.md) or [Fire Resources](../resources/fire.md).

## Scale & placement cards

<details class="fc">
  <summary>What is the lowest possible Glasgow Coma Scale total, and why not zero?</summary>
  <p><strong>3.</strong> Each component's floor is 1 (E1 + V1 + M1) — there is no "0" score.
  Intubated patients are recorded as V1T so the total stays comparable.
  See <a href="../quick-refs/glasgow-coma-scale.html">Glasgow Coma Scale</a>.</p>
</details>

<details class="fc">
  <summary>Which five signs make up APGAR, and when is it recorded?</summary>
  <p>Appearance, Pulse, Grimace, Activity, Respiration — 0 to 2 each, conventionally at 1 and
  5 minutes. It never delays resuscitation.
  See <a href="../quick-refs/apgar-scoring.html">APGAR Scoring</a>.</p>
</details>

<details class="fc">
  <summary>An adult's front of trunk plus both legs equals what % TBSA?</summary>
  <p><strong>18 + 18 + 18 = 54%.</strong> Rule of Nines: head 9, each arm 9, front trunk 18,
  back trunk 18, each leg 18, perineum 1.
  See <a href="../quick-refs/burn-tbsa-estimation.html">Burn TBSA Estimation</a>.</p>
</details>

<details class="fc">
  <summary>Why does the Rule of Nines mislead on a 1-year-old?</summary>
  <p>Their head is proportionally much larger (~18% vs 9%) and legs smaller (~13.5% vs 18%) —
  the adult table over-reads the head and under-reads the legs. Lund-Browder corrects it.
  See <a href="../quick-refs/burn-tbsa-estimation.html">Burn TBSA Estimation</a>.</p>
</details>

<details class="fc">
  <summary>Where exactly does V4 go, and why place it before V3?</summary>
  <p>5th intercostal space, mid-clavicular line. V3 is defined as halfway between V2 and V4,
  so V4 has to exist first — and spaces are counted down from the second at the sternal angle.
  See <a href="../quick-refs/ecg-12-lead-placement.html">12-Lead ECG Placement</a>.</p>
</details>

<details class="fc">
  <summary>Which contiguous leads look at the inferior wall, and what does III + aVF without II mean?</summary>
  <p><strong>II, III, aVF</strong> — usually the RCA. Elevation in III and aVF <em>without</em>
  II is typically positional/lead-placement effect, not a true inferior injury.
  See <a href="../quick-refs/ecg-12-lead-placement.html">12-Lead ECG Placement</a> and
  <a href="../protocols/administrative/01_STEMI_Field_Triage_PROC.html">STEMI Field Triage</a>.</p>
</details>

## Site-navigation cards

<details class="fc">
  <summary>A patient needs a weight-based dose and you have no signal. Where do you go?</summary>
  <p><a href="../pediatric-dosing/calculator.html">Pediatric Dosing Calculator</a> — it is cached
  offline and computes as you type, no network needed.
  Zone/length-based values are on
  <a href="../pediatric-dosing/dosing-tables.html">Pediatric Dosing Tables</a>.</p>
</details>

<details class="fc">
  <summary>You spotted a wrong value on a protocol page. What do you do between calls?</summary>
  <p>Tap <strong>Report a correction on this page</strong> at the bottom of that protocol — it
  opens the intake form with the page name already filled in. The submission goes to the OMD;
  the page does not change until they approve it. See
  <a href="../station-info.html">How to Use This Site</a>.</p>
</details>

<details class="fc">
  <summary>Where is the scope legend defined, and can you read one cell by itself?</summary>
  <p><a href="../protocols/front-matter/01 - How to Read the Protocols.html">How to Read the
  Protocols</a> defines what a bullet, <code>MC</code>, and a blank cell mean across
  EMR | EMT | A | I | P. No — a single cell cannot be read apart from those rules.</p>
</details>

---

??? info "How this page is meant to grow"
    Static `<details>` cards are deliberately the first step: no JavaScript, no new dependency,
    cached by the service worker, and they work offline on a phone. Quizzes with scoring,
    timed scenario drills and CE tracking need real content ownership and OMD sign-off before
    they can claim to say anything about practice — so they stay out until that exists.
    Anything that states a clinical number should live on a ratified protocol page first and
    be *quoted* here, never invented here.
