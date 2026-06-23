# AI Personal Tutor custom prompt packs

This folder contains generated custom packs built from YAML files in `src/prompt-library/custom-packs/`.
Each custom pack includes the shared operating/help rules, the generated menu/router, and the selected tool instructions.

Build all custom packs from the repository root with:

```bash
python scripts/build_prompt_libraries.py --include-custom
```

Check all custom packs without writing changes with:

```bash
python scripts/build_prompt_libraries.py --include-custom --check
```

## Included custom packs

### First-Year Writing Support Pack

- Source YAML: `src/prompt-library/custom-packs/example-first-year-writing-support.yml`
- Generated file: `docs/prompt-libraries/custom/first_year_writing_support_pack.md`
- Tool count: 4
- Tools: WT2 — Clarity Clinic, WT3 — Single Paragraph Analysis, ST1 — Paragraph Structure Review Across a Whole Draft, SW1 — Revision Plan
