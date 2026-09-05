# Audit documentation

Run deterministic checks on the actual layout:

```bash
python3 scripts/check_docs.py PATH --path README.md --path documentation --format json
```

Without `--path`, the checker scans a root README plus existing `docs/`, `doc/`, and `documentation/` directories. It does not require a baseline or index. Use repeated `--require RELATIVE_PATH` only for explicit project requirements. Missing targets of local Markdown links are errors. Markdown code fences and inline code are ignored; inline, image, and reference-style links are checked. HTTP links are not fetched. Fragments are not verified because heading IDs differ across renderers. Renderer-specific extensions and generated routes may need manual verification.

Use `--line-limit N` to request advisory size warnings, and `--strict` only when intentionally treating warnings as failure. There is no implicit size threshold. Exit 0 means no failing findings, 1 means issues (or strict warnings), and 2 means invalid scope or inaccessible input. JSON returns `files_checked`, `issues`, and `warnings`. No matching documents produces a warning; it does not justify creating new structure during an audit.

Then review semantic accuracy: trace commands and behavior to relevant source, inspect navigation and duplicated explanations, and check whether diagrams still represent the system. Explain semantic defects separately from structural checks. HTML accessibility and self-containment require an appropriate artifact check; this Markdown checker does not claim to audit them. Re-run only affected checks after authorized fixes.
