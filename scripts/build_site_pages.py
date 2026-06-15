#!/usr/bin/env python3
"""Build/check generated static site pages that are not prompt-library Markdown.

This script generates the task-choice and download/catalogue pages that depend on
`docs/data/tool_index.json`, then normalises the shared site navigation/footer.
Library scripts build Markdown prompt assets; this page script builds static HTML
pages that help users find and download those assets.

Typical use from the repository root:
    python scripts/build_site_pages.py

Check mode:
    python scripts/build_site_pages.py --check
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
GITHUB_URL = "https://github.com/markbeachill/tutorprompts"
GENERATOR_VERSION = "1.0"

FAMILY_ORDER = ["writing-tutor", "structure-tutor", "academic-thinking", "research-proposal", "study-workflow"]
FAMILY_LABELS = {
    "writing-tutor": "Writing Tutor",
    "structure-tutor": "Structure Tutor",
    "academic-thinking": "Academic Thinking Tutor",
    "research-proposal": "Research Proposal Tutor",
    "study-workflow": "Study Workflow Tutor",
}
FAMILY_NOTES = {
    "writing-tutor": "Sentence, paragraph, style, mistake, referencing, paraphrase and quotation tools.",
    "structure-tutor": "Paragraph, whole-draft structure and reverse-outline tools.",
    "academic-thinking": "Argument, evidence, concept, source and critical-thinking tools.",
    "research-proposal": "Research question, methodology, supervisor-review and viva-practice tools.",
    "study-workflow": "Revision planning, tutor-feedback action planning and AI-use records.",
}

CSS_BLOCK = r'''

/* Accessible heading refinement: keep strong hierarchy while reducing tight headline spacing. */
h1 {
  letter-spacing: -0.01em;
  font-weight: 700;
  line-height: 1.18;
}
h2 {
  letter-spacing: 0;
  font-weight: 650;
  line-height: 1.32;
}
body.home h1 {
  letter-spacing: -0.018em;
  font-weight: 720;
  line-height: 1.08;
}
body.home h2 {
  letter-spacing: -0.005em;
  font-weight: 680;
  line-height: 1.2;
}

/* Navigation refresh */
nav a.active,
nav a[aria-current="page"] {
  color: var(--accent);
  text-decoration: underline;
  text-underline-offset: 0.24em;
}

/* Collapsed tool catalogue and task chooser. */
.accordion-list {
  display: grid;
  gap: 12px;
  max-width: 100%;
}
.tool-section {
  background: rgba(255, 255, 255, 0.58);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0;
  max-width: 100%;
}
.tool-section > summary {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 14px;
  cursor: pointer;
  padding: 14px 16px;
  font-weight: 720;
  color: var(--ink);
  list-style: none;
}
.tool-section > summary::-webkit-details-marker { display: none; }
.tool-section > summary::before {
  content: "▸";
  margin-right: 8px;
  color: var(--accent);
}
.tool-section[open] > summary::before { content: "▾"; }
.tool-section > summary span { flex: 1; }
.tool-section > summary small {
  color: var(--muted);
  font-weight: 620;
}
.tool-section > p {
  margin: 0 16px 12px;
  color: var(--muted);
}
.tool-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  max-width: 100%;
  padding: 0 16px 16px;
}
.tool-card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: none;
  max-width: 100%;
}
.tool-card h3 {
  margin: 0 0 6px;
  font-size: 1rem;
  line-height: 1.35;
}
.tool-card p {
  font-size: 0.96rem;
  line-height: 1.55;
  margin-bottom: 0.65rem;
}
.tool-code {
  color: var(--accent2);
  font-weight: 760;
}
.tool-actions {
  gap: 7px;
  margin-top: 10px;
}
.button.small-button,
body.menu .button.small-button {
  padding: 4px 7px;
  border-radius: 7px;
  font-size: 0.82rem;
  line-height: 1.2;
  font-weight: 650;
}
.button.download-tool {
  background: transparent;
  color: var(--accent);
  border-color: var(--line-strong);
}
.download-card .button.small-button:not(.secondary) {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

/* Home layout tune only: keep the existing text and warning structure, but avoid oversized boxes with empty right-hand space. */
body.home .panel:not(#downloads) {
  max-width: var(--measure);
}
body.home .panel.notice {
  max-width: var(--measure);
}
body.home #downloads {
  max-width: 100%;
}

@media (max-width: 860px) {
  .tool-grid { grid-template-columns: 1fr; }
}
'''

@dataclass(frozen=True)
class WritePlan:
    path: Path
    text: str


def rel_prefix(path: Path, docs: Path = DOCS) -> str:
    rel_dir = path.parent.relative_to(docs)
    if str(rel_dir) == ".":
        return ""
    return "../" * len(rel_dir.parts)


def header_html(prefix: str, current: str = "") -> str:
    items = [
        ("Home", prefix + "index.html", "home"),
        ("Where to start?", prefix + "where-to-start/", "start"),
        ("Tools", prefix + "tools/", "tools"),
        ("Examples", prefix + "examples/", "examples"),
        ("Student Help", prefix + "student-help/", "student-help"),
        ("Guides", prefix + "guides/", "guides"),
        ("Download", prefix + "download/", "download"),
    ]
    lis: list[str] = []
    for label, href, key in items:
        cls = ' class="active" aria-current="page"' if key == current else ""
        lis.append(f'<li><a{cls} href="{href}">{label}</a></li>')
    return (
        '<header><div class="container nav"><a class="brand" href="'
        + prefix
        + 'index.html">AI Personal Tutor Toolkit<small>Structured writing support</small></a><nav><ul>'
        + "".join(lis)
        + "</ul></nav></div></header>"
    )


def footer_html(prefix: str) -> str:
    return (
        '<footer class="footer"><div class="container">'
        '<p>AI Personal Tutor Toolkit. Structured writing support for learning-focused AI use.</p>'
        '<p class="footer-links"><a href="'
        + prefix
        + 'changelog/">Changelog</a> | <a href="'
        + GITHUB_URL
        + '" rel="noopener noreferrer" target="_blank">GitHub</a> | <a href="'
        + prefix
        + 'about.html">About this site</a></p></div></footer>'
    )


def current_for_path(path: Path, docs: Path = DOCS) -> str:
    rel = path.relative_to(docs)
    parts = rel.parts
    if rel.as_posix() in ("index.html", "index.no.html"):
        return "home"
    first = parts[0]
    if first == "where-to-start":
        return "start"
    if first == "tools":
        return "tools"
    if first == "examples":
        return "examples"
    if first == "student-help":
        return "student-help"
    if first == "guides":
        return "guides"
    if first == "download":
        return "download"
    return ""


def replace_header_footer(text: str, prefix: str, current: str) -> str:
    text = re.sub(r'<header><div class="container nav">.*?</header>', header_html(prefix, current), text, count=1, flags=re.S)
    text = re.sub(r'<footer class="footer">.*?</footer>\s*</footer>', footer_html(prefix), text, flags=re.S)
    text = re.sub(r'<footer class="footer">.*?</footer>', footer_html(prefix), text, flags=re.S)
    return text


def read_tool_data(root: Path = ROOT) -> tuple[list[dict[str, object]], str]:
    path = root / "docs" / "data" / "tool_index.json"
    if not path.exists():
        raise SystemExit("docs/data/tool_index.json is missing. Run python scripts/build_site_data.py first.")
    tooldata = json.loads(path.read_text(encoding="utf-8"))
    tools = list(tooldata.get("tools", []))
    version = str(tooldata.get("release_version") or tooldata.get("prompt_library_version") or tooldata.get("toolkit_version") or "")
    if not tools:
        raise SystemExit("docs/data/tool_index.json does not contain any tools.")
    return tools, version


def example_exists(code: str, docs: Path = DOCS) -> bool:
    return (docs / "examples" / f"example-{code.lower()}.html").exists()


def tool_card(tool: dict[str, object], *, prefix: str = "../", include_anchor: bool = True) -> str:
    code_raw = str(tool["code"])
    code = html.escape(code_raw)
    title = html.escape(str(tool["title"]))
    desc = html.escape(str(tool.get("launcher_description") or tool.get("master_manifest_description") or ""))
    best = html.escape(str(tool.get("master_manifest_description") or tool.get("mini_manifest_description") or ""))
    output = str(tool.get("single_tool_output") or "")
    single = prefix + output.replace("docs/", "", 1)
    ex_link = ""
    if example_exists(code_raw):
        ex_link = f'<a class="button secondary small-button" href="{prefix}examples/example-{code_raw.lower()}.html">View example</a>'
    anchor = f' id="tool-{code}"' if include_anchor else ""
    return f'''<article class="tool-card"{anchor}>
<h3><span class="tool-code">{code}</span> — {title}</h3>
<p>{desc}</p>
<p class="small-note"><strong>Best for:</strong> {best}.</p>
<div class="actions tool-actions"><a class="button secondary small-button" href="{single}">Open tool file</a><a class="button secondary small-button download-tool" download href="{single}">Download this tool</a>{ex_link}</div>
</article>'''


def build_tools_page(tools: list[dict[str, object]], version: str) -> str:
    by_family: dict[str, list[dict[str, object]]] = defaultdict(list)
    for tool in tools:
        by_family[str(tool["family"])].append(tool)
    sections: list[str] = []
    for family in FAMILY_ORDER:
        items = by_family.get(family, [])
        if not items:
            continue
        cards = "\n".join(tool_card(tool, prefix="../", include_anchor=True) for tool in items)
        sections.append(f'''<details class="tool-section" id="{family}">
<summary><span>{html.escape(FAMILY_LABELS[family])}</span><small>{len(items)} tools</small></summary>
<p>{html.escape(FAMILY_NOTES[family])}</p>
<div class="tool-grid">{cards}</div>
</details>''')
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Tools | AI Personal Tutor Toolkit</title>
<meta content="A collapsed catalogue of every tool in the AI Personal Tutor Toolkit." name="description"/>
<link href="../style.css" rel="stylesheet"/><link href="../css/aichat.css" rel="stylesheet"/>
</head>
<body class="reference tools-catalogue">
{header_html("../", "tools")}
<main><article class="reading"><header class="page-intro">
<p class="kicker">Tools</p>
<h1>Browse the tool catalogue.</h1>
<p class="lead">This page only lists tools. Expand a tutor section to see the tools in that group, then open an example or download the individual tool file.</p>
<p class="small-note">Current release version: <strong>v{html.escape(version)}</strong>.</p>
</header>
<section class="panel"><p>Not sure which tool you need? Start with <a href="../where-to-start/">Where to start?</a>. To download whole libraries rather than single tools, use <a href="../download/">Download</a>.</p></section>
<section class="accordion-list wide">
{"".join(sections)}
</section>
</article></main>
{footer_html("../")}
</body>
</html>'''


def build_where_to_start_page(tools: list[dict[str, object]]) -> str:
    by_code = {str(tool["code"]): tool for tool in tools}
    def cards_for(codes: Sequence[str]) -> str:
        return "\n".join(tool_card(by_code[code], prefix="../", include_anchor=False) for code in codes if code in by_code)
    groups = [
        ("improve-draft", "I want to improve a draft", "Use these when the student has existing writing and wants focused feedback rather than a replacement draft.", ["WT1", "WT2", "WT5", "ST1"]),
        ("understand-feedback", "I want to understand feedback", "Use these when the student has comments, marks or tutor feedback and needs to turn it into revision moves.", ["SW2", "SW1", "WT4"]),
        ("fix-mistake", "I want to fix a recurring mistake", "Use this when a student keeps making the same kind of mistake and needs a micro-lesson or tutor lesson material.", ["WT4", "WT3"]),
        ("check-paraphrasing", "I want to check paraphrasing, quotations or referencing", "Use these when source use, attribution, quotations or too-close paraphrase are the main issue.", ["WT7", "WT6", "AT8"]),
        ("plan-structure", "I want to plan or structure an assignment", "Use these when the shape of the argument, paragraph sequence or whole draft needs attention.", ["ST2", "ST4", "AT1", "AT2"]),
        ("reverse-outline", "I want to reverse-outline a draft", "Use this to create a private diagnostic map of what each paragraph is doing. It is a revision aid, not submitted writing.", ["ST4", "ST1"]),
        ("evaluate-sources", "I want to evaluate sources or evidence", "Use these when the problem is source quality, source use, evidence gaps or critical engagement.", ["AT8", "AT4", "AT6"]),
        ("think-critically", "I want to challenge or deepen my argument", "Use these when the draft needs more analysis, counterargument, conceptual clarity or critical pressure.", ["AT3", "AT5", "AT7", "AT9", "AT10"]),
        ("research-proposal", "I want help with a research proposal", "Use these for research questions, methodology fit, supervisor-style review, viva practice and topic development.", ["RP1", "RP2", "RP3", "RP4", "RP5"]),
        ("reflect-plan", "I want to reflect, plan revision or record AI use", "Use these when the student needs a plan, a record of AI use, or a workflow for acting on feedback.", ["SW1", "SW2", "SW3"]),
        ("test-tutor", "I want to test or verify the toolkit", "Use the testing guide and source material rather than a student-facing tool.", []),
    ]
    sections: list[str] = []
    for slug, title, desc, codes in groups:
        if codes:
            content = cards_for(codes)
        else:
            content = '''<div class="tool-grid"><article class="tool-card"><h3>Testing and verification</h3><p>Use the testing and audit pages to check whether a tutor behaves as a learning-support tool rather than an answer machine.</p><div class="actions tool-actions"><a class="button secondary small-button" href="../testing.html">Open testing</a><a class="button secondary small-button" href="../guides/">Open Guides</a><a class="button secondary small-button" href="../source-material/">Open source material</a></div></article></div>'''
        sections.append(f'''<details class="tool-section" id="{slug}">
<summary><span>{html.escape(title)}</span></summary>
<p>{html.escape(desc)}</p>
<div class="tool-grid">{content}</div>
</details>''')
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Where to start? | AI Personal Tutor Toolkit</title>
<meta content="A task-based guide to choosing the right AI Personal Tutor Toolkit tool." name="description"/>
<link href="../style.css" rel="stylesheet"/><link href="../css/aichat.css" rel="stylesheet"/>
</head>
<body class="reference start-page">
{header_html("../", "start")}
<main><article class="reading"><header class="page-intro">
<p class="kicker">Where to start?</p>
<h1>Choose a tool by what you want to do.</h1>
<p class="lead">Open the section closest to your situation. Each section suggests a small number of relevant tools rather than listing the whole toolkit.</p>
</header>
<section class="accordion-list wide">
{"".join(sections)}
</section>
</article></main>
{footer_html("../")}
</body>
</html>'''


def build_download_page(tools: list[dict[str, object]], version: str) -> str:
    by_family: dict[str, list[dict[str, object]]] = defaultdict(list)
    for tool in tools:
        by_family[str(tool["family"])].append(tool)
    libraries = [
        ("Master Library", "Everything in one prompt-library file. Best for staff review, testing or users who want the full toolkit.", "../prompt-libraries/latest/ai_personal_tutor_master_library.md"),
        ("All mini libraries ZIP", "All five focused mini-library files in one ZIP.", "../prompt-libraries/latest/ai_personal_tutor_mini_libraries.zip"),
        ("Writing Tutor Library", "Writing, style, mistakes, referencing, paraphrase and quotation support.", "../prompt-libraries/latest/01_writing_tutor_library.md"),
        ("Structure Tutor Library", "Paragraph, draft structure, meaning review and reverse outlining.", "../prompt-libraries/latest/02_structure_tutor_library.md"),
        ("Academic Thinking Tutor Library", "Argument, evidence, concepts, source reliability and critical challenge.", "../prompt-libraries/latest/03_academic_thinking_tutor_library.md"),
        ("Research Proposal Tutor Library", "Research questions, methods, supervisor review, viva practice and topic brainstorming.", "../prompt-libraries/latest/04_research_proposal_tutor_library.md"),
        ("Study Workflow Tutor Library", "Revision planning, feedback-to-action and AI-use records.", "../prompt-libraries/latest/05_study_workflow_tutor_library.md"),
    ]
    lib_cards = []
    for title, desc, href in libraries:
        lib_cards.append(f'''<article class="tool-card download-card"><h3>{html.escape(title)}</h3><p>{html.escape(desc)}</p><div class="actions tool-actions"><a class="button secondary small-button" href="{href}">Open file</a><a class="button small-button" download href="{href}">Download</a></div></article>''')
    individual_sections = []
    for family in FAMILY_ORDER:
        items = by_family.get(family, [])
        if not items:
            continue
        individual_sections.append(f'''<details class="tool-section" id="{family}-downloads">
<summary><span>{html.escape(FAMILY_LABELS[family])} single-tool downloads</span><small>{len(items)} tools</small></summary>
<div class="tool-grid">{"".join(tool_card(tool, prefix="../", include_anchor=False) for tool in items)}</div>
</details>''')
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Download | AI Personal Tutor Toolkit</title>
<meta content="Download complete prompt libraries, mini libraries and individual tool files." name="description"/>
<link href="../style.css" rel="stylesheet"/><link href="../css/aichat.css" rel="stylesheet"/>
</head>
<body class="reference download-page">
{header_html("../", "download")}
<main><article class="reading"><header class="page-intro">
<p class="kicker">Download</p>
<h1>Download prompt libraries and individual tools.</h1>
<p class="lead">Use a mini library for most student work. Use a single-tool file when upload limits are tight or you want one focused prompt.</p>
<p class="small-note">Current release version: <strong>v{html.escape(version)}</strong>.</p>
</header>
<section class="panel wide"><h2>Complete and mini libraries</h2><div class="tool-grid">{"".join(lib_cards)}</div></section>
<section class="panel wide" id="individual-tools"><h2>Individual tool downloads</h2><p>Expand a section to download one tool file.</p><div class="accordion-list">{"".join(individual_sections)}</div></section>
</article></main>
{footer_html("../")}
</body>
</html>'''


def normalise_css(css: str) -> str:
    css = re.sub(r"\n/\* Accessible heading refinement:.*?@media \(max-width: 860px\) \{\n  \.tool-grid \{ grid-template-columns: 1fr; \}\n\}\n", "\n", css, flags=re.S)
    css = re.sub(r"\n/\* Navigation refresh \*/.*?@media \(max-width: 860px\) \{\n  \.tool-grid \{ grid-template-columns: 1fr; \}\n\}\n", "\n", css, flags=re.S)
    css = re.sub(r"h1 \{\n  font-size: clamp\(1\.7rem, 3vw, 2\.2rem\);\n  line-height: [^;]+;\n  margin: 0 0 8px;\n  letter-spacing: [^;]+;\n  font-weight: [^;]+;\n\}", "h1 {\n  font-size: clamp(1.7rem, 3vw, 2.2rem);\n  line-height: 1.18;\n  margin: 0 0 8px;\n  letter-spacing: -0.01em;\n  font-weight: 700;\n}", css)
    css = re.sub(r"h2 \{\n  font-size: clamp\(1\.08rem, 1\.35vw, 1\.18rem\);\n  line-height: [^;]+;\n  margin: 28px 0 7px;\n  letter-spacing: [^;]+;\n  font-weight: [^;]+;\n\}", "h2 {\n  font-size: clamp(1.08rem, 1.35vw, 1.18rem);\n  line-height: 1.32;\n  margin: 28px 0 7px;\n  letter-spacing: 0;\n  font-weight: 650;\n}", css)
    css = re.sub(r"body\.home h1 \{\n  font-size: clamp\(2\.1rem, 5vw, 4\.5rem\);\n  line-height: [^;]+;\n  margin: 0 0 16px;\n  letter-spacing: [^;]+;\n  font-weight: [^;]+;\n\}", "body.home h1 {\n  font-size: clamp(2.1rem, 5vw, 4.5rem);\n  line-height: 1.08;\n  margin: 0 0 16px;\n  letter-spacing: -0.018em;\n  font-weight: 720;\n}", css)
    css = re.sub(r"body\.home h2 \{\n  font-size: clamp\(1\.45rem, 3vw, 2\.05rem\);\n  margin: 0 0 12px;\n  letter-spacing: [^;]+;\n  line-height: [^;]+;\n  font-weight: [^;]+;\n\}", "body.home h2 {\n  font-size: clamp(1.45rem, 3vw, 2.05rem);\n  margin: 0 0 12px;\n  letter-spacing: -0.005em;\n  line-height: 1.2;\n  font-weight: 680;\n}", css)
    return css.rstrip() + CSS_BLOCK + "\n"


def build_plan(root: Path = ROOT) -> list[WritePlan]:
    docs = root / "docs"
    tools, version = read_tool_data(root)
    planned: dict[Path, str] = {
        docs / "tools" / "index.html": build_tools_page(tools, version),
        docs / "where-to-start" / "index.html": build_where_to_start_page(tools),
        docs / "download" / "index.html": build_download_page(tools, version),
    }
    for path in sorted(docs.rglob("*.html")):
        text = planned.get(path)
        if text is None:
            text = path.read_text(encoding="utf-8", errors="ignore")
        if '<header><div class="container nav">' not in text and '<footer class="footer">' not in text:
            continue
        prefix = rel_prefix(path, docs)
        current = current_for_path(path, docs)
        planned[path] = replace_header_footer(text, prefix, current)
    home = docs / "index.html"
    if home in planned:
        text = planned[home]
        replacements = {
            'href="tools/writing-tutor.html"': 'href="tools/#writing-tutor"',
            'href="tools/structure-tutor.html"': 'href="tools/#structure-tutor"',
            'href="tools/academic-thinking.html"': 'href="tools/#academic-thinking"',
            'href="tools/research-proposal.html"': 'href="tools/#research-proposal"',
            'href="tools/study-workflow.html"': 'href="tools/#study-workflow"',
            'href="tools/single-tools.html"': 'href="download/#individual-tools"',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        planned[home] = text
    css_path = docs / "style.css"
    if css_path.exists():
        planned[css_path] = normalise_css(css_path.read_text(encoding="utf-8", errors="ignore"))
    return [WritePlan(path, text) for path, text in sorted(planned.items(), key=lambda item: item[0].as_posix())]


def write_plans(plans: Sequence[WritePlan], *, dry_run: bool = False) -> list[Path]:
    changed: list[Path] = []
    for plan in plans:
        old = plan.path.read_text(encoding="utf-8", errors="ignore") if plan.path.exists() else ""
        if old != plan.text:
            changed.append(plan.path)
            if not dry_run:
                plan.path.parent.mkdir(parents=True, exist_ok=True)
                plan.path.write_text(plan.text, encoding="utf-8", newline="\n")
    return changed


def check_plans(plans: Sequence[WritePlan]) -> int:
    stale: list[Path] = []
    for plan in plans:
        old = plan.path.read_text(encoding="utf-8", errors="ignore") if plan.path.exists() else ""
        if old != plan.text:
            stale.append(plan.path)
    if stale:
        print("Generated site pages are out of date:", file=sys.stderr)
        for path in stale[:50]:
            print(f"  - {path.relative_to(ROOT).as_posix()}", file=sys.stderr)
        if len(stale) > 50:
            print(f"  ... and {len(stale) - 50} more", file=sys.stderr)
        print("Run: python scripts/build_site_pages.py", file=sys.stderr)
        return 1
    print("Generated site pages are up to date.")
    return 0


def validate() -> int:
    required = [DOCS / "tools" / "index.html", DOCS / "where-to-start" / "index.html", DOCS / "download" / "index.html", DOCS / "style.css"]
    missing = [path for path in required if not path.exists()]
    if missing:
        print("Missing generated site page output(s):", file=sys.stderr)
        for path in missing:
            print(f"  - {path.relative_to(ROOT).as_posix()}", file=sys.stderr)
        return 1
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build/check generated static site pages.")
    parser.add_argument("--check", action="store_true", help="Do not write files; fail if generated site pages are stale.")
    parser.add_argument("--validate", action="store_true", help="Validate required generated page outputs exist.")
    parser.add_argument("--dry-run", action="store_true", help="List files that would change without writing anything.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.validate:
        rc = validate()
        if rc:
            return rc
    plans = build_plan(ROOT)
    if args.check:
        return check_plans(plans)
    changed = write_plans(plans, dry_run=args.dry_run)
    label = "Would update" if args.dry_run else "Updated"
    print(f"{label} {len(changed)} generated site page/style file(s).")
    for path in changed:
        print(f"  - {path.relative_to(ROOT).as_posix()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
