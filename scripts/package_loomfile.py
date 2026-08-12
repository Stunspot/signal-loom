#!/usr/bin/env python3
"""Validate and package a Loomfile as a one-root ZIP with a checksum manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from .validate_loomfile import validate
except ImportError:  # Direct script execution.
    from validate_loomfile import validate


DENIED_NAMES = {".env", "id_rsa", "id_ed25519", "credentials", "credentials.json"}
DENIED_SUFFIXES = {".key", ".pem", ".pfx", ".p12"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def _temporary_path(directory: Path, prefix: str, suffix: str) -> Path:
    descriptor, name = tempfile.mkstemp(dir=directory, prefix=prefix, suffix=suffix)
    os.close(descriptor)
    return Path(name)


def _remove_if_present(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def package(root: Path, output: Path) -> tuple[Path, int]:
    root = root.expanduser().resolve()
    output = output.expanduser().resolve()
    if output.exists() or output.is_symlink():
        raise ValueError(f"output already exists: {output}")

    errors, warnings = validate(root)
    if errors:
        raise ValueError("Loomfile validation failed:\n- " + "\n- ".join(errors))

    manifest_path = root / "review" / "release-manifest.json"
    files: list[Path] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if path.is_symlink():
            raise ValueError(f"symbolic links are not packaged: {path.relative_to(root)}")
        if not path.is_file():
            continue
        if path.name.lower() in DENIED_NAMES or path.suffix.lower() in DENIED_SUFFIXES:
            raise ValueError(f"secret-like file denied: {path.relative_to(root)}")
        if path != manifest_path:
            files.append(path)

    manifest = {
        "status": "packaged",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "warnings": warnings,
        "files": [
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
            for path in files
        ],
    }
    manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_archive = None
    temporary_manifest = None
    output_committed = False

    try:
        temporary_archive = _temporary_path(output.parent, f".{output.name}.", ".tmp")
        temporary_manifest = _temporary_path(manifest_path.parent, ".release-manifest.", ".tmp")
        temporary_manifest.write_bytes(manifest_bytes)
        with zipfile.ZipFile(
            temporary_archive,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in files:
                archive.write(path, f"{root.name}/{path.relative_to(root).as_posix()}")
            archive.writestr(f"{root.name}/review/release-manifest.json", manifest_bytes)

        # A hard link atomically creates the final name without overwriting a file
        # created after the initial guard. The temporary archive is on the same volume.
        os.link(temporary_archive, output)
        output_committed = True
        _remove_if_present(temporary_archive)
        temporary_archive = None
        os.replace(temporary_manifest, manifest_path)
        temporary_manifest = None
        return output, len(files) + 1
    except BaseException:
        if output_committed:
            _remove_if_present(output)
        raise
    finally:
        if temporary_archive is not None:
            _remove_if_present(temporary_archive)
        if temporary_manifest is not None:
            _remove_if_present(temporary_manifest)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("loomfile", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    try:
        output, count = package(args.loomfile, args.output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Packaged {count} files: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
