#!/usr/bin/env python3
"""Prepare version stamps for an AI Personal Tutor Toolkit release.

Package Generator v1.9 helper.

This script updates the structured version/date stamps used by the prompt-library
source files and the public site labels that are safe to edit mechanically. It is
not a changelog writer: release-note prose remains a manual authoring step.

Typical use from the repository root:
    python scripts/prepare_toolkit_release.py --version 3.6 --date 2026-06-14
    python scripts/build_prompt_libraries.py
    python scripts/build_site_package.py --run-generator-check --version 3.6

Dry run:
    python scripts/prepare_toolkit_release.py --version 3.6 --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
PROMPT_SRC = SRC / "prompt-library"
AUDIT_SRC = SRC / "audit-library"
RELEASE_YML = SRC / "release.yml"


@dataclass(frozen=True)
class ReleaseValues:
    toolkit_version: str
    prompt_library_version: str
    testing_pack_version: str
    release_date: str
    status: str = "active public release"

    @property
    def toolkit_label(self) -> str:
        return "v" + self.toolkit_version.lstrip("v")

    @property
    def prompt_label(self) -> str:
        return "v" + self.prompt_library_version.lstrip("v")

    @property
    def testing_label(self) -> str:
        return "v" + self.testing_pack_version.lstrip("v")

    @property
    def prompt_archive_dir(self) -> str:
        return self.prompt_label

    @property
    def prompt_archive_suffix(self) -> str:
        return "_v" + self.prompt_library_version.lstrip("v").replace(".", "_")


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


def write_release_yml(values: ReleaseValues, dry_run: bool, changed: list[Path]) -> None:
    text = (
        "# Package Generator v1.3 release metadata source.\n"
        "# This file is intentionally simple key: value YAML so it can be read without\n"
        "# third-party Python packages.\n\n"
        f"toolkit_version: {values.toolkit_version}\n"
        f"prompt_library_version: {values.prompt_library_version}\n"
        f"testing_pack_version: {values.testing_pack_version}\n"
        f"release_date: {values.release_date}\n"
        f"status: {values.status}\n"
    )
    replace_file_text(RELEASE_YML, text, dry_run=dry_run, changed=changed, force=True)


def replace_file_text(path: Path, new_text: str, dry_run: bool, changed: list[Path], force: bool = False) -> None:
    old_text = path.read_text(encoding="utf-8") if path.exists() else ""
    if force or old_text != new_text:
        changed.append(path)
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(new_text, encoding="utf-8", newline="\n")


def apply_subs(path: Path, substitutions: Sequence[tuple[str, str]], dry_run: bool, changed: list[Path]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    original = text
    for pattern, repl in substitutions:
        text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    if text != original:
        replace_file_text(path, text, dry_run=dry_run, changed=changed)


def update_prompt_source(values: ReleaseValues, dry_run: bool, changed: list[Path]) -> None:
    if not PROMPT_SRC.exists():
        raise SystemExit("src/prompt-library was not found. Run this from the repository root after installing the package generator.")

    # Pack manifests and launcher headings.
    for path in sorted((PROMPT_SRC / "pack-sections").rglob("*.md")):
        substitutions = [
            (r"^version:\s*[0-9]+(?:\.[0-9]+)*\s*$", f"version: {values.prompt_library_version}"),
            (r"^\*\*Version:\*\*\s*v?[0-9]+(?:\.[0-9]+)*\s*$", f"**Version:** {values.prompt_label}"),
            (r"^\*\*Last updated:\*\*\s*\d{{4}}-\d{{2}}-\d{{2}}\s*$", f"**Last updated:** {values.release_date}"),
            (r"^\*\*Status:\*\*\s*.*$", f"**Status:** {values.status}"),
            (
                r"^\*\*Release stamp:\*\*\s*Toolkit version v?[0-9]+(?:\.[0-9]+)*\s*/\s*Prompt-library suite v?[0-9]+(?:\.[0-9]+)*\s*/\s*Testing pack v?[0-9]+(?:\.[0-9]+)*\s*",
                f"**Release stamp:** Toolkit version {values.toolkit_label} / Prompt-library suite {values.prompt_label} / Testing pack {values.testing_label}  ",
            ),
            (r"^(\*\*This file:\*\*\s*.+?)\s+v[0-9]+(?:\.[0-9]+)*\s*$", rf"\1 {values.prompt_label}"),
            (r"(\*\*This file:\*\*\s*.+?)\s+v[0-9]+(?:\.[0-9]+)*", rf"\1 {values.prompt_label}"),
            (
                r"prompt-libraries/v[0-9]+(?:\.[0-9]+)*/([^`\s]+?)_v[0-9]+(?:_[0-9]+)*\.md",
                lambda_match_to_archive(values),
            ),
            (r"^(#\s+.+?)\s+v[0-9]+(?:\.[0-9]+)*\s*$", rf"\1 {values.prompt_label}"),
        ]
        # re.sub cannot accept a function inside our simple tuple loop, so handle archive after basic substitutions.
        text = path.read_text(encoding="utf-8")
        original = text
        for pattern, repl in substitutions:
            if callable(repl):
                text = re.sub(pattern, repl, text, flags=re.MULTILINE)
            else:
                text = re.sub(pattern, repl, text, flags=re.MULTILINE)
        if text != original:
            replace_file_text(path, text, dry_run=dry_run, changed=changed)

    # Tool headings. This intentionally updates versioned H1 headings only, not ordinary text like "3-5 actions".
    for path in sorted((PROMPT_SRC / "tools").glob("*.md")):
        apply_subs(path, [(r"^(#\s+[A-Z]{2}\d+\s+—\s+.+?)\s+v[0-9]+(?:\.[0-9]+)*\s*$", rf"\1 {values.prompt_label}")], dry_run, changed)

    # Pack archive outputs.
    for path in sorted((PROMPT_SRC / "packs").glob("*.yml")):
        apply_subs(
            path,
            [
                (
                    r"^(archive_output:\s*docs/prompt-libraries/)v[0-9]+(?:\.[0-9]+)*/(.+?)_v[0-9]+(?:_[0-9]+)*\.md\s*$",
                    rf"\1{values.prompt_archive_dir}/\2{values.prompt_archive_suffix}.md",
                )
            ],
            dry_run,
            changed,
        )


def update_audit_source(values: ReleaseValues, dry_run: bool, changed: list[Path]) -> None:
    """Update testing/audit-pack source version stamps where the text carries them."""
    if not AUDIT_SRC.exists():
        return
    for path in sorted(AUDIT_SRC.rglob("*.md")):
        substitutions = [
            (r"^version:\s*[0-9]+(?:\.[0-9]+)*\s*$", f"version: {values.testing_pack_version}"),
            (r"^\*\*Version:\*\*\s*v?[0-9]+(?:\.[0-9]+)*\s*$", f"**Version:** {values.testing_label}"),
            (r"^\*\*Last updated:\*\*\s*\d{{4}}-\d{{2}}-\d{{2}}\s*$", f"**Last updated:** {values.release_date}"),
            (r"^\*\*Status:\*\*\s*.*$", f"**Status:** {values.status}"),
            (
                r"^\*\*Release stamp:\*\*\s*Site package v?[0-9]+(?:\.[0-9]+)*\s*/\s*Prompt-library suite v?[0-9]+(?:\.[0-9]+)*\s*/\s*Testing pack v?[0-9]+(?:\.[0-9]+)*\s*",
                f"**Release stamp:** Site package {values.toolkit_label} / Prompt-library suite {values.prompt_label} / Testing pack {values.testing_label}  ",
            ),
            (
                r"^\*\*Release stamp:\*\*\s*Toolkit version v?[0-9]+(?:\.[0-9]+)*\s*/\s*Prompt-library suite v?[0-9]+(?:\.[0-9]+)*\s*/\s*Testing pack v?[0-9]+(?:\.[0-9]+)*\s*",
                f"**Release stamp:** Toolkit version {values.toolkit_label} / Prompt-library suite {values.prompt_label} / Testing pack {values.testing_label}  ",
            ),
            (r"^(#\s+.+?)\s+v[0-9]+(?:\.[0-9]+)*\s*$", rf"\1 {values.testing_label}"),
            (r"ai_tutor_toolkit_audit_prompt_with_menu_v[0-9]+(?:_[0-9]+)*\.md", "ai_tutor_toolkit_audit_prompt_with_menu.md"),
        ]
        apply_subs(path, substitutions, dry_run, changed)


def lambda_match_to_archive(values: ReleaseValues):
    def repl(match: re.Match[str]) -> str:
        filename_base = match.group(1)
        return f"prompt-libraries/{values.prompt_archive_dir}/{filename_base}{values.prompt_archive_suffix}.md"
    return repl


def update_site_stamps(values: ReleaseValues, dry_run: bool, changed: list[Path]) -> None:
    # These are intentionally conservative replacements. Changelog prose is not rewritten.
    candidates = [
        ROOT / "README.md",
        ROOT / "docs" / "index.html",
        ROOT / "docs" / "tools" / "index.html",
        ROOT / "docs" / "testing.html",
        ROOT / "docs" / "release_manifest.md",
    ]
    for path in candidates:
        if not path.exists():
            continue
        substitutions = [
            (r"Current toolkit version:\s*(?:<strong>)?v?[0-9]+(?:\.[0-9]+)*(?:</strong>)?", f"Current toolkit version: <strong>{values.toolkit_label}</strong>"),
            (r"Toolkit version:\s*v?[0-9]+(?:\.[0-9]+)*", f"Toolkit version: {values.toolkit_label}"),
            (r"Toolkit version\s+v?[0-9]+(?:\.[0-9]+)*", f"Toolkit version {values.toolkit_label}"),
            (r"Prompt libraries:\s*v?[0-9]+(?:\.[0-9]+)*", f"Prompt libraries: {values.prompt_label}"),
            (r"Prompt libraries\s+v?[0-9]+(?:\.[0-9]+)*", f"Prompt libraries {values.prompt_label}"),
            (r"Prompt-library suite:\s*v?[0-9]+(?:\.[0-9]+)*", f"Prompt-library suite: {values.prompt_label}"),
            (r"Prompt-library suite\s+v?[0-9]+(?:\.[0-9]+)*", f"Prompt-library suite {values.prompt_label}"),
            (r"Testing pack:\s*v?[0-9]+(?:\.[0-9]+)*", f"Testing pack: {values.testing_label}"),
            (r"Testing pack\s+v?[0-9]+(?:\.[0-9]+)*", f"Testing pack {values.testing_label}"),
            (r"Site package:\s*v?[0-9]+(?:\.[0-9]+)*", f"Site package: {values.toolkit_label}"),
            (r"Site package\s+v?[0-9]+(?:\.[0-9]+)*", f"Site package {values.toolkit_label}"),
            (r"Last updated:\s*\d{4}-\d{2}-\d{2}", f"Last updated: {values.release_date}"),
        ]
        apply_subs(path, substitutions, dry_run, changed)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    config = simple_yaml_load(RELEASE_YML)
    parser = argparse.ArgumentParser(description="Prepare structured version/date stamps for a toolkit release.")
    parser.add_argument("--version", help="Set toolkit/site and prompt-library version together, for example 3.6. Does not change the testing/audit pack version unless --testing-pack-version is also supplied.")
    parser.add_argument("--toolkit-version", help="Toolkit/site package version. Defaults to src/release.yml or --version.")
    parser.add_argument("--prompt-library-version", help="Prompt-library suite version. Defaults to src/release.yml or --version.")
    parser.add_argument("--testing-pack-version", help="Testing/audit pack version. Defaults to src/release.yml and can intentionally differ from the toolkit/prompt-library version.")
    parser.add_argument("--date", default=config.get("release_date") or date.today().isoformat(), help="Release date in YYYY-MM-DD format. Defaults to src/release.yml or today.")
    parser.add_argument("--status", default=config.get("status") or "active public release", help="Release status label for generated prompt-library files.")
    parser.add_argument("--site-only", action="store_true", help="Only update public site/version stamp files, not prompt-library source files.")
    parser.add_argument("--prompt-only", action="store_true", help="Only update prompt-library source files, not public site/version stamp files.")
    parser.add_argument("--dry-run", action="store_true", help="Report files that would change without writing anything.")
    args = parser.parse_args(argv)
    args.testing_pack_version_explicit = args.testing_pack_version is not None
    if args.site_only and args.prompt_only:
        parser.error("Use at most one of --site-only or --prompt-only.")
    if args.version:
        args.toolkit_version = args.toolkit_version or args.version
        args.prompt_library_version = args.prompt_library_version or args.version
    args.toolkit_version = args.toolkit_version or config.get("toolkit_version")
    args.prompt_library_version = args.prompt_library_version or config.get("prompt_library_version")
    args.testing_pack_version = args.testing_pack_version or config.get("testing_pack_version")
    missing = [name for name in ("toolkit_version", "prompt_library_version", "testing_pack_version") if not getattr(args, name)]
    if missing:
        parser.error("Missing version value(s): " + ", ".join(missing) + ". Use --version or set src/release.yml.")
    for name in ("toolkit_version", "prompt_library_version", "testing_pack_version"):
        value = getattr(args, name)
        if not re.fullmatch(r"\d+(?:\.\d+)*", value.lstrip("v")):
            parser.error(f"{name.replace('_', '-')} should look like 3.6 or v3.6")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        parser.error("--date must be YYYY-MM-DD")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    values = ReleaseValues(
        toolkit_version=args.toolkit_version.lstrip("v"),
        prompt_library_version=args.prompt_library_version.lstrip("v"),
        testing_pack_version=args.testing_pack_version.lstrip("v"),
        release_date=args.date,
        status=args.status,
    )
    changed: list[Path] = []
    write_release_yml(values, dry_run=args.dry_run, changed=changed)
    if not args.site_only:
        update_prompt_source(values, dry_run=args.dry_run, changed=changed)
        if args.testing_pack_version_explicit:
            update_audit_source(values, dry_run=args.dry_run, changed=changed)
    if not args.prompt_only:
        update_site_stamps(values, dry_run=args.dry_run, changed=changed)

    # De-duplicate while preserving order.
    seen: set[Path] = set()
    unique = []
    for path in changed:
        if path not in seen:
            seen.add(path)
            unique.append(path)

    if args.dry_run:
        print(f"Would update {len(unique)} file(s):")
    else:
        print(f"Updated {len(unique)} file(s).")
    for path in unique:
        try:
            display = path.relative_to(ROOT).as_posix()
        except ValueError:
            display = str(path)
        print(f"  - {display}")
    if not args.dry_run:
        print("Next recommended commands:")
        print("  python scripts/build_prompt_libraries.py")
        print("  python scripts/build_audit_pack.py")
        print(f"  python scripts/build_site_package.py --run-generator-check --version {values.toolkit_version}")
        if values.testing_pack_version != values.toolkit_version:
            print(f"Note: testing/audit pack remains on its own version v{values.testing_pack_version}.")
            print("To bump audit/testing content too, rerun with --testing-pack-version <version>.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
