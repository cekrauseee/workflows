# Pull request writing

Lead with the problem and resulting behavior. A concrete before/after example often provides more context than an inventory of implementation steps. Route reviewers to the few files or boundaries where judgment matters. Report checks actually performed and material limitations. A description guides review; it is not proof that the implementation is correct.

Use a Conventional Commit title by default, such as `fix(cache): expire stale entries`. Classify the principal outcome independently from the branch prefix and supporting commits. English, a concise imperative description, and a roughly 72-character title are writing preferences, not publication gates when the user or project chose another valid form.

## Optional renderer

Use the renderer when a generated body helps; it is not required for existing templates.

```bash
python3 scripts/render_pr.py \
  --branch codex/cache-expiry \
  --title 'fix(cache): expire stale entries' \
  --summary 'Expired entries remained visible until restart. Reads now reject entries past their expiry time.' \
  --verification 'Passed cache regression tests.' \
  --format json
```

Add `--behavior`, `--change target=description`, `--review target=question`, or `--risk` only when useful. Repeat section options as needed. No section count, item count, or body length limit is imposed. Longer output is a writing judgment; the renderer does not silently truncate it.

To preserve a project's existing body, use `--body-file FILE` instead of `--summary`. The file is preserved as supplied; the tool does not force headings into it. It cannot be combined with generated section flags. With `--allow-nonconventional-title`, a nonempty user/project title is preserved with an advisory warning. Normal title validation reports structural errors and advisory style warnings.

Output is Markdown by default or JSON containing `ok`, `title`, `body`, `errors`, and `warnings`. An optional branch is checked only for valid Git syntax. Exit 0 means rendering succeeded, 1 means invalid content, and 2 means input/Git could not be read. The renderer never reads repository diffs or publishes anything; evidence must come from the actual review preparation.
