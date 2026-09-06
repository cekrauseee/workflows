# Technical contracts

Workflows is an instruction-only skill package. Each directory under `skills/` is an independent distribution unit: `SKILL.md` defines the workflow and `agents/openai.yaml` supplies aligned host metadata. The package has no runtime, bundled executable helpers, hooks, or dependency on another skill.

The skills rely on the host's existing file, Git, GitHub, validation, and browser tools. Those tools provide evidence; the agent remains responsible for scope, judgment, verification and truthful reporting. Successful tool execution does not establish task completion. User choices and repository rules override package preferences.

Review requests remain read-only unless fixes or publication are also requested. Commit creation, PR publication, worktree creation or retirement, and other mutations require the corresponding user request. HTML artifacts use an explicit destination and remain self-contained when that is the requested format.

Harness is optional. When a project already uses an installed Harness, follow that installation's current coordination instructions. Do not initialize it, guess commands, or duplicate its state model in these skills.

## Verification

From the repository root:

```bash
npx skills add . --list
```

Use the host's bundled skill validator on every skill and plugin validator on this repository when available. These validators belong to the host; this package does not vendor them or assume their install paths. Before publication, also inspect both manifests and perform selected-skill installation tests in isolated destinations.
