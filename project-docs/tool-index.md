# Tool index and metadata

This document explains where the current tool list comes from. It is not intended to duplicate the whole tool catalogue by hand.

## Source of truth

Tool metadata is edited here:

```text
src/prompt-library/tool-metadata.json
src/prompt-library/tools/
src/prompt-library/packs/
```

Generated tool data is written here:

```text
docs/data/tool_index.json
docs/prompt-libraries/single-tools/
```

The website pages use generated metadata and page-generation logic rather than a separate hand-maintained tool list.

## Why not keep a full hand-written tool list here?

Tool names, codes and routing can change during releases. A hand-written maintainer list can go stale. For the current tool list, inspect `src/prompt-library/tool-metadata.json` or `docs/data/tool_index.json`.
