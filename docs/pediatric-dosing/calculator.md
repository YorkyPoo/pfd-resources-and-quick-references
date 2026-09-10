# Pediatric Dosing Calculator

Select or enter the patient's estimated weight below to calculate all Poquoson protocol doses, equipment sizes, and energy settings instantly.

---

<div id="pedi-calc" style="background:#141414;border-radius:14px;padding:22px 18px;max-width:800px;margin:0 auto 30px auto;font-family:sans-serif;color:#fff;box-shadow:0 6px 24px rgba(0,0,0,.5)">

## Input

<div class="calc-field" style="margin-bottom:14px">
  <label for="zone-select" style="font-size:13px;font-weight:600;color:#4db8ff;display:block;margin-bottom:5px">Patient Zone</label>
  <select id="zone-select" onchange="updateFromZone()" style="width:100%;background:#000;color:#fff;border:1px solid #4db8ff;border-radius:8px;padding:12px 14px;font-size:16px;outline:none;cursor:pointer;box-sizing:border-box">
    <option value="">-- Select Zone --</option>
    <option value="4">Pink (3-5 kg / 50-60 cm)</option>
    <option value="6.5">Red (6-7 kg / 60-70 cm)</option>
    <option value="8.5">Purple (8-9 kg / 70-85 cm)</option>
    <option value="10.5">Yellow (10-11 kg / 85-95 cm)</option>
    <option value="13">White (12-14 kg / 95-105 cm)</option>
    <option value="16.5">Blue (15-18 kg / 105-120 cm)</option>
    <option value="21">Orange (19-23 kg / 120-135 cm)</option>
    <option value="26.5">Green (24-29 kg / 135-150 cm)</option>
    <option value="33">Brown (30-36 kg / 150-160 cm)</option>
    <option value="41.5">Gray (37-46 kg / 160-170 cm)</option>
  </select>
</div>

OR

<div class="calc-field" style="margin-bottom:14px">
  <label for="weight-input" style="font-size:13px;font-weight:600;color:#ffb84d;display:block;margin-bottom:5px">Enter Exact Weight (kg)</label>
  <input type="number" id="weight-input" oninput="updateFromWeight()" placeholder="Enter weight in kg" style="width:100%;background:#000;color:#fff;border:1px solid #ffb84d;border-radius:8px;padding:12px 14px;font-size:16px;outline:none;box-sizing:border-box">
</div>

<div id="err-msg" style="background:rgba(255,82,82,0.1);color:#ff5252;border:1px solid #ff5252;padding:15px;border-radius:8px;text-align:center;margin-bottom:20px;font-weight:600;display:none"></div>

<div class="btn-row" style="display:flex;gap:12px;margin:20px 0 16px">
  <button onclick="calculate()" style="flex:1;padding:15px;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;background:#4db8ff;color:#000;transition:transform .1s">Calculate</button>
  <button onclick="resetCalc()" style="flex:1;padding:15px;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;background:#2e2e2e;color:#fff;transition:transform .1s">Reset</button>
</div>

## Results

<div id="results" style="display:none">

<div id="info-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center;margin-bottom:16px">
  <div style="font-size:12px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Estimated Weight</div>
  <div id="est-weight" style="font-size:32px;font-weight:800;color:#4db8ff"></div>
</div>

<div style="font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#888;margin:18px 0 10px;padding-bottom:6px;border-bottom:1px solid #2a2a2a">Equipment Sizing</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">ETT (Cuffed)</div>
    <div id="ett-cuffed" style="font-size:24px;font-weight:800"></div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">ETT (Uncuffed)</div>
    <div id="ett-uncuffed" style="font-size:24px;font-weight:800"></div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">LMA</div>
    <div id="lma" style="font-size:24px;font-weight:800"></div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Blade</div>
    <div id="blade" style="font-size:24px;font-weight:800"></div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">NG/OG Tube</div>
    <div id="ng-tube" style="font-size:24px;font-weight:800"></div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Foley</div>
    <div id="foley" style="font-size:24px;font-weight:800"></div>
  </div>
</div>

<div style="font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#888;margin:18px 0 10px;padding-bottom:6px;border-bottom:1px solid #2a2a2a">Defibrillation / Cardioversion</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px">
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Defib Initial</div>
    <div id="defib-init" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">2 J/kg</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Defib Subsequent</div>
    <div id="defib-sub" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">4 J/kg</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Cardioversion</div>
    <div id="cvd" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">0.5-1 J/kg</div>
  </div>
</div>

<div style="font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#888;margin:18px 0 10px;padding-bottom:6px;border-bottom:1px solid #2a2a2a">Cardiac Arrest Medications</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Epinephrine</div>
    <div id="epi-cardiac" style="font-size:24px;font-weight:800;color:#ff5252"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">0.01 mg/kg q3-5min (max 1 mg)</div>
  </div>
  <div class="out-card" style="background:#041420;border:1px solid #1a496b;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Amiodarone</div>
    <div id="amiodarone" style="font-size:24px;font-weight:800;color:#4db8ff"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">5 mg/kg (max 300 mg)</div>
  </div>
</div>

<div style="font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#888;margin:18px 0 10px;padding-bottom:6px;border-bottom:1px solid #2a2a2a">Respiratory Medications</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px">
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Methylprednisolone</div>
    <div id="methylpred" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">2 mg/kg (max 125 mg)</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Magnesium Sulfate</div>
    <div id="magnesium" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">40 mg/kg over 15min (max 2 g)</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Atropine</div>
    <div id="atropine" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">0.02 mg/kg (min 0.1, max 0.5 mg)</div>
  </div>
</div>

<div style="font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#888;margin:18px 0 10px;padding-bottom:6px;border-bottom:1px solid #2a2a2a">Other Medications</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px">
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Fentanyl (Pain)</div>
    <div id="fentanyl" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">1 mcg/kg</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Midazolam IV/IO</div>
    <div id="midazolam-iv" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">0.1 mg/kg (max 2.5 mg)</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Midazolam IN/IM</div>
    <div id="midazolam-in" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">0.2 mg/kg (max 5 mg)</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Ondansetron</div>
    <div id="ondansetron" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">0.15 mg/kg (max 4 mg)</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Naloxone</div>
    <div id="naloxone" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">0.1 mg/kg (max 2 mg)</div>
  </div>
  <div class="out-card" style="background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center">
    <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">NS Fluid Bolus</div>
    <div id="ns-bolus" style="font-size:24px;font-weight:800"></div>
    <div style="font-size:11px;color:#666;margin-top:4px">20 mL/kg</div>
  </div>
</div>

</div>

</div>

<script>
var zoneData = {
  4: { ett_c: "3.0", ett_u: "3.5", lma: "1.0", blade: "0 Miller", ng: "5 Fr", foley: "6 Fr" },
  6.5: { ett_c: "3.5", ett_u: "4.0", lma: "1.5", blade: "1 Miller", ng: "5 Fr", foley: "8 Fr" },
  8.5: { ett_c: "4.0", ett_u: "4.5", lma: "1.5", blade: "1 Miller", ng: "8 Fr", foley: "8 Fr" },
  10.5: { ett_c: "4.5", ett_u: "5.0", lma: "2.0", blade: "1 Miller", ng: "8 Fr", foley: "10 Fr" },
  13: { ett_c: "5.0", ett_u: "5.5", lma: "2.0", blade: "2 Miller", ng: "10 Fr", foley: "10 Fr" },
  16.5: { ett_c: "5.5", ett_u: "6.0", lma: "2.5", blade: "2 Miller", ng: "10 Fr", foley: "12 Fr" },
  21: { ett_c: "6.0", ett_u: "6.5", lma: "2.5", blade: "2-3 Mac", ng: "14 Fr", foley: "12 Fr" },
  26.5: { ett_c: "6.5 cuffed", ett_u: "---", lma: "3.0", blade: "2-3 Mac", ng: "14 Fr", foley: "14 Fr" },
  33: { ett_c: "7.0 cuffed", ett_u: "---", lma: "3.0", blade: "3 Mac", ng: "14 Fr", foley: "14 Fr" },
  41.5: { ett_c: "7.0 cuffed", ett_u: "---", lma: "3.0", blade: "3 Mac", ng: "14 Fr", foley: "14-15G" }
};

function roundTo(val, dec) {
  return Math.round(val * Math.pow(10, dec)) / Math.pow(10, dec);
}

function calcDose(mgPerKg, wt, maxDose) {
  var val = mgPerKg * wt;
  if (maxDose && val > maxDose) return maxDose;
  return roundTo(val, 1);
}

function updateFromZone() {
  var sel = document.getElementById("zone-select");
  if (sel.value) {
    document.getElementById("weight-input").value = sel.value;
    calculate();
  }
}

function updateFromWeight() {
  document.getElementById("zone-select").value = "";
  calculate();
}

function calculate() {
  var errEl = document.getElementById("err-msg");
  var wt = parseFloat(document.getElementById("weight-input").value);
  if (!wt || wt <= 0 || wt > 70) {
    errEl.style.display = "block";
    errEl.textContent = "Please enter a valid weight between 1 and 70 kg, or select a zone.";
    document.getElementById("results").style.display = "none";
    return;
  }
  errEl.style.display = "none";

  // Find best equipment match
  var eq = null;
  var keys = Object.keys(zoneData).map(Number).sort(function(a,b){return a-b;});
  for (var i = 0; i < keys.length; i++) {
    if (wt <= keys[i]) { eq = zoneData[keys[i]]; break; }
  }
  if (!eq) eq = zoneData[41.5];

  document.getElementById("results").style.display = "block";
  document.getElementById("est-weight").textContent = wt + " kg";

  // Equipment
  document.getElementById("ett-cuffed").textContent = eq.ett_c;
  document.getElementById("ett-uncuffed").textContent = eq.ett_u;
  document.getElementById("lma").textContent = eq.lma;
  document.getElementById("blade").textContent = eq.blade;
  document.getElementById("ng-tube").textContent = eq.ng;
  document.getElementById("foley").textContent = eq.foley;

  // Defib
  document.getElementById("defib-init").textContent = Math.round(2 * wt) + " J";
  document.getElementById("defib-sub").textContent = Math.round(4 * wt) + " J";
  document.getElementById("cvd").textContent = Math.round(1 * wt) + " J";

  // Cardiac
  var epi = calcDose(0.01, wt, 1);
  document.getElementById("epi-cardiac").textContent = (epi * 100 >= 100 ? epi : epi.toFixed(2)) + " mg";
  var amio = calcDose(5, wt, 300);
  document.getElementById("amiodarone").textContent = Math.round(amio) + " mg";

  // Respiratory
  var meth = calcDose(2, wt, 125);
  document.getElementById("methylpred").textContent = Math.round(meth) + " mg";
  var mag = calcDose(40, wt, 2000);
  document.getElementById("magnesium").textContent = Math.round(mag) + " mg";
  var atr = calcDose(0.02, wt, 0.5);
  if (atr < 0.1) atr = 0.1;
  document.getElementById("atropine").textContent = atr.toFixed(2) + " mg";

  // Other
  var fent = Math.min(25, Math.round(1 * wt));
  document.getElementById("fentanyl").textContent = fent + " mcg" + (fent >= 25 ? " (max 25 mcg)" : "");
  var midiv = calcDose(0.1, wt, 2.5);
  document.getElementById("midazolam-iv").textContent = midiv.toFixed(1) + " mg";
  var midin = calcDose(0.2, wt, 5);
  document.getElementById("midazolam-in").textContent = midin.toFixed(1) + " mg";
  var onda = calcDose(0.15, wt, 4);
  document.getElementById("ondansetron").textContent = onda + " mg";
  var nal = calcDose(0.1, wt, 2);
  document.getElementById("naloxone").textContent = nal + " mg";
  var ns = Math.round(20 * wt);
  document.getElementById("ns-bolus").textContent = ns + " mL";
}

function resetCalc() {
  document.getElementById("zone-select").value = "";
  document.getElementById("weight-input").value = "";
  document.getElementById("results").style.display = "none";
  document.getElementById("err-msg").style.display = "none";
}
</script>

---

[← Back to Pediatric Dosing Reference](30%20-%20projects/Active/Fire%20and%20EMS%20Resources%20SSG%201/docs/pediatric-dosing/index.md) | [Pre-Calculated Dosing Tables →](dosing-tables.md)
