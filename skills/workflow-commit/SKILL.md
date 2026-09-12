---
name: workflow-commit
description: Draft commit messages, prepare staging, or create requested commits from the relevant changes.
---

# Commit

Match the work to the request: wording, a staging plan, or commit creation. Reuse current diffs and conventions; inspect repository status and affected changes when needed to establish scope and ownership. Read recent commit style only when the convention is unknown.

Group files or hunks by cohesive intent, preserving unrelated work and staging. Tests and documentation belong with the behavior they support. Prefer English Conventional Commits unless user or project choices differ; branch prefixes do not determine commit types.

A message or plan request is read-only. A commit request includes necessary staging, but not amending, bypassing hooks, pushing or publication. Before committing, verify the staged scope and use sufficient checks for the changes, reusing current results. Report the resulting hash, included scope and relevant remaining work.
