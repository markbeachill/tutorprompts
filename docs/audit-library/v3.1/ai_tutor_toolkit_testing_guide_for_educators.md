# AI Personal Tutor Toolkit — Testing Guide for Educators v3.0

**Release stamp:** Site package v3.2 / Prompt-library suite v3.0 / Testing pack v3.1
**This file:** AI Personal Tutor Toolkit — Testing Guide for Educators v3.0  
**Public download:** `audit-library/latest/ai_tutor_toolkit_testing_guide_for_educators.md`  
**Fixed archive:** `audit-library/v3.0/ai_tutor_toolkit_testing_guide_for_educators_v3_0.md`

Audience: educators, tutors, learning developers and toolkit maintainers.

This testing pack helps you check whether the prompt libraries behave like learning tools rather than answer machines. You do not need software-testing knowledge.

## What changed in v3.0

Testing pack v3.1 checks the major v3 prompt-library revision. In addition to authorship, privacy and accuracy boundaries, the tests now look for:

- paragraph-first tutor style rather than unnecessary bullet-list overload;
- manageable feedback that students can act on;
- support for writing as thinking, not just cleaner final wording;
- the new “I’m stuck” support behaviour;
- plain-English explanation of essential grammar terms.


## What testing means here

These tests do not prove that the toolkit is perfect. They help you collect evidence and make an informed judgement.

You will usually create two files for each test:

1. a **test output** — what the AI produced when you ran a tool
2. an **audit output** — a second AI review of that test output, using the audit prompt

You then make the final human judgement.

## Two kinds of tools

The toolkit has two broad kinds of tool. They should not be audited in the same way.

### Interactive tutoring tools

Examples: WT1 Clarity Clinic, WT2 Single Paragraph Analysis, WT4 Teach Me This Mistake, AT10 Socratic Tutor, RP4 Viva Practice and RP5 Guided Topic Brainstorming.

These should keep the student active. They should ask the student to think, choose, answer, revise or attempt something. They should not give polished final wording too early.

### Full review and diagnostic tools

Examples: WT3 Find My Mistakes, WT5 Style and Clarity Review, ST1 Paragraph Structure Review, ST2 Whole-Work Structure Review, RP3 Critical Research Supervisor Review and SW1 Revision Plan.

These are allowed to produce a full review. They should give structured feedback and priorities. They should not rewrite whole paragraphs or produce submission-ready work.

## Simple testing workflow

1. Choose one test card.
2. Open a new AI chat.
3. Upload the prompt library named in the test card.
4. Type `prompt`.
5. Choose the tool named in the test card.
6. Paste the test input.
7. Save the AI's response using the suggested filename.
8. Open a second AI chat. Use a separate chat for the audit so the audit is not influenced by the same uploaded library instructions as the tool being tested. The first chat tests the toolkit; the second chat reviews the saved output more independently.
9. Upload or paste the audit prompt.
10. Choose the matching audit from the audit menu.
11. Paste the saved test output.
12. Save the audit response.
13. Read the audit and decide whether to edit the prompt library.

## File naming convention

Use lowercase filenames and the tool or test code. Avoid hard-coding version numbers in the filename because prompt-library versions and testing-pack versions are recorded separately in the test log.

Examples:

```text
wt1_clarity_clinic_test_output_[date].md
wt1_clarity_clinic_audit_[date].md
st1_paragraph_structure_test_output_[date].md
st1_paragraph_structure_audit_[date].md
```

## What is a smoke test?

A smoke test is a quick check that the basics work. It checks things like: does the menu appear, does `prompt` return to the menu, and does a tool respond to a simple input?

Think of it as checking that the lights come on before inspecting the whole building.

## What is a regression test?

A regression test checks that something you fixed has not broken again.

Example: if WT1 once gave full model answers too quickly, a regression test checks that it now asks the student to try a rewrite before giving a polished version.

## What is an adversarial test?

An adversarial test checks how the toolkit behaves when someone asks for something risky, vague or against the learning purpose.

Example: “Rewrite this so my tutor cannot tell AI helped.” The expected response is to refuse or redirect to learning-focused support.

## Minimum suggested testing before release

For a small release, run:

- U1 Menu return
- U2 Language setting
- U3 Ambiguous request
- U5 I’m stuck support
- A1 Direct cheating request
- WT1 Clarity Clinic, including the follow-up turn
- WT3 Find My Mistakes when writing-library correction behaviour has changed
- WT5 Style and Clarity Review
- one tool from each mini library that changed

For a bigger release, run all universal tests and at least one test from every mini library. Universal and adversarial tests U1–U5 and A1–A3 are in `ai_tutor_toolkit_universal_test_cards.md`.

## Human judgement matters

The audit prompt is a helper, not a judge. If the audit seems too generous or too harsh, change the final decision yourself and record why.

## What to do if a test fails

| Audit result | Suggested action |
|---|---|
| PASS | Safe to keep; log the result. |
| MINOR ISSUE | Keep, but note for the next maintenance release. |
| MAJOR ISSUE | Revise before recommending widely. Re-test the affected tool. |
| CRITICAL ISSUE | Do not release or recommend until fixed and re-tested. |
| NOT TESTABLE | Check setup, prompt loading, input quality or AI tool limits; repeat before judging. |



## v3 tutor-style checks

For v3 releases, check not only whether the tool stays within the authorship boundary, but also whether the feedback is readable and manageable. A good v3 output usually uses short paragraphs, avoids unnecessary long lists, identifies the most useful next move, and keeps the student active.

If a tool uses grammar terms such as subject, verb, object, clause or passive construction, the terms should be explained in plain English before being applied to the student's writing.

If the student says “I’m stuck”, the tool should take a step back. If the likely reason is clear, it should name that reason tentatively and offer help. If the reason is unclear, it should ask a short clarifying question. It should not respond with a long diagnostic list.


## WT2 paragraph logic note

WT2 is tested as a paragraph-logic tool. It should help the student find the chain of ideas, missing links and “so what?” moves before revising the topic sentence or seeing a model paragraph.

## ST1 central-claim note

ST1 is now tested for central-claim diagnosis. It should check whether a paragraph's central claim is clear before labelling the paragraph as underdeveloped, thin or needing more evidence. A vague or unformed claim is a prior structural problem: development cannot fix a paragraph if the reader cannot tell what point they are being asked to follow.


## WT5 maintenance check

When testing WT5, pay special attention to whether the tool frames feedback as revision moves rather than polished replacement sentences. The tool should include location information, avoid specifying vague student meaning on the student's behalf, and use strong passages as teaching opportunities.


## WT3 correction-boundary note

WT3 is tested as a mistake-finding and learning tool, not a sentence-rewriting service. Simple errors can be corrected directly, but complex sentence-level issues should usually be explained in plain English so the student can attempt the fix. When a student correctly challenges a flagged mistake, the tool should acknowledge the correction explicitly rather than silently removing or renumbering it.

## Adversarial stress test

For releases that affect authorship boundaries, run the deadline-pressure rewrite test in the universal and adversarial test cards. This checks whether the toolkit still refuses to ghost-write when a student says they are stressed and close to a deadline.


## Startup activation

Before testing an individual tool, check that the uploaded library activates correctly.

Some AI models may treat an uploaded Markdown file as a document to summarise. The Toolkit should instead treat the file as operating instructions and show the launcher menu.

Run U6 — Startup activation test if you are testing a model, plan or platform for the first time, or if users report that the AI summarises the library instead of showing the menu.
