# Site update v2: pages rebuilt on the site design (style.css)

Merge this tree into /docs, replacing the standalone-styled versions of the same files.

## What changed from the previous drop

- All ten pages now use the site skeleton: ../style.css (or style.css) link, the real header/nav (.container.nav/.brand), hero sections with .kicker/.lead, content in .panel.reading sections, the site footer with .footer-links, lang="en-GB".
- guides/index.html rebuilt with the site's guide-card system (.card.guide-card with .guide-label, colour classes tutor/technical/resources/student) in a .grid.
- Buttons use the site's .button / .button.secondary classes. A small inline <style> block on each page adds only what style.css lacks: button.button cursor/font, .copywrap spacing, .fileframe for the canonical-file iframes, and panel h2 top-margin. Move these four rules into style.css if preferred and delete the inline block.
- audit-library/ content unchanged from the previous drop (same v4.0 pack files and zips); included again for completeness.

## Pages

guides/setup.html, guides/deployment-routes.html, guides/deployment-check.html, guides/documentation.html, guides/index.html, testing.html, testing-collector.html, testing-audit.html, testing-cards.html, testing-limitations.html

## Notes

- The collector page's copy box is generated verbatim from audit-library/latest/ai_tutor_toolkit_output_collector.md at build time (machine-verified identical).
- Iframes require the .md files to be served raw (a .nojekyll file if the Pages build runs Jekyll).
- Guide-card colour mapping used: Tutor/Educators -> tutor (purple), Developer/Maintainer -> technical (blue), Pedagogy -> student (green), Resources -> resources (gold), About/Release history -> default. Adjust classes in guides/index.html if you prefer different colours.
- Remove this README before publishing.
