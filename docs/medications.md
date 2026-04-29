# Medications & Calculators

Use the search bar at the top of the screen to quickly find specific dosages or protocols.

## Advanced Drip Rate Calculator

<div style="background: #1e1e1e; color: #ffffff; border-radius: 12px; padding: 20px; font-family: sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.3); max-width: 500px; margin: 0 auto 30px auto;">

<!-- Input Section -->
<div style="display: flex; align-items: center; margin-bottom: 15px;">
<div style="flex: 1;"><span style="background: #555; padding: 10px 15px; border-radius: 6px; display: inline-block; font-size: 14px; width: 120px; text-align: center;">Drug Amount</span></div>
<div style="flex: 1; display: flex; align-items: center;">
<input type="number" id="calc-amount" placeholder="0" style="width: 80px; padding: 10px; background: #000; border: 1px solid #444; color: #fff; border-radius: 4px; text-align: right; font-size: 16px;">
<span style="margin-left: 10px; font-size: 16px;">mg</span>
</div>
</div>

<div style="display: flex; align-items: center; margin-bottom: 15px;">
<div style="flex: 1;"><span style="background: #555; padding: 10px 15px; border-radius: 6px; display: inline-block; font-size: 14px; width: 120px; text-align: center;">Volume</span></div>
<div style="flex: 1; display: flex; align-items: center;">
<input type="number" id="calc-volume" placeholder="0" style="width: 80px; padding: 10px; background: #000; border: 1px solid #444; color: #fff; border-radius: 4px; text-align: right; font-size: 16px;">
<span style="margin-left: 10px; font-size: 16px;">mL</span>
</div>
</div>

<div style="display: flex; align-items: center; margin-bottom: 25px;">
<div style="flex: 1;"><span style="background: #555; padding: 10px 15px; border-radius: 6px; display: inline-block; font-size: 14px; width: 120px; text-align: center;">Dose Ordered</span></div>
<div style="flex: 1; display: flex; align-items: center;">
<input type="number" id="calc-dose" placeholder="0" style="width: 80px; padding: 10px; background: #000; border: 1px solid #444; color: #fff; border-radius: 4px; text-align: right; font-size: 16px;">
<span style="margin-left: 10px; font-size: 16px;">mg/hr</span>
</div>
</div>

<!-- Buttons -->
<div style="display: flex; gap: 15px; margin-bottom: 25px; justify-content: center;">
<button onclick="calculateAdvancedDrip()" style="background: #777; color: white; border: none; padding: 12px 25px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; width: 120px;">Calculate</button>
<button onclick="resetAdvancedDrip()" style="background: #555; color: white; border: none; padding: 12px 25px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; width: 120px;">Reset</button>
</div>

<!-- Drip Set Radios -->
<div style="text-align: center; margin-bottom: 25px;">
<h4 style="margin: 0 0 15px 0; font-style: italic; font-weight: normal; color: #ccc;">Choose A Dripset (Drops per mL)</h4>
<div style="display: flex; justify-content: center; gap: 20px; font-size: 16px;">
<label style="cursor: pointer;"><input type="radio" name="calc-dropfactor" value="10" checked style="accent-color: #4db8ff;"> 10</label>
<label style="cursor: pointer;"><input type="radio" name="calc-dropfactor" value="15" style="accent-color: #4db8ff;"> 15</label>
<label style="cursor: pointer;"><input type="radio" name="calc-dropfactor" value="20" style="accent-color: #4db8ff;"> 20</label>
<label style="cursor: pointer;"><input type="radio" name="calc-dropfactor" value="60" style="accent-color: #4db8ff;"> 60</label>
</div>
</div>

<!-- Output Error Message -->
<div id="calc-error" style="color: #ff5252; text-align: center; margin-bottom: 15px; font-weight: bold; display: none;">Please fill out all fields correctly.</div>

<!-- Output Section -->
<div style="display: flex; align-items: center; margin-bottom: 15px;">
<div style="flex: 1;"><span style="background: #555; padding: 10px 15px; border-radius: 6px; display: inline-block; font-size: 14px; width: 120px; text-align: center;">Ratio</span></div>
<div style="flex: 1; display: flex; align-items: center; justify-content: space-between; padding-right: 20px;">
<span id="out-ratio" style="font-size: 18px; font-weight: bold;">--</span>
<span style="font-size: 14px; color: #aaa;">mg/mL</span>
</div>
</div>

<div style="display: flex; align-items: center; margin-bottom: 15px;">
<div style="flex: 1;"><span style="background: #555; padding: 10px 15px; border-radius: 6px; display: inline-block; font-size: 14px; width: 120px; text-align: center;">Infusion Rate</span></div>
<div style="flex: 1; display: flex; align-items: center; justify-content: space-between; padding-right: 20px;">
<span id="out-infusion" style="font-size: 18px; font-weight: bold;">--</span>
<span style="font-size: 14px; color: #aaa;">mL/hr</span>
</div>
</div>

<div style="display: flex; align-items: center;">
<div style="flex: 1;"><span style="background: #555; padding: 10px 15px; border-radius: 6px; display: inline-block; font-size: 14px; width: 120px; text-align: center;">Manual Rate</span></div>
<div style="flex: 1; display: flex; align-items: center; justify-content: space-between; padding-right: 20px;">
<span id="out-manual" style="font-size: 18px; font-weight: bold; color: #4db8ff;">--</span>
<span style="font-size: 14px; color: #aaa;">gtts/min</span>
</div>
</div>
</div>

<script>
function calculateAdvancedDrip() {
const errorDiv = document.getElementById('calc-error');
errorDiv.style.display = 'none';
const amount = parseFloat(document.getElementById('calc-amount').value);
const volume = parseFloat(document.getElementById('calc-volume').value);
const dose = parseFloat(document.getElementById('calc-dose').value);
let dropFactor = 10;
const radios = document.getElementsByName('calc-dropfactor');
for (let i = 0; i < radios.length; i++) {
if (radios[i].checked) {
dropFactor = parseFloat(radios[i].value);
break;
}
}
if (isNaN(amount) || isNaN(volume) || isNaN(dose) || amount <= 0 || volume <= 0 || dose < 0) {
errorDiv.style.display = 'block';
document.getElementById('out-ratio').innerText = "--";
document.getElementById('out-infusion').innerText = "--";
document.getElementById('out-manual').innerText = "--";
return;
}
const ratio = amount / volume;
const infusionRate = dose / ratio;
const manualRate = (infusionRate * dropFactor) / 60;
document.getElementById('out-ratio').innerText = ratio.toFixed(2);
document.getElementById('out-infusion').innerText = infusionRate.toFixed(2);
document.getElementById('out-manual').innerText = Math.round(manualRate);
}
function resetAdvancedDrip() {
document.getElementById('calc-amount').value = '';
document.getElementById('calc-volume').value = '';
document.getElementById('calc-dose').value = '';
document.getElementById('out-ratio').innerText = '--';
document.getElementById('out-infusion').innerText = '--';
document.getElementById('out-manual').innerText = '--';
document.getElementById('calc-error').style.display = 'none';
const radios = document.getElementsByName('calc-dropfactor');
radios[0].checked = true;
}
</script>

## Common Cardiology Dosages

* **Amiodarone:** 300mg IV/IO push (Cardiac Arrest - First Dose)
* **Epinephrine (1:10,000):** 1mg IV/IO every 3-5 mins (Cardiac Arrest)
* **Atropine:** 1mg IV/IO every 3-5 mins (Symptomatic Bradycardia)

