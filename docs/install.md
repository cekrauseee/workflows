# Installation

Install from `cekrauseee/workflows` or a local source directory. The repository includes Codex and Claude plugin manifests plus ordinary skill directories; use one installation route per agent to avoid duplicate discovery.

## Skills CLI

List the public package before selecting skills; use `.` in place of `cekrauseee/workflows` for a local checkout:

```bash
npx skills add cekrauseee/workflows --list
npx skills add cekrauseee/workflows --skill workflow-review --agent codex
npx skills add cekrauseee/workflows --skill workflow-docs --agent claude-code
```

The first command is discovery only. Add `--global` only when you want a user-wide installation; without it, follow the CLI's project-local destination. The CLI can install several selected skills together. It may use network access to obtain its own current package.

## Independent copy

Copy an entire `skills/workflow-NAME/` directory into the active host's skill directory. For example, a Codex user's skill directory is normally `~/.codex/skills/`, and Claude Code supports `.claude/skills/` in a project. Respect any configured host-specific location instead of hard-coding one into Workflows.

Do not copy just `SKILL.md`, and do not merge new files over an unrelated same-named skill. Choose an absent destination or compare the existing installed copy first. Each skill works when copied alone.

## Plugin loading

Codex discovers `.codex-plugin/plugin.json`; Claude Code discovers `.claude-plugin/plugin.json`. Both describe the same seven skills. This checkout contains no marketplace registration or hooks. Load it through the host's supported local plugin flow. For a temporary Claude Code session, `claude --plugin-dir /absolute/path/to/workflows` loads this local plugin.

A Codex marketplace entry can be created later through the host's plugin management flow when desired. The package does not mutate personal marketplace configuration. Avoid running both a plugin installation and loose copies of its skills in the same host.

## Verify and update

After installation, start a fresh agent session when needed for discovery and confirm the selected names and descriptions. Then invoke a selected skill on an appropriate test request and inspect its behavior.

Update the installed package through the same route that installed it. Remove a separately installed copy through that route before switching installation methods, so the host discovers only one copy of each skill. No updater here deletes host state or manages installed plugin caches.
