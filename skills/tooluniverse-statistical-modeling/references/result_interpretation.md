## Reasoning Framework for Result Interpretation

### Evidence Grading

| Grade | Criteria | Example |
|-------|----------|---------|
| **Strong** | p < 0.001, effect size clinically meaningful, model assumptions met | OR = 3.5 (95% CI: 2.1-5.8), p < 0.001, Hosmer-Lemeshow p > 0.05 |
| **Moderate** | p < 0.05, reasonable effect size, minor assumption concerns | HR = 1.8 (95% CI: 1.1-2.9), p = 0.02, borderline PH test |
| **Weak** | p < 0.05 but wide CI, small effect, or assumption violations | OR = 1.2 (95% CI: 1.01-1.43), p = 0.04, VIF > 5 for a covariate |
| **Insufficient** | p >= 0.05, or model fails convergence/diagnostics | Non-significant coefficient with model separation warning |

### Interpretation Guidance

- **Model diagnostics (R-squared)**: For OLS, R-squared > 0.7 indicates good fit in biomedical data; 0.3-0.7 is moderate. Adjusted R-squared penalizes added predictors. For logistic models, use pseudo-R-squared (McFadden > 0.2 is acceptable) and AUC (> 0.7 = acceptable, > 0.8 = good discrimination).
- **AIC/BIC for model comparison**: Lower is better. AIC difference > 10 between models is strong evidence for the lower-AIC model. BIC penalizes complexity more heavily than AIC, preferring simpler models. Use AIC for prediction-focused selection, BIC for inference.
- **Coefficient significance thresholds**: Report exact p-values rather than just significance stars. For multiple predictors, apply Bonferroni or FDR correction. A coefficient with p = 0.049 in a model with 20 predictors is likely a false positive without correction.
- **Survival analysis HR interpretation**: HR > 1 means increased hazard (worse outcome) for the exposed group. HR = 2.0 means twice the instantaneous risk of the event. Always verify the proportional hazards assumption -- if violated, the HR is an average over time and may be misleading. Report median survival times alongside HRs for clinical interpretability.
- **Odds ratio interpretation**: OR = 1.0 means no association. OR > 1 indicates increased odds. The 95% CI excluding 1.0 confirms significance. For rare outcomes, OR approximates relative risk; for common outcomes (> 10% prevalence), OR overstates the relative risk.
- **Confounding assessment**: Compare crude vs adjusted ORs/HRs. A change > 10% in the effect estimate after adjusting for a covariate suggests confounding by that variable.

### Synthesis Questions

1. Do the model diagnostics (residual plots, Hosmer-Lemeshow, PH test) support the validity of the chosen model, or do assumption violations require alternative approaches (e.g., robust standard errors, stratified models)?
2. For adjusted models, does the inclusion of confounders change the primary effect estimate by more than 10%, indicating meaningful confounding?
3. Are the reported effect sizes (OR, HR, coefficients) clinically meaningful in addition to being statistically significant, considering the scale of the predictor and outcome?
4. When comparing nested models via AIC/BIC, does the more complex model provide substantially better fit, or is the simpler model preferred by parsimony?
5. For survival analysis, is the proportional hazards assumption met throughout the follow-up period, or do Schoenfeld residuals suggest time-varying effects?

---
