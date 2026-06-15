# Package Generator Start Here

For current build instructions, use the canonical guide:

- [`BUILD_AND_GENERATOR_GUIDE.md`](BUILD_AND_GENERATOR_GUIDE.md)

Most common command:

```bash
python scripts/run_generator_checks.py --build-first
```

That command rebuilds prompt libraries, audit/testing outputs, source material, generated site pages and site metadata, then runs the standard checks.

The older package-generator notes are still useful for background design context, but this file now deliberately points maintainers to one consolidated build guide so the script instructions do not drift.
