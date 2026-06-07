# Customising prompt libraries

A short guide for developers, teachers and departments who want to build a smaller, tailored prompt library from the master library — and add their own local rules — without breaking the core *tutor, not ghost-writer* design.

This guide is for confident users. Most students should use the official mini libraries or the master library without editing them.

**Based on:** AI Personal Tutor Master Prompt Library v3.0
**Approach:** start from the master library and **delete down**. Do not build a new library from scratch.

---

## The one big idea

The simplest reliable way to make a custom library is to **take the master library, remove the tools you do not want, and add your local rules in one place.**

You are not writing anything new. Everything you keep already works together. You only:

1. delete the tool blocks you do not need,
2. trim the menu so it matches,
3. add your local rules to the global-rules section.

That is the whole method. The rest of this guide is detail and one worked example.

---

## When not to customise

Do not customise the library if you only need ordinary student use. Use the official mini libraries instead.

Do not customise by removing authorship, privacy, accuracy or learning-focused rules.

Do not customise a library for assessed work without checking your course or institution rules.

Do not give a customised library to students until you have tested it.


## Before you start: how the file is built

Open `ai_personal_tutor_master_library.md`. It is one file made of marked sections. Each section is wrapped like this:

```text
<!-- FILE: clarity-clinic.md -->
...section content...
<!-- END FILE -->
```

There are two kinds of section.

**1. Shared scaffolding — keep all of it.** These sections make every tool behave. Do not delete them:

| Section marker | What it does |
|---|---|
| `00-manifest` | Front matter, operating instructions, and a table of all tools |
| `01-global-rules` | The rules every tool obeys: authorship, privacy, precision, UK English. **This is also where your custom rules go.** |
| `02-markdown-output-rules` | How `create md` output is formatted |
| `03-launcher` | The welcome screen and the numbered menu the student sees |
| `04-router` | Maps the student's choice (number or code) to the right tool |

**2. Tool blocks — keep only the ones you want.** There are 27, each a self-contained `<!-- FILE: ... -->` unit with its own front matter (`tool_code`, `menu_number`). Examples: `clarity-clinic` (WT1), `find-mistakes` (WT3), `revision-plan` (SW1).

### The one trap to watch

The menu of tools appears in **three** places, and they must always agree:

1. the **`00-manifest`** "Available tools" tables,
2. the **`03-launcher`** numbered list (what the student sees),
3. the **`04-router`** number-routing table.

If you delete a tool from one place but leave it in another, the AI gets contradictory instructions and may route to a tool that no longer exists. **Every time you remove or reorder a tool, fix all three.** This is the single most common way a custom library breaks.

---

## The method, step by step

### Step 1 — Copy the file and rename it

Work on a copy so the master stays intact.

```text
ai_personal_tutor_master_library.md  →  first_year_writing_support_library.md
```

### Step 2 — Decide which tools to keep

Pick from the 27 by tool code. Write the list down before you start cutting.

### Step 3 — Delete the tool blocks you do not want

For each unwanted tool, delete everything from its `<!-- FILE: ... -->` line to its matching `<!-- END FILE -->` line, inclusive. Leave the shared scaffolding untouched.

A shorter file is not just tidier — on free AI plans it behaves more reliably, because there is less for the model to wade through.

### Step 4 — Trim the menu in all three places

Now make the three lists match the tools you kept (see "the one trap" above). Remove the lines for deleted tools from:

- the `00-manifest` tool tables,
- the `03-launcher` numbered list,
- the `04-router` number-routing table and its natural-language routing hints.

### Step 5 — Renumber (optional)

If you want a different menu order, renumber the **menu numbers** (1, 2, 3...) in the launcher, manifest and router so they stay in sync.

**Keep the original tool codes** (WT1, WT5, SW1). The codes are how a tool is traced back to the official library, and they make version updates far easier. So menu item 3 can be `WT5`; that is fine and expected. Change the position, not the code.

### Step 6 — Add your local rules in ONE place

Open `01-global-rules`. At the **end** of that section, just before its `<!-- END FILE -->`, add a clearly marked block:

```markdown
## Local customisation

The following rules are added locally for this course or institution.
They add to the rules above. They do not override the academic-integrity,
privacy, accuracy or learning-focused rules in this section.

[Add your local context, assessment rules, privacy rules, and writing
expectations here.]
```

Why here? Because `01-global-rules` is applied to every tool and sits above all the tool blocks — exactly where standing rules belong. You add your rules in one spot and they reach every tool. You never edit individual tool blocks for this.

**Be honest about what this does.** The "do not override" line is an instruction to the AI, not a lock. AI tools do not run Markdown like software, so a customised file can still drift — especially on free plans. The only real check is to test the file (Step 8).

### Step 7 — Update the release stamp

Near the top of the file (`00-manifest`), note what you based it on and that it is a local build:

```markdown
**Local build:** First-Year Writing Support Library
**Based on:** AI Personal Tutor Master Prompt Library v3.0
**Maintained by:** [your name / department]
```

This is what lets you migrate cleanly later: when a new master version ships, you rebuild from it and re-apply only your "Local customisation" block — you never copy old core rules forward over new ones.

### Step 8 — Test before you hand it to students

Upload the finished file to the AI tool you expect students to use and check:

- Typing `prompt` shows **only** your chosen tools, correctly numbered.
- Each kept tool runs when chosen by number and by code.
- No deleted tool is offered or routes to anything.
- The AI still refuses to rewrite assessed work.
- The privacy reminder still appears when relevant.
- Your local rules are followed.
- It still behaves like a tutor, not a ghost-writer.

If any check fails, the usual cause is a menu left out of sync across the three places in Step 4.

---

## Worked example: a 5-tool First-Year Writing Support library

**Goal:** a small library for first-year undergraduates, focused on clarity, mistakes and revision. No research-proposal or advanced thinking tools.

**Tools kept (5 of 27):**

| New menu | Code | Tool |
|---:|---|---|
| 1 | WT1 | Clarity Clinic |
| 2 | WT3 | Find My Mistakes |
| 3 | WT4 | Teach Me This Mistake |
| 4 | WT5 | Style and Clarity Review |
| 5 | SW1 | Revision Plan |

Note that the codes are not 1–5; they are the original codes, renumbered only by menu position. That is intentional (Step 5).

**What you delete:** the 22 tool blocks for WT2, WT6, all ST, all AT, RP1–RP5, SW2, SW3.

**What the trimmed `03-launcher` menu looks like:**

```markdown
Choose one option, or describe what you need.

1. **WT1 — Clarity Clinic** — improve one sentence, a few sentences, or one paragraph.
2. **WT3 — Find My Mistakes** — identify grammar, logic, clarity, factual, spelling, punctuation and referencing problems.
3. **WT4 — Teach Me This Mistake** — learn from mistakes identified by Find My Mistakes.
4. **WT5 — Style and Clarity Review** — improve readability, tone and style without rewriting the assignment.
5. **SW1 — Revision Plan** — turn feedback into a revision plan.

You can type `prompt` at any time to return to this menu.
```

**What the trimmed `04-router` number table looks like:**

```markdown
| Student choice | Code | Tool ID |
|---:|---|---|
| 1 | `WT1` | `clarity-clinic` |
| 2 | `WT3` | `find-mistakes` |
| 3 | `WT4` | `teach-mistake` |
| 4 | `WT5` | `style-clarity-review` |
| 5 | `SW1` | `revision-plan` |
```

(Trim the manifest tables and the router's natural-language hints the same way.)

**The local rules added at the end of `01-global-rules`:**

```markdown
## Local customisation

The following rules are added locally for this course.
They add to the rules above. They do not override the academic-integrity,
privacy, accuracy or learning-focused rules in this section.

- Students are first-year undergraduate sociology students unless they say otherwise.
- This library is for formative feedback on drafts only. Students must not use
  AI to generate final submission wording.
- Use Harvard referencing terminology.
- Prioritise clarity of argument and paragraph meaning before sentence-level polish.
```

That is the whole build: delete 22 blocks, sync three menus, add one local block, restamp, test.

---

## Quick reference card

```text
1. Copy + rename the master library.
2. List the tools to keep.
3. Delete the <!-- FILE --> … <!-- END FILE --> block for each unwanted tool.
4. Trim the menu in ALL THREE places: manifest, launcher, router.
5. (Optional) Renumber menu order. KEEP original tool codes.
6. Add local rules ONCE, at the end of 01-global-rules.
7. Update the release stamp.
8. Test: menu correct, tools route, authorship + privacy intact, behaves like a tutor.
9. When a new official version is released, rebuild from the new master file. Do not copy old core rules forward.
```

**Golden rules**

- Keep all shared scaffolding (`00`–`04`). Only delete tool blocks.
- The menu lives in three places — they must always match.
- Keep original tool codes; change only the menu position.
- Local rules add to the core rules; they never replace them.
- A customised file is not tested until you have tested it.
