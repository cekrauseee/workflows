---
name: workflow-orchestrate
description: Coordinate scoped subagent work with explicit model selection, minimal context, and proportionate verification. Use when delegating independent engineering work or managing an existing agent team.
---

# Orchestrate

Delegate only when independent execution, context isolation, or parallel investigation outweighs assignment and integration overhead. Handle small or tightly coupled work directly. Available concurrency is a ceiling, not a target; parallel tool calls do not require separate agents.

## Select capability and context

Choose the model and reasoning effort explicitly for each assignment when the host supports it, honoring user choices and available models. Prefer an economical model with low effort for narrow discovery, medium effort for scoped implementation, and higher effort for difficult logic or ambiguity. Reserve premium models for a concrete need; do not inherit the coordinator's expensive model merely by omission. These are task-based defaults, not a requirement to try an unsuitable model first. Keep model identifiers and personal defaults in host configuration rather than making this skill depend on one provider.

Prefer a fresh context with a self-contained assignment. Include the objective, relevant paths and evidence, applicable restrictions, write ownership, completion criteria, and expected output. Include essential authorization and tool boundaries even when the host also propagates them. Pass references to necessary material instead of copying unrelated history. Use limited history only when earlier decisions materially affect the assignment; use full history only when that benefit justifies its cost and inheritance behavior.

Check the available spawn schema: some hosts couple full-history forks to the parent's model and effort and reject overrides. When supported, use `fork_turns: "none"` with explicit `model` and `reasoning_effort` for an independently configured worker. If the host cannot select the requested capability, disclose the limitation and adapt within the authorized scope rather than silently substituting a premium agent.

## Assign complete units

Give each worker a coherent result, including its relevant checks, and keep write scopes non-overlapping. Avoid splitting a short sequence across a scout, implementer, and tester when one worker can complete it. Keep discovery read-only unless implementation is assigned.

Workers execute directly by default. Tell leaf agents: "Complete this assignment directly. Do not spawn other agents; your parent's delegation instructions apply only to your parent." Allow further delegation only when explicitly assigned and justified within the shared concurrency budget.

The coordinator retains integration and critical decisions while doing useful complementary work. Do not duplicate an assigned investigation or implementation. Review returned evidence and affected boundaries instead of repeating the worker's entire process.

## Communicate and finish

Request a concise result: outcome, changed files or precise evidence, checks performed, and unresolved issues. Keep necessary details accessible through file references; do not request execution diaries or raw logs. Agents may send relevant findings directly to a dependent teammate; avoid broadcasts and repeated coordinator relays. Report changes that affect scope or ownership to the coordinator before acting on them.

Reuse an existing agent for follow-up on the same scope when its context remains useful. Wait for meaningful results rather than repeatedly polling unchanged state. Keep user updates focused on progress, decisions, and blockers.

Escalate when evidence shows missing capability, unresolved ambiguity, or a failed approach. Carry forward the diagnosis and useful results; do not restart blindly or retry the same approach indefinitely. Resolve missing requirements with the user when necessary rather than treating every blocker as a model problem.

Use proportionate verification and any required independent review. After accepted fixes, recheck affected behavior and stop when completion criteria are met; expand checks only for new failures or material uncertainty. Assess efficiency by total work through accepted delivery, including coordination and rework, rather than agent count or latency alone. Report measured usage only when available; do not invent savings.

Delegation grants no additional permission for commits, publication, external messages, or other actions. If an installed Harness is already in use, follow its scoped recall and writer ownership procedures; do not initialize it or duplicate its state in messages. Keep transient coordination in agent messages and genuine continuation needs in current handoffs.
