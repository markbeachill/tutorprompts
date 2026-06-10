# Prompt Library v4.0 Source Split Update Notes

Source master used: `/mnt/data/ai_personal_tutor_master_library_v4_0_1.md`.

Version normalisation: visible prompt-library/toolkit labels normalised to v4.0, not v4.0.1.

Testing pack release stamp: set to v4.0 to align the public prompt-library and testing/audit releases before first public v4 publication.

## What changed

- Split the v4.0.1 master library back into the repository build-source structure.
- Updated `src/prompt-library/header.md` from the activation preamble before the first file marker.
- Updated shared source files:
  - `src/prompt-library/shared/01-global-rules.md`
  - `src/prompt-library/shared/02-markdown-output-rules.md`
- Updated all 27 files in `src/prompt-library/tools/` from the marked tool blocks in the master library.
- Preserved the generator architecture: generated master sections were not copied wholesale over pack templates.
- Updated `src/prompt-library/pack-sections/` templates so the build script still generates menus and routing tables from `tool-metadata.json`.
- Added the v4 launcher triage wording into generated-menu templates: students can describe their problem in one sentence and the AI should suggest one or two tools.
- Updated router templates so tool suggestions name at most two tools and ask for confirmation before starting.
- Removed generated version-history footers from pack outputs by clearing footer entries in pack specs; version history is treated as published separately.
- Updated `src/release.yml` to v4.0 toolkit, prompt-library and testing/audit labels.
- Regenerated latest prompt libraries, v4.0 archives, custom pack output, single-tool packs, testing/audit files and site data.

## Validation run

From the repository root:

```bash
python scripts/build_prompt_libraries.py --check
python scripts/build_prompt_libraries.py --validate
python scripts/build_prompt_libraries.py --include-single-tools --include-custom --check
python scripts/build_prompt_libraries.py --include-single-tools --include-custom --validate
python scripts/build_audit_pack.py --check
python scripts/build_audit_pack.py --validate
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
python scripts/release_consistency_check.py --fail-on-problems
```

All checks passed.
