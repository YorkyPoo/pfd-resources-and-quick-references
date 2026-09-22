#!/usr/bin/env python3
"""Generate the PWA icons + favicon referenced by docs/manifest.webmanifest.

mkdocs.yml/theme reference `assets/images/favicon.png` (mkdocs-material's
default) and manifest.webmanifest references `icon-192.png` / `icon-512.png`
at the site root. None of these files existed, so every page emitted a 404
for the favicon and the PWA install icons failed to load.

Design: navy field, white medical cross, red flame accent.
Content stays inside the inner 80% so `purpose: maskable` crops cleanly.
"""
import os
from PIL import Image, ImageDraw

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
NAVY = (22, 33, 62, 255)
WHITE = (245, 247, 250, 255)
RED = (200, 40, 45, 255)


def make_icon(size: int, maskable: bool = True) -> Image.Image:
    img = Image.new("RGBA", (size, size), NAVY)
    d = ImageDraw.Draw(img)

    # safe zone: maskable icons must keep key art inside a centred circle of 80%
    inset = 0.22 * size if maskable else 0.12 * size
    box = (inset, inset, size - inset, size - inset)
    w = int((box[2] - box[0]) * 0.34)          # cross arm thickness
    cx = (box[0] + box[2]) / 2

    # vertical arm
    d.rounded_rectangle(
        [cx - w / 2, box[1], cx + w / 2, box[3]],
        radius=w * 0.18, fill=WHITE,
    )
    # horizontal arm
    cy = (box[1] + box[3]) / 2
    d.rounded_rectangle(
        [box[0], cy - w / 2, box[2], cy + w / 2],
        radius=w * 0.18, fill=WHITE,
    )
    # flame accent over the cross centre
    fr = w * 0.78
    d.ellipse([cx - fr, cy - fr * 1.25, cx + fr, cy + fr * 0.75], fill=RED)
    d.polygon(
        [(cx, cy - fr * 2.05), (cx + fr * 0.62, cy - fr * 0.55), (cx - fr * 0.62, cy - fr * 0.55)],
        fill=RED,
    )
    d.ellipse([cx - fr * 0.42, cy - fr * 0.25, cx + fr * 0.42, cy + fr * 0.72], fill=NAVY)
    return img


def main() -> None:
    targets = [
        (os.path.join(DOCS, "assets", "images", "favicon.png"), 64, False),
        (os.path.join(DOCS, "icon-192.png"), 192, True),
        (os.path.join(DOCS, "icon-512.png"), 512, True),
    ]
    for path, size, maskable in targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        make_icon(size, maskable).save(path, "PNG", optimize=True)
        print(f"wrote {size}x{size}  {os.path.relpath(path, DOCS)}")


if __name__ == "__main__":
    main()