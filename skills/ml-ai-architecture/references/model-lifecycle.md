# Model Lifecycle

Use this reference when choosing a model or designing training, fine-tuning, evaluation, deployment, or monitoring.

## Choose the approach

Compare a hosted model API, a self-hosted open model, a traditional ML/CV model, retrieval, fine-tuning, and training from scratch against the task and constraints.

- Use prompting or structured outputs when the base model already performs the task well.
- Use retrieval when the model needs current, private, large, or source-cited knowledge.
- Consider fine-tuning when examples show a repeatable gap in behavior, format, or task performance and suitable training data exists.
- Consider custom training when the task, data, licensing, or measured quality gap requires a model that existing models cannot meet.
- Compare hosted and self-hosted inference using latency, throughput, data handling, availability, operational burden, and cost at expected volume.

Treat these as starting hypotheses. Choose through evaluation on representative data.

## Build a defensible data and evaluation loop

Track data source, consent or license, transformations, labels, and dataset versions. Split evaluation data to avoid leakage across users, entities, time periods, or near-duplicate samples as appropriate. Preserve a baseline and define task-specific quality, safety, latency, and cost thresholds before tuning.

For fine-tuning or training, state why the data can teach the target behavior and how the result will be compared with the baseline. Estimate dataset volume, training time, compute, checkpoint storage, and evaluation runs; size training and serving separately. Include a holdout evaluation and failure analysis. Keep prompts, preprocessing, model weights, and evaluation results versioned together.

## Plan deployment and operations

Define model and preprocessing versioning, hardware and runtime requirements, rollout strategy, rollback path, and capacity limits. Choose batch, online, streaming, edge, or embedded inference to fit latency, connectivity, privacy, and volume constraints. When containers fit, pin runtime and system dependencies, record accelerator compatibility, keep model artifacts versioned, and keep secrets outside the image.

Monitor operational signals such as latency, throughput, errors, resource use, and cost alongside quality signals such as drift, confidence, task outcomes, and human corrections. Set thresholds and an owner for retraining or rollback decisions. Check current model, hardware, and provider documentation for changing limits, licenses, and deployment support.
