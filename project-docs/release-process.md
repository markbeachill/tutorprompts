# Release process

Public releases use a single release version. The release version, prompt-library version and testing/audit version should match.

The release metadata source is:

```text
src/release.yml
```

Expected policy:

```yaml
release_version: 4.2.1
toolkit_version: 4.2.1
prompt_library_version: 4.2.1
testing_pack_version: 4.2.1
```

`release_version` is the public source of truth. Legacy keys are kept for compatibility but must match.

## Normal release build

```bash
python scripts/run_generator_checks.py --build-first
python scripts/build_site_package.py --run-generator-check --version 4.2.1
python scripts/build_site_package.py --include-generator --run-generator-check --version 4.2.1
```

For orchestrated releases, see `scripts/build_toolkit_release.py` and the root `BUILD_AND_GENERATOR_GUIDE.md`.

## Changelog

Root `CHANGELOG.md` points to the public changelog and release manifest. Detailed public release notes are served from `docs/changelog/`.
