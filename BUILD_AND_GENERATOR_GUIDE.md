# Build and Generator Guide

This is the canonical build guide for the AI Personal Tutor Toolkit repository.

The repository has two different kinds of generated output:

1. **Library outputs** — prompt-library Markdown files, single-tool files, audit/testing files and JSON metadata.
2. **Page outputs** — static HTML pages that help users find tools, choose a starting point, download files and use source material.

Keeping those separate makes maintenance easier: edit `src/` for tool content, edit page/source data for site behaviour, then rebuild the relevant generated outputs.

## Quick commands

Rebuild all generated outputs and then run checks:

```bash
python scripts/run_generator_checks.py --build-first
```

Check everything without changing generated files:

```bash
python scripts/run_generator_checks.py
```

Build the clean public site ZIP:

```bash
python scripts/build_site_package.py --run-generator-check --version 4.2.1
```

Build the full repository ZIP, including generator files:

```bash
python scripts/build_site_package.py --include-generator --run-generator-check --version 4.2.1
```

## Release version policy

Public releases use a single version number:

```yaml
release_version: 4.2.1
toolkit_version: 4.2.1
prompt_library_version: 4.2.1
testing_pack_version: 4.2.1
```

`release_version` is the source of truth. The legacy keys are retained for compatibility with older scripts and generated text, but they must match `release_version`.

The audit/testing pack no longer has a separate public version. Audit/testing changes should be described in the changelog or release notes, while the generated audit library uses the same release version as the tutor libraries.

## Library generation scripts

These scripts build files that users copy, download or audit.

```bash
python scripts/build_prompt_libraries.py --include-single-tools --include-custom
python scripts/build_audit_pack.py
python scripts/build_site_data.py
```

What they do:

- `build_prompt_libraries.py` builds master, mini-library, custom and single-tool Markdown outputs under `docs/prompt-libraries/`.
- `build_audit_pack.py` builds audit/testing support files under `docs/audit-library/`.
- `build_site_data.py` builds JSON metadata under `docs/data/`, including the tool index used by generated site pages.

Check-only commands:

```bash
python scripts/build_prompt_libraries.py --ci
python scripts/build_audit_pack.py --ci
python scripts/build_site_data.py --check
```

## Page generation scripts

These scripts build static site pages. They do not change the prompt text itself.

```bash
python scripts/build_source_material_library.py
python scripts/build_site_pages.py
```

What they do:

- `build_source_material_library.py` builds the copy-ready source-material page, Markdown downloads and source-material JSON index.
- `build_site_pages.py` builds the collapsed Tools page, expandable Where to start? page, canonical Try It page, Examples index and Download page from generated metadata/hardcoded site links, then normalises site navigation and footer links.

Check-only commands:

```bash
python scripts/build_source_material_library.py --check
python scripts/build_site_pages.py --check
```

## Normal workflows

After editing a tutor tool under `src/prompt-library/tools/`:

```bash
python scripts/run_generator_checks.py --build-first
```

After editing source-material items under `src/source-material/items/`:

```bash
python scripts/run_generator_checks.py --build-first
```

After editing page/navigation generation logic:

```bash
python scripts/build_site_pages.py
python scripts/run_generator_checks.py
```

Before a release:

```bash
python scripts/build_toolkit_release.py --version 4.2.1 --date 2026-06-16
```

## What to commit

For prompt/tool changes, commit the source and generated outputs:

```text
src/prompt-library/...
docs/prompt-libraries/...
docs/data/...
```

For audit/testing changes, commit:

```text
src/audit-library/...
docs/audit-library/...
```

For source-material changes, commit:

```text
src/source-material/...
docs/source-material/...
docs/data/source_material_index.json
```

For page/navigation changes, commit:

```text
scripts/build_site_pages.py
docs/tools/index.html
docs/where-to-start/index.html
docs/download/index.html
docs/examples/index.html
docs/style.css
```

## GitHub Actions

The GitHub Pages workflow runs:

```bash
python scripts/run_generator_checks.py --build-first
```

That command rebuilds libraries, audit/testing outputs, source material and generated site pages before deployment. To use it, set GitHub Pages to deploy from **GitHub Actions** in the repository settings.

## Prompt files and customising

Human-edited prompt source lives under:

```text
src/prompt-library/
src/prompt-library/tools/
src/prompt-library/packs/
src/release.yml
```

Generated public prompt files live under:

```text
docs/prompt-libraries/latest/
docs/prompt-libraries/v4.2/
docs/prompt-libraries/single-tools/
```

Do not manually edit the generated prompt-library files as the primary source of truth. Edit the source files under `src/`, then rebuild with:

```bash
python scripts/run_generator_checks.py --build-first
```

For local/custom prompt-library adaptation, keep using:

```text
CUSTOMISING_PROMPTS.md
```

That file remains in the repository root because it is a live maintainer/educator guide rather than historical design notes.

## GitHub Pages build workflow

The optional GitHub-side build workflow lives at:

```text
.github/workflows/deploy-github-pages.yml
```

It runs the same build command used locally:

```bash
python scripts/run_generator_checks.py --build-first
```

This is a deploy-time build only. GitHub Pages still serves a static site to visitors.

To use it, set GitHub Pages to deploy from **GitHub Actions** in repository settings.

## Documentation organisation

The repository separates current maintainer documentation, historical design notes and future proposals:

```text
project-docs/  current maintainer/developer documentation
tool-history/  past tool-development decisions, design rationales and release-era notes
roadmaps/      future work and proposals
docs/          public GitHub Pages site
```

Use `project-docs/` for current operational documentation. Use `tool-history/` when preserving the record of an earlier approach or completed design decision. Use `roadmaps/` only for future or proposed work.

Older package-generator notes and superseded root notes have been moved out of the repository root to:

```text
tool-history/repository-docs/root-docs/
```

The current canonical build instructions are this file plus `UPDATE-CHECKLISTS.md`, `project-docs/` and `PACKAGE_GENERATOR_START_HERE.md`.
