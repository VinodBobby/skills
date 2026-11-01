# Harvard ToolUniverse skills

This directory tracks the upstream source revision, the mirrored skill names, and local fixes for the ToolUniverse catalog in the repository's top-level `skills/` directory.

- Upstream: [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse)
- License: [Apache-2.0](../../third-party-licenses/harvard-tooluniverse-LICENSE.txt)
- Sync: [upstream catalog maintenance](../../docs/upstream-catalogs.md)

Local fixes, re-applied after every sync:

- [overrides.json](overrides.json): shortened descriptions that exceeded the 1,024-character limit, YAML quoting, explicit-only invocation for `devtu-github`, removal of its unlinked auto-push instructions, and a renamed nested template manifest in `create-tooluniverse-skill`.
- [local-overrides/](local-overrides/): whole-file replacements that stop `devtu-github`, `devtu-self-evolve`, and `devtu-code-optimization` from committing or pushing without an explicit request, fix broken reference links, and add two missing `tooluniverse-rnaseq-deseq2` reference guides. [overlay-bases.json](overlay-bases.json) records the upstream file each replacement was based on.

Submit these fixes upstream when practical; delete the matching override once upstream includes it.
