---
name: gs-quant
description: Write or troubleshoot Python that uses Goldman Sachs' gs_quant library for instruments, market data, pricing, risk, or strategy backtests. Use for GS Quant API and backtest engine tasks, not general stock research or portfolio reviews.
---

# GS Quant

Use the official [GS Quant skill](https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/skills/gs-quant-overview) and [backtesting guide](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/skills/gs-quant-overview/backtesting.md) as the API reference. Check the installed `gs-quant` version and current docs before using methods whose signatures or behavior may have changed.

## Set the access and data path

- The Python package is open source and can be installed with `pip install gs-quant`. Installation does not grant Goldman Sachs API credentials or market-data entitlements. Calls to GS services need an authenticated `GsSession` and the required access.
- Never ask the user to paste client secrets into chat or source files. Use an authorized environment or secret store. If access is unavailable, explain which API calls cannot run and keep any offline work separate from GS service results.
- For an unchanged holding or fixed portfolio with no triggers, rebalancing, or hedging, use historical pricing directly instead of adding a backtest engine.
- For changing positions, model a `Strategy` with triggers and actions, then check which engine supports it. `GenericEngine` runs GS Quant instruments and risks; `EquityVolEngine` is optimized for a limited server-side equity-volatility workflow; `PredefinedAssetEngine` is the route to investigate for preloaded custom assets and price series. Follow the current official examples for the installed version.
- A `GenericDataSource` can provide a market series to trigger logic. Do not assume that this alone supplies historical instrument prices to every engine. For external data such as Massive, identify the exact engine and data adapter that consumes it, and label the provider and data transformations in the output.

## Build the backtest

1. Record the instrument or asset universe, data source, date range, currency, frequency, price-adjustment policy, trading calendar, and starting capital.
2. Define the trigger separately from its action. Triggers include schedules, dates, market levels, and strategy-risk thresholds. Actions can add, scale, hedge, rebalance, or close positions.
3. State the signal observation time and execution time. Avoid using a close to generate a signal and also assume execution at that same close unless the data and order model justify it.
4. Make position sizing explicit. Keep signal frequency separate from P&L evaluation frequency. Check trigger and action order where multiple actions occur on the same date.
5. Set entry and exit costs. Use supported transaction-cost models for fixed, size-based, risk-based, or combined costs. Add spread and slippage assumptions when the chosen engine does not model them.
6. Run a short date range first. Check missing dates, fills, open positions, cash, and trade history before running a full period.

## Review results and data integrity

- Inspect the trade ledger and the result series, including live position value, cash from closed trades, transaction costs, and total P&L. Review drawdown and drawdown duration, return and volatility, and the full-period benchmark on matching dates. A high win rate alone does not establish a robust strategy.
- For multi-asset or equity-universe tests, document how the universe was formed at each historical date. Avoid survivorship and look-ahead bias; do not use current constituents as if they were known in the past.
- Check corporate-action adjustments, stale or missing observations, fills on non-trading dates, and whether open positions at the end of the test are marked consistently.
- For `GenericDataSource` with missing dates, test the installed version's fill-forward and interpolation behavior. As of 2026-11-24, upstream [issue #375](https://github.com/goldmansachs/gs-quant/issues/375) reported an end-of-series fill error for a plain `datetime.date` index and mutation of the input series; the related [fix PR #376](https://github.com/goldmansachs/gs-quant/pull/376) was still open. Convert the index to `pandas.DatetimeIndex`, pass a copy of the series, and include a missing-date regression check until the fix is confirmed in the installed version.
- Treat backtest output as historical analysis, not a forecast or evidence that a strategy will make money live. State unverified assumptions and do not place or stage trades.

## Official references

- [GS Quant repository and requirements](https://github.com/goldmansachs/gs-quant)
- [GS Quant developer backtesting guide](https://developer.gs.com/docs/gsquant/pricing-and-risk/backtesting/)
- [PredefinedAssetEngine example notebook](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/documentation/04_backtesting/examples/01_PredefinedAssetEngine/040100_simple_example.ipynb)
- [GS Quant skills directory](https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/skills/gs-quant-overview)
