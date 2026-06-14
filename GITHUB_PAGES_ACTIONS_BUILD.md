# Optional GitHub Actions build for GitHub Pages

This repository can be used in two ways:

1. **Local/static build** — run the Python generator scripts on your computer, commit the generated `docs/` files, and let GitHub Pages serve the committed static site.
2. **GitHub-side build** — let GitHub Actions run the Python generator scripts on GitHub, then deploy the generated `docs/` folder to GitHub Pages.

The second option is the closest GitHub Pages can get to a “server-side build”. It is server-side **at deploy time**, not server-side **when a visitor opens the page**. GitHub Pages still serves a static site after deployment.

## Added workflow

The workflow file is:

```text
.github/workflows/deploy-github-pages.yml
```

It runs when:

- changes are pushed to `main` or `master` that affect `src/`, `scripts/`, `docs/`, or this workflow; or
- you manually run it from the GitHub **Actions** tab.

The workflow does this:

```text
1. Check out the repository
2. Set up Python
3. Run: python scripts/run_generator_checks.py --build-first
4. Upload the generated docs/ folder as a GitHub Pages artifact
5. Deploy that artifact to GitHub Pages
```

## How to enable it in GitHub

In the GitHub repository:

1. Go to **Settings**.
2. Open **Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Go to the **Actions** tab.
5. Run **Build and deploy GitHub Pages**, or push a change to `src/`, `scripts/`, or `docs/`.

## What this changes

You can now edit source files such as:

```text
src/prompt-library/tools/teach-mistake.md
src/source-material/items/example.md
src/prompt-library/packs/master.yml
```

Then GitHub can rebuild the generated public site during deployment.

This reduces the risk of forgetting to rebuild these generated outputs locally:

```text
docs/prompt-libraries/
docs/audit-library/
docs/data/
docs/source-material/
```

## What this does not change

This does **not** make the site dynamically server-side.

GitHub Pages cannot run Python when a visitor opens a page. The Python scripts only run inside GitHub Actions during the build/deploy workflow. After deployment, visitors still receive static HTML, CSS, JavaScript and Markdown files.

## Recommended working pattern

For normal editing, keep using the local check before committing:

```bash
python scripts/run_generator_checks.py --build-first
```

Then commit both the source changes and generated `docs/` changes. The GitHub Actions workflow acts as a second safety net and can also deploy the site from a clean GitHub-side build.

For a source-only workflow later, you could stop committing generated `docs/` changes and rely on GitHub Actions to build them at deployment time. For now, committing generated files is simpler and more transparent.

## Troubleshooting

If the workflow fails, check the failed step in the **Actions** tab. Most failures mean one of the generator checks failed locally too.

Run this locally to reproduce the same build/check step:

```bash
python scripts/run_generator_checks.py --build-first
```

If GitHub Pages does not update, check:

- **Settings → Pages → Source** is set to **GitHub Actions**;
- the workflow has permission to deploy Pages;
- the latest workflow run completed successfully; and
- the `docs/` folder exists after the build step.
