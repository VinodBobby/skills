# CONTEXT.md format

A `CONTEXT.md` is a glossary for one bounded context. It is not a spec, a scratch pad, or a place for implementation decisions.

```md
# {Context name}

{One or two sentences on what this context covers and why it exists.}

## Language

**Order**:
A customer's request to buy one or more products.
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request
```

## Rules

- Pick one term per concept and list rejected synonyms under `_Avoid_`.
- Define what the term is in one or two sentences, not what the code does with it.
- Include only terms specific to this domain. General programming concepts do not belong, even when the code uses them heavily.
- Group terms under subheadings when natural clusters appear; a flat list is fine otherwise.

## Several contexts

When the repository has more than one bounded context, keep a `CONTEXT-MAP.md` at the root:

```md
# Context map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md): receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md): issues invoices and processes payments

## Relationships

- **Ordering → Billing**: Ordering emits `OrderPlaced`; Billing consumes it to issue an invoice
```
