# STORM Analysis: Applying AXI, Firstmate, and no-mistakes to this skills repository

## Assumptions and scope

This analysis covers the portable skills repository in this checkout and the current public contents of [`gh-axi`](https://github.com/kunchenguid/gh-axi), [`firstmate`](https://github.com/kunchenguid/firstmate), [`axi`](https://github.com/kunchenguid/axi), and [`no-mistakes`](https://github.com/kunchenguid/no-mistakes). The goal is to improve the repo's skill authoring and agent workflows, not to turn this skills catalog into a coding-agent runtime.

The checkout tracks 52 `SKILL.md` packages under `skills/`; 11 are ToolUniverse-oriented and 3 are listed as optional. The README already separates default, optional, and science installs.

## Perspectives and interview questions

| Perspective | Question | Finding |
| --- | --- | --- |
| Skill user | How quickly can an agent choose the right workflow and act without repeated lookups? | The portable design guide already calls for focused triggers and progressive disclosure. It did not explicitly cover low-noise outputs, definitive empty states, or avoiding retrying a successful write after a failed readback. |
| Skill maintainer | How can guidance stay brief and avoid drifting from fast-changing tools? | `gh-axi` uses a small discovery skill that points to the CLI's current dashboard and help rather than maintaining a second command manual. This is a useful pattern for tool-backed skills, but a runtime dependency should remain optional. |
| Work coordinator | How should research, implementation, and review be assigned? | Firstmate separates read-only "scout" reports from authorized "ship" changes, gives parallel editors isolated worktrees, and keeps one liaison responsible for reconciling the crew's work. Its supervisor contract also uses task-specific briefs, treats overlap as a risk rather than an automatic blocker, serializes true dependencies or shared state, and avoids duplicate review gates. These refine the repo's existing independence, worktree, evaluator, and concurrency guidance. |
| Delivery gate | Where should validation happen, and what should a green result mean? | `no-mistakes` defines one opt-in, isolated path with ordered review, test, docs, lint, publish, PR, and CI steps. It distinguishes low-risk mechanical fixes from findings that require user judgment and keeps merge authorization separate from validation. This fits as an optional path in the existing workflow and publishing skill, not as a second default pipeline. |
| Portability and safety | Which upstream features fit a cross-harness skill catalog? | Compact guidance, explicit task boundaries, actionable errors, and opt-in setup transfer well. Persistent agent fleets, runtime hooks, remote secondmates, and social relays belong to an execution distro, not this portable skills catalog. |

## Evidence ledger

| Claim | Evidence | Confidence and limit |
| --- | --- | --- |
| The repo already has a portability and disclosure framework. | [`docs/portable-skill-design.md`](portable-skill-design.md) requires one clear job, trigger-specific descriptions, relative resources, host adapters, least privilege, and package and behavior validation. [`skills/skill-doctor/SKILL.md`](../skills/skill-doctor/SKILL.md) checks unique value, context cost, overlap, and evidence. | High; directly read in this checkout. |
| AXI is principally a design guide for agent-facing CLIs. | [`axi` README](https://github.com/kunchenguid/axi) describes ten principles including compact output, minimal defaults, truncation, aggregates, definitive empty states, structured errors, contextual next steps, and consistent help. | High for what the project specifies; applying it to static skill prose requires adaptation. |
| `gh-axi` has a discoverable runtime path and explicit error semantics. | [`gh-axi` README](https://github.com/kunchenguid/gh-axi) describes a small installable skill that directs agents to current CLI help, optional session hooks, zero-result versus fetch-failure states, and warnings against retrying a successful mutation when readback fails. | High for the documented design. The skill requires Node.js and authenticated `gh`; no dependency is added here. |
| The published benchmark favors `gh-axi` in its tested GitHub tasks. | The [`gh-axi` benchmark](https://github.com/kunchenguid/gh-axi#benchmarks) reports 17 tasks, 5 interface conditions, and 5 repeats using Claude Sonnet 4.6; its table shows 100% success and $0.050 average cost for `gh-axi` versus 86% and $0.054 for raw `gh`. | Moderate as evidence for that setup; the model, tasks, harness, and judge limit generalization. It is not evidence that every workflow should replace its existing GitHub integration. |
| Firstmate separates work shapes and defines concise dispatch and supervision contracts. | [`firstmate` README](https://github.com/kunchenguid/firstmate) describes scout reports versus ship tasks, clean worktrees for parallel tasks, one liaison, and event-driven supervision. Its [`AGENTS.md`](https://github.com/kunchenguid/firstmate/blob/main/AGENTS.md) says to keep briefs task-specific, preserve the user's ask as acceptance scope, treat overlap as a risk signal, serialize only real dependencies or unsafe shared state, and let the selected delivery path own its review rigor. | High for its stated design; exact runtime controls remain Firstmate-specific. |
| `no-mistakes` gates delivery before publication and keeps approval authority visible. | Its [Gate Model](https://kunchenguid.github.io/no-mistakes/concepts/gate-model/) uses a named opt-in remote, a disposable worktree, and an ordered intent, rebase, review, test, document, lint, push, PR, and CI pipeline. Its [pipeline guide](https://kunchenguid.github.io/no-mistakes/concepts/pipeline/) says configured checks add to, rather than replace or reorder, the core path; its [agent skill](https://github.com/kunchenguid/no-mistakes/blob/main/skills/no-mistakes/SKILL.md) distinguishes validate-only and task-first modes, preserves user intent, and escalates user-judgment findings. | High for its published behavior; the tool requires per-repository initialization, a daemon, a runnable agent, and explicit choice of this delivery path. |
| Existing skills already have useful GitHub routing and agent-work safeguards. | [`skills/github/SKILL.md`](../skills/github/SKILL.md) routes review, CI, and publishing to specialist skills and separates reads from writes. [`skills/agentic-software-workflow/SKILL.md`](../skills/agentic-software-workflow/SKILL.md) limits concurrency, scopes file ownership, separates evaluation, and measures outcomes. | High; direct local evidence. |

## Synthesis and changes

The best fit is to adapt the interface principles into skill-writing and auditing guidance, not copy all ten CLI requirements into every skill. Existing skills often describe a human-facing workflow rather than a command-line product, so output schemas, exit codes, and session hooks only apply when the skill actually fronts a tool.

Applied in this checkout:

1. Added interaction-efficiency guidance to [`docs/portable-skill-design.md`](portable-skill-design.md): compact defaults, clear empty versus failed results, bounded output, actionable errors, safe retry behavior, relevant next actions, and lightweight task-based measurement.
2. Extended [`skills/skill-doctor/SKILL.md`](../skills/skill-doctor/SKILL.md) to examine avoidable calls, output noise, task routing, and tool failure states alongside context cost and overlap.
3. Added scout, ship, and evaluator task shapes and a compact brief/handoff contract to [`skills/agentic-software-workflow/SKILL.md`](../skills/agentic-software-workflow/SKILL.md). The coordinator remains the user's contact; briefs preserve scope; isolated parallel work may continue through manageable file overlap; real dependencies, shared state, and unsafe integrations serialize; routine status and duplicate review are minimized.
4. Updated [`skills/github/SKILL.md`](../skills/github/SKILL.md) to use `gh-axi` when already installed for shell-based tasks, while preserving the connected integration and raw `gh` fallbacks. The guidance also protects against ambiguous empty results and duplicate writes after failed readback.
5. Added an optional gated-delivery path to [`skills/agentic-software-workflow/SKILL.md`](../skills/agentic-software-workflow/SKILL.md) and [`skills/yeet/SKILL.md`](../skills/yeet/SKILL.md). They preserve user intent for review, avoid duplicate checks, defer intent-sensitive findings, distinguish PR readiness from merge, and leave installation opt-in. The workflow also calls for behavioral checks against an independent oracle instead of treating source-string matches as proof.

## Defer

- Do not add a new general AXI skill: that would repeat the portable design guide and the existing skill authoring and audit paths.
- Do not install `gh-axi` or its session hooks by default. They add Node.js, authentication, and host setup requirements; use them only when already available or requested.
- Do not run `no-mistakes init` by default. It adds a named Git remote, local hooks, a background daemon, and an agent skill; repository initialization must be an explicit user choice. Avoid copying its full command guide because the upstream agent skill and CLI help are the current source of truth.
- Do not import Firstmate's entire distro, worker fleet, persistent supervision, or Relay into this catalog. Its task-boundary and worktree patterns are the reusable parts.
- Do not remove or merge skills based only on overlap in vocabulary. The repo's `skill-doctor` guidance requires evidence of redundant behavior and cautions against treating size or a lack of usage data as a deletion rule.

## Follow-up measurement

The changes are design-level improvements; no before/after behavior benchmark was run. For a later evaluation, compare two to five representative skill tasks with the same model, tools, context, and inputs. Record task success and correctness, unnecessary calls or turns, output size or input tokens when available, time spent resolving conflicts, and human review effort. Report the result as unknown where the host cannot isolate the skill or reproduce conditions.
