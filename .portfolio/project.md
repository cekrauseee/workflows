---
slug: workflows
name: cekrause/workflows
repositoryUrl: https://github.com/cekrauseee/workflows
description: >-
  skills for the everyday work of building software with agents.
metaDescription: >-
  independent agent skills for delegation, git, code review, documentation,
  and html explanations, using tools already available in the project.
summary: >-
  i built workflows as independent skills for agent delegation, worktrees,
  commits, pull requests, reviews, documentation, and html explanations.
  they describe the decisions and checks each task needs while respecting
  the project and the user's instructions.
highlights:
  - "focused agent delegation"
  - "worktrees, commits, and pull requests"
  - "reviews checked against the code"
  - "documentation and html explanations"
  - "skills that work independently"
---

workflows is a set of skills for recurring development tasks: working with
git, reviewing changes, writing documentation, and coordinating agents.

i put the instructions into separate skills so each one can be used on its
own, with the tools the agent already has. the package also covers pull
requests and standalone html explanations.

## making the task clear

a review should point to a concrete problem in the code and explain what it
affects. a pull request description should tell someone what changed and what
was checked. documentation should match how the project actually works.

the skills give the agent those expectations while leaving room to make
decisions. they also cover handing work to other agents: choosing an available
model, sharing the context they need, keeping edits separate, and checking
what comes back.

## fitting the way you work

i kept the package as instructions, with no separate runtime. existing project
conventions and your explicit choices come first. asking for a review, for
example, doesn't also mean asking for edits or publication.

workflows can be used alongside harness. workflows guides the task; harness
keeps the project context available for the next one.
