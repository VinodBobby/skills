# Portable Agent Skills

This repository develops reusable agent skills that can move across machines and supported agent environments.

## Install

```bash
git clone https://github.com/VinodBobby/skills.git ~/Projects/skills
~/Projects/skills/install.sh
```

The installer links each skill directory into `~/.agents/skills` (Codex, Cursor) and `~/.claude/skills` (Claude Code, Cursor), links each [subagent](#subagents) into `~/.claude/agents` (Claude Code, Cursor), and links [global/AGENTS.md](global/AGENTS.md) to `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`, and `~/.gemini/GEMINI.md`. Because these are links, `git pull` updates every harness.

| Flag | Effect |
| --- | --- |
| *(none)* | First-party skills and the Obsidian catalog |
| `--with-optional` | Adds skills listed in [profiles/optional.txt](profiles/optional.txt) |
| `--with-science` | Adds the Harvard ToolUniverse catalog |
| `--all` | Both of the above |
| `--no-memory` | Leaves global instruction files alone |
| `--defaults` | Returns this machine to the default selection |
| `--update` | Pulls this repository, then relinks |
| `--force` | Moves machine-local entries that share a repo name to `~/.skills-backup/<timestamp>/` and links the repo version |
| `--dry-run` | Prints the actions without changing anything |
| `--uninstall` | Removes every link into this repository |

The installer saves the selection flags (`--with-*`, `--all`, `--no-memory`, `--defaults`) in `~/.config/portable-skills/install-flags` and reuses them on any run that passes none, including `--update` and `--force`. Passing selection flags replaces the saved set.

### Keeping machines current

Run `install.sh --update` on each machine. It fast-forwards this checkout, links new skills and subagents, and removes links to deleted ones. It stops without relinking when the checkout has local commits or edits that block a fast-forward. Commit skill changes here and push them; avoid editing skills through the installed links on a machine. To update on a schedule, add a cron entry such as `0 9 * * * ~/Projects/skills/install.sh --update >/dev/null 2>&1`.

### Machine-local skills

Anything in the target directories that is not a link into this repository is machine-local, and the installer keeps it, including a local skill that shares a name with a repo skill. The installer lists those name clashes after each run; `--force` replaces them with the repo version. Same-name copies in the legacy `~/.codex/skills` directory are reported the same way, because Cursor also scans it. Broken links are removed.

Add a target directory to `SKILL_TARGETS` in [install.sh](install.sh) for another harness, such as `~/.gemini/skills`.

## Design

See [Portable skill design](docs/portable-skill-design.md) for the design principles, package shape, and validation approach.

## Starting a skill

Use [the skill template](templates/skill/SKILL.md) as a starting point. Keep each skill focused on one repeatable workflow. Add references, scripts, or assets only when they support that workflow. Run `python3 scripts/validate_skills.py` (requires PyYAML) before committing; CI runs the same check.

## Skills

- [Product UI](skills/product-ui/SKILL.md): design and implement polished, responsive interfaces with complete interaction states and accessible defaults.
- [Figma Design](skills/figma-design/SKILL.md) *(optional)*: create or revise product screens in Figma using its available design system and integration.
- [Diagram Design](skills/diagram-design/SKILL.md): create evidence-based flowcharts, architecture diagrams, sequences, state machines, and data models.
- [Document Editing](skills/document-editing/SKILL.md) *(optional)*: revise reports and office documents while preserving meaning and structure.
- [PDF Workflow](skills/pdf-workflow/SKILL.md) *(optional)*: inspect, create, and make authorized edits to PDFs with page-level checks.
- [System Design](skills/system-design/SKILL.md): design systems and evaluate architectural decisions. Synced from [Anthropic's upstream skill](skills/system-design/UPSTREAM.md).
- [Service Performance Architecture](skills/service-performance-architecture/SKILL.md): design responsive backend services with measured bottlenecks, bounded I/O, and cache-safe request paths.
- [Agentic Software Workflow](skills/agentic-software-workflow/SKILL.md): plan agent-assisted delivery, reduce coding-agent bottlenecks, and bootstrap agent-ready repositories.
- [Session Continuity](skills/session-continuity/SKILL.md): keep long-running work recoverable across sessions with a short continuity note.
- [Wayfinder](skills/wayfinder/SKILL.md): map decisions and dependencies for broad efforts before execution.
- [Organizational Knowledge Search](skills/organizational-knowledge-search/SKILL.md): search connected internal sources and synthesize cited answers.
- [Research](skills/research/SKILL.md): investigate general external questions when no focused research workflow fits.
- [Domain Modeling](skills/domain-modeling/SKILL.md): clarify and record domain language in CONTEXT.md and decisions in ADRs.
- [REA Reverse Engineering](skills/rea-reverse-engineering/SKILL.md): inspect packaged or running software with REA and report feature behavior with evidence.
- [ML/AI Architecture](skills/ml-ai-architecture/SKILL.md): design ML/AI systems, including model lifecycle, RAG, graph/vector retrieval, and image/video pipelines.
- [Code Review](skills/code-review/SKILL.md): review TypeScript, JavaScript, Python, and Rust changes for actionable defects and spec gaps.
- [Media Platforms Code Review](skills/media-platforms-code-review/SKILL.md): apply Ads Analytics and Voltron review anchors, including FRE integration contracts.
- [Equity Research](skills/equity-research/SKILL.md): scan public stocks and investigate companies with sourced facts and explicit assumptions.
- [Portfolio Review](skills/portfolio-review/SKILL.md) *(explicit)*: run a full portfolio review as a staged pipeline of the investment roles, in parallel subagents where the host supports them.
- [Portfolio Strategy](skills/portfolio-strategy/SKILL.md): assess household risk and set portfolio policy and allocation targets.
- [Investment Research](skills/investment-research/SKILL.md): compare investment vehicles and costs, and apply sourced investor-style profiles.
- [Investment Tax Planning](skills/investment-tax-planning/SKILL.md): assess tax effects, loss harvesting, tax lots, and asset location.
- [Portfolio Maintenance](skills/portfolio-maintenance/SKILL.md): review drift, rebalancing, dividends, cash, and fees.
- [Stock Scanner Analyst](skills/stock-scanner-analyst/SKILL.md): turn scanner results into ranked candidates and conditional entry/exit plans with explicit risk scenarios.
- [News Research](skills/news-research/SKILL.md): investigate events and claims, trace reports to evidence, and build cited timelines.
- [Stanford STORM](skills/stanford-storm/SKILL.md): research topics through multiple perspectives, source-grounded questions, a synthesized outline, and citation-aware writing.
- [GitHub](skills/github/SKILL.md): route general repository, issue, and pull request work to focused workflows.
- [Git Workflow](skills/git-workflow/SKILL.md): branch names, checks before commits, rebasing, and squashing.
- [Pull Request](skills/pull-request/SKILL.md): write PR titles and bodies that follow the repository template.
- [PR review follow-up](skills/gh-address-comments/SKILL.md): inspect and address review feedback.
- [GitHub Actions CI](skills/gh-fix-ci/SKILL.md): inspect failed Actions checks and logs, then fix the observed cause when requested.
- [Publish to GitHub](skills/yeet/SKILL.md): commit, push, and open a PR when the user explicitly requests it.

## Subagents

Each subagent runs one skill in its own context, read-only, and returns a handoff record. The [Portfolio Review](skills/portfolio-review/SKILL.md) skill orchestrates them; any parent agent can also delegate to them directly.

- [portfolio-policy](agents/portfolio-policy.md): runs Portfolio Strategy for the policy stage.
- [portfolio-maintainer](agents/portfolio-maintainer.md): runs Portfolio Maintenance for drift and draft trades.
- [investment-researcher](agents/investment-researcher.md): runs Investment Research for vehicles and costs.
- [equity-analyst](agents/equity-analyst.md): runs Equity Research on one company; fan out one per ticker.
- [tax-reviewer](agents/tax-reviewer.md): runs Investment Tax Planning on the draft trade set.

A subagent declares its skill in `skills:` (Claude Code preloads it) and gives the installed `SKILL.md` path in its body, because Cursor does not document skill preloading for subagents. Read-only access is enforced per host: `readonly: true` in Cursor, and in Claude Code a `tools` allowlist of `Read, Grep, Glob, WebFetch, WebSearch`, since Claude Code ignores `readonly` and grants every tool when `tools` is omitted. In Claude Code the roles therefore have no shell, MCP integrations, file edits, or nested agents; the orchestrator supplies account data in the snapshot and runs calculators itself. The validator checks the skill path, `readonly`, and the allowlist. Codex has no subagent adapter here; Portfolio Review runs its stages in one agent there.

## Upstream catalogs

Mirrored catalogs sync daily through review pull requests. Local fixes live in `upstreams/<name>/` and are re-applied after every sync; see [upstream maintenance](docs/upstream-catalogs.md).

- [Obsidian skills](upstreams/kepano-obsidian-skills/source.json) from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills): Obsidian Markdown, Bases, CLI, JSON Canvas, Defuddle, and Knap. Installed by default.
- [Harvard ToolUniverse science skills](docs/harvard-tooluniverse.md): scientific research workflows. Installed with `--with-science`.

## Portability boundary

The skill package contains the portable workflow and its resources. Host-specific installation, tool access, permissions, and optional UI metadata belong in adapters or host setup documentation.
