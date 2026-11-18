# STORM analysis: Pstack and Matt Pocock skills

**Reviewed:** 2026-11-18
**Scope:** Fit of Pstack and Matt Pocock's engineering skills to this portable skills repository, with a focused addition for codebase architecture.

## Assumptions

- “Pstack” means [`backnotprop/pstack`](https://github.com/backnotprop/pstack), its standalone mirror of Cursor's Pstack skills, not another project with the same name.
- “Better fit” means useful in this repo's cross-agent skill collection: focused, portable, compatible with the skills already here, and maintainable without requiring one agent host or external workflow service.
- This is an architecture-fit comparison. A benchmark result would need to isolate each skill under the same model, tools, repository, and task inputs.

## Perspectives

### 1. Fit to our codebase scenarios

Pstack's `architect` is a useful pre-code check: trace what the change touches, sketch two designs, and compare ownership and caller knowledge. The upstream README lists `arena` as a companion for `architect`. The broader Pstack `poteto-mode` routes many coding tasks through playbooks and principles.

Matt Pocock's `codebase-design` focuses on module interfaces, seams, and testability. `improve-codebase-architecture` surveys an existing repository for refactoring candidates and produces a visual report. For our existing skill set, the focused design lens fills a clearer gap than another all-purpose coding router.

### 2. Workflow and portability

Pstack's mirror is distributed as standalone Agent Skills and includes individual skills that can work without the main router. Its full `poteto-mode` still brings broad orchestration, model-role configuration, playbooks, and agent-specific delegation expectations. Adding that whole system would overlap our portable guidance and host adapters.

Matt's focused design skill is narrower, but its companion architecture survey expects a skill tool, subagents, a `GLOSSARY.md` convention, grilling, and a specific HTML report flow. Those details do not match this repo's current `CONTEXT.md` domain-modeling convention or its goal of keeping portable entry skills small. The design principles transfer; the full report workflow does not need to.

### 3. Overlap with skills already here

This repo already has `system-design` for greenfield system and API architecture, `domain-modeling` for business language, `service-performance-architecture` for measured performance goals, and `code-review` for implemented diffs. The missing route is choosing a sound module shape when changing an existing codebase. A focused `codebase-design` skill can own that route without replacing those skills.

### 4. Benchmark evidence

The repo's `devtu-benchmark-harness` evaluates ToolUniverse-oriented scientific benchmarks; it does not compare architecture or coding workflow skills.

The v2 SWE-Skills-Bench preprint pairs 98 skills with ten tasks each, running each task with and without the skill across four agent-model configurations. Its aggregate pass rate changes only from 76.6% to 76.9%, with 92 of 98 evaluated skills classified as having no statistically significant effect. The published aggregate does not establish a head-to-head result for Pstack versus Matt Pocock, and I found no candidate-specific comparison in the benchmark materials reviewed. The benchmark is evidence to test skills in their intended scenarios, not evidence that either collection wins here.

## Source ledger

| Claim | Source | Confidence and limit |
| --- | --- | --- |
| Pstack contains stand-alone skills and a larger task router; its `architect` skill compares designs before coding. | [Pstack README](https://github.com/backnotprop/pstack) and [`architect/SKILL.md`](https://github.com/backnotprop/pstack/blob/main/skills/architect/SKILL.md) | High for the published package description; the full router's host-specific steps still need review before adoption. |
| Matt Pocock's collection separates reusable codebase-design vocabulary from its repository-wide architecture survey. | [Matt Pocock skills README](https://github.com/mattpocock/skills/blob/main/README.md), [`codebase-design`](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md), and [`improve-codebase-architecture`](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md) | High for current upstream intent; the survey's surrounding tool and glossary conventions are not portable as-is. |
| General skill injection has small average effects and does not rank these two families. | [SWE-Skills-Bench paper, v2](https://arxiv.org/abs/2603.15401) and [benchmark results](https://github.com/ControllableModel/SWE-Skills-Bench) | High for the reported aggregate; no direct Pstack/Matt Pocock head-to-head was found. |
| The repo's existing skills cover greenfield architecture, domain modeling, performance architecture, and code review. | [`system-design`](../skills/system-design/SKILL.md), [`domain-modeling`](../skills/domain-modeling/SKILL.md), [`service-performance-architecture`](../skills/service-performance-architecture/SKILL.md), and [`code-review`](../skills/code-review/SKILL.md) | High; verified in this checkout. |

## Outline

1. Keep the current focused skills and preserve their separate jobs.
2. Add a codebase-design route for structural changes to existing systems.
3. Use Matt Pocock's module-design lens as the main source and Pstack's two-shape comparison as a bounded decision technique.
4. Leave Pstack's full router and Matt's visual survey workflow out until this repo has measured need and compatible adapters.

## Synthesis

For this repo, Matt Pocock's focused `codebase-design` is the better foundation: it covers module responsibilities, interfaces, and test seams without introducing a general coding orchestrator. Pstack's `architect` contributes one useful rule for non-trivial structural changes: compare two plausible shapes before settling on one.

I added a first-party [`codebase-design`](../skills/codebase-design/SKILL.md) skill that combines those parts in this repo's terms. It tells agents to trace actual callers and state, compare alternatives only when the change merits it, select the simplest sound shape, and route greenfield, performance, domain, and diff-review work to the existing skills.

## Gaps

- Neither package was present as a tracked skill directory in this checkout; the comparison uses their current upstream documentation.
- No controlled local A/B benchmark was run. This environment cannot inject each candidate in otherwise identical agent runs, and the repo's benchmark harness is for ToolUniverse tasks.
- The benchmark results provide a useful general caution but cannot support a measured winner between these two candidates. A direct pilot would need fixed tasks from this repo, a fixed agent/model/tool setup, and scored behavior with each candidate enabled and withheld.
