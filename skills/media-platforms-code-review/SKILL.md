---
name: media-platforms-code-review
description: Apply repository-specific review checks to diffs and pull requests in Media-Platforms/ads-and-analytics or Media-Platforms/voltron, including ads and FRE integration contracts. Use only for these repositories.
---

# Media Platforms Code Review

Use this skill to add focused repository context to a defect-focused code review. Historical review patterns are evidence, not rules. Report only issues that the current diff can cause.

## Route by repository

1. Confirm the repository from its Git remote or project context.
2. For `Media-Platforms/ads-and-analytics`, read [the Ads and Analytics review guide](references/ads-and-analytics.md).
3. For `Media-Platforms/voltron`, read [the Voltron review guide](references/voltron.md).
4. If the change spans both repositories, read both guides and trace each cross-repo contract from producer to consumer.

If the repository is neither target, use the repository's normal review guidance instead of these profiles.

## Review

- Inspect the requested diff and enough surrounding code to confirm each finding's trigger and effect.
- Apply only the review checks that match the changed behavior. Do not force a repository-specific concern onto unrelated code.
- Check existing helpers, contracts, tests, and architecture before suggesting a replacement.
- Separate confirmed defects from questions and optional improvements. Do not turn reviewer preferences into findings without evidence of risk or a local convention.
- For runtime changes, assess whether the PR gives reviewers concrete test or QA steps for changed and affected existing behavior. Do not demand broad coverage for mechanical or config-only changes.
- Do not change code during a review. Make fixes only when the user also asks for implementation.

## Report

Put actionable findings first. For each finding, include severity, a precise location, the triggering condition, its impact, and a concrete fix. Keep questions and optional suggestions separate. If there are no findings, state the scope reviewed and any meaningful verification limits. Include a short list of review lenses checked only when it helps explain coverage.
