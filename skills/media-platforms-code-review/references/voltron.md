# Voltron review guide

Apply these checks to changes in `Media-Platforms/voltron`, a GraphQL service backed by loaders, resources, caches, and downstream services.

## Schema and resolver design

- Treat GraphQL field, argument, type, and error behavior as public contracts. Check existing query compatibility, deliberate naming, deprecation or migration needs, and query examples for API-visible changes.
- Prefer established `Resource`, `Loader`, `Mutator`, and field patterns over custom resolver logic that repeats loading, normalization, cache, or exception handling.
- Check that loader construction and backend work preserve batching and request-local behavior.

## Cache and backend behavior

- Trace cache identity, loader namespaces, request-local memoization, metadata ownership, freshness, and invalidation. Look for collisions between resources that share an ID.
- Prefer batched or pipelined cache access when it fits existing patterns. Keep cache values and freshness or coordination metadata understandable and debuggable.
- For new filters or fetch paths, check whether clients can trigger broad scans, repeated requests, or unbounded work. Look for indexing, scope, batching, or performance evidence.

## Operations and verification

- For deployment, workflow, or global setting changes, check whether behavior is configurable, reversible, and coordinated with dependent services. Make temporary behavior explicit.
- Match tests and verification to risk. Loader, cache, schema, and async changes need targeted failure-mode coverage; API changes benefit from concrete queries; risky deploy changes may need stage or feature validation.
- For complex cache or architecture changes, check for human-readable documentation that explains the problem and the reason for the design. Do not ask for narrative docs on routine changes.
