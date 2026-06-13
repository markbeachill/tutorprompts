# Site v4.1 — WT7 paraphrase and quotation workshop

**Site package:** v4.1  
**Prompt-library suite:** v4.1  
**Testing/audit pack:** v4.1

This release adds WT7 — Paraphrase and Quotation Workshop to the Writing Tutor family. WT7 is a staged source-use tool for checking paraphrases, quotations, attribution and reporting verbs without writing the paraphrase or quote-integration sentence for the student.

## Main changes

- Added WT7 source file to `src/prompt-library/tools/`.
- Added WT7 to `tool-metadata.json` and the Writing Tutor pack source.
- Rebuilt current and v4.1 prompt-library downloads, including the master library, mini libraries, custom pack and single-tool packs.
- Added WT7 testing/audit checks for too-close paraphrase, unmarked direct quotation, plagiarism / patchwriting risk, quote framing and reporting-verb overclaiming.
- Updated public Tools, Writing Tutor, single-tool downloads, Testing, Changelog and Release Manifest pages.

## Behavioural note

WT7 is intentionally not a paraphrasing service. It asks for the source extract and the student’s attempt where needed, diagnoses the source-use problem and sets a student-owned revision task.
