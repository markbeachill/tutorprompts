#!/usr/bin/env python3
"""Create a draft changelog/update-notes file for a toolkit release.

Package Generator v1.3 helper.

This script deliberately creates a draft, not final release prose. It gives the
normal file path and a structured template so the author can fill in the actual
changes manually.

Typical use from the repository root:
    python scripts/generate_release_notes_draft.py
    python scripts/generate_release_notes_draft.py --version 3.6 --date 2026-06-14

By default, the script refuses to overwrite an existing notes file. Use --force
only when you deliberately want to recreate the draft.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
RELEASE_YML = ROOT / "src" / "release.yml"
DEFAULT_NOTES_DIR = ROOT / "docs" / "changelog" / "site-update-notes"


@dataclass(frozen=True)
class ReleaseValues:
    toolkit_version: str
    prompt_library_version: str
    testing_pack_version: str
    release_date: str

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
    def filename_version(self) -> str:
        return self.toolkit_version.lstrip("v").replace(".", "_")


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


def normalise_version(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return value.lstrip("v")


def load_release_values(version: str | None, release_date: str | None) -> ReleaseValues:
    config = simple_yaml_load(RELEASE_YML)
    toolkit = normalise_version(version) or normalise_version(config.get("toolkit_version"))
    prompt = normalise_version(config.get("prompt_library_version")) or toolkit
    testing = normalise_version(config.get("testing_pack_version")) or toolkit
    final_date = release_date or config.get("release_date") or date.today().isoformat()
    if not toolkit:
        raise SystemExit("No version supplied and src/release.yml does not contain toolkit_version.")
    if not prompt or not testing:
        raise SystemExit("Could not determine prompt_library_version or testing_pack_version from src/release.yml.")
    return ReleaseValues(toolkit_version=toolkit, prompt_library_version=prompt, testing_pack_version=testing, release_date=final_date)


def default_output_path(values: ReleaseValues) -> Path:
    return DEFAULT_NOTES_DIR / f"ai_personal_tutor_site_update_v{values.filename_version}_notes.md"


def build_template(values: ReleaseValues) -> str:
    return f"""# AI Personal Tutor Toolkit — update notes {values.toolkit_label}

**Release date:** {values.release_date}  
**Toolkit version:** {values.toolkit_label}  
**Prompt-library suite:** {values.prompt_label}  
**Testing pack:** {values.testing_label}

> Draft created by `scripts/generate_release_notes_draft.py`. Replace the TODO lines with the agreed release summary before publishing.

## Summary

TODO: Add a short one-paragraph summary of the release.

## Site changes

- TODO: List public website/page changes.

## Prompt-library changes

- TODO: List prompt-library changes, or write: Prompt libraries unchanged.

## Testing/audit-pack changes

- TODO: List testing/audit-pack changes, or write: Testing/audit pack unchanged.

## Generator/build changes

- TODO: List package-generator changes if this release includes them, or write: No public generator changes in the site package.

## Files to check before publishing

- `README.md`
- `docs/index.html`
- `docs/tools/index.html`
- `docs/testing.html`
- `docs/release_manifest.md`
- `docs/changelog/index.html`
- `docs/changelog/site-update-notes/ai_personal_tutor_site_update_v{values.filename_version}_notes.md`
- `docs/prompt-libraries/latest/`
- `docs/prompt-libraries/{values.prompt_label}/`
- `docs/prompt-libraries/latest/ai_personal_tutor_mini_libraries.zip`

## Suggested checks

```bash
python scripts/build_prompt_libraries.py --ci
python scripts/release_consistency_check.py --fail-on-problems
python scripts/build_site_package.py --run-generator-check --version {values.toolkit_version}
```
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a draft update-notes Markdown file for a toolkit release.")
    parser.add_argument("--version", help="Toolkit version for the draft, for example 3.6. Defaults to src/release.yml.")
    parser.add_argument("--date", help="Release date in YYYY-MM-DD format. Defaults to src/release.yml or today.")
    parser.add_argument("--output", type=Path, help="Optional output path. Defaults to docs/changelog/site-update-notes/...")
    parser.add_argument("--force", action="store_true", help="Overwrite the draft if it already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written without changing files.")
    parser.add_argument("--print", dest="print_text", action="store_true", help="Print the draft text to stdout as well as writing it unless --dry-run is used.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    values = load_release_values(args.version, args.date)
    output = args.output or default_output_path(values)
    if not output.is_absolute():
        output = ROOT / output
    text = build_template(values)

    if args.print_text:
        print(text)

    if args.dry_run:
        print(f"Would write draft release notes: {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
        return 0

    if output.exists() and not args.force:
        raise SystemExit(
            f"Release notes draft already exists: {output}\n"
            "Use --force to overwrite, or edit the existing file manually."
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8", newline="\n")
    try:
        shown = output.relative_to(ROOT)
    except ValueError:
        shown = output
    print(f"Created draft release notes: {shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
