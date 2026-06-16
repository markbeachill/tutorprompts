# Update Checklists

Use this file when changing prompt-library tools, audit/testing materials, or release packages.

This is an operational checklist for maintainers and AI assistants. It does not replace `BUILD_AND_GENERATOR_GUIDE.md`; it turns the common update workflows into step-by-step checks.

## How to use this file with an AI assistant

Before asking an AI assistant to make a change, point it to the relevant checklist and ask it to report:

```text
- which checklist items it completed;
- which items were not applicable;
- which generated files changed;
- which checks passed;
- which checks were not run.
```

The AI assistant should not guess from memory if this file and `BUILD_AND_GENERATOR_GUIDE.md` are available.

## A. Checklist for updating an individual prompt-library tool

Use this when changing a file under:

```text
src/prompt-library/tools/
```

### 1. Confirm the scope of the change

- Identify the tool code, title and source file, for example `WT4 — Find My Mistakes` and `src/prompt-library/tools/find-mistakes.md`.
- Decide whether the change is a wording clarification, behaviour change, boundary change, new tool, removed tool or numbering change.
- If the change records a completed design decision, add or update a note under `tool-history/`.
- If the change is only a future proposal, keep it under `roadmaps/` and do not integrate it into live tool files yet.

### 2. Edit the source tool file

- Edit the tool source file under `src/prompt-library/tools/`.
- Check the front matter:
  - `id`
  - `tool_code`
  - `master_number`
  - `title`
  - `type`
  - `menu_number`
  - `run_policy`
  - `input_required`
  - `output_style`
- Check the heading and version wording inside the tool file.
- Make sure the purpose, boundaries, output format and end behaviour still agree with each other.
- Remove draft labels before integrating into a release file unless the file is intentionally marked as a draft.

### 3. Check related prompt-library source files

Update these only if the change affects them:

```text
src/prompt-library/tool-metadata.json
src/prompt-library/packs/*.yml
src/prompt-library/custom-packs/*.yml
src/prompt-library/launchers/
src/prompt-library/routers/
```

Check especially:

- tool title and short description;
- visible menu wording;
- routing guidance;
- pack membership;
- cross-references from other tools;
- examples or source-material labels that mention the old behaviour;
- numbering if a tool has moved.

### 4. Check boundaries and neighbouring tools

- If the tool's boundary changed, check whether another tool should handle the excluded work.
- Do not broaden one tool just because a student might ask for adjacent help.
- If the change affects routing, update the router or launcher wording rather than relying on hidden assumptions.
- If the change affects audit expectations, also complete Checklist B.

### 5. Rebuild and check prompt libraries

Run:

```bash
python scripts/build_prompt_libraries.py --include-single-tools --include-custom
python scripts/build_prompt_libraries.py --include-single-tools --include-custom --check
python scripts/build_prompt_libraries.py --ci
```

Or run the full build/check command:

```bash
python scripts/run_generator_checks.py --build-first
```

### 6. Inspect generated outputs

Check the relevant generated files under:

```text
docs/prompt-libraries/latest/
docs/prompt-libraries/v<version>/
docs/prompt-libraries/single-tools/
docs/data/tool_index.json
```

Confirm that:

- the live library includes the changed tool text;
- the single-tool file includes the changed tool text;
- menus and metadata show the correct title, code and description;
- old wording has not survived in generated outputs.

## B. Checklist for updating the audit prompt or testing pack

Use this when changing audit rules, test cards, output-collector wording, testing guidance, or any tool behaviour that the audit pack should test.

Source files live under:

```text
src/audit-library/files/
```

### 1. Confirm what changed

- Identify whether the change affects the audit prompt, test cards, universal cards, educator guide, output collector or test log template.
- If a live tool boundary changed, make sure the audit prompt checks that boundary.
- If a new failure mode was discovered, decide whether it needs a regression card.

### 2. Edit audit source files

Check and edit relevant files under:

```text
src/audit-library/files/ai_tutor_toolkit_audit_prompt_with_menu.md
src/audit-library/files/ai_tutor_toolkit_step_by_step_test_cards.md
src/audit-library/files/ai_tutor_toolkit_universal_test_cards.md
src/audit-library/files/ai_tutor_toolkit_testing_guide_for_educators.md
src/audit-library/files/ai_tutor_toolkit_output_collector.md
src/audit-library/files/ai_tutor_toolkit_test_log_template.md
```

Check especially:

- menu entries and tool numbering;
- tool-specific checks;
- critical or hard-boundary rating rules;
- evidence-table rows;
- regression cards;
- version wording;
- whether the audit prompt tests the tool's actual purpose rather than a different tool's purpose.

### 3. Keep audit scope aligned with tool scope

- Do not make the audit prompt reward behaviour that the tool is not allowed to do.
- Do not make a writing tool pass by becoming a subject-answering, source-checking or evidence-checking tool.
- If a tool is intentionally narrow, audit it against that narrow job.
- If a test card expects broader behaviour, revise the test card rather than broadening the tool by accident.

### 4. Rebuild and check the audit pack

Run:

```bash
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --ci
```

Or run the full build/check command:

```bash
python scripts/run_generator_checks.py --build-first
```

### 5. Inspect generated audit outputs

Check:

```text
docs/audit-library/latest/
docs/audit-library/v<version>/
docs/audit-library/latest/ai_personal_tutor_testing_pack.zip
```

Confirm that:

- latest and versioned audit files match the source change;
- the testing ZIP contains the revised audit/test files;
- old audit wording has not survived in generated outputs;
- the audit prompt and test cards agree with each other.

## C. Final checks on a rebuild

Use this before returning packages, publishing a release, or asking someone else to use the updated repository.

### 1. Check release version policy

Check:

```text
src/release.yml
```

Confirm that these values match when the change is part of a public release:

```yaml
release_version: <version>
toolkit_version: <version>
prompt_library_version: <version>
testing_pack_version: <version>
```

Use the existing release version for documentation-only changes unless the user explicitly asks for a release bump.

### 2. Rebuild generated outputs

Run the full build/check command:

```bash
python scripts/run_generator_checks.py --build-first
```

Then run the check-only command:

```bash
python scripts/run_generator_checks.py
```

### 3. Package the public site and full repository

For the current release version, run:

```bash
python scripts/build_site_package.py --run-generator-check --version <version> --output /mnt/data/ai_personal_tutor_github_pages_site_v<version_for_filename>.zip
python scripts/build_site_package.py --include-generator --run-generator-check --version <version> --output /mnt/data/tutorprompts_repo_v<version_for_filename>.zip
```

Then check the packages:

```bash
python scripts/build_site_package.py --version <version> --output /mnt/data/ai_personal_tutor_github_pages_site_v<version_for_filename>.zip --check
python scripts/build_site_package.py --include-generator --version <version> --output /mnt/data/tutorprompts_repo_v<version_for_filename>.zip --check
```

Example filename convention:

```text
4.2.1 -> v4_2_1
```

### 4. Inspect high-risk generated areas

Depending on what changed, inspect the relevant generated files:

```text
docs/prompt-libraries/latest/
docs/prompt-libraries/single-tools/
docs/audit-library/latest/
docs/data/
docs/tools/index.html
docs/where-to-start/index.html
docs/download/index.html
docs/examples/index.html
docs/source-material/index.html
```

Check especially:

- release/version text;
- tool codes and numbering;
- tool descriptions;
- download links;
- old wording that should have disappeared;
- accidental changes to unrelated pages.

### 5. Final report

When reporting back, include:

```text
- source files changed;
- generated files changed;
- checklist items completed;
- checks run;
- checks passed or failed;
- package links;
- any items not run or not applicable.
```

Do not claim a check passed unless it was actually run.
