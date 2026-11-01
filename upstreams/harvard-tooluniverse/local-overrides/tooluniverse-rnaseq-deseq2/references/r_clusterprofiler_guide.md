# Comparing gseapy and R clusterProfiler results

The [enrichment analysis guide](enrichment_analysis.md) documents the gseapy workflow. Results from gseapy and R clusterProfiler may differ when their inputs or methods differ.

Before comparing results, check that both analyses use the same:

- gene identifiers and identifier mapping;
- gene set collection and version;
- background or universe;
- enrichment test and multiple-testing adjustment;
- significance threshold and term-simplification rules.

For exact reproduction, follow the R code and package versions used by the source analysis. Do not treat matching pathway names as proof that the p-values are directly comparable.
