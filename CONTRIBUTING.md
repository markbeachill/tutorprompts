# Contributing and maintenance workflow

This repository is source-driven. Most public files under `docs/` are generated from source files and scripts.

## Before changing the repository

Read:

```text
README.md
BUILD_AND_GENERATOR_GUIDE.md
project-docs/README.md
project-docs/repository-layout.md
```

## Normal workflow

1. Edit source files under `src/`, or generator files under `scripts/`.
2. Rebuild and check:

```bash
python scripts/run_generator_checks.py --build-first
```

3. Inspect the generated outputs in `docs/`.
4. Package if needed:

```bash
python scripts/build_site_package.py --run-generator-check --version 4.2
python scripts/build_site_package.py --include-generator --run-generator-check --version 4.2
```

## Do not hand-edit generated files as the source of truth

Generated outputs include prompt libraries, audit packs, site data, source-material pages and generated site pages. If a generated file is wrong, fix the source or generator and rebuild.

## Documentation locations

```text
project-docs/  current maintainer documentation
tool-history/  past tool and design history
roadmaps/      future proposals
docs/          public website
```
