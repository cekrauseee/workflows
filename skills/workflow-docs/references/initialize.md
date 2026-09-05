# Initialize documentation

Inspect the README, documentation directories, site configuration, package commands, and relevant source before creating files. Existing `doc/`, `documentation/`, README-based, or generated-site layouts are valid. Do not add a parallel `docs/` hierarchy just to match a template.

For a small undocumented project, README alone may suffice. When topics warrant separate pages, useful roles include an entry point, architecture, development, and focused subsystem guides. A routing index helps only when there are several documents to route. Create an artifact catalog only when artifacts exist.

The optional helper accepts selected paths:

```bash
python3 scripts/init_docs.py PATH --file README.md --file documentation/development.md
```

With no `--file`, it proposes only README.md. Use `--dry-run` for a JSON plan. `--title TEXT` sets the project name for a new README. It creates minimal editorial scaffolds that still require source-grounded content; created files are not verified finished documentation. Existing files are listed as preserved without modification. Paths must remain inside the project and use `.md`; escaping paths or symlink paths fail before writes. Each new file appears atomically, and repeated calls do not replace content. Exit 0 is success; exit 2 is an invalid path or filesystem error.

After creating the chosen files, fill the scaffolds from verified evidence, link them through the existing entry point, and check the affected links. Do not overwrite an existing document whose location or contents overlap a proposed page.
