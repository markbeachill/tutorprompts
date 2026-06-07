#!/usr/bin/env python3
"""Sync release metadata to generated prompt-library outputs.

Package Generator v2.5 helper.

This is a convenience recovery tool for the common mixed-version state where
`docs/prompt-libraries/latest/` has already been generated for a newer prompt-library
version, but `src/release.yml` still carries the previous version.

Typical use from the repository root:
    python scripts/sync_release_metadata.py --to-generated --build --check

The audit/testing pack keeps its own version unless you explicitly use the lower-level
prepare_toolkit_release.py command with --testing-pack-version.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
RELEASE_YML = ROOT / "src" / "release.yml"
LATEST = ROOT / "docs" / "prompt-libraries" / "latest"

PROMPT_FILES = [
    "ai_personal_tutor_master_library.md",
    "01_writing_tutor_library.md",
    "02_structure_tutor_library.md",
    "03_academic_thinking_tutor_library.md",
    "04_research_proposal_tutor_library.md",
    "05_study_workflow_tutor_library.md",
]


def simple_yaml_load(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.strip().lstrip("v").split(".") if part.isdigit())


def find_first(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else None


@dataclass(frozen=True)
class GeneratedVersionScan:
    versions: list[str]
    files_scanned: int

    @property
    def target_version(self) -> str | None:
        if not self.versions:
            return None
        return sorted(set(self.versions), key=version_key)[-1]

    @property
    def summary(self) -> str:
        if not self.versions:
            return "none"
        return ", ".join(sorted(set(self.versions), key=version_key))


def scan_generated_prompt_versions() -> GeneratedVersionScan:
    versions: list[str] = []
    files_scanned = 0
    for name in PROMPT_FILES:
        path = LATEST / name
        if not path.exists():
            continue
        files_scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in [
            r"^version:\s*v?([0-9]+(?:\.[0-9]+)+)\s*$",
            r"^\*\*Version:\*\*\s*v?([0-9]+(?:\.[0-9]+)+)\s*$",
            r"\*\*This file:\*\*[^\n]*?\bv([0-9]+(?:\.[0-9]+)+)",
            r"\*\*Fixed archive:\*\*\s*`prompt-libraries/v([0-9]+(?:\.[0-9]+)+)/",
        ]:
            value = find_first(pattern, text)
            if value:
                versions.append(value)
    return GeneratedVersionScan(versions=versions, files_scanned=files_scanned)


def run(args: list[str], *, dry_run: bool = False) -> int:
    cmd = [sys.executable, *args]
    print("  " + " ".join(cmd))
    if dry_run:
        return 0
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync src/release.yml to the newest generated prompt-library version."
    )
    parser.add_argument(
        "--to-generated",
        action="store_true",
        help="Infer the target version from docs/prompt-libraries/latest/. This is the normal recovery mode.",
    )
    parser.add_argument(
        "--date",
        help="Release date to write. Defaults to src/release.yml release_date, then today's date if missing.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="After updating release metadata, rebuild prompt libraries and site data.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="After optional build, run scripts/run_generator_checks.py.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without changing files.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.to_generated:
        print("No sync mode selected. Use --to-generated.")
        return 2

    release = simple_yaml_load(RELEASE_YML)
    scan = scan_generated_prompt_versions()
    target_version = scan.target_version
    if not target_version:
        print("Could not infer a prompt-library version from docs/prompt-libraries/latest/.")
        print("Run build_prompt_libraries.py first, or use prepare_toolkit_release.py directly.")
        return 1

    current_toolkit = release.get("toolkit_version", "unknown")
    current_prompt = release.get("prompt_library_version", "unknown")
    current_testing = release.get("testing_pack_version", "unknown")
    release_date = args.date or release.get("release_date") or __import__("datetime").date.today().isoformat()

    print("Release metadata sync")
    print(f"  src/release.yml toolkit_version: {current_toolkit}")
    print(f"  src/release.yml prompt_library_version: {current_prompt}")
    print(f"  src/release.yml testing_pack_version: {current_testing}")
    print(f"  generated prompt-library version stamp(s): {scan.summary}")
    print(f"  target toolkit/prompt-library version: {target_version}")
    print(f"  release date: {release_date}")
    print()

    if current_toolkit == target_version and current_prompt == target_version:
        print("src/release.yml already matches the newest generated prompt-library version.")
    else:
        print("Updating release metadata and prompt-library source stamps:")
        rc = run(["scripts/prepare_toolkit_release.py", "--version", target_version, "--date", release_date], dry_run=args.dry_run)
        if rc:
            return rc
        print()
        print("Note: testing_pack_version is left unchanged by this command. Use")
        print("prepare_toolkit_release.py --testing-pack-version only when audit/testing content changes.")

    if args.build:
        print()
        print("Rebuilding generated prompt libraries and site data:")
        for cmd in [
            ["scripts/build_prompt_libraries.py"],
            ["scripts/build_site_data.py"],
        ]:
            rc = run(cmd, dry_run=args.dry_run)
            if rc:
                return rc

    if args.check:
        print()
        print("Running standard generator checks:")
        rc = run(["scripts/run_generator_checks.py"], dry_run=args.dry_run)
        if rc:
            return rc

    if not args.build and not args.check:
        print()
        print("Next suggested commands:")
        print("  python scripts\\build_prompt_libraries.py")
        print("  python scripts\\build_site_data.py")
        print("  python scripts\\run_generator_checks.py")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
