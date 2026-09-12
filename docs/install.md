# Installation

Use one installation route per host to avoid duplicate discovery. Each `skills/<name>/` directory contains its instructions and host metadata and works independently.

## Skills CLI

```bash
npx skills add cekrauseee/workflows --list
npx skills add cekrauseee/workflows --skill workflow-review --agent codex
npx skills add cekrauseee/workflows --skill workflow-docs --agent claude-code
```

Use `.` instead of the repository name for a local checkout. Add `--global` for user-wide installation; otherwise use the CLI's project-local destination. The CLI may obtain its own package through the network.

## Independent copy or plugin

Copy the complete selected skill directory into the host's configured skill location. Compare an existing same-named copy before replacing it; do not merge over unrelated content.

The Codex and Claude manifests expose the same inventory through each host's plugin loader. For a temporary Claude Code session, `claude --plugin-dir /absolute/path/to/workflows` loads the local package. Use the host's supported plugin flow for Codex. This repository does not configure personal marketplaces or hooks.

## Verify and update

Confirm the selected names are discovered, refreshing the session when needed. Check an affected workflow when its behavior changed. Update through the route used for installation; when switching routes, remove the previous installation through its owning mechanism so only one copy is discovered. [Contributor guidance](../AGENTS.md) defines package verification.
