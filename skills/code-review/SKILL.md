---
name: code-review
description: Review Python snippets and changed Python code, diffs, branches, pull requests, and working trees for actionable correctness, security, and regression issues against the request and repository conventions. Also review changed TypeScript, JavaScript, and Rust code. Use python-library-review for whole-package health or release-readiness audits.
---

# Purpose

Find defects introduced by a code change and report evidence the author can verify.

# Workflow

## Set the review scope

Use the base revision, branch, pull request, or files named by the user. If the comparison point is unclear and changes outside the requested scope could affect the result, ask before reviewing. Read the repository's applicable agent instructions, coding standards, and relevant specification. Treat repository conventions as authoritative.

## Trace changed behavior

Inspect the full diff and enough surrounding code to follow inputs, callers, outputs, and failure paths. Check whether the implementation preserves existing behavior.

When an originating issue, ticket, or specification is available, compare the change with it: requirements that are missing or only partly met, behavior that was not requested, and acceptance criteria without a matching test. Report spec gaps as findings with the requirement quoted; skip this check when no spec exists. Inspect relevant tests and project configuration when they clarify expected behavior. Focus on issues the change introduces; skip unrelated pre-existing problems.

Apply language-specific checks where they matter:

- **TypeScript and JavaScript:** check boundary validation, null and undefined handling, type narrowing, coercion, async error paths, unhandled promises, shared mutation, serialization, and module or runtime compatibility.
- **Python:** distinguish required dictionary keys from optional keys and falsey values; use direct indexing or explicit boundary validation only when the contract requires a key, and reserve `.get()` for optional values with safe defaults. Check mutable defaults and class state, broad or swallowed exceptions, resource cleanup, async boundaries, and subprocess or path handling. When operator dunders change, check unsupported operands against `NotImplemented`/reflected dispatch and check augmented-assignment return behavior against the type's contract. Flag discarded list comprehensions only when their unused allocation has a concrete performance impact. For package changes, inspect public API compatibility, supported Python versions, and import-time dependency cost; preserve intentional lazy imports for optional or heavy dependencies.
- **Rust:** check error propagation, panic paths such as `unwrap` on fallible input, ownership and lifetime assumptions, `unsafe` invariants, concurrency and lock behavior, feature flags, and trait or type constraints.
- **Across languages:** check API compatibility, authorization and validation boundaries, resource limits, concurrency, and failure recovery when relevant to the diff.

Use judgment. Do not report a pattern merely because it appears on a checklist. Confirm its behavior and user impact in context. Treat style preferences as findings only when the repository requires them or they cause a concrete defect.

## Validate each finding

For every candidate issue, confirm that the changed lines cause it and identify a realistic trigger and consequence. Check whether nearby validation, callers, tests, or documented conventions already address it. Exclude speculative risks and issues caught by tooling unless they point to a real behavior problem.

Do not modify code during a review. Run checks only when the user requests them or when a specific result is needed to establish a finding.

# Report

Put actionable findings first. For each, include a severity, a concise title, a precise file and line, the condition that triggers it, and its effect. Use the repository's severity scheme when it has one; otherwise use P1 for serious functional or security failures, P2 for ordinary defects, and P3 for limited impact.

If you find no actionable issues, say so and summarize the scope reviewed. State any meaningful limit, such as missing source context or unavailable runtime checks. Keep findings separate from optional suggestions.
