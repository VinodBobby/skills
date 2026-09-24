# Graph and Vector Storage

Use this reference when selecting a retrieval store or deciding whether graph and vector search should work together.

## Start with queries and system of record

Write representative queries first. Identify what is authoritative in the system of record and what can be rebuilt as a search index. Separate transactional records, files, lexical indexes, embeddings, and graph relationships when they have different update or access patterns.

Choose the smallest set of stores that satisfies the query and operating requirements. A vector index is useful for semantic nearest-neighbor retrieval. A graph store is useful when queries depend on explicit entities, relationships, or multi-hop traversal. Full-text or relational queries may already solve the problem. Combine methods when tests show each adds useful evidence.

## Decide when GraphRAG fits

Use GraphRAG when the query needs relationship-aware retrieval, such as joining facts across entities or traversing multiple hops. Define the graph schema, entity resolution rules, source provenance, and update process before choosing a graph database. Evaluate extraction errors and whether graph structure improves answers on real questions.

Graph and vector retrieval can complement each other: vector search can find semantically relevant entities or passages, while graph traversal can add related facts. Keep the retrieval path explainable enough to show which passages, nodes, and edges supported an answer.

## Compare candidate stores

Compare options against:

- Existing infrastructure and team operating experience
- Query semantics, filters, hybrid search, and metadata needs
- Corpus size, dimensions, vector count, update rate, QPS, and latency targets
- Consistency, deletion, tenancy, backup, restore, and data residency
- Index build time, migration path, model-version compatibility, and rebuild cost
- Deployment mode, availability, monitoring, scaling limits, and total cost

If a relational database already meets the workload, compare its vector extension with a dedicated vector service using the same data and evaluation queries. Do not treat embeddings as canonical records; retain source data and provenance.

## Validate with workload evidence

Test realistic queries, including exact terms, semantic paraphrases, filters, multi-hop relations, and no-match cases. Measure retrieval quality and end-to-end latency at expected scale. Include ingestion, update, deletion, backup, restore, and tenant isolation in the operational plan. Use vendor documentation for current capabilities and limits after narrowing the candidates.
