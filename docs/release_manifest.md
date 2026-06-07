# AI Personal Tutor Toolkit — release manifest

Toolkit release: Site v3.3 / Prompt libraries v3.1 / Testing pack v3.1

This manifest describes the current public site package after the v3.1 site revision aligning the public website with the v3.0 paragraph-first tutor style and writing-as-thinking prompt-library update.

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
- `docs/prompt-libraries/v3.0/`

## Testing/audit downloads

Current public testing files are in:

- `docs/audit-library/latest/`

Versioned testing/audit archives are in:

- `docs/audit-library/v2.5/`
- `docs/audit-library/v2.6/`
- `docs/audit-library/v2.7/`
- `docs/audit-library/v2.8/`
- `docs/audit-library/v2.10/`
- `docs/audit-library/v3.0/`

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


## Site v2.25 — homepage and navigation polish; testing stress test

- Updated the homepage from the revised student-facing draft.
- Updated Student Help and Guides home pages from revised drafts.
- Simplified tool-detail pages using the Writing Tutor page as the model.
- Added a separate tool-code column to tool-detail tables.
- Updated the testing/audit pack to v2.10 with a deadline-pressure adversarial stress test.


## Site v3.0 — prompt-library v3.0 tutor-style revision

- Updated the prompt-library suite to v3.0.
- Added paragraph-first output guidance so student-facing feedback uses short, readable paragraphs by default and avoids unnecessary bullet overload.
- Added manageable-feedback guidance so tools focus on useful next moves rather than producing more feedback than the student can act on.
- Added the “I'm stuck” support model across libraries.
- Added “writing is thinking” as a guiding principle.
- Clarified the toolkit's scope as writing, revision, academic thinking, research planning and study workflow support rather than a general-purpose homework-answer system.
- Added plain-English grammar-term guidance for essential terms such as subject, verb and object.
- Rebuilt `docs/prompt-libraries/latest/`, `docs/prompt-libraries/v3.0/`, and the current mini-library ZIP downloads.
- Testing/audit pack remains v2.10.



## Site v3.3 — testing/audit v3 alignment

- Updated testing/audit pack to v3.0.
- Added audit checks for paragraph-first tutor style, manageable feedback, writing as thinking, plain-English grammar explanations and “I’m stuck” support.
- Added U5 “I’m stuck” support test and v3 regression cards.
- Rebuilt `docs/audit-library/latest/`, `docs/audit-library/v3.0/`, and the testing-pack ZIP downloads.
- Prompt libraries remain v3.0.

## Site v3.1 — site alignment with v3 tutor style

- Updated homepage and public site wording to present the toolkit as structured and specialist writing support, not only guardrails.
- Added clearer site guidance on writing as thinking, paragraph-first tutor style, manageable feedback and “I’m stuck” support.
- Updated Student Help, Teaching Approach, Educator and Tutor pages to reflect the v3 prompt-library principles.
- Prompt libraries remain v3.0 and testing/audit pack remains v2.10.
