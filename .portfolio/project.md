---
slug: workflows
name: cekrause/workflows
repositoryUrl: https://github.com/cekrauseee/workflows
description: >-
  Independent skills for engineering tasks and delegation between agents.
metaDescription: >-
  Workflows organizes recurring engineering tasks into procedures with explicit
  goals, boundaries, and completion criteria.
summary: >-
  I developed Workflows to organize recurring engineering tasks into
  procedures with explicit goals, boundaries, and completion criteria. The
  project includes seven skills covering orchestration, worktrees, commits,
  pull requests, reviews, documentation, and HTML deliverables. Each can be
  installed and used independently.
highlights:
  - seven skills covering orchestration, worktrees, commits, pull requests, reviews, documentation, and HTML deliverables
  - procedures with explicit goals, boundaries, and completion criteria
  - responsibility for the whole task
  - independently installed and used
---

I developed Workflows to organize recurring engineering tasks into procedures with explicit goals, boundaries, and completion criteria.

The project includes seven skills covering orchestration, worktrees, commits, pull requests, reviews, documentation, and HTML deliverables. Each can be installed and used independently.

## Procedures with defined boundaries

Each skill guides the decisions that matter for a particular task. A review should follow the requested criteria and connect its findings to evidence. A pull request should explain the problem, the resulting behavior, and the verification performed. A commit should bring together a coherent change.

The instructions also allow existing context and verification to be reused while they remain valid. Further investigation is called for when relevant information is missing.

The package consists of instructions and metadata, with no dedicated runtime, execution scripts, or hooks. Execution uses the tools and permissions of the environment where the skills are installed.

## Responsibility for the whole task

During orchestration, the coordinator defines objectives, assigns work, resolves dependencies, and assesses whether the results meet the request. Workers own investigation, technical decisions, implementation, integration, and verification.

Each assignment should provide the expected behavior, boundaries, and necessary context. When a delivery is incomplete, the coordinator describes what is missing and returns the task to the responsible worker.

This keeps technical responsibility with the agent doing the work. The coordinator manages outcomes and dependencies, while the worker carries the task through to completion.

Workflows can be used alongside Continuity: one guides execution procedures; the other keeps knowledge and contributions available across tasks and projects.
