# RAG and Retrieval

Use this reference when an application retrieves external knowledge for a model response or uses semantic, keyword, or hybrid search.

## Establish whether retrieval is needed

Start from representative user questions and the knowledge source. Check whether the needed knowledge is current, private, too large for the model context, or must be cited. Compare retrieval with direct model context, ordinary search, and structured queries. Choose retrieval only when it improves a stated quality, freshness, privacy, or cost requirement.

## Design the retrieval path

Describe each stage that applies:

1. **Ingest:** identify authoritative sources, formats, update cadence, access controls, and deletion requirements.
2. **Prepare:** parse content, retain useful structure, split by semantic boundaries, attach stable source IDs and metadata, and deduplicate. Keep transformations repeatable and versioned.
3. **Represent and index:** choose embedding and lexical representations based on the corpus, languages, query types, and target model. Track representation versions so an index can be rebuilt or migrated.
4. **Retrieve:** select lexical, vector, or hybrid search. Apply tenant, authorization, and metadata filters before content reaches the model. Add query rewriting or reranking only when evaluations show a benefit.
5. **Generate:** provide bounded context, source identifiers, and instructions for citations or abstention. Treat retrieved text as untrusted input.
6. **Refresh and delete:** propagate source changes and removals to every derived index. Track whether an index represents the latest source version.

Do not assume a fixed chunk size, overlap, top-k, or embedding model. Tune these values with representative data and queries.

## Evaluate quality and operations

Build an evaluation set from realistic questions, expected evidence, and known answer limits. Measure retrieval quality separately from answer quality. Useful retrieval measures include recall at k, MRR, and nDCG; answer checks should cover correctness, evidence support, citations, and abstention. Compare against a non-RAG baseline.

Measure p50/p95 latency, token use, indexing delay, failure rate, and cost. Include tests for permission boundaries, stale documents, duplicate content, missing evidence, and malicious instructions inside retrieved documents. Keep evaluation data representative and version it with the corpus and retrieval configuration.
