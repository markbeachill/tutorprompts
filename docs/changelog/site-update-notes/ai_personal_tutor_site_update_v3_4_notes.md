# Site update v3.4 — Startup activation and launcher fidelity

- Site package: v3.4
- Prompt libraries: v3.2
- Testing/audit pack: v3.2

## Summary

This release strengthens startup activation and launcher fidelity after testing showed that some AI models activate the library but reconstruct the menu from internal sections.

## Changes

- Added a menu source rule: the launcher is the only source for menu output.
- Marked manifest and router sections as internal and not for output.
- Added visible selected-tool version headings, such as `WT1 — Clarity Clinic v3.2`.
- Added current prompt-library version notes near downloads on the homepage and Tools page.
- Updated U6 to test both startup activation and faithful launcher output.
- Updated customising/developer documentation with menu-source guidance.
