---
name: agentic-software-workflow
description: Plan or improve software work that relies on coding agents, especially long-running tasks, parallel agents, or repository setup for agent work. Use when asked to bootstrap an agent-ready repository or reduce coding-agent bottlenecks; not for routine feature coding.
---

# Agentic software workflow

Use this skill when coding agents are a significant part of software delivery. Preserve the user's scope and the repository's existing conventions.

## Choose the path

- For a new repository or a deliberate agent-readiness bootstrap, read [new-repo-bootstrap.md](references/new-repo-bootstrap.md).
- For agent-assisted work in an existing repository, inspect its instructions, architecture, build environment, tests, and CI before proposing changes.

## Existing repository workflow

1. Define a user-visible outcome and a small acceptance contract before assigning implementation. Prefer one complete workflow over a long feature-presence checklist.
2. Identify the authoritative checks and test data. Keep acceptance evidence independent from implementation so an agent cannot make a feature pass by weakening or removing its test.
3. Decompose work into small, independently verifiable changes. Parallelize only when interfaces and file ownership are clear. Use isolated worktrees or branches; give each worker explicit files or modules and a completion check.
4. Limit concurrency to the repository's build, test, machine, and review capacity. If agents wait on builds, collide in shared files, or create a review queue, reduce concurrency or improve the harness before adding agents.
5. Give agents a complete development environment and short, reliable commands. Keep routine test output concise; preserve detailed logs for diagnosis. Maintain a brief progress handoff when work spans sessions.
6. For complex or high-risk work, separate implementation from evaluation. Let the evaluator run the product through its real interface, using fixed acceptance criteria, representative inputs, and independent oracles. Calibrate evaluator findings against human review; an evaluator agent is not proof by itself.
7. Verify at multiple levels that fit the task: focused tests during work, integration or end-to-end acceptance for the workflow, and the repository's full required checks before handoff. For visual products, inspect the rendered result and test interactions, not just code or screenshots.
8. Keep the tree in a clean, buildable state at handoff. Report what passed, what remains, and any limit in the evidence.

## Measure the workflow

For an initial pilot, record enough to compare agent-assisted work with the existing baseline:

- elapsed time, model or API cost when available, and human review time;
- changes accepted on first review, rework, regressions, and reopened defects;
- acceptance-test completion and user-reported workflow failures.

Do not treat lines of code, commits, agent-hours, or feature counts as product readiness by themselves. Prefer the smallest evaluator that catches the important failures. Add more orchestration only when measured results justify its cost.

