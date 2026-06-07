# AI Personal Tutor single-tool packs

This folder contains generated single-tool prompt packs. Each file contains the shared operating rules, a one-tool launcher/router, and one tool instruction block.

Prompt-library version: v3.5

Build all single-tool packs from the repository root with:

```bash
python scripts/build_prompt_libraries.py --include-single-tools
```

Check all single-tool packs without writing changes with:

```bash
python scripts/build_prompt_libraries.py --include-single-tools --check
```

## Included single-tool packs

| Code | Tool | Family | Generated file |
|---|---|---|---|
| WT1 | Clarity Clinic | Writing Tutor tools | `wt1_clarity_clinic.md` |
| WT2 | Single Paragraph Analysis | Writing Tutor tools | `wt2_single_paragraph_analysis.md` |
| WT3 | Find My Mistakes | Writing Tutor tools | `wt3_find_my_mistakes.md` |
| WT4 | Teach Me This Mistake | Writing Tutor tools | `wt4_teach_me_this_mistake.md` |
| WT5 | Style and Clarity Review | Writing Tutor tools | `wt5_style_and_clarity_review.md` |
| WT6 | Referencing Helper | Writing Tutor tools | `wt6_referencing_helper.md` |
| ST1 | Paragraph Structure Review Across a Whole Draft | Structure Tutor tools | `st1_paragraph_structure_review_across_a_whole_draft.md` |
| ST2 | Whole-Work Structure Review | Structure Tutor tools | `st2_whole_work_structure_review.md` |
| ST3 | Expert Meaning Review | Structure Tutor tools | `st3_expert_meaning_review.md` |
| AT1 | Assignment Brief Checker | Academic Thinking tools | `at1_assignment_brief_checker.md` |
| AT2 | Argument Map | Academic Thinking tools | `at2_argument_map.md` |
| AT3 | Descriptive vs Analytical Check | Academic Thinking tools | `at3_descriptive_vs_analytical_check.md` |
| AT4 | Evidence Gap Checker | Academic Thinking tools | `at4_evidence_gap_checker.md` |
| AT5 | Concept Clarity Checker | Academic Thinking tools | `at5_concept_clarity_checker.md` |
| AT6 | Literature Use Checker | Academic Thinking tools | `at6_literature_use_checker.md` |
| AT7 | Counterargument and Limitations Checker | Academic Thinking tools | `at7_counterargument_and_limitations_checker.md` |
| AT8 | Source Reliability Checker | Academic Thinking tools | `at8_source_reliability_checker.md` |
| AT9 | Critical Opponent Review | Academic Thinking tools | `at9_critical_opponent_review.md` |
| AT10 | Socratic Tutor | Academic Thinking tools | `at10_socratic_tutor.md` |
| RP1 | Research Question, Aim and Objectives Checker | Research Proposal tools | `rp1_research_question_aim_and_objectives_checker.md` |
| RP2 | Methodology Fit Checker | Research Proposal tools | `rp2_methodology_fit_checker.md` |
| RP3 | Critical Research Supervisor Review | Research Proposal tools | `rp3_critical_research_supervisor_review.md` |
| RP4 | Viva or Supervisor Practice | Research Proposal tools | `rp4_viva_or_supervisor_practice.md` |
| RP5 | Guided Topic Brainstorming | Research Proposal tools | `rp5_guided_topic_brainstorming.md` |
| SW1 | Revision Plan | Study Workflow tools | `sw1_revision_plan.md` |
| SW2 | Tutor Feedback to Action Plan | Study Workflow tools | `sw2_tutor_feedback_to_action_plan.md` |
| SW3 | AI-Use Record | Study Workflow tools | `sw3_ai_use_record.md` |

The ZIP `ai_personal_tutor_single_tool_packs.zip` contains this README, `single_tool_manifest.json`, and all generated single-tool Markdown files.
