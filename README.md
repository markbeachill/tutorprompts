# AI Personal Tutor Toolkit site

This repository contains a static GitHub Pages site for the AI Personal Tutor Toolkit.

## Folder structure

- `prompt-libraries/latest/`: current prompt library downloads used by the public site
- `prompt-libraries/v2.1/`: fixed archive of prompt library version v2.1
- `prompt-libraries/v2.2/`: fixed archive of prompt library version v2.2
- `prompt-libraries/v2.3/`: fixed archive of prompt library version v2.3
- `prompt-libraries/v2.4/`: fixed archive of prompt library version v2.4
- `audit-library/latest/`: current testing and audit downloads used by the public site
- `audit-library/v2.5/`: fixed archive of testing pack version v2.5
- `audit-library/v2.6/`: fixed archive of testing pack version v2.6
- `audit-library/v2.7/`: fixed archive of testing pack version v2.7
- `audit-library/v2.8/`: fixed archive of testing pack version v2.8

Student-facing pages should link to the `latest/` folders. Versioned folders are for educators, developers and audit trails.

Current prompt library version: v2.4
Current testing/audit pack version: v2.8
Current site package: v2.14


## How versions work

The project uses three related version labels:

- **Site package version**: the deployable website ZIP and public HTML pages.
- **Prompt-library suite version**: the current set of student-facing prompt libraries.
- **Testing/audit pack version**: the current educator testing and audit materials.

The `latest/` folders always contain the current public downloads. The fixed `v2.x/` folders are archive copies for educators, maintainers and audit trails. Each current downloadable Markdown file now includes a release stamp showing the site package, prompt-library suite, testing pack, public path and fixed archive path.

See `release_manifest.md` for the complete current file list.



## v2.14 guides section release

- Added a new top-level Guides navigation item.
- Added `guides.html` plus student, tutor/teacher, writing workflow, first-draft pedagogy and setup guide pages.
- Added `guide-setup.html` as a Coming soon placeholder.
- No prompt-library or testing/audit pack behaviour changed.

## v2.13 version-clarity maintenance release

- Added visible release stamps to the latest prompt-library and testing/audit Markdown downloads.
- Aligned current downloadable file headings with Libraries v2.4 and Testing pack v2.8.
- Added `release_manifest.md` to show how the public `latest/` downloads map to fixed archive files.
- Clarified the difference between site package, prompt-library suite and testing/audit pack versions.

## v2.12 formatting fix

- Rebuilt `testing.html` so its page header uses the same site header and hero structure as the other public pages.
- Added a CSS alias so `button-row` and `btn-row` both render consistently.
