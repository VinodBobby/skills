# Multi-factor design formula guide

Use the sample metadata to choose model terms. Confirm each term exists, has usable levels, and is not fully confounded with another term.

## Common formulas

- One factor: `~ condition`
- Batch-adjusted comparison: `~ batch + condition`
- Two factors with an interaction: `~ strain + treatment + strain:treatment`

Place the factor of interest last in an additive formula when that makes its contrast clear. Set categorical reference levels explicitly and define the contrast being tested. Do not add a batch or covariate that cannot be separated from the factor of interest in the observed design.

Before interpreting results, inspect the model terms and coefficient names. The skill's [PyDESeq2 workflow](pydeseq2_workflow.md) and [edgeR/limma workflow](edger_limma_voom.md) contain implementation examples.
