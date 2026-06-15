#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/prepare_toolkit_release.sh VERSION [YYYY-MM-DD]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

VERSION="$1"
if [ "$#" -ge 2 ]; then
  python scripts/prepare_toolkit_release.py --version "$VERSION" --date "$2"
else
  python scripts/prepare_toolkit_release.py --version "$VERSION"
fi
python scripts/build_prompt_libraries.py
python scripts/build_prompt_libraries.py --ci
python scripts/build_site_package.py --run-generator-check --version "$VERSION"
