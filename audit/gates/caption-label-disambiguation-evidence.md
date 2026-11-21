# Card t_a4b01dd6 — "EMS HUB" over a chip called "EMS Hub": measured evidence

Branch `caption-labels-r2`, base `origin/main 73766d97`, merge of main into the
branch first (`ebc5614f`), then the content commit.

Everything below was measured on the **built** site (`mkdocs build --strict`,
exit 0), served over `file://`, viewport 390×844 @ DPR 2, transitions disabled
before the scheme switch (Material fades link colours over ~125 ms and would
otherwise report the previous scheme's colour).

## 1. The two collisions are gone

| row | caption (label) | first chip | href (unchanged) |
|---|---|---|---|
| EMS | `EMS Hub` | **`EMS Clinical Hub`** | `ems/index.html` |
| Fire | `Fire resources` | **`Reference shelf`** | `resources/fire-resources.html` |
| Admin | `City & personnel policies` | **`Station Policies`** | `station/policies.html` |
| Util | `Crew links & portals` | `All Links` | `resources/links.html` |

The admin row was the same collision as the two the card named — caption
"City & personnel policies", chip "City & Personnel Policies", equal once case
and `&` are ignored — so it was renamed too rather than left as a hole in the
new guard. No href changed: all four first chips still point at their section
page, and the guard checks exactly that.

Measured at 390 px, both schemes:

```
scrollWidth - clientWidth = 0          (no horizontal overflow)
anchors inside .pfd-cap    = 0          (captions still plain labels)
every chip height          = 44 px      (13 + 5 + 7 + 10 = 35 chips)
```

## 2. The `all` chip is neutral now, not maroon

`All protocols` / `Reference shelf` carried `.pfd-chip--all`, which had no
`--pfd-accent` of its own and fell back to the maroon brand primary `#800000` —
the same hue family as FIRE `#b91c1c`, inside the blue EMS row.

Now, measured as computed style:

| scheme | `.pfd-chip--all` accent | label ink | chip tint bg | ink contrast | bar contrast |
|---|---|---|---|---|---|
| default | `#3f3f46` | `#27272a` | `rgb(236,236,237)` | **12.62:1** | **8.85:1** |
| slate | `#a1a1aa` | — (inherits) | `rgb(44,46,54)` | — | **5.28:1** |

Both above the 4.5:1 text / 3:1 UI floors. Linear-RGB distance from the
neighbouring hues (0–100, larger = more different):

```
maroon #800000   vs FIRE #b91c1c : 27.0     <- what it used to look like
zinc   #3f3f46   vs FIRE #b91c1c : 44.0
zinc   #3f3f46   vs EMS  #0284c7 : 54.3
zinc   #3f3f46   vs ADMIN #475569:  9.1     <- grey reads as the admin grey, stated plainly
```

The zinc accent is only 9.1 away from the admin slate. That is accepted, not
overlooked: admin chips live in the secondary row and never share a row with an
`all` chip, and the label ("All protocols") already says it is not a policy. The
point of the change was to stop an `all` chip reading as **fire** inside the EMS
row; that distance went from 27 to 44 and the hue is now achromatic.

## 3. The guard that would have caught it

`scripts/check_caption_labels.py` rule 3: no chip label may equal its own row's
caption, case-insensitive, punctuation ignored (`_norm_label` strips everything
but `[a-z0-9]`). Captions and rows are paired by document order — each row takes
the last caption emitted before it — so a caption is never matched to a row it
does not head.

`audit/gates/caption_label_negative.py` proves the rule bites. It copies the
built homepage into a temp dir and requires the guard to fail:

```
clean copy                    EXIT=0
planted 'EMS Hub'             EXIT=1  chip "EMS Hub" (ems/index.html) repeats its row caption "EMS Hub"
planted 'Fire resources'      EXIT=1  chip "Fire resources" (...) repeats its row caption "Fire resources"
planted 'City & Personnel Policies' EXIT=1  ... repeats its row caption "City & personnel policies"
restored                      EXIT=0
```

## 4. Gates

`bash audit/gates/run_gates_caption_labels.sh` — 21 gates, **ALL GATES EXIT=0**
(log: `audit/gates/caption-labels-<sha>.log`). Two things worth stating:

- `verify_pems_canonical` needs the git-ignored
  `audit/level-scan/.cache/pems_rows.jsonl`; a fresh worktree does not have it,
  so the file was copied from the main checkout's cache before the run. It is not
  committed (gitignored). Card t_7b6df26e documented this exact trap.
- `slate_untouched` permits exactly two slate-selector lines: the removed maroon
  `pfd-chip--all` accent and the added zinc one. Everything else in the dark
  scheme is untouched.
