# Medications & Calculators

Use the search bar at the top of the screen to quickly find specific dosages or protocols.

## Advanced Drip Rate & Protocol Calculator

.input-wrapper { display: flex; flex-direction: column; gap: 6px; }

label { font-size: 14px; font-weight: 600; color: var(--text-muted); }

.controls-row { display: flex; gap: 0; border-radius: 8px; overflow: hidden; border: 1px solid var(--border-color); }

.c-input, .c-select {

background: #000; color: #fff; border: none; padding: 12px 10px; font-size: 15px;

outline: none; transition: background 0.2s; width: 100%;

}

.c-input:focus, .c-select:focus { background: #111; }

.c-input { flex: 2; text-align: right; }

.c-select { flex: 1.5; border-left: 1px solid var(--border-color); cursor: pointer; }

/* Searchable Datalist Style */

.search-input { border-radius: 8px; border: 1px solid var(--border-color); padding: 12px; background: #000; color: #fff; width: 100%; font-size: 16px; outline: none; }

.search-input:focus { border-color: var(--accent); }

.radio-toolbar { display: flex; gap: 10px; flex-wrap: wrap; }

.radio-toolbar input[type="radio"] { display: none; }

.radio-toolbar label {

flex: 1; text-align: center; background: #000; padding: 12px; border: 1px solid var(--border-color);

border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600; color: var(--text-muted);

transition: all 0.2s;

}

.radio-toolbar input[type="radio"]:checked + label {

background: var(--accent); color: #000; border-color: var(--accent);

}

.btn-row { display: flex; gap: 15px; margin: 25px 0; }

.btn {

flex: 1; padding: 16px; border: none; border-radius: 10px; font-size: 16px; font-weight: 700;

cursor: pointer; transition: transform 0.1s, filter 0.2s;

}

.btn:active { transform: scale(0.98); }

.btn-calc { background: var(--accent); color: #000; }

.btn-calc:hover { filter: brightness(1.1); }

.btn-reset { background: #333; color: #fff; }

.btn-reset:hover { background: #444; }

.output-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }

.out-box { background: #000; border: 1px solid var(--border-color); border-radius: 10px; padding: 15px; text-align: center; }

.out-title { font-size: 12px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px; }

.out-val { font-size: 28px; font-weight: 800; color: #fff; line-height: 1; margin-bottom: 4px; }

.out-unit { font-size: 14px; color: var(--text-muted); }

.out-primary { background: #0a1f2e; border-color: #1a496b; grid-column: span 2; }

.out-primary .out-val { color: var(--accent); font-size: 42px; }

#err-msg { background: rgba(255,82,82,0.1); color: var(--error); border: 1px solid var(--error); padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px; font-weight: 600; display: none; }

  

```
<div class="input-wrapper" id="protocol-selector-wrapper" style="display:none;">
  <label style="color: var(--accent);">Protocol Dose</label>
  <select id="protocol-dose" class="search-input" style="border-color: var(--accent);" onchange="applyProtocol()">
    <option value="">Select Dose or Choose Manual Entry...</option>
  </select>
</div>
```

```
<div class="input-grid">
  <div class="input-wrapper" id="w-weight" style="display:none;">
    <label style="color: var(--accent);">Patient Weight</label>
    <div class="controls-row">
      <input type="number" id="c-weight" class="c-input" placeholder="0">
      <select class="c-select" disabled><option>kg</option></select>
    </div>
  </div>
  <div class="input-wrapper" id="w-time" style="display:none;">
    <label style="color: #ffb84d;">Infuse Over</label>
    <div class="controls-row">
      <input type="number" id="c-time" class="c-input" placeholder="Time">
      <select id="c-time-unit" class="c-select">
        <option value="MINUTES">MINUTES</option>
        <option value="HOURS">HOURS</option>
      </select>
    </div>
  </div>
</div>
```

## Common Cardiology Dosages

- **Amiodarone:** 300mg IV/IO push (Cardiac Arrest - First Dose)
    
- **Epinephrine (1:10,000):** 1mg IV/IO every 3-5 mins (Cardiac Arrest)
    
- **Atropine:** 1mg IV/IO every 3-5 mins (Symptomatic Bradycardia)