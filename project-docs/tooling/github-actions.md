# GitHub Actions

Workflow files live in:

```text
.github/workflows/
```

The deploy workflow can rebuild the site during deployment by running:

```bash
python scripts/run_generator_checks.py --build-first
```

This is a build-time process. GitHub Pages still serves a static site to visitors.

If deployment from GitHub Actions is used, configure GitHub Pages in repository settings to use **GitHub Actions** as the publishing source.
