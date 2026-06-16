# Package Generator Start Here

For current build instructions, use the canonical guide and maintainer documentation:

- [`BUILD_AND_GENERATOR_GUIDE.md`](BUILD_AND_GENERATOR_GUIDE.md)
- [`project-docs/README.md`](project-docs/README.md)

Most common command:

```bash
python scripts/run_generator_checks.py --build-first
```

That command rebuilds prompt libraries, audit/testing outputs, source material, generated site pages and site metadata, then runs the standard checks.

The older package-generator notes are still useful for background design context and now live under `tool-history/repository-docs/root-docs/`. This file deliberately points maintainers to the current build guide so script instructions do not drift.
