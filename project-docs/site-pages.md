# Site pages

The public site is served from `docs/`.

Generated/normalised site pages are maintained by:

```bash
python scripts/build_site_pages.py
python scripts/build_site_pages.py --check
```

This script builds or normalises pages such as:

```text
docs/tools/index.html
docs/where-to-start/index.html
docs/download/index.html
docs/examples/index.html
docs/try-it/index.html
```

It also normalises site navigation/footer links where required.

## Layout notes

Tools and Where to Start use accordion sections with table-based content. Mobile layouts should avoid internal accordion scrollbars; the page should scroll naturally and tables should degrade into readable stacked rows where needed.

## Public website rule

Do not put maintainer-only notes inside `docs/` unless they are intended to be published.

## Example pages and the create-examples tool

Example pages and the create-examples page are built by separate scripts and
documented in `project-docs/example-pages.md`:

```bash
python scripts/build_example_pages.py            # src/examples snippets -> docs/examples pages
python scripts/build_create_examples_page.py      # docs/create-examples/index.html
```

Both are also run and `--check`ed by `run_generator_checks.py`.
