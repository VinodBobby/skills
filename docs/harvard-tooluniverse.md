# Harvard ToolUniverse science skills

This repository mirrors the [ToolUniverse Agent Skills catalog](https://github.com/mims-harvard/ToolUniverse/tree/main/skills), maintained by the MIMS-Harvard project. At the imported revision, it contains 185 skills for scientific research workflows, including domain analysis, research, ToolUniverse setup, and skill development. The [`tooluniverse` router](../skills/tooluniverse/SKILL.md) refers to companion skills in the catalog.

## Use and dependencies

The skill folders follow the Agent Skills layout. To use one, install or expose the selected folder through the skill mechanism supported by the target agent. ToolUniverse workflows that call the ToolUniverse SDK, CLI, MCP server, or external scientific APIs also need those dependencies configured. This repository only mirrors skill instructions and supporting files; it does not install the ToolUniverse runtime or configure credentials. Follow the [upstream setup guide](https://github.com/mims-harvard/ToolUniverse#install) for those tasks.

The upstream project is licensed under Apache-2.0. Its license is preserved at [harvard-tooluniverse-LICENSE.txt](../third-party-licenses/harvard-tooluniverse-LICENSE.txt).

## Upstream maintenance

The catalog syncs daily through a review pull request; see [upstream catalog maintenance](upstream-catalogs.md). Do not edit mirrored skill directories directly. Local fixes live in [upstreams/harvard-tooluniverse](../upstreams/harvard-tooluniverse/README.md) and are re-applied after each sync.

Upstream SKILL.md files may include host-specific frontmatter extensions such as `disable-model-invocation`, `paths`, `triggers`, or `when_to_use`. Hosts that do not support a field ignore it, so treat these as discovery hints, not access controls. The `tooluniverse` router also uses host-specific skill-calling syntax.

The catalog is not installed by default. Run `./install.sh --with-science` to add it.
