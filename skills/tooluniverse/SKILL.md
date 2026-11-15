---
name: tooluniverse
description: "Route biology, chemistry, and medicine data or analysis requests to the relevant ToolUniverse tools and skills. Use for scientific lookups, file analysis, or computational workflows."
when_to_use: "Activate when the user provides data files to analyze, asks about differential expression, runs statistical tests on clinical data, performs variant analysis, does pathway enrichment, builds phylogenetic trees, or asks any scientific research question."
paths: "*.csv,*.xlsx,*.tsv,*.vcf,*.fa,*.fasta,*.faa,*.h5ad,*.rds,*.bam"
---

# ToolUniverse

Use this as a short router. Load only the specialist needed for the request.

## Workflow

1. Match the question and supplied files to a specialist using the available skill inventory and descriptions.
2. If descriptions are unavailable or leave a real ambiguity, read the [routing table](references/routing-table.md).
3. Load the selected skill with the host's native skill mechanism. If the host has no skill loader, read the package's `SKILL.md`.
4. Read [general strategies](references/general-strategies.md) only when no specialist matches or the user asks for a custom multi-skill workflow.

## Analysis

- Before writing code for supplied data, check for `*_executed.ipynb`. Use ToolUniverse `read_executed_notebook` or the host's equivalent to inspect relevant cell outputs; treat a matching published result as authoritative instead of recomputing it. Also check for a canonical script or published pipeline and prefer it over scratch files.
- Prefer an existing ToolUniverse tool or bundled helper for repeated tasks. Write custom analysis when no suitable helper exists.
- For quick lookups, make one to three targeted calls. For calculations, run the code and report the source, assumptions, units, and result.
- State denominators, scales, and ratio direction when they can change the answer. For ambiguous "ratio between A and B" wording, report both directions; match percent/proportion formatting to the request. For PhyKIT saturation, use column 2 (`1-slope`), not column 1 (`slope`).
- Prefer the most specific scientific skill over a general or setup skill when the request names a domain problem.
- If the available skill descriptions and routing table leave a consequential ambiguity, ask the user which path they want.
