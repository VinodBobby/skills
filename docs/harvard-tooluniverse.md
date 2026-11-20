# Curated Harvard ToolUniverse skills

This repository retains eleven ToolUniverse skills for skill authoring, benchmarking, SDK/custom-tool work, self-review, and local development. The five mirrored upstream skills are listed in [INCLUDE_SKILLS.txt](../upstreams/harvard-tooluniverse/INCLUDE_SKILLS.txt); six local development skills are listed in [LOCAL_SKILLS.txt](../upstreams/harvard-tooluniverse/LOCAL_SKILLS.txt) and together they form the [ToolUniverse core profile](../profiles/tooluniverse-core.txt). Broad biomedical research workflows and all `setup-*` guides are not mirrored. Stanford STORM remains a separate first-party skill.

## Selection basis

The selection follows the repository's general-purpose, portable-workflow focus. It retains reusable authoring, evaluation, SDK/custom-tool, review, and maintenance workflows; it excludes specialized biomedical procedures and setup guides tied to individual remote models or environments. The [official ToolUniverse skills catalog](https://zitniklab.hms.harvard.edu/ToolUniverse/guide/skills_showcase.html) describes those research skills as specialized domain workflows.

The independent [SkillsBench study](https://yubol-bobo.github.io/assets/pdf/SkillsBench.pdf) found that curated skills improved average task pass rates, but gains varied by task and 16 of 84 tasks regressed. In its benchmark, tasks supplied with 2–3 relevant skills improved more than those supplied with 4 or more. That supports keeping a focused collection and loading only task-relevant skills; it does **not** rank these specific ToolUniverse skills, which were not evaluated by that study.

## Use and dependencies

The skill folders follow the Agent Skills layout. To use one, install or expose the selected folder through the skill mechanism supported by the target agent. The SDK and custom-tool workflows also need their runtime dependencies configured. This repository only mirrors skill instructions and supporting files; it does not install the ToolUniverse runtime or configure credentials.

The upstream project is licensed under Apache-2.0. Its license is preserved at [harvard-tooluniverse-LICENSE.txt](../third-party-licenses/harvard-tooluniverse-LICENSE.txt).

## Upstream maintenance

The catalog syncs daily through a review pull request; see [upstream catalog maintenance](upstream-catalogs.md). Do not edit mirrored skill directories directly. Local fixes live in [upstreams/harvard-tooluniverse](../upstreams/harvard-tooluniverse/README.md) and are re-applied after each sync.

Upstream SKILL.md files may include host-specific frontmatter extensions such as `disable-model-invocation`, `paths`, `triggers`, or `when_to_use`. Hosts that do not support a field ignore it, so treat these as discovery hints, not access controls.

The curated set is not installed by default. Run `./install.sh --with-science` to add it.
