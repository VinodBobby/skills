# Voltron performance patterns

These examples come from implemented Voltron changes. They show the reasoning behind useful patterns; they do not make Voltron's exact stack or settings universal.

## Simplify cache access before switching to async

Voltron reduced request-path work with request-local read memoization, packed cache values, and deferred/coalesced writes before completing its async Redis migration. This avoided turning many small cache commands into many small awaits. Async I/O helped once the hot path had fewer, more useful operations.

When designing an async migration, first count and simplify the operations on the critical path. Then make network I/O non-blocking end to end. Do not assume that adding `async` to a high-round-trip flow makes it faster.

## Keep memoization scoped and semantically correct

Voltron's loader memoization is request-scoped and namespaced by loader and resource. Separate loaders can return different transformed shapes for the same backend ID, so sharing one memo entry can return the wrong value or skip a required mutator. Memoize the final shape under the identity that owns it.

For any request cache, define the full identity: tenant or caller scope, loader or data source, resource type, key, and any transformation that changes the value. Test same-ID collisions across loaders.

## Reduce cache round trips and separate coordination

Voltron packs resource data and freshness metadata together and stores a resultset as one packed value. A separate short-lived lease coordinates stale refreshes. Fresh data returns directly; acceptable stale data can return while one lease holder refreshes it.

Prefer a small number of cache calls, but keep data, freshness, and refresh ownership conceptually separate. Preserve versioning, expiration, invalidation, and a hard stale limit. Use stale responses only when product semantics allow them.

## Defer and bound non-critical writes

Voltron collects cache write intents during a request, groups them by Redis client, and flushes them through pipelines after the response. The queue has a bound: low-value cache sets can be dropped during pressure, while deletes needed for correctness are retained. Flush depth and dropped writes are observable.

Apply this pattern only when a missed write can be refilled safely. Bound pending work, report what was dropped, and never make invalidation best-effort if stale data would violate correctness.

## Respect async client lifetime and event-loop health

Long-lived async Redis pools can bind to an event loop. Voltron workers keep a persistent loop for message processing; creating and closing a loop for each message can leave a reused client attached to a closed loop. The service also measures event-loop lag so CPU-bound parsing or compression can be distinguished from slow Redis.

Match client lifetime to loop lifetime. Measure loop lag alongside downstream spans. Offload CPU work only when profiling shows it blocks useful I/O.

## Centralize loader invariants behind narrow hooks

Voltron's base loader owns the shared fetch, cache, mutation, and memoization path. Backend-specific argument translation, endpoint selection, and response extraction use explicit hooks. Subclasses no longer copy the whole pipeline just to change one step; full overrides remain for real semantic differences.

In a service architecture, centralize cross-cutting invariants and make variation points explicit. Keep separate implementations only when they preserve a distinct behavior such as cache identity, cache writes, or a single-resource shortcut.

## Reuse cached data for pages

Voltron slices a cached ranked result for offset/limit pagination, preserving the total count used to detect the end of a client scroll. This avoids making another backend request for each page. It also removed a redundant deep copy after a preceding helper had already returned an owned copy.

Local pagination works when the full result is bounded, fresh enough, and already cached. Preserve total-count and ordering semantics, establish mutation ownership, and avoid repeated upstream reads. Use backend pagination when full-result caching is too large or too stale.

## Tune limits from measurements

Voltron made Redis pool size and timeout configurable, then lowered defaults after observing async request concurrency. Shorter pool waits expose saturation instead of letting requests queue silently. The values are service-specific; derive them from concurrency, workload, and latency targets.

Use pool wait, queue depth, timeout, event-loop lag, cache hit/miss, and backend span metrics to find the actual constraint. Keep only metrics that answer a decision or diagnose a failure, and compare like-for-like workloads.
