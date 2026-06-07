#!/usr/bin/env python3
"""Print a compact health report for the AI Personal Tutor package generator.

Package Generator v2.7 helper.

This script is deliberately read-only. It checks whether the repository has the
expected generator/source files, release metadata, core pack definitions, generated
prompt-library outputs, downloadable ZIPs and GitHub workflow files.

Typical use from the repository root:
    python scripts/generator_health_report.py

Use --fail-on-problems for CI-style use.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_CORE_PACKS = [
    "master",
    "writing-tutor",
    "structure-tutor",
    "academic-thinking",
    "research-proposal",
    "study-workflow",
]

EXPECTED_WORKFLOWS = [
    ".github/workflows/prompt-library-generator-check.yml",
    ".github/workflows/build-site-package.yml",
    ".github/workflows/build-toolkit-release.yml",
]

EXPECTED_SCRIPTS = [
    "scripts/build_prompt_libraries.py",
    "scripts/build_site_package.py",
    "scripts/prepare_toolkit_release.py",
    "scripts/build_toolkit_release.py",
    "scripts/build_site_data.py",
    "scripts/build_audit_pack.py",
    "scripts/generator_health_report.py",
    "scripts/release_consistency_check.py",
    "scripts/run_generator_checks.py",
    "scripts/sync_release_metadata.py",
    "scripts/clean_generator_artifacts.py",
]

EXPECTED_DOCS = [
    "PACKAGE_GENERATOR_README.md",
    "PACKAGE_GENERATOR_DESIGN.md",
    "PACKAGE_GENERATOR_START_HERE.md",
]


EXPECTED_SITE_DATA_FILES = [
    "docs/data/release.json",
    "docs/data/tool_index.json",
    "docs/data/prompt_library_packs.json",
]

EXPECTED_AUDIT_FILES = [
    "docs/audit-library/latest/ai_tutor_toolkit_audit_prompt_with_menu.md",
    "docs/audit-library/latest/ai_tutor_toolkit_step_by_step_test_cards.md",
    "docs/audit-library/latest/ai_tutor_toolkit_test_log_template.md",
    "docs/audit-library/latest/ai_tutor_toolkit_testing_guide_for_educators.md",
    "docs/audit-library/latest/ai_tutor_toolkit_universal_test_cards.md",
    "docs/audit-library/latest/ai_personal_tutor_testing_pack.zip",
]

EXPECTED_AUDIT_ZIP_MEMBERS = [
    "ai_tutor_toolkit_audit_prompt_with_menu.md",
    "ai_tutor_toolkit_step_by_step_test_cards.md",
    "ai_tutor_toolkit_test_log_template.md",
    "ai_tutor_toolkit_testing_guide_for_educators.md",
    "ai_tutor_toolkit_universal_test_cards.md",
]

EXPECTED_LATEST_FILES = [
    "docs/prompt-libraries/latest/ai_personal_tutor_master_library.md",
    "docs/prompt-libraries/latest/01_writing_tutor_library.md",
    "docs/prompt-libraries/latest/02_structure_tutor_library.md",
    "docs/prompt-libraries/latest/03_academic_thinking_tutor_library.md",
    "docs/prompt-libraries/latest/04_research_proposal_tutor_library.md",
    "docs/prompt-libraries/latest/05_study_workflow_tutor_library.md",
    "docs/prompt-libraries/latest/ai_personal_tutor_mini_libraries.zip",
]

EXPECTED_MINI_ZIP_MEMBERS = [
    "01_writing_tutor_library.md",
    "02_structure_tutor_library.md",
    "03_academic_thinking_tutor_library.md",
    "04_research_proposal_tutor_library.md",
    "05_study_workflow_tutor_library.md",
]


@dataclass
class Check:
    name: str
    status: str
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "ok"


@dataclass
class HealthReport:
    toolkit_version: str | None
    prompt_library_version: str | None
    testing_pack_version: str | None
    release_date: str | None
    tool_count: int | None
    core_pack_count: int
    custom_pack_count: int
    checks: list[Check]

    @property
    def ok(self) -> bool:
        return all(check.ok for check in self.checks)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def simple_yaml_load(path: Path) -> dict[str, Any]:
    """Load the simple key/value YAML style used by release.yml.

    This is not a general YAML parser, but it is enough for src/release.yml and keeps
    the generator dependency-free.
    """
    data: dict[str, Any] = {}
    if not path.exists():
        return data
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        if line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def path_check(path: str, label: str | None = None) -> Check:
    p = ROOT / path
    return Check(label or path, "ok" if p.exists() else "problem", "found" if p.exists() else f"missing: {path}")


def check_expected_paths(paths: list[str], label: str) -> Check:
    missing = [path for path in paths if not (ROOT / path).exists()]
    if missing:
        return Check(label, "problem", "missing: " + ", ".join(missing))
    return Check(label, "ok", f"{len(paths)} expected files found")


def count_custom_packs() -> int:
    folder = ROOT / "src" / "prompt-library" / "custom-packs"
    if not folder.exists():
        return 0
    return len(sorted(folder.glob("*.yml"))) + len(sorted(folder.glob("*.yaml")))


def core_pack_files() -> list[Path]:
    folder = ROOT / "src" / "prompt-library" / "packs"
    if not folder.exists():
        return []
    return sorted(folder.glob("*.yml")) + sorted(folder.glob("*.yaml"))


def check_core_packs() -> Check:
    folder = ROOT / "src" / "prompt-library" / "packs"
    if not folder.exists():
        return Check("core pack manifests", "problem", "missing: src/prompt-library/packs/")
    missing = [pack for pack in EXPECTED_CORE_PACKS if not (folder / f"{pack}.yml").exists()]
    if missing:
        return Check("core pack manifests", "problem", "missing: " + ", ".join(missing))
    return Check("core pack manifests", "ok", f"{len(EXPECTED_CORE_PACKS)} expected core packs found")


def check_tool_metadata() -> tuple[Check, int | None]:
    path = ROOT / "src" / "prompt-library" / "tool-metadata.json"
    data = load_json(path)
    if data is None:
        return Check("tool metadata", "problem", "missing or invalid JSON: src/prompt-library/tool-metadata.json"), None
    tools = data.get("tools") if isinstance(data, dict) else None
    if not isinstance(tools, list):
        return Check("tool metadata", "problem", "tool-metadata.json does not contain a tools list"), None
    codes = [tool.get("code") for tool in tools if isinstance(tool, dict)]
    duplicate_codes = sorted({code for code in codes if code and codes.count(code) > 1})
    if duplicate_codes:
        return Check("tool metadata", "problem", "duplicate tool codes: " + ", ".join(duplicate_codes)), len(tools)
    return Check("tool metadata", "ok", f"{len(tools)} tools listed"), len(tools)



def _version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split(".") if part.isdigit())


def _find_first(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else None


def check_prompt_generated_versions(release: dict[str, Any]) -> Check:
    """Check that current prompt-library outputs match src/release.yml.

    This is intentionally a lightweight health-report check. It does not rebuild
    files. It catches the common mixed-version state where generated Markdown files
    were prepared for a newer prompt-library release but src/release.yml still points
    at the previous version.
    """
    toolkit_version = release.get("toolkit_version")
    prompt_version = release.get("prompt_library_version")
    testing_version = release.get("testing_pack_version")
    if not toolkit_version or not prompt_version or not testing_version:
        return Check("prompt-library generated version stamps", "problem", "src/release.yml is missing toolkit_version, prompt_library_version or testing_pack_version")

    problems: list[str] = []
    versions_seen: set[str] = set()
    for rel_path in EXPECTED_LATEST_FILES:
        if not rel_path.endswith(".md"):
            continue
        path = ROOT / rel_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        label = Path(rel_path).name

        manifest_version = _find_first(r"^version:\s*v?([0-9]+(?:\.[0-9]+)+)\s*$", text)
        visible_version = _find_first(r"^\*\*Version:\*\*\s*v?([0-9]+(?:\.[0-9]+)+)\s*$", text)
        this_file_version = _find_first(r"\*\*This file:\*\*[^\n]*?\bv([0-9]+(?:\.[0-9]+)+)", text)
        archive_version = _find_first(r"\*\*Fixed archive:\*\*\s*`prompt-libraries/v([0-9]+(?:\.[0-9]+)+)/", text)

        for value in [manifest_version, visible_version, this_file_version, archive_version]:
            if value:
                versions_seen.add(value)

        for field_name, value in [
            ("front-matter version", manifest_version),
            ("visible Version line", visible_version),
            ("This file stamp", this_file_version),
            ("Fixed archive path", archive_version),
        ]:
            if value and value != prompt_version:
                problems.append(f"{label}: {field_name} is {value}, expected {prompt_version}")
            elif value is None:
                problems.append(f"{label}: missing {field_name}")

        stamp_match = re.search(
            r"\*\*Release stamp:\*\*\s*Toolkit version v([0-9]+(?:\.[0-9]+)+)\s*/\s*Prompt-library suite v([0-9]+(?:\.[0-9]+)+)\s*/\s*Testing pack v([0-9]+(?:\.[0-9]+)+)",
            text,
        )
        if stamp_match:
            stamp_toolkit, stamp_prompt, stamp_testing = stamp_match.groups()
            versions_seen.update([stamp_toolkit, stamp_prompt, stamp_testing])
            if stamp_toolkit != toolkit_version:
                problems.append(f"{label}: release-stamp toolkit version is {stamp_toolkit}, expected {toolkit_version}")
            if stamp_prompt != prompt_version:
                problems.append(f"{label}: release-stamp prompt-library version is {stamp_prompt}, expected {prompt_version}")
            if stamp_testing != testing_version:
                problems.append(f"{label}: release-stamp testing-pack version is {stamp_testing}, expected {testing_version}")
        else:
            problems.append(f"{label}: missing Release stamp")

    if problems:
        preview = "; ".join(problems[:3])
        if len(problems) > 3:
            preview += f"; plus {len(problems) - 3} more"
        seen = ", ".join(sorted(versions_seen, key=_version_tuple)) if versions_seen else "none"
        return Check(
            "prompt-library generated version stamps",
            "problem",
            f"expected toolkit={toolkit_version}, prompt-library={prompt_version}, testing-pack={testing_version}; seen prompt-library file stamp version(s): {seen}; {preview}",
        )

    return Check(
        "prompt-library generated version stamps",
        "ok",
        f"match src/release.yml: toolkit v{toolkit_version}, prompt-library v{prompt_version}, testing-pack v{testing_version}",
    )


def check_mini_zip() -> Check:
    path = ROOT / "docs" / "prompt-libraries" / "latest" / "ai_personal_tutor_mini_libraries.zip"
    if not path.exists():
        return Check("mini-library ZIP", "problem", "missing current mini-library ZIP")
    try:
        with zipfile.ZipFile(path, "r") as zf:
            names = sorted([name for name in zf.namelist() if not name.endswith("/")])
    except zipfile.BadZipFile:
        return Check("mini-library ZIP", "problem", "not a valid ZIP")
    expected = sorted(EXPECTED_MINI_ZIP_MEMBERS)
    if names != expected:
        return Check("mini-library ZIP", "problem", f"expected {len(expected)} members, found {len(names)}: {', '.join(names)}")
    return Check("mini-library ZIP", "ok", "contains the expected five mini-library files")


def check_audit_zip() -> Check:
    path = ROOT / "docs" / "audit-library" / "latest" / "ai_personal_tutor_testing_pack.zip"
    if not path.exists():
        return Check("testing-pack ZIP", "problem", "missing current testing-pack ZIP")
    try:
        with zipfile.ZipFile(path, "r") as zf:
            names = sorted([name for name in zf.namelist() if not name.endswith("/")])
    except zipfile.BadZipFile:
        return Check("testing-pack ZIP", "problem", "not a valid ZIP")
    expected = sorted(EXPECTED_AUDIT_ZIP_MEMBERS)
    if names != expected:
        return Check("testing-pack ZIP", "problem", f"expected {len(expected)} members, found {len(names)}: {', '.join(names)}")
    return Check("testing-pack ZIP", "ok", "contains the expected testing-pack files")


def git_summary() -> Check:
    if not (ROOT / ".git").exists():
        return Check("git working tree", "ok", "not a Git checkout or .git not present; skipped")
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True, check=False)
    except OSError:
        return Check("git working tree", "ok", "git command unavailable; skipped")
    if result.returncode != 0:
        return Check("git working tree", "ok", "git status unavailable; skipped")
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        return Check("git working tree", "ok", "clean")
    return Check("git working tree", "ok", f"{len(lines)} changed/untracked path(s); review with git status")


def build_report() -> HealthReport:
    release = simple_yaml_load(ROOT / "src" / "release.yml")
    checks: list[Check] = []
    checks.append(check_expected_paths(EXPECTED_SCRIPTS, "generator scripts"))
    checks.append(check_expected_paths(EXPECTED_DOCS, "generator documentation"))
    checks.append(check_expected_paths(EXPECTED_WORKFLOWS, "GitHub workflows"))
    checks.append(path_check("src/release.yml", "release metadata"))
    checks.append(path_check("src/prompt-library/header.md", "prompt-library header source"))
    checks.append(path_check("src/prompt-library/shared/01-global-rules.md", "global rules source"))
    checks.append(path_check("src/prompt-library/shared/02-markdown-output-rules.md", "Markdown rules source"))
    checks.append(path_check("src/audit-library/audit-pack.yml", "audit/testing manifest source"))
    checks.append(check_expected_paths(["src/audit-library/files/" + p.split("/")[-1] for p in EXPECTED_AUDIT_FILES if p.endswith(".md")], "audit/testing source files"))
    checks.append(check_core_packs())
    metadata_check, tool_count = check_tool_metadata()
    checks.append(metadata_check)
    checks.append(check_expected_paths(EXPECTED_LATEST_FILES, "current generated prompt-library outputs"))
    checks.append(check_prompt_generated_versions(release))
    checks.append(check_expected_paths(EXPECTED_AUDIT_FILES, "current generated audit/testing outputs"))
    checks.append(check_expected_paths(EXPECTED_SITE_DATA_FILES, "generated site integration data"))
    checks.append(check_mini_zip())
    checks.append(check_audit_zip())
    checks.append(git_summary())

    return HealthReport(
        toolkit_version=release.get("toolkit_version"),
        prompt_library_version=release.get("prompt_library_version"),
        testing_pack_version=release.get("testing_pack_version"),
        release_date=release.get("release_date"),
        tool_count=tool_count,
        core_pack_count=len(core_pack_files()),
        custom_pack_count=count_custom_packs(),
        checks=checks,
    )


def print_text(report: HealthReport, *, show_recommendations: bool = True) -> None:
    print("AI Personal Tutor package generator health report")
    print("=" * 54)
    print(f"Repository root: {ROOT}")
    print(f"Toolkit version: {report.toolkit_version or 'unknown'}")
    print(f"Prompt-library version: {report.prompt_library_version or 'unknown'}")
    print(f"Testing-pack version: {report.testing_pack_version or 'unknown'}")
    print(f"Release date: {report.release_date or 'unknown'}")
    print(f"Tool metadata count: {report.tool_count if report.tool_count is not None else 'unknown'}")
    print(f"Core pack manifests: {report.core_pack_count}")
    print(f"Custom pack manifests: {report.custom_pack_count}")
    print()
    for check in report.checks:
        marker = "OK" if check.ok else "PROBLEM"
        print(f"[{marker}] {check.name}: {check.detail}")
    print()
    if report.ok:
        print("Health result: OK")
        if show_recommendations:
            print("Recommended standard checks:")
            print()
            print("Windows PowerShell / command prompt:")
            print("  python scripts\\run_generator_checks.py")
            print()
            print("macOS/Linux shell:")
            print("  python scripts/run_generator_checks.py")
    else:
        print("Health result: PROBLEMS FOUND")
        if show_recommendations:
            prompt_version_problem = any(
                (not check.ok) and check.name == "prompt-library generated version stamps"
                for check in report.checks
            )
            if prompt_version_problem:
                print("If the problem is a prompt-library version mismatch and you want to keep")
                print("the newer generated prompt-library version, run:")
                print("  python scripts\\run_generator_checks.py --sync-release-metadata")
                print()
                print("Equivalent direct recovery command:")
                print("  python scripts\\sync_release_metadata.py --to-generated --build --check")
                print()
            print("Otherwise, fix the problem lines above, then run the standard checks:")
            print("  python scripts\\run_generator_checks.py")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a read-only health report for the package generator.")
    parser.add_argument("--json", action="store_true", help="Print the report as JSON.")
    parser.add_argument("--fail-on-problems", action="store_true", help="Exit with status 1 if required files/checks are missing or invalid.")
    parser.add_argument("--no-recommendations", action="store_true", help="Suppress follow-up command suggestions. Useful when called by run_generator_checks.py.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report()
    if args.json:
        payload = asdict(report)
        payload["ok"] = report.ok
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text(report, show_recommendations=not args.no_recommendations)
    if args.fail_on_problems and not report.ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
