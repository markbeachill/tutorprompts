# Package Generator Design — v0.1

## Purpose

The package generator is intended to stop prompt-library drift. The master library and
mini-libraries should be built from the same reusable source blocks rather than edited
separately by hand.

This is a generator/tooling release, not a public website content release.

## Source and generated output

Human-edited source files live in:

```text
src/prompt-library/
```

Generated files are written to:

```text
docs/prompt-libraries/latest/
docs/prompt-libraries/v3.5/
```

The generator also rebuilds:

```text
docs/prompt-libraries/latest/ai_personal_tutor_mini_libraries.zip
```

## Current v0.1 structure

```text
src/prompt-library/
├─ header.md
├─ shared/
│  ├─ 01-global-rules.md
│  └─ 02-markdown-output-rules.md
├─ pack-sections/
│  ├─ master/
│  ├─ writing-tutor/
│  ├─ structure-tutor/
│  ├─ academic-thinking/
│  ├─ research-proposal/
│  └─ study-workflow/
├─ tools/
└─ packs/
```

## How packs work in v0.1

Each file in `src/prompt-library/packs/` defines one generated pack. It lists:

- the latest output file;
- the fixed archive output file;
- pack-specific sections such as manifest, launcher and router;
- the tool blocks to include;
- a footer/version-history block.

The generator concatenates:

1. `header.md`
2. pack manifest
3. shared global rules
4. shared Markdown output rules
5. pack launcher
6. pack router
7. included tool blocks
8. pack footer/version history

## Menu and metadata handling in v0.1

v0.1 preserves the existing hand-written menu, manifest and router blocks. It does not yet
generate these dynamically.

Tool text is shared from `src/prompt-library/tools/`. For mini-libraries, the script
removes `master_number` metadata and rewrites `menu_number` according to that mini-pack's
order.

## Known limitation: menu duplication

The current prompt-library format contains tool/menu information in several places:

- the available-tools table;
- the visible launcher menu;
- the router mapping;
- each tool metadata block.

v0.1 does **not** try to solve this. It keeps the current blocks intact so that the first
generator release is low-risk.

A later generator version should make tool metadata the source of truth and generate:

- available-tools tables;
- visible launcher menus;
- router mappings;
- pack-specific menu numbers.

## Suggested next stages

### v0.2

Generate repeated menu and router sections from canonical tool metadata.

### v0.3

Generate single-tool packs automatically.

### v0.4

Support user-defined custom packs from YAML pack manifests.

### v0.5

Add GitHub Actions checks so generated files cannot become stale.
