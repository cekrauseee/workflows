# Publication preparation

The public source repository is https://github.com/cekrauseee/workflows. It distributes ordinary skills and Codex/Claude plugin manifests. A merge to main does not create a tagged release or a marketplace registration.

GitHub repository metadata:

| Field | Value |
| --- | --- |
| Name | `workflows` |
| Description | Portable engineering workflows for agent orchestration, Git, reviews, documentation, and HTML artifacts. |
| Topics | `agent-skills`, `workflows`, `git`, `code-review`, `documentation`, `codex`, `claude-code` |
| License | MIT |
| Author | Henrique Krause |
| Initial version | `0.1.0` |

Before publication, validate all skills and the Codex manifest, inspect both plugin manifests for alignment, run `npx skills add . --list`, and test selected-skill installation into isolated Codex and Claude Code destinations. Inspect status and the resulting distribution so no caches, secrets, local state, or generated test workspaces are included.

Repository creation, commits, pushes, releases, marketplace registration, and edits to live metadata are separate external or version-control actions. The local package and this metadata draft do not perform or imply them. Update verified URLs in README and manifests together; do not add an unverified catalog or site URL.
