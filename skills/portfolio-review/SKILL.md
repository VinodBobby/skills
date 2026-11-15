---
name: portfolio-review
description: Run a coordinated household portfolio review as a staged pipeline of policy, research, maintenance, and tax roles, using separate subagents when the host supports them. Use when the user explicitly asks for a full or multi-agent portfolio review.
disable-model-invocation: true
---

# Portfolio Review

Coordinate one review run. You are the orchestrator: you freeze the inputs, brief each role, record each handoff, merge the proposals, and report. The roles analyze and propose. The run stops before account changes or orders unless the user explicitly authorizes them.

## Pipeline

| Stage | Role agent | Role skill | Starts after | Mode |
| --- | --- | --- | --- | --- |
| 1. Intake | orchestrator | none | user request or host schedule | sequential |
| 2. Policy | `portfolio-policy` | portfolio-strategy | 1 | gate |
| 3a. Maintenance | `portfolio-maintainer` | portfolio-maintenance | 2 | parallel |
| 3b. Vehicle research | `investment-researcher` | investment-research | 2 | parallel |
| 3c. Company diligence | `equity-analyst`, one per company | equity-research | 2 | parallel, only for individual stocks in scope |
| 4. Merge | orchestrator | none | all of 3 | sequential |
| 5. Tax | `tax-reviewer` | investment-tax-planning | 4 | gate |
| 6. Revision | affected role | its skill | 5 | at most one round |
| 7. Verify and report | orchestrator | none | 6 | sequential |

1. **Intake.** Agree a private run directory with the user, outside any public repository. Write `snapshot.md` with a run ID, snapshot ID or timestamp, data as-of times, jurisdiction and tax year, goals, constraints, accounts, positions, cash, available lots, an approved policy if one exists, and any requested investor profiles with their source. Refresh stale inputs before relying on them. The stage is done when every field has a value or appears under `missing_inputs`.
2. **Policy.** Brief `portfolio-policy` and write its record to `policy.md`. The role preserves an approved policy unless it proposes a reviewed change. If the record is `blocked`, ask the user for the missing inputs before continuing.
3. **Fan out.** Brief 3a, 3b, and each 3c in parallel, in batches within the host's concurrent subagent limit. When the limit is unknown, use batches of at most 5. Start 3a and 3b in the first batch. If a launch fails on the limit, wait for running agents to finish before launching it again. The stage is done when every role and ticker has a record. Write the records to `maintenance.md`, `research.md`, and `equity-<ticker>.md`. If the maintenance record flags fee or share-class issues that the research record does not cover, resume `investment-researcher` once with those items.
4. **Merge.** Combine the proposed actions into one draft set in `proposal.md`, including no action. Confirm every action ID is unique; send a record with a duplicate ID back to its role before continuing. Mark every trade preliminary. Where roles disagree, record each position and its evidence side by side.
5. **Tax.** Brief `tax-reviewer` with the snapshot, policy, and draft set. Write its record to `tax.md`.
6. **Revision.** If the tax record materially changes a trade, resume the affected role once with the tax record. Send changed trades back to `tax-reviewer`. Carry remaining conflicts to the report as unresolved.
7. **Verify and report.** Confirm that the tax review covers the final trades and snapshot; mark any other trade unreviewed. Check constraints, holdings, cash, lot availability, costs, and data freshness with available calculators or rule tools. Write `report.md` and present the choices with portfolio effects, estimated taxes and costs, assumptions, sources, unresolved issues, and the reason for any preferred option.

## Briefs and handoffs

Each subagent starts with a clean context and sees only its brief. Role agents can read files and the web but cannot run shell commands or account integrations, so put every account, lot, and market input they need in the snapshot, and run calculators yourself in stages 4 and 7. Build every brief and read every record with [the handoff contract](references/handoff.md). A record with status `blocked` stops the stages that depend on it.

## Without subagents

If the host cannot run subagents, or the user asks for one agent, run the same stages in order in this context. For each stage, read the role skill, write its handoff record, and continue. Run the stage 3 roles one after another. State in the report that the run used one agent.

## Requirements

Use read-only account and market integrations or dated user-provided data. Keep calculations in available tools or show verifiable arithmetic. Keep the run directory and any private investor profiles in a location the user authorized. If a role skill, agent, calculator, or integration is unavailable, state the limitation and continue with the supported work. Report only the agents, checks, and tools that actually ran.
