---
name: workflow-worktree
description: Plan, create, adopt, and safely retire isolated Git worktrees using the host or repository's branch and storage conventions.
---

# Worktree

Produce a verified isolated checkout for the requested task, or a concrete plan when creation is outside the request. Inputs are the repository, task, intended base, and any branch or storage preference. Neither Harness nor a fixed directory layout is required.

## Plan and create

1. Inspect repository instructions, current status, branch refs, and `git worktree list --porcelain`. Identify the intended base; do not infer it from a task's commit type.
2. Preserve an explicitly chosen branch. Otherwise use the active host or repository prefix, such as `codex/`, with a short English task slug. With no convention, a plain task slug or `type/slug` is reasonable. Conventional Commits does not prescribe branch names.
3. Optionally resolve and validate the plan without writing state:

   ```bash
   python3 scripts/resolve_branch.py --project PATH --prefix codex --slug 'repair cache expiry' --base main --require-available
   ```

   Pass `--branch existing/name` for an exact branch name. The result includes the resolved base commit, branch collisions, and existing checkouts. Omit `--require-available` only when inspecting or intentionally adopting an existing branch. See [worktree details](references/worktrees.md) for base selection and lifecycle checks.
4. Use host-native worktree tools when available. Otherwise create with Git at a path selected by the user, host, or repository convention. Worktree creation can be part of authorized implementation; planning alone does not authorize creating or retiring one.
5. Before editing, confirm the registered path, repository identity, current branch, and starting commit. For a new checkout, compare HEAD to the planned `base_commit`. For adoption, inspect divergence and current work instead of demanding HEAD still equal the original base.

## Complete or retire

Keep task edits and verification in the chosen checkout. Report the branch, path, base, and checks performed. A collision or invalid base is a planning error: report it and choose another name only within the user's intent. Never silently adopt an unrelated branch.

Before authorized retirement, inspect staged, unstaged, untracked, and ignored files; Git's ordinary status hides ignored files that removal could erase. Do not force removal of a checkout containing work. Prefer host-native removal so host bookkeeping stays consistent. Branch deletion is a separate action. Confirm only the intended checkout was removed.

If installed Harness is available and relevant continuity is needed, read its `scripts/harness.py consolidate --project PATH` report. Do not initialize Harness or require it to use this skill.
