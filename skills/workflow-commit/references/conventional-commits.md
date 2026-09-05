# Commit messages

Prefer `<type>(<optional-scope>)<optional-!>: <description>`, with a blank line before any body or footers. Use `!` or a `BREAKING CHANGE:` footer for an incompatible change.

| Type | Result |
| --- | --- |
| `feat` | New capability |
| `fix` | Bug fix |
| `docs` | Documentation-only change |
| `refactor` | Internal restructuring without a behavior change |
| `perf` | Performance improvement |
| `test` | Test-only change |
| `build` | Dependencies, packaging, or toolchain |
| `ci` | Continuous integration |
| `style` | Formatting-only change |
| `chore` | Other maintenance |
| `revert` | Revert an earlier change |

These types are defaults, not the complete set of valid Conventional Commit types. Use stable scopes meaningful in the repository. A feature plus tests is still `feat`; a dependency update usually uses `build`. Individual commits and the encompassing PR may truthfully have different types. Git branch syntax is independent of these semantics.

Prefer a concise English imperative description, lowercase type, no terminal period, and a header near 72 characters or less. Preserve product names, non-ASCII names, and an explicitly chosen language or style. Length, case, period, and unfamiliar types produce advisory warnings. `--strict-style` makes these warnings errors only when that policy is deliberately desired.

`validate_conventional.py` accepts `--message TEXT` or `--message-file FILE`, optional `--branch NAME`, and `--format text|json`. Exit 0 means no structural errors, 1 means validation failed, and 2 means an input or Git executable could not be read. JSON reports `ok`, `errors`, and `warnings`. Git checks branch syntax but the script never reads or mutates a repository.
