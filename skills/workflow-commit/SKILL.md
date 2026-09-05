---
name: workflow-commit
description: Prepare cohesive staging groups and Conventional Commit messages from actual changes, and create commits when requested.
---

# Commit

Produce a commit plan or the requested commits from verified repository changes. Inputs are the intended scope, current checkout, and any message or staging preferences. A message-only request is read-only; a commit request includes the staging needed for that commit, but does not imply pushing, amending, or bypassing hooks.

1. Read applicable repository instructions and inspect status, staged and unstaged diffs, relevant untracked file contents, and recent commit style. Trace each included file to the intended change. Do not interpret “all changes” as permission to absorb unrelated or still-active work.
2. If installed Harness tracks this project, read [optional consolidation](references/harness-integration.md) before asserting workspace completeness or creating commits. Secure a whole-workspace claim when available, inspect unresolved contributions, and compare the report with actual Git files. If a writer remains active, report the overlap and limit work to a clearly scoped read-only plan.
3. Group changes by cohesive intent. Accompanying tests and docs belong with the feature or fix they explain. Preserve unrelated staging; use explicit paths or hunks when needed. Ask only about ownership or scope that cannot be established from the current evidence.
4. Prefer English Conventional Commits, honoring explicit project or user choices. See [message conventions](references/conventional-commits.md) for classification. Branch prefixes and branch types do not constrain the message.

   ```bash
   python3 scripts/validate_conventional.py --message 'fix(cache): expire stale entries' --branch codex/cache-expiry --format json
   ```

   Structural errors fail validation; editorial warnings are advisory. The helper cannot prove truthfulness, English, or imperative wording.
5. When authorized to commit, run the relevant required checks, re-read the final staged diff, and create only the agreed grouping. Recheck status immediately afterwards and record the commit hash, included scope, checks, and remaining changes. If hooks fail, report the failure and preserve the staged work while addressing authorized fixes.

Completion is a concrete grouping and message for preparation, or verified commit hashes with remaining changes for execution. State any unresolved contribution or unperformed check; never claim all work was included from the chat history alone.
