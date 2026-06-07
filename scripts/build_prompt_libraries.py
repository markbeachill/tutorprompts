#!/usr/bin/env python3
"""Build AI Personal Tutor prompt libraries from source blocks.

Package Generator v1.5

v1.5 keeps the public prompt-library outputs behaviourally unchanged by default,
and adds distribution polish for single-tool packs: generated README/index,
JSON manifest, deterministic ZIP entries and stronger checks.
A single-tool pack is generated from the same canonical metadata and source tool block
as the master/mini/custom packs, so the visible menu, router and local menu number stay
in sync. The --ci command runs the no-write checks intended for GitHub Actions.

v1.1 improves stale-output diagnostics. If generated prompt-library files differ
mainly because the repository has been prepared for a newer toolkit version but
src/release.yml still contains an older version, the check now prints a targeted
release-metadata hint instead of only a raw diff.

The default build still builds only the master library and five mini-libraries.
Custom packs and single-tool packs are built explicitly with --custom-pack,
--include-custom, --single-tool or --include-single-tools.

Run from the repository root:
    python scripts/build_prompt_libraries.py

Check mode:
    python scripts/build_prompt_libraries.py --check

List packs:
    python scripts/build_prompt_libraries.py --list-packs

Validate without writing files:
    python scripts/build_prompt_libraries.py --validate

Build one custom pack:
    python scripts/build_prompt_libraries.py --custom-pack src/prompt-library/custom-packs/example-first-year-writing-support.yml

Build core packs plus every custom pack in src/prompt-library/custom-packs/:
    python scripts/build_prompt_libraries.py --include-custom

Build all single-tool packs and their ZIP:
    python scripts/build_prompt_libraries.py --include-single-tools

Build one single-tool pack by code or stable tool id:
    python scripts/build_prompt_libraries.py --single-tool WT1

CI check used by GitHub Actions:
    python scripts/build_prompt_libraries.py --ci
"""
from __future__ import annotations

import argparse
import difflib
import io
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "prompt-library"
PACK_DIR = SRC / "packs"
CUSTOM_PACK_DIR = SRC / "custom-packs"
SINGLE_TOOL_OUTPUT_DIR = ROOT / "docs" / "prompt-libraries" / "single-tools"
CUSTOM_OUTPUT_DIR = ROOT / "docs" / "prompt-libraries" / "custom"
HEADER = SRC / "header.md"
TOOL_METADATA = SRC / "tool-metadata.json"
MINI_ZIP = ROOT / "docs" / "prompt-libraries" / "latest" / "ai_personal_tutor_mini_libraries.zip"
SINGLE_TOOL_ZIP = ROOT / "docs" / "prompt-libraries" / "single-tools" / "ai_personal_tutor_single_tool_packs.zip"
SINGLE_TOOL_README = SINGLE_TOOL_OUTPUT_DIR / "README.md"
SINGLE_TOOL_MANIFEST = SINGLE_TOOL_OUTPUT_DIR / "single_tool_manifest.json"
CUSTOM_PACK_ZIP = CUSTOM_OUTPUT_DIR / "ai_personal_tutor_custom_packs.zip"
CUSTOM_PACK_README = CUSTOM_OUTPUT_DIR / "README.md"
RELEASE_YML = ROOT / "src" / "release.yml"

MINI_LIBRARY_LATEST = [
    "docs/prompt-libraries/latest/01_writing_tutor_library.md",
    "docs/prompt-libraries/latest/02_structure_tutor_library.md",
    "docs/prompt-libraries/latest/03_academic_thinking_tutor_library.md",
    "docs/prompt-libraries/latest/04_research_proposal_tutor_library.md",
    "docs/prompt-libraries/latest/05_study_workflow_tutor_library.md",
]

FAMILY_ORDER = [
    "writing-tutor",
    "structure-tutor",
    "academic-thinking",
    "research-proposal",
    "study-workflow",
]

MINI_MANIFEST_HEADINGS = {
    "writing-tutor": "Writing and referencing tools",
    "structure-tutor": "Structure tools",
    "academic-thinking": "Academic thinking tools",
    "research-proposal": "Research proposal tools",
    "study-workflow": "Study workflow tools",
}


SECTION_MARKERS = {
    "manifest": "00-manifest.md",
    "launcher": "03-launcher.md",
    "router": "04-router.md",
}

SINGLE_TOOL_SECTIONS = [
    "pack-sections/single-tool/00-manifest.md",
    "shared/01-global-rules.md",
    "shared/02-markdown-output-rules.md",
    "pack-sections/single-tool/03-launcher.md",
    "pack-sections/single-tool/04-router.md",
]

REQUIRED_TOOL_FRONT_MATTER = {"id", "tool_code", "title", "type", "menu_number", "run_policy"}


@dataclass(frozen=True)
class ToolMeta:
    id: str
    code: str
    title: str
    family: str
    family_label: str
    master_manifest_description: str
    mini_manifest_description: str
    mini_family_label: str
    launcher_description: str


def read_simple_yaml(path: Path) -> Dict[str, object]:
    """Read the deliberately small pack-manifest YAML subset used by this project.

    This is not a general YAML parser. It supports top-level scalar keys and top-level
    lists only, which keeps the generator dependency-free for Windows/macOS/Linux users.
    """
    data: Dict[str, object] = {}
    current_list: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            current_list = stripped[:-1]
            data[current_list] = []
            continue
        if current_list and line.startswith("  - "):
            data[current_list].append(_unquote(line[4:].strip()))
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = _unquote(value.strip())
            current_list = None
            continue
        raise ValueError(f"Unsupported line in {path}: {raw!r}")
    return data


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'\"', "'"}:
        return value[1:-1]
    return value




def read_release_metadata() -> Dict[str, str]:
    """Read src/release.yml using the generator's deliberately small YAML subset."""
    if not RELEASE_YML.exists():
        return {}
    raw = read_simple_yaml(RELEASE_YML)
    return {str(key): str(value) for key, value in raw.items() if not isinstance(value, list)}


def extract_version_tokens(text: str) -> set[str]:
    """Extract toolkit/prompt/testing version tokens from generated prompt-library text."""
    tokens: set[str] = set()
    patterns = [
        r"^version:\s*v?([0-9]+(?:\.[0-9]+)*)\s*$",
        r"^\*\*Version:\*\*\s*v?([0-9]+(?:\.[0-9]+)*)\s*$",
        r"Toolkit version\s+v?([0-9]+(?:\.[0-9]+)*)",
        r"Prompt-library suite\s+v?([0-9]+(?:\.[0-9]+)*)",
        r"Testing pack\s+v?([0-9]+(?:\.[0-9]+)*)",
        r"prompt-libraries/v([0-9]+(?:\.[0-9]+)*)/",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.MULTILINE):
            tokens.add(match.group(1))
    return tokens


def format_version_set(values: set[str]) -> str:
    if not values:
        return "not detected"
    return ", ".join(sorted(values, key=lambda v: [int(part) for part in v.split('.')]))


def print_stale_output_diagnostics(changes: Sequence[str], diffs: Sequence[str], generated_texts: Sequence[tuple[Path, str]] | None = None) -> None:
    """Print consistent stale-output diagnostics for --check and --ci.

    v1.1 adds a targeted hint for the common case where a user has prepared generated
    files for a new release version, but the source release metadata still points at
    the previous version. In that situation the generator correctly tries to rebuild
    back to the old metadata, but the raw diff alone is confusing.
    """
    print("Generated prompt-library files are out of date:", file=sys.stderr)
    for change in changes:
        print(f"  - {change}", file=sys.stderr)

    release = read_release_metadata()
    current_versions: set[str] = set()
    generated_versions: set[str] = set()
    for rel in changes:
        path = ROOT / rel
        if path.suffix.lower() == ".md" and path.exists():
            current_versions.update(extract_version_tokens(path.read_text(encoding="utf-8")))
    for path, text in generated_texts or []:
        generated_versions.update(extract_version_tokens(text))

    if release or current_versions or generated_versions:
        print("\nVersion diagnostic:", file=sys.stderr)
        if release:
            print(
                "  - src/release.yml: "
                f"toolkit_version={release.get('toolkit_version', 'unset')}, "
                f"prompt_library_version={release.get('prompt_library_version', 'unset')}, "
                f"testing_pack_version={release.get('testing_pack_version', 'unset')}, "
                f"release_date={release.get('release_date', 'unset')}",
                file=sys.stderr,
            )
        if current_versions:
            print(f"  - current generated files contain version(s): {format_version_set(current_versions)}", file=sys.stderr)
        if generated_versions:
            print(f"  - rebuilding from source would produce version(s): {format_version_set(generated_versions)}", file=sys.stderr)
        source_versions = {
            value.lstrip("v")
            for key, value in release.items()
            if key.endswith("_version") and value
        }
        if current_versions and source_versions and not current_versions.issubset(source_versions):
            likely = sorted(current_versions - source_versions, key=lambda v: [int(part) for part in v.split('.')])[-1]
            release_date = release.get("release_date", "YYYY-MM-DD")
            print("\nLikely cause:", file=sys.stderr)
            print("  The generated files appear to have been prepared for a version that is not in src/release.yml.", file=sys.stderr)
            print("\nLikely fix from the repository root:", file=sys.stderr)
            print(f"  python scripts\\prepare_toolkit_release.py --version {likely} --date {release_date}", file=sys.stderr)
            print("  python scripts\\build_prompt_libraries.py", file=sys.stderr)
            print("  python scripts\\build_prompt_libraries.py --ci", file=sys.stderr)
        else:
            print("\nLikely fix from the repository root:", file=sys.stderr)
            print("  python scripts\\build_prompt_libraries.py", file=sys.stderr)
            print("  python scripts\\build_prompt_libraries.py --ci", file=sys.stderr)

    if diffs:
        print("\nFirst diff lines:", file=sys.stderr)
        print("\n".join(diffs), file=sys.stderr)


def load_tool_metadata() -> Dict[str, ToolMeta]:
    if not TOOL_METADATA.exists():
        raise FileNotFoundError(f"Missing tool metadata file: {TOOL_METADATA}")
    raw = json.loads(TOOL_METADATA.read_text(encoding="utf-8"))
    tools = raw.get("tools")
    if not isinstance(tools, list):
        raise ValueError(f"{TOOL_METADATA}: expected a top-level 'tools' list")
    by_id: Dict[str, ToolMeta] = {}
    seen_codes: set[str] = set()
    required = {"id", "code", "title", "family", "family_label", "master_manifest_description", "mini_manifest_description", "mini_family_label", "launcher_description"}
    for item in tools:
        if not isinstance(item, dict):
            raise ValueError(f"{TOOL_METADATA}: every tool entry must be an object")
        missing = sorted(required - set(item))
        if missing:
            raise ValueError(f"{TOOL_METADATA}: tool entry missing {', '.join(missing)}")
        meta = ToolMeta(**{key: str(item[key]) for key in required})
        if meta.id in by_id:
            raise ValueError(f"{TOOL_METADATA}: duplicate tool id {meta.id}")
        if meta.code in seen_codes:
            raise ValueError(f"{TOOL_METADATA}: duplicate tool code {meta.code}")
        if meta.family not in FAMILY_ORDER:
            raise ValueError(f"{TOOL_METADATA}: unknown family {meta.family!r} for {meta.id}")
        if not meta.launcher_description.endswith("."):
            raise ValueError(f"{TOOL_METADATA}: launcher_description for {meta.id} should end with a full stop")
        by_id[meta.id] = meta
        seen_codes.add(meta.code)
    return by_id


def read_source(rel_path: str) -> str:
    path = SRC / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Missing source block: {path}")
    return path.read_text(encoding="utf-8")


def extract_front_matter(block: str, rel_path: str) -> Dict[str, str]:
    """Extract simple YAML-like front matter from a source block.

    The source files use a deliberately small front-matter subset. This parser is
    enough for validation; it is not intended to be a general YAML parser.
    """
    match = re.search(r"^---\n(.*?)\n---\n", block, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"{rel_path}: missing front matter block")
    data: Dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.startswith("  - ") or raw.startswith(" "):
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            data[key.strip()] = _unquote(value.strip())
    return data


def extract_generated_section(text: str, marker_name: str, pack_id: object) -> str:
    """Return the rendered body for a marked generated section."""
    pattern = rf"<!-- FILE: {re.escape(marker_name)} -->\n(.*?)<!-- END FILE -->"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Pack {pack_id}: generated output is missing section {marker_name}")
    return match.group(1)


def source_tool_id(rel_path: str) -> str | None:
    if not rel_path.startswith("tools/"):
        return None
    block = read_source(rel_path)
    front_matter = extract_front_matter(block, rel_path)
    tool_id = front_matter.get("id")
    if not tool_id:
        raise ValueError(f"{rel_path}: missing id field in tool front matter")
    return tool_id


def tool_source_paths_by_id() -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for path in sorted((SRC / "tools").glob("*.md")):
        rel = path.relative_to(SRC).as_posix()
        tool_id = source_tool_id(rel)
        if not tool_id:
            continue
        if tool_id in mapping:
            raise ValueError(f"Duplicate tool source id found: {tool_id}")
        mapping[tool_id] = rel
    return mapping


def tool_id_from_selector(selector: str, metadata: Dict[str, ToolMeta]) -> str:
    selector = str(selector).strip()
    if selector in metadata:
        return selector
    selector_upper = selector.upper()
    matches = [tool.id for tool in metadata.values() if tool.code.upper() == selector_upper]
    if matches:
        return matches[0]
    raise ValueError(f"Unknown tool selector {selector!r}. Use a stable tool id such as clarity-clinic or a code such as WT1.")


def normalise_pack_spec(spec: Dict[str, object], metadata: Dict[str, ToolMeta]) -> Dict[str, object]:
    """Return a pack spec with an explicit tools list.

    Core packs already list source file paths under `tools`. Custom packs may
    instead list user-friendly tool selectors under `include_tools`; each selector
    can be either a stable tool id or a short code such as WT1.
    """
    spec = dict(spec)
    if "tools" in spec:
        return spec
    include = spec.get("include_tools")
    if not isinstance(include, list):
        raise ValueError(f"Pack {spec.get('id')}: expected either tools: or include_tools:")
    source_by_id = tool_source_paths_by_id()
    tool_ids = [tool_id_from_selector(str(item), metadata) for item in include]
    try:
        spec["tools"] = [source_by_id[tool_id] for tool_id in tool_ids]
    except KeyError as exc:
        raise ValueError(f"Pack {spec.get('id')}: no source file found for tool id {exc.args[0]}") from exc
    spec.setdefault("sections", [
        "pack-sections/custom/00-manifest.md",
        "shared/01-global-rules.md",
        "shared/02-markdown-output-rules.md",
        "pack-sections/custom/03-launcher.md",
        "pack-sections/custom/04-router.md",
    ])
    spec.setdefault("tool_metadata_mode", "mini")
    spec.setdefault("footer", [])
    pack_id = str(spec.get("id", "custom-pack"))
    safe_id = re.sub(r"[^a-zA-Z0-9_-]+", "_", pack_id).strip("_").lower() or "custom_pack"
    spec.setdefault("latest_output", f"docs/prompt-libraries/custom/{safe_id}.md")
    return spec



def slugify(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return safe or "pack"


def single_tool_spec(tool: ToolMeta, source_by_id: Dict[str, str]) -> Dict[str, object]:
    """Return an in-memory pack spec for one tool.

    Single-tool packs are generated, not hand-maintained YAML files. This keeps
    them in sync with the canonical source tool block and metadata.
    """
    code = tool.code.lower()
    slug = slugify(tool.title)
    return {
        "id": f"single-{tool.code.lower()}",
        "title": f"{tool.code} — {tool.title} Single-Tool Pack",
        "kind": "single-tool",
        "latest_output": f"docs/prompt-libraries/single-tools/{code}_{slug}.md",
        "sections": SINGLE_TOOL_SECTIONS,
        "tools": [source_by_id[tool.id]],
        "tool_metadata_mode": "mini",
        "footer": [],
    }


def configured_single_tool_specs(metadata: Dict[str, ToolMeta], selector: str | None = None) -> List[Dict[str, object]]:
    source_by_id = tool_source_paths_by_id()
    if selector:
        tool_id = tool_id_from_selector(selector, metadata)
        return [single_tool_spec(metadata[tool_id], source_by_id)]
    # Preserve the canonical order from tool-metadata.json. This avoids lexical sorting
    # problems such as AT10 appearing before AT2.
    return [single_tool_spec(tool, source_by_id) for tool in metadata.values()]

def pack_tool_ids(spec: Dict[str, object], metadata: Dict[str, ToolMeta] | None = None) -> List[str]:
    if metadata is not None:
        spec = normalise_pack_spec(spec, metadata)
    tools = spec.get("tools")
    if not isinstance(tools, list):
        raise ValueError("Pack spec has no tools list")
    ids: List[str] = []
    for rel in tools:
        tool_id = source_tool_id(str(rel))
        if tool_id:
            ids.append(tool_id)
    return ids


def ordered_tool_meta(spec: Dict[str, object], metadata: Dict[str, ToolMeta]) -> List[ToolMeta]:
    ordered: List[ToolMeta] = []
    for tool_id in pack_tool_ids(spec, metadata):
        if tool_id not in metadata:
            raise ValueError(f"Pack {spec.get('id')}: no metadata for tool id {tool_id}")
        ordered.append(metadata[tool_id])
    return ordered


def grouped_tools(tools: Sequence[ToolMeta]) -> List[tuple[str, List[ToolMeta]]]:
    groups: List[tuple[str, List[ToolMeta]]] = []
    for family in FAMILY_ORDER:
        items = [tool for tool in tools if tool.family == family]
        if items:
            groups.append((family, items))
    return groups


def generate_available_tools_table(spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    is_master = spec.get("id") == "master"
    is_custom = str(spec.get("kind", "")).lower() == "custom" or "include_tools" in spec
    groups = grouped_tools(tools) if (is_master or is_custom) else [(tools[0].family, list(tools))]
    lines: List[str] = []
    number = 1
    for family, items in groups:
        heading = items[0].family_label if is_master else items[0].mini_family_label
        if lines:
            lines.append("")
        lines.append(f"**{heading}**")
        lines.append("")
        lines.append("| Menu | Code | ID | Tool title | Use when the student wants to... |")
        lines.append("|---:|---|---|---|---|")
        for tool in items:
            desc = tool.master_manifest_description if is_master else tool.mini_manifest_description
            lines.append(f"| {number} | {tool.code} | {tool.id} | {tool.title} | {desc} |")
            number += 1
    return "\n".join(lines)


def generate_launcher_menu(spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    is_master = spec.get("id") == "master"
    lines: List[str] = []
    number = 1
    is_custom = str(spec.get("kind", "")).lower() == "custom" or "include_tools" in spec
    groups = grouped_tools(tools) if (is_master or is_custom) else [(tools[0].family, list(tools))]
    for _family, items in groups:
        if is_master:
            if lines:
                lines.append("")
            lines.append(f"**{items[0].family_label}**")
        for tool in items:
            lines.append(f"{number}. **{tool.code} — {tool.title}** — {tool.launcher_description}")
            number += 1
    return "\n".join(lines)


def generate_number_routing_table(tools: Sequence[ToolMeta]) -> str:
    lines = ["| Student choice | Code | Tool ID |", "|---:|---|---|"]
    for number, tool in enumerate(tools, start=1):
        lines.append(f"| {number} | `{tool.code}` | `{tool.id}` |")
    return "\n".join(lines)


def generate_menu_mapping(spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    is_custom = str(spec.get("kind", "")).lower() == "custom" or "include_tools" in spec
    families = {tool.family for tool in tools}
    if is_custom or len(families) > 1:
        heading = "Included tools"
    else:
        heading = tools[0].mini_family_label
    lines = [f"**{heading}**"]
    for number, tool in enumerate(tools, start=1):
        lines.append(f"- `{number}`, `{tool.code}` or `{tool.title}` → run `{tool.id}`")
    return "\n".join(lines) + "\n"


def render_generated_sections(text: str, spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    replacements = {
        "{{PACK_ID}}": str(spec.get("id", "custom-pack")),
        "{{PACK_TITLE}}": str(spec.get("title", spec.get("id", "Custom Prompt Pack"))),
        "{{PACK_KIND}}": str(spec.get("kind", "pack")),
        "{{AVAILABLE_TOOLS_TABLE}}": generate_available_tools_table(spec, tools),
        "{{LAUNCHER_MENU}}": generate_launcher_menu(spec, tools),
        "{{NUMBER_ROUTING_TABLE}}": generate_number_routing_table(tools),
        "{{MENU_MAPPING}}": generate_menu_mapping(spec, tools),
    }
    for marker, generated in replacements.items():
        text = text.replace(marker, generated)
    if "{{" in text or "}}" in text:
        raise ValueError(f"Unresolved template marker in generated section for pack {spec.get('id')}")
    return text


def mini_tool_metadata(block: str, menu_number: int) -> str:
    """Convert a master tool block to a mini-library block.

    Mini-libraries need local menu numbering, and they do not include the optional
    master_number field. Stable tool identity lives in the tool front matter; pack-
    specific menu_number remains generated during the build.
    """
    block = re.sub(r"^master_number: .*\n", "", block, flags=re.MULTILINE)
    block = re.sub(r"^menu_number: .*\n", f"menu_number: {menu_number}\n", block, count=1, flags=re.MULTILINE)
    return block


def build_pack_from_spec(spec: Dict[str, object], metadata: Dict[str, ToolMeta]) -> tuple[Path, Path | None, str]:
    spec = normalise_pack_spec(spec, metadata)
    required = ["id", "latest_output", "sections", "tools"]
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError(f"{pack_file} missing required keys: {', '.join(missing)}")

    sections = spec["sections"]
    tools = spec["tools"]
    footer = spec.get("footer", [])
    mode = str(spec.get("tool_metadata_mode", "master"))
    if not isinstance(sections, list) or not isinstance(tools, list) or not isinstance(footer, list):
        raise ValueError(f"{pack_file}: sections, tools and footer must be lists")

    tool_meta = ordered_tool_meta(spec, metadata)
    parts: List[str] = [HEADER.read_text(encoding="utf-8")]
    for rel in sections:
        section = read_source(str(rel))
        section = render_generated_sections(section, spec, tool_meta)
        parts.append(section)

    menu_i = 0
    for rel in tools:
        block = read_source(str(rel))
        if str(rel).startswith("tools/"):
            menu_i += 1
            if mode == "mini":
                block = mini_tool_metadata(block, menu_i)
        parts.append(block)
    footer_parts = [read_source(str(rel)) for rel in footer]

    output_text = "\n\n\n".join(part.rstrip("\n") for part in parts).rstrip()
    if footer_parts:
        output_text += "".join(part.rstrip("\n") for part in footer_parts)
    output_text += "\n"
    latest = ROOT / str(spec["latest_output"])
    archive = ROOT / str(spec["archive_output"]) if spec.get("archive_output") else None
    return latest, archive, output_text


def build_pack(pack_file: Path, metadata: Dict[str, ToolMeta]) -> tuple[Path, Path | None, str]:
    return build_pack_from_spec(read_simple_yaml(pack_file), metadata)


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def expected_manifest_row(number: int, tool: ToolMeta) -> str:
    return f"| {number} | {tool.code} | {tool.id} | {tool.title} |"


def expected_launcher_line(number: int, tool: ToolMeta) -> str:
    return f"{number}. **{tool.code} — {tool.title}** — {tool.launcher_description}"


def expected_number_routing_row(number: int, tool: ToolMeta) -> str:
    return f"| {number} | `{tool.code}` | `{tool.id}` |"


def expected_menu_mapping_line(number: int, tool: ToolMeta) -> str:
    return f"- `{number}`, `{tool.code}` or `{tool.title}` → run `{tool.id}`"


def validate_tool_source_metadata(rel_path: str, metadata: Dict[str, ToolMeta]) -> None:
    block = read_source(rel_path)
    fm = extract_front_matter(block, rel_path)
    missing = sorted(REQUIRED_TOOL_FRONT_MATTER - set(fm))
    if missing:
        raise ValueError(f"{rel_path}: missing required front-matter field(s): {', '.join(missing)}")
    if fm.get("type") != "tool":
        raise ValueError(f"{rel_path}: expected type: tool")
    tool_id = fm["id"]
    if tool_id not in metadata:
        raise ValueError(f"{rel_path}: no metadata entry for tool id {tool_id}")
    meta = metadata[tool_id]
    if fm.get("tool_code") != meta.code:
        raise ValueError(f"{rel_path}: tool_code {fm.get('tool_code')!r} does not match metadata code {meta.code!r}")
    if fm.get("title") != meta.title:
        raise ValueError(f"{rel_path}: title {fm.get('title')!r} does not match metadata title {meta.title!r}")
    if not re.search(rf"^#\s+{re.escape(meta.code)}\s+—\s+{re.escape(meta.title)}\b", block, flags=re.MULTILINE):
        raise ValueError(f"{rel_path}: top heading does not match {meta.code} — {meta.title}")


def validate_rendered_pack_semantics(spec: Dict[str, object], text: str, tools: Sequence[ToolMeta]) -> None:
    pack_id = spec.get("id")
    manifest = extract_generated_section(text, SECTION_MARKERS["manifest"], pack_id)
    launcher = extract_generated_section(text, SECTION_MARKERS["launcher"], pack_id)
    router = extract_generated_section(text, SECTION_MARKERS["router"], pack_id)

    is_master = pack_id == "master"
    if is_master:
        if "| Student choice | Code | Tool ID |" not in router:
            raise ValueError(f"Pack {pack_id}: master router is missing the generated number-routing table header")
    else:
        if "## Menu mapping" not in router:
            raise ValueError(f"Pack {pack_id}: mini-library router is missing Menu mapping heading")

    for number, tool in enumerate(tools, start=1):
        if expected_manifest_row(number, tool) not in manifest:
            raise ValueError(f"Pack {pack_id}: Available tools table missing row prefix for {number} / {tool.code} / {tool.id}")
        if expected_launcher_line(number, tool) not in launcher:
            raise ValueError(f"Pack {pack_id}: launcher menu missing exact generated line for {number} / {tool.code}")
        if is_master:
            expected = expected_number_routing_row(number, tool)
        else:
            expected = expected_menu_mapping_line(number, tool)
        if expected not in router:
            raise ValueError(f"Pack {pack_id}: router missing exact generated mapping for {number} / {tool.code} / {tool.id}")

        # Each generated file should contain exactly one tool section for every included tool.
        if len(re.findall(rf"^id:\s*{re.escape(tool.id)}\s*$", text, flags=re.MULTILINE)) != 1:
            raise ValueError(f"Pack {pack_id}: expected exactly one tool section with id {tool.id}")
        if len(re.findall(rf"^tool_code:\s*{re.escape(tool.code)}\s*$", text, flags=re.MULTILINE)) != 1:
            raise ValueError(f"Pack {pack_id}: expected exactly one tool_code {tool.code}")

    # Mini-library outputs must not expose menu entries for tools outside the pack.
    if not is_master:
        included = {tool.id for tool in tools}
        for meta in load_tool_metadata().values():
            if meta.id in included:
                continue
            if f"| {meta.code} | {meta.id} |" in manifest:
                raise ValueError(f"Pack {pack_id}: manifest includes excluded tool {meta.code}")
            if f"**{meta.code} — {meta.title}**" in launcher:
                raise ValueError(f"Pack {pack_id}: launcher includes excluded tool {meta.code}")
            if f"`{meta.code}`" in router and f"`{meta.id}`" in router:
                raise ValueError(f"Pack {pack_id}: router appears to include excluded tool {meta.code}")


def validate_mini_zip_contents() -> None:
    if not MINI_ZIP.exists():
        raise FileNotFoundError(f"Mini-library ZIP does not exist: {MINI_ZIP}")
    expected = [Path(rel).name for rel in MINI_LIBRARY_LATEST]
    with zipfile.ZipFile(MINI_ZIP, "r") as zf:
        actual = sorted(zf.namelist())
    if actual != sorted(expected):
        raise ValueError(f"Mini-library ZIP contents differ. Expected {sorted(expected)}, got {actual}")


def build_mini_zip_bytes() -> bytes:
    """Build deterministic mini-library ZIP bytes.

    Python's ZipFile.write() stores source file timestamps, which can make the ZIP
    change even when the Markdown content has not changed. v0.3 writes fixed
    timestamps so --check can reliably detect real changes only.
    """
    buffer = io.BytesIO()
    fixed_time = (2026, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in MINI_LIBRARY_LATEST:
            path = ROOT / rel
            if not path.exists():
                raise FileNotFoundError(f"Cannot add missing mini-library to ZIP: {path}")
            info = zipfile.ZipInfo(filename=Path(rel).name, date_time=fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    return buffer.getvalue()


def mini_zip_is_current() -> bool:
    if not MINI_ZIP.exists():
        return False
    return MINI_ZIP.read_bytes() == build_mini_zip_bytes()


def rebuild_mini_zip() -> bool:
    MINI_ZIP.parent.mkdir(parents=True, exist_ok=True)
    before = MINI_ZIP.read_bytes() if MINI_ZIP.exists() else None
    after = build_mini_zip_bytes()
    if before == after:
        return False
    MINI_ZIP.write_bytes(after)
    return True



def expected_single_tool_relpaths(metadata: Dict[str, ToolMeta]) -> List[str]:
    return [Path(str(spec["latest_output"])).name for spec in configured_single_tool_specs(metadata)]


def single_tool_manifest_data(metadata: Dict[str, ToolMeta]) -> Dict[str, object]:
    release = read_release_metadata()
    packs = []
    for spec in configured_single_tool_specs(metadata):
        tools = ordered_tool_meta(spec, metadata)
        tool = tools[0]
        packs.append({
            "code": tool.code,
            "id": tool.id,
            "title": tool.title,
            "family": tool.family,
            "family_label": tool.family_label,
            "generated_file": Path(str(spec["latest_output"])).name,
            "pack_title": str(spec.get("title", "")),
        })
    return {
        "generator_feature": "single-tool-packs",
        "toolkit_version": release.get("toolkit_version", ""),
        "prompt_library_version": release.get("prompt_library_version", ""),
        "release_date": release.get("release_date", ""),
        "pack_count": len(packs),
        "packs": packs,
    }


def build_single_tool_manifest_text(metadata: Dict[str, ToolMeta]) -> str:
    return json.dumps(single_tool_manifest_data(metadata), indent=2, ensure_ascii=False) + "\n"


def build_single_tool_readme_text(metadata: Dict[str, ToolMeta]) -> str:
    release = read_release_metadata()
    version = release.get("prompt_library_version", "")
    lines = [
        "# AI Personal Tutor single-tool packs",
        "",
        "This folder contains generated single-tool prompt packs. Each file contains the shared operating rules, a one-tool launcher/router, and one tool instruction block.",
        "",
        f"Prompt-library version: v{version}" if version else "Prompt-library version: not set",
        "",
        "Build all single-tool packs from the repository root with:",
        "",
        "```bash",
        "python scripts/build_prompt_libraries.py --include-single-tools",
        "```",
        "",
        "Check all single-tool packs without writing changes with:",
        "",
        "```bash",
        "python scripts/build_prompt_libraries.py --include-single-tools --check",
        "```",
        "",
        "## Included single-tool packs",
        "",
        "| Code | Tool | Family | Generated file |",
        "|---|---|---|---|",
    ]
    for spec in configured_single_tool_specs(metadata):
        tool = ordered_tool_meta(spec, metadata)[0]
        filename = Path(str(spec["latest_output"])).name
        lines.append(f"| {tool.code} | {tool.title} | {tool.family_label} | `{filename}` |")
    lines.extend([
        "",
        "The ZIP `ai_personal_tutor_single_tool_packs.zip` contains this README, `single_tool_manifest.json`, and all generated single-tool Markdown files.",
    ])
    return "\n".join(lines).rstrip() + "\n"


def rebuild_single_tool_readme(metadata: Dict[str, ToolMeta]) -> bool:
    SINGLE_TOOL_README.parent.mkdir(parents=True, exist_ok=True)
    return write_if_changed(SINGLE_TOOL_README, build_single_tool_readme_text(metadata))


def rebuild_single_tool_manifest(metadata: Dict[str, ToolMeta]) -> bool:
    SINGLE_TOOL_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    return write_if_changed(SINGLE_TOOL_MANIFEST, build_single_tool_manifest_text(metadata))


def single_tool_readme_is_current(metadata: Dict[str, ToolMeta]) -> bool:
    return SINGLE_TOOL_README.exists() and SINGLE_TOOL_README.read_text(encoding="utf-8") == build_single_tool_readme_text(metadata)


def single_tool_manifest_is_current(metadata: Dict[str, ToolMeta]) -> bool:
    return SINGLE_TOOL_MANIFEST.exists() and SINGLE_TOOL_MANIFEST.read_text(encoding="utf-8") == build_single_tool_manifest_text(metadata)


def build_single_tool_zip_bytes(metadata: Dict[str, ToolMeta]) -> bytes:
    buffer = io.BytesIO()
    fixed_time = (2026, 1, 1, 0, 0, 0)
    specs = configured_single_tool_specs(metadata)
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        readme_info = zipfile.ZipInfo(filename="README.md", date_time=fixed_time)
        readme_info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(readme_info, build_single_tool_readme_text(metadata).encode("utf-8"))
        manifest_info = zipfile.ZipInfo(filename="single_tool_manifest.json", date_time=fixed_time)
        manifest_info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(manifest_info, build_single_tool_manifest_text(metadata).encode("utf-8"))
        for spec in specs:
            path = ROOT / str(spec["latest_output"])
            if not path.exists():
                raise FileNotFoundError(f"Cannot add missing single-tool pack to ZIP: {path}")
            info = zipfile.ZipInfo(filename=Path(str(spec["latest_output"])).name, date_time=fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    return buffer.getvalue()


def single_tool_zip_is_current(metadata: Dict[str, ToolMeta]) -> bool:
    if not SINGLE_TOOL_ZIP.exists():
        return False
    return SINGLE_TOOL_ZIP.read_bytes() == build_single_tool_zip_bytes(metadata)


def rebuild_single_tool_zip(metadata: Dict[str, ToolMeta]) -> bool:
    SINGLE_TOOL_ZIP.parent.mkdir(parents=True, exist_ok=True)
    before = SINGLE_TOOL_ZIP.read_bytes() if SINGLE_TOOL_ZIP.exists() else None
    after = build_single_tool_zip_bytes(metadata)
    if before == after:
        return False
    SINGLE_TOOL_ZIP.write_bytes(after)
    return True


def validate_single_tool_zip_contents(metadata: Dict[str, ToolMeta]) -> None:
    if not SINGLE_TOOL_ZIP.exists():
        raise FileNotFoundError(f"Single-tool ZIP does not exist: {SINGLE_TOOL_ZIP}")
    expected = sorted(["README.md", "single_tool_manifest.json"] + expected_single_tool_relpaths(metadata))
    with zipfile.ZipFile(SINGLE_TOOL_ZIP, "r") as zf:
        actual = sorted(zf.namelist())
        if "single_tool_manifest.json" in zf.namelist():
            data = json.loads(zf.read("single_tool_manifest.json").decode("utf-8"))
            if data.get("pack_count") != len(expected_single_tool_relpaths(metadata)):
                raise ValueError("Single-tool ZIP manifest pack_count does not match expected single-tool count")
    if actual != expected:
        raise ValueError(f"Single-tool ZIP contents differ. Expected {expected}, got {actual}")


def custom_pack_files_for_distribution(metadata: Dict[str, ToolMeta]) -> List[Path]:
    """Return generated custom-pack Markdown files that should be included in the custom ZIP."""
    files: List[Path] = []
    if CUSTOM_PACK_DIR.exists():
        for pack_file in sorted(CUSTOM_PACK_DIR.glob("*.yml")):
            spec = normalise_pack_spec(read_simple_yaml(pack_file), metadata)
            files.append(ROOT / str(spec["latest_output"]))
    return files


def build_custom_pack_readme_text(metadata: Dict[str, ToolMeta]) -> str:
    lines = [
        "# AI Personal Tutor custom prompt packs",
        "",
        "This folder contains generated custom packs built from YAML files in `src/prompt-library/custom-packs/`.",
        "Each custom pack includes the shared operating rules, the generated menu/router, and the selected tool instructions.",
        "",
        "Build all custom packs from the repository root with:",
        "",
        "```bash",
        "python scripts/build_prompt_libraries.py --include-custom",
        "```",
        "",
        "Check all custom packs without writing changes with:",
        "",
        "```bash",
        "python scripts/build_prompt_libraries.py --include-custom --check",
        "```",
        "",
        "## Included custom packs",
        "",
    ]
    if not CUSTOM_PACK_DIR.exists() or not list(CUSTOM_PACK_DIR.glob("*.yml")):
        lines.append("No custom-pack YAML files were found.")
        return "\n".join(lines).rstrip() + "\n"

    for pack_file in sorted(CUSTOM_PACK_DIR.glob("*.yml")):
        spec = normalise_pack_spec(read_simple_yaml(pack_file), metadata)
        tools = ordered_tool_meta(spec, metadata)
        output = str(spec.get("latest_output", ""))
        lines.extend([
            f"### {spec.get('title', spec.get('id', 'Custom pack'))}",
            "",
            f"- Source YAML: `{pack_file.relative_to(ROOT).as_posix()}`",
            f"- Generated file: `{output}`",
            f"- Tool count: {len(tools)}",
            "- Tools: " + ", ".join(f"{tool.code} — {tool.title}" for tool in tools),
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def build_custom_pack_zip_bytes(metadata: Dict[str, ToolMeta]) -> bytes:
    files = custom_pack_files_for_distribution(metadata)
    if not files:
        raise FileNotFoundError(f"No generated custom packs found under {CUSTOM_OUTPUT_DIR}")
    buffer = io.BytesIO()
    fixed_time = (2026, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        readme_text = build_custom_pack_readme_text(metadata)
        info = zipfile.ZipInfo(filename="README.md", date_time=fixed_time)
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, readme_text.encode("utf-8"))
        for path in files:
            if not path.exists():
                raise FileNotFoundError(f"Cannot add missing custom pack to ZIP: {path}")
            info = zipfile.ZipInfo(filename=path.name, date_time=fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    return buffer.getvalue()


def custom_pack_zip_is_current(metadata: Dict[str, ToolMeta]) -> bool:
    if not CUSTOM_PACK_ZIP.exists():
        return False
    return CUSTOM_PACK_ZIP.read_bytes() == build_custom_pack_zip_bytes(metadata)


def rebuild_custom_pack_readme(metadata: Dict[str, ToolMeta]) -> bool:
    CUSTOM_PACK_README.parent.mkdir(parents=True, exist_ok=True)
    return write_if_changed(CUSTOM_PACK_README, build_custom_pack_readme_text(metadata))


def rebuild_custom_pack_zip(metadata: Dict[str, ToolMeta]) -> bool:
    CUSTOM_PACK_ZIP.parent.mkdir(parents=True, exist_ok=True)
    before = CUSTOM_PACK_ZIP.read_bytes() if CUSTOM_PACK_ZIP.exists() else None
    after = build_custom_pack_zip_bytes(metadata)
    if before == after:
        return False
    CUSTOM_PACK_ZIP.write_bytes(after)
    return True


def validate_custom_pack_zip_contents(metadata: Dict[str, ToolMeta]) -> None:
    if not CUSTOM_PACK_ZIP.exists():
        raise FileNotFoundError(f"Custom-pack ZIP does not exist: {CUSTOM_PACK_ZIP}")
    expected = sorted(["README.md"] + [path.name for path in custom_pack_files_for_distribution(metadata)])
    with zipfile.ZipFile(CUSTOM_PACK_ZIP, "r") as zf:
        actual = sorted(zf.namelist())
    if actual != expected:
        raise ValueError(f"Custom-pack ZIP contents differ. Expected {expected}, got {actual}")

def configured_pack_files(include_custom: bool = False, custom_pack: Path | None = None) -> List[Path]:
    pack_files = sorted(PACK_DIR.glob("*.yml"))
    if include_custom and CUSTOM_PACK_DIR.exists():
        pack_files.extend(sorted(CUSTOM_PACK_DIR.glob("*.yml")))
    if custom_pack is not None:
        custom_path = custom_pack if custom_pack.is_absolute() else ROOT / custom_pack
        if not custom_path.exists():
            raise FileNotFoundError(f"Custom pack file does not exist: {custom_path}")
        pack_files.append(custom_path)
    # Deduplicate while preserving order.
    seen: set[Path] = set()
    unique: List[Path] = []
    for pack_file in pack_files:
        resolved = pack_file.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(pack_file)
    return unique


def validate_pack_sources(metadata: Dict[str, ToolMeta], pack_files: List[Path] | None = None, extra_specs: List[Dict[str, object]] | None = None) -> None:
    if not HEADER.exists():
        raise FileNotFoundError(f"Missing header file: {HEADER}")
    if pack_files is None:
        pack_files = configured_pack_files()
    if not pack_files:
        raise FileNotFoundError(f"No pack files found in {PACK_DIR}")

    all_tool_source_ids: set[str] = set()
    for tool_path in sorted((SRC / "tools").glob("*.md")):
        rel = tool_path.relative_to(SRC).as_posix()
        validate_tool_source_metadata(rel, metadata)
        tool_id = source_tool_id(rel)
        if tool_id in all_tool_source_ids:
            raise ValueError(f"Duplicate tool source id found: {tool_id}")
        all_tool_source_ids.add(tool_id)

    metadata_ids = set(metadata)
    if all_tool_source_ids != metadata_ids:
        missing_source = sorted(metadata_ids - all_tool_source_ids)
        missing_metadata = sorted(all_tool_source_ids - metadata_ids)
        details = []
        if missing_source:
            details.append(f"metadata without source: {', '.join(missing_source)}")
        if missing_metadata:
            details.append(f"source without metadata: {', '.join(missing_metadata)}")
        raise ValueError("Tool source/metadata mismatch: " + "; ".join(details))

    seen_pack_ids: set[str] = set()
    specs_to_validate: List[tuple[str, Dict[str, object]]] = []
    for pack_file in pack_files:
        specs_to_validate.append((str(pack_file), read_simple_yaml(pack_file)))
    for spec in extra_specs or []:
        specs_to_validate.append((str(spec.get("id", "single-tool-spec")), spec))

    for source_label, raw_spec in specs_to_validate:
        spec = normalise_pack_spec(raw_spec, metadata)
        pack_id = str(spec.get("id", ""))
        if not pack_id:
            raise ValueError(f"{source_label}: missing pack id")
        if pack_id in seen_pack_ids:
            raise ValueError(f"Duplicate pack id: {pack_id}")
        seen_pack_ids.add(pack_id)

        ids = pack_tool_ids(spec, metadata)
        if not ids:
            raise ValueError(f"{source_label}: pack has no tool files")
        if len(ids) != len(set(ids)):
            raise ValueError(f"{source_label}: duplicate tool IDs in pack")
        missing_meta = [tool_id for tool_id in ids if tool_id not in metadata]
        if missing_meta:
            raise ValueError(f"{source_label}: missing metadata for {', '.join(missing_meta)}")

        ordered = ordered_tool_meta(spec, metadata)
        latest, archive, text = build_pack_from_spec(spec, metadata)
        for marker in SECTION_MARKERS.values():
            if f"<!-- FILE: {marker} -->" not in text:
                raise ValueError(f"{source_label}: generated output has no {marker} block")
        if "{{" in text or "}}" in text:
            raise ValueError(f"{source_label}: generated output contains unresolved template markers")

        validate_rendered_pack_semantics(spec, text, ordered)

        if pack_id != "master":
            for number, tool in enumerate(ordered, start=1):
                if f"menu_number: {number}" not in text:
                    raise ValueError(f"{source_label}: mini-library/single-tool output missing local menu_number {number}")

    required_pack_ids = {"master", "writing-tutor", "structure-tutor", "academic-thinking", "research-proposal", "study-workflow"}
    if not required_pack_ids.issubset(seen_pack_ids):
        missing = sorted(required_pack_ids - seen_pack_ids)
        raise ValueError(f"Missing required pack(s): {', '.join(missing)}")


def list_packs(include_custom: bool = False, include_single_tools: bool = False) -> None:
    metadata = load_tool_metadata()
    for pack_file in configured_pack_files(include_custom=include_custom):
        raw = read_simple_yaml(pack_file)
        spec = normalise_pack_spec(raw, metadata)
        tools = ordered_tool_meta(spec, metadata)
        label = "custom" if ("include_tools" in raw or str(spec.get("kind", "")).lower() == "custom") else "core"
        print(f"{spec.get('id')}: {spec.get('title', '')} [{label}]")
        for number, tool in enumerate(tools, start=1):
            print(f"  {number:>2}. {tool.code} — {tool.title} ({tool.id})")
    if include_single_tools:
        for spec in configured_single_tool_specs(metadata):
            tools = ordered_tool_meta(spec, metadata)
            print(f"{spec.get('id')}: {spec.get('title', '')} [single-tool]")
            for number, tool in enumerate(tools, start=1):
                print(f"  {number:>2}. {tool.code} — {tool.title} ({tool.id})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build AI Personal Tutor prompt libraries from source blocks.")
    parser.add_argument("--check", action="store_true", help="Fail if generated files differ from the files currently in the repository.")
    parser.add_argument("--validate", action="store_true", help="Validate source metadata and generated semantics without writing files.")
    parser.add_argument("--list-packs", action="store_true", help="List configured packs and generated menu order, then exit.")
    parser.add_argument("--include-custom", action="store_true", help="Also build/check custom packs from src/prompt-library/custom-packs/. v1.4+ also updates the custom-pack README and ZIP when writing.")
    parser.add_argument("--custom-pack", type=Path, help="Build/check one custom pack YAML file. Path can be relative to the repository root.")
    parser.add_argument("--include-single-tools", action="store_true", help="Also build/check every single-tool pack plus the generated single-tool README, manifest and ZIP.")
    parser.add_argument("--single-tool", help="Build/check one single-tool pack by code such as WT1 or stable tool id such as clarity-clinic.")
    parser.add_argument("--ci", action="store_true", help="Run the no-write checks intended for GitHub Actions: validate all pack sources and check core generated outputs.")
    args = parser.parse_args()

    if args.single_tool and args.include_single_tools:
        parser.error("Use either --single-tool or --include-single-tools, not both.")

    if args.ci:
        if args.single_tool or args.custom_pack or args.include_custom or args.include_single_tools or args.check or args.validate or args.list_packs:
            parser.error("Use --ci on its own; it already performs the intended no-write validation/check sequence.")
        metadata = load_tool_metadata()
        all_pack_files = configured_pack_files(include_custom=True)
        all_single_specs = configured_single_tool_specs(metadata)
        validate_pack_sources(metadata, pack_files=all_pack_files, extra_specs=all_single_specs)
        if MINI_ZIP.exists():
            validate_mini_zip_contents()
        if SINGLE_TOOL_ZIP.exists():
            validate_single_tool_zip_contents(metadata)
        if CUSTOM_PACK_ZIP.exists():
            validate_custom_pack_zip_contents(metadata)

        changes: List[str] = []
        diffs: List[str] = []
        generated_texts: List[tuple[Path, str]] = []
        for pack_file in configured_pack_files():
            latest, archive, text = build_pack(pack_file, metadata)
            for path in [latest, archive] if archive else [latest]:
                current = path.read_text(encoding="utf-8") if path.exists() else ""
                if current != text:
                    changes.append(str(path.relative_to(ROOT)))
                    generated_texts.append((path, text))
                    diff = difflib.unified_diff(
                        current.splitlines(), text.splitlines(),
                        fromfile=str(path.relative_to(ROOT)),
                        tofile=f"generated/{path.relative_to(ROOT)}", lineterm="")
                    diffs.extend(list(diff)[:200])
        if not mini_zip_is_current():
            changes.append(str(MINI_ZIP.relative_to(ROOT)))
        if changes:
            print_stale_output_diagnostics(changes, diffs, generated_texts)
            return 1
        print("CI prompt-library checks passed: source metadata, optional pack specs and core generated outputs are current.")
        return 0

    if args.list_packs:
        list_packs(include_custom=args.include_custom, include_single_tools=args.include_single_tools or bool(args.single_tool))
        return 0

    metadata = load_tool_metadata()
    pack_files = configured_pack_files(include_custom=args.include_custom, custom_pack=args.custom_pack)
    single_tool_specs = configured_single_tool_specs(metadata, args.single_tool) if (args.include_single_tools or args.single_tool) else []
    validate_pack_sources(metadata, pack_files=pack_files, extra_specs=single_tool_specs)

    if args.validate:
        if MINI_ZIP.exists():
            validate_mini_zip_contents()
        if args.include_single_tools:
            if SINGLE_TOOL_README.exists() and not single_tool_readme_is_current(metadata):
                raise ValueError(f"Single-tool README is out of date: {SINGLE_TOOL_README}")
            if SINGLE_TOOL_MANIFEST.exists() and not single_tool_manifest_is_current(metadata):
                raise ValueError(f"Single-tool manifest is out of date: {SINGLE_TOOL_MANIFEST}")
            if SINGLE_TOOL_ZIP.exists():
                validate_single_tool_zip_contents(metadata)
        if args.include_custom and CUSTOM_PACK_ZIP.exists():
            validate_custom_pack_zip_contents(metadata)
        print("Prompt-library source metadata and generated pack semantics validated.")
        return 0

    changes: List[str] = []
    diffs: List[str] = []
    generated_texts: List[tuple[Path, str]] = []
    build_items: List[tuple[Path | None, Dict[str, object] | None]] = [(pack_file, None) for pack_file in pack_files]
    build_items.extend((None, spec) for spec in single_tool_specs)

    for pack_file, spec in build_items:
        if pack_file is not None:
            latest, archive, text = build_pack(pack_file, metadata)
        else:
            assert spec is not None
            latest, archive, text = build_pack_from_spec(spec, metadata)
        for path in [latest, archive] if archive else [latest]:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != text:
                changes.append(str(path.relative_to(ROOT)))
                generated_texts.append((path, text))
                if args.check:
                    diff = difflib.unified_diff(
                        current.splitlines(), text.splitlines(),
                        fromfile=str(path.relative_to(ROOT)),
                        tofile=f"generated/{path.relative_to(ROOT)}", lineterm="")
                    diffs.extend(list(diff)[:200])
                else:
                    write_if_changed(path, text)

    built_core_packs = any((PACK_DIR / pack_file.name).resolve() == pack_file.resolve() for pack_file in pack_files)

    if args.check:
        if built_core_packs and not mini_zip_is_current():
            changes.append(str(MINI_ZIP.relative_to(ROOT)))
        if args.include_single_tools:
            if not single_tool_readme_is_current(metadata):
                changes.append(str(SINGLE_TOOL_README.relative_to(ROOT)))
            if not single_tool_manifest_is_current(metadata):
                changes.append(str(SINGLE_TOOL_MANIFEST.relative_to(ROOT)))
            if not single_tool_zip_is_current(metadata):
                changes.append(str(SINGLE_TOOL_ZIP.relative_to(ROOT)))
        if args.include_custom:
            readme_text = build_custom_pack_readme_text(metadata)
            current_readme = CUSTOM_PACK_README.read_text(encoding="utf-8") if CUSTOM_PACK_README.exists() else ""
            if current_readme != readme_text:
                changes.append(str(CUSTOM_PACK_README.relative_to(ROOT)))
            if not custom_pack_zip_is_current(metadata):
                changes.append(str(CUSTOM_PACK_ZIP.relative_to(ROOT)))
        if changes:
            print_stale_output_diagnostics(changes, diffs, generated_texts)
            return 1
        if MINI_ZIP.exists():
            validate_mini_zip_contents()
        if args.include_single_tools and SINGLE_TOOL_ZIP.exists():
            validate_single_tool_zip_contents(metadata)
        if args.include_custom and CUSTOM_PACK_ZIP.exists():
            validate_custom_pack_zip_contents(metadata)
        print("Prompt-library generated files are up to date and semantic validation passed.")
        return 0

    built_core_packs = any((PACK_DIR / pack_file.name).resolve() == pack_file.resolve() for pack_file in pack_files)
    if built_core_packs and rebuild_mini_zip():
        changes.append(str(MINI_ZIP.relative_to(ROOT)))
    if args.include_single_tools:
        if rebuild_single_tool_readme(metadata):
            changes.append(str(SINGLE_TOOL_README.relative_to(ROOT)))
        if rebuild_single_tool_manifest(metadata):
            changes.append(str(SINGLE_TOOL_MANIFEST.relative_to(ROOT)))
        if rebuild_single_tool_zip(metadata):
            changes.append(str(SINGLE_TOOL_ZIP.relative_to(ROOT)))
    if args.include_custom:
        if rebuild_custom_pack_readme(metadata):
            changes.append(str(CUSTOM_PACK_README.relative_to(ROOT)))
        if rebuild_custom_pack_zip(metadata):
            changes.append(str(CUSTOM_PACK_ZIP.relative_to(ROOT)))

    if changes:
        print("Updated generated prompt-library files:")
        for change in changes:
            print(f"  - {change}")
    else:
        print("No prompt-library changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
