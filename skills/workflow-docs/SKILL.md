---
name: workflow-docs
description: Create, maintain, or audit developer documentation while preserving the project's existing structure and verifying claims against source.
---

# Documentation

Inspect the current documentation layout, repository instructions, generators, and relevant source before deciding what belongs where. Preserve existing locations, templates, navigation, and language unless the request includes a migration.

For new documentation, create only the files the project needs. For updates, change the narrowest canonical explanation and affected links or examples. For audits, check navigation, local links, duplicated guidance, and claims against source, configuration, and tests. An audit request is read-only.

Use concise English by default while honoring user and project choices. Keep one canonical explanation and link to it. Do not invent commands, architecture, behavior, or verification. Run the project's documentation checks when relevant and report any material validation gap.

If the project uses an installed Harness, follow its current coordination instructions when relevant. Do not initialize Harness or assume its commands or state format.
