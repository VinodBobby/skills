---
name: python-library-review
description: Audit an existing Python library or package as a whole for health and release readiness across distribution, public API, tests, security, documentation, supported Python versions, and CI. Use for package-wide or pre-release assessments; use code-review for a specific Python snippet, diff, branch, or pull request.
---

# Purpose

Assess whether a Python library is coherent and ready for its intended users or release. Produce prioritized, evidence-based findings. Do not modify the library during an audit.

# Workflow

## Set the audit scope

Identify the package root, import package, distribution target, supported Python versions, intended users, and requested outcome. Distinguish an overall library-health audit from a review of a specific change; route change reviews to [code-review](../code-review/SKILL.md).

Read the project configuration and the relevant source, public exports, tests, documentation, build files, and CI/release workflows. Treat the library's declared support range and established conventions as authoritative. Mark dimensions that do not apply or cannot be assessed.

## Review the library dimensions

- **Distribution and metadata:** inspect build configuration, package inclusion, runtime and optional dependencies, license metadata, and supported Python range. Check `py.typed` or wheel contents when the project distributes typed packages. Treat `src/` layout as an option, not a requirement.
- **Public API and compatibility:** inspect exported names, signatures, defaults, types, documented errors, and deprecation or compatibility policy. Check whether tests and examples exercise behavior through the public API.
- **Correctness and maintainability:** trace important input, state, resource, concurrency, async, and failure paths. Apply Python-specific review checks where relevant; read [code-review](../code-review/SKILL.md) for line-level defects.
- **Tests and CI:** assess coverage of public behavior, boundary values, and failure paths. Check that CI covers the versions and tools the project declares it supports. Use a configured coverage bar if one exists.
- **Security and dependencies:** inspect trust boundaries, secrets, dependency policy, and security checks relevant to the package's actual use. Report scan results only when a scan was run.
- **Documentation and release process:** compare installation instructions and runnable examples with the package's current API. Check changelog, licensing, build, and release steps when the project distributes releases or maintains those artifacts.

## Keep criteria project-specific

Do not impose a universal coverage percentage, `src/` layout, `__all__`, changelog, type marker, dependency pinning policy, or Python minimum. Check whether each practice is required by the package's users, distribution model, configuration, or stated policy. Treat a long time since the last commit as context, not a defect by itself. Avoid style-only findings unless project policy requires the change or it causes a concrete problem.

Run the project's configured checks only when the user requests verification or a specific result is needed to establish a finding. Read the tool configuration before choosing commands; do not assume `uv`, pytest, mypy, Ruff, or a particular coverage threshold is installed or used.

# Report

Put actionable findings first and order them by impact. For each, give a severity, affected file or dimension, concrete evidence, user impact, and the smallest useful next step. Package-level findings may cite a configuration file or missing artifact instead of a changed line. Separate assessed dimensions from findings, and say when a check was not run or evidence is unavailable. Avoid star ratings or numerical scores unless the user asks for them.
