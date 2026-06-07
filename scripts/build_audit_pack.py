#!/usr/bin/env python3
"""Build/check the AI Personal Tutor audit/testing pack from source files.

Package Generator v1.9 helper.

This script mirrors the prompt-library generator discipline for the testing pack:
source files live under src/audit-library/files/, while docs/audit-library/latest/,
docs/audit-library/v<testing_pack_version>/ and the testing-pack ZIP are generated outputs.

Typical use from the repository root:
    python scripts/build_audit_pack.py
    python scripts/build_audit_pack.py --check
    python scripts/build_audit_pack.py --validate
"""
from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "audit-library"
FILES_DIR = SRC / "files"
MANIFEST = SRC / "audit-pack.yml"
RELEASE_YML = ROOT / "src" / "release.yml"
FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)


@dataclass(frozen=True)
class AuditSpec:
    pack_id: str
    title: str
    latest_dir: str
    archive_dir_template: str
    zip_latest: str
    zip_archive_template: str
    files: list[str]


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def read_simple_yaml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list: str | None = None
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            current_list = stripped[:-1]
            data[current_list] = []
            continue
        if current_list and line.startswith("  - "):
            assert isinstance(data[current_list], list)
            data[current_list].append(_unquote(line[4:]))
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = _unquote(value)
            current_list = None
    return data


def read_release_version() -> str:
    data = read_simple_yaml(RELEASE_YML)
    version = str(data.get("testing_pack_version") or data.get("toolkit_version") or "").strip().lstrip("v")
    if not re.fullmatch(r"\d+(?:\.\d+)*", version):
        raise SystemExit("Could not read a valid testing_pack_version from src/release.yml")
    return version


def version_suffix(version: str) -> str:
    return version.replace(".", "_")


def load_spec() -> AuditSpec:
    raw = read_simple_yaml(MANIFEST)
    required = ["pack_id", "title", "latest_dir", "archive_dir_template", "zip_latest", "zip_archive_template", "files"]
    missing = [key for key in required if key not in raw or raw[key] in ("", [])]
    if missing:
        raise SystemExit("Missing audit-pack manifest field(s): " + ", ".join(missing))
    files = raw["files"]
    if not isinstance(files, list) or not all(isinstance(item, str) and item.endswith(".md") for item in files):
        raise SystemExit("audit-pack.yml files must be a list of Markdown filenames")
    return AuditSpec(
        pack_id=str(raw["pack_id"]),
        title=str(raw["title"]),
        latest_dir=str(raw["latest_dir"]),
        archive_dir_template=str(raw["archive_dir_template"]),
        zip_latest=str(raw["zip_latest"]),
        zip_archive_template=str(raw["zip_archive_template"]),
        files=list(files),
    )


def archive_name(filename: str, version: str) -> str:
    stem = filename[:-3] if filename.endswith(".md") else filename
    return f"{stem}_v{version_suffix(version)}.md"


def render_outputs(spec: AuditSpec, version: str, base: Path) -> list[Path]:
    latest_dir = base / spec.latest_dir
    archive_dir = base / spec.archive_dir_template.format(version=version, version_us=version_suffix(version))
    latest_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for filename in spec.files:
        source = FILES_DIR / filename
        if not source.exists():
            raise SystemExit(f"Missing audit source file: {rel(source)}")
        text = source.read_text(encoding="utf-8")
        latest_path = latest_dir / filename
        archive_path = archive_dir / archive_name(filename, version)
        latest_path.write_text(text, encoding="utf-8", newline="\n")
        archive_path.write_text(text, encoding="utf-8", newline="\n")
        written.extend([latest_path, archive_path])

    zip_latest = base / spec.zip_latest
    zip_archive = base / spec.zip_archive_template.format(version=version, version_us=version_suffix(version))
    for zip_path in (zip_latest, zip_archive):
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for filename in sorted(spec.files):
                latest_path = latest_dir / filename
                info = zipfile.ZipInfo(filename, FIXED_ZIP_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, latest_path.read_bytes())
        written.append(zip_path)
    return written


def build(spec: AuditSpec, version: str) -> None:
    written = render_outputs(spec, version, ROOT)
    print(f"Built audit/testing pack v{version}:")
    for path in written:
        print(f"  - {rel(path)}")


def first_diff(path: Path, expected: Path) -> list[str]:
    if path.suffix == ".zip":
        return [f"Binary ZIP differs: {rel(path)}"]
    old = path.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True) if path.exists() else []
    new = expected.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
    return list(difflib.unified_diff(old, new, fromfile=rel(path), tofile="generated/" + rel(path), n=3))[:80]


def check(spec: AuditSpec, version: str) -> bool:
    with tempfile.TemporaryDirectory(prefix="audit-pack-check-") as tmp:
        tmp_root = Path(tmp)
        generated_root = tmp_root / "generated"
        render_outputs(spec, version, generated_root)
        generated_files = [p for p in generated_root.rglob("*") if p.is_file()]
        stale: list[tuple[Path, Path]] = []
        missing: list[Path] = []
        for generated in generated_files:
            relative = generated.relative_to(generated_root)
            actual = ROOT / relative
            if not actual.exists():
                missing.append(actual)
            elif actual.read_bytes() != generated.read_bytes():
                stale.append((actual, generated))
        if not missing and not stale:
            print("Audit/testing pack generated files are up to date.")
            return True
        print("Audit/testing pack generated files are out of date:")
        for path in missing[:20]:
            print(f"  - missing {rel(path)}")
        for actual, _generated in stale[:20]:
            print(f"  - {rel(actual)}")
        if stale:
            print("\nFirst diff lines:")
            for line in first_diff(stale[0][0], stale[0][1]):
                print(line, end="" if line.endswith("\n") else "\n")
        print("\nCommon fix:")
        print("  python scripts\\build_audit_pack.py")
        print("  python scripts\\build_audit_pack.py --check")
        return False


def validate(spec: AuditSpec, version: str) -> bool:
    problems: list[str] = []
    if len(spec.files) != len(set(spec.files)):
        problems.append("audit-pack.yml contains duplicate filenames")
    for filename in spec.files:
        path = FILES_DIR / filename
        if not path.exists():
            problems.append(f"missing source file: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "v" + version not in text and f"version: {version}" not in text:
            problems.append(f"{rel(path)} does not appear to contain v{version} / version: {version}")
    latest_dir = ROOT / spec.latest_dir
    expected_members = set(spec.files)
    zip_path = ROOT / spec.zip_latest
    if zip_path.exists():
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                members = {name for name in zf.namelist() if not name.endswith("/")}
                if members != expected_members:
                    problems.append("latest testing-pack ZIP members differ: " + ", ".join(sorted(members)))
                else:
                    for filename in spec.files:
                        latest_file = latest_dir / filename
                        if latest_file.exists() and zf.read(filename) != latest_file.read_bytes():
                            problems.append(f"ZIP copy differs from latest file: {filename}")
        except zipfile.BadZipFile:
            problems.append(f"invalid ZIP: {rel(zip_path)}")
    else:
        problems.append(f"missing latest testing-pack ZIP: {rel(zip_path)}")

    if problems:
        print("Audit/testing pack validation: PROBLEMS FOUND")
        for problem in problems:
            print(f"  - {problem}")
        return False
    print(f"Audit/testing pack validation: OK ({len(spec.files)} file(s), v{version})")
    return True


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build/check the audit/testing pack from source files.")
    parser.add_argument("--check", action="store_true", help="Do not write files; fail if generated audit/testing outputs are stale.")
    parser.add_argument("--validate", action="store_true", help="Validate audit source and ZIP contents.")
    parser.add_argument("--ci", action="store_true", help="Run --check and --validate.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    spec = load_spec()
    version = read_release_version()
    ok = True
    if args.ci:
        ok = check(spec, version) and validate(spec, version)
    elif args.check:
        ok = check(spec, version)
    elif args.validate:
        ok = validate(spec, version)
    else:
        build(spec, version)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
