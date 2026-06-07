#!/usr/bin/env python3
"""Build machine-readable site integration data from generator source metadata.

Package Generator v1.6 helper.

This script creates small JSON files under docs/data/. They are not used by the
current static pages yet, but they provide a single generated data source that
future pages can read instead of manually duplicating tool, pack and release
metadata.

Typical use from the repository root:
    python scripts/build_site_data.py

Check mode:
    python scripts/build_site_data.py --check

Validate source metadata and any current generated data:
    python scripts/build_site_data.py --validate
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_prompt_libraries as bpl  # type: ignore  # local generator module

DATA_DIR = ROOT / "docs" / "data"
RELEASE_JSON = DATA_DIR / "release.json"
TOOL_INDEX_JSON = DATA_DIR / "tool_index.json"
PROMPT_LIBRARY_PACKS_JSON = DATA_DIR / "prompt_library_packs.json"

OUTPUTS = [RELEASE_JSON, TOOL_INDEX_JSON, PROMPT_LIBRARY_PACKS_JSON]
GENERATOR_VERSION = "1.6"


def json_text(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def rel(path: Path | str | None) -> str | None:
    if path is None:
        return None
    p = ROOT / path if isinstance(path, str) else path
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def release_data() -> dict[str, Any]:
    release = bpl.read_release_metadata()
    return {
        "generated_by": f"ai-personal-tutor-package-generator-v{GENERATOR_VERSION}",
        "toolkit_version": release.get("toolkit_version", ""),
        "prompt_library_version": release.get("prompt_library_version", ""),
        "testing_pack_version": release.get("testing_pack_version", ""),
        "release_date": release.get("release_date", ""),
        "source": "src/release.yml",
    }


def tool_source_path_by_id() -> dict[str, str]:
    return bpl.tool_source_paths_by_id()


def pack_records(metadata: dict[str, bpl.ToolMeta]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for pack_file in bpl.configured_pack_files(include_custom=True):
        raw = bpl.read_simple_yaml(pack_file)
        spec = bpl.normalise_pack_spec(raw, metadata)
        tools = bpl.ordered_tool_meta(spec, metadata)
        kind = str(spec.get("kind", "core"))
        if "include_tools" in raw:
            kind = "custom"
        records.append({
            "id": str(spec.get("id", "")),
            "title": str(spec.get("title", "")),
            "kind": kind,
            "source": rel(pack_file),
            "latest_output": str(spec.get("latest_output", "")),
            "archive_output": str(spec.get("archive_output", "")) if spec.get("archive_output") else None,
            "tool_count": len(tools),
            "tool_codes": [tool.code for tool in tools],
            "tool_ids": [tool.id for tool in tools],
        })
    return records


def single_tool_records(metadata: dict[str, bpl.ToolMeta]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for spec in bpl.configured_single_tool_specs(metadata):
        tools = bpl.ordered_tool_meta(spec, metadata)
        tool = tools[0]
        records.append({
            "id": str(spec.get("id", "")),
            "title": str(spec.get("title", "")),
            "kind": "single-tool",
            "latest_output": str(spec.get("latest_output", "")),
            "tool_count": 1,
            "tool_codes": [tool.code],
            "tool_ids": [tool.id],
        })
    return records


def prompt_library_packs_data(metadata: dict[str, bpl.ToolMeta]) -> dict[str, Any]:
    core_and_custom = pack_records(metadata)
    singles = single_tool_records(metadata)
    all_packs = core_and_custom + singles
    return {
        **release_data(),
        "pack_count": len(all_packs),
        "core_pack_count": len([p for p in core_and_custom if p["kind"] == "core"]),
        "custom_pack_count": len([p for p in core_and_custom if p["kind"] == "custom"]),
        "single_tool_pack_count": len(singles),
        "packs": all_packs,
    }


def tool_index_data(metadata: dict[str, bpl.ToolMeta]) -> dict[str, Any]:
    source_by_id = tool_source_path_by_id()
    packs = pack_records(metadata)
    singles = {rec["tool_ids"][0]: rec for rec in single_tool_records(metadata)}
    tools: list[dict[str, Any]] = []
    for tool in metadata.values():
        included_in = [pack["id"] for pack in packs if tool.id in pack["tool_ids"]]
        single = singles.get(tool.id)
        tools.append({
            "code": tool.code,
            "id": tool.id,
            "title": tool.title,
            "family": tool.family,
            "family_label": tool.family_label,
            "mini_family_label": tool.mini_family_label,
            "source": source_by_id.get(tool.id, ""),
            "master_manifest_description": tool.master_manifest_description,
            "mini_manifest_description": tool.mini_manifest_description,
            "launcher_description": tool.launcher_description,
            "included_in_packs": included_in,
            "single_tool_output": single.get("latest_output") if single else None,
        })
    return {
        **release_data(),
        "tool_count": len(tools),
        "tools": tools,
    }


def expected_outputs() -> dict[Path, str]:
    metadata = bpl.load_tool_metadata()
    bpl.validate_pack_sources(
        metadata,
        pack_files=bpl.configured_pack_files(include_custom=True),
        extra_specs=bpl.configured_single_tool_specs(metadata),
    )
    return {
        RELEASE_JSON: json_text(release_data()),
        TOOL_INDEX_JSON: json_text(tool_index_data(metadata)),
        PROMPT_LIBRARY_PACKS_JSON: json_text(prompt_library_packs_data(metadata)),
    }


def write_outputs() -> list[str]:
    changes: list[str] = []
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for path, text in expected_outputs().items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            path.write_text(text, encoding="utf-8")
            changes.append(rel(path) or str(path))
    return changes


def check_outputs() -> list[str]:
    changes: list[str] = []
    for path, text in expected_outputs().items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != text:
            changes.append(rel(path) or str(path))
    return changes


def validate_current_outputs() -> None:
    for path, expected_text in expected_outputs().items():
        if not path.exists():
            raise FileNotFoundError(f"Missing generated site data file: {rel(path)}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {rel(path)}: {exc}") from exc
        expected = json.loads(expected_text)
        if data != expected:
            raise ValueError(f"Generated site data is out of date: {rel(path)}")
    tool_data = json.loads(TOOL_INDEX_JSON.read_text(encoding="utf-8"))
    if tool_data.get("tool_count") != len(tool_data.get("tools", [])):
        raise ValueError("tool_index.json tool_count does not match tools length")
    pack_data = json.loads(PROMPT_LIBRARY_PACKS_JSON.read_text(encoding="utf-8"))
    if pack_data.get("pack_count") != len(pack_data.get("packs", [])):
        raise ValueError("prompt_library_packs.json pack_count does not match packs length")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build generated site integration JSON data.")
    parser.add_argument("--check", action="store_true", help="Fail if docs/data generated files are missing or out of date.")
    parser.add_argument("--validate", action="store_true", help="Validate source metadata and current docs/data generated files.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.check:
        changes = check_outputs()
        if changes:
            print("Generated site data files are out of date:", file=sys.stderr)
            for change in changes:
                print(f"  - {change}", file=sys.stderr)
            print("\nLikely fix from the repository root:", file=sys.stderr)
            print("  python scripts\\build_site_data.py", file=sys.stderr)
            print("  python scripts\\build_site_data.py --check", file=sys.stderr)
            return 1
        print("Generated site data files are up to date.")
        return 0
    if args.validate:
        validate_current_outputs()
        print("Generated site data files validated.")
        return 0
    changes = write_outputs()
    if changes:
        print("Updated generated site data files:")
        for change in changes:
            print(f"  - {change}")
    else:
        print("No site data changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
