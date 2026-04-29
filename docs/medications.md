# Medications & Calculators

Use the search bar at the top of the screen to quickly find specific dosages or protocols.

## Advanced Drip Rate & Protocol Calculator

<style>
.calc-wrap {
  background: #141414;
  border-radius: 14px;
  padding: 22px 18px;
  max-width: 520px;
  margin: 0 auto 30px auto;
  font-family: sans-serif;
  color: #fff;
  box-shadow: 0 6px 24px rgba(0,0,0,0.5);
}
.calc-section-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #888;
  margin: 18px 0 10px 0;
  padding-bottom: 6px;
  border-bottom: 1px solid #2a2a2a;
}
.calc-field { margin-bottom: 14px; }
.calc-label { font-size: 13px; font-weight: 600; color: #aaa; margin-bottom: 5px; display: block; }
.calc-label.accent { color: #4db8ff; }
.calc-label.warm { color: #ffb84d; }
.calc-row { display: flex; gap: 0; border-radius: 8px; overflow: hidden; border: 1px solid #2e2e2e; }
.calc-input {
  flex: 2; background: #000; color: #fff; border: none;
  padding: 12px 10px; font-size: 16px; outline: none;
  text-align: right; width: 100%; transition: background 0.15s;
}
.calc-input:focus { background: #0a0a0a; }
.calc-unit {
  background: #1a1a1a; color: #888; border: none; border-left: 1px solid #2e2e2e;
  padding: 12px 10px; font-size: 13px; min-width: 64px; text-align: center;
  display: flex; align-items: center; justify-content: center;
}
.calc-select {
  flex: 1.5; background: #1a1a1a; color: #fff; border: none;
  border-left: 1px solid #2e2e2e; padding: 12px 8px; font-size: 14px;
  outline: none; cursor: pointer;
}
.calc-search {
  width: 100%; background: #000; color: #fff;
  border: 1px solid #2e2e2e; border-radius: 8px;
  padding: 12px 14px; font-size: 16px; outline: none; box-sizing: border-box;
  transition: border-color 0.2s;
}
.calc-search:focus { border-color: #4db8ff; }
.calc-proto-select {
  width: 100%; background: #000; color: #fff;
  border: 1px solid #4db8ff; border-radius: 8px;
  padding: 12px 14px; font-size: 14px; outline: none; cursor: pointer; box-sizing: border-box;
}
.drip-toolbar { display: flex; gap: 8px; flex-wrap: wrap; }
.drip-toolbar input[type="radio"] { display: none; }
.drip-toolbar label {
  flex: 1; text-align: center; background: #000;
  padding: 11px 6px; border: 1px solid #2e2e2e;
  border-radius: 8px; cursor: pointer; font-size: 15px;
  font-weight: 600; color: #666; transition: all 0.15s;
  min-width: 48px;
}
.drip-toolbar input[type="radio"]:checked + label {
  background: #4db8ff; color: #000; border-color: #4db8ff;
}
.calc-btn-row { display: flex; gap: 12px; margin: 20px 0 16px 0; }
.calc-btn {
  flex: 1; padding: 15px; border: none; border-radius: 10px;
  font-size: 16px; font-weight: 700; cursor: pointer;
  transition: transform 0.1s, filter 0.15s;
}
.calc-btn:active { transform: scale(0.97); }
.calc-btn-go { background: #4db8ff; color: #000; }
.calc-btn-go:hover { filter: brightness(1.12); }
.calc-btn-rst { background: #2e2e2e; color: #fff; }
.calc-btn-rst:hover { background: #3a3a3a; }
.out-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.out-card {
  background: #0d0d0d; border: 1px solid #2a2a2a;
  border-radius: 10px; padding: 14px; text-align: center;
}
.out-card.primary {
  grid-column: span 2;
  background: #041420; border-color: #1a496b;
}
.out-card-title { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.out-card-val {
  font-size: 26px; font-weight: 800; color: #fff;
  line-height: 1; margin-bottom: 4px;
}
.out-card.primary .out-card-val { font-size: 40px; color: #4db8ff; }
.out-card-unit { font-size: 13px; color: #555; }
#calc-err {
  background: rgba(255,82,82,0.08); color: #ff5252;
  border: 1px solid #ff5252; padding: 12px; border-radius: 8px;
  text-align: center; margin-bottom: 16px; font-weight: 600; display: none;
}
.calc-hidden { display: none; }
</style>

<div markdown="0" class="calc-wrap">

  <div class="calc-section-title">Drug Search</div>

  <div class="calc-field">
    <input list="drug-list" id="drug-search" class="calc-search" placeholder="Type to search drugs..." oninput="onDrugSearch()" />
    <datalist id="drug-list">
      <option value="Adenosine"></option>
      <option value="Albuterol"></option>
      <option value="Amiodarone"></option>
      <option value="Aspirin"></option>
      <option value="Atropine Sulfate"></option>
      <option value="Calcium Chloride"></option>
      <option value="Dextrose"></option>
      <option value="Dopamine"></option>
      <option value="Epinephrine"></option>
      <option value="Fentanyl"></option>
      <option value="Glucagon"></option>
      <option value="Ketamine"></option>
      <option value="Lidocaine"></option>
      <option value="Magnesium Sulfate"></option>
      <option value="Midazolam"></option>
      <option value="Naloxone"></option>
      <option value="Nitroglycerin"></option>
      <option value="Norepinephrine (Levophed)"></option>
      <option value="Ondansetron"></option>
      <option value="Sodium Bicarbonate"></option>
      <option value="TXA (Tranexamic Acid)"></option>
    </datalist>
  </div>

  <div class="calc-field calc-hidden" id="proto-wrapper">
    <label class="calc-label accent">Protocol Dose</label>
    <select id="proto-select" class="calc-proto-select" onchange="applyProtocol()">
      <option value="">-- Select Protocol Dose --</option>
    </select>
  </div>

  <div class="calc-section-title">Bag Setup</div>

  <div class="calc-field">
    <label class="calc-label">Drug Amount in Bag</label>
    <div class="calc-row">
      <input type="number" id="c-amount" class="calc-input" placeholder="0">
      <span class="calc-unit">mg</span>
    </div>
  </div>

  <div class="calc-field">
    <label class="calc-label">Bag Volume</label>
    <div class="calc-row">
      <input type="number" id="c-volume" class="calc-input" placeholder="0">
      <span class="calc-unit">mL</span>
    </div>
  </div>

  <div class="calc-section-title">Dose Ordered</div>

  <div class="calc-field">
    <div class="calc-row">
      <input type="number" id="c-dose" class="calc-input" placeholder="0">
      <select id="c-unit" class="calc-select" onchange="updateConditionalFields()">
        <option value="mg_hr">mg / hr</option>
        <option value="mg_min">mg / min</option>
        <option value="mcg_hr">mcg / hr</option>
        <option value="mcg_min">mcg / min</option>
        <option value="mcg_kg_min">mcg / kg / min</option>
        <option value="mg_kg_hr">mg / kg / hr</option>
        <option value="mg_dose">mg / DOSE</option>
        <option value="mcg_dose">mcg / DOSE</option>
        <option value="units_hr">units / hr</option>
        <option value="g_hr">g / hr</option>
      </select>
    </div>
  </div>

  <div class="calc-field calc-hidden" id="w-weight">
    <label class="calc-label accent">Patient Weight</label>
    <div class="calc-row">
      <input type="number" id="c-weight" class="calc-input" placeholder="0">
      <span class="calc-unit">kg</span>
    </div>
  </div>

  <div class="calc-field calc-hidden" id="w-time">
    <label class="calc-label warm">Infuse Over</label>
    <div class="calc-row">
      <input type="number" id="c-time" class="calc-input" placeholder="Time">
      <select id="c-time-unit" class="calc-select">
        <option value="min">Minutes</option>
        <option value="hr">Hours</option>
      </select>
    </div>
  </div>

  <div class="calc-section-title">Drip Set (gtts / mL)</div>

  <div class="calc-field">
    <div class="drip-toolbar">
      <input type="radio" id="d10" name="drip" value="10" checked>
      <label for="d10">10</label>
      <input type="radio" id="d15" name="drip" value="15">
      <label for="d15">15</label>
      <input type="radio" id="d20" name="drip" value="20">
      <label for="d20">20</label>
      <input type="radio" id="d60" name="drip" value="60">
      <label for="d60">60</label>
    </div>
  </div>

  <div class="calc-btn-row">
    <button class="calc-btn calc-btn-go" onclick="runCalc()">Calculate</button>
    <button class="calc-btn calc-btn-rst" onclick="resetCalc()">Reset</button>
  </div>

  <div id="calc-err">Please fill in all required fields with valid values.</div>

  <div class="out-grid">
    <div class="out-card primary">
      <div class="out-card-title">Manual Drip Rate</div>
      <div class="out-card-val" id="o-drip">--</div>
      <div class="out-card-unit">gtts / min</div>
    </div>
    <div class="out-card">
      <div class="out-card-title">Concentration</div>
      <div class="out-card-val" id="o-conc">--</div>
      <div class="out-card-unit">mg / mL</div>
    </div>
    <div class="out-card">
      <div class="out-card-title">Pump Rate</div>
      <div class="out-card-val" id="o-rate">--</div>
      <div class="out-card-unit">mL / hr</div>
    </div>
    <div class="out-card">
      <div class="out-card-title">Est. Run Time</div>
      <div class="out-card-val" id="o-time">--</div>
      <div class="out-card-unit">minutes</div>
    </div>
  </div>

</div>

<script>
var calcDb = {
  "Amiodarone": [
    {label: "Cardiac Arrest - 300 mg push", amount: 300, volume: 20, dose: 300, unit: "mg_dose", time: 1, timeUnit: "min"},
    {label: "V-Fib/V-Tach - 150 mg over 10 min", amount: 150, volume: 100, dose: 150, unit: "mg_dose", time: 10, timeUnit: "min"}
  ],
  "Epinephrine": [
    {label: "Cardiac Arrest - 1 mg push", amount: 1, volume: 10, dose: 1, unit: "mg_dose", time: 1, timeUnit: "min"},
    {label: "Anaphylaxis - 0.3 mg push", amount: 0.3, volume: 3, dose: 0.3, unit: "mg_dose", time: 1, timeUnit: "min"},
    {label: "Bradycardia Infusion - 2 mcg/min", amount: 1, volume: 250, dose: 2, unit: "mcg_min"}
  ],
  "Magnesium Sulfate": [
    {label: "Torsades - 2 g over 10 min", amount: 2000, volume: 100, dose: 2000, unit: "mg_dose", time: 10, timeUnit: "min"},
    {label: "Severe Asthma - 2 g over 20 min", amount: 2000, volume: 100, dose: 2000, unit: "mg_dose", time: 20, timeUnit: "min"},
    {label: "OB Eclampsia - 4 g over 20 min", amount: 4000, volume: 100, dose: 4000, unit: "mg_dose", time: 20, timeUnit: "min"}
  ],
  "TXA (Tranexamic Acid)": [
    {label: "Trauma Hemorrhage - 1 g over 10 min", amount: 1000, volume: 100, dose: 1000, unit: "mg_dose", time: 10, timeUnit: "min"}
  ],
  "Norepinephrine (Levophed)": [
    {label: "Septic Shock - 0.1 mcg/kg/min", amount: 4, volume: 250, dose: 0.1, unit: "mcg_kg_min"}
  ],
  "Lidocaine": [
    {label: "Maintenance Infusion - 2 mg/min", amount: 1000, volume: 250, dose: 2, unit: "mg_min"}
  ],
  "Fentanyl": [
    {label: "Pain Control - 1 mcg/kg", amount: 0.1, volume: 2, dose: 1, unit: "mcg_kg_min"}
  ],
  "Midazolam": [
    {label: "Sedation - 0.05 mg/kg", amount: 50, volume: 50, dose: 0.05, unit: "mg_kg_hr"}
  ],
  "Ketamine": [
    {label: "Dissociative - 1 mg/kg", amount: 500, volume: 10, dose: 1, unit: "mg_kg_hr"},
    {label: "Sub-dissociative - 0.3 mg/kg", amount: 500, volume: 10, dose: 0.3, unit: "mg_kg_hr"}
  ],
  "Dopamine": [
    {label: "Standard Infusion - 5 mcg/kg/min", amount: 400, volume: 250, dose: 5, unit: "mcg_kg_min"}
  ]
};

function onDrugSearch() {
  var val = document.getElementById("drug-search").value;
  var wrapper = document.getElementById("proto-wrapper");
  var sel = document.getElementById("proto-select");
  if (calcDb[val]) {
    sel.innerHTML = '<option value="">-- Select Protocol Dose --</option>';
    calcDb[val].forEach(function(p, i) {
      var opt = document.createElement("option");
      opt.value = i;
      opt.textContent = p.label;
      sel.appendChild(opt);
    });
    var manOpt = document.createElement("option");
    manOpt.value = "manual";
    manOpt.textContent = "Manual Entry";
    sel.appendChild(manOpt);
    wrapper.classList.remove("calc-hidden");
  } else {
    wrapper.classList.add("calc-hidden");
  }
}

function applyProtocol() {
  var drug = document.getElementById("drug-search").value;
  var idx = document.getElementById("proto-select").value;
  if (idx === "" || idx === "manual" || !calcDb[drug]) return;
  var p = calcDb[drug][parseInt(idx)];
  document.getElementById("c-amount").value = p.amount;
  document.getElementById("c-volume").value = p.volume;
  document.getElementById("c-dose").value = p.dose;
  var unitSel = document.getElementById("c-unit");
  if (p.unit) unitSel.value = p.unit;
  updateConditionalFields();
  if (p.time) {
    document.getElementById("c-time").value = p.time;
    document.getElementById("c-time-unit").value = p.timeUnit || "min";
  }
}

function updateConditionalFields() {
  var unit = document.getElementById("c-unit").value;
  var needsWeight = (unit === "mcg_kg_min" || unit === "mg_kg_hr");
  var needsTime = (unit === "mg_dose" || unit === "mcg_dose");
  document.getElementById("w-weight").classList.toggle("calc-hidden", !needsWeight);
  document.getElementById("w-time").classList.toggle("calc-hidden", !needsTime);
}

function getDropFactor() {
  var r = document.querySelector('input[name="drip"]:checked');
  return r ? parseFloat(r.value) : 10;
}

function runCalc() {
  var err = document.getElementById("calc-err");
  err.style.display = "none";
  var amount = parseFloat(document.getElementById("c-amount").value);
  var volume = parseFloat(document.getElementById("c-volume").value);
  var dose = parseFloat(document.getElementById("c-dose").value);
  var unit = document.getElementById("c-unit").value;
  var dropFactor = getDropFactor();
  if (isNaN(amount) || isNaN(volume) || isNaN(dose) || amount <= 0 || volume <= 0 || dose < 0) {
    err.style.display = "block"; clearOutputs(); return;
  }
  var conc = amount / volume;
  var rateMLhr = 0;
  if (unit === "mg_hr") {
    rateMLhr = dose / conc;
  } else if (unit === "mg_min") {
    rateMLhr = (dose * 60) / conc;
  } else if (unit === "mcg_hr") {
    rateMLhr = (dose / 1000) / conc;
  } else if (unit === "mcg_min") {
    rateMLhr = ((dose / 1000) * 60) / conc;
  } else if (unit === "mcg_kg_min") {
    var kg1 = parseFloat(document.getElementById("c-weight").value);
    if (isNaN(kg1) || kg1 <= 0) { err.style.display = "block"; clearOutputs(); return; }
    rateMLhr = ((dose / 1000) * kg1 * 60) / conc;
  } else if (unit === "mg_kg_hr") {
    var kg2 = parseFloat(document.getElementById("c-weight").value);
    if (isNaN(kg2) || kg2 <= 0) { err.style.display = "block"; clearOutputs(); return; }
    rateMLhr = (dose * kg2) / conc;
  } else if (unit === "mg_dose" || unit === "mcg_dose") {
    var t = parseFloat(document.getElementById("c-time").value);
    var tUnit = document.getElementById("c-time-unit").value;
    if (isNaN(t) || t <= 0) { err.style.display = "block"; clearOutputs(); return; }
    var doseInMg = (unit === "mcg_dose") ? dose / 1000 : dose;
    var tHr = (tUnit === "min") ? t / 60 : t;
    rateMLhr = (doseInMg / conc) / tHr;
  } else if (unit === "units_hr") {
    rateMLhr = dose / conc;
  } else if (unit === "g_hr") {
    rateMLhr = (dose * 1000) / conc;
  }
  var dripRate = Math.round((rateMLhr * dropFactor) / 60);
  var runTime = Math.round((volume / rateMLhr) * 60);
  document.getElementById("o-conc").textContent = conc.toFixed(2);
  document.getElementById("o-rate").textContent = rateMLhr.toFixed(1);
  document.getElementById("o-drip").textContent = dripRate;
  document.getElementById("o-time").textContent = isFinite(runTime) ? runTime : "--";
}

function clearOutputs() {
  ["o-conc", "o-rate", "o-drip", "o-time"].forEach(function(id) {
    document.getElementById(id).textContent = "--";
  });
}

function resetCalc() {
  ["c-amount", "c-volume", "c-dose", "c-weight", "c-time"].forEach(function(id) {
    var el = document.getElementById(id);
    if (el) el.value = "";
  });
  document.getElementById("drug-search").value = "";
  document.getElementById("proto-wrapper").classList.add("calc-hidden");
  document.getElementById("c-unit").value = "mg_hr";
  document.getElementById("w-weight").classList.add("calc-hidden");
  document.getElementById("w-time").classList.add("calc-hidden");
  document.getElementById("calc-err").style.display = "none";
  document.getElementById("d10").checked = true;
  clearOutputs();
}
</script>

## Common Cardiology Dosages

* **Amiodarone:** 300mg IV/IO push (Cardiac Arrest - First Dose)
* **Epinephrine (1:10,000):** 1mg IV/IO every 3-5 mins (Cardiac Arrest)
* **Atropine:** 1mg IV/IO every 3-5 mins (Symptomatic Bradycardia)
