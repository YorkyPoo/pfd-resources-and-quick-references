# Medications & Calculators

Use the search bar at the top of the screen to quickly find specific dosages or protocols.

## Advanced Drip Rate & Protocol Calculator

```
.radio-group { display: flex; justify-content: center; gap: 20px; padding: 10px 0; }
.radio-label { cursor: pointer; font-size: 16px; display: flex; align-items: center; gap: 5px; }
.radio-label input { accent-color: #4db8ff; width: 18px; height: 18px; }

.output-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 15px;
}
.output-card {
  background: #111; border: 1px solid #333; border-radius: 8px; padding: 15px;
  text-align: center;
}
.output-title { font-size: 12px; color: #888; margin-bottom: 5px; text-transform: uppercase; }
.output-value { font-size: 24px; font-weight: bold; color: #fff; }
.output-unit { font-size: 14px; color: #aaa; }
.highlight-value { color: #4db8ff; }

#calc-error {
  background: rgba(255, 82, 82, 0.1); border: 1px solid #ff5252; color: #ff5252;
  padding: 12px; border-radius: 6px; text-align: center; margin-bottom: 20px; display: none;
}
```

```
<!-- Conditional: Weight -->
<div class="input-row" id="row-weight" style="display: none;">
  <div class="input-label" style="color:#4db8ff;">Patient Weight</div>
  <div class="input-group">
    <input type="number" id="calc-weight" class="calc-input" placeholder="0">
    <select class="calc-select" style="flex: 0.8;" disabled><option>kg</option></select>
  </div>
</div>

<!-- Conditional: Duration (for /DOSE) -->
<div class="input-row" id="row-duration" style="display: none;">
  <div class="input-label" style="color:#ffb84d;">Infuse Over</div>
  <div class="input-group">
    <input type="number" id="calc-duration" class="calc-input" placeholder="Time">
    <select id="calc-duration-unit" class="calc-select" style="flex: 0.8;">
      <option value="min">Mins</option>
      <option value="hr">Hours</option>
    </select>
  </div>
</div>
```


## Common Cardiology Dosages

* **Amiodarone:** 300mg IV/IO push (Cardiac Arrest - First Dose)
* **Epinephrine (1:10,000):** 1mg IV/IO every 3-5 mins (Cardiac Arrest)
* **Atropine:** 1mg IV/IO every 3-5 mins (Symptomatic Bradycardia)

