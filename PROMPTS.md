# Prompt libraries

This file is for developers, teachers, departments and maintainers who want to understand where the AI Personal Tutor Toolkit prompt files live and how they are structured.

Most students should use the live website and the official toolkit downloads without editing them.

## Where the prompt files live

The current public prompt libraries are stored inside the public site folder:

- `docs/prompt-libraries/latest/`

Versioned prompt-library archives are stored in:

- `docs/prompt-libraries/v2.1/`
- `docs/prompt-libraries/v2.2/`
- `docs/prompt-libraries/v2.3/`
- `docs/prompt-libraries/v2.4/`
- `docs/prompt-libraries/v2.5/`
- `docs/prompt-libraries/v3.0/`

They live inside `docs/` because GitHub Pages is configured to publish the live website from the `/docs` folder. The live download links use these same files.

Do not duplicate prompt files at the repository root. Update the files in `docs/prompt-libraries/latest/` and then create or update versioned archive folders when making a release.

## Current prompt libraries

The current public prompt-library suite is v3.0.

The main files are:

- `01_writing_tutor_library.md`
- `02_structure_tutor_library.md`
- `03_academic_thinking_tutor_library.md`
- `04_research_proposal_tutor_library.md`
- `05_study_workflow_tutor_library.md`
- `ai_personal_tutor_master_library.md`

The master library contains all tools. The five mini libraries contain related groups of tools.

## v3.0 design direction

v3.0 adds the paragraph-first tutor style, manageable feedback, the “I'm stuck” support model, the writing-is-thinking principle, scope clarification, and plain-English grammar-term guidance.

The design brief is stored at `V3_DESIGN_BRIEF.md`.

## How a mini library is structured

A mini library is not just a list of prompts. It is a controlled prompt environment. Its job is to load shared rules, show a menu, route the student to the right tool, and keep the AI within learning-focused boundaries.

A typical mini library contains:

1. **Release stamp** — site, prompt-library and testing-pack version information.
2. **Purpose statement** — what the library is for.
3. **Global rules** — the rules every tool must follow, including authorship, privacy, accuracy, UK English and learning-focused behaviour.
4. **Menu behaviour** — what the AI should show when the user types `prompt`.
5. **Tool list** — the included tools and their stable tool codes.
6. **Tool instructions** — detailed instructions for each tool.
7. **Output formats** — the expected structure for each tool's response.
8. **Follow-up rules** — how the AI should behave after the first response.
9. **Return-to-menu instruction** — a way to reset the interaction if the model drifts.

## Customising prompt libraries

The official mini libraries are recommended for most users. Developers, teachers and departments who want a smaller or locally tailored library can start from the master library and delete down.

Use this method rather than building from scratch:

1. copy the master library;
2. remove the tool blocks you do not need;
3. trim the menu, manifest and router so they match;
4. add local rules in one place;
5. restamp the file;
6. test it before sharing it with students.

See `CUSTOMISING_PROMPTS.md` for the detailed interim customisation guide.

## Global, library-level and tool-specific customisation

Customisation can happen at different levels.

**Global customisation** applies to the whole custom library. Examples include local AI-use rules, privacy rules, course level, discipline, referencing style or institutional expectations.

**Library-level customisation** applies to one mini library. For example, a writing-focused custom library may prioritise student voice and clarity before grammar polish.

**Tool-specific customisation** applies to one tool only. This is more powerful but riskier, because it can alter the behaviour of individual tools in subtle ways. Treat this as an advanced option.

For now, the recommended interim approach is to add local rules once, at the end of the master library's `01-global-rules` section, rather than editing every tool block.

## Migration guidance

When a new official version is released, rebuild customised libraries from the new master library.

Do not copy old core rules forward over newer official rules. Copy only your local customisation block into the new version, then test again.

## Testing customised libraries

Before recommending a customised library to students, test that:

- typing `prompt` shows only the intended tools;
- each kept tool routes correctly by number and code;
- deleted tools are not offered;
- authorship boundaries still hold;
- privacy warnings still appear when relevant;
- local rules are followed;
- the AI still behaves like a tutor, not a ghost-writer.

The testing/audit files live in:

- `docs/audit-library/latest/`

## Future development

Possible future developer support could include:

- a formal custom mini-library template;
- a custom instructions template for AI project spaces;
- a tool-block template;
- one-tool extracts if there is enough demand.

These are not needed for ordinary student use.


## Why global rules are repeated

Each mini library repeats the global rules, Markdown output rules, launcher and router because students may upload only one file to an AI tool. Each file therefore needs to work on its own.

This creates some maintenance duplication. When global rules change, maintainers must update the master library and each affected mini library, then rebuild the latest and versioned release folders.

Privacy warnings are also repeated intentionally because each mini library must work as a standalone uploaded file.
