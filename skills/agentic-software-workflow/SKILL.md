---
name: agentic-software-workflow
description: Plan or improve software work that relies on coding agents, especially long-running tasks, parallel agents, or repository setup for agent work. Use when asked to bootstrap an agent-ready repository or reduce coding-agent bottlenecks; not for routine feature coding.
---

# Agentic software workflow

Use this skill when coding agents are a significant part of software delivery. Preserve the user's scope and the repository's existing conventions.

## Choose the path

- For a new repository or a deliberate agent-readiness bootstrap, read [new-repo-bootstrap.md](references/new-repo-bootstrap.md).
- For agent-assisted work in an existing repository, inspect its instructions, architecture, build environment, tests, and CI before proposing changes.

## Choose a task shape

- **Scout:** investigate, plan, or audit without editing; return a standalone report with evidence, gaps, and a recommendation.
- **Ship:** make an authorized change against a clear outcome and acceptance contract; name the owned files or area and the completion evidence.
- **Evaluator:** independently check higher-risk work against fixed acceptance criteria; return evidence without changing the implementation unless assigned a separate ship task.
- Split research from implementation when it can clarify scope or produce an independent outcome. Keep one coordinator responsible for user communication and integration.

## Existing repository workflow

1. Define a user-visible outcome and a small acceptance contract before assigning work. Default to one owner; split only when the outcomes can proceed and be verified independently. Prefer one complete workflow over a long feature-presence checklist.
2. Identify the authoritative checks and test data. Keep acceptance evidence independent from implementation so an agent cannot make a feature pass by weakening or removing its test. Test observable behavior through a public interface with an independent oracle; source-string checks only prove behavior when the text itself is the contract.
3. Give each worker the smallest self-sufficient brief: task shape and outcome, observable done condition, relevant source-of-truth context, owned area and boundaries, required check, and return format. Do not forward the full conversation or repeat general instructions. Treat the user's ask as scope; record useful out-of-scope ideas as follow-up instead of adding them.
4. Give each editor an isolated worktree or branch and clear ownership. Prefer non-overlapping areas, but treat file overlap as a risk rather than an automatic blocker when tasks are independent, independently verifiable, and safe to reconcile. Serialize true semantic dependencies, shared mutable state, incompatible migrations, or work that cannot be reconciled safely.
5. Keep one coordinator responsible for routing, integration, and user communication. Workers return to the coordinator. Use completion signals where available; send updates when a deliverable, blocker, or decision changes, and avoid routine status chatter or repeated polling of healthy work. Resolve routine choices directly and surface decisions that affect scope, acceptance, or authority.
6. Limit concurrency to build, test, machine, and review capacity. If agents wait on builds, create conflicts that are hard to reconcile, or leave a review queue, reduce concurrency or improve the harness before adding agents. Give workers a reproducible environment and short commands; keep routine output concise and retain detailed logs for diagnosis.
7. For complex or high-risk work, separate implementation from evaluation. Let the evaluator use the real interface, fixed acceptance criteria, representative inputs, and independent evidence. Reuse the selected delivery path's review and test gates; do not add a duplicate reviewer for the same checks. An evaluator agent is not proof by itself.
8. Verify acceptance against artifacts and checks, not a worker's status message alone. Run focused checks, workflow-level acceptance, and the repository's required checks as appropriate. For visual products, inspect the rendered result and interactions. At handoff, report changed paths, checks and results, remaining risks, and what could not be verified.

### Brief and handoff shape

```text
Task: <scout, ship, or evaluator outcome>
Done when: <observable acceptance condition>
Context and scope: <source-of-truth links, owned area, constraints, non-goals>
Verify: <check and independent evidence>
Return: <result, artifact or changed paths, check outcomes, blockers or unknowns>
```

If a worker finds a material ambiguity, scope conflict, or authority question, return the specific blocker and decision needed to the coordinator. Do not guess, broaden the task, or contact the user around the coordinator. A ship task does not authorize commit, push, merge, deployment, or other external writes unless the brief explicitly includes that action.

## Gate-managed delivery

When the user chooses a configured delivery gate such as `no-mistakes`, treat it as the single owner of its review, test, documentation, lint, publish, PR, and CI stages. Use its installed skill and current CLI help; do not run a parallel copy of the same gates or push around a parked gate. Only skip or override a gate through its supported decision path with the required authorization.

- Preserve the user's intent, constraints, and decisions as the gate's review context; do not replace them with a summary of the diff.
- Let the gate work in its isolated workspace. Apply only findings it classifies as low-risk mechanical fixes; return product, scope, or intent decisions to the user.
- Re-run affected checks after fixes. If a repair changes reviewed code or its base and the gate cannot prove it is still covered, require review again before publication.
- Wait on the gate's completion or decision signal instead of polling. Report skips, overrides, and failure states accurately. A green check result means the change is ready for the next authorized step; it does not mean the PR was merged.
- Do not install or initialize a gate, push, open a PR, or merge unless the user's request authorizes that action.

For work that spans sessions, follow the [session-continuity](../session-continuity/SKILL.md) skill.

## Measure the workflow

For an initial pilot, record enough to compare agent-assisted work with the existing baseline:

- elapsed time, model or API cost when available, and human review time;
- changes accepted on first review, rework, regressions, and reopened defects;
- acceptance-test completion and user-reported workflow failures.

Do not treat lines of code, commits, agent-hours, or feature counts as product readiness by themselves. Prefer the smallest evaluator that catches the important failures. Add more orchestration only when measured results justify its cost.

