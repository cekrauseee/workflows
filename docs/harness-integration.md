# Optional Harness integration

Workflows does not depend on Harness, import its runtime, initialize projects, or write continuity files. For a project already managed by an installed Harness, the reporting interface is `python3 <installed-harness>/scripts/harness.py consolidate --project PATH [--data JSON]`. Resolve the actual installed path and use that version's documented options.

The report gives continuity and ownership context. It does not substitute for inspecting actual Git files, diffs, revisions, and untracked content. Ordinary reviews may read the report without claiming write ownership. Commit/PR preparation that asserts stable workspace completeness additionally acquires an exclusive whole-workspace claim through Harness `task.start` with `resources: ["."]`, checks unresolved contributions, and checkpoints its own delivery. An active writer or failed claim prevents an unqualified completeness claim; scoped read-only preparation remains possible.

The exact commands and failure behavior are bundled in the [commit integration reference](../skills/workflow-commit/references/harness-integration.md). An identical copy ships inside the PR skill so either skill can be installed alone. The package tests keep both copies aligned. Follow those commands only when installed Harness supports them; never create guessed state files as a fallback.

Release the consolidation session before waiting for user approval, and obtain a new claim plus fresh evidence for later authorized mutation. Checkpointing this session does not mark other contributions complete or imply a commit, push, or publication occurred. Report missing coordination or checkpoint failures when they leave a material gap.
