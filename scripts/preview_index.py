#!/usr/bin/env python3
"""Regenerate the /preview/ index (and robots.txt) from preview/slots.json.

    python3 scripts/preview_index.py <gh-pages-worktree>

`preview/slots.json` is the single source of truth for which slots exist:

    {"slots": {"pilot": {"branch": "...", "sha": "...", "description": "...",
                         "built_at": "2026-11-20T05:00:00Z"}}}

The index lists every slot with its one-line description, the branch and short
SHA it was built from, and the build timestamp, so a reviewer can state
provenance unambiguously. The index itself is noindex/nofollow like every other
preview page.
"""
import datetime
import html
import json
import os
import shutil
import sys

BASE = "https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Preview slots — Poquoson Fire &amp; Rescue Protocols</title>
<style>
  body {{ background:#16213e; color:#e8e8e8; font:16px/1.5 system-ui, sans-serif;
         margin:0; padding:2rem 1.25rem; }}
  main {{ max-width:60rem; margin:0 auto; }}
  h1 {{ font-size:1.5rem; margin:0 0 .25rem; }}
  p.lede {{ color:#a9b4c9; margin:.25rem 0 1.75rem; }}
  table {{ border-collapse:collapse; width:100%; }}
  th, td {{ text-align:left; padding:.6rem .5rem; border-bottom:1px solid #2c3a5e;
            vertical-align:top; }}
  th {{ color:#a9b4c9; font-weight:600; font-size:.85rem; text-transform:uppercase;
        letter-spacing:.04em; }}
  a {{ color:#7fb2ff; }}
  code {{ background:#0f1830; padding:.1rem .35rem; border-radius:3px; font-size:.85em; }}
  .meta {{ color:#8b97ad; font-size:.85rem; }}
  footer {{ margin-top:2rem; color:#8b97ad; font-size:.8rem; }}
</style>
</head>
<body>
<main>
<h1>Preview slots</h1>
<p class="lede">Each slot is built from one branch/commit and lives at its own
subpath, so parallel cards cannot overwrite each other. Not indexed; no service
worker anywhere under <code>/preview/</code>.</p>
<table>
<thead><tr><th>Slot</th><th>What it is</th><th>Built from</th><th>Built</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<footer>Index regenerated {now}. Live site: <a href="../">root</a>.</footer>
</main>
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: preview_index.py <gh-pages-worktree>")
    work = sys.argv[1]
    preview = os.path.join(work, "preview")
    os.makedirs(preview, exist_ok=True)

    manifest_path = os.path.join(preview, "slots.json")
    manifest: dict = {"slots": {}}
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
    slots = manifest.get("slots", {})

    # The pre-slots layout served a full site build at preview/ root. Once any
    # slot exists, anything at that root that is not the index, robots.txt,
    # slots.json or a known slot is stale legacy content: remove it so
    # /preview/ is an index and nothing else. Never touches live-root paths.
    keep = {"index.html", "robots.txt", "slots.json"} | set(slots)
    pruned = []
    for entry in sorted(os.listdir(preview)):
        if entry in keep:
            continue
        p = os.path.join(preview, entry)
        if os.path.isdir(p) and not os.path.islink(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
        pruned.append(entry)
    if pruned:
        print("pruned legacy preview-root entries:", ", ".join(pruned))

    rows = []
    for name in sorted(slots):
        rec = slots[name]
        desc = html.escape(rec.get("description", ""))
        branch = html.escape(rec.get("branch", "?"))
        sha = html.escape((rec.get("sha") or "")[:7])
        built = html.escape(rec.get("built_at", ""))
        href = html.escape(f"{name}/index.html")
        rows.append(
            f'<tr><td><a href="{href}"><code>{html.escape(name)}/</code></a></td>'
            f"<td>{desc}</td>"
            f'<td><code>{branch}</code> @ <code>{sha}</code></td>'
            f'<td class="meta">{built}</td></tr>'
        )
    if not rows:
        rows.append('<tr><td colspan="4">No slots published.</td></tr>')

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(os.path.join(preview, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PAGE.format(rows="\n".join(rows), now=now))

    with open(os.path.join(preview, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nDisallow: /\n")

    manifest["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"regenerated {os.path.join(preview, 'index.html')} with {len(slots)} slot(s): "
          + ", ".join(sorted(slots)))


if __name__ == "__main__":
    main()
