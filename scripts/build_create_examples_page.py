#!/usr/bin/env python3
"""Build the self-contained create-examples page.

The page at ``docs/create-examples/index.html`` is the one-stop maintainer tool
for turning a tool session into a published example. It assembles, from their
canonical sources at build time so nothing drifts:

- the **output collector prompt**, read from the testing pack
  (``docs/audit-library/latest/ai_tutor_toolkit_output_collector.md``);
- the **example cards**, read from ``docs/create-examples/example-cards.md``;
- the **converter**, read from ``src/examples-tools/collector-to-snippet.js``
  and inlined so the conversion runs directly on this page.

Re-run whenever any of those sources change.

Usage::

    python scripts/build_create_examples_page.py
    python scripts/build_create_examples_page.py --check
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
JS_SRC = ROOT / "src" / "examples-tools" / "collector-to-snippet.js"
CARDS = DOCS / "create-examples" / "example-cards.md"
COLLECTOR_MD = DOCS / "audit-library" / "latest" / "ai_tutor_toolkit_output_collector.md"
PAGE = DOCS / "create-examples" / "index.html"

FAMILY_ORDER = [
    "writing-tutor",
    "structure-tutor",
    "academic-thinking",
    "research-proposal",
    "study-workflow",
]
FAMILY_LABELS = {
    "writing-tutor": "Writing Tutor",
    "structure-tutor": "Structure Tutor",
    "academic-thinking": "Academic Thinking Tutor",
    "research-proposal": "Research Proposal Tutor",
    "study-workflow": "Study Workflow Tutor",
}

NAV = (
    '<header><div class="container nav"><a class="brand" href="../index.html">'
    "AI Personal Tutor Toolkit<small>Structured writing support</small></a>"
    "<nav><ul>"
    '<li><a href="../index.html">Home</a></li>'
    '<li><a href="../where-to-start/">Where to start?</a></li>'
    '<li><a href="../try-it/">Try It</a></li>'
    '<li><a href="../tools/">Tools</a></li>'
    '<li><a href="../examples/">Examples</a></li>'
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


def read_collector_prompt() -> str:
    text = COLLECTOR_MD.read_text(encoding="utf-8")
    m = re.search(
        r"(Stop acting as the tutor toolkit.*?\*\*END OF COLLECTOR PROMPT\*\*)",
        text,
        re.DOTALL,
    )
    if not m:
        raise SystemExit("Could not find the collector prompt body in the pack file.")
    return m.group(1).strip()


def parse_cards_md(text: str, valid_codes: set[str]) -> list[dict]:
    """Parse the Markdown example-cards file into card dicts, with validation.

    Format per card:
        ## CODE — Title
        **Scenario:** ...
        **Shows:** ...
        ### Input            (or ### Input 1, ### Input 2, ...)
        ```
        verbatim input
        ```
    Raises SystemExit with a clear message on any structural problem.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    cards: list[dict] = []
    errors: list[str] = []
    i = 0
    n = len(lines)

    card_head = re.compile(r"^##\s+([A-Za-z]{2}\d{1,2})\b\s*(?:[—-].*)?$")
    input_head = re.compile(r"^###\s+Input\b", re.IGNORECASE)
    label = re.compile(r"^\*\*(Scenario|Shows):\*\*\s*(.*)$", re.IGNORECASE)

    while i < n:
        m = card_head.match(lines[i])
        if not m:
            i += 1
            continue
        code = m.group(1).upper()
        start_line = i + 1
        i += 1
        scenario = shows = None
        inputs: list[str] = []
        # consume until the next card heading
        while i < n and not card_head.match(lines[i]):
            lab = label.match(lines[i])
            if lab:
                if lab.group(1).lower() == "scenario":
                    scenario = lab.group(2).strip()
                else:
                    shows = lab.group(2).strip()
                i += 1
                continue
            if input_head.match(lines[i]):
                i += 1
                # skip blank lines up to the fence
                while i < n and lines[i].strip() == "":
                    i += 1
                if i >= n or not re.match(r"^(`{3,}|~{3,})", lines[i]):
                    errors.append(f"{code}: an '### Input' is not followed by a fenced code block (line {i+1}).")
                    continue
                fence = re.match(r"^(`{3,}|~{3,})", lines[i]).group(1)
                i += 1
                buf: list[str] = []
                while i < n and lines[i].strip() != fence and not lines[i].startswith(fence):
                    buf.append(lines[i])
                    i += 1
                i += 1  # closing fence
                inputs.append("\n".join(buf).strip("\n"))
                continue
            i += 1
        # validate this card
        if code not in valid_codes:
            errors.append(f"{code} (line {start_line}): code is not in the tool index.")
        if not scenario:
            errors.append(f"{code}: missing '**Scenario:**' line.")
        if not shows:
            errors.append(f"{code}: missing '**Shows:**' line.")
        if not inputs:
            errors.append(f"{code}: no inputs found (need at least one '### Input' + fenced block).")
        if any(not s.strip() for s in inputs):
            errors.append(f"{code}: an input block is empty.")
        cards.append({"code": code, "scenario": scenario or "", "shows": shows or "", "inputs": inputs})

    seen = [c["code"] for c in cards]
    dupes = {c for c in seen if seen.count(c) > 1}
    if dupes:
        errors.append("Duplicate cards for: " + ", ".join(sorted(dupes)))
    missing = sorted(valid_codes - set(seen))
    if missing:
        errors.append("No card for tool(s): " + ", ".join(missing))

    if errors:
        raise SystemExit("Example-cards validation failed:\n  - " + "\n  - ".join(errors))
    return cards


def load_tool_order() -> dict[str, dict]:
    data = json.loads((DOCS / "data" / "tool_index.json").read_text(encoding="utf-8"))
    return {t["code"]: t for t in data["tools"]}


def render_cards(cards: list[dict], tools: dict[str, dict]) -> str:
    by_family: dict[str, list[dict]] = {f: [] for f in FAMILY_ORDER}
    for card in cards:
        fam = tools.get(card["code"], {}).get("family", "")
        by_family.setdefault(fam, []).append(card)

    out: list[str] = []
    counter = 0
    for fam in FAMILY_ORDER:
        items = by_family.get(fam, [])
        if not items:
            continue
        out.append(f'<h3>{html.escape(FAMILY_LABELS[fam])}</h3>')
        for card in items:
            counter += 1
            code = html.escape(card["code"])
            title = html.escape(tools.get(card["code"], {}).get("title", ""))
            scenario = html.escape(card["scenario"])
            shows = html.escape(card["shows"])
            out.append(f'<div class="excard">')
            out.append(f'<h4>{code} — {title}</h4>')
            out.append(f'<p class="excard-scenario">{scenario}</p>')
            out.append(f'<p class="excard-shows"><strong>Example shows:</strong> {shows}</p>')
            for j, inp in enumerate(card["inputs"], start=1):
                counter += 1
                bid = f"exc{counter}"
                label = "Input" if len(card["inputs"]) == 1 else f"Input {j}"
                out.append(
                    f'<div class="copywrap"><button class="button small-button" '
                    f"onclick=\"copyBox('{bid}',this)\">Copy {label.lower()}</button>"
                    f'<pre id="{bid}"><code>{html.escape(inp)}</code></pre></div>'
                )
            out.append("</div>")
    return "\n".join(out)


def build_page(collector_prompt: str, cards_html: str, js: str) -> str:
    collector_escaped = html.escape(collector_prompt)
    return f"""<!DOCTYPE html>

<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Create an example | AI Personal Tutor Toolkit</title>
<meta content="One-stop maintainer tool: run an example card, capture it with the collector, and convert it to an example chat snippet in your browser." name="description"/>
<link href="../style.css" rel="stylesheet"/>
<style>
button.button{{cursor:pointer;font:inherit;font-weight:800}}
.small-button{{font-size:13px;padding:6px 10px}}
.copywrap{{margin:10px 0}}
.copywrap textarea{{width:100%;min-height:200px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff}}
.copywrap pre{{margin:8px 0 0;max-height:320px;overflow:auto;border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff}}
.excard{{border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:14px 0;background:#fff}}
.excard h4{{margin:0 0 6px}}
.excard-scenario{{margin:0 0 6px}}
.excard-shows{{margin:0 0 10px;font-size:14px;color:var(--muted,#555)}}
.meta{{font-size:14px;color:var(--muted,#555);margin:8px 0}}
.warn{{color:#9a3b00}}
details.cardlib > summary{{cursor:pointer;font-weight:800;margin:6px 0}}
</style>
</head>
<body>
{NAV}
<main>
<article class="reading"><header class="page-intro"><p class="kicker">Maintainer guide · Examples</p><h1>Create an example</h1><p class="lead">Run one example card in a tool, capture the session with the collector prompt, and convert it to an example chat snippet — all from this page. The conversion runs in your browser; nothing is sent anywhere.</p></header>

<section>
<h2 id="steps">The four steps</h2>
<ol>
<li><strong>Run a card.</strong> Open a fresh chat, upload the relevant library, type <code>prompt</code>, choose the tool, and paste the inputs from its example card below (in order, letting the tool respond each time). Pick a clean, representative run — examples are shop-window content.</li>
<li><strong>Capture.</strong> When the session is complete, paste the collector prompt (below) as the final message. The AI produces a Markdown test record.</li>
<li><strong>Convert.</strong> Paste that record into the converter below and select Convert. Copy the snippet it produces.</li>
<li><strong>Place and build.</strong> Save the snippet as the filename shown, in <code>src/examples/</code>. Then run <code>python scripts/build_example_pages.py</code> and <code>python scripts/build_site_pages.py</code>.</li>
</ol>
<p class="meta"><strong>Spot-check.</strong> The record is produced by the same AI that was tested, so compare at least one turn of the snippet against the live chat before saving. Edit the <code>&lt;!-- lead: ... --&gt;</code> line in the snippet to set the example's intro sentence.</p>
</section>

<section>
<h2 id="collector">1 · Collector prompt</h2>
<p>Paste this as the final message of the session, after the last tool turn. It is the same canonical prompt used for audit records.</p>
<div class="copywrap"><button class="button" onclick="copyBox('collectorprompt',this)">Copy collector prompt</button><pre id="collectorprompt"><code>{collector_escaped}</code></pre></div>
</section>

<section>
<h2 id="cards">2 · Example cards</h2>
<p>One clean scenario per tool. These are written for examples, not audits, so they avoid the adversarial decoys in the test cards. The full audit cards remain in the <a href="../testing-cards.html">test-cards</a> pack.</p>
{cards_html}
</section>

<section>
<h2 id="convert">3 · Convert a record to a snippet</h2>
<div class="copywrap">
<label for="inputmd"><strong>Paste the collector record</strong></label>
<textarea id="inputmd" placeholder="# Test record: WT2 — Clarity Clinic&#10;&#10;## Metadata&#10;...&#10;## Transcript&#10;### Turn 1 — Toolkit&#10;..."></textarea>
</div>
<div class="btn-row"><button class="button" id="convertbtn">Convert</button></div>
<div id="status" class="meta"></div>
<div class="copywrap">
<label for="outputhtml"><strong>Snippet</strong> — save as <code id="filename">(convert to see filename)</code> in <code>src/examples/</code></label>
<div class="btn-row"><button class="button" id="copybtn">Copy snippet</button></div>
<pre id="outputhtml"><code></code></pre>
</div>
</section>
</article>
</main>
{FOOTER}
<script>
function copyBox(id, btn){{
  var el=document.getElementById(id);
  var text=el ? el.textContent : '';
  if(!text){{return;}}
  navigator.clipboard.writeText(text).then(function(){{
    var t=btn.textContent; btn.textContent='Copied'; setTimeout(function(){{btn.textContent=t;}},1200);
  }});
}}
</script>
<script>
{js}
</script>
<script>
(function(){{
  var input=document.getElementById('inputmd');
  var status=document.getElementById('status');
  var out=document.getElementById('outputhtml').querySelector('code');
  var fname=document.getElementById('filename');
  function run(){{
    var md=input.value||'';
    if(!md.trim()){{status.textContent='Paste a collector record first.';return;}}
    var r=CollectorToSnippet.convert(md);
    out.textContent=r.html;
    fname.textContent=r.filename;
    var msg='Converted '+r.turns.length+' turn(s)';
    if(r.code) msg+=' · code '+r.code;
    if(r.title) msg+=' · '+r.title;
    if(r.warnings.length){{
      status.innerHTML=msg+' · <span class="warn">'+r.warnings.length+' warning(s): '+r.warnings.join('; ')+'</span>';
    }} else {{
      status.textContent=msg+' · no warnings';
    }}
  }}
  document.getElementById('convertbtn').addEventListener('click',run);
  document.getElementById('copybtn').addEventListener('click',function(){{
    var text=out.textContent; if(!text){{return;}}
    navigator.clipboard.writeText(text).then(function(){{
      var b=document.getElementById('copybtn');var t=b.textContent;b.textContent='Copied';setTimeout(function(){{b.textContent=t;}},1200);
    }});
  }});
}})();
</script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit non-zero if the page is stale")
    args = ap.parse_args()

    collector = read_collector_prompt()
    tools = load_tool_order()
    cards = parse_cards_md(CARDS.read_text(encoding="utf-8"), set(tools.keys()))
    cards_html = render_cards(cards, tools)
    js = JS_SRC.read_text(encoding="utf-8")
    page = build_page(collector, cards_html, js)

    existing = PAGE.read_text(encoding="utf-8") if PAGE.exists() else None
    if existing == page:
        print("Create-examples page up to date.")
        return 0
    if args.check:
        print("Create-examples page is stale; run build_create_examples_page.py")
        return 1
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"Wrote {PAGE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
