---
name: workflow-orchestrate
description: Coordinate explicitly requested delegation or continue an authorized agent team.
---

# Orchestrate

Orchestrate only when requested or when continuing an authorized team. The coordinator owns the overall objective, task boundaries, priorities, dependencies and acceptance of delivered outcomes. Workers own technical investigation, implementation decisions, execution, integration, verification and fixes. Do not perform those activities alongside workers or audit their implementation after delivery.

## Assign complete outcomes

Give each worker a coherent outcome with the context needed to understand it: expected behavior, scope, relevant references, confirmed constraints and what to return. Use concrete examples to resolve ambiguity. Pass mandatory technical constraints or existing interfaces when relevant, but leave the implementation approach, code structure, tools and test selection to the worker.

For a worker that needs clearer reasoning boundaries, narrow the problem and clarify the desired behavior. Do not compensate with a technical plan that leaves the worker only edits and tool calls. Let the worker investigate technical unknowns as part of the assignment. Avoid both vague objectives and unrelated history.

For example: "Add a CSV export of the currently filtered results. Preserve existing filtering and follow the project's export conventions. Handle implementation and relevant checks. Return the resulting behavior, affected files and any remaining limitation."

Use the user's model and cost constraints when selecting workers. Configure model and reasoning effort explicitly when supported; account for history defaults that inherit the coordinator's settings. Prefer fresh, scoped context and follow the host's spawn schema. Keep model identifiers and personal preferences in host configuration.

Each worker executes its assignment directly unless further delegation is explicitly assigned. Keep write scopes non-overlapping and concurrency within the user's authorization. Reuse a worker for related follow-up. Assign integration to a worker when multiple outputs need to work together.

## Manage and accept

Request a concise outcome, relevant deliverable or file references, a verification summary when applicable, and remaining issues. Trust the worker's result as the normal basis for acceptance. Assess whether the requested outcome was delivered and contributes to the overall goal; technical proof is not a second coordinator deliverable. A smaller worker model does not by itself justify extra scrutiny.

Do not request tool-call transcripts, raw logs, exhaustive diffs or repeated checks to gain confidence in the worker. If the result is missing, contradictory or functionally incomplete, describe the specific outcome gap and return it to a worker. Technical diagnosis and verification remain with that worker. Assign any explicitly required technical review to a worker rather than performing it yourself or adding review layers by default.

Wait for meaningful results when no management decision is pending. Resolve scope questions and dependencies without maintaining a parallel implementation. If delegation is unavailable, report the limitation; remain in the coordinator role until the user changes the arrangement.

Finish when the overall objective is met and known outcome gaps are resolved. Report the result and material limitations without claiming unverified success. Delegation grants no additional execution permissions. Follow applicable project ownership and continuity rules without duplicating their state.
