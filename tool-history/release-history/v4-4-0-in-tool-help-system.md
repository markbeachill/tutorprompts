# v4.4.0 — In-tool help system and EAL mode

This release implements the shared in-tool help system developed in `roadmaps/plans/in-tool-help-system-spec.md`.

## Main decisions

- Add a shared `05-help-system.md` always-apply section to every master, mini-library, custom and single-tool pack.
- Keep `help` focused on using the last output, not rerunning the tool, choosing a new tool, grading, rewriting or routing across the toolkit.
- Add post-output help footers for full-review tools and Tier-1-aware footers for tiered-review tools.
- Keep interactive tools conversational: if a student is stuck mid-dialogue, the tool slows down and continues inline rather than opening the review-output help menu.
- Add an opt-in `EAL on` / `EAL off` session flag. EAL mode changes explanation style across tools but does not change the authorship boundary or lower the academic level.

## Help menu

The review-output help menu is:

```text
How can I help you use the last feedback?

1. Explain this differently.
2. Give me one first step.
3. I'm short on time — give me three short takeaways.
4. Show me an example.
5. Take me back to the menu.
```

The fifth option is an exit, not a routing tool. It returns to the current menu or, in a single-tool pack, explains that the prompt only contains the current tool.

## Testing focus

The audit/testing pack adds HS1–HS6 cards for full-review help, tiered `help`/`expand`, inline stuckness in interactive tools, EAL mode, menu help/fallback, and single-tool menu-exit behaviour.
