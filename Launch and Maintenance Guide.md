# Poquoson Fire & Rescue MkDocs Implementation

This repository contains the plain-text Markdown files that power your frictionless, offline-capable protocol site. It is designed to be easily manipulated by you, or autonomously edited by your SystemSculpt AI agents.

## 1. Initial Launch (One-Time Setup)

To build this on your local machine, open your terminal (or command Agent Zero to do it) and run the following in this folder:

```
# Install the MkDocs Material framework
pip install mkdocs-material

# Preview the site locally on your computer
mkdocs serve
```

Open `http://127.0.0.1:8000` in your browser. You will see the live, mobile-responsive site.

## 2. Deploying for the Crew (Zero Cost)

To publish this so the crew can access it without a login:

1. Create a free GitHub repository and push this folder to it.
    
2. Run the deployment command in your terminal:
    

```
mkdocs gh-deploy
```

GitHub Pages will instantly host the site. The crew simply navigates to the URL. If they select "Add to Home Screen" on their iOS or Android device, the site will cache locally and operate flawlessly even deep inside a concrete building with zero cell service.

## 3. The 15-Minute Daily Maintenance Habit (Goal G2)

To hit your G2 metric and maintain your tools, follow this friction-free loop:

1. Check your "Suggestion Box" form for any input from the crew.
    
2. Open the relevant `.md` file in the `docs/` folder (e.g., `docs/medications.md`) using your preferred editor or Obsidian.
    
3. Make the text edit.
    
4. Run `mkdocs gh-deploy` in your terminal.
    

The site updates instantly. Your system remains perfectly organized, and the crew's problem-solving tools are always up-to-date.