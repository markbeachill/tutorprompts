# v4.3.0 tiered-output update notes

This note records the design decision behind the v4.3.0 prompt-library update.

## Purpose

Several long review tools were useful but could produce outputs that felt too large for students to act on. The v4.3.0 update keeps whole-input analysis, but changes selected long review tools so they show a short usable first response and offer fuller detail only when the student asks to expand.

## Tools changed

| Tool | Treatment |
|---|---|
| ST1 — Paragraph Structure Review Across a Whole Draft | Tiered output; paragraph-function table stays visible first, detailed paragraph comments expand later. |
| ST2 — Whole-Work Structure Review | Tiered output; compressed reverse-outline snapshot stays visible first, full map/issues expand later. |
| ST3 — Expert Meaning Review | Tiered output; overall judgement, strongest idea and top priorities stay visible first, full issues expand later. |
| AT7 — Counterargument and Limitations Checker | Tiered output; top challenge/limitation priorities and a student task stay visible first, tables expand later. |
| AT9 — Critical Opponent Review | Tiered output; opponent type, single strongest challenge and top actions stay visible first, objections/assumptions/questions expand later. |
| WT4 — Find My Mistakes | Not gated; adds a short first-focus note but still shows every in-scope mistake in full. |

## Mechanism

Each tiered tool should analyse the whole input before choosing the Tier 1 priorities. The Tier 1 summary is therefore grounded in the full reading.

The tool must not claim that hidden tables or full reviews are stored across turns. If the student asks to expand, the tool should produce fuller detail from the original input and the Tier 1 summary already given. If the relevant original text is no longer visible in the conversation, it should ask the student to paste it again before expanding.

## Accepted review edits

Before integration, the proposed updates were tightened as follows:

- ST1 omits the **Recurring pattern** section unless there is a genuine recurring pattern.
- ST2 makes the student-proposes-order stopping rule explicit and does not give a suggested-order table until asked or the student says they are stuck.
- ST3 raises discipline-specific accuracy concerns as questions to check with a subject tutor or source, and does not become a fact-checking list.
- WT4 adds no first-focus note when there are no mistakes within WT4's scope.

## Audit implication

The audit pack must not mark the Tier 1 output incomplete merely because detailed tables or issue lists are withheld. It should check whether the first response is useful, grounded, manageable and gives clear expansion instructions. Expansion turns should stay consistent with the Tier 1 summary.
