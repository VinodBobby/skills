---
name: yeet
description: Publish local changes to GitHub by preparing a branch, committing the intended changes, pushing, and opening a pull request. Use only when the user explicitly requests this publishing workflow.
disable-model-invocation: true
---

# Publish Changes to GitHub

Use this workflow only when the user explicitly asks to publish changes, such as committing and pushing them or opening a pull request.

## Requirements

- A local Git repository with an accessible GitHub remote.
- `gh` installed and authenticated, unless an available GitHub integration can complete the requested PR operation.
- A clear understanding of which changes belong in the publication.

## Workflow

1. Inspect `git status -sb`, the current branch, remotes, and the diff.
2. If unrelated or unexplained changes are present, ask which files belong in the requested publication. Do not stage them by default.
3. If on the default branch, create a branch named by the [git-workflow](../git-workflow/SKILL.md) conventions. Otherwise use the current branch unless the user specified another branch.
4. Run the repository's lint and format checks on the changed scope and fix what they report; report any checks not run.
5. Stage only the intended files and review the staged diff.
6. Commit with a concise message that describes the change.
7. Push the branch with upstream tracking.
8. Open a draft PR following the [pull-request](../pull-request/SKILL.md) skill. Use the repository's default branch unless the user specified a base branch.
9. Summarize the branch, commit, PR, and validation results.

## Write boundaries

- This skill authorizes only the full publishing flow the user explicitly requested. Do not infer a push or PR request from a request to edit code.
- Never publish unrelated working-tree changes without confirming their scope.
- Default to a draft PR unless the user asks for a ready-for-review PR.
- If there is no accessible GitHub remote or authentication, stop before committing or pushing and explain what is missing.
- Put an accurate summary of the changes, reason, and validation in the PR description. Do not claim checks passed unless they ran.
