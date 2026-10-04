---
name: stanford-storm
description: Use Stanford STORM-style research and writing to create grounded, Wikipedia-like explainers, reports, outlines, or article drafts from a topic. Trigger when the user asks for STORM mode, Stanford STORM, multi-perspective research, expert-interview-style question generation, citation-backed synthesis, or a research-first outline before drafting.
---

# Stanford STORM

## Overview

Use this skill to run a STORM-inspired knowledge curation workflow: discover perspectives, ask source-grounded questions, build an outline, then draft or polish the article. Treat it as a workflow guide unless the user explicitly asks to install or run the official `knowledge-storm` package.

For exact STORM concepts and implementation notes, read [references/storm-workflow.md](references/storm-workflow.md).

## Workflow

1. Frame the topic.
   - Capture the topic, audience, geographic or time scope, target length, and citation expectations.
   - If the user did not specify details, make conservative defaults and state them briefly.

2. Build perspectives before drafting.
   - Generate 4-8 distinct research perspectives, such as technical, historical, stakeholder, economic, policy, risks, controversies, and future directions.
   - Prefer perspectives that would change the outline, not generic labels.

3. Run simulated expert interviews.
   - For each perspective, ask focused questions and follow-ups.
   - Answer only from supplied sources, browsed sources, or clearly marked assumptions.
   - Keep a source ledger with claim, source, confidence, and unresolved gaps.

4. Create the outline.
   - Organize findings into a hierarchy that would be useful for a neutral encyclopedia-style article or research report.
   - Merge duplicate sections, separate background from analysis, and include a section for limitations or open questions when evidence is mixed.

5. Draft from the outline.
   - Use neutral, evidence-led prose.
   - Cite sources for factual claims when citations are expected.
   - Do not invent citations, quotes, statistics, dates, or institutional claims.

6. Validate before finalizing.
   - Check that every major factual section has source support.
   - Flag weak, stale, conflicting, or missing evidence instead of smoothing it over.
   - For current facts, legal, medical, financial, or high-stakes topics, browse and cite reliable sources.

## Output Shapes

- For a short request, return a concise outline plus key findings and gaps.
- For "STORM mode", return sections in this order: assumptions, perspectives, source ledger, outline, draft, gaps.
- For a full article request, return the article first if the user prioritizes the deliverable, then a compact source and gap appendix.
- For user-provided sources, ground the work in those sources first and only browse when the user asks or the topic requires current verification.

## Official Package Use

If the user asks to run official Stanford STORM rather than apply STORM mode, inspect the current official repository or package docs first. Running it may require installing `knowledge-storm`, configuring an LLM provider, and configuring a retrieval provider such as Bing, You.com, Brave, Tavily, Google, Azure AI Search, SearXNG, DuckDuckGo, Serper, or a vector retriever.
