# Package Generator Design — v2.7

## Purpose

The package generator is intended to stop drift between source files, generated prompt libraries, audit/testing files, archive copies, version stamps, ZIP files and release metadata.

This is a generator/tooling system, not a public website content release.

## Core principle

Edit source files. Generate public outputs.

Human-edited source files live mainly in:

```text
src/prompt-library/
src/audit-library/files/
src/release.yml
```

Generated outputs live mainly in:

```text
docs/prompt-libraries/
docs/audit-library/
docs/data/
dist/
```

## Current v2.7 structure

```text
.github/workflows/
├─ prompt-library-generator-check.yml
├─ build-site-package.yml
└─ build-toolkit-release.yml
scripts/
├─ build_prompt_libraries.py
├─ build_audit_pack.py
├─ build_site_data.py
├─ build_site_package.py
├─ build_toolkit_release.py
├─ prepare_toolkit_release.py
├─ release_consistency_check.py
├─ generator_health_report.py
├─ generate_release_notes_draft.py
└─ run_generator_checks.py
src/
├─ release.yml
├─ prompt-library/
└─ audit-library/
PACKAGE_GENERATOR_START_HERE.md
PACKAGE_GENERATOR_README.md
PACKAGE_GENERATOR_DESIGN.md
```

## Prompt-library generator

The prompt-library generator builds:

- the master prompt library;
- the five mini-libraries;
- custom packs from YAML;
- single-tool packs;
- deterministic ZIPs;
- metadata-driven menus, available-tools tables and router mappings.

The source of truth for stable tool metadata is:

```text
src/prompt-library/tool-metadata.json
```

Pack definitions live in:

```text
src/prompt-library/packs/
src/prompt-library/custom-packs/
```

Single-tool packs are generated from tool metadata and source tool files rather than from 27 separate hand-maintained manifests.

## Audit/testing-pack generator

The audit/testing pack is intentionally simpler than the tutor prompt-library system.

Audit source files are manually edited in:

```text
src/audit-library/files/
```

The audit build copies/stamps them into:

```text
docs/audit-library/latest/
docs/audit-library/v<toolkit-version>/
```

and rebuilds the testing-pack ZIP.

The audit/testing pack has its own content version:

```text
testing_pack_version
```

This may intentionally differ from the toolkit/prompt-library version if the audit/testing content has not changed.

## Release metadata

Release metadata lives in:

```text
src/release.yml
```

It supports separate values for:

```text
toolkit_version
prompt_library_version
testing_pack_version
release_date
status
```

Normal releases update the toolkit and prompt-library versions. The audit/testing pack version changes only when explicitly requested.

## Standard checks

The v2.7 standard local check command is:

```powershell
python scripts\run_generator_checks.py
```

To rebuild generated outputs before checking, use:

```powershell
python scripts\run_generator_checks.py --build-first
```

It runs:

```text
generator health report
prompt-library CI
audit/testing-pack CI
site-data freshness check
release consistency check
```

## Release workflow

A typical toolkit release command is:

```powershell
python scripts\build_toolkit_release.py --version 3.6 --date 2026-06-14
```

If audit/testing content also changed:

```powershell
python scripts\build_toolkit_release.py --version 3.6 --testing-pack-version 3.6 --date 2026-06-14
```

The release command performs preparation, rebuilds generated outputs, runs checks and creates a clean distributable package ZIP.

## Generated files should not be edited by hand

The generator can detect when generated prompt-library, audit/testing or site-data files are stale. If generated files differ from source output, rebuild from source rather than hand-editing generated outputs.


## v2.7 note

`run_generator_checks.py` now captures prompt-library CI failures and, when the failure is caused by a release-version mismatch between `src/release.yml` and generated prompt-library files, prints a concise diagnosis instead of dumping the full diff. Run `python scripts\build_prompt_libraries.py --ci` directly when the raw diff is needed.


## v2.7 mixed-version recovery helper

Package Generator v2.7 adds a convenience command for the common case where generated prompt-library files have already moved to a newer version but `src/release.yml` still says the previous version. To keep the newer generated version, sync the source metadata, rebuild and check, run from the repository root:

```powershell
python scripts\run_generator_checks.py --sync-release-metadata
```

Equivalent direct recovery command:

```powershell
python scripts\sync_release_metadata.py --to-generated --build --check
```

This updates toolkit/prompt-library release metadata to match the newest generated prompt-library version, rebuilds the prompt libraries and site data, and runs the standard checks. The audit/testing-pack version remains independent.


## v2.7 workflow explanation helper

Package Generator v2.7 adds a read-only workflow guide:

```powershell
python scripts
un_generator_checks.py --explain
```

The guide is intentionally simple and Windows-friendly. It helps users choose between checking only, rebuilding before checking, syncing release metadata to generated files, and building a distributable toolkit release.

## v2.7 local clean-up helper

The generator now includes `scripts/clean_generator_artifacts.py`, a conservative utility for removing local-only temporary files such as Python `__pycache__` folders, `.pyc` files and temporary `generated/` comparison directories. It is dry-run by default and requires `--apply` to delete anything. It does not delete source files, public generated prompt-library files, archive copies or package ZIPs.
