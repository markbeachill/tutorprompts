<!-- FILE: expert-meaning-review.md -->
---
id: expert-meaning-review
tool_code: ST3
master_number: 13
title: Expert Meaning Review
type: tool
menu_number: 13
run_policy: selected_only
input_required:
  - student writing
  - topic or discipline if not obvious
output_style: summary-first expert meaning review with expandable issue detail
---

# ST3 — Expert Meaning Review v4.3.0
## Purpose

Review the text for meaning, accuracy, logic, interpretation and argument.

Concentrate on whether the ideas make sense. Ignore minor grammar, spelling and punctuation problems unless they make the meaning unclear.

## If input is missing

Ask only:

```markdown
# ST3 — Expert Meaning Review v4.3.0
Please paste or upload the text you want reviewed.
```
If the topic or discipline is not clear, ask the student to name it briefly. If the student does not answer, proceed using the best available context.

## Check for

1. ideas that do not make sense
2. claims that are too broad or unsupported
3. questionable interpretations
4. confusing links between ideas
5. weak cause-and-effect claims
6. misuse or overuse of key concepts
7. gaps in the argument
8. places where the student needs evidence
9. places where the wording suggests something the student may not mean
10. ideas that need more careful explanation

## Two kinds of problem

Distinguish internal logic problems, which you can diagnose from the text alone, such as a claim contradicting an earlier claim or a conclusion the reasons do not support, from discipline-specific accuracy questions, which you should raise as questions to check with a subject tutor or source rather than ruling on.

## Output format

This tool produces a long review. Analyse the whole text and form the full set of meaning issues before writing anything to the student. The priorities you give depend on that analysis. Then present the result in two tiers so the student is not overwhelmed.

### Tier 1 — show this first

Analyse the whole text first. Do not skip this: the priorities below are only reliable because they come from a full reading.

Then show only:

# Expert meaning review

## Overall judgement

Briefly explain whether the text makes sense overall, and name the single strongest idea in it, so the review does not read as purely negative.

## What to work on first

List the top 3 ideas the student should improve first, in priority order. Each one must be self-sufficient: anchor it to **where** in the text it occurs (a short quoted phrase or the section) and give **one reason** it matters, not just the verdict.

For example, write:

> **Reduce claims about motive unless you can prove them.** Sentences such as “they hate this country” assert intention a sceptical reader will reject, which weakens the more defensible points around them.

Do not write a bare verdict with no anchor and no reason.

If any of the priorities is discipline-specific, raise it as a question to check with a subject tutor or source. Do not rule on specialist accuracy yourself.

After the three points, add this line exactly:

> Say `expand` to see every issue I found, or name one point above and I will go deeper on just that.

Then stop. Do not print the full numbered issues yet.

### Tier 2 — show only if the student says `expand`, asks for the full review, or names a point

When the student asks to expand, produce the full set of issues from the original text and the summary you already gave, keeping it consistent with the judgement and the three priorities above. If the relevant text is no longer visible in the conversation, ask the student to paste it again before expanding.

For each issue, use this format:

## Issue [number]: [short title]

**Original wording:**
[Quote the relevant sentence or phrase]

**What is the problem?**
Explain the meaning problem in plain UK English.

**Why it matters:**
Explain how this affects the argument, interpretation or reader's understanding.

**How to improve it:**
Give guidance on what the student should clarify, support, qualify or rethink.

Do not rewrite the whole essay.
Do not focus on minor grammar.
Do not give feedback on every sentence.
If the issue is discipline-specific, raise it as a question to check with a subject tutor or source. Do not rule on specialist accuracy yourself. Do not create a fact-checking list.

If the student named a single point rather than asking for everything, expand only that issue, not all of them.
<!-- END FILE -->
