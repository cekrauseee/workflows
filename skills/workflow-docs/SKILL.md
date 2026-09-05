---
name: workflow-docs
description: Create, maintain, or audit developer documentation while preserving the project's existing structure and verifying claims against source.
---

# Documentation

Produce accurate, navigable project documentation at the requested scope. Inputs are the project, affected behavior or requested documentation mode, and any existing structure or style. Preserve current locations, generators, templates, and language choices unless a migration is part of the request.

## Choose the mode

- **Create or fill gaps:** Read [initialization](references/initialize.md). Inspect existing documentation before choosing new files. The helper creates only the paths you select and never overwrites content.
- **Update:** Read [maintenance](references/maintain.md). Change the narrowest canonical explanation and its affected routes.
- **Audit:** Read [audit](references/audit.md). Check links and structural issues, then compare claims with relevant source/configuration/tests. An audit alone does not authorize edits.

Use English and concise prose as defaults, honoring explicit project or user choices. Keep one canonical explanation and link to it. Treat proposed layouts and length thresholds as aids to navigation, not mandatory structure or arbitrary splitting rules. Never invent setup commands, architecture, verification, or product behavior.

No HTML output is required by this skill. Use an artifact workflow only when the requested deliverable benefits from a standalone HTML explanation. Temporary work may live in any appropriate user/host-selected location; no Harness workspace or fixed scratch path is required.

Completion includes the actual files created or updated, facts or checks used to verify them, and any remaining uncertainty. For an audit, return actionable findings and coverage; do not disguise an unverified claim as a broken-link result. If installed Harness is available and relevant continuity is needed, read its `scripts/harness.py consolidate --project PATH` report without initializing it.
