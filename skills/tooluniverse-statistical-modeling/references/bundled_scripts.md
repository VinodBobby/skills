## Bundled Scripts

These ready-to-run scripts live in `skills/tooluniverse-statistical-modeling/scripts/`.
Use them via the Bash tool — they are the deterministic answer for the recurring
question patterns documented above.

### `r_natural_spline_regression.py` — Natural spline regression in R

Shells out to `Rscript` to fit `lm(y ~ ns(x, df=K))` with `splines::ns()`.
Emits R², adj R², F-stat with df1/df2, overall F-test p-value, residual SE,
coefficient table (estimate, SE, t, p), and the prediction-grid peak with
95% CI from `predict.lm(..., interval='confidence')`. Supports a
`--ratio-col` shortcut to convert "a:b" string ratios into a frequency
fraction `a/(a+b)`. Refuses to write into the input CSV's parent directory.

### `spline_model_compare.py` — Quadratic vs cubic vs natural spline

Fits all three models on the same x,y in R, ranks by adjusted R², AIC, and
BIC, and emits the best model's peak (x*, y*) with 95% CI. Use for
"best-fitting model" questions and "maximum predicted y at optimal x".

### `logistic_regression_or.py` — Binary or ordinal logistic regression with ORs

Fits `sm.Logit` (binary) or `OrderedModel` (ordinal proportional-odds) and
emits ORs (`exp(coef)`) plus 95% CIs and p-values for every coefficient.
Handles label encoding (`--encode A,B,C`), explicit value maps
(`--encode-map TRTGRP:Placebo=0,BCG=1`), and interaction columns
(`--interaction A:B` -> creates `A_B = A*B`). With `--coef-name <NAME>`
also prints a SCALARS block tagged for the requested coefficient.

### `power_analysis.py` — Two-sample required-N for a t-test

Computes Cohen's d (pooled SD) from a CSV given `--value-col`, `--group-col`,
`--group-a`, `--group-b`, then `TTestIndPower.solve_power` with `--alpha`,
`--power`, `--alternative`. Use for "minimum sample size per group" power
questions. Returns both the raw and the ceil-ed N.

### `stat_tests.py` — Basic statistical tests (pure stdlib, no scipy)

Implements chi-square goodness-of-fit, Fisher's exact test, and simple linear regression
without any external dependencies. All p-values are computed from first principles using
the gamma function (chi-square) or hypergeometric enumeration (Fisher's).

```
# Chi-square goodness-of-fit
python stat_tests.py --type chi_square --observed 100,50,25 --expected 87.5,50,37.5

# Fisher's exact test (2×2 table)
python stat_tests.py --type fisher_exact --a 10 --b 5 --c 3 --d 20
python stat_tests.py --type fisher_exact --a 10 --b 5 --c 3 --d 20 --alternative greater

# Simple linear regression (OLS)
python stat_tests.py --type regression --x "1,2,3,4,5" --y "2.1,4.0,5.9,8.1,10.0"
```

Key formulas:
- `chi_square`: χ² = Σ (O−E)²/E; p-value via upper regularized incomplete gamma Q(df/2, χ²/2)
- `fisher_exact`: hypergeometric PMF; p-value = sum of probabilities ≤ P(observed)
- `regression`: b1 = Sxy/Sxx; b0 = ȳ − b1x̄; R² = 1 − SSR/SST; SE and t-statistics included

Output includes: full contingency/data table, step-by-step arithmetic, significance statement,
and a round-trip verification for each test.

When to use `stat_tests.py` vs `statsmodels`:
- Use `stat_tests.py` when you need a quick sanity check with no imports, or when the
  environment lacks scipy/statsmodels.
- Use statsmodels when you need multivariate regression, logistic models, or survival analysis.

### `format_statistical_output.py` — Format results for reporting

Utility functions to format fitted statsmodels results as publication-ready tables.
Import and call from analysis scripts; not a standalone CLI tool.

### `model_diagnostics.py` — Automated model diagnostics

Runs assumption checks (normality, heteroscedasticity, multicollinearity) on fitted models.
Import and call from analysis scripts; not a standalone CLI tool.

---
