---
name: research
description: Answer a general external question with source comparison and a short cited synthesis. Use only when no specialist fits; not for internal knowledge (organizational-knowledge-search), news or contested claims (news-research), stocks (equity-research), long-form articles (stanford-storm), or biomedical questions (tooluniverse skills).
---

# Research

Investigate the question the user asked, then report what the evidence supports and where it remains uncertain. Use current search for facts that may have changed. Prefer original sources such as official documentation, standards, papers, datasets, filings, and direct statements. Use high-quality secondary sources to add context or find primary evidence.

## Scope

Use this for general external research when no focused workflow fits. Route to the specialist when one matches, even if it is not installed on this machine; say so instead of silently broadening this skill:

- Organization-specific systems, processes, or decisions: `organizational-knowledge-search`.
- Current events, breaking news, or contested claims: `news-research`.
- Public companies, stocks, or valuation: `equity-research`.
- A Wikipedia-style article or report built from multiple perspectives: `stanford-storm`.
- Diseases, drugs, genes, or other biomedical questions: the `tooluniverse` router or `tooluniverse-literature-deep-research`.

## Workflow

1. Define the question, relevant scope, and any date or decision constraints.
2. Identify the source types that can establish the answer. Search for primary sources first and inspect the source itself before relying on a search snippet.
3. Compare sources when the claim is consequential, disputed, or likely to have changed. Check publication dates and whether multiple reports rely on the same underlying source.
4. Separate established facts from interpretation, estimates, and unresolved points. Mark inferences as inferences.
5. Write the answer around the question, with citations next to the supported claims. Include material limits and unanswered questions without implying the search was exhaustive.

Save findings as a Markdown artifact when the user requests one or when the research will support ongoing work. Follow the repository's existing location and format. For a direct question, a concise cited answer in the conversation is enough. Delegate independent research only when it improves coverage and the available tools and task rules permit it.
