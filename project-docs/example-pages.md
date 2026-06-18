# Example pages: architecture and workflow

This note records how tool example pages are built and how to make new ones. It
is a maintainer note kept in `project-docs/`, not in the published `docs/` tree.

## Goal

Every tool in `docs/data/tool_index.json` (32 tools across WT, ST, AT, RP, SW)
has a worked example page at `docs/examples/example-{code}.html` showing a real
interaction.

## Architecture: snippet + wrapper, fed by a deterministic converter

The conversation content, the page furniture, and the conversion step are kept
separate:

```text
src/examples/{code}-example-chat.html         Hand-editable chat snippet (the content).
scripts/build_example_pages.py                 Wraps each snippet in page furniture.
docs/examples/example-{code}.html               Generated page (do not hand-edit).

src/examples-tools/collector-to-snippet.js      Deterministic converter (canonical source).
docs/create-examples/index.html                  One-stop page: cards + collector + in-browser converter.
docs/create-examples/example-cards.md            Hand-written example scenarios, Markdown (one per tool).
scripts/build_create_examples_page.py            Assembles the create-examples page from its sources.
```

A **snippet** is the complete chat region only — the `<div class="ai-chat-page">`
(or `<section>`) block and its `ai-chat-turn` bubbles, nothing else. No head,
nav, intro or footer. This is exactly the markup the converter produces, so a
converted record is saved as a snippet with no further translation.

## Why a converter, not the AI

The conversion from a chat transcript to `ai-chat-*` HTML is too detailed to
trust to a language model freehand, and we want byte-identical output every
time. So the AI never does the conversion. The flow is:

1. **Collect.** Run a clean, representative test session and paste the existing
   [output collector](../docs/testing-collector.html) prompt as the final
   message. The AI reproduces the chat as a Markdown test record (unchanged
   behaviour; the collector is not modified).
2. **Convert.** Paste that record into the
   [create-examples](../docs/create-examples/index.html) page. A deterministic
   JavaScript function parses the record and emits the snippet in your browser.
   Nothing is sent anywhere.
3. **Place.** Save the snippet where the page tells you, using the filename it
   gives: `src/examples/{code}-example-chat.html`.
4. **Build.** Run the example-pages build, then the site build.

The AI's only role is reproducing the chat (the same self-report the collector
already relies on); the format conversion is code.

## Example cards

`docs/create-examples/example-cards.md` holds one hand-written scenario per
tool: a clear, representative situation plus the input(s) to paste and a short
"shows" note. These are deliberately **not** the adversarial audit inputs —
examples are shop-window content, so the cards avoid decoys and traps.

The file is Markdown, so it edits without escaping (literal newlines and quotes
inside fenced input blocks). One card looks like:

```text
## WT2 — Clarity Clinic

**Scenario:** A student wants one vague sentence made clearer.

**Shows:** Clarity Clinic diagnoses the real problem and asks for a rewrite.

### Input

```
Can you help me make this clearer?

There are a number of elements that play a part in the outcome.
```
```

The code is read from the `##` heading (the title after the dash is just for
readers); `### Input 1`, `### Input 2`, ... give multi-turn inputs. The
create-examples page builder parses this file and **validates it**: it fails the
build with a clear message if a tool has no card, a card is missing its
scenario/shows/input, an input has no fenced block, or a code is unknown. The
audit/test cards remain separate and authoritative for testing.

## Workflow commands

```bash
# After saving the snippet from the converter:
python scripts/build_example_pages.py            # all pages
python scripts/build_example_pages.py --only WT1  # one
python scripts/build_site_pages.py                # refresh index + tool links
```

`build_site_pages.py` auto-detects any `example-{code}.html` via its
`example_exists()` helper and updates the examples-index status, the Tools page
and the Where-to-start "Example" buttons. No manual wiring.

### Checks

```bash
python scripts/build_example_pages.py --check              # non-zero if any page is stale (CI)
python scripts/build_create_examples_page.py --check         # non-zero if the create-examples page is stale
node src/examples-tools/test-collector-to-snippet.mjs        # converter unit tests
```

## The intro lead line

The page-intro `lead` sentence is editorial, not part of the chat. The converter
writes `<!-- lead: REPLACE ME WITH A ONE-LINE INTRODUCTION TO THIS EXAMPLE. -->`
at the top of every snippet. Edit that comment in the snippet to set the intro;
the build uses it and strips the comment from the page body. If left as the
placeholder, the placeholder text appears on the page until edited.

## The converter

`src/examples-tools/collector-to-snippet.js` is the canonical converter. It:

- parses the collector record's Metadata table and `### Turn N — Role` headers;
- reads each turn's verbatim fenced block;
- renders the bubble Markdown (headings, lists, blockquotes, tables, fenced
  code, inline bold/italic/code) to the `ai-chat-bubble` HTML used by examples;
- derives the tool code (from the Test code field, the record title, or the
  first tool heading) and suggests the snippet filename;
- returns warnings (e.g. missing code, missing fenced block) rather than
  guessing silently.

The create-examples page at `docs/create-examples/index.html` inlines a copy of
this exact code (along with the collector prompt and the example cards). If you
change the JS, re-run `scripts/build_create_examples_page.py` so the page does
not drift. Tests live in
`src/examples-tools/test-collector-to-snippet.mjs`.

## Title source

`code` and `title` for each page come from `docs/data/tool_index.json`, so page
titles cannot drift from the tool metadata.

## Provenance of the current snippets

- **WT2-WT7 (6):** extracted from the pre-existing hand-made example pages.
- **The other 26:** authored against the "What to look for" checklists in
  `docs/audit-library/latest/ai_tutor_toolkit_step_by_step_test_cards.md`. These
  are illustrative, not captured model output. Replacing any of them with a real
  captured-and-converted session is a content-only change.

ST4 has no test card; its snippet was authored from the tool description in
`tool_index.json`.

## Spot-check

The collector record is produced by the same AI that was tested, so it is
self-reported. Compare at least one turn of the snippet against the live chat
before committing, exactly as for an audit record.

## Standardisation

Generated pages share one head/nav/footer and use `css/aichat.css`. Each
snippet's own chat-region wrapper (`<div>` or `<section>`) is preserved as
written, since the snippet is the source of truth for the chat.
