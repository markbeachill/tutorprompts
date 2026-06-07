#!/usr/bin/env python3
"""Run the standard Package Generator checks in a Windows-friendly sequence.

This is a convenience wrapper. It does not replace the individual scripts; it runs
those scripts in the recommended order and stops at the first failure.

Package Generator v2.7 includes a concise prompt-library version-state diagnostic and an optional
--sync-release-metadata recovery mode. If prompt-library generated files have been
prepared for a different version than src/release.yml, this wrapper can either stop
with a short explanation or run sync_release_metadata.py before the checks.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _print_concise_prompt_version_failure(output: str) -> bool:
    """Print a concise version diagnostic if build_prompt_libraries.py reported one.

    Returns True if the output was recognised and summarised.
    """
    if "Version diagnostic:" not in output:
        return False

    current_versions = "unknown"
    rebuilt_versions = "unknown"
    release_line = "unknown"
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("- src/release.yml:"):
            release_line = stripped.removeprefix("- src/release.yml:").strip()
        elif stripped.startswith("- current generated files contain version(s):"):
            current_versions = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- rebuilding from source would produce version(s):"):
            rebuilt_versions = stripped.split(":", 1)[1].strip()

    likely_version = None
    # Prefer the highest looking version in the generated files if it differs from rebuilt.
    found = re.findall(r"\d+(?:\.\d+)+", current_versions)
    if found:
        def key(v: str) -> tuple[int, ...]:
            return tuple(int(part) for part in v.split("."))
        likely_version = sorted(found, key=key)[-1]

    print("Generated prompt-library files are out of date.")
    print()
    print("Concise version diagnostic:")
    print(f"  src/release.yml: {release_line}")
    print(f"  Current generated prompt-library files contain version(s): {current_versions}")
    print(f"  Rebuilding from source would produce version(s): {rebuilt_versions}")
    print()
    print("This usually means the generated files have been prepared for a newer")
    print("toolkit/prompt-library version, but src/release.yml has not been updated")
    print("to match, or vice versa.")
    print()
    if likely_version:
        print("Likely fix if you intend to keep the newer generated version:")
        print("  python scripts\\run_generator_checks.py --sync-release-metadata")
        print()
        print("Equivalent direct recovery command:")
        print("  python scripts\\sync_release_metadata.py --to-generated --build --check")
        print()
        print("Equivalent manual commands:")
        print(f"  python scripts\\prepare_toolkit_release.py --version {likely_version} --date <YYYY-MM-DD>")
        print("  python scripts\\build_prompt_libraries.py")
        print("  python scripts\\build_site_data.py")
        print("  python scripts\\run_generator_checks.py")
        print()
    print("Alternative if you intend to keep the version in src/release.yml:")
    print("  python scripts\\build_prompt_libraries.py")
    print("  python scripts\\run_generator_checks.py")
    print()
    print("For the full raw diff, run:")
    print("  python scripts\\build_prompt_libraries.py --ci")
    return True


def run_step(label: str, args: list[str], *, dry_run: bool = False) -> int:
    cmd = [sys.executable, *args]
    print(f"\n== {label} ==")
    print(" ".join(str(part) for part in cmd))
    if dry_run:
        return 0

    # Capture prompt-library CI output so version-mismatch failures do not dump pages
    # of diff in the standard all-checks command.
    capture_prompt_ci = label == "Prompt-library CI" and "--ci" in args
    if capture_prompt_ci:
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        output = (result.stdout or "") + (result.stderr or "")
        if result.returncode == 0:
            if output.strip():
                print(output, end="" if output.endswith("\n") else "\n")
            return 0
        if not _print_concise_prompt_version_failure(output):
            print(output, end="" if output.endswith("\n") else "\n")
        print(f"\nFAILED: {label} exited with status {result.returncode}")
        return result.returncode

    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"\nFAILED: {label} exited with status {result.returncode}")
    return result.returncode



def print_workflow_help() -> None:
    """Print a concise guide to the common generator commands."""
    print("AI Personal Tutor Package Generator command guide")
    print("=" * 52)
    print(f"Repository root: {ROOT}")
    print()
    print("Most common commands")
    print("--------------------")
    print("1. Check everything without changing generated files:")
    print("   python scripts\\run_generator_checks.py")
    print()
    print("2. Rebuild generated files first, then check everything:")
    print("   python scripts\\run_generator_checks.py --build-first")
    print()
    print("3. Fix the common mixed-version case, then check everything:")
    print("   python scripts\\run_generator_checks.py --sync-release-metadata")
    print()
    print("4. Preview local clean-up of temporary generator artifacts:")
    print("   python scripts\\clean_generator_artifacts.py")
    print()
    print("5. Remove local temporary generator artifacts after reviewing the preview:")
    print("   python scripts\\clean_generator_artifacts.py --apply")
    print()
    print("6. Prepare and build a normal toolkit release:")
    print("   python scripts\\build_toolkit_release.py --version 3.6 --date 2026-06-14")
    print()
    print("7. Prepare and build a release where the audit/testing pack also changed:")
    print("   python scripts\\build_toolkit_release.py --version 3.6 --testing-pack-version 3.6 --date 2026-06-14")
    print()
    print("When to use which")
    print("-----------------")
    print("- Use the standard check before committing generator or source changes.")
    print("- Use --build-first after editing source files under src/.")
    print("- Use --sync-release-metadata only when generated prompt-library files are")
    print("  already on a newer version and you intend to keep that newer version.")
    print("- Use build_toolkit_release.py when creating a distributable site package.")
    print("- Use clean_generator_artifacts.py when Python cache or temporary generated/ folders")
    print("  are cluttering git status. It is dry-run by default.")
    print()
    print("Windows note")
    print("------------")
    print("Run the Python commands directly. The .ps1 helper scripts are optional and")
    print("may be blocked by local PowerShell execution policy.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the standard package-generator checks in sequence."
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print a concise guide to the common generator workflows, then exit.",
    )
    parser.add_argument(
        "--skip-health",
        action="store_true",
        help="Skip the quick generator health report.",
    )
    parser.add_argument(
        "--skip-prompt",
        action="store_true",
        help="Skip prompt-library CI checks.",
    )
    parser.add_argument(
        "--skip-audit",
        action="store_true",
        help="Skip audit/testing-pack CI checks.",
    )
    parser.add_argument(
        "--skip-site-data",
        action="store_true",
        help="Skip generated site-data checks.",
    )
    parser.add_argument(
        "--skip-release-consistency",
        action="store_true",
        help="Skip release consistency checks.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the commands that would run, without running them.",
    )
    parser.add_argument(
        "--build-first",
        action="store_true",
        help="Rebuild prompt libraries, audit/testing pack and site data before running checks.",
    )
    parser.add_argument(
        "--sync-release-metadata",
        action="store_true",
        help=(
            "Before running checks, sync src/release.yml to the newest generated "
            "prompt-library version, rebuild prompt libraries and site data, then continue. "
            "Use this only when you intentionally want to keep the newer generated version."
        ),
    )
    args = parser.parse_args()

    if args.explain:
        print_workflow_help()
        return 0

    if args.sync_release_metadata and args.build_first:
        print("Use either --sync-release-metadata or --build-first, not both.")
        return 2

    if args.sync_release_metadata:
        print("Package Generator release-metadata sync")
        print(f"Repository root: {ROOT}")
        rc = run_step(
            "Sync release metadata to generated prompt-library version",
            ["scripts/sync_release_metadata.py", "--to-generated", "--build"],
            dry_run=args.dry_run,
        )
        if rc:
            return rc

    if args.build_first:
        print("Package Generator build refresh")
        print(f"Repository root: {ROOT}")
        for label, cmd in [
            ("Rebuild prompt libraries", ["scripts/build_prompt_libraries.py"]),
            ("Rebuild audit/testing pack", ["scripts/build_audit_pack.py"]),
            ("Rebuild site data", ["scripts/build_site_data.py"]),
        ]:
            rc = run_step(label, cmd, dry_run=args.dry_run)
            if rc:
                return rc

    steps: list[tuple[str, list[str]]] = []
    if not args.skip_health:
        steps.append(("Generator health report", ["scripts/generator_health_report.py", "--fail-on-problems", "--no-recommendations"]))
    if not args.skip_prompt:
        steps.append(("Prompt-library CI", ["scripts/build_prompt_libraries.py", "--ci"]))
    if not args.skip_audit:
        steps.append(("Audit/testing-pack CI", ["scripts/build_audit_pack.py", "--ci"]))
    if not args.skip_site_data:
        steps.append(("Generated site-data check", ["scripts/build_site_data.py", "--check"]))
    if not args.skip_release_consistency:
        steps.append(("Release consistency check", ["scripts/release_consistency_check.py", "--fail-on-problems"]))

    if not steps:
        print("No checks selected.")
        return 0

    print("Package Generator standard checks")
    print(f"Repository root: {ROOT}")
    for label, cmd in steps:
        rc = run_step(label, cmd, dry_run=args.dry_run)
        if rc:
            return rc
    print("\nAll selected generator checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
