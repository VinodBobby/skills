---
name: pull-request
description: Write or update a GitHub pull request title and body, following the repository's PR template when one exists. Use when opening a PR, editing a PR description, or preparing a branch for review.
---

# Pull request

Open or update a pull request only when the user asks. Default to a draft unless the user asks for ready-for-review.

## Gather context

Resolve the base branch (the repository default unless specified), then inspect the branch:

```bash
git --no-pager log "origin/$BASE"..HEAD --oneline
git --no-pager diff "origin/$BASE"... --stat
```

Read local conventions in this order and let them override the defaults below: `.github/PULL_REQUEST_TEMPLATE.md`, `CONTRIBUTING.md`, `AGENTS.md` or `CLAUDE.md`, then recent merged PRs.

## Title

Use the repository's convention. Otherwise: `PROJECT-123: short imperative description`, lowercase after the colon unless a proper noun, under about 72 characters. Find the issue key from the user's request, the branch name, commit messages, or the task context. Without an issue, write a short imperative title and say in the body that no issue is linked.

## Body

If `.github/PULL_REQUEST_TEMPLATE.md` exists, it is the body skeleton:

- Keep every heading in order. Fill each section; write `None.` or `N/A` when it does not apply.
- Preserve placeholders and comment blocks that automation replaces, such as `[#PR]` or `<!-- pr-body-macro:... -->`.
- Replace generic placeholders with real content. Do not add sections the template lacks or swap in a custom summary format.

Without a template, write a summary of what changed and why, a test plan with concrete steps, and related issues.

The description must be specific to this diff, and the test plan must list steps a reviewer can run. Do not claim checks passed unless they ran.

## Create or update

Push the branch with upstream tracking, then use the available GitHub integration or `gh pr create --draft`. When updating, read the current title and body first and keep human edits unless they are wrong or outdated. Refresh the narrative and test plan after new commits; leave automation blocks alone. Report the PR link.
