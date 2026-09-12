---
name: workflow-review
description: Review proposed changes for concrete defects, or assess code and documentation against explicitly requested review criteria.
---

# Review

Establish the requested scope and criteria. For a change review, identify the revision and comparison base, inspect all changed files in scope, and follow dependencies needed to assess behavior. Reuse current evidence; a focused request does not require reviewing unrelated changes.

For correctness findings, identify a reachable trigger, concrete impact and precise file and line evidence. Use the host's severity scheme when required; otherwise P0 means catastrophic, P1 urgent, P2 ordinary correctness or reliability, and P3 localized low risk. Separate defects from recommendations in a requested design, structure or documentation assessment.

Report actionable findings with a correction direction. If none are found, say so without implying that unexamined behavior is correct. Include material verification gaps.

Review is read-only unless the request also includes implementation. It does not authorize commits, remote comments, approvals or requested-changes state.
