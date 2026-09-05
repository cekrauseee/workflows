# Artifact implementation

## Creation

`create_artifact.py OUTPUT.html --title TEXT --summary TEXT [--lang CODE] [--replace]` creates a responsive single-file baseline. Defaults are English, system fonts, semantic header/main, visible focus, and CSS using system colors. Adapt them to the user's visual goal. Output can be any appropriate destination; there is no mandatory project or temporary path.

By default, existing identical content is unchanged and differing content is an error. `--replace` permits atomic replacement of this one named file. Symlink output paths are rejected. The helper does not create a catalog or rewrite documentation automatically. Exit 0 returns JSON with the absolute path and `created`, `unchanged`, or `replaced` status; exit 2 reports invalid input or filesystem failure.

When adding the completed file to project documentation, edit the existing route in its own format and inspect the final link. For a one-off output, deliver the absolute file link directly.

## Checks

`check_artifacts.py FILE_OR_DIRECTORY... --format json` scans named `.html` files or HTML files recursively in named directories. It checks HTML doctype, nonempty language/title, UTF-8 declaration, viewport, a main landmark, one h1, and image alt attributes. It detects common external and sibling-file runtime dependencies in HTML attributes, CSS URLs/imports, inline style, scripts, and SVG image/use references. Normal supporting links are allowed. Optional `--index FILE` checks links from that specific catalog; no catalog is required otherwise.

Exit 0 means these static checks passed, 1 means contract violations, and 2 means invalid inputs. No HTML in a requested directory is an input error. The JSON result reports `files_checked`, `issues`, and `warnings`.

The scanner uses the standard library, not a browser or full JavaScript/CSS parser. Detection of network APIs and module imports is heuristic; it is not a security sandbox. Inspect complex code and generated URLs yourself. It cannot prove contrast, responsive layout, keyboard behavior, semantic truth, or the correctness of an alt description. Use proportionate manual or browser QA when requested or materially needed, and report its limits.
