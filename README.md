# AI Personal Tutor Toolkit site

This is the deployable GitHub Pages version of the AI Personal Tutor Toolkit.

## Folder structure

- Root HTML files: public website pages
- `style.css`: shared styling
- `prompt-libraries/latest/`: current student-facing prompt libraries with stable filenames
- `prompt-libraries/v2.0/`: fixed archive of prompt library version 2.0
- `audit-library/latest/`: current educator testing and audit materials with stable filenames
- `audit-library/v2.4/`: fixed archive of testing pack version 2.4

## Versioning approach

The website links to the `latest/` folders so download URLs can remain stable.
Versioned folders preserve the exact release files for developers and educators who need to know which version they are testing or adapting.

Current prompt library version: v2.0
Current testing/audit pack version: v2.4

## Deploying

Upload the contents of this folder to the root of a GitHub Pages repository.


## Site editing rules

- Student-facing pages should explain what the toolkit does and how to use it. Avoid GitHub folder-structure details on Home, Tools, Examples and library pages.
- Put visible content inside `<section class="hero"><div class="container">...` or inside `<div class="container"><section class="panel">...`.
- Do not place `<section class="panel">` directly under `<main>` unless it is an intentional exception. The CSS includes a fallback guardrail, but the clean structure is still preferred.
- Keep version-folder and release-archive details on `testing.html`, `changelog.html` or in this README.
