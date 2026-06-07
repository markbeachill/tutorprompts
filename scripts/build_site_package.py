#!/usr/bin/env python3
"""Build a clean distributable ZIP for the AI Personal Tutor Toolkit site.

Package Generator v1.3 helper

This script is separate from the prompt-library generator. It packages the public
site/repository deliverables into a ZIP while excluding local repository machinery and
source/build tooling by default.

Run from the repository root:
    python scripts/build_site_package.py

Recommended release-package build:
    python scripts/build_prompt_libraries.py --ci
    python scripts/build_site_package.py --run-generator-check
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".pytest_cache",
    "__pycache__",
    "dist",
    "src",
    "scripts",
}

DEFAULT_EXCLUDED_FILENAMES = {
    ".DS_Store",
    "Thumbs.db",
    "PACKAGE_GENERATOR_DESIGN.md",
    "PACKAGE_GENERATOR_README.md",
}

DEFAULT_EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
}

DEFAULT_EXCLUDED_PREFIXES = {
    "ai_personal_tutor_package_generator_",
}


@dataclass(frozen=True)
class PackagePlan:
    output: Path
    include_generator: bool
    explicit_version: str | None
    dry_run: bool
    check_only: bool
    run_generator_check: bool


def infer_toolkit_version() -> str:
    """Infer the visible toolkit version from the homepage, falling back to 'current'."""
    index = ROOT / "docs" / "index.html"
    candidates: list[str] = []
    if index.exists():
        raw = index.read_text(encoding="utf-8", errors="ignore")
        text = re.sub(r"<[^>]+>", " ", raw)
        text = re.sub(r"\s+", " ", text)
        # Prefer the explicit current-toolkit label on the homepage. Search patterns
        # separately so old changelog/download text cannot accidentally win.
        preferred = re.search(r"Current toolkit version:\s*v?([0-9]+(?:\.[0-9]+)*)", text, flags=re.IGNORECASE)
        if preferred:
            return "v" + preferred.group(1).lstrip("v")
        patterns = [
            r"Toolkit version\s*v?([0-9]+(?:\.[0-9]+)*)",
            r"Prompt libraries\s*v?([0-9]+(?:\.[0-9]+)*)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                candidates.append(match.group(1))
    if candidates:
        return "v" + candidates[0].lstrip("v")
    manifest = ROOT / "docs" / "release_manifest.md"
    if manifest.exists():
        text = manifest.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"(?:Current toolkit version|Prompt-library suite).*?v?([0-9]+(?:\.[0-9]+)*)", text, flags=re.IGNORECASE)
        if match:
            return "v" + match.group(1).lstrip("v")
    return "current"


def normalise_version_for_filename(version: str) -> str:
    label = version if version.lower().startswith("v") else "v" + version
    return label.replace(".", "_")


def default_output_path(explicit_version: str | None = None) -> Path:
    version = normalise_version_for_filename(explicit_version) if explicit_version else infer_toolkit_version().replace(".", "_")
    return DIST / f"ai_personal_tutor_github_pages_site_{version}.zip"


def should_exclude(path: Path, include_generator: bool) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    name = path.name

    if not include_generator:
        if any(part in DEFAULT_EXCLUDED_DIRS for part in parts):
            return True
        if name in DEFAULT_EXCLUDED_FILENAMES:
            return True
        if any(name.startswith(prefix) for prefix in DEFAULT_EXCLUDED_PREFIXES):
            return True
    else:
        # Even when including generator files, never package git metadata, caches or dist output.
        if any(part in {".git", ".pytest_cache", "__pycache__", "dist"} for part in parts):
            return True

    if name in {".DS_Store", "Thumbs.db"}:
        return True
    if path.suffix in DEFAULT_EXCLUDED_SUFFIXES:
        return True
    return False


def iter_package_files(include_generator: bool) -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if should_exclude(path, include_generator=include_generator):
            continue
        files.append(path)
    return files


def run_generator_check() -> None:
    checks = [
        ROOT / "scripts" / "build_prompt_libraries.py",
        ROOT / "scripts" / "build_audit_pack.py",
    ]
    for script in checks:
        if not script.exists():
            raise SystemExit(f"Cannot run generator check: {script.relative_to(ROOT).as_posix()} was not found.")
        result = subprocess.run([sys.executable, str(script), "--ci"], cwd=ROOT)
        if result.returncode != 0:
            raise SystemExit(result.returncode)


def write_zip(output: Path, files: Sequence[Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    # Stable timestamp for deterministic package metadata. ZIP cannot store dates before 1980.
    timestamp = (2026, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(rel, date_time=timestamp)
            # Use a regular-file mode. This keeps ZIP contents predictable across platforms.
            info.external_attr = 0o644 << 16
            data = path.read_bytes()
            zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)


def parse_args(argv: Sequence[str] | None = None) -> PackagePlan:
    parser = argparse.ArgumentParser(description="Build a clean distributable ZIP for the AI Personal Tutor Toolkit site.")
    parser.add_argument("--output", type=Path, help="Output ZIP path. Defaults to dist/ai_personal_tutor_github_pages_site_<version>.zip")
    parser.add_argument("--version", help="Version label to use in the default output filename, for example 3.6. Does not rewrite site content; use prepare_toolkit_release.py for that.")
    parser.add_argument("--include-generator", action="store_true", help="Include src/, scripts/ and package-generator docs in the ZIP. Default is a clean public site package without generator tooling.")
    parser.add_argument("--dry-run", action="store_true", help="List files that would be packaged without writing a ZIP.")
    parser.add_argument("--check", action="store_true", help="Check that the output ZIP exists and matches what would be built, without writing changes.")
    parser.add_argument("--run-generator-check", action="store_true", help="Run prompt-library and audit/testing generator CI checks before packaging.")
    args = parser.parse_args(argv)

    output = args.output if args.output else default_output_path(args.version)
    if not output.is_absolute():
        output = ROOT / output
    if output.suffix.lower() != ".zip":
        parser.error("--output must end with .zip")
    return PackagePlan(output=output, include_generator=args.include_generator, explicit_version=args.version, dry_run=args.dry_run, check_only=args.check, run_generator_check=args.run_generator_check)


def main(argv: Sequence[str] | None = None) -> int:
    plan = parse_args(argv)
    if plan.run_generator_check:
        run_generator_check()

    files = iter_package_files(include_generator=plan.include_generator)
    if not files:
        print("No files selected for packaging.", file=sys.stderr)
        return 1

    if plan.dry_run:
        print(f"Would package {len(files)} files into {plan.output.relative_to(ROOT) if plan.output.is_relative_to(ROOT) else plan.output}:")
        for path in files:
            print(f"  - {path.relative_to(ROOT).as_posix()}")
        return 0

    if plan.check_only:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_zip = Path(tmp) / plan.output.name
            write_zip(tmp_zip, files)
            if not plan.output.exists():
                print(f"Package is missing: {plan.output}", file=sys.stderr)
                return 1
            if tmp_zip.read_bytes() != plan.output.read_bytes():
                print(f"Package is out of date: {plan.output}", file=sys.stderr)
                print("Run: python scripts/build_site_package.py", file=sys.stderr)
                return 1
        print(f"Site package is up to date: {plan.output}")
        return 0

    write_zip(plan.output, files)
    display = plan.output.relative_to(ROOT) if plan.output.is_relative_to(ROOT) else plan.output
    print(f"Created site package: {display}")
    print(f"Files included: {len(files)}")
    if not plan.include_generator:
        print("Generator/source tooling excluded by default. Use --include-generator to include it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
