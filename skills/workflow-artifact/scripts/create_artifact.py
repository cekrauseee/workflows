#!/usr/bin/env python3
"""Create a portable HTML scaffold at an explicit destination atomically."""
from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile

def render(title: str, summary: str, lang: str = "en") -> str:
    safe_title = html.escape(title)
    safe_summary = html.escape(summary)
    return f"""<!doctype html>
<html lang="{html.escape(lang, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>
    :root {{ color-scheme: light dark; font-family: ui-sans-serif, system-ui, sans-serif; line-height: 1.5; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: Canvas; color: CanvasText; }}
    a {{ color: LinkText; }}
    a:focus-visible, button:focus-visible {{ outline: 3px solid Highlight; outline-offset: 3px; }}
    .skip-link {{ position: absolute; left: 1rem; top: -4rem; padding: .5rem .75rem; background: Canvas; }}
    .skip-link:focus {{ top: 1rem; }}
    header, main {{ width: min(72rem, calc(100% - 2rem)); margin-inline: auto; }}
    header {{ padding-block: 3rem 1rem; border-bottom: 1px solid GrayText; }}
    main {{ padding-block: 2rem 4rem; }}
    h1 {{ max-width: 24ch; margin: 0; font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.1; }}
    .summary {{ max-width: 70ch; font-size: 1.1rem; }}
    section {{ max-width: 70rem; margin-top: 2rem; }}
  </style>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header>
    <h1>{safe_title}</h1>
    <p class="summary">{safe_summary}</p>
  </header>
  <main id="main-content">
    <section aria-labelledby="overview-heading">
      <h2 id="overview-heading">Overview</h2>
      <p>{safe_summary}</p>
    </section>
  </main>
</body>
</html>
"""



def write_artifact(target: Path, content: str, replace: bool) -> str:
    if target.is_symlink():
        raise ValueError(f"refusing symlink output: {target}")
    if target.exists():
        if not target.is_file():
            raise ValueError(f"output is not a file: {target}")
        if target.read_text(encoding="utf-8") == content:
            return "unchanged"
        if not replace:
            raise ValueError(f"output exists with different content: {target}; use --replace only for intended replacement")
    target.parent.mkdir(parents=True, exist_ok=True)
    existed = target.exists()
    fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if replace:
            os.replace(temporary, target)
        else:
            os.link(temporary, target)
        return "replaced" if existed else "created"
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--lang", default="en")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    try:
        target = args.output.expanduser().absolute()
        if target.suffix.lower() != ".html":
            raise ValueError("output must use the .html extension")
        if not args.title.strip() or not args.summary.strip():
            raise ValueError("title and summary must not be empty")
        if not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", args.lang):
            raise ValueError("lang must be a language tag such as en or pt-BR")
        status = write_artifact(target, render(args.title.strip(), args.summary.strip(), args.lang), args.replace)
        print(json.dumps({"path": str(target.resolve()), "status": status}))
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"ok": False, "errors": [str(error)]}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
