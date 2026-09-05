# Publication preparation

This checkout is a local Workflows package. A remote repository and marketplace publication have not been established here. Do not add homepage/repository URLs until their destinations exist and are verified.

Suggested GitHub metadata for an explicitly authorized future repository:

| Field | Draft value |
| --- | --- |
| Name | `workflows` |
| Description | Portable engineering workflows for Git, reviews, documentation, and HTML artifacts. |
| Topics | `agent-skills`, `workflows`, `git`, `code-review`, `documentation`, `codex`, `claude-code` |
| License | MIT |
| Author | Henrique Krause |
| Initial version | `0.1.0` |

Before publication, run the unit tests, validate all skills and the Codex manifest, inspect both plugin manifests for alignment, run `npx skills add . --list`, and test selected-skill installation into isolated Codex and Claude Code destinations. Inspect status and the resulting distribution so no caches, secrets, local state, or generated test workspaces are included.

Repository creation, commits, pushes, releases, marketplace registration, and edits to live metadata are separate external or version-control actions. The local package and this metadata draft do not perform or imply them. Once a remote exists, update the verified URLs in README and manifests together instead of publishing a guessed destination.
