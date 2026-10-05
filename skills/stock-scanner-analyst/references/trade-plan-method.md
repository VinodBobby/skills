# Trade Plan Method

Use this reference when the user asks for entry or exit levels, upside/downside estimates, or risk calibration. Levels are conditional analysis, not orders.

## Establish the baseline

- Record ticker, exchange, currency, quote source, quote timestamp and timezone, and whether data are real-time or delayed.
- State the intended direction and holding period. Keep an investment thesis separate from a short-term technical setup.
- Check for earnings, court or regulator decisions, corporate actions, and other near-term events that can create gaps.

## Define the setup

- **Trigger:** the observable condition that would make the setup active, such as a close above resistance with volume confirmation.
- **Entry zone:** a range supported by the setup. Explain when to wait or abandon the entry, including a large gap or a failed confirmation.
- **Invalidation:** the price or fundamental event that would show the thesis or setup is wrong. Keep this distinct from a target and explain the basis for the level.
- **Exit plan:** give one or more targets and their basis. Include a time-based review or exit condition when relevant. If no defensible level exists, say that the level is unavailable.

## Quantify scenarios

Show bear, base, and bull cases only when the evidence supports distinct cases. For each, state the horizon, target or range, key assumptions, main risks, and confidence. Do not assign probabilities or calculate an expected value from invented weights.

For a proposed entry price `E`, target `T`, and invalidation price `S`:

- Long upside to target: `(T - E) / E × 100%`
- Long downside to invalidation: `(E - S) / E × 100%`
- Long reward/risk: `(T - E) / (E - S)`
- Short upside (gain) to target: `(E - T) / E × 100%`
- Short adverse move to invalidation: `(S - E) / E × 100%`
- Short reward/risk: `(E - T) / (S - E)`

Use positive distances in reward/risk calculations and show the prices used. If entry is a range, use conservative endpoints or show the range of outcomes. If the target or stop is not evidence-based, omit the ratio rather than imply precision.

If the user supplies a maximum dollar risk, an illustrative share count is `risk budget / per-share loss to invalidation`, rounded down. Without a user-supplied risk budget, show only per-share or percentage risk. Explain that stops may fill worse than the stop price during gaps or thin trading.

## Calibrate, do not guess

Use numeric measures when reliable data exist: ATR as a percent of price, realized volatility over a stated window, historical drawdown, liquidity, spread, and loss to invalidation. These describe different risks; do not collapse them into an unsupported probability of success.

If the user asks for a risk label, use **lower**, **moderate**, or **higher** relative to the candidates in this scan. Explain the drivers, such as volatility, leverage, liquidity, event exposure, valuation uncertainty, or conflicting evidence. Label the evidence confidence separately:

- **Higher confidence:** fresh primary data, a clear setup, and evidence that agrees across relevant measures.
- **Medium confidence:** usable data but mixed signals, meaningful assumptions, or one material gap.
- **Lower confidence:** stale or incomplete data, thin trading, event risk, or a thesis that depends on unverified assumptions.

Do not call any stock “low risk” in absolute terms. Do not treat analyst targets, model outputs, backtests, or scanner scores as forecasts of guaranteed results.

## Suggested scenario table

| Case | Trigger / price range | Return from entry | Assumptions and risks | Confidence |
|---|---|---:|---|---|
| Bear | Invalidation or downside case | Calculated or not available | Main downside drivers | Lower / medium / higher |
| Base | Most evidence-supported case | Calculated or not available | Central assumptions | Lower / medium / higher |
| Bull | Upside case | Calculated or not available | What must go right | Lower / medium / higher |

Follow the table with the entry trigger, entry zone, invalidation level, exit method, reward/risk if supportable, and source citations. Keep risks and confidence distinct from scenario labels.
