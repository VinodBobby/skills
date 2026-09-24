# Harvard ToolUniverse skills

This directory tracks the upstream source revision and skill names mirrored into the repository's top-level `skills/` catalog.

- Upstream: [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse)
- Upstream skill catalog: [skills/](https://github.com/mims-harvard/ToolUniverse/tree/main/skills)
- License: [Apache-2.0](../../third-party-licenses/harvard-tooluniverse-LICENSE.txt)
- Sync workflow: [sync-harvard-tooluniverse-skills.yml](../../.github/workflows/sync-harvard-tooluniverse-skills.yml)

The sync runs every six hours and on manual dispatch. It opens a review pull request and does not merge changes automatically. If a sync pull request is already open, later runs wait. The workflow does not force-push or delete skills; upstream removals stop for manual review. Enable **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests** so the workflow can open pull requests.

The upstream catalog includes host-specific frontmatter extensions. The imported files preserve those fields. Some hosts may ignore extensions such as `disable-model-invocation`, `paths`, `triggers`, or `when_to_use`; treat them as discovery hints, not access controls. A small normalizer wraps three upstream plain-scalar descriptions that contain colon-space sequences so strict YAML parsers can read them. It changes presentation, not the description text.
