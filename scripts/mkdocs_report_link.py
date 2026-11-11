"""Append a prefilled "report a correction" link to the end of every content page.

Why this exists: the site is a public GitHub Pages build with no backend, and the
intake is a Google Form. A bare link to the form produces reports like "the heart
thing is wrong" — the correction then has to be reverse-engineered into a page.
Google Forms accepts URL prefills (verified live: query params land in the input,
including em-dashes and pipes), so each page can hand the form its OWN title.

Two things that bit during setup, encoded here so nobody re-derives them:

1. Use the CANONICAL viewform URL, never the `forms.gle` short link. Verified: the
   short link's redirect DROPS query params, so prefill silently does nothing and
   you get an empty field with no error.
2. `page.title` is a nav title, not a filesystem name — the labels the crew actually
   see. That is the string worth prefiling.

The link is injected at build time (on_post_page), so no source file is touched:
porter-owned pages stay unmodified and `scripts/gen_connected_notes.py` never sees it.
"""
from urllib.parse import quote

FORM_ID = "1FAIpQLSdB-Pcd-hoZ9TMA09J7tUSkzpGtr_cOoLJi2w-JVZycWexa6g"
# "Which page?" — entry ids read out of the live form schema (FB_PUBLIC_LOAD_DATA_)
ENTRY_PAGE = "entry.217344317"
BASE = f"https://docs.google.com/forms/d/e/{FORM_ID}/viewform"

# Pages where a per-page report button is the wrong affordance:
#  - the homepage, which carries the full intake section and a big button;
#  - every section index / generated hub, because a hub is a LIST of links, so a
#    submission "about" it would prefill a title like "EMS Resources" and the
#    correction could not be located. Content pages keep the button; the homepage
#    link is always there as the fallback for a hub.
# NB: MkDocs Page objects have NO `src_path` attribute (probed live). The relative
# source path is `page.file.src_uri`, a str. Guessing the attribute name fails in BOTH
# directions: `getattr(page,"src_path",None) or ""` yields "" so nothing is ever
# skipped, and a `not src` guard then skips everything. Read the real attribute.
SKIP_HOMEPAGE = "index.md"


def _href(title: str) -> str:
    # quote() not quote_plus(): Forms decodes '+' inconsistently across browsers, and
    # the em-dash / pipe in real nav titles must survive (both verified in a live probe).
    return f"{BASE}?{ENTRY_PAGE}={quote(title, safe='')}"


def _skip(src: str) -> bool:
    if not src or src == SKIP_HOMEPAGE or src in {"README.md"}:
        return True
    if src.split("/")[-1] == "index.md":          # section indexes / overviews
        return True
    return src.startswith("resources/")           # generated fire+EMS hubs


def _src_uri(page) -> str:
    f = getattr(page, "file", None)
    return str(getattr(f, "src_uri", "") or "") if f is not None else ""


def on_post_page(output: str, *, page, config) -> str:
    src = _src_uri(page)
    if _skip(src):
        return output
    title = (page.title or src).strip()
    snippet = (
        f'\n<div class="report-line"><a class="report-btn" href="{_href(title)}"'
        f' target="_blank" rel="noopener">Report a correction on this page</a>'
        f'<span class="report-note">Goes to the OMD for review — nothing changes until'
        f" they approve. <strong>Never include patient names or case details.</strong></span></div>"
    )
    # Material's document body ends at </article>; inserting before it keeps the link
    # inside .md-content so it inherits typography and the footer stays below.
    marker = "</article>"
    if marker in output:
        return output.replace(marker, snippet + marker, 1)
    return output + snippet
