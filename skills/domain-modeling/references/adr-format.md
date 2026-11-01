# ADR format

Store ADRs in `docs/adr/` (or the context's own `docs/adr/` for context-specific decisions) as `0001-slug.md`, `0002-slug.md`, and so on. Take the next number after the highest existing one.

```md
# {Short title of the decision}

{One to three sentences: the context, what was decided, and why.}
```

A single paragraph is often enough. The value is recording that a decision was made and why.

Add these only when they help a future reader:

- **Status**: proposed, accepted, deprecated, or superseded by ADR-NNNN.
- **Considered options**: when the rejected alternatives are worth remembering.
- **Consequences**: when downstream effects are not obvious.

## What qualifies

Record a decision only when it is hard to reverse, surprising without context, and the result of a real trade-off. Typical examples:

- architectural shape, such as an event-sourced write model;
- integration patterns between contexts;
- technology choices with real lock-in;
- ownership and boundary decisions, including explicit exclusions;
- deliberate deviations from the obvious approach;
- constraints that the code cannot show, such as compliance or partner contract limits.
