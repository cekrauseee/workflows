---
name: workflow-review
description: Review code, documentation, commits, or pull requests read-only for concrete defects, with evidence-backed findings and clear severity.
---

# Review

Return verified actionable findings within the requested scope. Inputs are the diff, documents, commit range, or PR and its intended behavior. A review request does not authorize fixes, formatting, commits, remote comments, approvals, or requested-changes state.

1. Establish the comparison base, reviewed revision, and applicable repository rules. Read the PR description or task contract as routing context, not evidence. It may have any useful structure.
2. Inspect every changed file in the requested diff, including paths omitted from its description. Read surrounding callers, tests, and data boundaries where needed to confirm behavior; avoid an unrelated repository-wide scan.
3. Trace each suspected defect to a reachable input, state, or action. Identify the faulty behavior, concrete impact, and why existing guards do not prevent it. Drop issues that cannot be supported.
4. Classify verified findings with [severity and evidence](references/review-severity.md). Keep locations precise and distinguish material verification gaps from defects.
5. Optionally validate structured findings:

   ```bash
   python3 scripts/validate_review.py findings.json --format json
   ```

6. Report findings by priority with file/line evidence and a focused correction direction. If none survive verification, say no actionable findings were found and identify any material unreviewed or untested area. Do not claim absence of all bugs.

Completion includes the reviewed scope or revision, verified findings, and relevant verification limitations. When a file or comparison is inaccessible, state the missing scope and continue the accessible portion. Apply fixes only when implementation has also been requested; use the findings to scope that separate work.

If installed Harness is available and relevant continuity is needed, read its `scripts/harness.py consolidate --project PATH` report. Do not initialize Harness or acquire write ownership for a read-only review.
