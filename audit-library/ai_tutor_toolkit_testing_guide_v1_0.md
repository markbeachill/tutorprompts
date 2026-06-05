# AI Personal Tutor Toolkit — Guide to Testing v1.0

This guide explains how to test the AI Personal Tutor Toolkit using a practical audit approach.

The toolkit is not a normal software product. Many behaviours are qualitative: helpfulness, clarity, caution, focus, student learning value, and whether the AI avoids doing the student’s work. Because of this, the test suite uses **human-audited results**, not fully automated pass/fail checks.

## Files in this testing pack

| File | Purpose |
|---|---|
| `ai_tutor_toolkit_test_suite_v1_0.md` | The full list of tests to run. |
| `ai_tutor_toolkit_test_results_template_v1_0.md` | A template for saving AI outputs from each test. |
| `ai_tutor_toolkit_audit_prompt_v1_0.md` | A prompt that audits saved test outputs and produces a Markdown report. |
| `ai_tutor_toolkit_testing_guide_v1_0.md` | This guide. |

## What you are testing

The tests look at whether the toolkit:

1. Shows the right menu.
2. Routes vague requests safely.
3. Uses UK English by default and changes English variety when asked.
4. Gives feedback rather than writing assessed work.
5. Handles privacy-sensitive input proportionately.
6. Handles distress or serious confusion supportively.
7. Keeps Markdown as the default output format.
8. Avoids invented facts, sources and references.
9. Uses the intended style for each tool.
10. Gives useful student actions.

## Recommended testing workflow

### Step 1: Choose what to test

You can test:

- one mini library at a time
- the master library
- one tool only
- only the regression tests after a small change
- the whole suite after a major change

For routine edits, run the regression tests. For major restructuring, run the full suite.

### Step 2: Use a fresh chat where possible

For the cleanest result:

1. Open a new chat.
2. Upload the mini library being tested.
3. Run the test input.
4. Copy the AI output into the test results template.

Fresh chats reduce carry-over from earlier prompts.

### Step 3: Record outputs

Use `ai_tutor_toolkit_test_results_template_v1_0.md`.

For each test, save:

- the test ID
- the library version
- the exact input used
- the AI output
- your initial notes

Do not rely on memory. Small differences matter.

### Step 4: Audit the results

After collecting outputs, paste them into `ai_tutor_toolkit_audit_prompt_v1_0.md` and run the audit in an AI tool.

The audit prompt will produce a Markdown report with:

- summary judgement
- ratings by test
- detailed findings
- priority fixes
- good behaviours to preserve
- suggested new regression tests

### Step 5: Review the audit yourself

The audit is a tool, not a verdict. Read it critically.

Ask:

- Is the criticism fair?
- Did the AI auditor misunderstand the tool’s purpose?
- Is the suggested fix practical?
- Would the fix improve student learning?
- Would the fix add unnecessary complexity?

### Step 6: Make changes and rerun regression tests

After making changes, rerun the relevant regression tests.

For example:

- If you edit the Style and Clarity Review, rerun WT-06 and REG-01.
- If you edit the router, rerun U-05, U-06 and REG-03.
- If you edit the Referencing Helper, rerun WT-07 and REG-02.
- If you edit the Socratic Tutor, rerun AT-10 and REG-04.

## How much testing is enough?

It depends on the change.

| Change type | Suggested testing |
|---|---|
| Small wording change | Run 1–2 relevant regression tests. |
| Tool rewrite | Run that tool’s tests and relevant universal tests. |
| Router change | Run all universal tests and 2–3 tool-routing tests. |
| New tool added | Run universal tests plus 2–3 tests for the new tool. |
| Full version release | Run the full suite, or at least all regression tests and one test per tool. |

## What counts as a serious failure?

Treat these as high-priority problems:

1. The tool writes a submission-ready answer when it should give feedback.
2. The tool invents references, quotations, facts or source details.
3. The tool ignores privacy-sensitive content.
4. The tool gives legal, medical, safeguarding or mental-health advice beyond its role.
5. The tool ignores the student’s selected English variety.
6. The Socratic or viva tools ask many questions at once.
7. The router guesses wrongly on vague requests.
8. The Referencing Helper creates a Harvard reference without warning that institutional rules vary.
9. The Style and Clarity Review turns student writing into lifeless academese.
10. The tool loses the learning focus and becomes an editing service.

## What counts as a minor issue?

Examples:

- A table heading is slightly different from expected.
- The output is useful but too long.
- It gives four actions where three were requested.
- It forgets to mention `prompt` at the end.
- It uses a slightly formal tone but remains clear.
- It gives a good answer but the structure could be easier to scan.

## Testing interactive tools

Some tools cannot be judged from one answer.

Interactive tools include:

- Socratic Tutor
- Viva or Supervisor Practice
- Guided Topic Brainstorming
- Critical Opponent Review, when used as dialogue

For these, test only the first two or three turns.

Check whether the tool:

- asks one question at a time
- responds to the student’s answer
- does not lecture too much
- does not answer for the student
- keeps the student thinking
- gives a summary only when asked or when closing

## Testing on free plans

If testing on a free AI plan:

- use a mini library, not the master library
- test one tool at a time
- use short inputs
- avoid full-draft tests unless needed
- record if the model switches to a smaller model or starts giving weaker answers

Free-plan behaviour matters because students may use the toolkit there.

## Suggested release checklist

Before publishing a new toolkit version, check:

- [ ] Index page links point to the latest files.
- [ ] Mini library ZIP contains the latest mini libraries.
- [ ] Master library has the same tool content as the mini libraries.
- [ ] Privacy and responsibility note appears near the top of the index page.
- [ ] Free-plan Markdown advice is present but not overlong.
- [ ] UK English default rule is present.
- [ ] Router handles `prompt`, `use US English`, and vague requests.
- [ ] Referencing Helper asks for institution/course guide or explicit house-style confirmation.
- [ ] Style and Clarity Review defaults to academic–journalistic clarity.
- [ ] Teaching materials tool clearly follows Find My Mistakes.
- [ ] Socratic Tutor asks one question at a time.
- [ ] Critical Opponent includes ideological assumptions mode.
- [ ] All files have version numbers.

## Suggested folder structure

```text
/testing
  ai_tutor_toolkit_test_suite_v1_0.md
  ai_tutor_toolkit_test_results_template_v1_0.md
  ai_tutor_toolkit_audit_prompt_v1_0.md
  ai_tutor_toolkit_testing_guide_v1_0.md

/audit-reports
  audit_report_writing_tutor_v1_4.md
  audit_report_structure_tutor_v1_4.md
  audit_report_academic_thinking_v1_4.md
  audit_report_research_proposal_v1_4.md
  audit_report_study_workflow_v1_4.md
```

## Suggested rhythm

A practical rhythm might be:

1. Run smoke tests after every edit.
2. Run regression tests before each published version.
3. Run the full test suite after major restructuring.
4. Keep audit reports so you can see whether the toolkit is improving over time.

## Final note

The aim of testing is not to prove that the toolkit is perfect. It is to make weaknesses visible, preserve good behaviours, and avoid accidental drift towards ghost-writing, fake certainty, or overcomplicated academic prose.
