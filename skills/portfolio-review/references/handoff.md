# Handoff contract

Every role in a portfolio-review run receives a brief and returns one handoff record. The orchestrator writes each record to the run directory unchanged.

## Brief

Send this to the role agent, or use it as the stage prompt in a single-agent run.

```markdown
# Brief: <role> for run <run_id>

Snapshot: <snapshot_id>, as of <timestamp>. Path: <run-dir>/snapshot.md
Upstream records: <paths, for example policy.md>
Scope: <the question for this stage; for equity-analyst, one ticker>
Jurisdiction and tax year: <values>
Investor profiles: <requested names and their source: public catalog or the user's private location; or none>
Boundary: read-only analysis and proposals. Account changes and orders are out of scope.

<Paste the snapshot and upstream records here when the role cannot read the run directory.>

Return one handoff record in the format below and nothing else.

<Paste the record format below.>
```

## Record

```markdown
---
run_id: <from brief>
snapshot_id: <from brief>
role: policy | maintenance | research | equity | tax
status: complete | conditional | blocked
confidence: lower | medium | higher
data_as_of:
  <source>: <timestamp>
proposed_actions:
  - id: <role>-<n>, or equity-<ticker>-<n>
    action: no-action | buy | sell | exchange | redirect-cash | change-dividends | policy-change
    account: <account>
    security: <ticker or fund>
    amount: <shares, value, or percent>
    depends_on: [<action ids>]
missing_inputs: []
open_questions: []
---

## Reasoning

Why each proposed action follows from the policy and evidence. Include the no-action comparison.

## Expected effects

Portfolio exposure, estimated tax, and cost effects where known. Mark unknown effects.

## Calculations and assumptions

Inputs, formulas or tool output, and each assumption.

## Sources

Each source with its as-of date.
```

## Rules

- `blocked` means a required input is missing; list it under `missing_inputs`. `conditional` means the result holds only under stated assumptions.
- A role states conflicts with an upstream record in `open_questions` and keeps its own evidence. The orchestrator presents conflicts; it does not average them.
- Action IDs are unique within the run and stay stable across revision rounds, so the tax review can be matched to the final trades. Equity records include the ticker from the brief's scope, as in `equity-MSFT-1`, because several equity agents share the role.
