# Package Generator Roadmap

This roadmap records optional future improvements for the AI Personal Tutor Toolkit package generator. These items are not needed to sign off the current generator workflow. They can be revisited later if the project needs more automation or stronger checks.

## Current status

The package generator already supports the core workflow:

- source-driven prompt-library generation;
- master and mini-library builds;
- metadata-driven menus, tool tables and router mappings;
- custom pack generation;
- single-tool pack generation;
- GitHub Actions checks;
- clean site-package ZIP generation;
- release preparation and release orchestration;
- health reports and release consistency checks;
- draft release-note helper;
- generated site-data JSON;
- audit/testing-pack build, archive and ZIP process;
- independent testing-pack versioning;
- mixed-version diagnostics and recovery;
- build-first and sync-release-metadata workflows;
- local clean-up helper.

## Optional future work

### 1. Use the generator for a real toolkit release

The most important practical test is to use the generator for a normal toolkit release from start to finish.

Suggested workflow:

```powershell
python scripts\run_generator_checks.py --build-first
python scripts\build_toolkit_release.py --version 3.7 --date YYYY-MM-DD --draft-notes
```

Then inspect the generated package in `dist/` before publishing.

### 2. Site link and download checker

Add a script such as:

```powershell
python scripts\check_site_links.py
```

Possible checks:

- internal links point to existing files;
- download links point to files that exist;
- archive links exist for the current release;
- generated ZIP files exist;
- no stale version labels remain after release preparation.

This is probably the next most useful reliability improvement after version/build automation.

### 3. Changelog integration

The generator can already create draft update notes. A future version could also:

- create a draft changelog entry;
- check that `docs/changelog/index.html` links to the new update notes;
- warn if a release package has no update-note file;
- keep final prose manual.

### 4. Website integration with generated data

The generator now creates JSON data files such as:

```text
docs/data/release.json
docs/data/tool_index.json
docs/data/prompt_library_packs.json
```

A future site update could use this data to drive tools/download pages, or the generator could check that hand-written website cards match the generated data.

### 5. Custom-pack usability improvements

Custom packs currently use YAML. Future improvements could include:

- a template generator for new custom packs;
- clearer plain-English validation messages;
- example packs for common teaching scenarios;
- optional generated README files for each individual custom pack;
- later, a simple webpage or form that writes custom-pack YAML.

### 6. Stronger content-level guardrail checks

The generator mostly checks structure, versioning and packaging. A future checker could look for pedagogical/prompt-safety rules, for example:

- every tool applies the global rules;
- every pack includes the shared global and Markdown rules;
- every pack includes recovery instructions;
- referencing/source tools include verification cautions;
- no tool silently invites the AI to write finished assessed work for the student.

These checks should be conservative and should not replace human review.

### 7. Audit/testing-pack improvements

The audit pack is now included in the generator workflow, but it is much simpler than the prompt-library system. Future work could add:

- more explicit human-review notes;
- checks for stale internal filenames;
- clearer testing-pack manifest output;
- optional audit-pack changelog notes when the testing pack content version changes.

### 8. Documentation and onboarding polish

After the generator has been used for a real release, revisit the docs and improve instructions for common situations:

- “I changed a tool.”
- “I changed the audit pack.”
- “I want to make a new toolkit release.”
- “I got a version mismatch.”
- “I want to make a custom pack.”
- “I want to clean temporary files.”

## Recommended next generator feature if work resumes

If the generator is picked up again, the recommended next feature is:

> **Site link and download checker** — a script that verifies internal website links, download links, archive paths and current-version labels.

This would address the next major reliability risk after prompt-library/version drift.
