# Coordinated portfolio review

Use this workflow when the user requests a review that combines strategy, investment research, tax, and maintenance. It is a process for an available host or agent, not a scheduler, data service, or trading integration.

1. **Start and freeze inputs.** A user request, host schedule, or meaningful event starts a run. Record a run ID, portfolio snapshot ID or timestamp, data as-of times, jurisdiction and tax year, goals, constraints, accounts, positions, cash, and available lots. Record missing data and refresh stale inputs before relying on them.
2. **Set policy.** Apply portfolio strategy to produce or confirm targets, ranges, liquidity needs, and restrictions. Preserve an existing approved policy unless a change is proposed and reviewed.
3. **Research vehicles.** Apply investment research to compare eligible holdings or alternatives against the policy. Use the existing equity-research skill for company due diligence when it is available. Treat any requested investor profile as a research lens.
4. **Model maintenance.** Apply portfolio maintenance to calculate drift and draft cash, dividend, rebalancing, and fee actions, including no action. Mark trades as preliminary until tax review.
5. **Review tax.** Apply investment tax planning to the proposed trades and account placement. State which tax-lot and household data are missing. Feed material changes back to the affected role for one review round; then present any unresolved conflict.
6. **Check and report.** Confirm that tax review applies to the final proposed trades and snapshot; if they changed after review, send them back or mark them unreviewed. Use available calculation and rule tools to check constraints, holdings, cash, lot availability, costs, and data freshness. Present choices with portfolio effects, estimated taxes and costs, assumptions, sources, unresolved issues, and the reason for any preferred option. Stop before account changes or orders unless those actions are explicitly authorized.

## Handoff record

Each role returns the same run and snapshot identifiers, its data timestamps and sources, relevant constraints, proposed action or no-action option, expected portfolio and tax effects where known, calculations or assumptions, confidence, missing inputs, and unresolved questions. Mark a conclusion blocked when its required data are missing. Preserve the record and surface conflicts rather than averaging agent opinions.

Keep handoffs containing private profile details in a location authorized for that information; do not write them into a public repository by default.

If a specialist skill, calculator, integration, or separate-agent capability is unavailable, state that limitation and perform the supported work with the available information. Do not claim a tool, agent, check, or schedule ran when it did not.
