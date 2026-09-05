# Migration from Harness workflows

Workflows extracts the on-demand engineering procedures from Harness. Harness remains responsible for project continuity, relevant recall, contribution ownership, and handoffs; Workflows supplies the procedures for a specific deliverable. Installing Workflows does not create or migrate continuity state.

| Former skill | Replacement |
| --- | --- |
| `harness-worktree` | `workflow-worktree` |
| `harness-commit` | `workflow-commit` |
| `harness-pr` | `workflow-pr` |
| `harness-review` | `workflow-review` |
| `harness-docs-init` | `workflow-docs` → initialization reference |
| `harness-docs-maintain` | `workflow-docs` → maintenance reference |
| `harness-docs-audit` | `workflow-docs` → audit reference |
| `harness-artifact` | `workflow-artifact` |

Install the replacements through the existing host's installation route. Compare and remove only the old workflow copies that the user intends to replace; do not remove Harness continuity skills or unrelated local customizations. Update personal prompts or repository instructions that explicitly invoke an old skill. Existing task branches, commits, PRs, docs, artifacts, and Harness state need no rename or migration to keep working.

The extracted skills intentionally relax former preferences that impeded legitimate host/user choices:

- Git-valid host prefixes work. Branch naming does not force a PR or commit type.
- English, common Conventional Commit types, and concise headers remain defaults; valid custom types and language/style choices are not rejected as invalid ASCII.
- A PR may use its repository's template or a compact description. Six headings and arbitrary length/item limits are not required.
- Existing documentation structures are preserved. The docs helper creates only requested missing paths, and audits do not require a baseline tree.
- HTML destinations and visual style follow the deliverable. No Harness scratch directory, neutral branding restriction, mandatory catalog, or automatic visualization is imposed.
- A review request remains read-only. Its findings do not authorize fixes or remote comments.

Script interfaces changed: worktree resolution accepts `--prefix` or an exact `--branch`; commit style findings are warnings; PR rendering supports a preserved `--body-file`; docs initialization uses repeated `--file`; artifact creation takes an explicit output HTML path. Use each helper's `--help` before replacing an old scripted call. Validation is still required for structural errors; these changes do not weaken evidence requirements or imply authorization for external actions.

When Harness is installed for the project, use the [optional integration](harness-integration.md) to coordinate final commit/PR preparation. Independent workflows remain useful without it.
