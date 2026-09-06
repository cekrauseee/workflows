# Workflows contributor guidance

Workflows contains independently installable, instruction-only engineering skills. It does not own project continuity, hooks, agent configuration, or executable workflow tooling.

- Keep each published skill self-contained within its own directory.
- Treat writing and layout preferences as advisory unless the user/project requires them.
- Do not couple host branch prefixes, commit types, or PR types.
- Keep review-only requests read-only and optional Harness integration optional.
- Write repository documentation and commit/PR content in concise English; use Conventional Commits unless an explicit choice says otherwise.

Validate every skill and the plugin manifest with available host validators, inspect both plugin manifests for alignment, and run `npx skills add . --list` before publication. Browser and visual QA are opt-in. Do not commit, push, publish, or alter user installations without the relevant request.
