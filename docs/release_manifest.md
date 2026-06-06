# AI Personal Tutor Toolkit — release manifest

Toolkit release: Site v2.24 / Prompt libraries v2.5 / Testing pack v2.9

This manifest describes the current public site package after the v2.24 prompt-library maintenance update.

## Repository-level developer files

- `README.md` — repository introduction and live site link
- `PROMPTS.md` — developer guide to prompt-library locations, structure and customisation strategy
- `CUSTOMISING_PROMPTS.md` — interim guide for building smaller tailored libraries from the master library

## Publishing structure

The public GitHub Pages site is now contained in the `docs/` folder. GitHub Pages should be configured to publish from `main` / `docs`.

## Main site pages

- `docs/index.html` — homepage
- `docs/tools/index.html` — tools directory
- `docs/tools/writing-tutor.html` — Writing Tutor page
- `docs/tools/structure-tutor.html` — Structure Tutor page
- `docs/tools/academic-thinking.html` — Academic Thinking page
- `docs/tools/research-proposal.html` — Research Proposal page
- `docs/tools/study-workflow.html` — Study Workflow page
- `docs/examples/index.html` — examples page
- `docs/student-help/index.html` — Student Help home
- `docs/guides/index.html` — Guides home
- `docs/testing.html` — testing and audit page
- `docs/about.html` — About this site
- `docs/changelog/index.html` — public changelog

## Student Help pages

- `docs/student-help/students.html`
- `docs/student-help/writing-workflow.html`
- `docs/student-help/not-first-draft.html`
- `docs/student-help/free-tier.html`
- `docs/student-help/markdown.html`

## Guides and reference pages

- `docs/guides/teaching-approach.html`
- `docs/guides/why-educators.html`
- `docs/guides/tutors.html`
- `docs/guides/setup.html`
- `docs/guides/customising-prompts.html`
- `docs/guides/other-ai-tutoring-resources.html`

## Prompt-library downloads

Current public downloads are in:

- `docs/prompt-libraries/latest/`

Versioned prompt-library archives are in:

- `docs/prompt-libraries/v2.1/`
- `docs/prompt-libraries/v2.2/`
- `docs/prompt-libraries/v2.3/`
- `docs/prompt-libraries/v2.4/`
- `docs/prompt-libraries/v2.5/`

## Testing/audit downloads

Current public testing files are in:

- `docs/audit-library/latest/`

Versioned testing/audit archives are in:

- `docs/audit-library/v2.5/`
- `docs/audit-library/v2.6/`
- `docs/audit-library/v2.7/`
- `docs/audit-library/v2.8/`
- `docs/audit-library/v2.9/`

## Detailed update notes

Detailed update notes are in:

- `docs/changelog/site-update-notes/`

## v2.21 housekeeping notes

- The repository root is now kept for repository-level files, especially `README.md`.
- The public site lives under `docs/`.
- Tool pages now live under `docs/tools/`.
- The examples page now lives under `docs/examples/`.
- The old root-level `changelog.html` compatibility page has been removed.
- Prompt-library and testing/audit behaviour did not change.

## v2.22 housekeeping notes

- Added root-level `PROMPTS.md` so developers can find the prompt libraries and understand the mini-library structure.
- Added root-level `CUSTOMISING_PROMPTS.md` with the interim “delete down from the master library” customisation method.
- Added a quiet public guide page at `docs/guides/customising-prompts.html` that points to the developer notes.
- Added an About page note for developers and departments.
- Prompt-library and testing/audit behaviour did not change.


## v2.23 housekeeping notes

- Updated the testing/audit pack to v2.9.
- Added two-chat audit workflow guidance, clearer rating boundaries, N/A evidence-table guidance, stronger SW3 testing, and a richer test log with AI tool/model and plan/access fields.
- Removed ambiguous version numbers from suggested test-output filenames and records versions in the test log instead.
- Improved the Examples page with more varied placeholder examples and a short dialogue example.
- Refined Student Help, Guides and Tools wording based on review feedback.
- Prompt-library behaviour did not change.


## v2.24 housekeeping notes

- Updated the prompt-library suite to v2.5.
- Changed visible file status in current prompt-library downloads from “working draft” to “active public release”.
- Added level, discipline and task calibration guidance to the global rules.
- Improved WT6 house-style fallback wording, added a WT3 worked correction-boundary example, and changed AT10 “random topic” wording to “useful starting point”.
- Rebuilt `docs/prompt-libraries/latest/`, `docs/prompt-libraries/v2.5/`, and the current mini-library ZIP downloads.
- Testing/audit pack remains v2.9.
