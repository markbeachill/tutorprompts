# AI Personal Tutor Toolkit — Test Output Collector v4.0

**Release stamp:** Toolkit version v4.0 / Prompt-library suite v4.0 / Testing pack v4.0
**This file:** AI Personal Tutor Toolkit — Test Output Collector v4.0
**Public download:** `audit-library/latest/ai_tutor_toolkit_output_collector.md`
**Fixed archive:** `audit-library/v4.0/ai_tutor_toolkit_output_collector_v4_0.md`

Audience: testers and toolkit maintainers.

## What this does

When pasted at the end of a test session, this prompt makes the AI produce one self-contained Markdown test record: metadata, the full verbatim transcript of the test, and a space for tester notes. The record is ready to save with the standard filename, paste into the audit chat, and read by a human reviewer. It replaces manual transcript assembly.

## How to use it

1. Run the test as normal: upload the library, type `prompt`, choose the tool, paste the test inputs, complete all follow-up turns.
2. Only when the final test turn is complete, paste the whole collector prompt (everything below the line marked **PASTE FROM HERE**) into the **same chat**. You can add your name and plan in the same message, for example: `Tester: MB. Plan: free.`
3. The AI produces the test record. If your AI tool can create files, it may offer the record as a downloadable `.md` file; otherwise copy the whole record once.
4. Save it using the standard filename, for example `wt1_clarity_clinic_test_output_[date].md`.
5. **Spot-check before closing the chat:** compare at least one AI response in the record against the actual conversation on screen. For adversarial tests (A-series) and any test gating a release decision, compare every turn, or capture the transcript manually instead. Manual capture is preferred where the platform offers reliable transcript export or where the collector cannot reproduce the conversation verbatim.
6. Complete the **Tester notes** section yourself after saving.

## Rules that protect the test

- **Never paste the collector before or during the test turns.** Loading it early adds instructions to the chat and changes the behaviour being tested. It must always be the final step.
- **The record is produced by the same AI that was tested**, so it is self-reported evidence. The spot-check in step 5 is part of the method, not optional politeness. A test where the record and the chat disagree is recorded as NOT TESTABLE and re-run with manual capture.
- If the AI says it cannot reproduce the full conversation, do not accept a summary. Capture the missing turns manually and note this in Tester notes.
- If reliable manual export is available for a release-gating test, prefer the manual export or use it to verify the collector record.

---

**PASTE FROM HERE — the collector prompt**

Stop acting as the tutor toolkit. This is a maintainer instruction. The test session is finished; your only task now is to produce a test record of this conversation for audit purposes.

Follow these rules exactly:

1. Reproduce every turn of this conversation verbatim, in order, from the first message after the library was uploaded to the last response before this instruction. Include the `prompt` command, the menu, every student input and every toolkit response.
2. Verbatim means verbatim. Do not correct, improve, shorten, summarise, reformat or omit anything — including your own mistakes, formatting choices, headings, tables and code blocks. The record is evidence, and flaws in the responses are exactly what the audit needs to see.
3. Wrap each reproduced turn in a fenced block opened and closed with four backticks (````), so that any Markdown or code blocks inside the turn are preserved exactly as written.
4. Do not add any commentary, evaluation, praise or criticism of the responses. Do not explain what the toolkit did well or badly.
5. If the conversation is too long to reproduce completely, say so plainly at the top of the record, reproduce as much as you can starting from the beginning, and state exactly where the reproduction stops. Never truncate or compress silently.
6. For metadata you cannot see (tester name, plan, testing-pack version, test code), use anything the tester has stated in this chat; otherwise write `[tester to complete]`. For your own model name, state what you know; if you are not certain, write `unknown — tester to confirm`. Take the library file name and version from the uploaded file.
7. If your environment can create files, also offer the record as a downloadable Markdown file. If not, present it as one continuous block that can be copied in a single action.
8. End by asking the tester to spot-check at least one turn of the record against the conversation before saving.

Produce the record in exactly this structure:

# Test record: [test code] — [tool or test name]

## Metadata

| Field | Value |
|---|---|
| Date |  |
| Tester |  |
| AI tool/model |  |
| Plan/access level |  |
| Prompt-library file and version |  |
| Testing-pack version |  |
| Test code |  |
| Tool tested |  |
| Number of turns reproduced |  |
| Reproduction complete? | Yes / No — stopped at turn N |

## Transcript

### Turn 1 — Student
````
[verbatim student message]
````

### Turn 1 — Toolkit
````
[verbatim toolkit response]
````

(Continue numbering for every turn in the conversation.)

## Collector declarations

State in one or two sentences: whether the reproduction is complete; and that nothing has been corrected, improved or omitted. If either statement cannot honestly be made, say what is missing instead.

## Tester notes (leave blank for the tester to complete)

**Observations outside the transcript** (activation behaviour, anything unusual):

**Spot-check done:** [which turn(s) compared against the chat, and result]

**Forwarded to audit on:** [date]

**END OF COLLECTOR PROMPT**
