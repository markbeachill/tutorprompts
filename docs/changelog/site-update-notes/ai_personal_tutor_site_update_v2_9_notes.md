# AI Personal Tutor Toolkit — site update v2.9 notes

## Release summary

This update responds to the ST1 audit finding that Paragraph Structure Review Across a Whole Draft was diagnosing paragraph development before checking whether the paragraph's central claim was clear enough for a reader to follow.

## Updated versions

- Site package: v2.9
- Prompt libraries: v2.2
- Structure Tutor Library: v2.2
- Testing/audit pack: v2.6

## Main prompt-library changes

- ST1 now checks central claim clarity before topic sentence, development, evidence, links or polish.
- ST1 now distinguishes an unclear or unformed central claim from thin development.
- ST1 follow-up turns now avoid writing near-usable sentences in the student's voice using the student's own source material.
- ST1 now uses fictional examples when modelling a structural move in follow-up.
- ST1 now handles marker, tutor or supervisor feedback as evidence of reader confusion rather than as a marker-response service.
- ST1 conclusion guidance now uses student-owned planning questions rather than a fixed three-move prescription.

## Testing changes

- Testing pack updated to v2.6.
- Audit prompt includes ST1-specific central-claim criteria.
- ST1 step-by-step test card includes an intentionally vague “conflict” paragraph to check that the tool flags the unformed claim before development.

## Website changes

- Changelog updated with Site v2.9 / Libraries v2.2 / Testing pack v2.6.
- Testing page updated to describe the v2.6 ST1 regression check.
- Structure Tutor page updated to describe central-claim-first diagnosis.
- README updated with new version folders and current versions.
