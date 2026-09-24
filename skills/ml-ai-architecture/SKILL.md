---
name: ml-ai-architecture
description: >-
  Design or review ML/AI systems, including model selection, RAG, graph/vector
  retrieval, model lifecycle, and image/video pipelines. Use for architecture,
  sizing, deployment, evaluation, or scalability decisions.
---

# ML/AI Architecture

Design ML- and AI-powered workloads around their data, quality targets, operational limits, and existing stack. Use this skill for ML/AI-specific architecture; use a general system-design skill when the wider application architecture is also in scope.

## Workflow

1. **Understand the workload.** Inspect the repository and identify its languages, frameworks, current models, data stores, deployment shape, and operational conventions. Clarify the task, input and output modalities, batch or real-time needs, quality, latency, throughput, availability, privacy, compliance, budget, and hardware constraints. Separate known facts from assumptions. Ask only for missing facts that change the design.
2. **Choose the ML/AI approach.** Compare hosted models, self-hosted models, traditional ML or computer vision, prompting, retrieval, fine-tuning, and training from scratch as relevant. Prefer the least complex approach that can meet measured quality and operating targets. Read [model lifecycle](references/model-lifecycle.md) when model development or fine-tuning is in scope.
3. **Design the data and retrieval path.** Trace data from source through preparation, indexing or feature generation, inference, persistence, and user-visible output. Read [RAG and retrieval](references/rag-and-retrieval.md) for knowledge-grounded generation; read [graph and vector storage](references/graph-and-vector-storage.md) when selecting or combining search stores.
4. **Handle media workloads explicitly.** For image or video input, include decode and preprocessing, model inference, metadata, storage, and retrieval as needed. Read [image and video pipelines](references/image-and-video-pipelines.md) for those branches.
5. **Size and operate the design.** Estimate throughput, concurrency, tokens or media volume, storage growth, latency, accelerator needs, and cost from stated assumptions. Identify what benchmark or prototype would confirm the estimate. Describe deployment, scaling, security, data/model versioning, observability, quality monitoring, rollback, and ownership. Correlate traces with model, prompt, preprocessing, and retriever versions while limiting sensitive payload capture. Fit the deployment to the target environment; do not assume a cloud, container, GPU, or orchestration platform.
6. **Compare and communicate.** Compare only alternatives that materially change quality, cost, complexity, or operations. Recommend one approach and explain its trade-offs. Include a system/data-flow diagram, assumptions, risks, capacity estimates, and a validation plan. Record durable decisions as an ADR when the repository uses ADRs.

## Requirements

No particular framework, cloud provider, database, model vendor, or runtime is required for architecture work. When a recommendation depends on changing product capabilities, pricing, limits, licenses, or API behavior, consult current first-party documentation for the selected stack. Keep provider-specific guidance conditional.

## Resources

- For document or knowledge retrieval, read [RAG and retrieval](references/rag-and-retrieval.md).
- For graph databases, vector databases, or hybrid storage, read [graph and vector storage](references/graph-and-vector-storage.md).
- For computer vision or video analytics, read [image and video pipelines](references/image-and-video-pipelines.md).
- For model selection, training, fine-tuning, or production model operations, read [model lifecycle](references/model-lifecycle.md).
