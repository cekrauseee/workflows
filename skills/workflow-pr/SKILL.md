---
name: workflow-pr
description: Draft or update evidence-based pull request titles and descriptions from the complete diff, and publish when requested.
---

# Pull request

Produce a reviewer-ready title and description for the intended base and head. Inputs are the repository or PR, intended delivery scope, and any template. Drafting is read-only. Creating or updating a remote PR, including a draft, requires that action to be requested; a review request belongs to a read-only review workflow.

1. Confirm the target repository, base, head, and existing PR template or description. Inspect included commits, the complete base-to-head diff, and current staged, unstaged, and untracked files. Local changes absent from the head are not part of a published PR.
2. If installed Harness tracks this project, read [optional consolidation](references/harness-integration.md) before claiming delivery completeness or publishing. Compare unresolved and active contributions with actual Git files. Acquire a whole-workspace claim for stable consolidation when available; report overlap and keep a draft explicitly incomplete while another writer is active.
3. Derive the title from the principal resulting behavior. Prefer English Conventional Commits; follow explicit user/project choices. Host prefixes such as `codex/` are valid and a PR type need not match its branch or each supporting commit.
4. Preserve the repository's template. For a simple change, a short explanation plus verification is enough. Add change locations, review questions, or risks when they help assess a larger change. See [writing and renderer options](references/pull-requests.md). Do not invent verification, risks, or an obligatory set of headings.
5. Check each claim against the diff and evidence. State which relevant checks were not run and why. When scope changes, rewrite the description around the final result rather than the conversation history.
6. Return the draft unless publication is requested. For publication, verify base, head, branch availability on the remote, and current diff again. Use an available connector or CLI; preserve real newlines with a body file. A PR request does not itself authorize a merge. Re-read the resulting PR and report its URL and any remaining limitations.

Completion is a reviewable draft, or a verified remote PR after authorized publication. If the remote, credentials, permissions, or a contribution conflict block publishing, keep the finished local draft and report the specific blocker.
