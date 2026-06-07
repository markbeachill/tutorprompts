# Package Generator — Start here

This package generator is repository tooling for the AI Personal Tutor Toolkit. It is not a public website release.

Extract the generator ZIP into the root of the GitHub repository. The repository root is the folder that contains `docs/`, `src/`, `scripts/` and `README.md`.

## First check after installing

From the repository root, run:

```powershell
python scripts\run_generator_checks.py
```

This runs the standard checks in a Windows-friendly sequence:

```powershell
python scripts\generator_health_report.py --fail-on-problems
python scripts\build_prompt_libraries.py --ci
python scripts\build_audit_pack.py --ci
python scripts\build_site_data.py --check
python scripts\release_consistency_check.py --fail-on-problems
```

If generated outputs may be missing or stale, use the refresh-and-check command instead:

```powershell
python scripts\run_generator_checks.py --build-first
```

On macOS/Linux/Git Bash, the same command is:

```bash
python scripts/run_generator_checks.py
```

## Normal editing workflow

Edit source files, not generated prompt-library files.

Human-edited sources live mainly in:

```text
src/prompt-library/
src/audit-library/files/
src/release.yml
```

Generated files live mainly in:

```text
docs/prompt-libraries/
docs/audit-library/
docs/data/
dist/
```

After editing prompt-library source files:

```powershell
python scripts\build_prompt_libraries.py
python scripts\run_generator_checks.py
```

After editing audit/testing source files:

```powershell
python scripts\build_audit_pack.py
python scripts\run_generator_checks.py
```

## Preparing a toolkit release

If the prompt libraries and site move to a new version but the audit/testing pack did not change:

```powershell
python scripts\build_toolkit_release.py --version 3.6 --date 2026-06-14
```

If the audit/testing pack also changed and needs its own version bump:

```powershell
python scripts\build_toolkit_release.py --version 3.6 --testing-pack-version 3.6 --date 2026-06-14
```

The testing/audit pack has its own content version. It may intentionally stay at an earlier version when its files have not changed.

## Common fixes

If checks say generated prompt-library files are out of date, run:

```powershell
python scripts\build_prompt_libraries.py
python scripts\run_generator_checks.py
```

If checks say audit/testing files are out of date, run:

```powershell
python scripts\build_audit_pack.py
python scripts\run_generator_checks.py
```

If checks show generated files are on a newer version than `src/release.yml`, run the release-preparation command printed by the diagnostic, then rebuild.


## v2.7 note

When `run_generator_checks.py` calls the health report, it now suppresses the health report follow-up suggestions. Running `generator_health_report.py` directly still shows the standard next command.


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


## Not sure which command to run?

Use the built-in command guide:

```powershell
python scripts
un_generator_checks.py --explain
```

This does not change any files. It explains the standard check, build refresh, mixed-version recovery and release-package workflows.

## Optional clean-up command

If your local `git status` is cluttered by Python cache files or temporary `generated/` folders, preview the clean-up first:

```powershell
python scripts\clean_generator_artifacts.py
```

Then apply it only if the preview looks right:

```powershell
python scripts\clean_generator_artifacts.py --apply
```
