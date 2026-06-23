# In-tool help system and EAL mode specification

## Status

Implementation specification for the v4.4.0 in-tool help system and optional EAL mode. The live implementation is generated from shared prompt-library source files, especially `src/prompt-library/shared/05-help-system.md`.

## 1. Purpose

The toolkit should give students a simple way to get help after a tool has produced feedback.

The help system should help students use the last output. It should not become a general routing tool, a rewrite tool, a grading tool, or a new review tool.

The core design is:

```text
help = help me use the last feedback
```

not:

```text
help = diagnose my whole paper again
help = choose a different tool for me
help = rewrite my work
```

## 2. Scope

This specification covers:

- a post-output help trigger for review-style tools
- a compact help menu
- the behaviour behind each help option
- an optional global `EAL on` mode
- interaction with tiered-review tools
- a safe fallback for ambiguous state
- what was dropped or changed from earlier proposals

This specification does not implement:

- model-detected stuckness
- automatic cross-library routing
- lockout or refusal behaviour
- grading or reassurance checks
- a general-purpose mismatch-routing tool
- a general “improve my essay” catch-all tool

## 3. Help trigger

The student may type:

```text
help
```

or:

```text
I'm stuck
```

after a tool output.

When this happens, the toolkit should help the student use the last output. It should not automatically re-run the tool, choose a new tool, or perform a new review.

If the student is at a menu, `help` should point them back to the menu options already available there.

If the student is inside an interactive tool, the tool should handle stuckness inline rather than opening the review-output help menu.

## 4. Post-output footer

After a non-interactive review output, the tool may show a quiet footer:

```text
Stuck, short on time, or want this explained differently? Type `help`.
```

The footer should be short. It should not display the full help menu unless the student asks for it.

If the output is from a tiered-review tool at Tier 1, use a version that respects `expand`:

```text
Need help using this summary? Type `help`. Need more detail? Type `expand`.
```

The footer should not appear in the middle of an output.

## 5. Help menu

When the student types `help` after a review output, show:

```text
How can I help you use the last feedback?

1. Explain this differently.
2. Give me one first step.
3. I'm short on time — give me three short takeaways.
4. Show me an example.
5. Take me back to the menu.
```

The menu has four help behaviours plus one visible exit:

1. comprehension support
2. next-action support
3. time-triage support
4. modelling support
5. return to the current menu

The fifth item is not a routing tool. It returns the student to the current library menu, or explains that a single-tool prompt contains only the current tool.

## 6. Behaviour for option 1: Explain this differently

Purpose:

```text
Help the student understand the last feedback.
```

The tutor should:

- re-explain the last feedback in clearer language
- reduce unnecessary jargon
- define necessary grammar, writing or academic terms
- use one short example if useful
- keep the student focused on the same feedback point
- avoid expanding into a full new review

If the student has EAL mode on, or says English is not their first language, the tutor should also:

- make the language pattern visible
- explain academic wording choices where useful
- keep the intellectual content at the same level
- avoid treating language patterns as carelessness
- avoid rewriting the student’s work

A light term explanation is allowed. A deeper lesson or practice sequence should be suggested as a next step only if the student wants more depth.

Example boundary:

```text
Allowed:
“Comma splice means two complete sentences have been joined only with a comma. In your sentence, the comma is doing work that needs a full stop, semicolon, or joining word.”

Not allowed:
A long grammar lesson that ignores the original feedback.
```

## 7. Behaviour for option 2: Give me one first step

Purpose:

```text
Reduce overwhelm by choosing one action.
```

The tutor should:

- choose one practical first action from the last feedback
- explain why this is the best place to start
- give a small instruction the student can act on
- stop after that one action

This option covers both:

```text
It's too much.
```

and:

```text
I don't know where to start.
```

The output should not become a three-point triage list. That belongs to option 3.

## 8. Behaviour for option 3: I'm short on time — give me three short takeaways

Purpose:

```text
Help the student prioritise under time pressure.
```

The tutor should:

- give up to three short takeaways
- choose them by likely impact
- name the changes rather than write the changes
- keep the student responsible for the final wording
- avoid producing a corrected or improved version of the student’s work

This differs from option 2:

```text
Option 2 = one first step for sequencing.
Option 3 = up to three high-impact takeaways for triage.
```

## 9. Behaviour for option 4: Show me an example

Purpose:

```text
Demonstrate the move without doing the student’s work.
```

The tutor should:

- use parallel, invented or simplified material where possible
- show the same writing or thinking move on different content
- explain what the example demonstrates
- invite the student to try the same move on their own work

The tutor must not produce a model improved version of the student’s own paragraph, section, essay or answer unless the selected tool explicitly permits a tiny local correction.

Boundary:

```text
Allowed:
A parallel example that demonstrates how to make a cautious claim.

Not allowed:
A rewritten version of the student’s own paragraph presented as a model answer.
```

## 10. Behaviour for option 5: Take me back to the menu

Purpose:

```text
Give the student a visible way out when the current output is not useful.
```

The tutor should:

- return to the current library menu
- avoid diagnosing the mismatch in depth
- avoid recommending a different tool unless the current menu already provides that choice
- avoid re-running the tool
- avoid performing a new review

If the student is using a single-tool prompt, say:

```text
This prompt only contains the current tool. To choose a different tool, open the relevant mini-library or the master library.
```

This option is an exit, not a router.

## 11. EAL mode

The toolkit should support an optional global flag:

```text
EAL on
```

and:

```text
EAL off
```

The launcher or menu may advertise this briefly:

```text
Optional: type `EAL on` if English is not your first language. I will explain feedback in clearer English, define key terms, and keep the academic level of your ideas.
```

When `EAL on` is active, all tools should adapt their explanations.

## 12. What EAL mode changes

When EAL mode is on, the tutor should:

- use clearer, more direct explanations
- define key academic, grammar or writing terms when they matter
- make language patterns visible
- explain useful academic wording choices
- use concrete examples where helpful
- treat language patterns as learnable, not careless
- keep the student’s intellectual content at the same level
- help the student make their own revision decisions

## 13. What EAL mode must not change

EAL mode must not:

- simplify the student’s ideas
- lower the academic level
- become proofreading mode
- become rewriting mode
- over-correct the student’s voice
- replace the student’s own wording wholesale
- override tool-specific boundaries
- make every response longer than necessary

EAL mode changes the explanation style. It does not change the authorship boundary.

## 14. Interaction with tool modes

The help system should respect existing tool modes.

### Routing-helper tools

Routing-helper tools do limited triage. If the student is at a routing/menu stage and types `help`, the tool should help them use the available menu. It should not run a review.

### Interactive tools

Interactive tools should handle stuckness inline.

If the student says they are stuck, lost or overwhelmed during an interactive tool, the tutor should:

- slow down
- recap briefly
- ask a simpler question
- offer a smaller next move
- continue the interaction

Interactive tools should not open the review-output help menu mid-dialogue.

### Full-review tools

Full-review tools may show the standard post-output footer after the full review.

If the student types `help`, show the five-item help menu.

### Tiered-review tools

Tiered-review tools should not treat `help` as a substitute for `expand`.

At Tier 1:

- `expand` means show more detail
- `help` means help the student use the Tier 1 summary

The Tier-1 footer should make this distinction clear.

## 15. Safe fallback for ambiguous state

If the tutor cannot tell whether the student is at a menu, after a review output, at Tier 1, or mid-dialogue, use the safest fallback.

The fallback should:

- step back
- ask what the student needs next
- avoid running a new review
- avoid rewriting
- avoid choosing a new tool automatically

Fallback wording:

```text
Let’s step back. What do you need next?

1. Explain the last feedback more clearly.
2. Give you one first step.
3. Help you choose from the menu.
4. Show a short example on different material.
```

This fallback is deliberately conservative. It is safer to ask a small clarifying question than to assume the wrong state and perform the wrong behaviour.

## 16. Implementation notes

A future implementation should probably add a shared file such as:

```text
src/prompt-library/shared/05-help-system.md
```

This file should contain:

- help trigger behaviour
- post-output footer wording
- the five-item help menu
- behaviours for each menu item
- EAL flag handling
- interaction with tool modes
- safe fallback rules

Tools should not each contain their own copied help menu. They should point to the shared help-system behaviour.

A tool’s end behaviour can say, where appropriate:

```text
Then show the standard help footer.
```

or, for Tier 1:

```text
Then show the Tier-1 help footer.
```

## 17. Audit and testing requirements

If implemented, the audit pack should test:

- the footer appears only after appropriate outputs
- `help` after a full-review output opens the five-item menu
- option 1 explains feedback differently without re-running the tool
- option 2 gives one first step only
- option 3 gives up to three short takeaways, named not written
- option 4 gives a parallel example, not a rewritten version of the student’s own work
- option 5 returns to the menu without becoming a routing tool
- `help` at a menu resolves to menu help, not review-output help
- `help` mid-dialogue in an interactive tool is handled inline
- `EAL on` changes explanation style without simplifying ideas or rewriting work
- tiered tools keep `help` and `expand` distinct
- ambiguous state uses the safe fallback
- the help system behaves under master-library context load

## 18. Dropped or changed ideas

### Dropped: “Help me improve it without rewriting it for me”

This was dropped because it was too close to the general purpose of the tools themselves. It risked becoming a catch-all improvement tool or a second version of the selected tool.

The student’s goal is usually to improve the work. The help menu should instead ask what kind of help they need with the last feedback.

### Changed: “This isn’t what I needed”

This was changed into:

```text
Take me back to the menu.
```

The earlier wording risked becoming a hidden routing tool. The revised wording gives the student a visible exit without inviting a new diagnostic process.

### Merged: “It’s too much” and “I don’t know where to start”

These were merged into:

```text
Give me one first step.
```

They describe different feelings, but they need the same practical response: one first action.

### Changed: “I’m short on time”

This was kept, but clarified as:

```text
I'm short on time — give me three short takeaways.
```

This distinguishes it from “Give me one first step.”

### Changed: EAL support

EAL support was not added as a help-menu item. Instead, it became a global optional flag:

```text
EAL on
```

This is better because EAL support should affect all tool behaviour, not just one help response.

### Kept: “Explain this differently”

This remains the comprehension-support option. It covers unclear feedback, dense wording, unfamiliar terms and, when EAL mode is on, language-aware explanation.

### Kept: “Show me an example”

This remains the modelling option, but with a strict boundary: examples should use parallel material and must not become rewritten versions of the student’s own work.

### Added: ambiguous-state fallback

This was added because state detection may be fragile under master-library context load. The fallback asks what the student needs next instead of guessing the wrong state.
