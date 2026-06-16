# Project documentation

This folder contains the current maintainer documentation for the AI Personal Tutor Toolkit repository.

Use this folder when you need to understand how the repository works **now**. Historical design notes and future proposals live elsewhere.

## Start here

- `repository-layout.md` — what belongs in each top-level folder.
- `build-system.md` — the generator scripts and how they fit together.
- `release-process.md` — the release-version policy and release workflow.
- `generated-files.md` — which files are edited by hand and which are generated.
- `site-pages.md` — how the generated website pages are maintained.
- `audit-testing.md` — how the testing/audit pack is built.
- `source-material.md` — how the source-material library is edited and generated.
- `tool-index.md` — where the current tool list and tool metadata live.
- `tooling/scripts.md` — script-by-script maintainer notes.
- `tooling/github-actions.md` — GitHub Actions and deploy-time build notes.

## Related folders

```text
project-docs/  current maintainer/developer documentation
tool-history/  past design decisions, release-era notes and tool-development records
roadmaps/      future work and proposals
docs/          public GitHub Pages site
src/           editable source material for generated outputs
scripts/       build, check and packaging scripts
```

## Rule for AI assistants

If you have no prior context and are asked to update or build the repository:

1. Read `README.md` in the repository root.
2. Read `BUILD_AND_GENERATOR_GUIDE.md` in the repository root.
3. Read this file and `repository-layout.md`.
4. Edit source files under `src/` or generator files under `scripts/` as appropriate.
5. Run `python scripts/run_generator_checks.py --build-first` before packaging.

Do not treat `tool-history/` or `roadmaps/` as current instructions unless the user explicitly asks you to implement something from them.
