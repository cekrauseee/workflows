---
name: workflow-worktree
description: Create, adopt or retire Git worktrees, or prepare a requested worktree plan.
---

# Worktree

Use the checks needed for the requested operation and reuse current host evidence. Preserve an explicit branch or path; otherwise follow host and repository conventions. A plan is read-only.

For creation, establish the base and destination and check branch or checkout collisions with native Git or host support. For adoption, also inspect existing changes and divergence. Confirm the resulting repository, registered path, branch and starting commit from reliable operation results or a targeted check. Never silently adopt unrelated work or force past a collision.

For authorized retirement, inspect changes, untracked or ignored user files and commits that could be lost. Disposable build output does not itself prevent removal. Preserve meaningful work and do not force its deletion. Worktree removal does not authorize branch deletion.

Use native tools rather than a separate storage system. Report the resulting path and branch, or the remaining obstacle.
