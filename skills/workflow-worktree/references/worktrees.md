# Worktree details

## Resolver contract

`resolve_branch.py` is read-only. It does not create branches or select storage. Give either `--branch NAME`, or `--slug TEXT` with optional `--prefix PREFIX`. `--type TYPE` is a convenience prefix when no explicit prefix is supplied; it does not constrain future commit or PR types.

An explicit `--base` resolves through Git to a commit, so tags, commit IDs, and expressions such as `HEAD~1` work. Without one, the resolver tries the locally recorded `origin/HEAD`, current branch, then HEAD. It does not fetch and cannot know whether a remote ref is stale. Check that its selected base matches the requested delivery target, especially when starting from an existing feature branch.

The JSON result includes `branch`, `base`, `base_commit`, `branch_exists`, `ref_conflicts`, and `checkouts`. Exit 0 means resolution succeeded. Exit 2 with JSON errors on stderr means invalid input, unresolved base, inaccessible Git, or a collision when availability was required. Hierarchical ref collisions such as existing `codex/task` versus proposed `codex/task/fix` also count.

## Creation and adoption

Use host-native operations when they preserve the planned branch and base. Otherwise Git's `worktree add -b BRANCH PATH BASE_COMMIT` creates from the verified commit. Resolve paths before acting; never use Harness state as a storage root. Prefer an ordinary host/user-selected project directory when no host allocator exists.

A detached worktree may be valid when explicitly intended. For branch adoption, compare repository identity, registered checkout path, branch, merge base, status, and ongoing work. A branch already checked out elsewhere should route to that existing checkout or a new task branch; do not bypass Git's protection with `--force`.

## Retirement

Inspect `git status --short`, `git status --short --ignored`, the registration, and the branch's committed work. Explain where unmerged commits remain before removal when relevant. Use ordinary removal without force after authorization and preserve the branch unless deletion is also authorized. Never prune an unavailable removable drive's registration merely because its path is temporarily absent.
