# Example cards

Hand-written example scenarios, one per tool, used to create site example
snippets. These are deliberately NOT the adversarial audit inputs: examples are
shop-window content, so scenarios are clear and representative. Inputs are
pasted into a real tool session, which is then captured with the output
collector and converted on the create-examples page.

Format (parsed by scripts/build_create_examples_page.py):

- `## CODE — Title` starts a card. The code is read from the heading; the title
  is taken from the tool index, so the part after the dash is just for readers.
- `**Scenario:**` and `**Shows:**` lines give the two descriptions.
- One or more `### Input` (or `### Input 1`, `### Input 2`, ...) sections, each
  followed by a fenced code block holding the verbatim input. Fences mean
  newlines and quotes are literal — no escaping needed.

Keep inputs distinct in topic and structure from the library's embedded teaching
examples (the test-input hygiene rule still applies).

## WT1 — Which Writing Tool Should I Use?

**Scenario:** A student has a short paragraph and is unsure which writing tool fits.

**Shows:** WT1 suggests at most two tools with reasons and the exact text to submit, without fixing the writing.

### Input

```
I have this paragraph and I am not sure which tool to use:

Remote working changed how teams communicate. Email went up. Some managers felt they had less control. Productivity is hard to measure now.
```

## WT2 — Clarity Clinic

**Scenario:** A student wants one vague sentence made clearer.

**Shows:** Clarity Clinic diagnoses the real clarity problem, teaches with a made-up before/after, and asks the student to attempt the rewrite.

### Input

```
Can you help me make this clearer?

There are a number of elements that play a part in why the outcome ended up being what it was.
```

## WT3 — Single Paragraph Analysis

**Scenario:** A student pastes one body paragraph to check it gets its point across.

**Shows:** Single Paragraph Analysis maps the chain of ideas, finds where it breaks, and sets a focused revision task.

### Input

```
Please check this paragraph:

Electric cars are becoming popular. They are quiet and cheaper to run. Charging can be slow. The government offers grants. People worry about battery life on long trips.
```

## WT4 — Find My Mistakes

**Scenario:** A student asks for surface mistakes in a couple of sentences.

**Shows:** Find My Mistakes lists concrete grammar, punctuation and word-choice issues and explains each briefly, without rewriting the work.

### Input

```
Can you find my mistakes?

The results was suprising, it showed that most participants prefered the second option, however the sample were quite small so we cant be to confident.
```

## WT5 — Teach Me This Mistake

**Scenario:** A student brings a recurring mistake from WT4 and wants to understand it.

**Shows:** Teach Me This Mistake runs a short interactive micro-lesson on one pattern and checks understanding.

### Input 1

```
WT4 said I keep using a comma to join two full sentences. Can you teach me this one so I stop doing it?
```

### Input 2

```
So I should use a full stop or a semicolon between them?
```

## WT6 — Style and Clarity Review

**Scenario:** A student wants tone and readability improved without the content being rewritten.

**Shows:** Style and Clarity Review names the move to make and shows the principle, rather than supplying a finished rewrite.

### Input

```
Can you improve the style of this?

Due to the fact that the experiment was conducted in a manner that was not entirely consistent, it is possible to say that the results may potentially be considered somewhat unreliable.
```

## WT7 — Referencing Helper

**Scenario:** A student needs a Harvard reference checked and built from details.

**Shows:** Referencing Helper checks the format carefully and asks for any missing details rather than inventing them.

### Input 1

```
Is this Harvard reference correct?

Smith, J. (2020) The Future of Work. London, Routledge.
```

### Input 2

```
It was the second edition if that matters.
```

## WT8 — Paraphrase and Quotation Workshop

**Scenario:** A student checks whether their paraphrase of a source is safe.

**Shows:** Paraphrase and Quotation Workshop diagnoses too-close wording as an integrity risk and sets a task that produces new wording, without writing the paraphrase.

### Input

```
Please check whether this is a safe paraphrase.

Source: “Regular short breaks during study improve focus and reduce fatigue more than a single long break.”

My attempt: Taking regular short breaks while studying improves focus and reduces tiredness more than one long break (Lee, 2021).
```

## WT9 — Flow and Coherence: The Running Subject

**Scenario:** A student wants to know why a paragraph feels disconnected.

**Shows:** Flow and Coherence lists the grammatical subject of each sentence and comments on the hand-offs, asking the student to repair the weak join.

### Input

```
Why does this paragraph not flow well?

The museum reopened after a long refurbishment. Visitor numbers were recorded carefully by staff. A new digital ticketing system was introduced. This system reduced queues at the entrance considerably.
```

## WT10 — Learn Subjects: Parsing Your Own Sentences

**Scenario:** A student wants to practise finding subjects and verbs in their own sentences.

**Shows:** Learn Subjects teaches the fixed verb-first method and asks the student to try it, correcting the topic-vs-subject confusion.

### Input 1

```
Can you teach me to find subjects and verbs using my sentences?

The library extended its opening hours. The decision was praised by students. After the exams finished.
```

### Input 2

```
I think the subject of the second one is students.
```

## ST1 — Paragraph Structure Review Across a Whole Draft

**Scenario:** A student pastes three short paragraphs to check each works.

**Shows:** Paragraph Structure Review checks central-claim clarity before development and reports honestly, without inventing a pattern.

### Input

```
Please review these paragraphs:

Paragraph 1: Recycling rates vary a lot between cities.

Paragraph 2: Our town introduced food-waste collection. Households were given small bins. This created a problem. Participation was high in the first month. The scheme was featured in the local news.

Paragraph 3: Education also matters. People recycle more when they understand what can be recycled.
```

## ST2 — Whole-Work Structure Review

**Scenario:** A student lists the sections of a report in an odd order.

**Shows:** Whole-Work Structure Review maps the structure and asks the student to propose a better order before offering one.

### Input 1

```
Here are my sections:

Conclusion: The policy should be expanded.

Introduction: This report looks at the cycling subsidy.

Findings: Uptake rose by 20 percent.

Background: The subsidy began in 2023 to reduce car use.
```

### Input 2

```
I am stuck, can you show me an order?
```

## ST3 — Expert Meaning Review

**Scenario:** A student has a sentence that overstates its case.

**Shows:** Expert Meaning Review challenges the overclaiming and weak logic, separating what it can judge from subject facts to verify.

### Input

```
Does this make sense as an argument?

The trial proves that the new teaching method works for everyone and that traditional lectures should be abandoned completely.
```

## ST4 — Reverse Outline Mapper

**Scenario:** A student pastes a short draft and wants its structure mapped.

**Shows:** Reverse Outline Mapper produces a one-line-per-paragraph map of what the draft currently does and flags a likely digression.

### Input

```
Can you map the structure of this draft?

Para 1: This essay examines food delivery apps and small restaurants.

Para 2: The apps charge high commission, which cuts restaurant profits.

Para 3: Apps also bring new customers who would not have found the restaurant.

Para 4: Some cities have beautiful historic high streets.

Para 5: Overall the apps are a mixed blessing for small restaurants.
```

## AT1 — Assignment Brief Checker

**Scenario:** A student shares a brief, criteria, and a descriptive draft extract.

**Shows:** Assignment Brief Checker explains the task word, shows the extract describes rather than meets the task, and relates this to the criteria, without grading.

### Input

```
Brief: Compare two approaches to managing remote teams and recommend one.

Marking criteria: 40% comparison; 30% evidence; 20% recommendation; 10% clarity.

Draft extract: There are many ways to manage remote teams. Some managers use daily calls. Others use written updates. Remote work is common now.
```

## AT2 — Argument Map

**Scenario:** A student pastes a short passage that does contain an argument.

**Shows:** Argument Map separates the main claim, supporting points, evidence and assumptions, and names any gaps.

### Input

```
Map the argument in this:

Flexible hours improve productivity because employees work when they are most alert. A company trial found output rose after flexible hours were introduced. Therefore more firms should adopt flexible scheduling.
```

## AT3 — Descriptive vs Analytical Check

**Scenario:** A student pastes a paragraph that is mostly description.

**Shows:** Descriptive vs Analytical Check shows the balance, treats some description as necessary, and shows how to add the analytical step.

### Input

```
Is this descriptive or analytical?

The company launched a loyalty app in 2022. The app offered points for purchases. Many customers downloaded it. The points could be exchanged for discounts.
```

## AT4 — Evidence Gap Checker

**Scenario:** A student makes two strong claims with no support.

**Shows:** Evidence Gap Checker flags the claims needing evidence, suggests what kind would help, and asks the student to decide what counts as common knowledge.

### Input

```
Check my claims for evidence gaps:

Everyone now does their shopping online, which means physical shops will disappear within ten years.
```

## AT5 — Concept Clarity Checker

**Scenario:** A student names several overlapping concepts without defining them.

**Shows:** Concept Clarity Checker asks for clearer definitions, distinguishes related terms, and flags an ambiguous word.

### Input

```
Are my key concepts clear?

This study explores wellbeing, resilience, engagement and motivation at work, and shows that the effects on staff are significant.
```

## AT6 — Literature Use Checker

**Scenario:** A student lists three sources one after another.

**Shows:** Literature Use Checker names source-by-source listing as the main issue and suggests organising by theme or disagreement.

### Input

```
Is my literature use okay?

Brown (2018) writes about team motivation. Patel (2019) writes about remote communication. Olsen (2021) writes about employee wellbeing. These sources support my topic.
```

## AT7 — Counterargument and Limitations Checker

**Scenario:** A student states a confident claim with no counterargument.

**Shows:** Counterargument and Limitations Checker surfaces objections and ways to qualify the claim, auditing the text rather than staging a debate.

### Input

```
What counterarguments should I consider?

Four-day weeks are clearly better because one company tried it and staff were happier, so all employers should switch.
```

## AT8 — Source Reliability Checker

**Scenario:** A student lists a mix of sources of differing reliability.

**Shows:** Source Reliability Checker classifies each cautiously and gives reusable checks the student can apply themselves.

### Input

```
Can you check the reliability of my sources?

Sources: a company blog post, a peer-reviewed journal article from 2019, a Wikipedia article, and a national statistics agency report.
```

## AT9 — Critical Opponent Review

**Scenario:** A student asks to be challenged from a chosen standpoint.

**Shows:** Critical Opponent Review adopts the standpoint, surfaces assumptions and tough questions, and does not rewrite the argument.

### Input

```
Use the practical-feasibility opponent. My argument: Every school should give each pupil a laptop because it improves digital skills and makes lessons more engaging.
```

## AT10 — Socratic Tutor

**Scenario:** A student offers a tentative idea for Socratic questioning.

**Shows:** Socratic Tutor asks one focused question at a time, corrects a plain factual error briefly, and offers a checkpoint when answers repeat.

### Input 1

```
Ask me Socratic questions about this idea: Working from home may reduce a team's sense of belonging.
```

### Input 2

```
I think it reduces belonging because people do not chat as much. Also remote work was invented during the 2020 pandemic.
```

### Input 3

```
Like I said, it is mainly because there is less chatting between people.
```

## RP1 — Research Question, Aim and Objectives Checker

**Scenario:** A student has a broad topic with vague aims and objectives.

**Shows:** Research Question Checker identifies breadth and the missing question, and asks for the level and word count.

### Input

```
Topic: working from home. Aim: to study working from home and productivity and wellbeing and communication. Objectives: look at studies, talk about managers, explore productivity, discuss the future.
```

## RP2 — Methodology Fit Checker

**Scenario:** A student's method does not match their question.

**Shows:** Methodology Fit Checker spots the mismatch and names whether it is a design problem or a thin-description problem.

### Input

```
Research question: How do remote workers experience loneliness? Method: I will analyse ten company wellbeing policies using content analysis.
```

## RP3 — Critical Research Supervisor Review

**Scenario:** A student brings an early, pre-supervision idea.

**Shows:** Critical Research Supervisor Review calibrates to the early stage: honest questions and grounded encouragement, not final-approval standards.

### Input

```
This is an early idea before my first supervision meeting. I am thinking of studying how remote work affects team belonging, maybe interviewing a few people. I have not settled the method yet.
```

## RP4 — Viva or Supervisor Practice

**Scenario:** A student asks to be questioned like a supervisor and gives a vague answer.

**Shows:** Viva or Supervisor Practice asks one focused question, then probes the same point again when the answer is vague.

### Input 1

```
My proposal is about remote work and team belonging. Please question me like a supervisor.
```

### Input 2

```
It is about how working from home affects things in teams, really. There is a lot to it.
```

## RP5 — Guided Topic Brainstorming

**Scenario:** A student names a broad area and wants help finding a topic.

**Shows:** Guided Topic Brainstorming asks clarifying questions, offers directions, and viability-tests the chosen idea before asking the student to draft the question.

### Input 1

```
I want to do a dissertation about online learning and student motivation.
```

### Input 2

```
I like the first idea best.
```

## SW1 — Revision Plan

**Scenario:** A student has mixed feedback and a tight, stated time budget.

**Shows:** Revision Plan groups feedback into prioritised actions that fit the two evenings available.

### Input

```
Feedback: The argument is unclear. The evidence is thin. The structure jumps around. There are some referencing errors. It is a bit wordy.

My deadline is Monday and I have two free evenings before then.
```

## SW2 — Tutor Feedback to Action Plan

**Scenario:** A student received blunt tutor feedback.

**Shows:** Tutor Feedback to Action Plan acknowledges the bluntness, separates tone from usable content, and avoids speculating about the marker.

### Input

```
Tutor feedback: “This is muddled and feels rushed. Not your best.”
```

## SW3 — AI-Use Record

**Scenario:** A student is unsure what AI use to declare.

**Shows:** AI-Use Record distinguishes the kinds of help, builds a transparent record, and will not help downplay or hide AI use.

### Input

```
I used AI to reorganise my structure and to check my grammar, then I rewrote parts myself. I am not sure what I need to declare.
```

