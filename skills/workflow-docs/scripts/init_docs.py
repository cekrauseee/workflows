#!/usr/bin/env python3
"""Create only selected missing Markdown scaffolds, without replacing existing files."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
import sys


def target_path(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or path.suffix.lower() != ".md":
        raise ValueError(f"expected a project-relative Markdown path: {relative!r}")
    target = root / path
    for candidate in [target, *target.parents]:
        if candidate == root:
            break
        if candidate.is_symlink():
            raise ValueError(f"symlink path is not supported: {relative!r}")
    if not target.resolve().is_relative_to(root):
        raise ValueError(f"path leaves project: {relative!r}")
    if target.exists() and not target.is_file():
        raise ValueError(f"target is not a regular file: {relative!r}")
    for parent in target.parents:
        if parent == root:
            break
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"parent is not a directory: {relative!r}")
    return target


def scaffold(path: Path, project_title: str) -> str:
    heading = project_title if path.name.lower() == "readme.md" else path.stem.replace("-", " ").replace("_", " ").capitalize()
    return f"# {heading}\n\nDescribe this topic using verified project sources.\n"


def create_missing(target: Path, content: str) -> bool:
    """Publish a complete new file atomically; never overwrite a concurrent creator."""
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError:
            return False
        return True
    finally:
        os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--file", action="append", dest="files")
    parser.add_argument("--title", default="Project")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        root = Path(args.project).expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"project root is not a directory: {root}")
        if not args.title.strip() or "\n" in args.title or "\r" in args.title:
            raise ValueError("title must be one nonempty line")
        targets = list(dict.fromkeys(target_path(root, path) for path in args.files or ["README.md"]))
        created, preserved, planned = [], [], []
        for target in targets:
            relative = target.relative_to(root).as_posix()
            if target.exists():
                preserved.append(relative)
            elif args.dry_run:
                planned.append(relative)
            elif create_missing(target, scaffold(target, args.title.strip())):
                created.append(relative)
            else:
                preserved.append(relative)
        print(json.dumps({"root": str(root), "created": created, "preserved": preserved, "planned": planned,
                          "requires_content_review": bool(created or planned)}, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"ok": False, "errors": [str(error)]}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
