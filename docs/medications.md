# Medications & Calculators

Use the **search bar** at the top to quickly find specific dosages, protocols, or drug names.

---

## IV Drip Rate Calculator

<div style="background: var(--md-code-bg-color, #f5f5f5); border-radius: 8px; padding: 1.5rem; max-width: 480px; margin-bottom: 1.5rem;">

  <div style="margin-bottom: 1rem;">
    <label style="display:block; font-weight:600; margin-bottom:0.25rem;">Volume to infuse (mL)</label>
    <input id="volume" type="number" min="0" placeholder="e.g. 250" style="width:100%; padding:0.5rem; border:1px solid #ccc; border-radius:4px; font-size:1rem;">
  </div>

  <div style="margin-bottom: 1rem;">
    <label style="display:block; font-weight:600; margin-bottom:0.25rem;">Time of infusion (minutes)</label>
    <input id="time" type="number" min="1" placeholder="e.g. 60" style="width:100%; padding:0.5rem; border:1px solid #ccc; border-radius:4px; font-size:1rem;">
  </div>

  <div style="margin-bottom: 1rem;">
    <label style="display:block; font-weight:600; margin-bottom:0.25rem;">Drop Factor (gtts/mL)</label>
    <select id="dropfactor" style="width:100%; padding:0.5rem; border:1px solid #ccc; border-radius:4px; font-size:1rem;">
      <option value="10">10 gtts/mL (Macro)</option>
      <option value="15">15 gtts/mL (Macro)</option>
      <option value="20">20 gtts/mL (Macro)</option>
      <option value="60">60 gtts/mL (Micro)</option>
    </select>
  </div>

  <button onclick="calcDrip()" style="background:#c62828; color:white; border:none; padding:0.6rem 1.5rem; border-radius:4px; font-size:1rem; font-weight:600; cursor:pointer; width:100%;">Calculate Rate</button>

  <div id="drip-result" style="margin-top:1rem; font-size:1.2rem; font-weight:700; text-align:center;"></div>

</div>

<script>
function calcDrip() {
  var vol = parseFloat(document.getElementById("volume").value);
  var time = parseFloat(document.getElementById("time").value);
  var df = parseFloat(document.getElementById("dropfactor").value);
  var result = document.getElementById("drip-result");
  if (isNaN(vol) || isNaN(time) || time <= 0) {
    result.innerHTML = "<span style=color:#c62828>Please enter valid volume and time.</span>";
    return;
  }
  var rate = (vol * df) / time;
  result.innerHTML = "Drip Rate: <span style=color:#c62828>" + rate.toFixed(1) + " gtts/min</span>";
}
</script>

---

## Cardiac Arrest

| Medication | Dose | Route | Notes |
|-----------|------|-------|-------|
| **Epinephrine 1:10,000** | 1 mg | IV/IO | Every 3–5 min |
| **Amiodarone** | 300 mg (1st dose) | IV/IO push | 150 mg for 2nd dose |
| **Lidocaine** | 1–1.5 mg/kg | IV/IO | Alternative to amiodarone |
| **Sodium Bicarbonate** | 1 mEq/kg | IV/IO | Suspected hyperkalemia or TCA OD |
| **Calcium Chloride (10%)** | 1 g (10 mL) | IV/IO | Hyperkalemia, calcium-channel blocker OD |

---

## Symptomatic Bradycardia

| Medication | Dose | Route | Notes |
|-----------|------|-------|-------|
| **Atropine** | 0.5 mg | IV | Repeat q3–5 min; max 3 mg |
| **Dopamine** | 2–20 mcg/kg/min | IV infusion | Titrate to effect |
| **Epinephrine** | 2–10 mcg/min | IV infusion | Refractory bradycardia |

---

## Tachycardia

| Medication | Dose | Route | Notes |
|-----------|------|-------|-------|
| **Adenosine** | 6 mg (1st dose) | Rapid IV push | 12 mg for 2nd/3rd dose; SVT |
| **Amiodarone** | 150 mg over 10 min | IV | Stable VT with pulse |
| **Synchronized Cardioversion** | 100–200 J | — | Unstable tachycardia |

---

## Analgesia & Sedation

| Medication | Dose | Route | Notes |
|-----------|------|-------|-------|
| **Morphine** | 2–4 mg | IV/IM | Titrate; reassess pain |
| **Fentanyl** | 1–2 mcg/kg | IV/IN | Preferred in hemodynamic instability |
| **Ketamine** | 1–2 mg/kg | IV | Dissociative; airway maintained |
| **Midazolam** | 2–5 mg | IV/IM/IN | Seizures, sedation |

---

## Airway

| Medication | Dose | Route | Notes |
|-----------|------|-------|-------|
| **Succinylcholine** | 1.5 mg/kg | IV/IO | RSI paralytic; avoid in hyperkalemia |
| **Rocuronium** | 1.2 mg/kg | IV/IO | RSI alternative; reversal with sugammadex |
| **Etomidate** | 0.3 mg/kg | IV | RSI induction |
| **Ketamine** | 1–2 mg/kg | IV | RSI induction; preferred in hypotension |

---

## Allergic Reaction / Anaphylaxis

| Medication | Dose | Route | Notes |
|-----------|------|-------|-------|
| **Epinephrine 1:1,000** | 0.3–0.5 mg | IM (lateral thigh) | First-line anaphylaxis |
| **Diphenhydramine** | 25–50 mg | IV/IM | Adjunct; not first-line |
| **Methylprednisolone** | 125 mg | IV | Prevent biphasic reaction |
| **Albuterol** | 2.5 mg | Nebulized | Bronchospasm |

---

## Hypoglycemia

| Medication | Dose | Route | Notes |
|-----------|------|-------|-------|
| **Dextrose 50%** | 25 g (50 mL) | IV | BGL < 60 with AMS |
| **Glucagon** | 1 mg | IM/IN | No IV access |
| **Oral Glucose** | 15–30 g | PO | Alert patient; able to protect airway |

---

!!! warning "Protocol Authority"
    All dosages listed are reference values. **Always follow your current approved PEMS/locality protocols.** When in doubt, consult medical direction.
