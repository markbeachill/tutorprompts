# AI Personal Tutor Package Generator v2.7

This is a repository tooling release for the AI Personal Tutor Toolkit. It is **not** a website/content release.

Extract this ZIP into the **root of your local GitHub repository**. It adds and updates generator source files, scripts, GitHub workflows and documentation.

## Start here

For the shortest instructions, read:

```text
PACKAGE_GENERATOR_START_HERE.md
```

After extracting the ZIP, run the standard checks from the repository root:

```powershell
python scripts\run_generator_checks.py
```

This command is Windows-friendly and runs the deeper generator checks in sequence.

## What v2.7 does

v2.7 keeps the mixed-version diagnostics and adds a one-command recovery option to the standard check runner. If generated prompt-library files are already on a newer version than `src/release.yml`, you can now run `python scripts\run_generator_checks.py --sync-release-metadata` to sync release metadata, rebuild prompt libraries and site data, then run the checks.

v2.7 keeps the existing prompt-library, audit-pack, site-data, release-preparation and packaging behaviour. It adds a safer explanation path for choosing between standard checks, build refreshes, mixed-version recovery and release packaging.

New in v2.7:

- `run_generator_checks.py --explain` prints a concise command guide for the common generator workflows.
- The command guide explains when to use the standard check, `--build-first`, `--sync-release-metadata`, and `build_toolkit_release.py`.
- Documentation now points users to the built-in command guide before choosing a recovery or release command.
- Existing v2.5 commands remain unchanged.

Kept from earlier generator releases:

- Source-driven prompt-library generation from `src/prompt-library/`.
- Metadata-driven tool menus, available-tools tables and router mappings.
- Master library and five mini-library generation.
- Custom-pack generation.
- Single-tool pack generation, README, manifest and ZIP output.
- Audit/testing-pack source, latest/archive copying, versioning and ZIP generation.
- Generated site-integration data under `docs/data/`.
- Release-preparation support from `src/release.yml`.
- Separate `testing_pack_version` support for audit/testing content.
- Clean site-package ZIP creation under `dist/`.
- One-command release orchestration.
- GitHub Actions checks.

## Main commands

### Standard local checks

```powershell
python scripts\run_generator_checks.py
```

This runs:

```powershell
python scripts\generator_health_report.py --fail-on-problems --no-recommendations
python scripts\build_prompt_libraries.py --ci
python scripts\build_audit_pack.py --ci
python scripts\build_site_data.py --check
python scripts\release_consistency_check.py --fail-on-problems
```

### Build prompt libraries

```powershell
python scripts\build_prompt_libraries.py
```

### Build audit/testing pack

```powershell
python scripts\build_audit_pack.py
```

### Build generated site data

```powershell
python scripts\build_site_data.py
```

### Prepare and build a toolkit release

If the audit/testing pack did not change:

```powershell
python scripts\build_toolkit_release.py --version 3.6 --date 2026-06-14
```

If the audit/testing pack also changed and should receive its own version bump:

```powershell
python scripts\build_toolkit_release.py --version 3.6 --testing-pack-version 3.6 --date 2026-06-14
```

### Create draft release notes

```powershell
python scripts\generate_release_notes_draft.py --version 3.6 --date 2026-06-14
```

## Source and generated files

Human-edited source files are mainly in:

```text
src/prompt-library/
src/audit-library/files/
src/release.yml
```

Generated files are mainly in:

```text
docs/prompt-libraries/
docs/audit-library/
docs/data/
dist/
```

The prompt libraries are assembled from many source blocks. The audit/testing pack is simpler: its source files are manually edited, then copied, stamped, archived and zipped by the generator.

## Windows note

The `.ps1` helper scripts are optional. If PowerShell blocks them because they are not digitally signed, run the Python commands directly. The Python commands are the source of truth.

## GitHub Actions

The generator includes workflows under:

```text
.github/workflows/
```

These are repository automation files. They are not part of the public GitHub Pages website.

## What v2.7 deliberately does not do

- It does not automatically write final changelog prose.
- It does not provide a web interface for creating custom packs.
- It does not publish custom or single-tool packs on the website automatically.
- It does not make the audit/testing pack structurally complex; audit source files remain manually edited.


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

## v2.7 local clean-up helper

Package Generator v2.7 adds a conservative clean-up helper for local temporary files created while running checks and builds.

Preview what would be removed:

```powershell
python scripts\clean_generator_artifacts.py
```

Actually remove the listed temporary files:

```powershell
python scripts\clean_generator_artifacts.py --apply
```

The helper targets Python bytecode caches and temporary `generated/` comparison folders. It does not remove source files, generated public library files, archive folders or ZIP packages. Use `--include-dist` only if you also want to remove built packages in `dist/`.
