---
name: codebase-design
description: Design structural changes to an existing codebase. Use when module responsibilities, state ownership, interfaces, or test seams need reshaping; not for greenfield systems (system-design), measured performance work (service-performance-architecture), or review of a completed diff (code-review).
---

# Codebase Design

Shape changes to existing code so callers have a clear, stable way to use the behavior and maintainers can find where it lives. Base recommendations on the repository's actual code and constraints.

## Workflow

1. **Set the scope.** Follow the user's target. Read the applicable repository instructions, relevant domain notes or ADRs, and the code paths and callers involved. Don't scan the whole repository unless asked or needed to understand the change.
2. **Trace current behavior.** Identify entry points, data flow, state ownership, dependencies, failure behavior, and the checks that describe current behavior. Separate observed friction from possible future needs.
3. **Sketch options for structural changes.** For a change that crosses a meaningful module boundary, outline two viable shapes before choosing. Include the caller-facing interface, responsibility and state owner, dependencies, and failure behavior. Skip artificial alternatives for a small or obvious change.
4. **Choose the simplest sound shape.** Prefer fewer concepts and clear ownership. Hide implementation details when doing so reduces what callers must know. Add an adapter or abstraction when a real variation or dependency seam needs it, not only for a hypothetical future.
5. **Make the design concrete.** Describe the proposed responsibilities and interfaces, the resulting flow, key trade-offs, compatibility or migration concerns, and how the expected behavior can be checked. Use a small diagram when it clarifies relationships.
6. **Match the requested work.** If asked for analysis, present the design and open decisions. If asked to implement it, stay within the requested scope and use the repository's existing implementation and verification conventions.

## Route to related skills

- New system, service, or API architecture: [system-design](../system-design/SKILL.md).
- A measured latency, throughput, or backend-load goal: [service-performance-architecture](../service-performance-architecture/SKILL.md).
- Unclear business concepts or domain boundaries: [domain-modeling](../domain-modeling/SKILL.md).
- Review of an implemented diff: [code-review](../code-review/SKILL.md).

## Output

Keep the response proportional to the task. For a design recommendation, state the evidence, proposed structure, alternatives considered, trade-offs, and verification plan. Mark assumptions and unresolved product or domain decisions.
