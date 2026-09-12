# Workflows

Seven independently installable skills for engineering tasks. Each provides task-specific decision criteria and completion requirements using the host's existing tools. Workflows has no runtime, bundled scripts or hooks.

| Skill | Use |
| --- | --- |
| [workflow-orchestrate](skills/workflow-orchestrate/SKILL.md) | Coordinate explicitly requested delegation |
| [workflow-worktree](skills/workflow-worktree/SKILL.md) | Create, adopt or retire a Git worktree |
| [workflow-commit](skills/workflow-commit/SKILL.md) | Draft messages, prepare staging or create requested commits |
| [workflow-pr](skills/workflow-pr/SKILL.md) | Draft or revise PR content and perform requested publication |
| [workflow-review](skills/workflow-review/SKILL.md) | Review changes or apply requested assessment criteria |
| [workflow-docs](skills/workflow-docs/SKILL.md) | Create, update or audit developer documentation |
| [workflow-artifact](skills/workflow-artifact/SKILL.md) | Deliver a requested standalone HTML explanation or report |

## Install and use

```bash
npx skills add cekrauseee/workflows --skill '*' --global -a codex -a claude-code -y
```

Select only the skills and host you need. See [installation](docs/install.md) for independent copies, plugin loading and updates. Replace the repository name with `.` to use a local checkout.

Ask for the desired outcome or invoke a skill directly, such as `Use $workflow-pr to draft a description for this branch.` Skills reuse current context and verification. User and project instructions govern scope, language and execution permissions.

Harness is optional. A project's existing host instruction controls when its knowledge or coordination is needed; invoking Workflows does not start a Harness lifecycle. Workflows contains no Harness commands or state model.

The Codex and Claude manifests describe the same skill inventory and package version. Contributor and verification requirements are in [AGENTS.md](AGENTS.md). Publication and user installation updates are separate requested actions.

[MIT license](LICENSE), Henrique Krause.
