# AI Personal Tutor Toolkit — v3 Design Brief

**Working title:** v3.0 — Paragraph-first tutor style and writing-as-thinking revision  
**Status:** Design brief for discussion  
**Applies to:** Site, prompt libraries, testing/audit pack, developer documentation  

---

## 1. Purpose of this brief

This brief sets out the proposed direction for a major v3 revision of the AI Personal Tutor Toolkit.

The current toolkit is already built around an important boundary: students should use AI as a tutor, not as a ghost-writer. The v3 revision keeps that boundary, but adds a more positive and practical design layer:

> The toolkit should provide structured, readable and specialist writing support that helps students think, revise and learn without being overwhelmed by AI output.

The revision is not only about stronger guardrails. It is about the quality of the tutoring interaction: how much the AI says, how it says it, whether the feedback feels manageable, and whether the student is encouraged to think rather than simply receive an answer.

---

## 2. Why v3 is needed

The current toolkit is strong on responsibility, authorship boundaries and structured prompt behaviour. It repeatedly explains that AI should support the student’s own work rather than replace it.

However, general-purpose AI systems have another common problem: they often produce too much. They default to long lists, many headings, dense bullet points and over-detailed explanations. This can make feedback feel intimidating even when the content is useful.

Students may experience AI feedback as:

- too long;
- too list-heavy;
- too abstract;
- too much like a report;
- too hard to act on;
- disconnected from how a human tutor would speak.

The v3 revision should make the AI feel more like a focused writing tutor. It should still be structured, but not needlessly exhaustive. It should give students enough to move forward, not so much that the response becomes another burden.

---

## 3. Core v3 design idea

The v3 design idea is:

> Paragraph-first, manageable, specialist writing support.

This means:

- short paragraphs by default;
- fewer unnecessary bullet lists;
- tables only where they genuinely help;
- plain English explanations;
- one or a few clear next steps;
- support for students who say they are stuck;
- recognition that writing is a form of thinking;
- grammar terms taught plainly rather than avoided;
- a stronger positive pitch: this is not only guardrails, but focused writing support.

---

## 4. Relationship to the toolkit’s purpose

The toolkit’s purpose is not to automate student work. It is to help students use AI for feedback, explanation, practice and revision.

The v3 revision strengthens this purpose by focusing on the student’s experience of the output.

A tool can technically avoid ghost-writing but still fail educationally if it overwhelms the student with a long list of tasks. A student who receives too much feedback may stop thinking, skim, copy, or give up. A good tutor does not simply say everything that could be said. A good tutor chooses what the student can use next.

The v3 revision should therefore treat output shape as part of pedagogy.

---

## 5. Principle 1: paragraph-first output

### Proposed principle

The toolkit should use short, readable paragraphs by default.

Bullet points and tables should still be used where they help, especially for:

- menus;
- error lists;
- test logs;
- revision plans;
- comparison tables;
- tool directories;
- audit evidence tables.

But they should not be the default style for all feedback.

### Rationale

AI systems often produce long bullet-heavy outputs because this looks organised. But for many students, this can feel overwhelming. Short paragraphs can feel more like a tutor explaining something directly.

Paragraph-first output also supports plain English. It encourages explanation rather than dumping categories.

### Draft global rule

```markdown
## Output style: paragraph-first by default

Write in short, readable paragraphs by default. Do not overuse bullet points or long nested lists.

Use tables or bullet points only when they make the feedback easier to act on, such as for menus, error lists, comparison tables, revision plans, test logs or audit evidence.

Prefer plain English, short sentences and a tutor-like style. Give the student a manageable amount of feedback.
```

---

## 6. Principle 2: manageable feedback

### Proposed principle

The AI should give the student a usable amount of feedback.

For most student-facing tools, this means focusing on the most important issue first rather than producing a catalogue of every possible issue.

### Rationale

Students do not improve because they are given more comments. They improve when they understand what to do next.

A long response can make the student feel that the work is worse than it is, or that revision is impossible. The toolkit should encourage focused improvement.

### Draft global rule

```markdown
## Manageable feedback

Give the student a manageable amount of feedback.

For most student-facing tools, focus on the most important issue first. Do not produce a long catalogue unless the tool specifically requires it, such as WT3, ST1, ST2 or an audit/testing tool.

Where possible, end with one clear next action.
```

---

## 7. Principle 3: writing is thinking

### Proposed principle

Writing should be presented as part of thinking, not merely as the final expression of thinking.

### Rationale

Students often discover what they think by trying to write it. They notice gaps, contradictions and uncertainties through the act of drafting. If AI makes the early choices too quickly, it may remove the productive struggle that helps learning happen.

This principle supports the “not a first-draft generator” page, but it should also shape the prompt libraries themselves.

### Draft wording

```markdown
## Writing is thinking

Writing is not just the final record of thinking. It is one of the ways students think.

When students struggle to choose words, connect evidence, organise paragraphs and explain claims, they are developing understanding. The toolkit should support that struggle, not remove it too early.
```

---

## 8. Principle 4: structured and specialist writing support

### Proposed principle

The site pitch should balance responsibility and positive value.

The toolkit is not only a set of guardrails. It provides structured writing support: focused feedback, explanation, practice and revision guidance of the kind a tutor might provide.

### Rationale

The current “not a ghost-writer” framing is essential, but if overused it can make the toolkit sound mainly restrictive. The positive claim should be clearer:

> This is a way to make general AI more useful for academic writing, revision and thinking.

### Draft site wording

```text
The toolkit is not only a set of guardrails. It gives students structured writing support: focused feedback, plain explanation, practice and revision guidance of the kind a tutor might provide.
```

Alternative shorter wording:

```text
It turns general AI into more focused writing-support conversations.
```

---

## 9. Principle 5: not a general-purpose homework-answer tutor

### Proposed principle

The toolkit should clarify its scope.

It is mainly for writing, revision, academic thinking, research planning and study workflow. It is not a general-purpose homework-answer system.

### Rationale

The name “AI Personal Tutor Toolkit” is broad. The site should avoid overclaiming. Its centre of gravity is writing and academic development, not tutoring every subject or answering any homework question.

### Draft wording

```text
The toolkit is mainly for writing, revision, academic thinking, research planning and study workflow. It is not a general-purpose homework-answer system.
```

---

## 10. Principle 6: “I’m stuck” support

### Proposed principle

The toolkit should explicitly tell students that they can say “I’m stuck” at any stage.

If the student says they are stuck, confused, overwhelmed, unsure what to do next, or unable to continue, the AI should switch into a slower, conversational support mode.

This should not trigger a long menu, a long diagnostic report, or a large set of tasks. The aim is to take a step back, reduce pressure, and help the student find a manageable next move.

### Student-facing contract

The launcher or opening guidance should include a short reassurance such as:

```text
If you get stuck at any point, say: “I’m stuck.” I will take a step back and help you work out a manageable next move.
```

This matters because students often do not know what kind of help to ask for. The toolkit should make it legitimate to pause and ask for orientation.

### If the reason is clear from context

If the conversation makes it reasonably clear why the student is stuck, the AI should say what it thinks the problem is and offer help with that likely problem.

For example:

```text
I think you may be stuck because you are trying to make the paragraph sound academic before you are clear what the main point is.

If that is right, we can first name the main claim in plain English. If I have misunderstood, tell me what feels stuck.
```

The AI should be tentative, not overconfident. It should make the likely problem visible, but it should also invite correction.

### If the reason is unclear

If it is not clear why the student is stuck, the AI should ask a short clarifying question rather than guessing or giving a long list.

For example:

```text
What feels stuck: the idea, the structure, the wording, the evidence, or knowing which tool to use?
```

The question should be simple enough for the student to answer quickly.

### Output style

The response should usually give two or three possible ways forward, written in short paragraphs rather than a bullet-heavy checklist.

It should end conversationally, for example:

```text
Does one of these fit, or is the problem somewhere else?
```

The aim is to reduce pressure, not add more tasks.

### Draft global rule

```markdown
## “I’m stuck” support

Tell students that they can say “I’m stuck” at any stage.

If the student says they are stuck, confused, overwhelmed, unsure what to do next, or unable to continue, slow down and take a step back. Do not give a long menu, a long diagnosis, or a large task list.

If the reason seems clear from the conversation, briefly say what you think is causing the problem, then offer help with that likely issue. Make clear that the student can correct you if you have misunderstood.

If the reason is unclear, ask a short clarifying question, such as whether the problem is the idea, the structure, the wording, the evidence, or choosing the right tool.

Usually offer two or three manageable ways forward, in short paragraphs. End conversationally by asking whether one of those fits or whether the problem is somewhere else.
```

### Example response style

```text
I think you may be stuck because the paragraph is trying to sound academic before the main point is clear. If that is right, the next move is not to polish the wording. It is to say the main claim in plain English first.

Another possibility is that the paragraph has too many ideas competing for space. If so, choose the single claim you most want the reader to understand, and move the other ideas aside for now.

If the problem is really the evidence, we can look at what your source actually proves and what it does not yet prove.

Does one of these fit, or is the problem somewhere else?
```

---

## 11. Principle 7: grammar terms should be taught, not hidden

### Proposed principle

The toolkit should not avoid essential grammar terms. It should explain them in plain English.

Terms such as subject, verb, object, clause, sentence, passive construction and conjunction are useful building blocks for writing support. The problem is not the terms themselves. The problem is using them without explanation.

### Rationale

Students may struggle with grammatical terminology, but these concepts can help them understand sentence problems, incomplete sentences and run-on sentences. The toolkit should teach the terms through simple examples before applying them to the student’s writing.

The uploaded Essay Writing Guide explains sentence structure through “The boy kicks the ball”: the boy is the subject because he does the action, kicks is the verb because it names the action, and the ball is the object because it receives the action. It also uses this subject/verb logic to explain incomplete sentences and run-on sentences.

### Draft writing-library rule

```markdown
## Grammar terms

Do not avoid essential grammar terms such as subject, verb, object, clause, sentence, passive construction or conjunction.

When using a grammar term, explain it in plain English the first time. Use a simple example before applying it to the student’s writing.

For example, in “The boy kicks the ball”, “the boy” is the subject because he does the action, “kicks” is the verb because it names the action, and “the ball” is the object because it receives the action.
```

### Likely affected tools

- WT1 — Clarity Clinic
- WT3 — Find My Mistakes
- WT4 — Teach Me This Mistake
- WT5 — Style and Clarity Review, where sentence structure affects style
- WT2 — Single Paragraph Analysis, where sentence structure affects paragraph meaning

---

## 12. Prompt-library implications

A v3 prompt-library revision should update:

- global rules;
- output style rules;
- master library;
- all five mini libraries;
- launcher wording if necessary;
- WT1, WT3 and WT4 especially;
- any tool that tends to produce long bullet-heavy output;
- any tool that uses grammar terminology;
- any follow-up behaviour where students ask for shorter, simpler, or rewrite-like help.

### Key changes to implement

1. Add paragraph-first output rule.
2. Add manageable-feedback rule.
3. Add writing-is-thinking principle.
4. Add “I’m stuck” support rule and student-facing reassurance.
5. Add grammar-terms guidance in Writing Tutor and master library.
6. Review tools for excessive bullet-heavy output.
7. Review tools for endings: each student-facing tool should usually end with a clear next action.

---

## 13. Site implications

A v3 site revision should update the project pitch across key pages.

### Likely affected pages

- homepage;
- Student Help homepage;
- Student guide;
- Why this is not a first-draft generator;
- Teaching approach;
- Why educators should consider this toolkit;
- Tutor and teacher guide;
- About page;
- Tools page;
- Writing Tutor page;
- Examples page if examples are revised.

### Main site message shift

From:

```text
Use AI responsibly and avoid ghost-writing.
```

To:

```text
Use AI for structured, focused writing support that helps you think, revise and learn.
```

The ghost-writing boundary remains essential, but it becomes part of a wider positive pitch.

---

## 14. Testing and audit implications

The testing/audit pack should be updated so that reviewers check the new v3 behaviours.

### New audit questions

- Does the output avoid unnecessary bullet-list overload?
- Does the tool give a manageable amount of feedback?
- Does the output use short paragraphs where appropriate?
- If tables or bullets are used, do they genuinely help?
- If grammar terms are used, are they explained plainly?
- If the student says “I’m stuck”, does the tool offer a few manageable ways forward rather than a long diagnostic list?
- Does the output support writing as thinking rather than rushing to a finished answer?
- Does the output end with a clear next action?

### New or revised test cards

Add a test for “I’m stuck” behaviour.

Example input:

```text
I'm stuck. I don't know what to do with this paragraph.
```

Expected behaviour:

- no long bullet list;
- switches into a slower, conversational support mode;
- if the reason for being stuck is clear, names the likely problem tentatively;
- if the reason is unclear, asks a short clarifying question;
- usually offers two or three manageable ways forward in short paragraphs;
- calm, supportive tone;
- asks whether one option fits or whether the problem is somewhere else.

Add or revise tests for output length:

```text
Can you explain this more simply? The feedback is too much.
```

Expected behaviour:

- shorter response;
- paragraphs rather than a long list;
- one or two priorities;
- one next action.

Add or revise tests for grammar terminology:

```text
I don't understand what subject and verb mean.
```

Expected behaviour:

- simple example;
- plain explanation;
- then application to the student's sentence.

---

## 15. Developer and maintenance implications

The v3 revision should also improve maintainability.

Current architecture deliberately repeats global rules in each mini library because each downloadable file must work independently when uploaded to an AI tool.

The v3 revision may make this more important, because global output style rules will affect every file. Maintainers should consider whether future tooling should generate mini libraries from a canonical source to reduce version drift.

### Developer roadmap implication

A future build process could:

- keep global rules in one canonical source;
- keep tool blocks in one source location;
- generate the master library;
- generate the five mini libraries;
- rebuild latest and versioned archives;
- reduce manual copying.

This is not required before v3, but v3 makes the case stronger.

---

## 16. Suggested staging for v3

### Stage 1 — Design brief

This document.

Purpose:

- agree the direction before editing libraries;
- define the v3 principles;
- identify affected files;
- clarify testing implications.

### Stage 2 — Prompt-library v3 draft

Create draft v3 versions of:

- master library;
- all five mini libraries.

Focus on:

- global rules;
- paragraph-first output;
- manageable feedback;
- writing-is-thinking;
- “I’m stuck” support, including the student-facing reassurance and contextual response rules;
- grammar terms guidance.

### Stage 3 — Site v3 draft

Revise the site pitch and key explanatory pages.

Focus on:

- structured and specialist writing support;
- writing as thinking;
- not just guardrails;
- not a general homework-answer tutor;
- readable tutor-like help.

### Stage 4 — Testing/audit v3 draft

Update:

- audit prompt;
- educator testing guide;
- step-by-step test cards;
- universal/adversarial tests;
- test log if needed.

Add tests for:

- paragraph-first output;
- manageable feedback;
- “I’m stuck” support;
- grammar-term explanation;
- output overload.

### Stage 5 — Full v3 release

Release as:

```text
Site v3.0
Prompt libraries v3.0
Testing/audit pack v3.0
```

Changelog theme:

```text
Major revision: paragraph-first tutor style, writing-as-thinking principle, manageable feedback, “I’m stuck” support, and clearer grammar teaching guidance.
```

---

## 17. Risks and cautions

### Risk 1: paragraph-first output could reduce useful structure

Some tools need tables, lists and structured outputs. The rule should be paragraph-first by default, not paragraph-only.

### Risk 2: shorter output could become too vague

Manageable feedback should still be specific. The aim is not to make the tutor less useful. The aim is to prioritise.

### Risk 3: grammar terms could intimidate students

Terms should be taught through simple examples. The toolkit should not assume prior grammar knowledge.

### Risk 4: “I’m stuck” support could become generic reassurance

The response must still be useful. It should either identify the likely reason the student is stuck or ask a short clarifying question. It should offer concrete ways forward, not just encouragement.

### Risk 5: site pitch could become too broad

The toolkit should not overclaim. It is mainly for writing, revision, academic thinking, research planning and study workflow.

---

## 18. Success criteria for v3

The v3 revision succeeds if:

- student-facing outputs feel more readable and less overwhelming;
- the toolkit’s positive value is clearer, not only its restrictions;
- the idea that writing is thinking is visible in the site and prompts;
- students who say “I’m stuck” receive a useful, manageable and conversational response that either names the likely problem or asks a short clarifying question;
- grammar terms are explained plainly rather than avoided or used opaquely;
- audit tests can check the new behaviours;
- the toolkit still protects student authorship and academic integrity;
- educators can still inspect, test and adapt the prompt libraries.

---

## 19. Summary recommendation

The v3 revision should be treated as a major design update.

It should shift the toolkit from:

```text
responsible AI guardrails
```

towards:

```text
structured, readable and specialist writing support that protects student thinking
```

The core boundary remains the same: the toolkit should help students use AI as a tutor, not as a ghost-writer. The new emphasis is that good tutoring is not just safe; it is readable, focused, humane and manageable.


## Why paragraph-first output matters

Many AI tools produce answers that are easy to skim but harder to read carefully: headings, bullet points, nested lists and fragments of advice. This can look organised, but it can also overwhelm students or make feedback feel like a long checklist of things to fix.

The toolkit uses a paragraph-first style because a good paragraph already supports both skimming and understanding. The first sentence gives the reader the main point. The rest of the paragraph explains, illustrates or qualifies that point.

This matters for tutoring. Students do not only need information they can scan. They often need a short explanation they can actually read, follow and think with.

Paragraphs are not anti-accessibility. Poor paragraphs are. A short, well-led paragraph can be easier to read than a long list of disconnected points.
