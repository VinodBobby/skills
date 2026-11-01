---
name: domain-modeling
description: Clarify and record a project's domain terms, relationships, and boundaries in CONTEXT.md and ADRs. Use when business language is ambiguous, the domain model is changing, requirements and code disagree, or a CONTEXT.md or ADR needs writing; not for merely reading the glossary.
---

# Domain Modeling

Build a shared model of the problem domain while discussing or designing the work. Focus on the meaning of the concepts and their relationships, including those that live outside the codebase. Reading an existing glossary for vocabulary is a habit, not this skill; use this skill when the model changes.

## Find the model

- If `CONTEXT-MAP.md` exists at the repository root, it lists several bounded contexts and where each `CONTEXT.md` lives. Infer which context the topic belongs to, and ask when unclear.
- Otherwise use the root `CONTEXT.md` when it exists.
- Follow an existing glossary or ADR location if the repository already has one instead of introducing these files.
- Create files lazily: a `CONTEXT.md` when the first term is settled, `docs/adr/` when the first ADR is needed.

## Clarify the model

- Check the existing glossary, specifications, and relevant behavior before introducing new terms.
- When the user uses a term that conflicts with the glossary, say so right away and ask which meaning is intended.
- Identify overloaded words and propose one precise term. Ask the user to resolve ambiguity when the distinction affects behavior or scope.
- Test concept boundaries, lifecycle, ownership, and relationships with concrete scenarios and edge cases.
- Compare claims about how the domain works with code, data, and documentation. Surface conflicts and ask which source is authoritative when evidence cannot resolve them.
- Record each settled term in `CONTEXT.md` when it is settled, not in a batch at the end. Use [the CONTEXT.md format](references/context-format.md). Keep the glossary free of implementation details.

## Record decisions carefully

Offer an ADR only when a decision is hard to reverse, surprising without context, and the result of a real trade-off. If any of the three is missing, skip it. Use [the ADR format](references/adr-format.md) unless the repository has its own.

Do not silently settle a user-owned business rule. Present the concrete scenarios and ask for the decision when the evidence and existing rules do not determine it.
