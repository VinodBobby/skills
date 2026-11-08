# Harvard ToolUniverse skills

This directory tracks the upstream source revision, mirrored skill names, locally retained skills, and fixes for the ToolUniverse catalog in the repository's top-level `skills/` directory.

- Upstream: [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse)
- License: [Apache-2.0](../../third-party-licenses/harvard-tooluniverse-LICENSE.txt)
- Sync: [upstream catalog maintenance](../../docs/upstream-catalogs.md)

`SKILL_NAMES.txt` lists skills currently mirrored from upstream. `LOCAL_SKILLS.txt` lists useful skills removed upstream that we keep for active local workflows. Both groups are installed only with `--with-science`. `source.json` maps eight upstream folder names that contain underscores to valid hyphenated local skill names.

| Local-only skill | Reason to keep |
| --- | --- |
| `devtu-code-optimization` | Keeps ToolUniverse-specific debugging patterns used by `devtu-self-evolve`. |
| `devtu-create-tool` | Active dependency of the tool-creation, benchmark, and self-evolution workflows. |
| `devtu-fix-tool` | Active dependency of tool creation, benchmark triage, and self-evolution. |
| `devtu-github` | Preserves the local explicit-action publishing policy and its OpenAI metadata override. |
| `devtu-optimize-skills` | Active dependency of skill creation, benchmarking, and self-evolution. |
| `devtu-self-evolve` | Local orchestrator with explicit publishing boundaries and local fixes. |

Retired skills: `devtu-auto-discover-apis` (use `research` plus the existing ToolUniverse inventory), `devtu-docs-quality` (use the repository's documented checks and `tooluniverse-self-review`), and `devtu-optimize-descriptions` (use `tooluniverse-custom-tool`; no separate optimizer is needed).

Local fixes, re-applied after every sync:

- [overrides.json](overrides.json): shortened descriptions that exceeded the 1,024-character limit, YAML quoting, explicit-only invocation for `devtu-github`, removal of its unlinked auto-push instructions, and a renamed nested template manifest in `create-tooluniverse-skill`.
- [local-overrides/](local-overrides/): whole-file replacements that stop `devtu-github`, `devtu-self-evolve`, and `devtu-code-optimization` from committing or pushing without an explicit request, fix broken reference links, and add two missing `tooluniverse-rnaseq-deseq2` reference guides. [overlay-bases.json](overlay-bases.json) records the upstream file each replacement was based on.

Submit these fixes upstream when practical; delete the matching override once upstream includes it.
