---
slug: workflows
name: cekrause/workflows
repositoryUrl: https://github.com/cekrauseee/workflows
description: >-
  clear outcomes for everyday development work with agents.
metaDescription: >-
  seven independent skills for delegation, git, reviews, documentation, and html
  deliverables, with scoped context and technical autonomy for workers.
summary: >-
  i built workflows to make recurring engineering tasks clear without scripting
  every action. seven independent skills cover delegation, worktrees, commits,
  pull requests, reviews, documentation, and html deliverables. workers own the
  technical work; coordinators manage the outcomes.
highlights:
  - "delegation through complete outcomes"
  - "worktrees, commits, and pull requests"
  - "reviews within the requested scope"
  - "documentation and standalone html deliverables"
  - "independent skills using existing tools"
---

workflows is a set of skills for the development tasks i kept coming back to:
git operations, reviews, documentation, and coordinating agents. i separated
them so an agent can load the procedure it needs without taking on every
other workflow at the same time.

the package contains seven independent skills and uses the host's existing
tools. there is no separate runtime, required model, or bundled execution script.

## make the outcome clear

a commit should group a coherent change. a pull request should explain the
problem, the resulting behavior, and what was checked. a review should follow
the requested criteria and connect its findings to evidence. documentation
should match how the project actually works.

the instructions focus on those results. a wording change to a pull request
doesn't need a fresh investigation of the repository. current context and
relevant verification can be reused, with more inspection when a real gap
needs to be resolved.

## delegate the whole task

when i ask for orchestration, the coordinator defines outcomes, assigns work,
manages dependencies, and checks whether the delivered result meets the goal.
workers own investigation, implementation choices, integration, checks, and fixes.

a handoff explains the expected behavior, boundaries, and necessary context.
it leaves technical decisions with the worker instead of turning the assignment
into a list of edits. the coordinator can return an incomplete result with a
clear description of what is missing, without reconstructing every tool call.

model choices follow the request and the capability the work needs. delegation
is explicit; without it, the agent works directly. the coordinator stays in its
management role while the workers execute.

## fit the project

project conventions and explicit user choices come first. a request for a
review doesn't also authorize edits or publication. an html file is created
when that is the requested deliverable, and checks stay relevant to the work.

workflows can be used alongside continuity. continuity groups related projects
in shared environments and keeps knowledge and contributions available.
workflows handles the execution procedure; it doesn't create those environments
or turn shared context into an instruction to read every project.
