---
title: Crew Links & Portals
robots: noindex
---

# Crew Links & Portals

Department systems, grouped by **when you touch them** — on the scene, after the run, before
duty, for your ticket, then the city. Every link opens in its own tab.

!!! warning "Never put patient information on these pages from here"
    Do not type patient names, MRNs, call numbers or case details into a search box or
    bookmark on this site. That information belongs inside ePCR and NERIS, after you log in.

## On-Scene & Response {#response}

<div class="lgrid">
  <a class="lcard lcard--live" href="https://www.geoplan.app/poquoson/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Poquoson GIS Map</span><span class="lcard-s">Parcels, addresses, structures</span></a>
  <a class="lcard lcard--live" href="https://dof.virginia.gov/wildland-prescribed-fire/fire-danger/daily-fire-danger-rating/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Daily Fire Danger</span><span class="lcard-s">VA Dept. of Forestry rating</span></a>
  <a class="lcard lcard--live" href="https://www.pulsepoint.org/download" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Rip &amp; Run</span><span class="lcard-s">PulsePoint app download</span></a>
</div>

## Run Documentation {#doc}

<div class="lgrid">
  <a class="lcard lcard--live" href="https://www.esosuite.net/login/Va00340" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">ESO Suite</span><span class="lcard-s">ePCR &amp; NERIS incident reporting</span></a>
  <a class="lcard lcard--live" href="https://logrx.com/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">LogRx</span><span class="lcard-s">Controlled-substance / narcotics log</span></a>
</div>

## Apparatus & Scheduling {#readiness}

<div class="lgrid">
  <a class="lcard lcard--live" href="https://ems.vendnovation.com/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Truck Box &amp; Apparatus Checks</span><span class="lcard-s">VendNovation EMS</span></a>
  <a class="lcard lcard--live" href="https://sizeup.firstduesizeup.com/responderV2/index" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Scheduling</span><span class="lcard-s">First Due SizeUp</span></a>
</div>

## Training & Credentialing {#training}

<div class="lgrid">
  <a class="lcard lcard--live" href="https://www.vdh.virginia.gov/emergency-medical-services/education-certification/ems-provider-portal-2/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Virginia EMS Portal</span><span class="lcard-s">VDH OEMS — certification &amp; CE record</span></a>
  <a class="lcard lcard--live" href="https://www.vafire.com/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">VA Dept. of Fire Programs</span><span class="lcard-s">Fire service training &amp; news</span></a>
  <span class="lcard lcard--pending" aria-disabled="true">
    <span class="lcard-t">Cornerstone LMS</span><span class="lcard-s">URL unconfirmed — see note below</span></span>
</div>

## City & Department {#city}

<div class="lgrid">
  <a class="lcard lcard--live" href="https://www.poquoson-va.gov/177/Fire-Rescue" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">Poquoson Fire &amp; Rescue</span><span class="lcard-s">Department page on the city site</span></a>
  <a class="lcard lcard--live" href="https://www.poquoson-va.gov/" target="_blank" rel="noopener noreferrer">
    <span class="lcard-t">City of Poquoson</span><span class="lcard-s">Government, utilities, agendas</span></a>
  <a class="lcard lcard--live" href="../personnel-policies/index.html">
    <span class="lcard-t">Personnel Policy Manual</span><span class="lcard-s">Leave, pay, conduct, promotion</span></a>
</div>

???+ danger "Cornerstone is listed but not linked — on purpose"
    The address given for Cornerstone (`vafire.csod.com`) **does not resolve from the public
    internet** — DNS returns NXDOMAIN. Publishing it would hand crew a tile that only ever
    says "this site can't be reached", and guessing a look-alike host for a login page is
    exactly how credential phishing starts. Send the correct host to the site maintainer and
    this tile goes live in one edit.

---

??? info "Maintenance rules (why these links look the way they do)"
    1. **Never paste a URL copied out of your browser's address bar after logging in.** The
       VendNova link arrived as `/u/login/identifier?state=<blob>`. That blob is a one-time
       Auth0 handoff (it decodes to a tenant id and client id — no credentials, but it
       expires). The site's own root, `ems.vendnovation.com/`, mints a fresh one by itself,
       which is why the root is what is published here.
    2. **Publish the destination, not the redirect.** Three of these moved: the city's site is
       now `poquoson-va.gov` (the old `ci.poquoson.va.us` still redirects), `vafire.com` lands
       on the Dept. of Fire Programs, and SizeUp settles on `/auth/signin-v2`. Links were
       rewritten to where they actually end up, and each was opened in a real browser first —
       not just `curl`, which the Dept. of Forestry blocks (it answers 403 to scripts, 200 to
       a phone).
    3. **No private addresses.** Nothing on `10.x`, `192.168.x`, `.local`, or a station-only
       host — if it does not resolve on LTE, it does not belong here.
    4. **No credential guidance.** No username formats, password rules, reset procedures,
       staffing patterns or who-is-on-which-shift text. This page is `noindex` and out of the
       sitemap, but the site itself is public — assume it can be read.
    5. **Keep `robots: noindex` in the front matter.** `overrides/main.html` emits
       `<meta name="robots" content="noindex, nofollow">` and
       `scripts/mkdocs_post_build.py` drops the page from `sitemap.xml`.
    6. **Group anchors are load-bearing.** The home page's "Crew Links & Portals" door points
       at `#response` `#doc` `#readiness` `#training` `#city` — they are hand-written `{#ids}`
       so renaming a heading does not silently break the strip.
