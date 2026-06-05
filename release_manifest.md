# AI Personal Tutor Toolkit — Release Manifest

**Current site package:** v2.15  
**Prompt-library suite:** v2.4  
**Testing/audit pack:** v2.8  
**Last updated:** 2026-06-05  
**Release type:** site navigation and guides cleanup

## How versions work

The toolkit uses three related version labels:

1. **Site package version** — the deployable website ZIP and public pages.
2. **Prompt-library suite version** — the current set of student-facing prompt libraries.
3. **Testing/audit pack version** — the current educator testing and audit materials.

Individual files also display their own file name and current suite/pack version. The `latest/` folders always contain the current public downloads. The fixed `v2.x/` folders preserve archived release copies for educators, developers and audit trails.

## Current public prompt-library downloads

| File | Current file version | Public path | Fixed archive path |
|---|---:|---|---|
| Writing Tutor Mini Library | v2.4 | `prompt-libraries/latest/01_writing_tutor_library.md` | `prompt-libraries/v2.4/01_writing_tutor_library_v2_4.md` |
| Structure Tutor Mini Library | v2.4 | `prompt-libraries/latest/02_structure_tutor_library.md` | `prompt-libraries/v2.4/02_structure_tutor_library_v2_4.md` |
| Academic Thinking Tutor Mini Library | v2.4 | `prompt-libraries/latest/03_academic_thinking_tutor_library.md` | `prompt-libraries/v2.4/03_academic_thinking_tutor_library_v2_4.md` |
| Research Proposal Tutor Mini Library | v2.4 | `prompt-libraries/latest/04_research_proposal_tutor_library.md` | `prompt-libraries/v2.4/04_research_proposal_tutor_library_v2_4.md` |
| Study Workflow Tutor Mini Library | v2.4 | `prompt-libraries/latest/05_study_workflow_tutor_library.md` | `prompt-libraries/v2.4/05_study_workflow_tutor_library_v2_4.md` |
| AI Personal Tutor Master Prompt Library | v2.4 | `prompt-libraries/latest/ai_personal_tutor_master_library.md` | `prompt-libraries/v2.4/ai_personal_tutor_master_library_v2_4.md` |
| Mini-library ZIP bundle | v2.4 | `prompt-libraries/latest/ai_personal_tutor_mini_libraries.zip` | `prompt-libraries/v2.4/ai_personal_tutor_mini_libraries_v2_4.zip` |

## Current public testing/audit downloads

| File | Current file version | Public path | Fixed archive path |
|---|---:|---|---|
| Audit Prompt with Menu | v2.8 | `audit-library/latest/ai_tutor_toolkit_audit_prompt_with_menu.md` | `audit-library/v2.8/ai_tutor_toolkit_audit_prompt_with_menu_v2_8.md` |
| Step-by-Step Test Cards | v2.8 | `audit-library/latest/ai_tutor_toolkit_step_by_step_test_cards.md` | `audit-library/v2.8/ai_tutor_toolkit_step_by_step_test_cards_v2_8.md` |
| Test Log Template | v2.8 | `audit-library/latest/ai_tutor_toolkit_test_log_template.md` | `audit-library/v2.8/ai_tutor_toolkit_test_log_template_v2_8.md` |
| Testing Guide for Educators | v2.8 | `audit-library/latest/ai_tutor_toolkit_testing_guide_for_educators.md` | `audit-library/v2.8/ai_tutor_toolkit_testing_guide_for_educators_v2_8.md` |
| Universal and Adversarial Test Cards | v2.8 | `audit-library/latest/ai_tutor_toolkit_universal_test_cards.md` | `audit-library/v2.8/ai_tutor_toolkit_universal_test_cards_v2_8.md` |
| Testing pack ZIP bundle | v2.8 | `audit-library/latest/ai_personal_tutor_testing_pack.zip` | `audit-library/v2.8/ai_personal_tutor_testing_pack_v2_8.zip` |

## What changed in v2.13

This release does not change tool behaviour. It clarifies version signalling by:

- adding visible release stamps to current downloadable Markdown files;
- aligning internal headings in the latest prompt-library files with prompt-library suite v2.4;
- aligning internal headings in the latest testing/audit files with testing pack v2.8;
- adding this manifest so educators can see which public downloads and archive files belong together;
- updating README, Testing and Changelog notes to explain suite versions versus file versions.


## What changed in v2.14

This release adds the public Guides section. It does not change prompt-library or testing/audit behaviour. New pages: `guides.html`, `guide-students.html`, `guide-tutors.html`, `guide-writing-workflow.html`, `guide-not-first-draft.html`, and `guide-setup.html`.


## What changed in v2.15

This release reorganises the public website navigation. The top-level navigation now contains Home, Tools, Examples and Guides. Teaching approach, Testing and Changelog are linked from the Guides page and the footer, while their URLs remain unchanged. The homepage order has been adjusted, the Paragraph logic before polish explanation has moved to the Teaching approach page, and a blank `about.html` page has been added. No prompt-library or testing/audit behaviour changed.
