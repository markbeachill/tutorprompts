#!/usr/bin/env python3
"""Run the normal toolkit release build sequence.

Package Generator v1.9 helper.

This script is an orchestration convenience. It does not replace the underlying
scripts; it runs them in the safe order:

1. prepare structured version/date stamps;
2. rebuild prompt-library outputs;
3. rebuild audit/testing pack outputs;
4. run prompt-library and audit/testing CI checks;
5. build generated site integration data;
6. check generated site integration data;
7. run release consistency checks;
8. optionally create a draft release-notes file;
9. build the clean public site package;
10. check that the package is current.

Typical use from the repository root:
    python scripts/build_toolkit_release.py --version 3.6 --date 2026-06-14

Use --dry-run to print the commands without executing them.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
RELEASE_YML = ROOT / "src" / "release.yml"


@dataclass(frozen=True)
class ReleasePlan:
    version: str | None
    date: str | None
    dry_run: bool
    skip_prepare: bool
    no_package: bool
    include_custom: bool
    include_single_tools: bool
    output: Path | None
    draft_notes: bool
    force_draft_notes: bool
    testing_pack_version: str | None


def simple_yaml_load(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def normalise_version(version: str | None) -> str | None:
    if version is None:
        return None
    return version.lstrip("v")


def infer_version(explicit: str | None) -> str:
    if explicit:
        return normalise_version(explicit) or explicit
    config = simple_yaml_load(RELEASE_YML)
    version = config.get("toolkit_version") or config.get("prompt_library_version")
    if not version:
        raise SystemExit("No version supplied and src/release.yml does not contain toolkit_version.")
    return version.lstrip("v")


def display_command(cmd: Sequence[str]) -> str:
    return " ".join(cmd)


def run(cmd: Sequence[str], dry_run: bool) -> None:
    print("$ " + display_command(cmd))
    if dry_run:
        return
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def build_commands(plan: ReleasePlan) -> list[list[str]]:
    python = sys.executable
    version = infer_version(plan.version)
    release_date = plan.date or simple_yaml_load(RELEASE_YML).get("release_date") or date.today().isoformat()

    commands: list[list[str]] = []
    if not plan.skip_prepare:
        commands.append([
            python,
            "scripts/prepare_toolkit_release.py",
            "--version",
            version,
            "--date",
            release_date,
        ])
        if plan.testing_pack_version:
            commands[-1].extend(["--testing-pack-version", normalise_version(plan.testing_pack_version) or plan.testing_pack_version])

    build_cmd = [python, "scripts/build_prompt_libraries.py"]
    if plan.include_custom:
        build_cmd.append("--include-custom")
    if plan.include_single_tools:
        build_cmd.append("--include-single-tools")
    commands.append(build_cmd)
    commands.append([python, "scripts/build_audit_pack.py"])

    commands.append([python, "scripts/build_prompt_libraries.py", "--ci"])
    commands.append([python, "scripts/build_audit_pack.py", "--ci"])
    commands.append([python, "scripts/build_site_data.py"])
    commands.append([python, "scripts/build_site_data.py", "--check"])
    commands.append([python, "scripts/release_consistency_check.py", "--fail-on-problems"])

    if plan.draft_notes:
        notes_cmd = [python, "scripts/generate_release_notes_draft.py", "--version", version, "--date", release_date]
        if plan.force_draft_notes:
            notes_cmd.append("--force")
        commands.append(notes_cmd)

    if not plan.no_package:
        package_cmd = [
            python,
            "scripts/build_site_package.py",
            "--run-generator-check",
            "--version",
            version,
        ]
        if plan.output:
            package_cmd.extend(["--output", str(plan.output)])
        commands.append(package_cmd)

        check_cmd = [python, "scripts/build_site_package.py", "--check", "--version", version]
        if plan.output:
            check_cmd.extend(["--output", str(plan.output)])
        commands.append(check_cmd)

    return commands


def parse_args(argv: Sequence[str] | None = None) -> ReleasePlan:
    parser = argparse.ArgumentParser(description="Run the normal toolkit release build sequence.")
    parser.add_argument("--version", help="Toolkit version to prepare/package, for example 3.6. Defaults to src/release.yml.")
    parser.add_argument("--date", help="Release date in YYYY-MM-DD format. Defaults to src/release.yml or today.")
    parser.add_argument("--testing-pack-version", help="Optional testing/audit pack version. If omitted, the existing src/release.yml testing_pack_version is kept.")
    parser.add_argument("--skip-prepare", action="store_true", help="Do not run prepare_toolkit_release.py; use existing stamps.")
    parser.add_argument("--no-package", action="store_true", help="Prepare/rebuild/check prompt libraries, but do not create the site ZIP.")
    parser.add_argument("--include-custom", action="store_true", help="Also build custom packs before checks/package creation.")
    parser.add_argument("--include-single-tools", action="store_true", help="Also build all single-tool packs and their ZIP before checks/package creation.")
    parser.add_argument("--output", type=Path, help="Optional output ZIP path for build_site_package.py.")
    parser.add_argument("--draft-notes", action="store_true", help="Also create a draft update-notes Markdown file using generate_release_notes_draft.py.")
    parser.add_argument("--force-draft-notes", action="store_true", help="Allow --draft-notes to overwrite an existing draft notes file.")
    parser.add_argument("--dry-run", action="store_true", help="Print the release commands without executing them.")
    args = parser.parse_args(argv)
    return ReleasePlan(
        version=args.version,
        date=args.date,
        dry_run=args.dry_run,
        skip_prepare=args.skip_prepare,
        no_package=args.no_package,
        include_custom=args.include_custom,
        include_single_tools=args.include_single_tools,
        output=args.output,
        draft_notes=args.draft_notes,
        force_draft_notes=args.force_draft_notes,
        testing_pack_version=args.testing_pack_version,
    )


def main(argv: Sequence[str] | None = None) -> int:
    plan = parse_args(argv)
    commands = build_commands(plan)
    print("Toolkit release build plan:")
    for cmd in commands:
        run(cmd, dry_run=plan.dry_run)
    if plan.dry_run:
        print("Dry run complete. No files were changed.")
    else:
        print("Toolkit release build complete.")
        print("Review changes with: git status && git diff")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
