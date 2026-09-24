---
name: gh-fix-ci
description: Diagnose failing GitHub Actions checks for a pull request and implement a focused fix when requested. Use for failed Actions checks and logs; report other CI providers without treating them as GitHub Actions.
---

# GitHub Actions CI

Use `gh` to inspect check status and logs. A GitHub integration may provide PR metadata, but do not assume it exposes Actions logs.

## Requirements

- `gh` installed and authenticated with repository and workflow read access.
- A repository and PR number or URL, or a local branch with an associated PR.
- Python 3 only when using the bundled `scripts/inspect_pr_checks.py` helper.

## Workflow

1. Verify `gh auth status` and resolve the PR.
2. Inspect failing checks with the bundled script when available. From this skill's directory, run:
   `python scripts/inspect_pr_checks.py --repo <repo-path> --pr <number-or-url>`
   Add `--json` for machine-readable output. If the PR is associated with the current branch, omit `--pr`.
3. If needed, use `gh pr checks` and `gh run view` to inspect check details and logs. Adapt requested JSON fields to those supported by the installed `gh` version.
4. For each failed check, report its name, URL, and a concise relevant log excerpt. Identify missing logs and uncertain causes.
5. If the check is not a GitHub Actions run, report its provider and URL. Do not investigate another provider as if it were Actions.
6. If the user asked to fix the failure, implement a focused local change tied to the observed cause. Otherwise give a focused proposed fix.
7. Recheck relevant local behavior and report what still needs a rerun on GitHub.

## Guardrails

- Do not infer root cause from a check name alone. Use the log or state what evidence is missing.
- Do not change workflow configuration or application code unrelated to the failing check.
- Do not commit, push, or rerun remote workflows unless the user asks for those actions.
- Report clearly when authentication, permissions, or missing logs block inspection.
