#!/usr/bin/env python3
"""Build AI Personal Tutor prompt libraries from source blocks.

Package Generator v0.1

This first generator intentionally keeps the current prompt-library structure intact.
It concatenates source blocks into the master library and five mini-libraries, then
rebuilds the mini-libraries ZIP.

Run from the repository root:
    python scripts/build_prompt_libraries.py

Check mode:
    python scripts/build_prompt_libraries.py --check
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
import zipfile
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "prompt-library"
PACK_DIR = SRC / "packs"
HEADER = SRC / "header.md"
MINI_ZIP = ROOT / "docs" / "prompt-libraries" / "latest" / "ai_personal_tutor_mini_libraries.zip"

MINI_LIBRARY_LATEST = [
    "docs/prompt-libraries/latest/01_writing_tutor_library.md",
    "docs/prompt-libraries/latest/02_structure_tutor_library.md",
    "docs/prompt-libraries/latest/03_academic_thinking_tutor_library.md",
    "docs/prompt-libraries/latest/04_research_proposal_tutor_library.md",
    "docs/prompt-libraries/latest/05_study_workflow_tutor_library.md",
]


def read_simple_yaml(path: Path) -> Dict[str, object]:
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


def read_source(rel_path: str) -> str:
    path = SRC / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Missing source block: {path}")
    return path.read_text(encoding="utf-8")


def mini_tool_metadata(block: str, menu_number: int) -> str:
    """Convert a master tool block to a mini-library block.

    v0.1 uses the master tool block as the canonical tool body. Mini-libraries need
    local menu numbering, and they do not include the optional master_number field.
    """
    block = re.sub(r"^master_number: .*\n", "", block, flags=re.MULTILINE)
    block = re.sub(r"^menu_number: .*\n", f"menu_number: {menu_number}\n", block, count=1, flags=re.MULTILINE)
    return block


def build_pack(pack_file: Path) -> tuple[Path, Path | None, str]:
    spec = read_simple_yaml(pack_file)
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

    parts: List[str] = [HEADER.read_text(encoding="utf-8")]
    parts.extend(read_source(str(rel)) for rel in sections)
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


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def rebuild_mini_zip() -> bool:
    MINI_ZIP.parent.mkdir(parents=True, exist_ok=True)
    before = MINI_ZIP.read_bytes() if MINI_ZIP.exists() else None
    tmp = MINI_ZIP.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in MINI_LIBRARY_LATEST:
            path = ROOT / rel
            if not path.exists():
                raise FileNotFoundError(f"Cannot add missing mini-library to ZIP: {path}")
            zf.write(path, arcname=Path(rel).name)
    after = tmp.read_bytes()
    if before == after:
        tmp.unlink()
        return False
    tmp.replace(MINI_ZIP)
    return True


def validate_pack_sources() -> None:
    if not HEADER.exists():
        raise FileNotFoundError(f"Missing header file: {HEADER}")
    pack_files = sorted(PACK_DIR.glob("*.yml"))
    if not pack_files:
        raise FileNotFoundError(f"No pack files found in {PACK_DIR}")
    for pack_file in pack_files:
        latest, archive, text = build_pack(pack_file)
        for marker in ["00-manifest.md", "03-launcher.md", "04-router.md"]:
            if f"<!-- FILE: {marker} -->" not in text:
                raise ValueError(f"{pack_file}: generated output has no {marker} block")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build AI Personal Tutor prompt libraries from source blocks.")
    parser.add_argument("--check", action="store_true", help="Fail if generated files differ from the files currently in the repository.")
    args = parser.parse_args()

    validate_pack_sources()
    changes: List[str] = []
    diffs: List[str] = []
    for pack_file in sorted(PACK_DIR.glob("*.yml")):
        latest, archive, text = build_pack(pack_file)
        for path in [latest, archive] if archive else [latest]:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != text:
                changes.append(str(path.relative_to(ROOT)))
                if args.check:
                    diff = difflib.unified_diff(
                        current.splitlines(), text.splitlines(),
                        fromfile=str(path.relative_to(ROOT)),
                        tofile=f"generated/{path.relative_to(ROOT)}", lineterm="")
                    diffs.extend(list(diff)[:200])
                else:
                    write_if_changed(path, text)

    if args.check:
        if changes:
            print("Generated prompt-library files are out of date:", file=sys.stderr)
            for change in changes:
                print(f"  - {change}", file=sys.stderr)
            if diffs:
                print("\nFirst diff lines:", file=sys.stderr)
                print("\n".join(diffs), file=sys.stderr)
            return 1
        print("Prompt-library generated files are up to date.")
        return 0

    if rebuild_mini_zip():
        changes.append(str(MINI_ZIP.relative_to(ROOT)))

    if changes:
        print("Updated generated prompt-library files:")
        for change in changes:
            print(f"  - {change}")
    else:
        print("No prompt-library changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
