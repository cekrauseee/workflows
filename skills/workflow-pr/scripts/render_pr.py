#!/usr/bin/env python3
"""Render optional pull request sections or preserve an existing template body."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from validate_conventional import validate_branch, validate_message


def bullets(values: list[str], section: str, routed: bool = False) -> str:
    result = []
    for value in values:
        value = value.strip()
        if not value:
            raise ValueError(f"{section} items must not be empty")
        if routed:
            target, separator, description = value.partition("=")
            target, description = target.strip(), description.strip()
            if not separator or not target or not description or "`" in target or "\n" in target:
                raise ValueError(f"{section} items must use target=description with a simple nonempty target")
            value = f"`{target}`: {description}"
        result.append("- " + value.replace("\n", "\n  "))
    return "\n".join(result)


def render_body(args: argparse.Namespace) -> str:
    sections = [("Desired behavior", args.behavior, False), ("Change map", args.change, True),
                ("Verification", args.verification, False), ("Review focus", args.review, True), ("Risks", args.risk, False)]
    if args.body_file:
        if any(values for _, values, _ in sections):
            raise ValueError("--body-file cannot be combined with generated section flags")
        body = args.body_file.read_text(encoding="utf-8")
        if not body.strip():
            raise ValueError("body file is empty")
        return body
    summary = args.summary.strip()
    if not summary:
        raise ValueError("summary must not be empty")
    parts = [summary]
    for name, values, routed in sections:
        if values:
            parts.append(f"## {name}\n\n{bullets(values, name, routed)}")
    return "\n\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--branch", default="")
    parser.add_argument("--allow-nonconventional-title", action="store_true")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--summary", "--goal", dest="summary")
    source.add_argument("--body-file", type=Path)
    for name in ("behavior", "change", "verification", "review", "risk"):
        parser.add_argument("--" + name, action="append", default=[])
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    errors, warnings = validate_message(args.title)
    if not args.title.strip() or "\n" in args.title or "\r" in args.title:
        errors = ["title must be one nonempty line"]
    elif errors and args.allow_nonconventional_title:
        warnings.append("nonconventional title preserved by explicit option")
        errors = []
    try:
        errors += validate_branch(args.branch)
        body = render_body(args)
    except ValueError as error:
        errors.append(str(error))
        body = ""
    except (OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    payload = {"ok": not errors, "title": args.title, "body": body, "errors": errors, "warnings": warnings}
    if args.branch:
        payload["branch"] = args.branch
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        if not errors:
            print(body, end="")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
