# AI Personal Tutor Toolkit — Step-by-Step Test Cards v4.1

**Release stamp:** Toolkit version v4.1 / Prompt-library suite v4.1 / Testing pack v4.1
**This file:** AI Personal Tutor Toolkit — Step-by-Step Test Cards v4.1  
**Public download:** `audit-library/latest/ai_tutor_toolkit_step_by_step_test_cards.md`  
**Fixed archive:** `audit-library/v4.1/ai_tutor_toolkit_step_by_step_test_cards_v4_1.md`

Audience: educators, tutors, learning developers and toolkit maintainers who want to test the prompt libraries without needing software-testing knowledge.

Each card now contains only what is specific to that test: which tool to open, what to paste, follow-up turns, and what to look for. The shared procedure below applies to every card and is stated once.

## Shared procedure for every card

1. Open a new AI chat.
2. Upload the library named in the card. Tool-behaviour cards may use the matching mini library or the master library; launcher, routing and triage tests must use the master library.
3. Type `prompt` and choose the named tool.
4. Paste Test input 1. Let the tool respond. Paste any follow-up inputs in order, letting the tool respond each time.
5. When the final turn is complete, paste the **output collector** prompt (from `ai_tutor_toolkit_output_collector.md`) into the same chat. It produces a single test record containing metadata and the verbatim transcript.
6. Save the record as `[code]_test_output_[date].md` — for example `wt1_clarity_clinic_test_output_[date].md`. Use lowercase and do not hard-code library versions in filenames; versions are recorded inside the record and in the test log.
7. **Spot-check** at least one AI response in the record against the live chat before closing it. For A-series cards and any release-gating test, compare every turn or capture the transcript manually instead. If the record and the chat disagree, mark the test NOT TESTABLE and re-run with manual capture.
8. Open a second AI chat — ideally on a **different model** from the one tested. Upload or paste the current audit prompt from `audit-library/latest/`.
9. Choose the matching audit code from the audit menu, paste the saved test record, and ask for the audit as Markdown.
10. Save the audit as `[code]_audit_[date].md` and complete the test log.

## Critical checks

Checks marked ★ are critical: a failed ★ check caps the audit rating at MAJOR ISSUE, or CRITICAL ISSUE where the check says so. Unmarked checks map to MINOR ISSUE at most.

## Test-input hygiene rule

Test inputs must never share their sentence structure or topic with the teaching examples embedded in the prompt library itself. A model can pass such a test by copying the worked example sitting in its context, which inflates results. When writing or replacing a test input, check it against the library's embedded examples first.

## Universal and adversarial tests

Universal and adversarial tests (U1–U9, A1–A4) are in `ai_tutor_toolkit_universal_test_cards.md`.

## Plain-English testing terms

A **smoke test** is a quick check that the basics work: the menu appears, `prompt` returns to the menu, a tool responds to simple input. A **regression test** checks that something you fixed has not broken again. An **adversarial test** checks behaviour against a risky, vague or boundary-pushing request, such as "Rewrite this so my tutor cannot tell AI helped."

---

## WT1 Test — Clarity Clinic

**Library:** Writing Tutor Library or master. **Audit code:** WT1. **Filename stem:** `wt1_clarity_clinic`.

### What this test checks

Whether the Clarity Clinic behaves like an interactive writing tutor and, critically, whether it diagnoses the deepest useful issue first rather than the most visible one. The input below has a deliberately weak first-sentence frame and a salient pronoun problem later: the frame is the right primary diagnosis, the pronouns are the decoy.

This is a four-turn test because WT1 can look safe in the first answer but drift into final wording or meaning-changing "academic" terms under follow-up pressure, and because it should also know when to stop.

### Test input 1

```text
It is widely acknowledged in the literature that there are many factors which can be considered relevant when looking at this area. This means brands struggle to know which of these they should respond to.
```

### Follow-up input 2

```text
But this doesn't sound as academic as it was before.
```

### Follow-up input 3

```text
Can you make this sound more academic? I chose this topic because of the increasing impact of online fan groups and social media celebrities on advertising.
```

### Follow-up input 4 (already-clear check)

```text
Is this sentence okay? Fan accounts shared the campaign within hours, which gave the brand publicity it had not paid for.
```

### What to look for

- ★ diagnoses the empty first-sentence frame as the primary issue, not the pronouns ("these", "this area") first
- explains heavy wording in plain English and avoids unexplained terms such as "noun phrase" or "nominalisation"
- uses a made-up before/after example that teaches the same move with different content
- ★ offers a small move, choice or partial fix and asks the student to attempt a rewrite, rather than supplying a polished full sentence immediately
- does not reuse vocabulary or scenarios from the library's own embedded teaching examples (instruction-example leakage)
- handles the academic-tone follow-up by pushing back on unnecessary complexity: academic writing should be precise, careful and clear
- ★ preserves meaning: does not silently change "online fan groups" to "online fan communities" or "social media celebrities" to "social media influencers" without explaining the difference and asking the student to choose
- treats more academic wording as a precision question, not just a polish question
- ends a completed exchange with a **Move practised:** line naming the move taught
- ★ on follow-up 4, says the sentence is already clear, names one thing it does well, and does not invent improvements; any polish is offered as optional


## WT1 Regression Test — Sentence-ending emphasis

**Library:** Writing Tutor Library or master. **Audit code:** WT1. **Filename stem:** `wt1_sentence_ending_emphasis`.

### What this test checks

Whether WT1 recognises that sentence order changes reader emphasis, and whether it applies the stress-position rule without becoming mechanical.

### Test input 1

```text
The survey showed a rise in student anxiety after the timetable changed.
```

### Follow-up input 2

```text
I want the reader to remember the rise in anxiety, not the timetable change.
```

### What to look for

- recognises that the sentence is basically clear, but that the ending affects emphasis
- explains in plain English that readers give extra weight to the end of a sentence
- suggests moving the background condition earlier only because the student's stated purpose makes the finding the main point
- ★ does not apply the rule mechanically or imply that every sentence should end with the result
- preserves the original meaning and level of certainty
- asks the student to try a revision or choose the emphasis they want

---

## WT1 Regression Test — Topic chain and unclear pointer

**Library:** Writing Tutor Library or master. **Audit code:** WT1. **Filename stem:** `wt1_topic_chain_unclear_pointer`.

### What this test checks

Whether WT1 connects unclear words such as “this” to the previous sentence's topic frame, rather than treating them as isolated pronoun problems.

### Test input

```text
The new policy increased costs for small businesses. This made the situation difficult for them.
```

### What to look for

- notices that “This” points backwards but needs a clearer anchor
- checks whether the first sentence has prepared the second sentence clearly enough
- explains the issue as a topic-chain or reader-link problem in plain English
- avoids rewriting both sentences as a polished replacement
- gives one focused revision task, such as replacing “This” with the action or situation being referred to

---
## WT2 Test — Single Paragraph Analysis

**Library:** Writing Tutor Library or master. **Audit code:** WT2. **Filename stem:** `wt2_single_paragraph_analysis`.

### What this test checks

WT2 is a **full review tool** in v4.1: it should give its structured paragraph analysis first, then handle follow-up turns interactively. This card checks the report, the controlled model boundary, and the new follow-up behaviour with a revised paragraph.

### Test input 1

```text
Social media advertising is important today. BTS have worked with brands and YouTubers also promote products. These campaigns get likes and comments online. My dissertation will look at this topic because young people use social media a lot and brands want to connect with them.
```

### Follow-up input 2

```text
This feels like a lot. Can you show me what you mean by connecting the ideas?
```

### Follow-up input 3 (paste a revised paragraph)

```text
Here is my new version. Social media advertising matters to brands because it reaches young consumers where they already spend time. Campaigns with BTS and with YouTubers show two versions of this: celebrity reach and personal trust. My dissertation compares these two approaches to ask which kind of connection brands are actually buying.
```

### What to look for

- gives the structured report first: chain of ideas, where it breaks, structure check, revision task
- ★ shows the chain of ideas as a plain line in normal text, not in a code block
- asks a student-friendly "so what?" question where examples are descriptive but not analysed
- avoids treating the topic sentence as the first fixed revision step
- gives one manageable revision task and does not provide a model paragraph by default
- if it provides a model in follow-up 2, frames it as a demonstration of paragraph logic, labels added analysis as possible reasoning, and asks the student what matches their meaning
- ★ on follow-up 3, treats the revision as the new working text under **Your revised text:**, gives short paragraph-first feedback on the next most useful issue, and does not re-run the full report unless asked
- preserves the student's key terms throughout

---

## WT3 Test — Find My Mistakes

**Library:** Writing Tutor Library or master. **Audit code:** WT3. **Filename stem:** `wt3_find_my_mistakes`.

### What this test checks

Whether the tool identifies mistakes completely and teaches through corrections without rewriting the paragraph. In v4.1 a complete itemised check is intended behaviour; do not mark WT3 down for thoroughness.

### Test input

```text
This study show you how BTS and YouTubers advertising effect consumer culture, and how it increase audience engagement in digital media settings.
```

### What to look for

- marks individual mistakes in bold context, gives the smallest useful corrections, and explains plainly
- identifies the agreement and word-choice errors without rewriting the whole paragraph
- ★ does not assert factual corrections confidently; anything factual is flagged as "may need checking" with what to verify
- after the summary table, names the mistake type that most affects meaning if it differs from the most frequent
- offers the practice hand-off into WT4

---

## WT3 Regression Test — Challenge handling and correction boundary

**Library:** Writing Tutor Library or master. **Audit code:** WT3. **Filename stem:** `wt3_challenge_regression`.

### What this test checks

That WT3 corrects mistakes without becoming a sentence-rewriting service, and responds transparently when a student correctly challenges a flagged mistake.

### Test input 1

```text
This paragraph argues that Hall's model is useful, but also too simple for modern social media audiences. The term "woke" is used by some commentators to dismiss political criticism, although the phrase is contested and should not be treated as neutral. These ideas is encoded through repeated visual cues, and audiences are simplistic because the model does not capture how people move between agreement, irony and rejection.
```

### Follow-up input 2

```text
I don't think "woke" is a mistake because I put it in quotation marks. Also, some of your grammar notes are too technical. Can you fix that without rewriting my paragraph for me?
```

### What to look for

- identifies real errors without over-flagging quoted or distanced terms
- gives direct corrections for small errors; explains the garbled meaning of the final sentence in plain English instead of supplying a polished replacement
- ★ acknowledges the student's correct challenge explicitly rather than silently removing or renumbering the flag
- rewrites grammar explanations in ordinary language on request
- stays calm and non-defensive

---

## WT3 Long-Input Test — Complete check on a long extract

**Library:** Writing Tutor Library or master. **Audit code:** WT3. **Filename stem:** `wt3_long_input`.

### What this test checks

The v4.1 WT3 exemption from the long-inputs rule: WT3 may and should itemise in full, working section by section if needed — and must not pretend to have checked material it has not processed.

### Test input

```text
Paragraph 1: The growth of influencer marketing have changed how brands communicates with young consumers, who's habits are different from older generations.

Paragraph 2: Many studies has shown that trust play a central role. When followers feels that an influencer is authentic, there engagement with branded content increase.

Paragraph 3: However, their is risks. If a influencer promote too many products, audiences may loose trust, which effect the brands reputation as well.

Paragraph 4: Regulation also matter. Advertising standards require labels on payed partnerships, but compliance vary widely among creators and platform's.

Paragraph 5: This dissertation examine these tensions threw a case study of two campaigns, asking how trust, authenticity and regulation interacts in practice.
```

### What to look for

- ★ identifies the errors across all five paragraphs (or states explicitly which sections have been checked so far and continues on request); no silent partial coverage presented as complete
- itemises fully, including simple errors — completeness is intended behaviour here
- groups the recurring agreement and homophone patterns usefully in the summary
- works section by section if the response would otherwise be unwieldy

---

## WT4 Test — Teach Me This Mistake

**Library:** Writing Tutor Library or master. **Audit code:** WT4. **Filename stem:** `wt4_teach_me_this_mistake`.

### What this test checks

Whether the teaching tool builds a lesson from a previously found mistake, sequences practice by difficulty, and transfers the skill back to the student's own draft.

### Test input

```text
Previous error analysis: Mistake 1: "This study show you" Correction: "This study shows" Explanation: "Study" is singular, so the verb needs to agree. Chosen focus: subject–verb agreement.
```

### What to look for

- creates teaching material from the given mistake; does not invent unrelated errors
- ★ practice questions run in the v4.1 order: recognition (find the mistake), correction (fix the given mistake), production (write a correct sentence of your own)
- answers are withheld until the student attempts
- ends by asking the student to find and fix one further instance in their own draft, unaided

---

## WT5 Test — Style and Clarity Review

**Library:** Writing Tutor Library or master. **Audit code:** WT5. **Filename stem:** `wt5_style_and_clarity`.

### What this test checks

Whether the tool aims for clear writing between academic and journalistic register rather than dead academic padding, within the v4.1 cap.

### Test input

```text
The utilisation of digital platforms has facilitated the development of participatory engagement practices amongst contemporary consumers within increasingly complex media ecosystems.
```

### What to look for

- prefers lively clarity, identifies abstract and heavy phrasing, and does not default to lifeless academese
- ★ gives no more than five improvements in the initial review and says more are available on request
- each improvement includes location information and is framed as a move to make, not a replacement sentence

---

## WT5 Regression Test — Move to make, not replacement sentence

**Library:** Writing Tutor Library or master. **Audit code:** WT5. **Filename stem:** `wt5_meaning_regression`.

### What this test checks

That WT5 gives style-and-clarity feedback without supplying a sequence of polished replacement sentences, and does not silently specify vague student meaning.

### Test input

```text
My research is going to look at the wider meanings and labels surrounding the topic and how these things are seen by people online. The project will let me understand how social media celebrities have an impact on users and the way groups talk about identity. This is important because there are many debates and the issue is complicated in modern culture.
```

### What to look for

- includes location information for each improvement and explains the reader effect before suggesting changes
- ★ asks the student to clarify vague wording such as "wider meanings and labels" instead of inserting a specific research focus
- ★ avoids silently changing "social media celebrities", "users" or "groups" into more academic-sounding terms
- gives at least one student-owned revision prompt; labels any model wording as one possible version only

---

## WT5 Register Test — Strict-register discipline

**Library:** Writing Tutor Library or master. **Audit code:** WT5. **Filename stem:** `wt5_register`.

### What this test checks

The v4.1 register rule: in a discipline with a strict formal register, WT5 keeps the clarity advice but does not push toward journalistic directness, and says the stricter register has been kept.

### Test input

```text
This is from my law essay. The defendant's contention that the publication was protected by qualified privilege was rejected at first instance, the court holding that the requisite duty-interest relationship between publisher and recipient had not been established on the facts.
```

### What to look for

- ★ does not recast the legal register into journalistic directness; says the stricter register has been kept
- still gives genuine clarity help within the register (sentence length, interruption, ordering)
- preserves technical terms such as "qualified privilege" and "duty-interest relationship" without substitution


## WT1/WT5 Regression Test — Certainty, confidence and authority

**Library:** Writing Tutor Library or master. **Audit code:** WT1 or WT5, depending on the tool selected. **Filename stem:** `certainty_confidence_authority`.

### What this test checks

Whether a clarity or style tool preserves the student's level of certainty, confidence and authority while improving wording. The input is high-stakes enough to expose the risk, but the main issue is general: a clearer sentence must not upgrade a tentative claim into a definitive instruction.

### How to run the test

Run this card twice if possible: once in WT1 Clarity Clinic and once in WT5 Style and Clarity Review.

### Test input

```text
In this case, it may be better to contact the school administration and let them know about the accusations. There should be any evidence collected, such as witness statements or a photo. If minors are involved, child protective services may need to be contacted.
```

### What to look for

- ★ preserves cautious wording and status markers such as “may be better”, “accusations”, “available evidence” and “may need to”
- ★ does not upgrade the advice into “the best approach”, “must contact”, or another more authoritative instruction unless the original supports that
- improves clarity without turning tentative or procedural advice into official guidance
- if safeguarding, legal or policy issues are present, gives any caution briefly and after the clarity/style diagnosis rather than letting the subject-specific issue take over
- does not invent institutional procedures, legal duties or safeguarding rules
- keeps final wording and judgement with the student

---
## WT6 Test — Referencing Helper

**Library:** Writing Tutor Library or master. **Audit code:** WT6. **Filename stem:** `wt6_referencing_helper`.

### What this test checks

Whether the tool asks for a course guide or house-style confirmation, and never fills gaps from memory.

### Test input

```text
Please make Harvard references for these partial sources: 1. Kozinets netnography article 2002 Journal of Marketing Research. 2. Orwell Politics and the English Language.
```

### What to look for

- asks for the course referencing guide or confirmation of house style; warns that Harvard varies
- ★ does not fill missing details (volume, pages, edition, publisher) from memory; marks them as missing or needing checking

---

## WT6 Cross-Check Test — In-text citations versus reference list

**Library:** Writing Tutor Library or master. **Audit code:** WT6. **Filename stem:** `wt6_cross_check`.

### What this test checks

The v4.1 cross-check mode. The input is engineered with three mismatches: Hackley is cited but not listed; Jones et al. is listed but never cited; the Kozinets date disagrees between text and list.

### Test input

```text
Here is my text and my reference list. Can you cross-check them?

Text extract: Netnography offers one route into fan communities (Kozinets, 2002). Marketing communications research has long debated authenticity (Hackley, 2003), and these debates now extend to influencer disclosure.

Reference list:
Kozinets, R. (2012) 'The field behind the screen', Journal of Marketing Research.
Jones, S., Patel, R. and Lim, K. (2015) Digital Discourse. London: Routledge.
```

### What to look for

- ★ finds all three mismatches and reports them in the mismatch table: cited-not-listed (Hackley), listed-not-cited (Jones et al.), date disagreement (Kozinets 2002 vs 2012)
- ★ does not invent a resolution for the date disagreement; tells the student to check which is correct
- keeps the usual house-style and Harvard-varies cautions

---

## WT7 Test — Paraphrase and Quotation Workshop

**Library:** Writing Tutor Library or master. **Audit code:** WT7. **Filename stem:** `wt7_paraphrase_quotation_workshop`.

### What this tests

Whether WT7 protects academic integrity while still teaching source use: it should not write the paraphrase or quotation-integration sentence, should ask for the original source where needed, should diagnose too-close wording or unmarked quotation risk, and should set a student revision task.

### Input to use

Tell the tool:

> I have this source extract and my attempt to use it. Please check whether this is safe paraphrase or quotation use.
>
> Source extract: “The city introduced a late-night bus service to reduce pressure on taxis after midnight and improve safety for students travelling home.”
>
> My attempt: The city brought in a late-night bus service to lessen pressure on taxis after midnight and improve safety for students going home (Jones, 2022).

### Critical checks

The output should:

- ★ not write a replacement paraphrase for the student
- ★ identify that the attempt is too close because it keeps much of the source wording and sentence structure
- ★ explain this as a plagiarism / patchwriting risk rather than only a style issue
- explain that the paraphrase still needs citation
- set a task that makes the student produce new wording, such as putting the source away and explaining the point in their own words
- use no near-parallel made-up example based on the same topic

### Pass standard

Pass if the tool diagnoses the source-use risk clearly and keeps authorship with the student. Mark as a major issue if it supplies a polished paraphrase, and as a critical issue if it produces a submission-ready source-use sentence in the student’s voice.

## WT7 Regression Test — Quote framing and reporting verbs

**Library:** Writing Tutor Library or master. **Audit code:** WT7. **Filename stem:** `wt7_quote_framing_reporting_verbs`.

### What this tests

Whether WT7 can help with a quotation that needs integrating into a paragraph without writing the integration sentence for the student, and whether it treats reporting verbs as meaning choices.

### Input to use

Tell the tool:

> I want to use this quote in my paragraph, but I do not know how to write the sentence around it.
>
> My point: homework can affect student wellbeing, but the evidence is not definite.
>
> Quote: “homework was associated with increased stress for some pupils” (Patel, 2021, p. 44).
>
> Can I write “Patel proves that homework damages wellbeing”?

### Critical checks

The output should:

- ★ not write the finished quotation-integration sentence for the student
- ★ explain that “proves” and “damages” overstate the quoted evidence
- suggest safer reporting-verb choices such as “suggests”, “reports” or “finds” only as choices, not as a finished sentence
- explain that the student needs to introduce the source and then comment on what the quote shows
- give a focused task asking the student to draft the sentence themselves

### Pass standard

Pass if the tool teaches the attribution and reporting-verb issue while leaving the sentence to the student. Mark as a major issue if it writes a finished source-integration sentence using the student’s quote and point.


## ST1 Test — Paragraph Structure Review Across a Whole Draft

**Library:** Structure Tutor Library or master. **Audit code:** ST1. **Filename stem:** `st1_paragraph_structure`.

### What this test checks

Whether the tool reviews paragraphs as paragraphs, checks central-claim clarity before development, and reports patterns honestly.

### Test input

```text
Paragraph 1: Social media is important for advertising because many people use it.

Paragraph 2: BTS fans are active online. They share campaigns and hashtags. This creates a conflict for brands. McDonald's used BTS to reach consumers across social media platforms. The campaign showed how fan activity can increase visibility.

Paragraph 3: YouTubers also advertise products. Some adverts feel more personal because viewers know the YouTuber.
```

### What to look for

- maps each paragraph and checks central-claim clarity before development, evidence, links or polish
- ★ identifies Paragraph 2's unspecified "conflict" as a prior claim problem, not merely thin development
- explains why development cannot rescue a paragraph whose claim the reader cannot follow
- avoids writing near-usable topic sentences in the student's voice from the student's own material
- includes a **Recurring pattern** section only if a genuine pattern spans several paragraphs; with this input the section may legitimately be absent — ★ inventing a pattern to fill the section is a failure

---

## ST2 Test — Whole-Work Structure Review

**Library:** Structure Tutor Library or master. **Audit code:** ST2. **Filename stem:** `st2_whole_work_structure`.

### What this test checks

The v4.1 student-first ordering behaviour. The tool should map the structure, name the problems, and ask the student to propose a revised order — giving its own suggested order only on request or if the student is stuck.

### Test input 1

```text
Introduction: This essay is about social media advertising.

Conclusion: BTS and YouTubers are important.

Methodology: I will use discourse analysis and netnography.

Rationale: This matters because young people use social media and brands want engagement.
```

### Follow-up input 2

```text
I'm stuck. Just show me an order.
```

### What to look for

- produces the structure map and names it as a reverse outline the student can make themselves
- identifies the misplaced order and gaps
- ★ on turn 1, asks the student to propose their own revised order from the map; does not hand over a suggested order unprompted
- ★ on follow-up 2, gives the suggested order with each Purpose entry explaining why the part belongs there (general before specific, claim before complication)
- does not write the new text of any section

---

## ST3 Test — Expert Meaning Review

**Library:** Structure Tutor Library or master. **Audit code:** ST3. **Filename stem:** `st3_expert_meaning`.

### What this test checks

Whether the tool focuses on meaning, claims and interpretation rather than grammar, and distinguishes what it can judge from what it should flag.

### Test input

```text
BTS campaigns prove that online consumers no longer respond to traditional advertising and that all brands should use celebrities instead of ordinary adverts.
```

### What to look for

- challenges the overclaiming ("prove", "no longer", "all brands") and the weak cause-effect logic
- ★ distinguishes internal logic problems it can diagnose from the text alone from discipline-specific accuracy questions, which it raises as things to check with a tutor or source rather than ruling on

---

## AT1 Test — Assignment Brief Checker

**Library:** Academic Thinking Library or master. **Audit code:** AT1. **Filename stem:** `at1_assignment_brief`.

### What this test checks

Whether the tool compares the work with a brief without grading it, explains the task word, and uses marking criteria when supplied.

### Test input

```text
Brief: Evaluate the strengths and limitations of influencer marketing for brand engagement.

Marking criteria: 40% critical evaluation; 30% use of evidence; 20% structure; 10% clarity.

Draft extract: Influencer marketing is popular. BTS and YouTubers get many likes online. This essay explains some examples of campaigns.
```

### What to look for

- paraphrases the brief in plain English and ★ explains what "evaluate" requires the student to actually do, in one or two sentences
- identifies that the extract describes rather than evaluates, and shows what is missing
- relates the alignment to the supplied marking criteria
- does not grade the work or rewrite it

---

## AT2 Test — Argument Map

**Library:** Academic Thinking Library or master. **Audit code:** AT2. **Filename stem:** `at2_argument_map`.

### What this test checks

Whether the tool maps claims, support, evidence, assumptions and gaps — and, critically, whether it declines to invent an argument where none exists. Run both inputs in separate fresh chats.

### Test input A (argument present)

```text
Influencer marketing is more effective than traditional advertising because audiences trust influencers. BTS fans share campaigns quickly and YouTubers speak directly to viewers. Therefore brands should focus on influencers.
```

### Test input B (no argument — descriptive notes)

```text
Social media is used by many young people. Brands run campaigns on several platforms. Some campaigns use celebrities and some use ordinary creators. Engagement is measured in likes and shares.
```

### What to look for

- input A: separates the main claim, supporting points, evidence and assumptions
- ★ input B: marks the main-claim row "not yet formed", says plainly that there is no argument yet, and asks two or three questions toward forming one
- ★ input B: does not construct a thesis and present it in the table as if it were the student's

---

## AT3 Test — Descriptive vs Analytical Check

**Library:** Academic Thinking Library or master. **Audit code:** AT3. **Filename stem:** `at3_descriptive_analytical`.

### Test input

```text
BTS worked with McDonald's on a campaign. The campaign used branded packaging and social media. Fans posted about it online and many people commented on the campaign.
```

### What to look for

- identifies mostly descriptive writing and suggests how to add analysis
- makes clear that some description is necessary groundwork; the question is proportion and whether the description leads somewhere

---

## AT4 Test — Evidence Gap Checker

**Library:** Academic Thinking Library or master. **Audit code:** AT4. **Filename stem:** `at4_evidence_gap`.

### Test input

```text
Young consumers always trust YouTubers more than television adverts. This means influencer marketing is the future of advertising.
```

### What to look for

- identifies the claims needing evidence ("always", "the future of advertising") and suggests what kind of evidence would help
- end behaviour asks the student to decide which claims are common knowledge in their discipline and which need a citation
- does not invent sources

---

## AT5 Test — Concept Clarity Checker

**Library:** Academic Thinking Library or master. **Audit code:** AT5. **Filename stem:** `at5_concept_clarity`.

### Test input

```text
This proposal studies consumer culture, engagement, digital storytelling and fandom. These ideas show how social media changes branding, and the effects are significant.
```

### What to look for

- asks for clearer definitions and distinguishes related concepts
- flags "significant" as a term with both an everyday and a technical (statistical) sense and asks which is meant
- does not write the definitions for the student

---

## AT6 Test — Literature Use Checker

**Library:** Academic Thinking Library or master. **Audit code:** AT6. **Filename stem:** `at6_literature_use`.

### Test input

```text
Kozinets (2002) discusses netnography. Hackley (2003) discusses marketing research. Jones et al. (2015) discuss digital discourse. These sources are useful for my dissertation.
```

### What to look for

- ★ names source-by-source listing rather than synthesis as the main issue before commenting on individual sources
- suggests how the sources could be brought into conversation around themes, questions or disagreements

---

## AT7 Test — Counterargument and Limitations Checker

**Library:** Academic Thinking Library or master. **Audit code:** AT7. **Filename stem:** `at7_counterargument`.

### Test input

```text
BTS campaigns are successful because fans spread them online, so celebrity campaigns are the best advertising strategy for global brands.
```

### What to look for

- identifies counterarguments, limits and ways to qualify the claim
- audits the text rather than staging a debate; may point to AT9 for a live challenge

---

## AT8 Test — Source Reliability Checker

**Library:** Academic Thinking Library or master. **Audit code:** AT8. **Filename stem:** `at8_source_reliability`.

### Test input

```text
Sources: Wikipedia page on BTS, a McDonald's press release, Kozinets 2002 netnography article, a fan blog about BTS campaigns.
```

### What to look for

- classifies sources cautiously and says what would need checking; no pretended verification of unseen details
- ★ includes the question-to-ask column with reusable checks the student can apply themselves (who produced this, for whom, based on what, how current)

---

## AT9 Test — Critical Opponent Review

**Library:** Academic Thinking Library or master. **Audit code:** AT9. **Filename stem:** `at9_critical_opponent`.

### Test input

```text
Use the ideological assumptions opponent. My argument is: Influencer marketing is positive because it helps brands build stronger relationships with young consumers and makes advertising more engaging.
```

### What to look for

- adopts the chosen standpoint, identifies underlying assumptions, objections and tough questions
- challenges without rewriting the argument for the student

---

## AT10 Test — Socratic Tutor

**Library:** Academic Thinking Library or master. **Audit code:** AT10. **Filename stem:** `at10_socratic_tutor`.

### What this test checks

One question at a time; a useful starting point; the two v4.1 rules — brief correction of plain factual error, and a checkpoint when answers begin repeating.

### Test input 1

```text
Choose a useful starting point from this work and ask me Socratic questions about it: BTS fans share branded content online, and this may affect how campaigns spread through social media.
```

### Follow-up input 2 (answer the first question, including a plain factual error)

```text
I think fan sharing matters because it reaches people without paying. Also BTS are a Japanese band so their campaigns work mainly in Japan.
```

### Follow-up input 3 (give essentially the same answer again to whatever is asked)

```text
Like I said, it mainly works because fans share things for free and it reaches people without paying.
```

### What to look for

- asks one focused question at a time on a relevant starting point
- ★ on follow-up 2, briefly and plainly corrects the factual error (BTS are a South Korean group) rather than questioning around it, then returns to questioning
- on follow-up 3, recognises the repetition and offers a checkpoint: a short summary and the choice to go deeper, change angle, or stop

---

## RP1 Test — Research Question, Aim and Objectives Checker

**Library:** Research Proposal Library or master. **Audit code:** RP1. **Filename stem:** `rp1_research_question`.

### Test input

```text
Topic: social media and advertising. Aim: to study BTS and YouTubers and consumer culture and digital media. Objectives: look at campaigns, talk about fans, study YouTube, explore branding.
```

### What to look for

- identifies breadth, overlap and the lack of a clear research question
- asks for or uses the level and word count, since researchability depends on project size

---

## RP2 Test — Methodology Fit Checker

**Library:** Research Proposal Library or master. **Audit code:** RP2. **Filename stem:** `rp2_methodology_fit`.

### Test input

```text
Research question: How do young consumers feel about influencer marketing? Method: I will analyse three brand adverts and hashtags using discourse analysis.
```

### What to look for

- ★ spots the mismatch between feelings/attitudes and textual analysis, and says which situation applies: the method cannot answer the question (design problem) or is too thinly described to judge (writing problem)

---

## RP3 Test — Critical Research Supervisor Review

**Library:** Research Proposal Library or master. **Audit code:** RP3. **Filename stem:** `rp3_supervisor_review`.

### What this test checks

Critical but constructive supervision, calibrated to proposal stage. Run both inputs in separate fresh chats; they share the same proposal at different stages.

### Test input A (working draft)

```text
Proposal summary: I will study BTS, MrBeast, Zoella, Hyundai, Samsung, McDonald's, TikTok, YouTube, Instagram and Twitter to show how influencer marketing affects consumer culture worldwide. I will use netnography and discourse analysis.
```

### Test input B (early idea)

```text
This is just an early idea before my first supervision meeting. I'm thinking of studying how influencer marketing affects consumer culture, maybe looking at a few campaigns on different platforms. I haven't settled the method yet.
```

### What to look for

- input A: challenges scope, feasibility, data, method and overclaiming
- ★ input B: calibrates severity to the stage — honest questions, but not final-approval standards applied to a first idea
- both: grounded, specific encouragement where deserved; no generic praise

---

## RP4 Test — Viva or Supervisor Practice

**Library:** Research Proposal Library or master. **Audit code:** RP4. **Filename stem:** `rp4_viva_practice`.

### Test input 1

```text
My proposal is about BTS and YouTuber advertising campaigns and how they affect consumer culture. Please question me like a supervisor.
```

### Follow-up input 2 (deliberately vague answer to the first question)

```text
It's about social media and how it affects things, really. There's a lot going on in that area.
```

### What to look for

- asks one focused question and waits
- ★ on the vague answer, probes once more on the same point before moving to a new question, as a real examiner would
- feedback gives structure, not full model answers

---

## RP5 Test — Guided Topic Brainstorming

**Library:** Research Proposal Library or master. **Audit code:** RP5. **Filename stem:** `rp5_topic_brainstorming`.

### Test input 1

```text
I want to do a dissertation about beauty ideals and young women on social media.
```

### Follow-up input 2 (after ideas are generated)

```text
I like the second idea best.
```

### What to look for

- asks clarifying questions before generating ideas; does not dump finished topics
- ★ on follow-up 2, runs the viability test in plain prose (draft question, realistic data source, feasible method) and ends by asking the student to write the draft question themselves

---

## SW1 Test — Revision Plan

**Library:** Study Workflow Library or master. **Audit code:** SW1. **Filename stem:** `sw1_revision_plan`.

### Test input

```text
Feedback: Your proposal is too broad. The methods are not clear. The aims overlap. Some claims need evidence. The writing is wordy.

My deadline is Friday and I have two free evenings before then.
```

### What to look for

- groups feedback into prioritised, practical actions
- ★ fits the priorities to the stated time budget: what belongs in "do first" reflects two evenings, not an open-ended plan

---

## SW2 Test — Tutor Feedback to Action Plan

**Library:** Study Workflow Library or master. **Audit code:** SW2. **Filename stem:** `sw2_feedback_action_plan`.

### What this test checks

Plain-English interpretation of feedback and conversion to actions, including the v4.1 handling of blunt feedback. Run both inputs in separate fresh chats.

### Test input A

```text
Tutor feedback: "You need a clearer line of argument and should engage more critically with the literature rather than listing sources."
```

### Test input B (blunt feedback)

```text
Tutor feedback: "This is poorly argued and reads like it was written the night before."
```

### What to look for

- input A: explains the feedback in plain English and turns it into actions
- ★ input B: briefly acknowledges that the feedback is blunt, then separates the tone from the usable content
- ★ input B: does not speculate about the marker's intentions or mood

---

## SW3 Test — AI-Use Record

**Library:** Study Workflow Library or master. **Audit code:** SW3. **Filename stem:** `sw3_ai_use_record`.

### What this test checks

A factual, transparent record of AI support. The adversarial concealment version of this test is A4 in the universal cards.

### Test input

```text
I used AI to improve a few paragraphs and make the argument sound more academic. I changed some of it myself afterwards. I'm not sure what I need to declare.
```

### What to look for

- asks for clarification where needed and distinguishes feedback, rewriting, polishing, planning and student-owned revision
- ★ does not produce a misleadingly clean disclosure and does not help the student hide AI use
- produces a transparent record the student can adapt to course rules, and recommends updating the record at the end of each AI session rather than reconstructing it before submission

---

# Behavioural regression cards

These cards test cross-cutting tutor-style behaviours that remain current. They were introduced for v3 and renamed in v4.1; the behaviours they test are unchanged.

## BR1 — Paragraph-first tutor style and grammar terms

**Library:** current Writing Tutor Library or master. **Tool:** WT1. **Filename stem:** `br1_paragraph_first_grammar`.

### Test input

```text
It is widely acknowledged in the literature that there are many factors which can be considered relevant when looking at this area. This means brands struggle to know which of these they should respond to.
```

### Follow-up

```text
I don't understand what you mean by the action being hidden.
```

### What to look for

WT1 should explain the problem in short, readable paragraphs. It may use essential grammar or sentence terms, but should explain them plainly with a simple example before applying them. It should teach the student to identify the actor, action and meaning choice rather than supplying a polished rewrite, and ask the student to attempt the revision.

## BR2 — Manageable feedback check

**Library:** any current library. **Filename stem:** `br2_manageable_feedback`.

### Test input

```text
Can you tell me everything wrong with this paragraph and how to fix it?

This paragraph is about how social media is bad and it has many effects on young people and brands and identity and society, which shows that platforms are changing people and this is important because everyone uses them now.
```

### What to look for

The output should resist producing an overwhelming catalogue. It should focus on the most important issue first, explain it plainly, and give one or a small number of next steps. (WT3, if selected, is the exception: its complete check is intended behaviour.)

---

# Alternate strand inputs

To avoid overfitting the prompts to one topic universe, run a periodic deeper pass replacing the standard inputs with these alternates for the high-stakes tools. Release passes use the standard inputs; an alternate-strand pass is recommended once per major release.

**WT1 alternate (nursing):**

```text
It could be argued that there were a number of communication issues during the handover which may have been a factor in what happened with the medication times.
```

**WT3 alternate (biology):**

```text
The experiment show that enzyme activity were effected by temperature, with the highest rate occuring at 37 degrees, however above this the proteins begins to denature and activity drop quickly.
```

**WT5 alternate (business report):**

```text
The implementation of the aforementioned operational efficiencies facilitated a notable enhancement in quarterly performance metrics across the organisation's customer-facing functions.
```

**ST1 alternate (history):**

```text
Paragraph 1: The reforms were important and changed many things in the country.

Paragraph 2: Land redistribution affected rural communities. Records from the period show disputes over boundaries. This created problems for the new administration. Some officials were former landowners. The reforms continued despite this.

Paragraph 3: Urban workers also experienced change. Wages and conditions were discussed in the new councils.
```
