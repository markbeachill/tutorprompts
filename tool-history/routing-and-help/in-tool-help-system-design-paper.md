# The in-tool help system: design paper

*Status: working paper / decision record. Captures the design of the student-triggered help system, reached incrementally across discussion. Records the reasoning, the decision tree, and the open items, so the work can be resumed rather than re-argued.*

---

## 1. Scope: in-tool, not in-menu

The help system to build is **in-tool**, not in-menu. Reasoning:

- **In-menu help is already largely solved.** The master launcher already gives a stuck student `not sure` (describe the problem → routed to a family), `I'm stuck` (step back, find a manageable move), and `list tools`. The family-first routing change handled the at-menu orientation case. There is little left to build there.
- **In-tool is where real stuck-ness lives.** At the menu the student has not engaged with anything; their difficulty is shallow ("which door"). Inside a tool, looking at real feedback on their own work, the genuine difficulties surface — don't understand, too much, disagree, out of time, just want the answer. Every rich stuck-state needs feedback in hand, which only exists in-tool.
- **In-tool is the reliable case.** The in-output helper needs *escalation, not routing*: context is already narrow, material is loaded, tool is known. It does not have to solve the hard "which of 32 tools" problem. This is the same category as the escalate-and-route work already drafted for WT4 and ST2.

### Escalation vs re-route
"In-tool help" is two things:
- **Escalation** — the student is stuck on this tool's output and needs this tool to respond differently (re-explain, example, slow down, triage, do-one-together). Self-contained; the core, high-value work.
- **Mismatch re-route** — the student is in the wrong tool. The honest response is "this isn't the right tool for what you describe — you want X." This reintroduces a small, scope-dependent routing tail (single tool → "look elsewhere"; mini-library → suggest a sibling; master → point anywhere). It must exist, because a help system that can *only* escalate within the current tool will help a student do the wrong thing better.

Design stance: **escalation-first, with a thin honest re-route for genuine mismatches.**

---

## 2. The student triggers it (not the model)

The help is **student-triggered**. This removes the model's two weakest jobs — *detecting* that the student is stuck and *inferring why*. The student declares it and picks the reason. It only loads when invoked, so it does not compete for context every turn. This is the `ask, don't guess` principle as a feature, and likely the most reliable mechanism in the toolkit.

Explicitly rejected: model-detected help (popping up because the student "seems confused"). Detection is unreliable and intrusive. Student-triggered, footer-advertised, is the robust version.

---

## 3. Two questions, kept separate: display vs trigger

A key clarification: **availability** and **visibility** are different, and **display** (passive: when the footer is shown) and **trigger** (active: what `help` does when typed) have different answers.

- **Availability: always.** The student can type `help` (or `I'm stuck`) at any point. No state, no conditions — a standing escape hatch. Locking it out anywhere fails the exact person it is for.
- **Visibility: limited.** The footer advertising help is shown in *fewer* places than the trigger is accepted.

### Display — when is the footer shown?
- **After a tool's output**, as a single quiet line (not an unfolding menu — that is the clutter failure). Example: *"Stuck, short on time, or want this explained differently? Type `help`."*
- **After output, not before** — the stuck-states do not exist until there is feedback. The moment of maximum stuck-ness is just after a tool hands back a wall of review.
- **Not** mid-output, **not** at menus (the menu is already help), **not** mid-dialogue (it interrupts), **not** model-triggered.

---

## 4. The decision tree: `help` is always available, but resolves by state

The central realisation: **`help` is one entry word that resolves to state-appropriate help. It is not one identical menu everywhere.** Universal availability, state-dependent resolution. The student never hits a wall; they get the help that fits where they are.

| State | Footer shown? | What `help` opens |
|---|---|---|
| **At a menu** (master or mini) | No (menu is already help) | Menu help — redirect to `not sure` / family routing. The in-tool stuck-states ("I don't understand the feedback") are meaningless with no feedback. |
| **After review-tool output** | Yes, full footer | Full six-item in-tool menu. The home case. |
| **At Tier 1 of a tiered tool** (summary shown, `expand` offered) | Yes, **trimmed** footer (no "too much" — the tool already reduced volume) | **Tier-1-aware** menu: omit "too much"; fold "I want more detail" into the existing `expand` rather than duplicating it. |
| **Mid-dialogue (interactive tool)** | No | Handled by the tool itself, inline — see §6. Not a help-system state. |

### Safe fallback
State detection is the known fragility (the model's state-tracking under load is weak). The branching must **degrade safely**: if the model cannot tell what state it is in, fall back to the *most generally useful* help — the step-back "let's work out your next move" (`I'm stuck`) behaviour, which makes sense in every state. Safe fallback beats precise-but-brittle.

---

## 5. The universal menu (one menu, six items)

Decision: **one universal menu**, not per-tool menus. Simpler, more reliable, easier for students to learn (same options everywhere), and avoids per-tool divergence. Accepts that an item or two occasionally does not apply on small tools (e.g. "too much" on a one-sentence Clarity Clinic output) — the misfit is tolerable; the Tier-1 case is handled by the trimming above.

Items (the paper's argued ceiling of ~6; more becomes its own "too much information" problem). All assume feedback is in hand:

1. **I don't understand the feedback** — re-explain the tool's last output in plainer terms, one example. (Distinct from not understanding the *topic* — label precisely.)
2. **It's too much** — collapse to the single most important thing and stop. (Mostly redundant on tiered tools; present for non-tiered ones; omitted from the Tier-1 menu.)
3. **I don't know where to start** — pick the one first action, nothing else. (The paralysis case the others miss; flagged as possibly the highest-value item.)
4. **I'm short on time** — triage: the two or three highest-impact fixes, named not written. (Routes to existing panicking-student behaviour.)
5. **I just want to improve it** — the goal-option. Routes by one question (learn how / see what's rewarded / fastest fixes), absorbing the "improve my grade / my essay" cluster. Includes the **no-verdict guard** (no grade prediction; route to criteria and self-assessment).
6. **This isn't what I needed** — the honest **mismatch re-route**; scope-aware ("you probably want ___ / look in another library"). The one item that points *out* of the tool.

### Items deliberately handled or held
- **"I disagree with the feedback"** — dropped as a separate item at six; mostly absorbed by #1 and #6. If kept explicit, it would replace #2 (since tiered tools already handle volume). Flagged as a judgement call.
- **The four "improve my essay" phrasings** — folded into one item (#5); they are one request at different urgencies.
- **"Is this allowed / cheating"** and **EAL/language** — left **off** the in-tool menu. They are not *stuck-on-this-output* states; they are standing concerns better served elsewhere (the AI-use record for honesty; global EAL handling for language). The in-tool menu stays tight and about *this output, right now*.

---

## 6. Interactive tools handle their own help inline (deleting State 4)

The fragile "mid-dialogue" state is not a help-system state at all — it is **the normal operation of an interactive tool**. "Mid-dialogue" maps almost exactly onto "an interactive tool is running" (AT10 Socratic, RP4 viva, WT5 teach, RP5 brainstorming, partly WT2). So it should be handled by the **tool**, not the help system.

Why inline help is better here than a menu:
- **Contextual.** A Socratic tutor three questions into a methodology discussion can answer "I'm stuck" with "let's back up — what's the one thing you're trying to find out?" A generic menu cannot; it does not know where the student is. The tool does. Inline help is *higher quality*, not just less disruptive.
- **Non-breaking.** Firing a menu into a dialogue throws away conversational state and interrupts the very back-and-forth that makes the tool work.
- **Removes the hardest detection problem.** The tool *knows* it is interactive because it is an interactive tool; no state detection needed. The fragile fourth state is **deleted**, not folded into a fallback.

Mechanism: a shared clause in the interactive tools' instructions — *"If the student signals they're stuck, lost or overwhelmed, don't break out to a menu. Ease off, step back a level, ask a simpler question or briefly recap where you've got to, then continue."* Defined once, referenced by all interactive tools (the pointer pattern).

Result: a clean disjoint split.
- **Interactive tools** → handle help themselves, in conversation.
- **Non-interactive (review) tools** → the help system catches `help` after output.

No tool is both; no state is ambiguous; the help system never detects mid-dialogue. This mirrors the gating fix: resolve behaviour by **tool category**, not by a global rule trying to handle all cases — same move, same payoff (no contradiction, clear ownership).

---

## 7. Where the code lives

Decision: **a separate file**, not code in each tool.

Rationale: one universal behaviour belongs in one place. The gating fix already moved away from per-tool repetition toward single-source category definitions to avoid drift. Thirty-two copies of the help menu means thirty-two chances to diverge. A separate file is one menu, edited once, identical everywhere by construction.

Placement: a peer of the existing cross-cutting numbered files (`01-global-rules`, `02-markdown-output-rules`, `03-launcher`, `04-router`) — e.g. **`05-help-system.md`, `run_policy: always_apply`**, so it is in context every turn and can fire on `help` from any tool. Router-adjacent is right, because the mismatch re-route (#6) needs the router's family knowledge.

### Division of labour (three pieces, not all in one place)
- **Menu, routing logic, state-branching, footer text → the separate help file.** The bulk. The help file detects state and branches (menu / post-output / tier-1) and owns the footer's actual wording.
- **Trigger-word recognition → the always-apply layer.** `help` / `I'm stuck` recognised the same way `prompt`, `create md` already are. A student typing `help` inside any tool is caught by the always-apply layer, not by the tool.
- **The footer's appearance at each tool's ending → a one-line pointer in each tool (Option B).** Each tool's end-behaviour says "...then show the standard help footer" — a pointer, not a copy. The footer text lives once in the help file; tools invoke it and position it relative to their own ending (`expand`, `prompt`). This matches the library's existing pattern (tools own their ending, referencing shared behaviours by name) and keeps single-source-of-truth while letting each tool place the footer correctly. Considered and not preferred: Option A (global "after any output, append the footer") — cleaner in tools but relies on a soft "after every output" instruction that can slip under load and sits awkwardly with tools that have specific endings.

The tools stay **thin**: a footer pointer, nothing more. No menu logic, no footer text, nothing that can diverge.

---

## 8. Consistency constraint (the recurring lesson)

`05-help-system` is always-apply, and so are the tiered-review category rules. Both shape how a tool ends. They must **agree**, not contradict — the same lesson as the gating fix. Specifically:
- The footer on a tiered tool must not offer "it's too much" as if volume were not already handled.
- `help` at Tier 1 must not fight the `expand` flow — it defers detail to `expand` rather than duplicating it.

Make the new always-apply layer *agree* with the category behaviours rather than issuing a blanket instruction that re-creates a contradiction. A deliberate consistency check between `05-help-system` and the tiered-review rules is required before shipping.

---

## 9. Open items to resolve

1. **Mark interactive tools explicitly.** The interactive-vs-review category rule needs a clean key — e.g. an `interaction_type: interactive` marker in front-matter. Without it the split is inferred, which is fragile.
2. **Hybrid tools.** Some tools may be partly interactive (produce a review, then offer to discuss it) — WT5 (builds a lesson *and* teaches interactively) is a candidate. Decide per tool which help model governs them, rather than leaving it to inference.
3. **"I disagree" item** — include explicitly (replacing #2) or leave absorbed by #1/#6? Judgement call.
4. **Reliability test under load.** As with everything in this toolkit, test the help system — especially state detection and the safe fallback — in the **master/large-file** condition where it is weakest, not only in minis.
5. **Footer wording per state** — finalise the trimmed Tier-1 footer vs the full post-output footer.
6. **Build order** — front door (trigger + menu) first, or the escalation behaviours behind each item first? Separable.

---

## One-line summary

Build a **student-triggered, universal, single-source in-tool help system** (`05-help-system`, always-apply): `help` is always available but resolves by state (menu → routing help; after review output → six-item menu; Tier 1 → trimmed menu deferring to `expand`); the footer is shown only after output (trimmed at Tier 1); interactive tools handle their own help inline (deleting the mid-dialogue state); tools stay thin with only a footer pointer; and the help layer must be checked for consistency against the tiered-review category rules.
