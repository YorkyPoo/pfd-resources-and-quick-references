---
title: Crew Links & Portals
robots: noindex
---

# Crew Links & Portals

Launchpad for the systems you use between calls. Everything here is a **public, top-level
HTTPS login page** — no shared credentials, no deep links carrying tokens, no notes about
password formats or crew routines.

!!! warning "Not a place for patient information"
    Never enter patient names, MRNs, call numbers or case details on this site. That data
    belongs inside ePCR and OEMS, after you log in there.

## Daily Station Ops {#ops}

<div class="lgrid">
  <a class="lcard lcard--live" href="https://www.vectorsolutions.com/login/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Vector Solutions</span><span class="lcard-s">Training &amp; CE</span></a>
  <span class="lcard lcard--pending" aria-disabled="true">
    <span class="lcard-t">Shift Scheduling</span><span class="lcard-s">Department URL pending</span></span>
  <span class="lcard lcard--pending" aria-disabled="true">
    <span class="lcard-t">Apparatus &amp; Station Checks</span><span class="lcard-s">Department URL pending</span></span>
</div>

## Clinical & Reporting {#clinical}

<div class="lgrid">
  <span class="lcard lcard--pending" aria-disabled="true">
    <span class="lcard-t">ePCR Portal</span><span class="lcard-s">Department URL pending</span></span>
  <a class="lcard lcard--live" href="https://www.vdh.virginia.gov/emergency-medical-services/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Virginia Office of EMS</span><span class="lcard-s">VDH · certification &amp; OEMS</span></a>
  <span class="lcard lcard--pending" aria-disabled="true">
    <span class="lcard-t">PEMS Council</span><span class="lcard-s">Regional references pending</span></span>
</div>

## City & Administration {#admin}

<div class="lgrid">
  <span class="lcard lcard--pending" aria-disabled="true">
    <span class="lcard-t">City Employee Self-Service</span><span class="lcard-s">Department URL pending</span></span>
  <span class="lcard lcard--pending" aria-disabled="true">
    <span class="lcard-t">Payroll &amp; Benefits</span><span class="lcard-s">Department URL pending</span></span>
  <a class="lcard lcard--live" href="../personnel-policies/index.html">
    <span class="lcard-t">Personnel Policy Manual</span><span class="lcard-s">43 indexed policies</span></a>
</div>

---

??? info "Adding a portal link (maintenance rules)"
    Edit `docs/resources/links.md` and swap a pending tile for a live one:

    ```html
    <a class="lcard lcard--live" href="https://DEPARTMENT-URL/" target="_blank"
       rel="noopener noreferrer">
      <span class="lcard-t">Shift Scheduling</span><span class="lcard-s">One short label</span></a>
    ```

    1. **HTTPS top-level login page only.** No query strings, tokens, session IDs or
       `?user=` state in the URL.
    2. **No private addresses.** Nothing on `10.x`, `192.168.x`, `.local`, or a station-only
       host — if it does not resolve on a phone using LTE, it does not belong here.
    3. **No credential guidance.** Username formats, password rules, reset procedures and
       staffing patterns are precisely what a scraped page hands to an impersonator.
    4. **Keep `robots: noindex` in the front matter.** `overrides/main.html` converts it to
       `<meta name="robots" content="noindex, nofollow">` and
       `scripts/mkdocs_post_build.py` drops the page from `sitemap.xml`.
    5. **A pending tile stays pending until a human confirms the URL.** Guessing a login
       address points crew at a domain the department does not control — that is a phishing
       surface, not a shortcut.
