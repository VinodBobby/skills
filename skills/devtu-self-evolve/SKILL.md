---
name: devtu-self-evolve
description: >
  Orchestrate ToolUniverse discovery, tool testing, fixes, and skill improvement. Use for
  debug rounds, tool coverage, or quality work. Publishing requires a separate explicit request.
---

# ToolUniverse Self-Evolution Orchestrator

Coordinates the full development lifecycle by dispatching to specialized devtu skills.

## The Cycle

```
Discover → Create → Test → Fix → Optimize → Report
```

Each phase maps to a dedicated skill:

| Phase | Skill | What it does |
|-------|-------|-------------|
| **Discover** | `research` | Research coverage gaps and compare candidate APIs |
| **Create** | `devtu-create-tool` | Build tool class + JSON config + test examples |
| **Test** | *(this skill)* | Launch researcher persona agents to find issues |
| **Fix** | `devtu-fix-tool` | Diagnose failures, implement fixes, validate |
| **Optimize** | `devtu-optimize-skills` | Improve skill reports, evidence handling, UX |
| **Tool descriptions** | `tooluniverse-custom-tool` | Write or revise descriptions against the tool schema and behavior |
| **Docs** | `tooluniverse-self-review` plus repository checks | Review documentation and run relevant validators |
| **Publish (explicit request only)** | `devtu-github` | Commit, push, or create a PR when the user asks |

## Quick Start

Pick an entry point based on what's needed:

- **"Run a test round"** → jump to [Testing Phase](#testing-phase)
- **"Expand coverage"** → invoke `Skill(skill="research")` to compare candidate APIs with current coverage
- **"Create a new tool"** → invoke `Skill(skill="devtu-create-tool")`
- **"Fix a broken tool"** → invoke `Skill(skill="devtu-fix-tool")`
- **"Improve skills"** → invoke `Skill(skill="devtu-optimize-skills")`
- **"Full cycle"** → follow the development phases below and report results; publishing needs a separate explicit request

---

## Phase 1: Discovery (optional)

Use `Skill(skill="research")` to compare ToolUniverse coverage with authoritative API documentation. Report candidates with evidence about fit, access requirements, license, and maintenance. Do not create tools or publish changes during discovery.

## Phase 2: Tool Creation (optional)

Invoke `Skill(skill="devtu-create-tool")` for each new API:
1. Create Python tool class implementing the API
2. Create JSON config with parameters, descriptions, test examples
3. Register in `_lazy_registry_static.py` and `default_config.py`
4. Validate: `python -m tooluniverse.cli test <ToolName>`

## Phase 3: Testing Phase

This is the core testing loop, run directly by this skill.

### Setup

1. Check for open PRs: `gh pr list --state open`
2. If unmerged PR → use that branch; if merged → new branch from `origin/main`
3. Rebase: `git fetch origin && git rebase origin/main`

### Researcher Persona Agents

Launch 2 agents per round (A + B) using the Agent tool with these parameters:

**Each agent gets:**
- Domain specialty (oncology, genomics, pharmacology, etc.)
- Research question (specific biological question)
- 5-7 test scenarios exercising different tools
- Instructions to report issues with severity (HIGH/MEDIUM/LOW)
- Issue IDs: `Feature-{round}{letter}-{num}` (e.g., `Feature-59A-001`)

**Agent prompt template** — see [references/persona-template.md](references/persona-template.md)

### Verification (CRITICAL)

Before implementing ANY agent-reported issue, verify via CLI:
```bash
python3 -m tooluniverse.cli run <ToolName> '<json_args>'
```

**50%+ of agent reports are false positives** from MCP interface confusion. Only fix verified issues.

### Fix Principles

1. **Prevent, don't recover** — fix root cause, not symptoms
2. **Validate at input** — reject bad params early with clear guidance
3. **Distinguish "no data" from "bad query"** — different messages for each
4. **Fix the abstraction** — don't add alias lists that grow forever

Anti-patterns: hint text instead of validation, parameter aliases instead of fixing naming, post-hoc probing instead of pre-validation.

### Skill Usefulness Testing (NEW — beyond tool testing)

Standard testing verifies tools work. Usefulness testing verifies skills actually solve scientist problems. Run this after standard testing:

1. **Pick a real research question** that the skill claims to answer (not a tool-level test)
2. **Launch an agent** following the skill workflow on the real question
3. **Assess honestly**: Does the skill produce an actionable answer, or just a data dump?

**Score 1-10 rubric**:
- 1-3: Tool catalog — lists tools without interpretation
- 4-6: Data collector — gathers data but doesn't help combine/interpret
- 7-8: Reasoning framework — guides interpretation with tables/scoring/synthesis
- 9-10: Decision engine — produces concrete, defensible recommendations

**Common failure patterns found in usefulness tests**:

| Pattern | Score Impact | Fix |
|---------|-------------|-----|
| "Call A, then B, then C" without explaining what to DO with results | -3 | Add interpretation tables |
| Tool params wrong (tool works but skill documents wrong names) | -2 | Verify ALL tool params via `get_tool_info()` |
| Promises data the API can't deliver (e.g., DepMap CRISPR scores) | -2 | Be honest about limitations; add computational procedure workaround |
| No synthesis phase at the end | -2 | Add "so what?" phase that combines all evidence |
| No evidence grading | -1 | Add T1-T4 or similar confidence tiers |
| No computational procedures for things tools can't do | -1 | Add Python code blocks using scipy/pandas/numpy |

**When tools can't help, add computational procedures**: Some analyses need Python code, not API calls. Skills should include working code blocks for:
- Statistical testing (scipy.stats, FDR correction)
- Data analysis from downloaded files (pandas + CSV from DepMap, TCGA, etc.)
- Scoring algorithms (ACMG classification, viability scores)
- Sequence analysis (Biopython)

See `devtu-optimize-skills` Patterns 14-15 for full guidance.

## Phase 3.5: Benchmark Evaluation

Quantify plugin performance after testing. Uses `Skill(skill="devtu-benchmark-harness")`.

```bash
# Run lab-bench (20 MCQ)
python skills/devtu-benchmark-harness/scripts/run_eval.py --benchmark lab-bench --mode plugin-only --n 20

# Run BixBench (computational, use first 20)
python skills/devtu-benchmark-harness/scripts/run_eval.py --benchmark bixbench --mode plugin-only --n 20

# Analyze results
python skills/devtu-benchmark-harness/scripts/analyze_results.py --results <results-file>

# Generate report
python skills/devtu-benchmark-harness/scripts/generate_report.py --results <results-file> --output BENCHMARK_REPORT.md
```

Compare with previous round. If any category regresses, prioritize fixing that skill/tool in Phase 4.

## Phase 4: Fix & Validate

1. Implement verified fixes (see [references/bug-patterns.md](references/bug-patterns.md) for code-level patterns)
2. **Run code-simplifier**: `Skill(skill="simplify")` — always after writing or modifying code
3. Lint: `ruff check src/tooluniverse/<file>.py`
4. Verify syntax: `python -c "from tooluniverse.<module> import <Class>"`
5. Test: `python -m tooluniverse.cli run <Tool> '<json>'`
6. Keep changes local and report the changed files and validation results.
7. Do not stage, commit, push, or open a PR unless the user explicitly requests that action.

> Also see `Skill(skill="devtu-code-optimization")` for reusable fix patterns and anti-patterns.

## Phase 5: Optimize (optional)

After fixes are stable:
- `Skill(skill="tooluniverse-custom-tool")` — revise tool descriptions against the actual schema and behavior
- `Skill(skill="devtu-optimize-skills")` — improve research skill quality
- `Skill(skill="tooluniverse-self-review")` and the repository's documented checks — review documentation accuracy

## Phase 6: Publish (only on explicit request)

Do not enter this phase unless the user explicitly asks to commit, push, or open/update a pull request. Perform only the requested action. Use `devtu-github` for the authorized publishing steps. Do not force-push or rewrite remote history without separate explicit approval.

**GitHub repo**: `mims-harvard/ToolUniverse` — always verify with `git remote -v` before pushing.

---

## Git Rules (CRITICAL)

- **NEVER push to main** — all work on feature branches
- **NEVER commit, push, or open a PR without an explicit user request**
- **NEVER have multiple open fix PRs** — keep adding to current branch
- **Always rebase before push**: `git fetch origin && git rebase origin/main`
- **Commit message format**: no "BUG" terminology, use "Feature" or "Fix"
- **No AI attribution** in commits

## Common Issue Categories

| Category | Signal |
|----------|--------|
| Silent parameter miss | Wrong-field check; param ignored |
| Always-fires conditional | `.get("field")` on wrong type |
| Silent normalization | Auto-transform not disclosed |
| Wrong notation/case | Gene fusions, Title Case names |
| Substring match | Short symbol returns multiple targets |
| try/except indent | Mismatched → SyntaxError |

Full patterns → [references/bug-patterns.md](references/bug-patterns.md)

## Round Tracking

After each round: advance counter, update patterns file, keep this SKILL.md under 150 lines.

**Current round: 127** (rounds completed: 52-126)
