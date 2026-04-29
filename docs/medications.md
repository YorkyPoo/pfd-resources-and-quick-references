# Medications & Calculators

Use the search bar at the top of the screen to quickly find specific dosages or protocols.

## Advanced Drip Rate & Protocol Calculator

<style>
.calc-wrap{background:#141414;border-radius:14px;padding:22px 18px;max-width:520px;margin:0 auto 30px auto;font-family:sans-serif;color:#fff;box-shadow:0 6px 24px rgba(0,0,0,.5)}
.calc-section-title{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#888;margin:18px 0 10px;padding-bottom:6px;border-bottom:1px solid #2a2a2a}
.calc-field{margin-bottom:14px}
.calc-label{font-size:13px;font-weight:600;color:#aaa;margin-bottom:5px;display:block}
.calc-label.accent{color:#4db8ff}
.calc-label.warm{color:#ffb84d}
.calc-row{display:flex;border-radius:8px;overflow:hidden;border:1px solid #2e2e2e}
.calc-input{flex:2;background:#000;color:#fff;border:none;padding:12px 10px;font-size:16px;outline:none;text-align:right;min-width:0;transition:background .15s}
.calc-input:focus{background:#0a0a0a}
.calc-unit{background:#1a1a1a;color:#888;border:none;border-left:1px solid #2e2e2e;padding:12px 10px;font-size:13px;min-width:64px;text-align:center;display:flex;align-items:center;justify-content:center}
.calc-select{background:#1a1a1a;color:#fff;border:none;border-left:1px solid #2e2e2e;padding:12px 8px;font-size:13px;outline:none;cursor:pointer;min-width:0}
.calc-search{width:100%;background:#000;color:#fff;border:1px solid #2e2e2e;border-radius:8px;padding:12px 14px;font-size:16px;outline:none;box-sizing:border-box;transition:border-color .2s}
.calc-search:focus{border-color:#4db8ff}
.calc-proto-select{width:100%;background:#000;color:#fff;border:1px solid #4db8ff;border-radius:8px;padding:12px 14px;font-size:14px;outline:none;cursor:pointer;box-sizing:border-box}
.drip-toolbar{display:flex;gap:8px;flex-wrap:wrap}
.drip-toolbar input[type=radio]{display:none}
.drip-toolbar label{flex:1;text-align:center;background:#000;padding:11px 6px;border:1px solid #2e2e2e;border-radius:8px;cursor:pointer;font-size:15px;font-weight:600;color:#666;transition:all .15s;min-width:48px}
.drip-toolbar input[type=radio]:checked+label{background:#4db8ff;color:#000;border-color:#4db8ff}
.calc-btn-row{display:flex;gap:12px;margin:20px 0 16px}
.calc-btn{flex:1;padding:15px;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;transition:transform .1s,filter .15s}
.calc-btn:active{transform:scale(.97)}
.calc-btn-go{background:#4db8ff;color:#000}
.calc-btn-go:hover{filter:brightness(1.12)}
.calc-btn-rst{background:#2e2e2e;color:#fff}
.calc-btn-rst:hover{background:#3a3a3a}
.out-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.out-card{background:#0d0d0d;border:1px solid #2a2a2a;border-radius:10px;padding:14px;text-align:center}
.out-card.primary{grid-column:span 2;background:#041420;border-color:#1a496b}
.out-card-title{font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.out-card-val{font-size:26px;font-weight:800;color:#fff;line-height:1;margin-bottom:4px}
.out-card.primary .out-card-val{font-size:40px;color:#4db8ff}
.out-card-unit{font-size:13px;color:#555}
#calc-err{background:rgba(255,82,82,.08);color:#ff5252;border:1px solid #ff5252;padding:12px;border-radius:8px;text-align:center;margin-bottom:16px;font-weight:600;display:none}
.calc-hidden{display:none}
</style>

<div markdown="0" class="calc-wrap">

<div class="calc-section-title">Drug Search</div>
<div class="calc-field">
  <input list="drug-list" id="drug-search" class="calc-search" placeholder="Type to search drugs..." oninput="onDrugSearch()" />
  <datalist id="drug-list">
    <option value="Adenosine"></option><option value="Albuterol"></option>
    <option value="Amiodarone"></option><option value="Aspirin"></option>
    <option value="Atropine Sulfate"></option><option value="Calcium Chloride"></option>
    <option value="Dextrose"></option><option value="Dopamine"></option>
    <option value="Epinephrine"></option><option value="Fentanyl"></option>
    <option value="Glucagon"></option><option value="Heparin"></option>
    <option value="Insulin"></option><option value="Ketamine"></option>
    <option value="Lidocaine"></option><option value="Magnesium Sulfate"></option>
    <option value="Midazolam"></option><option value="Morphine"></option>
    <option value="Naloxone"></option><option value="Nitroglycerin"></option>
    <option value="Norepinephrine (Levophed)"></option><option value="Ondansetron"></option>
    <option value="Sodium Bicarbonate"></option><option value="TXA (Tranexamic Acid)"></option>
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
    <select id="c-amount-unit" class="calc-select">
      <option value="mg">mg</option>
      <option value="mcg">MCG</option>
      <option value="g">grams</option>
      <option value="units">units</option>
    </select>
  </div>
</div>
<div class="calc-field">
  <label class="calc-label">Bag Volume</label>
  <div class="calc-row">
    <input type="number" id="c-volume" class="calc-input" placeholder="0">
    <span class="calc-unit">mL</span>
  </div>
</div>

<div class="calc-section-title">Dosage</div>
<div class="calc-field">
  <div class="calc-row">
    <input type="number" id="c-dose" class="calc-input" placeholder="0">
    <select id="c-unit" class="calc-select" onchange="updateConditionalFields()">
      <optgroup label="--- mg ---">
        <option value="mg_hr">mg / hr</option>
        <option value="mg_min">mg / min</option>
        <option value="mg_dose">mg / DOSE</option>
        <option value="mg_kg_hr">mg / kg / hr</option>
        <option value="mg_kg_min">mg / kg / min</option>
        <option value="mg_kg_dose">mg / kg / DOSE</option>
      </optgroup>
      <optgroup label="--- MCG ---">
        <option value="mcg_hr">MCG / hr</option>
        <option value="mcg_min">MCG / min</option>
        <option value="mcg_dose">MCG / DOSE</option>
        <option value="mcg_kg_hr">MCG / kg / hr</option>
        <option value="mcg_kg_min">MCG / kg / min</option>
        <option value="mcg_kg_dose">MCG / kg / DOSE</option>
      </optgroup>
      <optgroup label="--- units ---">
        <option value="u_hr">units / hr</option>
        <option value="u_min">units / min</option>
        <option value="u_dose">units / DOSE</option>
        <option value="u_kg_hr">units / kg / hr</option>
        <option value="u_kg_min">units / kg / min</option>
        <option value="u_kg_dose">units / kg / DOSE</option>
      </optgroup>
      <optgroup label="--- grams ---">
        <option value="g_hr">g / hr</option>
        <option value="g_min">g / min</option>
        <option value="g_dose">g / DOSE</option>
      </optgroup>
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
    <input type="radio" id="d10" name="drip" value="10" checked><label for="d10">10</label>
    <input type="radio" id="d15" name="drip" value="15"><label for="d15">15</label>
    <input type="radio" id="d20" name="drip" value="20"><label for="d20">20</label>
    <input type="radio" id="d60" name="drip" value="60"><label for="d60">60</label>
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
    <div class="out-card-unit" id="o-conc-unit">/ mL</div>
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
var calcDb={
"Amiodarone":[
{label:"Cardiac Arrest - 300 mg push",amount:300,amountUnit:"mg",volume:20,dose:300,unit:"mg_dose",time:1,timeUnit:"min"},
{label:"V-Fib/V-Tach - 150 mg over 10 min",amount:150,amountUnit:"mg",volume:100,dose:150,unit:"mg_dose",time:10,timeUnit:"min"}
],
"Epinephrine":[
{label:"Cardiac Arrest - 1 mg push",amount:1,amountUnit:"mg",volume:10,dose:1,unit:"mg_dose",time:1,timeUnit:"min"},
{label:"Anaphylaxis - 0.3 mg IM",amount:0.3,amountUnit:"mg",volume:3,dose:0.3,unit:"mg_dose",time:1,timeUnit:"min"},
{label:"Bradycardia Infusion - 2 MCG/min",amount:1,amountUnit:"mg",volume:250,dose:2,unit:"mcg_min"}
],
"Magnesium Sulfate":[
{label:"Torsades - 2 g over 10 min",amount:2,amountUnit:"g",volume:100,dose:2,unit:"g_dose",time:10,timeUnit:"min"},
{label:"Severe Asthma - 2 g over 20 min",amount:2,amountUnit:"g",volume:100,dose:2,unit:"g_dose",time:20,timeUnit:"min"},
{label:"OB Eclampsia - 4 g over 20 min",amount:4,amountUnit:"g",volume:100,dose:4,unit:"g_dose",time:20,timeUnit:"min"}
],
"TXA (Tranexamic Acid)":[
{label:"Trauma Hemorrhage - 1 g over 10 min",amount:1000,amountUnit:"mg",volume:100,dose:1000,unit:"mg_dose",time:10,timeUnit:"min"}
],
"Norepinephrine (Levophed)":[
{label:"Septic Shock - 0.1 MCG/kg/min",amount:4,amountUnit:"mg",volume:250,dose:0.1,unit:"mcg_kg_min"}
],
"Dopamine":[
{label:"Standard - 5 MCG/kg/min",amount:400,amountUnit:"mg",volume:250,dose:5,unit:"mcg_kg_min"},
{label:"High Dose - 10 MCG/kg/min",amount:400,amountUnit:"mg",volume:250,dose:10,unit:"mcg_kg_min"}
],
"Lidocaine":[
{label:"Maintenance Infusion - 2 mg/min",amount:1000,amountUnit:"mg",volume:250,dose:2,unit:"mg_min"}
],
"Fentanyl":[
{label:"Pain Control - 1 MCG/kg",amount:0.1,amountUnit:"mg",volume:2,dose:1,unit:"mcg_kg_dose",time:5,timeUnit:"min"}
],
"Morphine":[
{label:"Pain Control - 0.1 mg/kg",amount:10,amountUnit:"mg",volume:10,dose:0.1,unit:"mg_kg_dose",time:5,timeUnit:"min"}
],
"Midazolam":[
{label:"Sedation - 0.05 mg/kg IV",amount:50,amountUnit:"mg",volume:50,dose:0.05,unit:"mg_kg_dose",time:2,timeUnit:"min"}
],
"Ketamine":[
{label:"Dissociative - 1 mg/kg IV",amount:500,amountUnit:"mg",volume:10,dose:1,unit:"mg_kg_dose",time:1,timeUnit:"min"},
{label:"Sub-dissociative - 0.3 mg/kg IV",amount:500,amountUnit:"mg",volume:10,dose:0.3,unit:"mg_kg_dose",time:1,timeUnit:"min"}
],
"Heparin":[
{label:"ACS Infusion - 1000 units/hr",amount:25000,amountUnit:"units",volume:250,dose:1000,unit:"u_hr"}
],
"Insulin":[
{label:"DKA Infusion - 0.1 units/kg/hr",amount:100,amountUnit:"units",volume:100,dose:0.1,unit:"u_kg_hr"}
]
};

function onDrugSearch(){
  var val=document.getElementById("drug-search").value;
  var wrapper=document.getElementById("proto-wrapper");
  var sel=document.getElementById("proto-select");
  if(calcDb[val]){
    sel.innerHTML='<option value="">-- Select Protocol Dose --</option>';
    calcDb[val].forEach(function(p,i){
      var o=document.createElement("option");o.value=i;o.textContent=p.label;sel.appendChild(o);
    });
    var m=document.createElement("option");m.value="manual";m.textContent="Manual Entry";sel.appendChild(m);
    wrapper.classList.remove("calc-hidden");
  } else {
    wrapper.classList.add("calc-hidden");
  }
}

function applyProtocol(){
  var drug=document.getElementById("drug-search").value;
  var idx=document.getElementById("proto-select").value;
  if(idx===""||idx==="manual"||!calcDb[drug]) return;
  var p=calcDb[drug][parseInt(idx)];
  document.getElementById("c-amount").value=p.amount;
  document.getElementById("c-amount-unit").value=p.amountUnit||"mg";
  document.getElementById("c-volume").value=p.volume;
  document.getElementById("c-dose").value=p.dose;
  document.getElementById("c-unit").value=p.unit;
  updateConditionalFields();
  if(p.time){document.getElementById("c-time").value=p.time;document.getElementById("c-time-unit").value=p.timeUnit||"min";}
}

function updateConditionalFields(){
  var u=document.getElementById("c-unit").value;
  var needsKg=u.indexOf("kg")>-1;
  var needsTime=u.indexOf("dose")>-1;
  document.getElementById("w-weight").classList.toggle("calc-hidden",!needsKg);
  document.getElementById("w-time").classList.toggle("calc-hidden",!needsTime);
}

function getDropFactor(){
  var r=document.querySelector('input[name="drip"]:checked');
  return r?parseFloat(r.value):10;
}

function getDosePerHr(dose,unit,kg,tHr){
  // Returns dose in base bag-unit per hour
  // MCG-based units divide by 1000 to get mg equivalent
  var d=dose;
  if(unit==="mg_hr") return d;
  if(unit==="mg_min") return d*60;
  if(unit==="mg_dose") return tHr>0?d/tHr:null;
  if(unit==="mg_kg_hr") return d*kg;
  if(unit==="mg_kg_min") return d*kg*60;
  if(unit==="mg_kg_dose") return tHr>0?(d*kg)/tHr:null;
  if(unit==="mcg_hr") return d/1000;
  if(unit==="mcg_min") return (d/1000)*60;
  if(unit==="mcg_dose") return tHr>0?(d/1000)/tHr:null;
  if(unit==="mcg_kg_hr") return (d/1000)*kg;
  if(unit==="mcg_kg_min") return (d/1000)*kg*60;
  if(unit==="mcg_kg_dose") return tHr>0?((d/1000)*kg)/tHr:null;
  if(unit==="u_hr") return d;
  if(unit==="u_min") return d*60;
  if(unit==="u_dose") return tHr>0?d/tHr:null;
  if(unit==="u_kg_hr") return d*kg;
  if(unit==="u_kg_min") return d*kg*60;
  if(unit==="u_kg_dose") return tHr>0?(d*kg)/tHr:null;
  if(unit==="g_hr") return d*1000;
  if(unit==="g_min") return d*1000*60;
  if(unit==="g_dose") return tHr>0?(d*1000)/tHr:null;
  return null;
}

function getAmountInMg(amount,amtUnit){
  if(amtUnit==="mg") return amount;
  if(amtUnit==="mcg") return amount/1000;
  if(amtUnit==="g") return amount*1000;
  if(amtUnit==="units") return amount; // units stay as-is
  return amount;
}

function runCalc(){
  var err=document.getElementById("calc-err");
  err.style.display="none";
  var amount=parseFloat(document.getElementById("c-amount").value);
  var amtUnit=document.getElementById("c-amount-unit").value;
  var volume=parseFloat(document.getElementById("c-volume").value);
  var dose=parseFloat(document.getElementById("c-dose").value);
  var unit=document.getElementById("c-unit").value;
  var dropFactor=getDropFactor();
  if(isNaN(amount)||isNaN(volume)||isNaN(dose)||amount<=0||volume<=0||dose<0){
    err.style.display="block";clearOutputs();return;
  }
  var kg=0;
  if(unit.indexOf("kg")>-1){
    kg=parseFloat(document.getElementById("c-weight").value);
    if(isNaN(kg)||kg<=0){err.style.display="block";clearOutputs();return;}
  }
  var tHr=0;
  if(unit.indexOf("dose")>-1){
    var tVal=parseFloat(document.getElementById("c-time").value);
    var tUnit=document.getElementById("c-time-unit").value;
    if(isNaN(tVal)||tVal<=0){err.style.display="block";clearOutputs();return;}
    tHr=tUnit==="min"?tVal/60:tVal;
  }
  // Concentration uses raw amount / volume (in whatever bag unit)
  var conc=amount/volume;
  // Convert amount to mg-equivalent for rate math (except units stays as units)
  var amountMg=getAmountInMg(amount,amtUnit);
  var concMg=amountMg/volume;
  var dosePerHr=getDosePerHr(dose,unit,kg,tHr);
  if(dosePerHr===null||dosePerHr<=0){err.style.display="block";clearOutputs();return;}
  var rateMLhr=dosePerHr/concMg;
  var dripRate=Math.round((rateMLhr*dropFactor)/60);
  var runTime=Math.round((volume/rateMLhr)*60);
  var concLabel=amtUnit+" / mL";
  document.getElementById("o-conc-unit").textContent=concLabel;
  document.getElementById("o-conc").textContent=conc.toFixed(2);
  document.getElementById("o-rate").textContent=rateMLhr.toFixed(1);
  document.getElementById("o-drip").textContent=dripRate;
  document.getElementById("o-time").textContent=isFinite(runTime)?runTime:"--";
}

function clearOutputs(){
  ["o-conc","o-rate","o-drip","o-time"].forEach(function(id){
    document.getElementById(id).textContent="--";
  });
}

function resetCalc(){
  ["c-amount","c-volume","c-dose","c-weight","c-time"].forEach(function(id){
    var el=document.getElementById(id);if(el)el.value="";
  });
  document.getElementById("drug-search").value="";
  document.getElementById("proto-wrapper").classList.add("calc-hidden");
  document.getElementById("c-amount-unit").value="mg";
  document.getElementById("c-unit").value="mg_hr";
  document.getElementById("w-weight").classList.add("calc-hidden");
  document.getElementById("w-time").classList.add("calc-hidden");
  document.getElementById("calc-err").style.display="none";
  document.getElementById("d10").checked=true;
  clearOutputs();
}
</script>

---

## Common Cardiology Dosages

* **Amiodarone:** 300 mg IV/IO push — Cardiac Arrest (First Dose); 150 mg IV over 10 min — Stable V-Tach
* **Epinephrine (1:10,000):** 1 mg IV/IO q3-5 min — Cardiac Arrest
* **Epinephrine (1:1,000):** 0.3–0.5 mg IM — Anaphylaxis
* **Atropine Sulfate:** 0.5–1 mg IV — Symptomatic Bradycardia (max 3 mg)
* **Adenosine:** 6 mg rapid IV push — SVT (may repeat 12 mg x2)
* **Lidocaine:** 1–1.5 mg/kg IV — V-Fib/V-Tach (max 3 mg/kg); Infusion 1–4 mg/min
* **Magnesium Sulfate:** 1–2 g IV over 5–60 min — Torsades de Pointes
* **Dopamine:** 5–20 MCG/kg/min IV infusion — Hypotension/Bradycardia
* **Norepinephrine:** 0.1–2 MCG/kg/min IV — Septic Shock

---

## Analgesics & Sedation

* **Fentanyl:** 1–2 MCG/kg IV/IO/IN — Pain Management
* **Morphine:** 0.1 mg/kg IV/IO slow push — Pain Management
* **Ketamine:** 1–2 mg/kg IV — Dissociative Anesthesia; 0.1–0.3 mg/kg IV — Sub-dissociative analgesia
* **Midazolam:** 0.05–0.1 mg/kg IV/IO/IN — Sedation/Seizures
* **Naloxone:** 0.4–2 mg IV/IO/IM/IN — Opioid Reversal (may repeat q2-3 min)
* **Diazepam:** 5–10 mg IV — Seizures

---

## Respiratory Medications

* **Albuterol:** 2.5 mg nebulized — Bronchospasm/Asthma
* **Ipratropium Bromide:** 0.5 mg nebulized — Bronchospasm (combined with Albuterol)
* **Epinephrine (1:1,000):** 0.3 mg IM/SQ — Severe Bronchospasm/Anaphylaxis
* **Magnesium Sulfate:** 2 g IV over 20 min — Severe/Refractory Asthma
* **Methylprednisolone:** 125 mg IV — Asthma/Allergic Reaction

---

## Metabolic & Other

* **Dextrose 50%:** 25 g (50 mL) IV — Hypoglycemia
* **Dextrose 10%:** 0.5–1 g/kg IV — Pediatric Hypoglycemia
* **Glucagon:** 1 mg IM/SQ — Hypoglycemia (when IV access unavailable)
* **Sodium Bicarbonate:** 1 mEq/kg IV — Prolonged Cardiac Arrest/Acidosis/TCA OD
* **Calcium Chloride:** 1 g IV slow push — Hyperkalemia/CCB Toxicity
* **Ondansetron (Zofran):** 4 mg IV/IM/ODT — Nausea/Vomiting
* **Aspirin:** 324 mg PO chewed — Suspected ACS
* **Nitroglycerin:** 0.4 mg SL q5 min — ACS/CHF (max 3 doses; SBP > 90)
* **TXA (Tranexamic Acid):** 1 g IV over 10 min — Traumatic Hemorrhage (within 3 hrs of injury)
