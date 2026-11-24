# STORM Analysis: Goldman Sachs GS Quant skill

**Reviewed:** 2026-11-24

**Scope:** Assess Goldman Sachs' public GS Quant agent skill and backtesting materials for fit in this portable skills repository. The goal is to add useful coding guidance, not reproduce the video's reported strategy results or grant access to Goldman services.

## Assumptions

- The transcript refers to the official [`goldmansachs/gs-quant`](https://github.com/goldmansachs/gs-quant) repository and its [`gs-quant-overview` skill](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/skills/gs-quant-overview/SKILL.md), which links to `backtesting.md`.
- The desired integration is an installable skill for agents working with GS Quant and historical backtests.
- The transcript's reported win rates and annualized return are claims to assess, not verified benchmark results. No data, code, trading assumptions, or result files were supplied for reproducing them.

## Perspectives and questions

| Perspective | Question | Finding |
| --- | --- | --- |
| Task fit | What repeatable job does the Goldman skill help with? | It guides agents writing `gs_quant` code across sessions, instruments, pricing, risk, datasets, and backtesting. The backtest guide maps strategies into triggers, actions, and calculation engines. |
| Repo overlap | Do our existing finance skills already cover this job? | `equity-research` covers company diligence, `stock-scanner-analyst` covers scanner-based plans, and `portfolio-review` coordinates household reviews. None guides implementation or troubleshooting of GS Quant backtests. |
| Access and data | Does a free skill provide free GS pricing or data access? | No. The library is public and installable, but GS API calls require client credentials and entitlements. The official guide lists `PredefinedAssetEngine` for custom order-based backtests with predefined assets. Engine choice and data requirements need to be checked for the actual use case. |
| Backtest design | What design ideas are useful outside a Goldman-specific setup? | Separate a trigger from its action; carry positions through dates; define sizing and entry/exit costs; inspect trade ledgers, cash, live marks, drawdown, and P&L components. Skip an engine when a fixed portfolio can be priced directly. |
| Reliability | What can silently invalidate a result? | Data timing, missing dates, universe selection, and position treatment can change results. At review time, GS Quant issue #375 described a bad fill-forward/interpolation result for a missing date when a plain `datetime.date` index was used; PR #376 remained open. |
| Maintenance | Should we mirror the entire upstream documentation? | The upstream skill already has detailed references and may change. A short local workflow with direct links preserves the useful decisions without copying a second full API manual into this repo. |

## Source ledger

| Claim | Source | Confidence and limit |
| --- | --- | --- |
| Goldman publishes an official `gs-quant-overview` skill with a backtesting guide. | [Official skill](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/skills/gs-quant-overview/SKILL.md), [backtesting guide](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/skills/gs-quant-overview/backtesting.md) | High; files are in the public Goldman Sachs repository. |
| GS Quant is a public Python toolkit, while API access requires credentials available to Goldman institutional clients. | [Official repository README](https://github.com/goldmansachs/gs-quant#gs-quant) | High for the published access statement; individual API entitlements vary. |
| The backtest model separates strategy, trigger, action, and engine; the guide recommends direct historical pricing for a fixed hold with no position management. | [Official backtesting guide](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/skills/gs-quant-overview/backtesting.md), [developer guide](https://developer.gs.com/docs/gsquant/pricing-and-risk/backtesting/) | High for documented design. Exact API support is version-dependent. |
| GS Quant documents a `PredefinedAssetEngine` for custom order-based backtests with predefined assets and lists a dedicated example notebook. | [Official guide](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/skills/gs-quant-overview/backtesting.md), [official documentation index](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/documentation/README.md), [example notebook](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/documentation/04_backtesting/examples/01_PredefinedAssetEngine/040100_simple_example.ipynb) | High for the documented engine and the example's existence; inspect the notebook and installed version before implementing. |
| Backtest summaries expose performance, drawdown, trade, cash, and transaction-cost information; entry and exit costs can be configured. | [Official backtesting guide](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/skills/gs-quant-overview/backtesting.md) | High for the documented outputs and models; does not establish realistic costs for a particular asset or venue. |
| A date-indexed `GenericDataSource` can return a wrong forward-filled value for missing dates and mutate its input series. | [Official issue #375](https://github.com/goldmansachs/gs-quant/issues/375), [fix PR #376](https://github.com/goldmansachs/gs-quant/pull/376) | High for issue reproduction; issue and PR status checked on 2026-11-24. Recheck before relying on this warning. |
| The transcript's win rates and return are not established by the skill documentation. | Supplied transcript compared with the official skill and backtesting guide | High; results could not be reproduced because the transcript provides no data, code, execution rules, or complete universe methodology. |

## Synthesis and incorporation

Add a focused first-party [`gs-quant` skill](../skills/gs-quant/SKILL.md) to the default skill collection. It routes agents to the official source for API details and adds the operational rules this repository needs: separate the library from credentials and data entitlements, select the engine by data path, model timing and costs explicitly, inspect positions and drawdowns, and check for the currently reported missing-date issue when using `GenericDataSource`.

Keep it separate from equity research and portfolio-review skills. Those answer investment-analysis requests; this skill helps implement and validate code. Link to the current upstream docs instead of copying the full API manual, which keeps source attribution clear and reduces drift.

The new skill is listed in the repository README and uses the normal default install path. It adds no package dependency, credentials, or runtime integration.

## Gaps

- The supplied transcript does not include source code, price files, universe snapshots, cost assumptions, or a reproducible benchmark. The performance claims remain unverified.
- No controlled before/after task benchmark was run for this skill; the environment cannot isolate otherwise identical agent runs with the skill enabled and withheld.
- The official `PredefinedAssetEngine` example notebook should be checked against the user's installed `gs-quant` version before using it with a particular market-data provider.
