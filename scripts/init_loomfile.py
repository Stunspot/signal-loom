#!/usr/bin/env python3
"""Initialize a Signal Loom Infographics Loomfile from the bundled template."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
try:
    from .archive_paths import assert_chain, assert_unlinked
except ImportError:
    from archive_paths import assert_chain, assert_unlinked


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "loomfile.template"
REQUIRED_DIRECTORIES = (
    "sources/originals",
    "output/web",
    "output/carousel",
    "output/platforms",
    "checkpoints/snapshots",
)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "signal-loom-project"


def initialize(destination: Path, title: str) -> Path:
    destination = assert_chain(destination.expanduser(), allow_missing=True)
    if destination.exists():
        if destination.is_symlink():
            raise ValueError("destination must not be a symbolic link")
        if not destination.is_dir():
            raise ValueError("destination exists and is not a directory")
        if any(destination.iterdir()):
            raise ValueError("destination exists and is not empty")
        # Preserve the supplied empty directory and its metadata.
    destination.parent.mkdir(parents=True, exist_ok=True)
    assert_unlinked(TEMPLATE_ROOT)
    destination.mkdir(exist_ok=True)
    assert_chain(destination)
    for item in sorted(TEMPLATE_ROOT.rglob('*')):
        target = destination / item.relative_to(TEMPLATE_ROOT)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            assert_chain(target.parent)
            with item.open('rb') as incoming, target.open('xb') as outgoing:
                shutil.copyfileobj(incoming, outgoing)
    for relative in REQUIRED_DIRECTORIES:
        (destination / relative).mkdir(parents=True, exist_ok=True)

    project_path = destination / "project.yaml"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).isoformat()
    project.update(
        {
            "project_id": slugify(title),
            "title": title,
            "created_at": now,
            "updated_at": now,
        }
    )
    project_path.write_text(json.dumps(project, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--title", default="Untitled infographic")
    args = parser.parse_args(argv)
    try:
        created = initialize(args.destination, args.title)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Initialized Loomfile: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
