---
name: workflow-artifact
description: Create and check standalone self-contained HTML explanations, maps, comparisons, and reports when a file artifact is requested or useful within the authorized task.
---

# HTML artifact

Produce an inspectable HTML file that opens directly from disk. Inputs are the explanation or report, verified source material, destination, and any requested visual style. Use this workflow when a standalone artifact improves the requested deliverable; ordinary explanations do not require a visualization.

1. Establish the intended audience, evidence, and final destination. Respect existing project documentation routes or an explicitly requested output folder. A neutral system-font presentation is a useful default; project branding and user-selected styles are permitted.
2. For a new file, optionally create an accessible starting page:

   ```bash
   python3 scripts/create_artifact.py PATH/report.html --title 'Request flow' --summary 'How a request moves through the system'
   ```

   The scaffold is not a finished visualization. Replace its example structure with source-grounded content and interactions that help the explanation. Existing differing content is protected unless `--replace` is explicitly supplied. See [artifact implementation](references/artifacts.md) for helper options.
3. Keep runtime dependencies embedded: CSS, essential JavaScript, images, fonts, and data. Inline SVG or embedded image data are suitable. Use semantic structure, useful text alternatives, keyboard controls, visible focus, and reduced motion where needed. Display the language actually used in `lang`.
4. Validate with `python3 scripts/check_artifacts.py PATH/report.html`. Check facts and usability beyond what the static scanner can prove. Add or update the existing documentation route when this is a project documentation deliverable; an index is not mandatory for a standalone report.
5. Return the final file and validation result, mentioning any material unperformed visual or interactive check. Do not label a scaffold or unverified draft as complete.

The checker enforces a portable HTML contract, not a particular page design. A requested application prototype with external dependencies is a different deliverable; preserve that request rather than silently converting it to a static report. Temporary files need no specific Harness path. If installed Harness is available and relevant continuity is needed, read its `scripts/harness.py consolidate --project PATH` report without initializing it.
