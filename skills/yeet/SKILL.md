---
name: yeet
description: Publish local changes to GitHub by preparing a branch, committing the intended changes, pushing, and opening a pull request. Use only when the user explicitly requests this publishing workflow.
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
3. If on the default branch, create a descriptive `codex/<description>` branch. Otherwise use the current branch unless the user specified another branch.
4. Stage only the intended files and review the staged diff.
5. Commit with a concise message that describes the change.
6. Run relevant checks when requested or when needed to validate the change; report any checks not run.
7. Push the branch with upstream tracking.
8. Open a draft PR through an available GitHub integration or `gh pr create --draft`. Use the repository's default branch unless the user specified a base branch.
9. Summarize the branch, commit, PR, and validation results.

## Write boundaries

- This skill authorizes only the full publishing flow the user explicitly requested. Do not infer a push or PR request from a request to edit code.
- Never publish unrelated working-tree changes without confirming their scope.
- Default to a draft PR unless the user asks for a ready-for-review PR.
- If there is no accessible GitHub remote or authentication, stop before committing or pushing and explain what is missing.
- Put an accurate summary of the changes, reason, and validation in the PR description. Do not claim checks passed unless they ran.
