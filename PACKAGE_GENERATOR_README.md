# AI Personal Tutor Package Generator v0.1

This is a first-stage package generator for the AI Personal Tutor Toolkit prompt libraries.
It is **not** a new website release. It is a repository tool that should be extracted into
the root of the GitHub repository.

## What v0.1 does

- Adds `src/prompt-library/` as the source area for prompt-library blocks.
- Adds pack manifests for the master library and the five mini-libraries.
- Adds `scripts/build_prompt_libraries.py`.
- Rebuilds:
  - `docs/prompt-libraries/latest/ai_personal_tutor_master_library.md`
  - `docs/prompt-libraries/latest/01_writing_tutor_library.md`
  - `docs/prompt-libraries/latest/02_structure_tutor_library.md`
  - `docs/prompt-libraries/latest/03_academic_thinking_tutor_library.md`
  - `docs/prompt-libraries/latest/04_research_proposal_tutor_library.md`
  - `docs/prompt-libraries/latest/05_study_workflow_tutor_library.md`
  - matching fixed archive copies under `docs/prompt-libraries/v3.5/`
  - `docs/prompt-libraries/latest/ai_personal_tutor_mini_libraries.zip`

## What v0.1 deliberately does not do yet

- It does not yet generate menus dynamically from tool metadata.
- It does not yet generate single-tool packs.
- It does not yet generate custom packs.
- It does not yet update site pages, changelog files or release manifests.
- It does not yet automate GitHub Actions.

Those are intended later stages.

## How to use

From a clean local repository:

```bash
python scripts/build_prompt_libraries.py
```

Then inspect the result:

```bash
git status
git diff
```

To check whether generated files are current without changing files:

```bash
python scripts/build_prompt_libraries.py --check
```

## Source-of-truth rule

In this v0.1 generator, edit the source blocks in:

```text
src/prompt-library/
```

Then rebuild the generated Markdown files. Avoid editing generated files under
`docs/prompt-libraries/latest/` directly unless you intend to copy the same change back
into the source blocks.

## Important v0.1 note

The master tool blocks are the canonical tool text. When building mini-libraries, the
script removes `master_number` metadata and rewrites `menu_number` to match that mini-pack's
local order. This keeps the tool body shared while preserving the current mini-library
format.
