# Workflows

The agent owns investigation, decisions, execution and verification. Tools provide evidence and perform operations; their success does not replace the agent’s assessment of the result.

Six portable, instruction-only engineering skills for worktrees, commits, pull requests, reviews, developer documentation, and standalone HTML artifacts. Each skill can be installed independently and uses the host's existing file, Git, and GitHub tools.

Workflows gives an agent a focused procedure and concrete completion evidence. It does not initialize project continuity, run lifecycle hooks, or require Harness. Existing host conventions, project structure, and explicit user choices take precedence over its writing and layout defaults.

| Skill | Result |
| --- | --- |
| [workflow-worktree](skills/workflow-worktree/SKILL.md) | A validated worktree plan, checkout, or retirement |
| [workflow-commit](skills/workflow-commit/SKILL.md) | Cohesive staging groups, commit messages, or requested commits |
| [workflow-pr](skills/workflow-pr/SKILL.md) | A truthful PR draft or requested publication |
| [workflow-review](skills/workflow-review/SKILL.md) | Read-only findings with evidence and severity |
| [workflow-docs](skills/workflow-docs/SKILL.md) | Created, maintained, or audited developer documentation |
| [workflow-artifact](skills/workflow-artifact/SKILL.md) | A self-contained HTML explanation or report |

## Install

Install from the public repository:

```bash
npx skills add cekrauseee/workflows --list
npx skills add cekrauseee/workflows --skill '*' --global -a codex -a claude-code -y
```

Select the skills and agent you need. For agent-specific plugin loading, independent directory copies, and verification, see [installation](docs/install.md). Replace `cekrauseee/workflows` with `.` to test a local checkout.

## Use

Ask for the intended outcome, or invoke a skill explicitly:

```text
Use $workflow-pr to draft a PR description for the current branch.
Use $workflow-review to review this diff without changing files.
Use $workflow-docs to update the setup guide after this change.
```

English and Conventional Commits are preferences. Git-valid host prefixes such as `codex/` work, PR types need not match branch types, and existing PR templates and documentation layouts are preserved. A review remains read-only unless implementation is also requested. HTML is produced only when useful within the requested work.

Read [technical contracts](docs/technical.md) and [installation](docs/install.md). [Publication preparation](docs/publication.md) contains repository metadata and release checks; nothing here publishes automatically.

MIT licensed, copyright 2026 Henrique Krause. See [LICENSE](LICENSE).
