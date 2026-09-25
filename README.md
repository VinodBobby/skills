# Portable Agent Skills

This repository develops reusable agent skills that can move across machines and supported agent environments.

## Design

See [Portable skill design](docs/portable-skill-design.md) for the design principles, package shape, and validation approach.

## Starting a skill

Use [the skill template](templates/skill/SKILL.md) as a starting point. Keep each skill focused on one repeatable workflow. Add references, scripts, or assets only when they support that workflow.

## Skills

- [Product UI](skills/product-ui/SKILL.md): design and implement polished, responsive interfaces with complete interaction states and accessible defaults.
- [Figma Design](skills/figma-design/SKILL.md): create or revise product screens in Figma using its available design system and integration.
- [Diagram Design](skills/diagram-design/SKILL.md): create evidence-based flowcharts, architecture diagrams, sequences, state machines, and data models.
- [Obsidian Markdown](skills/obsidian-markdown/SKILL.md): edit vault notes while preserving Obsidian links, embeds, callouts, and properties.
- [Obsidian Bases](skills/obsidian-bases/SKILL.md): create and review Obsidian Base definitions and views.
- [Obsidian CLI](skills/obsidian-cli/SKILL.md): perform scoped operations on a live Obsidian vault through its CLI.
- [Document Editing](skills/document-editing/SKILL.md): revise reports and office documents while preserving meaning and structure.
- [PDF Workflow](skills/pdf-workflow/SKILL.md): inspect, create, and make authorized edits to PDFs with page-level checks.
- [System Design](skills/system-design/SKILL.md): design systems and evaluate architectural decisions. Synced from [Anthropic's upstream skill](skills/system-design/UPSTREAM.md).
- [ML/AI Architecture](skills/ml-ai-architecture/SKILL.md): design ML/AI systems, including model lifecycle, RAG, graph/vector retrieval, and image/video pipelines.
- [Code Review](skills/code-review/SKILL.md): review TypeScript, JavaScript, Python, and Rust changes for actionable defects against the request and repository conventions.
- [Equity Research](skills/equity-research/SKILL.md): scan public stocks and investigate companies with sourced facts and explicit assumptions.
- [News Research](skills/news-research/SKILL.md): investigate events and claims, trace reports to evidence, and build cited timelines.
- [Harvard ToolUniverse science skills](docs/harvard-tooluniverse.md): upstream-synced catalog of scientific research workflows.
- [GitHub](skills/github/SKILL.md): route general repository, issue, and pull request work to focused workflows.
- [PR review follow-up](skills/gh-address-comments/SKILL.md): inspect and address review feedback.
- [GitHub Actions CI](skills/gh-fix-ci/SKILL.md): inspect failed Actions checks and logs, then fix the observed cause when requested.
- [Publish to GitHub](skills/yeet/SKILL.md): commit, push, and open a PR when the user explicitly requests it.

## Portability boundary

The skill package contains the portable workflow and its resources. Host-specific installation, tool access, permissions, and optional UI metadata belong in adapters or host setup documentation.
