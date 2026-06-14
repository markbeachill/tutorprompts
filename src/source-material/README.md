# Source material library

This folder contains copy-ready source material used by tutor tools, examples and deployment checks.

Edit Markdown files in `src/source-material/items/`, then rebuild the public source-material page with:

```bash
python scripts/build_source_material_library.py
```

Check that the generated files are current with:

```bash
python scripts/build_source_material_library.py --check
```

Each item uses a small front-matter block followed by the source text to display and copy.
