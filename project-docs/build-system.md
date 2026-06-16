# Build system overview

The repository is source-driven. Human-edited files live mainly under `src/`; generated public files live mainly under `docs/`.

The canonical command is:

```bash
python scripts/run_generator_checks.py --build-first
```

This rebuilds the prompt libraries, audit/testing pack, site data, source-material library and generated site pages, then runs consistency checks.

## Main build layers

```text
Prompt libraries   scripts/build_prompt_libraries.py
Audit/testing      scripts/build_audit_pack.py
Site data          scripts/build_site_data.py
Source material    scripts/build_source_material_library.py
Generated pages    scripts/build_site_pages.py
Release checks     scripts/release_consistency_check.py
Release packages   scripts/build_site_package.py
```

Use `BUILD_AND_GENERATOR_GUIDE.md` in the root for full commands and release workflow details.

## Build-first rule

When a source file changes, use a build-first command before checking or packaging. Do not hand-edit generated files as the primary fix unless the relevant generator is also updated.
