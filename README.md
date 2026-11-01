# Portable Agent Skills

This repository develops reusable agent skills that can move across machines and supported agent environments.

## Install

```bash
git clone https://github.com/VinodBobby/skills.git ~/Projects/skills
~/Projects/skills/install.sh
```

The installer links each skill directory into `~/.agents/skills` (Codex, Cursor) and `~/.claude/skills` (Claude Code, Cursor), and links [global/AGENTS.md](global/AGENTS.md) to `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`, and `~/.gemini/GEMINI.md`. Because these are links, `git pull` updates every harness. Same-name copies already in those locations, including legacy copies in `~/.codex/skills`, move to `~/.skills-backup/<timestamp>/`.

| Flag | Effect |
| --- | --- |
| *(none)* | First-party skills and the Obsidian catalog |
| `--with-optional` | Adds skills listed in [profiles/optional.txt](profiles/optional.txt) |
| `--with-science` | Adds the Harvard ToolUniverse catalog |
| `--all` | Both of the above |
| `--no-memory` | Leaves global instruction files alone |
| `--dry-run` | Prints the actions without changing anything |
| `--uninstall` | Removes every link into this repository |

Rerun the installer after adding or removing a skill. Add a target directory to `SKILL_TARGETS` in [install.sh](install.sh) for another harness, such as `~/.gemini/skills`.

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
- [Stock Scanner Analyst](skills/stock-scanner-analyst/SKILL.md): turn scanner results into ranked candidates and conditional entry/exit plans with explicit risk scenarios.
- [News Research](skills/news-research/SKILL.md): investigate events and claims, trace reports to evidence, and build cited timelines.
- [Stanford STORM](skills/stanford-storm/SKILL.md): research topics through multiple perspectives, source-grounded questions, a synthesized outline, and citation-aware writing.
- [GitHub](skills/github/SKILL.md): route general repository, issue, and pull request work to focused workflows.
- [Git Workflow](skills/git-workflow/SKILL.md): branch names, checks before commits, rebasing, and squashing.
- [Pull Request](skills/pull-request/SKILL.md): write PR titles and bodies that follow the repository template.
- [PR review follow-up](skills/gh-address-comments/SKILL.md): inspect and address review feedback.
- [GitHub Actions CI](skills/gh-fix-ci/SKILL.md): inspect failed Actions checks and logs, then fix the observed cause when requested.
- [Publish to GitHub](skills/yeet/SKILL.md): commit, push, and open a PR when the user explicitly requests it.

## Upstream catalogs

Mirrored catalogs sync daily through review pull requests. Local fixes live in `upstreams/<name>/` and are re-applied after every sync; see [upstream maintenance](docs/upstream-catalogs.md).

- [Obsidian skills](upstreams/kepano-obsidian-skills/source.json) from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills): Obsidian Markdown, Bases, CLI, JSON Canvas, Defuddle, and Knap. Installed by default.
- [Harvard ToolUniverse science skills](docs/harvard-tooluniverse.md): scientific research workflows. Installed with `--with-science`.

## Portability boundary

The skill package contains the portable workflow and its resources. Host-specific installation, tool access, permissions, and optional UI metadata belong in adapters or host setup documentation.
