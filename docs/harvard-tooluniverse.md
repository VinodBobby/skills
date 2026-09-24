# Harvard ToolUniverse science skills

This repository mirrors the [ToolUniverse Agent Skills catalog](https://github.com/mims-harvard/ToolUniverse/tree/main/skills), maintained by the MIMS-Harvard project. At the imported revision, it contains 185 skills for scientific research workflows, including domain analysis, research, ToolUniverse setup, and skill development. The [`tooluniverse` router](../skills/tooluniverse/SKILL.md) refers to companion skills in the catalog.

## Use and dependencies

The skill folders follow the Agent Skills layout. To use one, install or expose the selected folder through the skill mechanism supported by the target agent. ToolUniverse workflows that call the ToolUniverse SDK, CLI, MCP server, or external scientific APIs also need those dependencies configured. This repository only mirrors skill instructions and supporting files; it does not install the ToolUniverse runtime or configure credentials. Follow the [upstream setup guide](https://github.com/mims-harvard/ToolUniverse#install) for those tasks.

The upstream project is licensed under Apache-2.0. Its license is preserved at [harvard-tooluniverse-LICENSE.txt](../third-party-licenses/harvard-tooluniverse-LICENSE.txt).

## Upstream maintenance

The [sync workflow](../.github/workflows/sync-harvard-tooluniverse-skills.yml) checks upstream every six hours and can also run manually. It opens a review pull request and never merges automatically. If a sync pull request is already open, later runs wait. It does not force-push or delete skills. If upstream removes a skill, the workflow stops so a maintainer can review that removal. Review each update before merging. Avoid editing mirrored skill directories directly; submit changes upstream or place local guidance in a separate skill.

Upstream SKILL.md files may include host-specific frontmatter extensions. Agents can ignore unknown fields, so host-specific invocation and path hints may work differently between clients. The `tooluniverse` router also uses host-specific skill-calling syntax. Check it on each target agent or add a small adapter where needed. The mirror preserves upstream content and applies one documented YAML formatting normalization to three descriptions that strict parsers otherwise reject.
