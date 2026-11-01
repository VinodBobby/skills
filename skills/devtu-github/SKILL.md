---
name: devtu-github
description: Prepare ToolUniverse changes for GitHub. Use only when the user explicitly asks to commit, push, or open or update a pull request; use the CI workflow for CI diagnosis and local fixes.
disable-model-invocation: true
---

# DevTU GitHub Workflow

Use this skill only for the GitHub action the user explicitly requested. A request to fix CI does not authorize a commit, push, or pull request. A commit request does not authorize a push. A push request does not authorize opening a pull request.

## Inspect the work

1. Resolve the repository, branch, remote, and requested action.
2. Check `git status --short` and inspect the relevant diff before staging anything.
3. Keep unrelated or unexplained changes untouched. Ask which files belong in the requested action when scope is unclear.
4. Identify likely temporary files and credentials for review. Do not move, delete, or unstage files automatically.
5. Use the GitHub Actions CI workflow for diagnosis or a local fix. Stop before GitHub mutations unless the user separately asks for them.

## Validate and publish

1. Run the checks the user requested and any focused checks needed to validate the change. Report checks that were not run.
2. If the user asked for a commit, stage only the intended files, review the staged diff, and commit. Do not push unless asked.
3. If the user asked for a push, verify the branch and remote, then use a normal push. If it is rejected because remote history changed, stop and explain. Do not force-push without separate explicit approval to rewrite remote history.
4. Open or update a pull request only when the user asks. Use the repository's PR template and report the resulting link.

## Boundaries

- Do not run `pre-commit install` or change Git hooks unless the user asks for hook setup.
- Never stage all files by default. Stage only files in the confirmed scope.
- Never move or delete files to make a branch look clean. Report candidates and let the user choose.
- Do not claim a push or PR succeeded unless the tool confirms it.
