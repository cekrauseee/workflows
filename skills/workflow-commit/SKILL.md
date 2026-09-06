---
name: workflow-commit
description: Prepare cohesive staging groups and Conventional Commit messages from actual changes, and create commits when requested.
---

# Commit

Inspect applicable repository instructions, status, staged and unstaged diffs, relevant untracked files, and recent commit style. Determine ownership from current evidence and preserve unrelated work and staging.

Group files and hunks by cohesive intent. Tests and documentation belong with the behavior they verify or explain. Prefer an English Conventional Commit message such as `fix(cache): expire stale entries`, while honoring user and project choices. Branch names do not determine commit types.

A request for a message or plan is read-only. A request to commit includes necessary staging, but does not authorize amending, bypassing hooks, pushing, or publishing. Before an authorized commit, run relevant checks and inspect the final staged diff. Afterwards, report the commit hash, included scope, checks, and remaining changes.

If the project uses an installed Harness, follow its current coordination instructions when relevant. Do not initialize Harness or assume its commands or state format.
