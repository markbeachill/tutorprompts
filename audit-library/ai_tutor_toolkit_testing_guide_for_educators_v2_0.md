# Testing Guide for Educators v2.0

This guide explains how to test the AI Personal Tutor Toolkit without needing technical testing knowledge.

## Why test the toolkit?

The toolkit is made of prompts. Prompts are not software. Different AI systems may follow them differently, especially on free plans. Testing helps you see whether the toolkit behaves well enough for students and where the wording needs improvement.

## What you are testing

You are not trying to prove that the toolkit is perfect. You are checking whether it usually:

- gives feedback rather than writing the assignment
- helps students learn
- follows the chosen tool
- avoids fake references or false certainty
- explains things clearly
- handles vague or risky requests sensibly

## The simplest testing workflow

1. Choose a test card.
2. Open a new AI chat.
3. Upload the relevant prompt library.
4. Type `prompt`.
5. Choose the tool named on the card.
6. Paste the test input from the card.
7. Save the AI output using the suggested filename.
8. Open a new AI chat.
9. Upload or paste the audit prompt.
10. Choose the matching audit code.
11. Paste the saved output.
12. Save the audit report.
13. Decide whether the prompt needs editing.

## What to save

Save two files for each test:

```text
wt1_clarity_clinic_test_output_v1_6.md
wt1_clarity_clinic_audit_v1_6.md
```

The first file is what the toolkit produced. The second file is the audit of that output.

## Minimum test run before sharing a new version

If you are short of time, run these tests:

- U1 Menu return
- U2 Language setting
- U3 Ambiguous request
- A1 Direct cheating request
- WT1 Clarity Clinic
- WT3 Find My Mistakes
- WT5 Style and Clarity Review
- AT9 Critical Opponent Review
- AT10 Socratic Tutor
- RP3 Critical Research Supervisor Review
- SW1 Revision Plan

## Smoke tests in plain English

A smoke test is a quick check that the basics work. It does not test everything. It checks whether the menu appears, whether a simple input works, and whether the AI avoids doing something obviously wrong.

## Regression tests in plain English

A regression test checks that something fixed in an earlier version has not broken again. Run regression tests after editing prompt wording.

## Adversarial tests in plain English

An adversarial test checks what happens when someone asks for something risky, vague or against the purpose of the toolkit. These tests are important because students do not always ask neat questions.

## How to judge results

Use the audit rating, but also use your judgement. A pass does not mean the tool is perfect. A minor issue may simply mean the wording could be clearer. A major or critical issue usually means the prompt needs editing before sharing.

## Common problems to watch for

- The model rewrites too much.
- The model ignores the chosen tool.
- The model gives a full essay paragraph rather than feedback.
- The model invents source details.
- The model asks too many questions in Socratic or viva mode.
- The model gives a long generic lecture instead of practical guidance.
- The model forgets the privacy/responsibility note.

## Suggested folder for test results

```text
test-results/
├── v1_6/
│   ├── wt1_clarity_clinic_test_output_v1_6.md
│   ├── wt1_clarity_clinic_audit_v1_6.md
│   └── ...
```

## Final release checklist

Before publishing a new version, check:

- All download links point to the current version.
- Menus use the correct tool codes.
- The privacy and responsibility note is present.
- The language setting rule is present.
- The “AI behaviour and limits” note is present.
- The referencing and source-checking tools do not encourage guessing.
- The testing page links to the current testing pack.
