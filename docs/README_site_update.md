# Site update: deployment guide, testing guide, documentation guide, audit-library v4.0

Merge this tree into the repository's /docs (the GitHub Pages root).

## Contents

HTML pages (standalone styling — swap the embedded <style> block for the site stylesheet if preferred):
- guides/setup.html              (revised: now Deployment guide 1 of 3)
- guides/deployment-routes.html  (new: Deployment guide 2 of 3)
- guides/deployment-check.html   (new: Deployment guide 3 of 3 — the Level 1 check, all 27 tools)
- guides/documentation.html      (new: Producing documentation guide)
- guides/index.html              (updated guides index)
- testing.html                   (rebuilt: maintainer overview, 1 of 5)
- testing-collector.html         (new, 2 of 5 — copy box generated from the canonical file at build time)
- testing-audit.html             (new, 3 of 5)
- testing-cards.html             (new, 4 of 5)
- testing-limitations.html       (new, 5 of 5)

Canonical testing pack v4.0:
- audit-library/latest/   six .md files + ai_tutor_toolkit_testing_pack.zip
- audit-library/v4.0/     same files with _v4_0 suffix + versioned zip

## Notes

- Maintainer pages display the canonical .md files in iframes with download buttons, so the page shows the served file rather than a copy. The iframes require the .md files to be served raw; if the site build processes .md files, add a .nojekyll file or exclude audit-library from processing.
- The deployment-check page's sample inputs are quoted from the step-by-step cards file; if a card input changes, rebuild or edit that section.
- Remove this README before publishing.
