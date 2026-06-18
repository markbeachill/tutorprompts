# Generated files

This project keeps editable source files and generated public outputs separate.

## Editable source areas

```text
src/prompt-library/        Prompt-library source files and pack definitions.
src/audit-library/         Testing/audit source files.
src/source-material/       Source-material items and metadata.
src/examples/              Hand-editable example chat snippets ({code}-example-chat.html).
src/examples-tools/        Deterministic collector-to-snippet converter and its tests.
src/release.yml            Release metadata.
scripts/                   Generators and checks.
```

## Generated public outputs

```text
docs/prompt-libraries/     Master, mini-library, custom and single-tool Markdown files.
docs/audit-library/        Audit/testing pack outputs.
docs/data/                 Generated JSON metadata.
docs/source-material/      Copy-ready source-material page and downloads.
docs/tools/                Generated and normalised tool pages.
docs/where-to-start/       Generated decision-support page.
docs/download/             Generated download page.
docs/examples/             Example index and example pages.
docs/create-examples/        Create-examples page (cards, collector prompt, in-browser converter).
```

Note: `docs/create-examples/index.html` is generated, but
`docs/create-examples/example-cards.md` in the same folder is hand-edited
source (the example scenarios). It is kept beside the page it feeds.

## Usual commands

```bash
python scripts/run_generator_checks.py --build-first
python scripts/run_generator_checks.py
```

## Commit rule

Commit both the source change and the generated output change unless the project deliberately moves to deploy-time-only generated output.
