# Repository documentation policy

Use this policy to decide where documentation belongs.

```text
Root files       Entry points and standard GitHub files.
project-docs/    Current maintainer and developer documentation.
tool-history/    Past tool-design decisions, release-era notes and approach records.
roadmaps/        Future work and proposals.
docs/            Published GitHub Pages site.
scripts/         Build, check and packaging scripts.
src/             Editable source for generated content.
```

If a document gives current build instructions, it belongs in `project-docs/` or the root build guide.

If a document explains how a tool or approach developed in the past, it belongs in `tool-history/`.

If a document describes a possible future tool or future site change, it belongs in `roadmaps/`.

If a document should appear on the public website, it belongs under `docs/` or should be generated there.
