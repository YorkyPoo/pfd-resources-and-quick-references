# Poquoson Fire & Rescue MkDocs Implementation

This repository contains the plain-text Markdown files that power your frictionless, offline-capable protocol site. It is designed to be easily manipulated by you, or autonomously edited by your Agent Zero AI agents.

---

## 1. Initial Launch (One-Time Setup)

To build this on your local machine, open your terminal and run the following in this folder:

```powershell
# Install the MkDocs Material framework
pip install mkdocs-material

# Preview the site locally on your computer
mkdocs serve
```

Open `http://127.0.0.1:8000` in your browser. You will see the live, mobile-responsive site.

---

## 2. Live Site

**🌐 https://YorkyPoo.github.io/pfd-resources-and-quick-references/**

**GitHub Source:** https://github.com/YorkyPoo/pfd-resources-and-quick-references

The crew can open the live URL on any phone. If they tap **"Add to Home Screen"** on iOS or Android, the site will cache locally and work flawlessly even with zero cell service inside a concrete building.

---

## 3. The 15-Minute Daily Maintenance Habit

To update protocols and publish changes to the crew:

### Step 1 — Edit
Open the relevant `.md` file in the `docs/` folder using Obsidian or any editor.

- Protocols: `docs/protocols/[category]/`
- Medications & Calculator: `docs/medications.md`
- Home page: `docs/index.md`

### Step 2 — Publish (4 commands, under 60 seconds)

```powershell
cd "D:\mindpalace\30 - projects\Active\Fire and EMS Resources SSG"
git add .
git commit -m "Update protocols"
git push
mkdocs gh-deploy --force
```

That's it. The live site updates within 1–2 minutes.

---

## 4. Local Preview (Before Publishing)

To preview changes on your own machine before pushing live:

```powershell
cd "D:\mindpalace\30 - projects\Active\Fire and EMS Resources SSG"
mkdocs serve
```

Open `http://127.0.0.1:8000` — live-reloads on every file save.

---

## 5. Protocol Source Files

Raw protocols (in-progress) are maintained separately at:
`D:\mindpalace\30 - projects\Active\EMS Protocols`

When protocols are reviewed and approved, copy updated files into:
`D:\mindpalace\30 - projects\Active\Fire and EMS Resources SSG\docs\protocols\[category]\`

Then run the **Step 2 publish commands** above.
