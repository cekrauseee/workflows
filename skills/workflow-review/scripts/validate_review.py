#!/usr/bin/env python3
"""Validate structured review findings without editing or publishing anything."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PRIORITIES = {"P0", "P1", "P2", "P3"}
REQUIRED_TEXT = ("title", "file", "evidence", "impact", "direction")


def validate_payload(payload: object) -> tuple[list[str], list[str]]:
    findings = payload.get("findings") if isinstance(payload, dict) else payload
    if not isinstance(findings, list):
        return ["payload must be a findings array or an object with a findings array"], []
    errors, warnings = [], []
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if not isinstance(finding.get("priority"), str) or finding["priority"] not in PRIORITIES:
            errors.append(f"{prefix}.priority must be P0, P1, P2, or P3")
        for field in REQUIRED_TEXT:
            value = finding.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} must be a nonempty string")
        start, end = finding.get("start"), finding.get("end", finding.get("start"))
        for field, value in (("start", start), ("end", end)):
            if type(value) is not int or value < 1:
                errors.append(f"{prefix}.{field} must be a positive integer")
        if type(start) is int and type(end) is int:
            if end < start:
                errors.append(f"{prefix}.end must not precede start")
            elif end - start > 10:
                warnings.append(f"{prefix}: prefer the narrowest line range supporting the finding")
        title = finding.get("title")
        if isinstance(title, str) and len(title) > 80:
            warnings.append(f"{prefix}: prefer a shorter title")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        raw = args.path.read_text(encoding="utf-8") if args.path else sys.stdin.read()
        errors, warnings = validate_payload(json.loads(raw))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings}, indent=2))
    else:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        if not errors:
            print("valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
