# Optional Harness consolidation

This workflow works without Harness. Use integration only when Harness is already installed and tracks the project. Resolve the installed package from available skills or host tools; do not assume a global install path, import a sibling skill, initialize a project, or write Harness state yourself.

For read-only context, the single reporting interface is:

```bash
python3 /resolved/installed/harness/scripts/harness.py consolidate --project /path/to/project
```

The report is read-only JSON: identity, current ownership/contributions, unresolved work, and report revision. Optional `--data JSON` is reserved for the installed command's documented report options. Use the installed help/schema if a version differs; do not invent fields. A report does not prove that current Git files match an earlier handoff.

## Stable commit or PR consolidation

Before treating the workspace as ready for a commit or PR delivery, request an exclusive whole-workspace claim through the installed Harness entry point:

```bash
python3 /resolved/installed/harness/scripts/harness.py task.start \
  --project /path/to/project \
  --data '{"objective":"Consolidate verified delivery changes","resources":["."],"request_id":"unique-consolidation-id"}'
```

Use a unique request ID for a new logical claim and preserve the returned `session.id` (or `session_id` when exposed by that installed version). An overlap means another writer may still be changing files. Report that overlap; do not force the claim, mark the other writer complete, or claim all contributions are included. A clearly limited read-only draft can proceed. If Harness is absent, unavailable, or not configured for the project, continue from Git and task evidence, explicitly stating the lack of coordinated ownership when material.

After a successful claim:

1. Read `consolidate` again and inspect actual status, staged/unstaged diffs, untracked contents, base-to-head commits/diff for a PR, and unresolved contribution records. Determine which files and results are included, excluded, or pending. Resolve uncertainty with evidence; do not infer completion from silence.
2. Preserve unrelated work and honor the requested action. A stable draft may still await commit or publication approval. Record the reviewed revision and files. Recheck Git immediately before an authorized mutation; claims coordinate participating agents, not external editors.
3. Checkpoint the result and release only the session created for this consolidation:

   ```bash
   python3 /resolved/installed/harness/scripts/harness.py task.checkpoint \
     --project /path/to/project \
     --data '{"session_id":"returned-session-id","summary":"Prepared the scoped delivery","evidence":["Actual changed paths and revision inspected; relevant check outcomes recorded"],"next_action":"Commit or publication approval remains pending, if applicable.","status":"delivered","request_id":"unique-delivery-id"}'
   ```

   Replace the illustrative evidence with actual paths, revisions, checks, unresolved contributions, and pending approvals. Do not store secrets or raw conversations. If the installed command uses a different documented checkpoint schema, follow it.

Do not retain a whole-workspace claim while awaiting the user. Before a later commit or publication, obtain a new claim and recheck contributions and actual Git state. If a claim or checkpoint fails, report that failure and avoid representing coordinated consolidation as successful. A delivered consolidation session means this preparation is complete; it does not mark other contributions delivered or imply every requested external action occurred.
