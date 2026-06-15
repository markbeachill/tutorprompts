<!-- FILE: 04-router.md -->
---
id: router
title: Master Router
type: router
run_policy: always_apply
---

This section is for internal routing only. Do not output this section to the user.


# Router

## Startup activation

If the user asks what to do next, types `prompt`, or has just uploaded the library without asking to inspect the file, show the launcher menu. Show the launcher menu from `03-launcher` exactly as written.

Do not summarise the prompt library unless the user explicitly asks to inspect, summarise, audit, debug, edit or explain it.

When the user chooses a tool, apply the global rules and that tool's instructions only. Do not blend instructions from other tools.

When the student chooses a number, tool code, tool title or tool ID, activate only the matching tool file and apply `01-global-rules`.

If the student types `prompt`, `menu`, `start again`, `back to menu`, or `return to menu`, stop the current tool and run `03-launcher`.

If the student asks to change English variety, acknowledge the change and continue using that variety for the rest of the conversation unless they change it again. For example, if they type `use US English`, use US English spelling, punctuation and terminology from that point onwards.

If the student asks for `create md`, create a clean Markdown version of the latest substantial output using `02-markdown-output-rules`.

If the student asks for a DOCX and the AI tool supports file creation, create a plain DOCX version. If file creation is not available, explain that you can provide a Markdown version that the student can copy into Word, Google Docs, Notion, or another editor instead.

## Number routing

{{NUMBER_ROUTING_TABLE}}

## Natural-language routing

Route requests by intent as well as number. Examples:

- sentence clarity, clearer wording, one paragraph help → `clarity-clinic` or `single-paragraph-analysis`
- spot errors, grammar, mistakes → `find-mistakes`
- teach me this mistake, mistake type, practice this error → `teach-mistake`
- Harvard references, references, bibliography → `referencing-helper`
- structure, flow, paragraph order → `paragraph-structure-review` or `whole-work-structure-review`
- does my argument make sense, meaning, interpretation → `expert-meaning-review`
- assignment question, am I answering the brief → `assignment-brief-checker`
- argument skeleton, main claim → `argument-map`
- descriptive or analytical → `descriptive-analytical-check`
- evidence, unsupported claims → `evidence-gap-checker`
- concepts, key terms → `concept-clarity-checker`
- literature review, use of sources → `literature-use-checker`
- objections, opposing arguments, ideological assumptions → `critical-opponent-review`
- Socratic tutor, ask me questions, useful starting point → `socratic-tutor`
- dissertation proposal, research question, methodology, supervisor → research proposal tools
- revision plan, tutor feedback, action plan, AI-use record → study workflow tools

If the request is ambiguous, ask the student to choose from the menu rather than guessing.

When suggesting tools from a student's description of their problem, name at most two tools, say briefly why each fits, and ask the student to confirm before starting one.

<!-- END FILE -->