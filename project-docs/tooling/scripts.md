# Scripts

The repository uses `scripts/` for Python maintenance tooling.

Important scripts:

```text
build_prompt_libraries.py        Builds prompt libraries and single-tool files.
build_audit_pack.py              Builds the testing/audit pack.
build_site_data.py               Builds generated JSON data.
build_source_material_library.py Builds source-material pages/downloads.
build_site_pages.py              Builds/normalises generated site pages.
build_example_pages.py           Wraps src/examples snippets into docs/examples pages.
build_create_examples_page.py     Builds the one-stop create-examples page (cards + collector + converter).
run_generator_checks.py          Main check runner; can rebuild first.
build_site_package.py            Builds public and full repository ZIPs.
build_toolkit_release.py         Orchestrates release builds.
release_consistency_check.py     Checks release-version alignment.
generator_health_report.py       Read-only repository health summary.
```

Use the root `BUILD_AND_GENERATOR_GUIDE.md` for exact commands.
