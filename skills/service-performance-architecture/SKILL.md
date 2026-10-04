---
name: service-performance-architecture
description: Design or restructure backend services where response latency, throughput, or backend load are key goals. Use for service architecture decisions and major performance refactors; focus on measured bottlenecks and end-to-end request paths.
---

# Service Performance Architecture

Design for responsiveness by removing wasted work from the critical path and keeping resource use bounded. Optimize the whole request flow, not an isolated component.

## Workflow

1. **Set a measurable target.** Define the latency percentiles, throughput, error rate, or backend load that should improve. Trace representative requests end to end and separate queueing, CPU work, network waits, cache access, and downstream calls. Confirm the bottleneck before proposing a structural change.
2. **Reduce work before adding concurrency.** Find duplicate fetches, repeated cache round trips, unnecessary payload fields, redundant transformations, and writes on the response path. Prefer memoization, batching, pipelining, or local slicing when they remove work outright.
3. **Design the request path.** Keep async I/O async end to end. Batch independent work within explicit limits. Scope memoization to one request and use cache identities that preserve resource and transformation boundaries. Move opportunistic writes off the response path and coalesce them where possible.
4. **Make cache and overload behavior explicit.** Define the source of truth, cache key, freshness, invalidation, stale behavior, and stampede control. Bound queues and connection pools. Choose what can be dropped, what must be preserved, and how saturation fails.
5. **Keep shared flow centralized.** Put common fetch, cache, mutation, and memoization behavior in one reusable path. Expose narrow hooks for backend-specific differences. Use a full override only when the behavior truly differs, and make that difference clear.
6. **Verify against the target.** Compare before and after using the same workload. Check tail latency, event-loop or worker lag, cache hit rate, downstream request count, pool waits, and error rates as relevant. Test cache collisions, invalidation, concurrent misses, partial failures, and pagination boundaries.

## Design principles

- Prefer fewer, larger, bounded operations over many small awaited operations.
- Use request-local memoization to collapse duplicate work without leaking values across requests or loader namespaces.
- Separate cached data, freshness, and refresh coordination. A stale-while-revalidate lease can limit a refresh to one worker while other requests use acceptable stale data.
- Treat cache writes as an optimization only when the source of truth can safely refill them. Preserve correctness-critical invalidations even when write queues are under pressure.
- Measure CPU work on async event loops. Serialization, compression, and parsing can make an apparently slow network call a symptom of loop starvation.
- Size pools and timeouts from observed concurrency. A bounded, visible failure is easier to diagnose than silent queueing.
- Keep data boundaries cacheable. Stable resource identifiers, flat resource records, and explicit references make targeted caching and invalidation easier.
- Keep performance changes compatible and reversible. State any API changes, rollout stages, and rollback conditions.

For concrete examples of these principles in Voltron, read [Voltron performance patterns](references/voltron-patterns.md). Treat the examples as design evidence, not fixed implementation requirements.

## Architecture output

Include the baseline and bottleneck, a request-flow diagram or sequence, the batching and cache design, concurrency and failure limits, correctness invariants, and a measurement plan with expected results. Call out migration and rollback steps when they affect clients or persisted cache data.
