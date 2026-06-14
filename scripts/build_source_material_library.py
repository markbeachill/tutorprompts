#!/usr/bin/env python3
"""Build the copy-ready source-material library page.

Source material lives in src/source-material/items/*.md. Each item has a small
front-matter block plus the Markdown text that should be displayed for copying.
The generated public outputs are:

  docs/source-material/index.html
  docs/source-material/latest/*.md
  docs/data/source_material_index.json

Run from the repository root:
    python scripts/build_source_material_library.py

Check mode:
    python scripts/build_source_material_library.py --check
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src" / "source-material" / "items"
OUT_DIR = ROOT / "docs" / "source-material"
LATEST_DIR = OUT_DIR / "latest"
DATA_JSON = ROOT / "docs" / "data" / "source_material_index.json"
INDEX_HTML = OUT_DIR / "index.html"
GENERATOR_VERSION = "1.0"

REQUIRED_FIELDS = {"id", "title", "tool_code", "tool_title", "category", "use_when"}


@dataclass(frozen=True)
class SourceItem:
    id: str
    title: str
    tool_code: str
    tool_title: str
    category: str
    use_when: str
    source_path: Path
    output_path: Path
    body: str

    @property
    def output_rel(self) -> str:
        return self.output_path.relative_to(ROOT).as_posix()

    @property
    def source_rel(self) -> str:
        return self.source_path.relative_to(ROOT).as_posix()


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_front_matter(text: str, path: Path) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"{rel(path)}: missing front matter")
    data: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{rel(path)}: unsupported front-matter line: {raw!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        raise ValueError(f"{rel(path)}: missing front-matter field(s): {', '.join(missing)}")
    return data, match.group(2).rstrip() + "\n"


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower() or "source-item"


def load_items() -> list[SourceItem]:
    if not SRC_DIR.exists():
        raise FileNotFoundError(f"Missing source material directory: {rel(SRC_DIR)}")
    items: list[SourceItem] = []
    seen_ids: set[str] = set()
    for path in sorted(SRC_DIR.glob("*.md")):
        data, body = parse_front_matter(path.read_text(encoding="utf-8"), path)
        item_id = data["id"]
        if item_id in seen_ids:
            raise ValueError(f"Duplicate source material id: {item_id}")
        seen_ids.add(item_id)
        out_name = slugify(item_id) + ".md"
        items.append(SourceItem(
            id=item_id,
            title=data["title"],
            tool_code=data["tool_code"],
            tool_title=data["tool_title"],
            category=data["category"],
            use_when=data["use_when"],
            source_path=path,
            output_path=LATEST_DIR / out_name,
            body=body,
        ))
    if not items:
        raise ValueError(f"No source material items found in {rel(SRC_DIR)}")
    return items


def json_text(data: object) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def build_data(items: Sequence[SourceItem]) -> dict[str, object]:
    return {
        "generated_by": f"ai-personal-tutor-source-material-generator-v{GENERATOR_VERSION}",
        "source": "src/source-material/items",
        "item_count": len(items),
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "tool_code": item.tool_code,
                "tool_title": item.tool_title,
                "category": item.category,
                "use_when": item.use_when,
                "source": item.source_rel,
                "download": item.output_rel,
            }
            for item in items
        ],
    }


def item_card(item: SourceItem, index: int) -> str:
    pre_id = f"sourcebox{index}"
    escaped_body = html.escape(item.body)
    return f'''<article class="card source-card">
<h2>{html.escape(item.title)}</h2>
<p class="small-note"><strong>{html.escape(item.tool_code)}</strong> — {html.escape(item.tool_title)} · {html.escape(item.category)}</p>
<p>{html.escape(item.use_when)}</p>
<div class="btn-row"><button class="button" onclick="copyBox('{pre_id}',this)">Copy source text</button><a class="button secondary" download href="latest/{html.escape(item.output_path.name)}">Download Markdown</a></div>
<pre id="{pre_id}"><code>{escaped_body}</code></pre>
</article>'''


def build_index_html(items: Sequence[SourceItem]) -> str:
    cards = "\n".join(item_card(item, i) for i, item in enumerate(items, start=1))
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Source material library | AI Personal Tutor Toolkit</title>
<meta content="Copy-ready source material for testing and using AI Personal Tutor Toolkit tools." name="description"/>
<link href="../style.css" rel="stylesheet"/><link href="../css/aichat.css" rel="stylesheet"/>
<style>
.source-card pre {{ margin-top: 14px; max-height: 520px; }}
.source-card h2 {{ margin-top: 0; }}
</style>
</head>
<body class="reference">
<header><div class="container nav"><a class="brand" href="../index.html">AI Personal Tutor Toolkit<small>Structured writing support</small></a><nav><ul><li><a href="../index.html">Home</a></li><li><a href="../tools/">Tools</a></li><li><a href="../examples/">Examples</a></li><li><a href="../student-help/">Student Help</a></li><li><a href="../guides/">Guides</a></li></ul></nav></div></header>
<main>
<article class="reading">
<header class="page-intro">
<p class="kicker">Source material</p>
<h1>Copy-ready source material.</h1>
<p class="lead">Use these short source packs when trying tools, demonstrating them to students, or checking whether a tool handles source material safely. Edit the Markdown files under <code>src/source-material/items/</code> and rebuild this page when you want to update the library.</p>
<div class="btn-row"><a class="button secondary" href="../guides/">Back to guides</a><a class="button secondary" href="../tools/">Browse tools</a></div>
</header>
<section class="panel notice">
<h2>How to use this page</h2>
<p>Choose an item, copy the text, then paste it into the relevant tutor tool. The source files are examples and testing material; they are not intended for student submission.</p>
</section>
{cards}
</article>
</main>
<footer class="footer"><div class="container"><p>AI Personal Tutor Toolkit. Structured writing support for learning-focused AI use.</p><p class="footer-links"><a href="../testing.html">Testing</a> | <a href="../changelog/">Changelog</a> | <a href="../guides/teaching-approach.html">Teaching approach</a> | <a href="../about.html">About this site</a></p></div></footer>
<script>
function copyBox(id,btn){{var t=document.getElementById(id).textContent;navigator.clipboard.writeText(t).then(function(){{var o=btn.textContent;btn.textContent='Copied';setTimeout(function(){{btn.textContent=o;}},1500);}});}}
</script>
</body>
</html>
'''


def expected_outputs() -> dict[Path, str]:
    items = load_items()
    outputs: dict[Path, str] = {
        INDEX_HTML: build_index_html(items),
        DATA_JSON: json_text(build_data(items)),
    }
    for item in items:
        outputs[item.output_path] = item.body
    return outputs


def remove_stale_latest_files(expected: dict[Path, str], *, write: bool) -> list[str]:
    stale: list[str] = []
    if not LATEST_DIR.exists():
        return stale
    expected_paths = set(expected)
    for path in sorted(LATEST_DIR.glob("*.md")):
        if path not in expected_paths:
            stale.append(rel(path))
            if write:
                path.unlink()
    return stale


def write_outputs() -> list[str]:
    outputs = expected_outputs()
    changes: list[str] = []
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    DATA_JSON.parent.mkdir(parents=True, exist_ok=True)
    changes.extend(remove_stale_latest_files(outputs, write=True))
    for path, text in outputs.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            changes.append(rel(path))
    return changes


def check_outputs() -> list[str]:
    outputs = expected_outputs()
    changes = remove_stale_latest_files(outputs, write=False)
    for path, text in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != text:
            changes.append(rel(path))
    return changes


def validate_outputs() -> None:
    changes = check_outputs()
    if changes:
        raise ValueError("Generated source-material files are out of date: " + ", ".join(changes))
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    if data.get("item_count") != len(data.get("items", [])):
        raise ValueError("source_material_index.json item_count does not match items length")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build copy-ready source material library outputs.")
    parser.add_argument("--check", action="store_true", help="Fail if generated source-material files are missing or out of date.")
    parser.add_argument("--validate", action="store_true", help="Validate generated source-material files without writing changes.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.check:
        changes = check_outputs()
        if changes:
            print("Generated source-material files are out of date:", file=sys.stderr)
            for change in changes:
                print(f"  - {change}", file=sys.stderr)
            print("\nLikely fix from the repository root:", file=sys.stderr)
            print("  python scripts\\build_source_material_library.py", file=sys.stderr)
            print("  python scripts\\build_source_material_library.py --check", file=sys.stderr)
            return 1
        print("Generated source-material files are up to date.")
        return 0
    if args.validate:
        validate_outputs()
        print("Generated source-material files validated.")
        return 0
    changes = write_outputs()
    if changes:
        print("Updated generated source-material files:")
        for change in changes:
            print(f"  - {change}")
    else:
        print("No source-material changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
