#!/usr/bin/env python3
"""Check Conventional Commit structure with advisory editorial guidance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

COMMON_TYPES = ("feat", "fix", "docs", "refactor", "perf", "test", "build", "ci", "style", "chore", "revert")
HEADER_RE = re.compile(r"^(?P<type>[A-Za-z][A-Za-z0-9-]*)(?:\((?P<scope>[^()\r\n]+)\))?!?: (?P<description>\S[^\r\n]*)$")


def validate_message(message: str) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    lines = message.splitlines()
    if not lines or not lines[0].strip():
        return ["message is empty"], []
    header = lines[0]
    match = HEADER_RE.fullmatch(header)
    if not match:
        errors.append("header must match type(optional-scope)(optional-!): description")
    else:
        kind = match.group("type")
        if kind != kind.lower():
            warnings.append("prefer a lowercase type")
        if kind.lower() not in COMMON_TYPES:
            warnings.append(f"type {kind!r} is valid but outside the common workflow vocabulary")
        if match.group("description").endswith("."):
            warnings.append("prefer a description without a terminal period")
        if header != header.rstrip():
            warnings.append("prefer no trailing header whitespace")
    if len(header) > 72:
        warnings.append("header exceeds the advisory 72-character target")
    if len(lines) > 1 and lines[1].strip():
        errors.append("body must be separated from the header by a blank line")
    return errors, warnings


def validate_branch(branch: str) -> list[str]:
    if not branch:
        return []
    result = subprocess.run(["git", "check-ref-format", f"refs/heads/{branch}"], capture_output=True, text=True, check=False)
    return [f"invalid Git branch name: {branch!r}"] if branch == "HEAD" or branch.startswith("-") or result.returncode else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--message")
    source.add_argument("--message-file", type=Path)
    parser.add_argument("--branch", default="")
    parser.add_argument("--strict-style", action="store_true", help="Explicitly fail on editorial warnings")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        message = args.message if args.message is not None else args.message_file.read_text(encoding="utf-8")
        errors, warnings = validate_message(message.rstrip("\n"))
        errors += validate_branch(args.branch)
    except (OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    ok = not errors and not (args.strict_style and warnings)
    if args.format == "json":
        print(json.dumps({"ok": ok, "errors": errors, "warnings": warnings}, indent=2))
    else:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        if ok:
            print("valid")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
