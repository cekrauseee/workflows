---
name: workflow-pr
description: Draft or update evidence-based pull request titles and descriptions from the complete diff, and publish when requested.
---

# Pull request

Confirm the repository, base, head, and any existing PR or template. Inspect the complete base-to-head diff and included commits. Check local status because uncommitted changes are absent from the published PR.

Lead the title and description with the concrete problem and resulting behavior. Preserve the repository template and scale detail to the change. Include verification actually performed and material risks or limitations; do not invent headings or evidence. Prefer an English Conventional Commit title while honoring user and project choices. Branch names and supporting commit types do not determine the PR type.

Drafting is read-only. Create or update a remote PR only when requested, and treat merging as a separate action. Before publication, verify the current base, head, remote branch, and diff; preserve real newlines in the body. Re-read the published PR and report its URL.

If the project uses an installed Harness, follow its current coordination instructions when relevant. Do not initialize Harness or assume its commands or state format.
