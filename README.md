# AI Personal Tutor Toolkit

The AI Personal Tutor Toolkit is a set of prompt libraries that help students use AI as a tutor, not as a ghost-writer.

The prompts are designed to give structured, specialist writing support: focused feedback, plain explanation, practice and revision guidance while students keep responsibility for their own writing and thinking. The v4 release consolidates the teaching loop across the toolkit, updates tool behaviour, improves routing and testing, and keeps the focus on writing as thinking rather than AI-generated submission text.

Live website: https://markbeachill.github.io/tutorprompts/

## What the toolkit helps with

- Writing clarity, style and repeated mistakes.
- Paragraph and whole-draft structure.
- Academic argument, evidence and concept clarity.
- Research proposal development.
- Revision planning and AI-use records.

## How students use it

1. Open the live website.
2. Choose a toolkit file.
3. Upload or paste it into an AI tool.
4. Type `prompt`.
5. Choose the help they need.

The toolkit files are provided as plain Markdown prompt libraries because that makes them easy for AI tools to read. Students do not need to understand Markdown to use the toolkit.

## For educators

The toolkit offers a structured way to guide independent student AI use. It is not a replacement for assessment rules, teacher judgement, institutional policy or student responsibility.

Educators can inspect the prompts, test them, adapt them for local teaching contexts, and use the testing pack before recommending a version to students.

## Where are the prompt files?

The prompt libraries are stored inside the public site folder:

- `docs/prompt-libraries/latest/`

They live there because GitHub Pages publishes the website from `/docs`, and the live download links use those files directly.

For a developer-focused guide to the prompt files and customisation, see `PROMPTS.md`.

## Customising the prompt libraries

The official mini libraries are recommended for most users. Developers, teachers and departments who want a smaller or locally tailored library can start from the master library and delete down.

See:

- `PROMPTS.md` — where the prompt files live and how the libraries are structured
- `CUSTOMISING_PROMPTS.md` — how to build a smaller custom library without duplicating files or weakening the core tutor-not-ghost-writer design

## Repository structure

The public website is published from the `docs/` folder.

```text
/
├── README.md
├── PROMPTS.md
├── CUSTOMISING_PROMPTS.md
├── V3_DESIGN_BRIEF.md
└── docs/
    ├── index.html
    ├── tools/
    ├── examples/
    ├── student-help/
    ├── guides/
    ├── changelog/
    ├── prompt-libraries/
    ├── audit-library/
    └── release_manifest.md
```

GitHub Pages should be configured to publish from the `docs/` folder on the main branch.

## Current public release

- Site package: v4.0
- Prompt-library suite: v4.0
- Testing/audit pack: v4.0

Detailed release notes are in `docs/changelog/site-update-notes/`.

## Discussion

Comments, questions and suggestions can be added in the repository discussions area:

https://github.com/markbeachill/tutorprompts/discussions
