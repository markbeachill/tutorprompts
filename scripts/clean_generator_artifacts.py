#!/usr/bin/env python3
"""Clean local package-generator temporary files.

This script is intentionally conservative. By default it only prints what it
would remove. Use --apply to actually delete files/directories.

It targets local build/check by-products such as Python bytecode caches and
temporary generated/ comparison folders. It does not delete source files, docs
outputs, archive folders, prompt-library ZIPs, audit ZIPs, or site packages
unless explicitly asked to include dist/.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def iter_targets(*, include_dist: bool = False) -> list[Path]:
    targets: list[Path] = []
    skip_dirs = {".git"}
    for path in ROOT.rglob("*"):
        rel_parts = set(path.relative_to(ROOT).parts)
        if rel_parts & skip_dirs:
            continue
        if path.is_dir() and path.name == "__pycache__":
            targets.append(path)
        elif path.is_file() and path.suffix == ".pyc":
            targets.append(path)
        elif path.is_dir() and path.name == "generated":
            targets.append(path)
    if include_dist:
        dist = ROOT / "dist"
        if dist.exists():
            targets.append(dist)
    # Remove children before parents where both appear.
    return sorted(set(targets), key=lambda p: len(p.parts), reverse=True)


def remove_target(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove local temporary package-generator artifacts. Defaults to dry run."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete the listed files/directories. Without this, only list them.",
    )
    parser.add_argument(
        "--include-dist",
        action="store_true",
        help="Also remove the dist/ folder. Use only if you no longer need built package ZIPs.",
    )
    args = parser.parse_args()

    targets = iter_targets(include_dist=args.include_dist)
    print("Package Generator clean-up")
    print(f"Repository root: {ROOT}")
    print()
    if not targets:
        print("No temporary generator artifacts found.")
        return 0

    action = "Removing" if args.apply else "Would remove"
    for target in targets:
        print(f"{action}: {target.relative_to(ROOT)}")
        if args.apply:
            remove_target(target)
    print()
    if args.apply:
        print(f"Removed {len(targets)} item(s).")
    else:
        print(f"Dry run only. Re-run with --apply to remove {len(targets)} item(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
