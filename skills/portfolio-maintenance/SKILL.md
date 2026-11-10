---
name: portfolio-maintenance
description: Review a portfolio for allocation drift, rebalancing, dividends, cash, and fees. Use for scheduled or event-driven portfolio maintenance and proposed actions.
---

# Portfolio Maintenance

Compare current holdings with the user's approved policy and produce a reviewable maintenance proposal. A schedule or event can request a review; this skill does not create a schedule or monitor accounts by itself.

## Workflow

1. Gather the policy targets and allowed ranges, dated holdings and prices, cash balances, accounts, planned contributions and withdrawals, dividend settings, fee data, and current restrictions. Record missing or stale information.
2. Calculate current exposures and drift across the household, including fund overlap where data permit. Distinguish a policy breach from a smaller deviation and use the user's stated review or rebalance thresholds.
3. Compare no action, available cash flows, dividend routing, and potential trades where relevant. Show the resulting allocation, liquidity, costs, and assumptions. Route proposed sales and replacements for tax review before presenting a combined recommendation.
4. Review idle cash against near-term obligations, settlement needs, liquidity, available sweep choices, yield, fees, and product risks. Do not assume a higher yield protects purchasing power or that cash vehicles have identical protections.
5. Flag material fees and changed share-class eligibility for investment research. Compare a proposed replacement with the cost and tax impact of the change.
6. Report proposed actions, priority, conditions, data dates, calculations, sources, and unresolved issues. In a portfolio-review run, return the handoff record from the brief. Record the next review trigger when the user or host provides one.

## Requirements

Use current read-only account and market data or dated user-provided inputs. Prefer deterministic calculators for exposures and costs. If a required calculation, tax review, account feature, or data source is unavailable, mark the affected action conditional. A maintenance proposal does not authorize account changes or orders.
