# Workflows contributor guidance

Workflows contains independently installable engineering skills. It does not own project continuity, hooks, or agent configuration.

- Preserve each skill's portable scripts and references within its own directory.
- Use Python 3.10+ standard library only for bundled helpers.
- Keep new-file writes atomic and idempotent; preserve existing content by default.
- Treat writing and layout preferences as advisory unless the user/project requires them.
- Do not couple host branch prefixes, commit types, or PR types.
- Keep review-only requests read-only and optional Harness integration optional.
- Write repository documentation and commit/PR content in concise English; use Conventional Commits unless an explicit choice says otherwise.

Run `python3 -m unittest discover -s tests -v`, validate every skill and the plugin manifest with available host validators, and run `npx skills add . --list` before publication. Git/installation tests must use isolated temporary directories. Browser and visual QA are opt-in. Do not commit, push, publish, or alter user installations without the relevant request.
