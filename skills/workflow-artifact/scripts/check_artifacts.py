#!/usr/bin/env python3
"""Check standalone HTML structure and common runtime dependencies, read-only."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

DOCTYPE = re.compile(r"^\s*<!doctype\s+html\s*>", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\s+(?:url\()?\s*['\"]?([^'\")\s;]+)", re.IGNORECASE)
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)", re.IGNORECASE)
NETWORK_API = re.compile(r"\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\s*(?:\(|\.)")
MODULE_IMPORT = re.compile(r"\b(?:import\s*(?:\(\s*)?|(?:import|export)\s+[^;\n]*?\s+from\s*)['\"]([^'\"]+)['\"]")


def dependency(value: str) -> bool:
    value = value.strip()
    return bool(value) and not value.lower().startswith("data:") and not value.startswith("#")


class ArtifactParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.charset = False
        self.viewport = False
        self.main_count = 0
        self.h1_count = 0
        self.title_parts = []
        self.script_parts = []
        self.style_parts = []
        self.dependencies = []
        self.images_without_alt = 0
        self._title = self._script = self._style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict((key.lower(), value or "") for key, value in attrs)
        tag = tag.lower()
        if tag == "html":
            self.lang = values.get("lang", "")
        elif tag == "meta":
            self.charset |= values.get("charset", "").lower() in {"utf-8", "utf8"}
            if values.get("http-equiv", "").lower() == "content-type":
                self.charset |= bool(re.search(r"charset\s*=\s*utf-?8", values.get("content", ""), re.I))
            self.viewport |= values.get("name", "").lower() == "viewport" and bool(values.get("content", ""))
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self._title = True
        elif tag == "script":
            self._script = True
        elif tag == "style":
            self._style = True
        elif tag == "img" and "alt" not in values:
            self.images_without_alt += 1
        if "style" in values:
            self.style_parts.append(values["style"])
        for attribute, value in values.items():
            if attribute.startswith("on"):
                self.script_parts.append(value)
        attrs_to_check = []
        if tag in {"script", "img", "iframe", "audio", "video", "source", "embed", "track", "input"}:
            attrs_to_check.append("src")
        if tag == "object":
            attrs_to_check.append("data")
        if tag == "video":
            attrs_to_check.append("poster")
        if tag in {"image", "use"}:
            attrs_to_check.extend(("href", "xlink:href"))
        if tag == "link" and set(values.get("rel", "").lower().split()) & {"stylesheet", "icon", "preload", "modulepreload", "prefetch", "manifest", "mask-icon"}:
            attrs_to_check.append("href")
        for attribute in attrs_to_check:
            value = values.get(attribute, "").strip()
            if dependency(value):
                self.dependencies.append(value)
        if tag in {"img", "source"} and values.get("srcset"):
            for match in re.finditer(r"(?:^|,\s*)(data:[^\s]+|[^\s,]+)(?:\s+[^,]*)?", values["srcset"]):
                if dependency(match.group(1)):
                    self.dependencies.append(match.group(1))
        if tag == "iframe" and values.get("srcdoc"):
            nested = ArtifactParser()
            nested.feed(values["srcdoc"])
            self.dependencies.extend(nested.dependencies)
            self.script_parts.extend(nested.script_parts)
            self.style_parts.extend(nested.style_parts)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._title = False
        elif tag == "script":
            self._script = False
        elif tag == "style":
            self._style = False

    def handle_data(self, text: str) -> None:
        if self._title:
            self.title_parts.append(text)
        if self._script:
            self.script_parts.append(text)
        if self._style:
            self.style_parts.append(text)


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    issues = []
    if not DOCTYPE.search(text):
        issues.append("missing HTML doctype")
    parser = ArtifactParser()
    parser.feed(text)
    parser.close()
    if not parser.lang.strip():
        issues.append("missing document language")
    if not parser.charset:
        issues.append("missing UTF-8 charset metadata")
    if not parser.viewport:
        issues.append("missing viewport metadata")
    if not "".join(parser.title_parts).strip():
        issues.append("missing title")
    if parser.main_count != 1:
        issues.append("expected one main landmark")
    if parser.h1_count != 1:
        issues.append("expected one h1")
    if parser.images_without_alt:
        issues.append("image missing alt attribute")
    for value in parser.dependencies:
        issues.append(f"runtime dependency: {value}")
    css = "\n".join(parser.style_parts)
    for value in CSS_IMPORT.findall(css) + CSS_URL.findall(css):
        if dependency(value):
            issues.append(f"CSS dependency: {value.strip()}")
    script = "\n".join(parser.script_parts)
    if NETWORK_API.search(script):
        issues.append("network API in script; inspect the reachable code")
    for value in MODULE_IMPORT.findall(script):
        if dependency(value):
            issues.append(f"module dependency: {value}")
    return sorted(set(issues))


def index_targets(index: Path) -> set[Path]:
    targets = set()
    for match in re.finditer(r"\[[^]]*\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+[^)]*)?\)", index.read_text(encoding="utf-8")):
        value = match.group(1).strip("<>")
        parsed = urlsplit(value)
        if parsed.path and not parsed.scheme and not parsed.netloc:
            targets.add((index.parent / unquote(parsed.path)).resolve())
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--index", type=Path, help="Optional explicit Markdown catalog to check")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        paths = set()
        for raw in args.paths:
            path = raw.expanduser().resolve()
            if path.is_dir():
                matched = list(path.rglob("*.html"))
                if not matched:
                    raise ValueError(f"no HTML files in requested directory: {path}")
                paths.update(matched)
            elif path.is_file() and path.suffix.lower() == ".html":
                paths.add(path)
            else:
                raise ValueError(f"not an HTML file or directory: {path}")
        indexed = index_targets(args.index.expanduser().resolve()) if args.index else None
        issues = []
        for path in sorted(paths):
            issues.extend(f"{path}: {item}" for item in validate(path))
            if indexed is not None and path.resolve() not in indexed:
                issues.append(f"{path}: missing link in requested catalog")
        result = {"files_checked": [str(path) for path in sorted(paths)], "issues": sorted(set(issues)), "warnings": []}
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        for issue in result["issues"]:
            print(f"issue: {issue}")
        print(f"Checked {len(paths)} HTML files")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
