---
name: workflow-worktree
description: Plan, create, adopt, and safely retire isolated Git worktrees using the host or repository's branch and storage conventions.
---

# Worktree

Inspect repository instructions, status, refs, the intended base, and registered worktrees. Preserve an explicit branch or path choice. Otherwise follow host and repository conventions and use a short task name. Validate branch syntax, ref collisions, base resolution, and existing checkouts with native Git before creating or adopting a worktree.

Use host worktree support when available, or Git directly. Before editing, confirm the repository identity, registered path, branch, and starting commit. For adoption, also inspect divergence and existing work. Never force past a collision or silently adopt an unrelated branch.

Before an authorized retirement, inspect staged, unstaged, untracked, ignored, and unmerged work. Do not force removal of a checkout containing work. Worktree removal and branch deletion are separate actions. Report the path, branch, base, and verification performed.

If the project uses an installed Harness, follow its current coordination instructions when relevant. Do not initialize Harness or use Harness state as worktree storage.
