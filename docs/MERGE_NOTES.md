# Merge notes: (b) site restructure integrated into repo docs

Base: repository `docs/` at v4.1. Source of design layer: package (b) `mysite` (labelled v4.0).
Package (c) `v4_site_update` contributed nothing (superseded: v4.0 audit content is generator-owned and older than the repo's v4.1).

## Generator-owned, left untouched
`audit-library/`, `prompt-libraries/`, `data/` — regenerated from `src/`, not hand-edited.

## Already identical (no action)
The testing-audit/cards/collector/limitations and deployment-routes/check/documentation pages were already byte-identical between repo and (b).

## Dual-evolved pages — YOUR ACTION NEEDED
Each kept the repo's v4.1 page and gained a `.alt.html` carrying (b)'s version. Reconcile by hand, then delete the `.alt.html`.

- `changelog/index.html`  <->  `changelog/index.alt.html`
- `guides/index.html`  <->  `guides/index.alt.html`
- `guides/setup.html`  <->  `guides/setup.alt.html`
- `index.html`  <->  `index.alt.html`
- `testing.html`  <->  `testing.alt.html`
- `tools/academic-thinking.html`  <->  `tools/academic-thinking.alt.html`
- `tools/index.html`  <->  `tools/index.alt.html`
- `tools/research-proposal.html`  <->  `tools/research-proposal.alt.html`
- `tools/single-tools.html`  <->  `tools/single-tools.alt.html`
- `tools/writing-tutor.html`  <->  `tools/writing-tutor.alt.html`

## Full action log

- `style.css`: REPLACED with restructured design-system stylesheet (b); oldstyle.css kept as backup
- `about.html`: ADOPTED b design (visible text identical)
- `examples/index.html`: ADOPTED b design (visible text identical)
- `guides/customising-prompts.html`: ADOPTED b design (visible text identical)
- `guides/other-ai-tutoring-resources.html`: ADOPTED b design (visible text identical)
- `guides/teaching-approach.html`: ADOPTED b design (visible text identical)
- `guides/tutors.html`: ADOPTED b design (visible text identical)
- `guides/why-educators.html`: ADOPTED b design (visible text identical)
- `student-help/directing-ai.html`: ADOPTED b design (visible text identical)
- `student-help/free-tier.html`: ADOPTED b design (visible text identical)
- `student-help/index.html`: ADOPTED b design (visible text identical)
- `student-help/markdown.html`: ADOPTED b design (visible text identical)
- `student-help/not-first-draft.html`: ADOPTED b design (visible text identical)
- `student-help/student-ai-setup.html`: ADOPTED b design (visible text identical)
- `student-help/students.html`: ADOPTED b design (visible text identical)
- `student-help/writing-workflow.html`: ADOPTED b design (visible text identical)
- `tools/structure-tutor.html`: ADOPTED b design (visible text identical)
- `tools/study-workflow.html`: ADOPTED b design (visible text identical)
- `changelog/index.html`: KEPT repo v4.1 version; b's v4.0 version added as changelog/index.alt.html for hand-reconciliation
- `guides/index.html`: KEPT repo v4.1 version; b's v4.0 version added as guides/index.alt.html for hand-reconciliation
- `guides/setup.html`: KEPT repo v4.1 version; b's v4.0 version added as guides/setup.alt.html for hand-reconciliation
- `index.html`: KEPT repo v4.1 version; b's v4.0 version added as index.alt.html for hand-reconciliation
- `testing.html`: KEPT repo v4.1 version; b's v4.0 version added as testing.alt.html for hand-reconciliation
- `tools/academic-thinking.html`: KEPT repo v4.1 version; b's v4.0 version added as tools/academic-thinking.alt.html for hand-reconciliation
- `tools/index.html`: KEPT repo v4.1 version; b's v4.0 version added as tools/index.alt.html for hand-reconciliation
- `tools/research-proposal.html`: KEPT repo v4.1 version; b's v4.0 version added as tools/research-proposal.alt.html for hand-reconciliation
- `tools/single-tools.html`: KEPT repo v4.1 version; b's v4.0 version added as tools/single-tools.alt.html for hand-reconciliation
- `tools/writing-tutor.html`: KEPT repo v4.1 version; b's v4.0 version added as tools/writing-tutor.alt.html for hand-reconciliation

## Note
`student-help/index2.html` is a repo-only page (not in b); left as-is.

## Pre-existing repo cruft
`README_site_update.md` was already in the repo `docs/` (a "remove before publishing" drop note). Left untouched; delete before publishing.
