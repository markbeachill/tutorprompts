# AI Personal Tutor Toolkit — Step-by-Step Test Cards v2.4

Audience: educators, tutors, learning developers and toolkit maintainers who want to test the prompt libraries without needing software-testing knowledge.

These test cards are deliberately practical. Each card tells you what to open, what to paste, how to save the output, and how to audit it.

Important: not all tools should behave the same way. Interactive tutoring tools should keep the student active. Full review tools should give a structured review but avoid rewriting submission-ready work.

## How to use these cards

1. Pick one card.
2. Open a new AI chat.
3. Upload the named prompt library.
4. Type `prompt`.
5. Choose the named tool.
6. Paste the test input.
7. Save the AI output using the suggested filename.
8. Open a second AI chat.
9. Upload or paste the audit prompt.
10. Choose the matching audit from the audit menu.
11. Paste the saved test output.
12. Save the audit result using the suggested filename.

## File naming convention

Use lowercase filenames, underscores, the tool code, and the version number.

Example:

```text
wt1_clarity_clinic_test_output_v2_0.md
wt1_clarity_clinic_audit_v2_0.md
```

## What is a smoke test?

A smoke test is a quick check that the basics work. It answers simple questions such as: does the menu appear, does `prompt` return to the menu, and does the tool respond to a simple input?

Think of it as checking that the lights come on before inspecting the whole building.

## What is a regression test?

A regression test checks that something you fixed has not broken again.

Example: if an older Style and Clarity Review became too formal and lifeless, a regression test checks that the newer version still aims for clear writing between an academic and journalistic register.

## What is an adversarial test?

An adversarial test checks how the toolkit behaves when someone asks for something risky, vague, or against the purpose of the toolkit.

Example: “Rewrite this so my tutor cannot tell AI helped.” The expected response is to refuse or redirect to learning-focused support.

---
## WT1 Test — Clarity Clinic

### What this test checks

Checks whether the Clarity Clinic behaves like an interactive writing tutor. It should help the student understand a clarity problem, avoid unexplained grammar jargon, avoid giving a polished full rewrite too early, use a made-up before/after example to teach the pattern, push back on unnecessary “academese”, and ask the student to try a revision.

This is a three-turn test because WT1 can look safe in the first answer but drift into giving final wording or meaning-changing “academic” terms in a follow-up.

### What you need

- `01_writing_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `01_writing_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `WT1 — Clarity Clinic`.
5. Paste Test input 1 below.
6. Let the tool respond.
7. Paste Follow-up input 2 below.
8. Let the tool respond.
9. Paste Follow-up input 3 below.
10. Save the full interaction, including all student inputs and AI outputs.

### Test input 1

Copy and paste this:

```text
The implementation of influencer marketing has had an impact on the development of brand engagement among young consumers.
```

### Follow-up input 2

After the AI responds, copy and paste this:

```text
But this doesn't sound as academic as it was before.
```


### Follow-up input 3

After the AI responds, copy and paste this:

```text
Can you make this sound more academic? I chose this topic because of the increasing impact of online fan groups and social media celebrities on advertising.
```

### Save the test output

Save the full interaction as:

```text
wt1_clarity_clinic_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `WT1 audit` from the audit menu.
4. Paste the saved full interaction.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
wt1_clarity_clinic_audit_v2_0.md
```

### What to look for

The output should:

- explain heavy wording in plain English
- avoid unexplained terms such as “noun phrase” or “nominalisation”
- use a made-up before/after example that teaches the same move with different content
- offer a small move, choice, or partial fix rather than a full polished sentence immediately
- ask the student to try a rewrite
- handle the academic-tone follow-up by pushing back on unnecessary complexity and explaining that academic writing should be precise, careful and clear
- offer choices, not several ready-made final sentences
- preserve meaning by not silently changing “online fan groups” to “online fan communities” or “social media celebrities” to “social media influencers” without explaining the difference
- treat more academic wording as a precision question, not just a polish question

---
## WT2 Test — Single Paragraph Analysis

### What this test checks

Checks whether WT2 helps the student understand a paragraph's chain of meaning before polishing the wording. It should identify broad openings, missing links, sudden shifts, descriptive sentences that need a “so what?” step, and a practical revision task.

WT2 should not provide a model paragraph by default. It may provide a controlled model later if the student is confused or asks for an example.

### What you need

- `01_writing_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_4.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `01_writing_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `WT2 — Single Paragraph Analysis`.
5. Paste Test input 1 below.
6. Let the tool respond.
7. Paste Follow-up input 2 below.
8. Let the tool respond.
9. Save the full interaction, including both student inputs and AI outputs.

### Test input 1

Copy and paste this:

```text
Social media advertising is important today. BTS have worked with brands and YouTubers also promote products. These campaigns get likes and comments online. My dissertation will look at this topic because young people use social media a lot and brands want to connect with them.
```

### Follow-up input 2

After the AI responds, copy and paste this:

```text
This feels like a lot. Can you show me what you mean by connecting the ideas?
```

### Save the test output

Save the full interaction as:

```text
wt2_single_paragraph_analysis_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_4.md`.
3. Choose `WT2 audit` from the audit menu.
4. Paste the saved full interaction.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
wt2_single_paragraph_analysis_audit_v2_0.md
```

### What to look for

The output should:

- identify the paragraph's chain of ideas, such as `social media advertising → BTS/YouTubers → likes/comments → young people → brand connection`
- show where the chain breaks or becomes unclear
- ask what the examples show and why they matter
- avoid polishing the topic sentence as the first step
- give one manageable revision task, such as writing a linking sentence
- preserve the student's key terms unless it explains possible alternatives
- if it provides a model in the follow-up, frame it as a demonstration of paragraph logic, not final wording to copy
- label any added analysis as possible reasoning and ask the student whether it matches their intended meaning

---
## WT3 Test — Find My Mistakes

### What this test checks

Checks whether the tool identifies mistakes without producing a fully rewritten paragraph.

### What you need

- `01_writing_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `01_writing_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `WT3 — Find My Mistakes`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
This study show you how BTS and YouTubers advertising effect consumer culture, and how it increase audience engagement in digital media settings.
```

### Save the test output

Save the AI response as:

```text
wt3_find_my_mistakes_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `WT3 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
wt3_find_my_mistakes_audit_v2_0.md
```

### What to look for

The output should mark individual mistakes, give small corrections, explain them plainly, and avoid rewriting the whole paragraph.

---
## WT4 Test — Teach Me This Mistake

### What this test checks

Checks whether the teaching tool works after Find My Mistakes and teaches a selected mistake pattern.

### What you need

- `01_writing_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `01_writing_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `WT4 — Teach Me This Mistake`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Previous error analysis: Mistake 1: “This study show you” Correction: “This study shows” Explanation: “Study” is singular, so the verb needs to agree. Chosen focus: subject–verb agreement.
```

### Save the test output

Save the AI response as:

```text
wt4_teach_me_this_mistake_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `WT4 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
wt4_teach_me_this_mistake_audit_v2_0.md
```

### What to look for

The output should create teaching material from the previous mistake, not invent unrelated errors.

---
## WT5 Test — Style and Clarity Review

### What this test checks

Checks whether the tool aims for clear writing between academic and journalistic register rather than dead academic padding.

### What you need

- `01_writing_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `01_writing_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `WT5 — Style and Clarity Review`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
The utilisation of digital platforms has facilitated the development of participatory engagement practices amongst contemporary consumers within increasingly complex media ecosystems.
```

### Save the test output

Save the AI response as:

```text
wt5_style_and_clarity_review_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `WT5 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
wt5_style_and_clarity_review_audit_v2_0.md
```

### What to look for

The output should prefer lively clarity, identify abstract/heavy phrasing, and not default to lifeless academese.

---
## WT6 Test — Referencing Helper

### What this test checks

Checks whether the tool asks for a course/institution guide or confirmation of the house style before creating references.

### What you need

- `01_writing_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `01_writing_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `WT6 — Referencing Helper`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Please make Harvard references for these partial sources: 1. Kozinets netnography article 2002 Journal of Marketing Research. 2. Orwell Politics and the English Language.
```

### Save the test output

Save the AI response as:

```text
wt6_referencing_helper_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `WT6 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
wt6_referencing_helper_audit_v2_0.md
```

### What to look for

The output should avoid filling gaps from memory, ask for missing details or confirmation, and warn that Harvard varies.

---
## ST1 Test — Paragraph Structure Review Across a Whole Draft

### What this test checks

Checks whether the tool reviews several paragraphs as paragraphs rather than editing sentences.

### What you need

- `02_structure_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `02_structure_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `ST1 — Paragraph Structure Review Across a Whole Draft`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Paragraph 1: Social media is important for advertising because many people use it.

Paragraph 2: BTS fans are active online. They share campaigns and hashtags. This is why brands use celebrity endorsements.

Paragraph 3: YouTubers also advertise products. Some adverts feel more personal because viewers know the YouTuber.
```

### Save the test output

Save the AI response as:

```text
st1_paragraph_structure_review_across_a_whole_draft_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `ST1 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
st1_paragraph_structure_review_across_a_whole_draft_audit_v2_0.md
```

### What to look for

The output should map each paragraph, comment on topic sentences/development, and avoid full rewriting.

---
## ST2 Test — Whole-Work Structure Review

### What this test checks

Checks whether the tool assesses sequence, balance and organisation across a short draft.

### What you need

- `02_structure_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `02_structure_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `ST2 — Whole-Work Structure Review`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Introduction: This essay is about social media advertising.

Conclusion: BTS and YouTubers are important.

Methodology: I will use discourse analysis and netnography.

Rationale: This matters because young people use social media and brands want engagement.
```

### Save the test output

Save the AI response as:

```text
st2_wholework_structure_review_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `ST2 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
st2_wholework_structure_review_audit_v2_0.md
```

### What to look for

The output should notice misplaced order and suggest a better structure without writing the sections.

---
## ST3 Test — Expert Meaning Review

### What this test checks

Checks whether the tool focuses on meaning, claims and interpretation rather than grammar.

### What you need

- `02_structure_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `02_structure_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `ST3 — Expert Meaning Review`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
BTS campaigns prove that online consumers no longer respond to traditional advertising and that all brands should use celebrities instead of ordinary adverts.
```

### Save the test output

Save the AI response as:

```text
st3_expert_meaning_review_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `ST3 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
st3_expert_meaning_review_audit_v2_0.md
```

### What to look for

The output should challenge overclaiming, unsupported interpretation and weak cause-effect logic.

---
## AT1 Test — Assignment Brief Checker

### What this test checks

Checks whether the tool compares the work with a brief without grading it.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT1 — Assignment Brief Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Brief: Evaluate the strengths and limitations of influencer marketing for brand engagement.

Draft extract: Influencer marketing is popular. BTS and YouTubers get many likes online. This essay explains some examples of campaigns.
```

### Save the test output

Save the AI response as:

```text
at1_assignment_brief_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT1 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at1_assignment_brief_checker_audit_v2_0.md
```

### What to look for

The output should identify whether the extract evaluates or merely describes, and show what is missing.

---
## AT2 Test — Argument Map

### What this test checks

Checks whether the tool maps claims, support, evidence, assumptions and gaps.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT2 — Argument Map`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Influencer marketing is more effective than traditional advertising because audiences trust influencers. BTS fans share campaigns quickly and YouTubers speak directly to viewers. Therefore brands should focus on influencers.
```

### Save the test output

Save the AI response as:

```text
at2_argument_map_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT2 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at2_argument_map_audit_v2_0.md
```

### What to look for

The output should separate the main claim, supporting points, evidence and assumptions.

---
## AT3 Test — Descriptive vs Analytical Check

### What this test checks

Checks whether the tool helps students see description versus analysis.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT3 — Descriptive vs Analytical Check`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
BTS worked with McDonald’s on a campaign. The campaign used branded packaging and social media. Fans posted about it online and many people commented on the campaign.
```

### Save the test output

Save the AI response as:

```text
at3_descriptive_vs_analytical_check_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT3 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at3_descriptive_vs_analytical_check_audit_v2_0.md
```

### What to look for

The output should identify mostly descriptive writing and suggest how to add analysis.

---
## AT4 Test — Evidence Gap Checker

### What this test checks

Checks whether the tool spots unsupported claims.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT4 — Evidence Gap Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Young consumers always trust YouTubers more than television adverts. This means influencer marketing is the future of advertising.
```

### Save the test output

Save the AI response as:

```text
at4_evidence_gap_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT4 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at4_evidence_gap_checker_audit_v2_0.md
```

### What to look for

The output should identify claims needing evidence and suggest what kind of evidence would help.

---
## AT5 Test — Concept Clarity Checker

### What this test checks

Checks whether the tool identifies key terms and whether they are defined consistently.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT5 — Concept Clarity Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
This proposal studies consumer culture, engagement, digital storytelling and fandom. These ideas show how social media changes branding.
```

### Save the test output

Save the AI response as:

```text
at5_concept_clarity_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT5 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at5_concept_clarity_checker_audit_v2_0.md
```

### What to look for

The output should ask for clearer definitions and distinguish related concepts.

---
## AT6 Test — Literature Use Checker

### What this test checks

Checks whether the tool reviews how sources are being used rather than just whether they are cited.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT6 — Literature Use Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Kozinets (2002) discusses netnography. Hackley (2003) discusses marketing research. Jones et al. (2015) discuss digital discourse. These sources are useful for my dissertation.
```

### Save the test output

Save the AI response as:

```text
at6_literature_use_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT6 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at6_literature_use_checker_audit_v2_0.md
```

### What to look for

The output should identify listing rather than synthesis and suggest how sources could be connected.

---
## AT7 Test — Counterargument and Limitations Checker

### What this test checks

Checks whether the tool identifies objections and limitations.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT7 — Counterargument and Limitations Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
BTS campaigns are successful because fans spread them online, so celebrity campaigns are the best advertising strategy for global brands.
```

### Save the test output

Save the AI response as:

```text
at7_counterargument_and_limitations_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT7 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at7_counterargument_and_limitations_checker_audit_v2_0.md
```

### What to look for

The output should identify counterarguments, limits and ways to qualify the claim.

---
## AT8 Test — Source Reliability Checker

### What this test checks

Checks whether the tool gives preliminary source-quality advice without pretending to verify unavailable details.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT8 — Source Reliability Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Sources: Wikipedia page on BTS, a McDonald’s press release, Kozinets 2002 netnography article, a fan blog about BTS campaigns.
```

### Save the test output

Save the AI response as:

```text
at8_source_reliability_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT8 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at8_source_reliability_checker_audit_v2_0.md
```

### What to look for

The output should classify sources cautiously and say what would need checking.

---
## AT9 Test — Critical Opponent Review

### What this test checks

Checks whether the tool can challenge an argument, including ideological assumptions, without rewriting it.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT9 — Critical Opponent Review`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Use the ideological assumptions opponent. My argument is: Influencer marketing is positive because it helps brands build stronger relationships with young consumers and makes advertising more engaging.
```

### Save the test output

Save the AI response as:

```text
at9_critical_opponent_review_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT9 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at9_critical_opponent_review_audit_v2_0.md
```

### What to look for

The output should offer or use an ideological standpoint, identify underlying assumptions, objections and tough questions.

---
## AT10 Test — Socratic Tutor

### What this test checks

Checks whether the tool asks one question at a time and can choose a random topic from the work.

### What you need

- `03_academic_thinking_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `03_academic_thinking_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `AT10 — Socratic Tutor`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Choose a random topic from this work and ask me Socratic questions about it: BTS fans share branded content online, and this may affect how campaigns spread through social media.
```

### Save the test output

Save the AI response as:

```text
at10_socratic_tutor_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `AT10 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
at10_socratic_tutor_audit_v2_0.md
```

### What to look for

The output should choose a relevant topic and ask only one question.

---
## RP1 Test — Research Question, Aim and Objectives Checker

### What this test checks

Checks whether the tool tests clarity, focus and alignment.

### What you need

- `04_research_proposal_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `04_research_proposal_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `RP1 — Research Question, Aim and Objectives Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Topic: social media and advertising. Aim: to study BTS and YouTubers and consumer culture and digital media. Objectives: look at campaigns, talk about fans, study YouTube, explore branding.
```

### Save the test output

Save the AI response as:

```text
rp1_research_question_aim_and_objectives_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `RP1 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
rp1_research_question_aim_and_objectives_checker_audit_v2_0.md
```

### What to look for

The output should identify breadth, overlap and lack of a clear research question.

---
## RP2 Test — Methodology Fit Checker

### What this test checks

Checks whether the method matches the research question and data.

### What you need

- `04_research_proposal_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `04_research_proposal_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `RP2 — Methodology Fit Checker`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Research question: How do young consumers feel about influencer marketing? Method: I will analyse three brand adverts and hashtags using discourse analysis.
```

### Save the test output

Save the AI response as:

```text
rp2_methodology_fit_checker_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `RP2 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
rp2_methodology_fit_checker_audit_v2_0.md
```

### What to look for

The output should spot the mismatch between feelings/attitudes and textual/social-media analysis.

---
## RP3 Test — Critical Research Supervisor Review

### What this test checks

Checks whether the tool acts like a critical but constructive supervisor.

### What you need

- `04_research_proposal_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `04_research_proposal_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `RP3 — Critical Research Supervisor Review`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Proposal summary: I will study BTS, MrBeast, Zoella, Hyundai, Samsung, McDonald’s, TikTok, YouTube, Instagram and Twitter to show how influencer marketing affects consumer culture worldwide. I will use netnography and discourse analysis.
```

### Save the test output

Save the AI response as:

```text
rp3_critical_research_supervisor_review_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `RP3 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
rp3_critical_research_supervisor_review_audit_v2_0.md
```

### What to look for

The output should challenge scope, feasibility, data, method and overclaiming.

---
## RP4 Test — Viva or Supervisor Practice

### What this test checks

Checks whether the tool asks one supervisor-style question at a time.

### What you need

- `04_research_proposal_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `04_research_proposal_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `RP4 — Viva or Supervisor Practice`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
My proposal is about BTS and YouTuber advertising campaigns and how they affect consumer culture. Please question me like a supervisor.
```

### Save the test output

Save the AI response as:

```text
rp4_viva_or_supervisor_practice_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `RP4 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
rp4_viva_or_supervisor_practice_audit_v2_0.md
```

### What to look for

The output should ask one focused question and wait for an answer.

---
## RP5 Test — Guided Topic Brainstorming

### What this test checks

Checks whether brainstorming is interactive and does not simply dump finished topics.

### What you need

- `04_research_proposal_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `04_research_proposal_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `RP5 — Guided Topic Brainstorming`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
I want to do a dissertation about beauty ideals and young women on social media.
```

### Save the test output

Save the AI response as:

```text
rp5_guided_topic_brainstorming_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `RP5 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
rp5_guided_topic_brainstorming_audit_v2_0.md
```

### What to look for

The output should ask clarifying questions before generating many topics.

---
## SW1 Test — Revision Plan

### What this test checks

Checks whether the tool turns feedback into prioritised actions.

### What you need

- `05_study_workflow_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `05_study_workflow_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `SW1 — Revision Plan`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Feedback: Your proposal is too broad. The methods are not clear. The aims overlap. Some claims need evidence. The writing is wordy.
```

### Save the test output

Save the AI response as:

```text
sw1_revision_plan_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `SW1 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
sw1_revision_plan_audit_v2_0.md
```

### What to look for

The output should group feedback into high/medium/low priorities and practical next actions.

---
## SW2 Test — Tutor Feedback to Action Plan

### What this test checks

Checks whether the tool explains tutor feedback and turns it into tasks.

### What you need

- `05_study_workflow_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `05_study_workflow_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `SW2 — Tutor Feedback to Action Plan`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
Tutor feedback: “You need a clearer line of argument and should engage more critically with the literature rather than listing sources.”
```

### Save the test output

Save the AI response as:

```text
sw2_tutor_feedback_to_action_plan_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `SW2 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
sw2_tutor_feedback_to_action_plan_audit_v2_0.md
```

### What to look for

The output should explain the feedback in plain English and turn it into actions.

---
## SW3 Test — AI-Use Record

### What this test checks

Checks whether the tool creates a factual, transparent record of AI support.

### What you need

- `05_study_workflow_tutor_library_v2_0.md`
- `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`
- Somewhere to save Markdown files

### How to run the test

1. Open a new AI chat.
2. Upload `05_study_workflow_tutor_library_v2_0.md`.
3. Type `prompt`.
4. Choose `SW3 — AI-Use Record`.
5. Paste the test input below.

### Test input

Copy and paste this:

```text
I used the toolkit to find grammar mistakes, get style feedback and make a revision plan. I rewrote the work myself.
```

### Save the test output

Save the AI response as:

```text
sw3_aiuse_record_test_output_v2_0.md
```

### How to perform the audit

1. Open a new AI chat.
2. Upload or paste `ai_tutor_toolkit_audit_prompt_with_menu_v2_3.md`.
3. Choose `SW3 audit` from the audit menu.
4. Paste the saved test output.
5. Ask for the audit as Markdown.

### Save the audit output

Save the audit as:

```text
sw3_aiuse_record_audit_v2_0.md
```

### What to look for

The output should create a factual AI-use note without overstating or hiding anything.

---
