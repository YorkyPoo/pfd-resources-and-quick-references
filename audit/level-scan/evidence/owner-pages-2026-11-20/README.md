# Owner-supplied PEMS page photographs — captured 2026-11-20

These are the owner's own photographs of the printed PEMS 2024 pages. They are **evidence**,
not source text: where a photograph and anything the pipeline derived disagree, the
photograph is the authority. Every file here is preserved byte-for-byte from the image the
owner sent — nothing is cropped, re-encoded or renamed in a lossy way.

| file | sha256 | what it shows |
|---|---|---|
| `01-airway-mgmt-p1-criteria-protocol.jpg` | `977211f1ef42a1995a127ddf9d4ee1afd58e7a0641d3a06c0da4d3c14578166a` | Airway Management and Ventilatory Support, page 1: CRITERIA + PROTOCOL table |
| `02-airway-mgmt-p2-pearls.jpg` | `94b79e8ee3dfb57c71ee184e625991f5d1a83b62329a244ced5d18c21ade9c4d` | Airway Management and Ventilatory Support, page 2: PEARLS |
| `03-ett-protocol.jpg` | `45c4e0db87e35673fede54251057bc1adb147e26d9ef9dae522d84e731da3866` | Endotracheal Intubation procedure page |
| `04-ett-pearls.jpg` | `4c2c55d33884705e0e377f7b42fdab059e3065bb533c8da4c91a79d5ce6979c0` | Endotracheal Intubation PEARLS page |
| `airway-management-cpap-2022v0722.jpg` | `f4a6c716aa7704f920e634f4767144ccd3f5b05e907ea13a39694b0b57cd02e8` | Airway Management and Ventilatory Support, page 1 of 2, **Version 2022v0722** — the CPAP row (see below) |

## The CPAP row — the printed basis of the 2026-11-20 PEEP titration ruling

`airway-management-cpap-2022v0722.jpg` is the page the owner sent on 2026-11-20 with his
ruling *"Only intermediates and above can titrate peep up to 15 mmhg"*. The CPAP row on it
reads, with its printed badges (EMT in both the left and right margin columns):

> Consider CPAP (PEEP: 5 cmH₂O) for respiratory distress. Refer to *CPAP* procedure.
> **I/P only: Adjust PEEP** to support ventilation and work of breathing, **up to 10 cmH₂O.**

The footer prints `Version: 2022v0722` and `Procedures: Airway Management and Ventilatory
Support — Page 1 of 2`.

The `I/P only` clause is the printed basis for the `I` floor on every PEEP-titration row.
It is **not** the ceiling the owner ruled: the page caps the adjustment at 10 cmH₂O, the
owner ruled 15 mmHg, and the discrepancy is recorded on purpose in
`audit/level-scan/level-rulings.yaml` (CPAP row 6) and `audit/level-scan/wording-rulings.yaml`
rather than silently reconciled on the page.

## Provenance

- Copied from the `chat` profile's native-input cache, which is prunable:
  `/root/.hermes/profiles/chat/cache/documents/native-inputs/f4a6c716aa7704f920e634f4767144ccd3f5b05e907ea13a39694b0b57cd02e8/img_6ff885b228b5.jpg`
  — the cache directory name is the file's own sha256, so the hash above also identifies the
  exact object the owner's session handed over.
- Recorded by card `t_7a22b040` (owner ruling: PEEP titration level + 15 mmHg ceiling, CPAP
  procedure row 6).
