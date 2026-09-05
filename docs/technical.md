# Technical contracts

Workflows is a skill package, not a service. Each published directory under `skills/` is an independent distribution unit. `SKILL.md` defines intent, inputs, behavior, and completion evidence; mode-specific details live in linked references; `agents/openai.yaml` supplies aligned host UI metadata. No script imports another skill, depends on this repository's root, or initializes Harness.

Bundled scripts use Python 3.10+ standard library only. Git helpers require Git on PATH. They do not fetch, stage, commit, publish, or alter branches themselves. Documentation and artifact creators publish complete files atomically and preserve existing content by default. Atomicity is per file, not a transaction across several new documents. Editorial scaffolds still need verified content before delivery.

| Skill | Helpers | Contract |
| --- | --- | --- |
| Worktree | `resolve_branch.py` | Resolve Git branch/base, refs, and checkout collisions without writes |
| Commit | `validate_conventional.py` | Structural errors plus advisory style warnings |
| PR | `render_pr.py`, `validate_conventional.py` | Optional sections or exact existing body; no publication |
| Review | `validate_review.py` | Validate finding structure, not source truth |
| Docs | `init_docs.py`, `check_docs.py` | Selected missing files; local Markdown link checks |
| Artifact | `create_artifact.py`, `check_artifacts.py` | Explicit HTML destination; static portability checks |

Normal validation exits 0 on success and 1 on contract violations; unreadable inputs and planning errors use 2. Each helper documents its arguments through `--help` and its linked skill reference. JSON is available for structured results. Scripts never decide whether the user authorized a commit, publication, fix, or removal; the skill and current conversation establish that boundary.

The commit validator and commit/PR Harness integration reference are intentionally copied into both skill directories for independent installation. Their copies are checked for equivalence by package tests; they must be updated together. This is distribution duplication, not an external runtime dependency.

## Verification

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 skills/workflow-docs/scripts/check_docs.py . --path README.md --path docs --path skills --format json
npx skills add . --list
```

Use the host's bundled skill validator on every skill and plugin validator on this repository when available. These validators belong to the host; this package does not vendor them or assume their install paths. Before publication, also perform selected-skill installation tests into isolated destinations for Codex and Claude Code.

Tests exercise isolated Git repositories, arbitrary valid branch prefixes, base resolution, reference collisions, unchanged repository state, template preservation, structured error handling, docs preservation and idempotence, existing custom layouts, local links, explicit HTML paths, embedded assets, dependency detection, and each independently copied skill's helpers. They use temporary workspaces and never touch user configuration or a remote.

Markdown checks do not fetch HTTP links, validate fragment IDs, or fully parse every site renderer extension. HTML checks do not execute JavaScript or prove accessibility, visual quality, or semantic accuracy. Visual/browser QA is not started automatically. Report those limits when they matter to a particular deliverable.
