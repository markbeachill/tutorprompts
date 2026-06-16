# Repository layout

This repository separates current source files, generated public files, maintainer documentation, historical notes and future proposals.

## Top-level folders

```text
src/           Human-edited source files for prompt libraries, audit packs, release metadata and source material.
scripts/       Python build, check, packaging and release scripts.
docs/          Public GitHub Pages site. Treat this as published website content.
dist/          Built release ZIPs, when present.
project-docs/  Current maintainer/developer documentation.
tool-history/  Record of past tool design decisions, release-era notes and approach documents.
roadmaps/      Future work, proposals and possible next directions.
.github/       GitHub Actions workflows.
```

## Root files

The root should stay small and should contain only entry points or standard GitHub files:

```text
README.md
CHANGELOG.md
CONTRIBUTING.md
BUILD_AND_GENERATOR_GUIDE.md
PACKAGE_GENERATOR_START_HERE.md
UPDATE-CHECKLISTS.md
CUSTOMISING_PROMPTS.md
SOURCE_MATERIAL_INDEX_EXPLAINER.md
```

`README.md` is the repository front door. `BUILD_AND_GENERATOR_GUIDE.md` is the build source of truth. `UPDATE-CHECKLISTS.md` is the operational checklist for tool, audit and rebuild changes. `CONTRIBUTING.md` is the shortest safe workflow for making a change.

## Public website rule

Because GitHub Pages uses `docs/` as the published site root, do not place maintainer-only notes in `docs/` unless they are intended to be public. Current maintainer notes go in `project-docs/`; historical notes go in `tool-history/`; future plans go in `roadmaps/`.

## Documentation status rule

```text
project-docs/ = current truth
tool-history/ = how we got here
roadmaps/ = where we may go next
```

If a document is not kept current, it should not live in `project-docs/` unless it clearly says so at the top.
