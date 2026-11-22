---
name: github
description: Triage GitHub repositories, issues, pull requests, and review context. Use for general GitHub help, then route review follow-up, Actions failures, or publishing work to the matching specialist skill.
---

# GitHub

Use the GitHub integration when the host provides one. Otherwise use the authenticated `gh` CLI and local Git context. State which capability is unavailable when neither can handle a requested operation.

## Route the work

- General repository, issue, or pull request triage: handle it here.
- Review threads and requested changes: read [gh-address-comments](../gh-address-comments/SKILL.md).
- Failing GitHub Actions checks: read [gh-fix-ci](../gh-fix-ci/SKILL.md).
- Branch publishing, commit, push, and pull request: read [yeet](../yeet/SKILL.md).

## Workflow

1. Resolve the repository and item from the user's request or local Git context. Ask for the repository when it remains unclear.
2. Use the available GitHub integration when it supports the requested operation. If shell access is needed, use `gh-axi` when it is already available and supports the task; otherwise use the authenticated `gh` CLI. Do not install a CLI or session hook as part of ordinary triage.
3. Route to a specialist once the task is clearly review follow-up, Actions debugging, or publishing.
4. Keep reads separate from writes. Comment, resolve a review, change labels, commit, push, or open a PR only when the user requested that action.
5. Summarize what you inspected, changed, and could not verify.

When using `gh-axi`, check its concise help for the command's current fields and flags. Treat an explicit zero result differently from a failed read. If a mutation succeeded but its readback failed, inspect current state before retrying so a completed write is not duplicated. The same status and retry discipline applies when using another GitHub interface.

## Capability boundaries

- A GitHub integration is optional. Do not assume a particular app, plugin, or connector exists.
- GitHub Actions status and logs may require `gh`, even when a GitHub integration is available.
- Do not claim that GitHub data or a local branch was inspected if the required access is unavailable.
