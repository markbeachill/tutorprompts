#!/usr/bin/env python3
"""Generate example pages by wrapping hand-editable chat snippets.

Each tool's example conversation lives as a standalone, hand-editable HTML
snippet at ``src/examples/{code}-example-chat.html``. A snippet is the complete
chat region (the ``ai-chat-page`` block and its turns) and nothing else - no
page head, nav or footer. It is exactly the kind of markup the ai-chat-to-html
converter (or a "make-example" chat prompt) produces, so a captured snippet can
be dropped in with no translation.

This script reads each snippet, wraps it in the standard example-page furniture
(head, nav, page intro, footer), and writes
``docs/examples/example-{code}.html``. Tool ``code`` and ``title`` come from
``docs/data/tool_index.json`` so titles never drift. The generated pages are
auto-detected by ``build_site_pages.py`` (examples index, tool cards, "Example"
buttons), so no manual wiring is needed.

The page intro ``lead`` line is editorial. If a snippet begins with an HTML
comment of the form ``<!-- lead: ... -->`` that text is used; otherwise a
placeholder is emitted for a human to replace.

Usage::

    python scripts/build_example_pages.py            # write/refresh all pages
    python scripts/build_example_pages.py --check     # fail if any page is stale
    python scripts/build_example_pages.py --only AT2  # one tool

After generating, run ``python scripts/build_site_pages.py`` to refresh the
examples index and tool-card links.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SNIPPETS = ROOT / "src" / "examples"
TOOL_INDEX = DOCS / "data" / "tool_index.json"
EXAMPLES_DIR = DOCS / "examples"

LEAD_PLACEHOLDER = "REPLACE ME WITH A ONE-LINE INTRODUCTION TO THIS EXAMPLE."
LEAD_RE = re.compile(r"<!--\s*lead:\s*(.*?)\s*-->", re.IGNORECASE | re.DOTALL)

NAV = (
    '<header><div class="container nav"><a class="brand" href="../index.html">'
    "AI Personal Tutor Toolkit<small>Structured writing support</small></a>"
    "<nav><ul>"
    '<li><a href="../index.html">Home</a></li>'
    '<li><a href="../where-to-start/">Where to start?</a></li>'
    '<li><a href="../try-it/">Try It</a></li>'
    '<li><a href="../tools/">Tools</a></li>'
    '<li><a class="active" aria-current="page" href="../examples/">Examples</a></li>'
    '<li><a href="../student-help/">Student Help</a></li>'
    '<li><a href="../guides/">Guides</a></li>'
    '<li><a href="../download/">Download</a></li>'
    "</ul></nav></div></header>"
)

FOOTER = (
    '<footer class="footer"><div class="container">'
    "<p>AI Personal Tutor Toolkit. Structured writing support for learning-focused AI use.</p>"
    '<p class="footer-links"><a href="../changelog/">Changelog</a> | '
    '<a href="https://github.com/markbeachill/tutorprompts" rel="noopener noreferrer" '
    'target="_blank">GitHub</a> | <a href="../about.html">About this site</a></p>'
    "</div></footer>"
)


def load_tools() -> dict:
    data = json.loads(TOOL_INDEX.read_text(encoding="utf-8"))
    return {t["code"]: t for t in data["tools"]}


def snippet_path(code: str) -> Path:
    return SNIPPETS / f"{code.lower()}-example-chat.html"


def parse_snippet(raw: str):
    """Return (lead, chat_html). Pull an optional ``<!-- lead: ... -->`` header."""
    lead = LEAD_PLACEHOLDER
    m = LEAD_RE.search(raw)
    if m:
        lead = m.group(1).strip()
        raw = LEAD_RE.sub("", raw, count=1)
    return lead, raw.strip()


def build_page(code: str, title: str, lead: str, chat_html: str) -> str:
    return f"""<!DOCTYPE html>

<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>{code} {title} example | AI Personal Tutor Toolkit</title>
<meta content="Worked example page for {code} {title}." name="description"/>
<link href="../style.css" rel="stylesheet"/>
<link href="../css/aichat.css" rel="stylesheet"/>
</head>
<body>
{NAV}
<main>
<article class="reading">
<header class="page-intro">
<h1>Example: {code} — {title}</h1>
<p class="lead">{lead}</p>
</header>
</article>

<!-- ************************************** -->
<!-- ************************************** -->
<!-- START OF THE EXAMPLE CHAT -->
<!-- ************************************** -->
<!-- ************************************** -->

{chat_html}
<!-- ************************************** -->
<!-- ************************************** -->
<!-- END OF THE EXAMPLE CHAT -->
<!-- ************************************** -->
<!-- ************************************** -->
</main>
{FOOTER}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="exit non-zero if any page would change")
    parser.add_argument("--only", metavar="CODE",
                        help="generate only this tool code (e.g. AT2)")
    args = parser.parse_args()

    tools = load_tools()
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    if args.only:
        codes = [args.only.upper()]
    else:
        codes = sorted(
            p.name[: -len("-example-chat.html")].upper()
            for p in SNIPPETS.glob("*-example-chat.html")
        )

    stale = []
    written = []
    missing_snippet = []

    for code in codes:
        if code not in tools:
            print(f"  skip {code}: not in tool_index.json", file=sys.stderr)
            continue
        sp = snippet_path(code)
        if not sp.exists():
            missing_snippet.append(code)
            continue
        lead, chat_html = parse_snippet(sp.read_text(encoding="utf-8"))
        page = build_page(code, tools[code]["title"], lead, chat_html)
        path = EXAMPLES_DIR / f"example-{code.lower()}.html"
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        if existing == page:
            continue
        if args.check:
            stale.append(code)
        else:
            path.write_text(page, encoding="utf-8")
            written.append(code)

    if missing_snippet:
        print(f"  note: no snippet for {', '.join(missing_snippet)} "
              f"(add src/examples/<code>-example-chat.html)", file=sys.stderr)

    if args.check:
        if stale:
            print("Stale example pages:", ", ".join(stale))
            return 1
        print("All example pages up to date.")
        return 0

    print(f"Wrote {len(written)} example page(s): {', '.join(written) or '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
