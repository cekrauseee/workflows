#!/usr/bin/env python3
"""Check local Markdown links in an existing documentation layout, read-only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]*>|(?:[^\s()]|\([^()]*\))+)(?:\s+[^)]*)?\)")
REFERENCE = re.compile(r"^ {0,3}\[([^]\n]+)\]:\s*(<[^>]*>|\S+)", re.MULTILINE)
REFERENCE_USE = re.compile(r"!?\[([^]\n]+)\]\[([^]\n]*)\]")


def prose_only(text: str) -> str:
    lines = []
    fence_char, fence_len = "", 0
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence_char:
            if match and match.group(1)[0] == fence_char and len(match.group(1)) >= fence_len:
                fence_char = ""
            continue
        if match:
            fence_char, fence_len = match.group(1)[0], len(match.group(1))
            continue
        lines.append(line)
    return re.sub(r"(`+)[^\n]*?\1", "", "\n".join(lines))


def destinations(text: str) -> tuple[list[str], list[str]]:
    prose = prose_only(text)
    refs = {" ".join(label.lower().split()): dest for label, dest in REFERENCE.findall(prose)}
    targets = [match.group(1) for match in INLINE_LINK.finditer(prose)]
    # Definitions are checked even when their shortcut use cannot be parsed reliably.
    targets.extend(refs.values())
    missing = []
    for text_label, ref_label in REFERENCE_USE.findall(prose):
        label = " ".join((ref_label or text_label).lower().split())
        if label not in refs:
            missing.append(label)
    return targets, missing


def local_target(root: Path, source: Path, value: str) -> Path | None:
    value = value.strip().removeprefix("<").removesuffix(">")
    value = re.sub(r"\\([\\() ])", r"\1", value)
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    return (root / path.lstrip("/") if path.startswith("/") else source.parent / path).resolve()


def scoped_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"scope leaves project: {relative!r}")
    return path


def check(root: Path, paths: list[str] | None, required: list[str], line_limit: int | None) -> dict[str, object]:
    issues, warnings = [], []
    scopes = [scoped_path(root, item) for item in paths] if paths else [root / name for name in ("README.md", "docs", "doc", "documentation") if (root / name).exists()]
    for relative in required:
        if not scoped_path(root, relative).exists():
            issues.append(f"missing required path: {relative}")
    files = set()
    for scope in scopes:
        if not scope.exists():
            issues.append(f"missing requested path: {scope.relative_to(root).as_posix()}")
        elif scope.is_dir():
            files.update(path for path in scope.rglob("*.md") if path.is_file() and ".git" not in path.relative_to(root).parts)
        elif scope.suffix.lower() == ".md":
            files.add(scope)
        else:
            raise ValueError(f"scope is not Markdown or a directory: {scope}")
    checked = []
    for path in sorted(files):
        relative = path.relative_to(root).as_posix()
        if not path.resolve().is_relative_to(root):
            issues.append(f"document symlink leaves project: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        checked.append(relative)
        if line_limit is not None and len(text.splitlines()) > line_limit:
            warnings.append(f"length exceeds advisory {line_limit} lines: {relative}")
        targets, missing = destinations(text)
        for value in targets:
            try:
                target = local_target(root, path, value)
            except ValueError:
                issues.append(f"invalid link: {relative} -> {value}")
                continue
            if target is not None and not target.exists():
                issues.append(f"broken link: {relative} -> {value}")
        for label in missing:
            issues.append(f"undefined link reference: {relative} -> {label}")
    if not checked:
        warnings.append("no Markdown documents matched the requested scope")
    return {"root": str(root), "files_checked": checked, "issues": sorted(set(issues)), "warnings": sorted(set(warnings))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--path", action="append", dest="paths")
    parser.add_argument("--require", action="append", default=[])
    parser.add_argument("--line-limit", type=int)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        root = Path(args.project).expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"project root is not a directory: {root}")
        if args.line_limit is not None and args.line_limit < 1:
            raise ValueError("--line-limit must be positive")
        result = check(root, args.paths, args.require, args.line_limit)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        for kind in ("issues", "warnings"):
            for message in result[kind]:
                print(f"{kind}: {message}")
        print(f"Checked {len(result['files_checked'])} Markdown files")
    return 1 if result["issues"] or (args.strict and result["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
