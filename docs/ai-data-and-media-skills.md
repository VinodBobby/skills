# RAG, Graph, Vector, Image, and Video Skills

**Reviewed:** 2026-09-23
**Purpose:** Find maintained Agent Skills that can inform this repository's planned ML/AI architecture guidance.

## Summary

There are strong task-specific skills for RAG, graph databases, vector databases, computer vision, and video analytics. The strongest candidates are vendor- or framework-specific. I did not find one mature, portable skill that selects architecture across all these domains.

Keep the planned ML/AI architecture skill provider-neutral. Use it to clarify workload, data modality, quality, latency, scale, privacy, deployment, and budget. Then route to an optional framework, database, cloud, or accelerator skill after choosing the stack. Treat public skills as implementation references, not defaults for every project.

## Candidate skills

| Area | Candidate | What it covers | Main limit |
| --- | --- | --- | --- |
| RAG workflows | [LangChain `langchain-rag`](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/langchain-rag/SKILL.md) | Document loading, chunking, embeddings, vector stores, retrieval, and a basic RAG agent. | Uses LangChain and example providers/stores; its parent repository labels itself early development. |
| RAG applications | [Weaviate Agent Skills](https://github.com/weaviate/agent-skills) | Basic, advanced, and agentic RAG examples; multimodal PDF ingestion; hybrid search; database workflows. | Uses Weaviate and its application stack. |
| Vector search architecture | [Qdrant Skills](https://github.com/qdrant/skills) | Sizing, scaling, search quality, hybrid search, monitoring, deployment, multi-tenancy, and embedding-model migration. The Qdrant Advisor retrieves current guidance live. | Qdrant-specific; live Advisor use needs network access. |
| Vector database operations | [Pinecone Agent Skills](https://github.com/pinecone-io/skills) | Index onboarding, semantic search, Assistant, full-text search, CLI/MCP, and related application workflows. | Pinecone-specific; some workflows require an account, API key, CLI, or MCP. |
| Vector database operations | [Milvus Skill](https://github.com/zilliztech/milvus-skill) | Collection and vector CRUD, indexes, hybrid/full-text search, RBAC, and RAG patterns. | Milvus and PyMilvus-specific. |
| Graph data and GraphRAG | [Neo4j Agent Skills](https://github.com/neo4j-contrib/neo4j-skills) | Graph modeling, Cypher, document-to-graph import, vector indexes, GraphRAG retrievers, graph analytics, drivers, and Aura. | Neo4j-specific. |
| Graph data and GraphRAG | [Memgraph Skills](https://github.com/memgraph/skills) | Graph modeling, Cypher, algorithms, indexes, and GraphRAG ingestion and hybrid retrieval. | Memgraph-specific and a smaller skill collection. |
| Image and vision | [NVIDIA Agent Skills](https://github.com/nvidia/skills) | Task-specific workflows for image embeddings, computer vision, model onboarding, evaluation, fine-tuning, and deployment. | Best aligned with NVIDIA software and GPU workflows; inspect individual skill, model, and product licenses. |
| Video analytics | [NVIDIA DeepStream skills](https://github.com/NVIDIA/DeepStream/tree/main/skills) and [Video Search and Summarization skills](https://github.com/nvidia/skills) | Video pipeline construction/profiling, vision model deployment, multi-stream analytics, archived video ingestion/search, and summarization. | NVIDIA DeepStream/VSS stack; GPU, Docker, service, and model requirements vary. |
| Multimodal API use | [Google Gemini API skill](https://github.com/google/skills/blob/main/skills/cloud/gemini-api/SKILL.md) | API examples for image/video/audio input, bounding-box detection in images/video, generation/editing, embeddings, and model tuning. | Google API and model-specific; it is not a general media-pipeline architecture guide. |

Sources: the skill repositories and skill files linked in the table. Their maintainers describe current coverage and requirements in those repositories.

## Local availability check

The repository currently has no dedicated RAG, graph/vector database, computer-vision, or video-pipeline skill. The machine has Vercel AI SDK and AI Gateway guidance, plus a Vercel AI architect agent profile and Adobe photo/video editing skills. Those cover AI app integration or creative editing; they do not provide provider-neutral ML pipeline architecture. Vercel storage guidance mentions pgvector and Pinecone as options, but is not a database-selection skill.

## Implemented skill

The repository now includes a portable [ML/AI Architecture skill](../skills/ml-ai-architecture/SKILL.md). It has focused references for RAG and retrieval, graph/vector storage, image/video pipelines, and model lifecycle. The core stays vendor-neutral and routes to current first-party documentation when the target stack is known.

The public skills in this survey remain optional implementation references: LangChain or Weaviate for RAG examples, Qdrant for vector sizing/operations, Neo4j for graph/GraphRAG, and NVIDIA DeepStream/VSS for NVIDIA video workloads. Use Google Gemini guidance when the chosen workload uses its multimodal APIs.

## Source links

- [LangChain Skills](https://github.com/langchain-ai/langchain-skills)
- [Weaviate Agent Skills](https://github.com/weaviate/agent-skills)
- [Qdrant Skills](https://github.com/qdrant/skills)
- [Pinecone Agent Skills](https://github.com/pinecone-io/skills)
- [Milvus Skill](https://github.com/zilliztech/milvus-skill)
- [Neo4j Agent Skills](https://github.com/neo4j-contrib/neo4j-skills)
- [Memgraph Skills](https://github.com/memgraph/skills)
- [NVIDIA Agent Skills](https://github.com/nvidia/skills)
- [NVIDIA DeepStream skills](https://github.com/NVIDIA/DeepStream/tree/main/skills)
- [Google Gemini API skill](https://github.com/google/skills/blob/main/skills/cloud/gemini-api/SKILL.md)
