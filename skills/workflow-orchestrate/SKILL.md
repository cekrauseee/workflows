---
name: workflow-orchestrate
description: Coordinate explicitly requested subagent work as a dedicated orchestrator, with model selection, minimal context, and delegated verification. Use when the user requests orchestration or delegation, or to continue an authorized agent team.
---

# Orchestrate

Use orchestration when the user requests it, including in natural language, or when continuing an already authorized team. Otherwise execute directly; task size or available concurrency alone does not activate delegation.

## Keep the coordinator role

During requested orchestration, the coordinator owns the objective, acceptance criteria, decomposition, assignments, cross-scope decisions, and final acceptance. Delegate operational discovery, implementation, integration, tests, review, and fixes. Read governing instructions and the context needed to make decisions, but do not conduct a parallel implementation or routine code investigation. Remain in this role through delivery unless the user explicitly asks for shared execution or changes the arrangement.

Responsibility for delivery does not require personally performing or repeating the workers' work. Assign small tasks whole to one worker rather than taking them over or manufacturing parallel work. Available concurrency is a ceiling, not a target. Waiting for a meaningful result is appropriate when no coordination decision is pending.

## Select capability and context

Choose the model and reasoning effort explicitly for each assignment when the host supports it, honoring user choices and available models. Prefer an economical model with low effort for narrow discovery, medium effort for scoped implementation, and higher effort for difficult logic or ambiguity. Reserve premium models for a concrete need; do not inherit the coordinator's expensive model merely by omission. These are task-based defaults, not a requirement to try an unsuitable model first. Keep model identifiers and personal defaults in host configuration rather than making this skill depend on one provider.

Prefer a fresh context with a self-contained assignment. Include the objective, relevant paths and evidence, applicable restrictions, write ownership, completion criteria, and expected output. Include essential authorization and tool boundaries even when the host also propagates them. Pass references to necessary material instead of copying unrelated history. Use limited history only when earlier decisions materially affect the assignment; use full history only when that benefit justifies its cost and inheritance behavior.

Check the available spawn schema: some hosts couple full-history forks to the parent's model and effort and reject overrides. When supported, use `fork_turns: "none"` with explicit `model` and `reasoning_effort` for an independently configured worker. If the host cannot select the requested capability, disclose the limitation and adapt within the authorized scope rather than silently substituting a premium agent.

## Assign complete units

Give each worker a coherent result, including its relevant checks, and keep write scopes non-overlapping. Avoid splitting a short sequence across a scout, implementer, and tester when one worker can complete it. Keep discovery read-only unless implementation is assigned.

Workers execute directly by default. Tell leaf agents: "Complete this assignment directly. Do not spawn other agents; your parent's delegation instructions apply only to your parent." Allow further delegation only when explicitly assigned and justified within the shared concurrency budget.

Assign integration and its relevant checks to a worker when work spans multiple assignments. The coordinator resolves interface and scope decisions; the integration worker performs the changes and checks. Do not duplicate assigned investigation, implementation, or verification.

## Communicate and finish

Request a concise result: outcome, changed files or precise evidence, checks performed, and unresolved issues. Keep necessary details accessible through file references; do not request execution diaries or raw logs. Agents may send relevant findings directly to a dependent teammate; avoid broadcasts and repeated coordinator relays. Report changes that affect scope or ownership to the coordinator before acting on them.

Reuse an existing agent for follow-up on the same scope when its context remains useful. Wait for meaningful results rather than repeatedly polling unchanged state. Keep user updates focused on progress, decisions, and blockers.

Escalate when evidence shows missing capability, unresolved ambiguity, or a failed approach. Clarify or reassign the work rather than silently taking over execution. If delegation is unavailable, report the limitation and retain the coordinator role until the user changes it. Carry forward the diagnosis and useful results; do not restart blindly or retry the same approach indefinitely. Resolve missing requirements with the user when necessary rather than treating every blocker as a model problem.

## Accept results without repeating execution

Define observable acceptance criteria and required verification in the assignment. Workers return the outcome, concise evidence against those criteria, checks actually performed, and remaining limitations. A bare completion claim is insufficient; request the missing evidence from the responsible worker.

Assess whether the result meets the objective and whether the evidence is coherent and sufficient. Do not routinely read full diffs, inspect tool-call histories, request raw logs, or rerun checks to audit a worker. Delegate a targeted investigation when a concrete gap, contradiction, failure, or unresolved material risk could change acceptance.

When the user requests code review or applicable instructions require it, assign a separate read-only reviewer. Decide which findings require action and return them to an implementation worker, including small fixes. Delegate verification of affected behavior after fixes; do not perform a second review of the reviewer's work. Keep required review distinct from routine worker verification rather than adding a reviewer to every assignment.

Stop when acceptance criteria and required checks are satisfied. Broaden verification only for new failures or unresolved material uncertainty. Assess efficiency by total work through accepted delivery, including coordination and rework, rather than agent count or latency alone. Report measured usage only when available; do not invent savings.

Delegation grants no additional permission for commits, publication, external messages, or other actions. If an installed Harness is already in use, follow its scoped recall and writer ownership procedures; do not initialize it or duplicate its state in messages. Keep transient coordination in agent messages and genuine continuation needs in current handoffs.
