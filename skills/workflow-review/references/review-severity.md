# Severity and evidence

| Priority | Meaning |
| --- | --- |
| `P0` | Certain catastrophic data loss, broad compromise, or equivalent operation blocker |
| `P1` | Major correctness, security, or regression risk needing urgent attention |
| `P2` | Relevant correctness, reliability, or maintainability defect worth fixing normally |
| `P3` | Localized, low-risk defect with concrete value in fixing |

Choose severity from impact, likelihood, and affected scope. A speculative edge case is not a finding. Explain a reachable trigger, the defective behavior, impact, and why another guard does not prevent it. Do not report stylistic preference or descriptions that merely assert “might break.” Keep separate defects separate.

The optional validator accepts an array or `{ "findings": [...] }`. Each finding has `priority`, `title`, `file`, positive integer `start`, optional `end`, and nonempty `evidence`, `impact`, `direction`. Empty findings are valid. JSON shape, priority, text, and line order are checked; title and range length produce advisory warnings. It cannot verify that a line exists or that the finding is true. Check locations against the actual reviewed revision.

Exit 0 means structurally valid, 1 means invalid fields, 2 means invalid JSON or an unreadable input. The tool reads a file or stdin and writes only its result. It never edits or publishes review content.
