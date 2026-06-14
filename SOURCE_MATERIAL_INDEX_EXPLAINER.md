# Source material index explainer

This file explains how the copy-ready source material area works, how the index page is built, and what to update when adding new material.

The source material library is separate from the prompt libraries. It is not a tutor prompt. It is a collection of example extracts, draft samples, student attempts and practice inputs that can be copied into the tools during testing, demonstration or teaching.

## What the source material index is

The public source material page is:

```text
docs/source-material/index.html
```

It displays each source item as a copy-ready card. Each card shows:

```text
- source material title
- related tool code, for example WT7 or ST4
- related tool title
- category, for example Writing Tutor or Structure Tutor
- when to use the material
- copy source text button
- download Markdown button
```

The page is linked from the guide index as a guide/resource item:

```text
docs/guides/index.html
docs/guides/index.alt.html
```

The link currently points to:

```text
docs/source-material/
```

You can move the link later if you decide the source material belongs somewhere else in the site navigation.

## Where source material is edited

Edit source material here:

```text
src/source-material/items/
```

Each item is a Markdown file with a front-matter block followed by the copy-ready source text.

Example structure:

```markdown
---
id: wt7-paraphrase-quotation-practice
title: WT7 paraphrase and quotation practice source
tool_code: WT7
tool_title: Paraphrase and Quotation Workshop
category: Writing Tutor
use_when: Use when testing whether a student paraphrase is too close, accurately attributed and safely integrated.
---
# WT7 paraphrase and quotation practice source

## Source extract

Paste the source material here.

## Student attempt

Paste the student attempt here.

## Student question

Paste the student question here.
```

The content after the second `---` is what appears in the public copy box and in the downloadable Markdown file.

## Required front-matter fields

Every source item must include these fields:

```text
id
title
tool_code
tool_title
category
use_when
```

### `id`

A stable machine-readable identifier. Use lowercase words separated by hyphens.

Good:

```text
wt7-paraphrase-quotation-practice
st4-reverse-outline-sample-draft
```

Avoid changing an existing `id` unless you intentionally want to change the generated Markdown filename and JSON entry.

### `title`

The public title shown on the source material card.

### `tool_code`

The tutor-tool code the material supports, for example:

```text
WT4
WT7
ST2
ST4
AT8
```

### `tool_title`

The human-readable tool name, for example:

```text
Teach Me This Mistake
Reverse Outline Mapper
Paraphrase and Quotation Workshop
```

### `category`

The broader library area, for example:

```text
Writing Tutor
Structure Tutor
Academic Thinking Tutor
```

### `use_when`

A short explanation of when a tutor, teacher or tester should use the source material.

## How the source material page is built

The generator script is:

```text
scripts/build_source_material_library.py
```

Run it from the repository root:

```bash
python scripts/build_source_material_library.py
```

This reads:

```text
src/source-material/items/*.md
```

and writes:

```text
docs/source-material/index.html
docs/source-material/latest/*.md
docs/data/source_material_index.json
```

## Check mode

To check whether the generated source material files are up to date without changing them, run:

```bash
python scripts/build_source_material_library.py --check
```

The full generator check also includes the source material check:

```bash
python scripts/run_generator_checks.py --build-first
```

Use that before committing or packaging a release.

## What gets generated

### `docs/source-material/index.html`

The public copy-ready index page. This is what users open in the browser.

### `docs/source-material/latest/*.md`

One downloadable Markdown file per source item. The filename is based on the item `id`.

### `docs/data/source_material_index.json`

A machine-readable index for future site features, search, filtering or generated navigation.

## How to add a new source item

1. Create a new Markdown file in:

```text
src/source-material/items/
```

2. Add the required front matter.

3. Put the copy-ready source text below the front matter.

4. Rebuild:

```bash
python scripts/build_source_material_library.py
```

5. Run the full checks:

```bash
python scripts/run_generator_checks.py --build-first
```

6. Commit both the source file and the generated outputs.

## What to commit after changing source material

When adding or editing source material, usually commit:

```text
src/source-material/items/<item>.md
docs/source-material/index.html
docs/source-material/latest/<item>.md
docs/data/source_material_index.json
```

If you rebuild the release/site package, also commit the relevant updated ZIP in:

```text
dist/
```

## Current source material examples

At the time this explainer was added, the source material library includes examples for:

```text
AT8 — Source Reliability Checker
ST2 — Whole-Work Structure Review
ST4 — Reverse Outline Mapper
WT7 — Paraphrase and Quotation Workshop
```

More can be added by creating additional Markdown files in `src/source-material/items/`.

## Design rule

Keep source material separate from prompt tools.

Prompt tools should define behaviour. Source material should provide realistic, copy-ready inputs for testing, demonstrations and classroom use. This keeps the master prompt library cleaner and makes examples easier to update without editing the tutor prompts themselves.

## Future improvement option

The current source material generator is intentionally simple: one Markdown file per source item.

A future version could add:

```text
- filtering by tool family
- filtering by difficulty or level
- tags such as citation, structure, grammar, source use
- direct links from individual tool pages to related source material
- a generated source-material navigation block on tool pages
```

For now, the reliable workflow is:

```text
edit src/source-material/items/*.md
run scripts/build_source_material_library.py
run scripts/run_generator_checks.py --build-first
commit source and generated files
```
