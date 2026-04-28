# This is the master configuration file. Your AI (Agent Zero) can easily parse and update this.
site_name: Poquoson Fire & Rescue Protocols
site_description: Frictionless, offline-capable EMS protocol and SOP dashboard
site_author: YorkyPoo

# Leaving the URL empty ensures the offline plugin resolves file paths correctly
site_url: ""
use_directory_urls: false

theme:
  name: material
  palette:
    primary: red
    accent: white
  features:
    # We purposefully exclude instant loading here to ensure 100% offline reliability
    - search.suggest
    - search.highlight

plugins:
  # The search plugin generates the fast, typo-tolerant index
  - search
  # The built-in offline plugin ensures the search and site work without an internet connection
  - offline

nav:
  - Home: index.md
  - Medications & Calculators: medications.md