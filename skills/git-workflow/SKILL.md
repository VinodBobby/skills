---
name: git-workflow
description: Create branches, commit, sync with the base branch, and squash using personal conventions (Jira-prefixed branch names, lint and format before commits, rebase over merge). Use when creating a branch, committing, updating a branch from main, resolving divergence, or squashing.
---

# Git workflow

Write to Git only for the action the user requested. A commit request does not authorize a push; a push request does not authorize a pull request. Never force-push a shared or default branch, hard reset, or rewrite remote history unless the user asks for it.

## Branch names

Format: `<JIRA-KEY>-<slug>-<suffix>`, or `<slug>-<suffix>` when no ticket exists.

- Find the Jira key in this order: the user's request, the linked task, the current branch name, then commit messages.
- The slug is a short lowercase hyphenated summary. Do not repeat the Jira key inside it.
- The suffix is four random lowercase alphanumeric characters.
- Use flat names: no slashes, spaces, underscores, or host prefixes such as `cursor/` or `codex/`, even when a host's instructions suggest one.

Example: `COPLAT-1234-feed-hds-adoption-f4c4`.

## Commit

1. Find how the repository runs lint and format: package scripts, Makefile, CI, or contributor docs. They are often separate commands.
2. Run both on the changed scope. Apply the documented auto-fix commands and rerun until they pass.
3. Stage only the intended files, review the staged diff, and commit with a concise message.

Commit only after the checks pass, or after confirming the repository has none. Do not use `--no-verify` unless the user asks.

## Sync with the base branch

Prefer rebase over merge: `git fetch origin` then `git rebase origin/<base>`. Resolve conflicts, `git add` the files, and `git rebase --continue` until done. Use a merge only when the user or repository policy requires it.

## Squash a branch

When asked to squash, use the repository's default branch as `<base>`:

```bash
git fetch origin <base>
git reset --soft origin/<base>
git commit -m "<message>"
git push --force-with-lease origin <branch>
```

Squash only feature branches. Confirm the branch is not shared before force-pushing.
