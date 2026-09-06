---
name: workflow-review
description: Review code, documentation, commits, or pull requests read-only for concrete defects, with evidence-backed findings and clear severity.
---

# Review

Establish the comparison base, reviewed revision, intended behavior, and applicable repository rules. Inspect every changed file in scope, then read callers, tests, and data boundaries needed to verify behavior.

Report only defects with a reachable trigger, concrete impact, and precise file and line evidence. Use P0 for catastrophic blockers, P1 for urgent major defects, P2 for ordinary correctness or reliability defects, and P3 for localized low-risk defects. Omit style preferences and unsupported suspicions.

List findings by severity with a concise correction direction. If there are none, say no actionable findings were found and identify material unreviewed or untested areas. Do not claim that no bugs exist.

A review request is read-only. It does not authorize fixes, commits, remote comments, approvals, or requested-changes state. If the project uses an installed Harness, follow its current read-only coordination instructions when relevant; do not initialize it or acquire write ownership.
