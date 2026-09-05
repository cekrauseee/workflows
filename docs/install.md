# Installation

Install from the local source directory. The repository includes Codex and Claude plugin manifests plus ordinary skill directories; use one installation route per agent to avoid duplicate discovery.

## Skills CLI

From the Workflows source checkout, list the package before selecting skills:

```bash
npx skills add . --list
npx skills add . --skill workflow-review --agent codex
npx skills add . --skill workflow-docs --agent claude-code
```

The first command is discovery only. Add `--global` only when you want a user-wide installation; without it, follow the CLI's project-local destination. The CLI can install several selected skills together. It may use network access to obtain its own current package. Repository scripts themselves need only Python 3.10+ and Git where indicated.

## Independent copy

Copy an entire `skills/workflow-NAME/` directory, including `scripts/`, `references/`, and `agents/`, into the active host's skill directory. For example, a Codex user's skill directory is normally `~/.codex/skills/`, and Claude Code supports `.claude/skills/` in a project. Respect any configured host-specific location instead of hard-coding one into workflows.

Do not copy just `SKILL.md`, and do not merge new files over an unrelated same-named skill. Choose an absent destination or compare the existing installed copy first. Each skill works when copied alone: the PR helper's message validator is bundled beside it, and docs initialization and audit helpers are in the same skill.

## Plugin loading

Codex discovers `.codex-plugin/plugin.json`; Claude Code discovers `.claude-plugin/plugin.json`. Both describe the same six skills. This checkout contains no marketplace registration or hooks. Load it through the host's supported local plugin flow. For a temporary Claude Code session, `claude --plugin-dir /absolute/path/to/workflows` loads this local plugin.

A Codex marketplace entry can be created later through the host's plugin management flow when desired. The package does not mutate personal marketplace configuration or assume a published GitHub repository. Avoid running both a plugin installation and loose copies of its skills in the same host.

## Verify and update

After installation, start a fresh agent session when needed for discovery and confirm the six selected names and descriptions. To check an independent copy, run its helper with `--help`; then perform a relevant read-only validation, such as checking a commit message or listing the worktree plan.

Update the installed package through the same route that installed it. Existing installations of the old Harness workflow names are separate and may remain discoverable until removed; see [migration](migration.md). No updater here deletes host state or manages installed plugin caches.
