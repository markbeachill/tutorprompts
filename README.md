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

For a developer-focused guide to the prompt files and build workflow, see `BUILD_AND_GENERATOR_GUIDE.md`.

## Customising the prompt libraries

The official mini libraries are recommended for most users. Developers, teachers and departments who want a smaller or locally tailored library can start from the master library and delete down.

See:

- `BUILD_AND_GENERATOR_GUIDE.md` — where the source and generated files live, and how to rebuild them
- `CUSTOMISING_PROMPTS.md` — how to build a smaller custom library without duplicating files or weakening the core tutor-not-ghost-writer design

## Repository structure

The public website is published from the `docs/` folder.

```text
/
├── README.md
├── BUILD_AND_GENERATOR_GUIDE.md
├── PACKAGE_GENERATOR_START_HERE.md
├── CUSTOMISING_PROMPTS.md
├── SOURCE_MATERIAL_INDEX_EXPLAINER.md
├── src/
├── scripts/
├── docs/
│   ├── index.html
│   ├── where-to-start/
│   ├── tools/
│   ├── examples/
│   ├── student-help/
│   ├── guides/
│   ├── download/
│   ├── prompt-libraries/
│   └── audit-library/
└── roadmaps/archive/root-docs/
```

GitHub Pages can publish from the committed `docs/` folder, or from the optional GitHub Actions build workflow described in `BUILD_AND_GENERATOR_GUIDE.md`.

## Current public release

- Site package: v4.1
- Prompt-library suite: v4.1
- Testing/audit pack: v4.1

Detailed release notes are in `docs/changelog/site-update-notes/`.

## Discussion

Comments, questions and suggestions can be added in the repository discussions area:

https://github.com/markbeachill/tutorprompts/discussions


## Build instructions

See [`BUILD_AND_GENERATOR_GUIDE.md`](BUILD_AND_GENERATOR_GUIDE.md) for the consolidated library/page build workflow and release-version policy.
