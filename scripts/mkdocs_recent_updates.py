# mkdocs_recent_updates.py — inject git-derived "New & Updated" + build stamp into pages
# Placeholders: {! recent !}  -> recent changes list ;  {! lastbuild !} -> commit/date stamp
import subprocess
from datetime import datetime, timezone
from pathlib import Path

_CACHE = {}

def _git_root(config):
    return str(Path(config["config_file_path"]).parent)

def _run(args, root):
    try:
        return subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return ""

def _recent_html(config):
    if "recent" in _CACHE:
        return _CACHE["recent"]
    root = _git_root(config)
    raw = _run(["git", "log", "--since=45 days ago", "--date=short",
                "--pretty=format:@@%h@@%ad@@%s", "--name-only", "-n", "40"], root)
    if not raw.strip():
        _CACHE["recent"] = "<p><em>No recent changes to report.</em></p>"
        return _CACHE["recent"]
    items = []
    cur = None
    for line in raw.splitlines():
        if line.startswith("@@"):
            _, sha, date, msg = line.split("@@")
            cur = {"sha": sha, "date": date, "msg": msg, "files": []}
            items.append(cur)
        elif line.strip() and cur is not None:
            f = line.strip()
            if f.startswith("docs/") and f.endswith(".md"):
                cur["files"].append(f[5:])
            if len(items) >= 12:
                break
    out = ['<ul class="recent-list">']
    for it in items:
        links = []
        for f in it["files"][:4]:
            url = f[:-3] + ".html"
            label = Path(f).stem.replace("-", " ").replace("_", " ")
            links.append('<a href="{}">{}</a>'.format(url, label))
        more = "<span class='recent-more'>+{} more</span>".format(len(it["files"]) - 4) if len(it["files"]) > 4 else ""
        out.append(
            '<li><span class="recent-date">{d}</span> <b>{m}</b>'
            '{links}<span class="recent-sha">{s}</span></li>'.format(
                d=it["date"], m=it["msg"][:80], s=it["sha"],
                links=("<div class='recent-files'>" + " · ".join(links) + more + "</div>") if links else ""))
    out.append("</ul>")
    html = "".join(out)
    _CACHE["recent"] = html
    return html

def _lastbuild(config):
    if "stamp" in _CACHE:
        return _CACHE["stamp"]
    root = _git_root(config)
    sha = _run(["git", "rev-parse", "--short", "HEAD"], root).strip()
    date = _run(["git", "log", "-1", "--date=iso-strict", "--pretty=format:%ad"], root).strip()
    when = date[:16].replace("T", " ") + " UTC" if date else datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    _CACHE["stamp"] = "{} · build of {}".format(sha, when) if sha else when
    return _CACHE["stamp"]

def on_page_markdown(markdown, page, config, files, **kwargs):
    if "{! recent !}" in markdown:
        markdown = markdown.replace("{! recent !}", _recent_html(config))
    if "{! lastbuild !}" in markdown:
        markdown = markdown.replace("{! lastbuild !}", _lastbuild(config))
    return markdown
