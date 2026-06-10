#!/usr/bin/env python3
"""Check release/version consistency across generated toolkit outputs.

Package Generator v1.3 helper.

This script is read-only. It checks that the repository's structured release
metadata, generated prompt-library files, fixed archive copies, mini-library ZIP
and visible current-version labels agree with one another.

Typical use from the repository root:
    python scripts/release_consistency_check.py

For CI use:
    python scripts/release_consistency_check.py --fail-on-problems
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
RELEASE_YML = ROOT / "src" / "release.yml"
PACK_DIR = ROOT / "src" / "prompt-library" / "packs"
MINI_ZIP = ROOT / "docs" / "prompt-libraries" / "latest" / "ai_personal_tutor_mini_libraries.zip"
AUDIT_ZIP = ROOT / "docs" / "audit-library" / "latest" / "ai_personal_tutor_testing_pack.zip"

EXPECTED_MINI_MEMBERS = {
    "01_writing_tutor_library.md",
    "02_structure_tutor_library.md",
    "03_academic_thinking_tutor_library.md",
    "04_research_proposal_tutor_library.md",
    "05_study_workflow_tutor_library.md",
}

EXPECTED_AUDIT_MEMBERS = {
    "ai_tutor_toolkit_audit_prompt_with_menu.md",
    "ai_tutor_toolkit_output_collector.md",
    "ai_tutor_toolkit_step_by_step_test_cards.md",
    "ai_tutor_toolkit_test_log_template.md",
    "ai_tutor_toolkit_testing_guide_for_educators.md",
    "ai_tutor_toolkit_universal_test_cards.md",
}

CURRENT_LABEL_FILES = [
    "docs/index.html",
    "docs/tools/index.html",
    "README.md",
]


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def read_simple_yaml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list: str | None = None
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            current_list = stripped[:-1]
            data[current_list] = []
            continue
        if current_list and line.startswith("  - "):
            value = _unquote(line[4:])
            assert isinstance(data[current_list], list)
            data[current_list].append(value)
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = _unquote(value)
            current_list = None
            continue
    return data


def release_metadata() -> dict[str, str]:
    raw = read_simple_yaml(RELEASE_YML)
    return {str(k): str(v) for k, v in raw.items() if not isinstance(v, list)}


def norm_version(value: str | None) -> str | None:
    if not value:
        return None
    return str(value).strip().lstrip("v")


def version_sort_key(value: str) -> list[int]:
    return [int(part) for part in value.split(".") if part.isdigit()]


def extract_current_version_tokens(text: str) -> set[str]:
    """Extract version tokens from current-release/version-stamp contexts.

    This deliberately avoids generic changelog/history matching; it is for current
    generated outputs and current-version labels, not historical release notes.
    """
    patterns = [
        r"^version:\s*v?([0-9]+(?:\.[0-9]+)*)\s*$",
        r"^\*\*Version:\*\*\s*v?([0-9]+(?:\.[0-9]+)*)\s*$",
        r"\*\*This file:\*\*.*?\bv?([0-9]+(?:\.[0-9]+)*)\b",
        r"Toolkit version\s+v?([0-9]+(?:\.[0-9]+)*)",
        r"Prompt-library suite\s+v?([0-9]+(?:\.[0-9]+)*)",
        r"Testing pack\s+v?([0-9]+(?:\.[0-9]+)*)",
        r"Current toolkit version:\s*v?([0-9]+(?:\.[0-9]+)*)",
        r"Toolkit version\s*v?([0-9]+(?:\.[0-9]+)*)",
        r"prompt-libraries/v([0-9]+(?:\.[0-9]+)*)/",
        r"prompt-libraries_v([0-9]+(?:_[0-9]+)*)",
    ]
    tokens: set[str] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            tokens.add(match.group(1).replace("_", ".").lstrip("v"))
    return tokens


def core_pack_specs() -> list[dict[str, object]]:
    if not PACK_DIR.exists():
        return []
    specs: list[dict[str, object]] = []
    for path in sorted(list(PACK_DIR.glob("*.yml")) + list(PACK_DIR.glob("*.yaml"))):
        spec = read_simple_yaml(path)
        spec["_path"] = path
        specs.append(spec)
    return specs


def expected_pack_paths(version: str) -> list[tuple[Path, Path, dict[str, object]]]:
    paths: list[tuple[Path, Path, dict[str, object]]] = []
    version_us = version.replace(".", "_")
    for spec in core_pack_specs():
        latest = spec.get("latest_output")
        archive = spec.get("archive_output")
        if not isinstance(latest, str) or not isinstance(archive, str):
            continue
        # The pack manifests should already be prepared for the current version. Do
        # not silently rewrite them here; use this expected path for validation only.
        expected_archive = re.sub(r"prompt-libraries/v[0-9]+(?:\.[0-9]+)*/", f"prompt-libraries/v{version}/", archive)
        expected_archive = re.sub(r"_v[0-9]+(?:_[0-9]+)*\.md$", f"_v{version_us}.md", expected_archive)
        paths.append((ROOT / latest, ROOT / expected_archive, spec))
    return paths


def check_release_yml() -> tuple[list[Check], dict[str, str] | None]:
    checks: list[Check] = []
    release = release_metadata()
    if not RELEASE_YML.exists():
        return [Check("src/release.yml", False, "missing")], None
    required = ["toolkit_version", "prompt_library_version", "testing_pack_version", "release_date"]
    missing = [key for key in required if not release.get(key)]
    if missing:
        checks.append(Check("src/release.yml", False, "missing keys: " + ", ".join(missing)))
        return checks, None
    versions = {
        "toolkit_version": norm_version(release.get("toolkit_version")) or "",
        "prompt_library_version": norm_version(release.get("prompt_library_version")) or "",
        "testing_pack_version": norm_version(release.get("testing_pack_version")) or "",
        "release_date": str(release.get("release_date") or ""),
    }
    invalid = [f"{key}={value!r}" for key, value in versions.items() if key.endswith("_version") and not re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", value)]
    if invalid:
        checks.append(Check("src/release.yml version format", False, "invalid value(s): " + ", ".join(invalid)))
        return checks, versions
    if versions["testing_pack_version"] != versions["toolkit_version"]:
        detail = (
            f"toolkit v{versions['toolkit_version']}, prompt libraries v{versions['prompt_library_version']}, "
            f"testing/audit pack v{versions['testing_pack_version']} (audit pack has its own version)"
        )
    else:
        detail = f"toolkit/prompt/testing v{versions['toolkit_version']}, date {versions['release_date']}"
    checks.append(Check("src/release.yml", True, detail))
    return checks, versions


def check_pack_manifests(version: str) -> list[Check]:
    checks: list[Check] = []
    specs = core_pack_specs()
    if not specs:
        return [Check("core pack manifests", False, "no pack manifests found")]
    problems: list[str] = []
    version_us = version.replace(".", "_")
    for spec in specs:
        path = spec.get("_path")
        archive = str(spec.get("archive_output", ""))
        if f"prompt-libraries/v{version}/" not in archive or not archive.endswith(f"_v{version_us}.md"):
            problems.append(f"{rel(path) if isinstance(path, Path) else path}: archive_output is {archive!r}")
    if problems:
        checks.append(Check("core pack archive_output values", False, "; ".join(problems[:6])))
    else:
        checks.append(Check("core pack archive_output values", True, f"{len(specs)} pack manifest(s) use v{version}"))
    return checks


def check_generated_prompt_files(version: str, allowed_extra_versions: set[str] | None = None) -> list[Check]:
    checks: list[Check] = []
    pairs = expected_pack_paths(version)
    missing_latest = [rel(latest) for latest, _archive, _spec in pairs if not latest.exists()]
    missing_archive = [rel(archive) for _latest, archive, _spec in pairs if not archive.exists()]
    if missing_latest:
        checks.append(Check("latest prompt-library files", False, "missing: " + ", ".join(missing_latest)))
    else:
        checks.append(Check("latest prompt-library files", True, f"{len(pairs)} latest file(s) found"))
    if missing_archive:
        checks.append(Check("fixed archive prompt-library files", False, "missing: " + ", ".join(missing_archive)))
    else:
        checks.append(Check("fixed archive prompt-library files", True, f"{len(pairs)} archive file(s) found for v{version}"))

    token_problems: list[str] = []
    archive_mismatch: list[str] = []
    allowed_versions = {version} | (allowed_extra_versions or set())
    for latest, archive, _spec in pairs:
        if latest.exists():
            tokens = extract_current_version_tokens(latest.read_text(encoding="utf-8", errors="ignore"))
            if version not in tokens or not tokens.issubset(allowed_versions):
                token_problems.append(f"{rel(latest)} has version token(s): {', '.join(sorted(tokens, key=version_sort_key)) or 'none'}")
        if latest.exists() and archive.exists() and latest.read_bytes() != archive.read_bytes():
            archive_mismatch.append(f"{rel(latest)} != {rel(archive)}")
    if token_problems:
        checks.append(Check("generated prompt-library version stamps", False, "; ".join(token_problems[:6])))
    else:
        checks.append(Check("generated prompt-library version stamps", True, f"latest prompt-library files consistently use v{version}"))
    if archive_mismatch:
        checks.append(Check("latest/archive prompt-library parity", False, "; ".join(archive_mismatch[:6])))
    elif not missing_latest and not missing_archive:
        checks.append(Check("latest/archive prompt-library parity", True, "archive copies match latest files"))
    return checks


def check_mini_zip() -> list[Check]:
    checks: list[Check] = []
    if not MINI_ZIP.exists():
        return [Check("mini-library ZIP", False, "missing: " + rel(MINI_ZIP))]
    try:
        with zipfile.ZipFile(MINI_ZIP, "r") as zf:
            names = {name for name in zf.namelist() if not name.endswith("/")}
            if names != EXPECTED_MINI_MEMBERS:
                checks.append(Check("mini-library ZIP members", False, "found: " + ", ".join(sorted(names))))
                return checks
            mismatches: list[str] = []
            for name in sorted(EXPECTED_MINI_MEMBERS):
                latest = ROOT / "docs" / "prompt-libraries" / "latest" / name
                if not latest.exists():
                    mismatches.append(f"{name}: latest file missing")
                    continue
                if zf.read(name) != latest.read_bytes():
                    mismatches.append(f"{name}: ZIP copy differs from latest file")
    except zipfile.BadZipFile:
        return [Check("mini-library ZIP", False, "not a valid ZIP")]
    if mismatches:
        checks.append(Check("mini-library ZIP parity", False, "; ".join(mismatches)))
    else:
        checks.append(Check("mini-library ZIP parity", True, "ZIP contains the expected five files and matches latest/"))
    return checks


def check_audit_pack(version: str) -> list[Check]:
    checks: list[Check] = []
    latest_dir = ROOT / "docs" / "audit-library" / "latest"
    archive_dir = ROOT / "docs" / "audit-library" / f"v{version}"
    version_us = version.replace(".", "_")
    missing_latest = [name for name in EXPECTED_AUDIT_MEMBERS if not (latest_dir / name).exists()]
    missing_archive = []
    for name in EXPECTED_AUDIT_MEMBERS:
        stem = name[:-3] if name.endswith(".md") else name
        archive_name = f"{stem}_v{version_us}.md"
        if not (archive_dir / archive_name).exists():
            missing_archive.append(archive_name)
    if missing_latest:
        checks.append(Check("latest audit/testing files", False, "missing: " + ", ".join(sorted(missing_latest))))
    else:
        checks.append(Check("latest audit/testing files", True, f"{len(EXPECTED_AUDIT_MEMBERS)} latest file(s) found"))
    if missing_archive:
        checks.append(Check("fixed archive audit/testing files", False, "missing: " + ", ".join(sorted(missing_archive))))
    else:
        checks.append(Check("fixed archive audit/testing files", True, f"{len(EXPECTED_AUDIT_MEMBERS)} archive file(s) found for v{version}"))

    parity: list[str] = []
    token_problems: list[str] = []
    for name in EXPECTED_AUDIT_MEMBERS:
        latest = latest_dir / name
        archive = archive_dir / f"{(name[:-3] if name.endswith('.md') else name)}_v{version_us}.md"
        if latest.exists():
            tokens = extract_current_version_tokens(latest.read_text(encoding="utf-8", errors="ignore"))
            if tokens and version not in tokens:
                token_problems.append(f"{rel(latest)} has current token(s): {', '.join(sorted(tokens, key=version_sort_key))}")
        if latest.exists() and archive.exists() and latest.read_bytes() != archive.read_bytes():
            parity.append(f"{rel(latest)} != {rel(archive)}")
    if token_problems:
        checks.append(Check("audit/testing version stamps", False, "; ".join(token_problems[:6])))
    else:
        checks.append(Check("audit/testing version stamps", True, f"latest audit/testing files agree with v{version} where stamped"))
    if parity:
        checks.append(Check("latest/archive audit/testing parity", False, "; ".join(parity[:6])))
    elif not missing_latest and not missing_archive:
        checks.append(Check("latest/archive audit/testing parity", True, "archive copies match latest files"))

    if not AUDIT_ZIP.exists():
        checks.append(Check("testing-pack ZIP", False, "missing: " + rel(AUDIT_ZIP)))
        return checks
    try:
        with zipfile.ZipFile(AUDIT_ZIP, "r") as zf:
            names = {name for name in zf.namelist() if not name.endswith("/")}
            if names != EXPECTED_AUDIT_MEMBERS:
                checks.append(Check("testing-pack ZIP members", False, "found: " + ", ".join(sorted(names))))
                return checks
            mismatches: list[str] = []
            for name in sorted(EXPECTED_AUDIT_MEMBERS):
                latest = latest_dir / name
                if latest.exists() and zf.read(name) != latest.read_bytes():
                    mismatches.append(f"{name}: ZIP copy differs from latest file")
    except zipfile.BadZipFile:
        checks.append(Check("testing-pack ZIP", False, "not a valid ZIP"))
        return checks
    if mismatches:
        checks.append(Check("testing-pack ZIP parity", False, "; ".join(mismatches)))
    else:
        checks.append(Check("testing-pack ZIP parity", True, "ZIP contains the expected files and matches latest/"))
    return checks


def check_current_site_labels(version: str) -> list[Check]:
    checks: list[Check] = []
    problems: list[str] = []
    checked = 0
    for rel_path in CURRENT_LABEL_FILES:
        path = ROOT / rel_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        tokens = extract_current_version_tokens(text)
        # README and release_manifest may mention package-generator versions or historical
        # notes. Only flag if a current-version token was detected and it differs.
        if tokens:
            checked += 1
            if version not in tokens:
                problems.append(f"{rel_path}: current label tokens are {', '.join(sorted(tokens, key=version_sort_key))}")
    if problems:
        checks.append(Check("current site/repo version labels", False, "; ".join(problems)))
    else:
        checks.append(Check("current site/repo version labels", True, f"{checked} current label file(s) agree with v{version} where detected"))
    return checks


def build_checks() -> list[Check]:
    checks, versions = check_release_yml()
    if not versions:
        return checks
    toolkit_version = versions["toolkit_version"]
    prompt_version = versions["prompt_library_version"]
    testing_version = versions["testing_pack_version"]
    checks.extend(check_pack_manifests(prompt_version))
    checks.extend(check_generated_prompt_files(prompt_version, allowed_extra_versions={testing_version, toolkit_version}))
    checks.extend(check_mini_zip())
    checks.extend(check_audit_pack(testing_version))
    checks.extend(check_current_site_labels(toolkit_version))
    return checks


def print_report(checks: Sequence[Check]) -> None:
    print("AI Personal Tutor release consistency check")
    print("=" * 50)
    for check in checks:
        marker = "OK" if check.ok else "PROBLEM"
        print(f"[{marker}] {check.name}: {check.detail}")
    print()
    if all(check.ok for check in checks):
        print("Release consistency result: OK")
    else:
        print("Release consistency result: PROBLEMS FOUND")
        print("Common fixes:")
        print("  python scripts\\prepare_toolkit_release.py --version <version> --date <YYYY-MM-DD>")
        print("  python scripts\\build_prompt_libraries.py")
        print("  python scripts\\build_prompt_libraries.py --ci")
        print("  python scripts\\release_consistency_check.py --fail-on-problems")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check release/version consistency across generated toolkit outputs.")
    parser.add_argument("--fail-on-problems", action="store_true", help="Exit with status 1 if any consistency check fails.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    checks = build_checks()
    print_report(checks)
    if args.fail_on_problems and not all(check.ok for check in checks):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
