---
name: stock-scanner-analyst
description: Turn backend scanner results into ranked equity candidates and conditional entry/exit plans with explicit upside, downside, and risk. Use for scanner-driven stock selection and trade-plan requests.
---

# Stock Scanner Analyst

Build a traceable watchlist and conditional, risk-aware plans from the user's criteria and an available stock scanner. Treat scanner hits as research candidates, not as buy or sell signals. Present conclusions as general research, not personalized investment advice.

## Workflow

1. **Set the scope.** Identify the market and security universe, long or short bias, strategy, and holding period. Use the user's filters. Ask only for missing details that would materially change the scan or plan; otherwise state reasonable assumptions.

2. **Check the data path.** Inspect the available integrations for the user's scanner or market-data backend and follow its current documentation. Use read-only access. Record the provider, fields, market session, quote latency, and scan time. Do not claim a live backend scan if no scanner is connected. If none is available, say so and ask for a connection or scanner output. Use a public-data scan only when its coverage and freshness are adequate, and label its limits.

3. **Run and report a reproducible scan.** Translate the request into explicit filters. Record the universe, exclusions, filter values, and number of matches. Do not silently relax filters to produce candidates. Exclude or flag stale, incomplete, illiquid, or inconsistent data. Rank candidates on visible criteria; do not hide judgment in an unexplained composite score.

4. **Assess finalists.** Check trend, liquidity, volatility, upcoming events, and the fundamental factors relevant to the user's strategy. Verify material company facts against regulatory filings, earnings releases, exchange disclosures, or investor-relations materials. Use current market data for price levels and technical claims. Label reported figures, estimates, scanner outputs, and calculations separately. When a separate equity-research workflow is available, use it for deeper fundamental diligence.

5. **Build conditional plans.** For each finalist, give a trigger and entry zone, the setup that would invalidate the idea, one or more exit targets, and an expected review horizon. Tie each level to sourced price data, support/resistance, volatility, a measured move, or a stated valuation method. Do not invent exact levels when the evidence does not support them. Treat stop prices as intended risk limits, not guaranteed execution prices; gaps and low liquidity can cause larger losses.

6. **Calibrate risk.** Compare downside to the invalidation level with upside to each target. Use recent volatility, ATR, drawdown history, average volume, bid-ask spread, and upcoming events when data are available. Explain missing inputs. Give numeric probabilities only when a relevant, described model or backtest supports them; otherwise use qualitative confidence and explain why.

7. **Close with evidence and uncertainty.** Cite or link current sources near the claims they support. State what could change the ranking or invalidate each plan. Do not promise returns, imply certainty, or place, stage, or modify trades.

## Requirements

- Never invent scanner access, current prices, volume, company facts, or source citations. Use only tools and data that are actually available.
- Timestamp market data and state whether it is real-time, delayed, or historical. For price-level analysis, include currency and exchange when available.
- Do not send or stage orders, modify a portfolio, or create external alerts. A request for stock ideas or levels is not permission to act in an account.
- Keep findings proportional to the request. For a scan, report scope, data source and as-of time, filters, exclusions, match count, and a ranked candidate table. For finalists, include entry, invalidation, exit, scenario returns, risk drivers, confidence, sources, and open questions.

## Resources

Use the scenario math and output structure in [references/trade-plan-method.md](references/trade-plan-method.md) when the user asks for entry/exit levels, upside/downside estimates, or risk calibration.
