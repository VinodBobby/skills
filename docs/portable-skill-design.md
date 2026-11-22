# Portable Skill Design

## Goal

Create skills that preserve their workflow and meaning across machines and agent hosts, while making host-specific requirements visible and manageable.

Portability does not mean every host has the same tools or behaves identically. A skill can be format-portable while still requiring a host adapter for discovery, permissions, or integrations.

## Baseline format

Use the open Agent Skills format as the shared package contract:

- A skill is a directory with one `SKILL.md` entry point.
- `SKILL.md` starts with YAML frontmatter containing `name` and `description`.
- Optional resources live beside it in `references/`, `scripts/`, or `assets/`.
- Supporting files are linked with relative paths from the skill instructions.

Reference specifications and host guidance:

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Skills guide](https://developers.openai.com/api/docs/guides/tools-skills)
- [Anthropic Skills documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)

Keep host-specific metadata out of the portable core unless it is accepted by all intended targets. Put required host metadata, installation steps, and capability mappings in a separate adapter layer.

## Authoring principles

1. **One clear job:** Define the user request that should activate the skill and the result it should produce.
2. **Specific discovery text:** Make the description distinguish this skill from related workflows.
3. **Host-neutral instructions:** Refer to the model, available tools, and user-provided inputs. Avoid assumptions about a particular agent, operating system, home directory, or shell.
4. **Declared capabilities:** Name required capabilities and prerequisites. Distinguish required from optional integrations and describe a fallback when one is viable.
5. **Relative resources:** Resolve references, templates, and scripts relative to the skill package. Do not depend on files outside the package unless they are explicit inputs.
6. **Reproducible helpers:** Keep scripts small, accept explicit arguments, and state runtime and dependency requirements. Avoid undeclared local state.
7. **Progressive detail:** Keep the entry point concise. Put conditional procedures, schemas, and substantial examples in linked references.
8. **Least privilege:** Request only the access needed for the workflow. Make external or destructive actions and approval points explicit.
9. **Reviewable packaging:** Keep skills in version control, inspect third-party code and instructions, and record meaningful changes.

## Agent interaction efficiency

Apply agent-ergonomic interface ideas to the workflows a skill exposes; CLI-specific rules do not apply to every skill.

- Make the trigger and first useful action clear. Keep the default path short, with optional detail behind direct links.
- Use the minimum sufficient interface: a clear trigger, one primary workflow, and a concrete result shape. Keep rare or host-specific cases in linked references; do not copy general instructions into every skill or task brief.
- For tool-backed skills, prefer compact defaults and include counts or status summaries when they avoid a follow-up call. Distinguish a successful empty result from a failed read; bound large output and explain how to retrieve the rest.
- Make errors actionable and self-correcting; translate noisy backend errors into a concise cause and next step. Keep progress separate from structured output, and make mutations non-interactive, target-explicit, and safe to retry. After a successful write with failed readback, inspect state before retrying.
- Offer next steps only when they help resolve the current task. Omit them when the result is complete.
- For fast-changing tools, point to their live help or authoritative documentation instead of copying a command catalog into the skill. Keep setup opt-in and scoped.
- Compare representative tasks for success, unnecessary calls or turns, output size, and review effort. Treat published benchmarks as context, not proof that a pattern will improve every host or workflow.

## Suggested package layout

```text
skill-name/
├── SKILL.md
├── references/   # Optional task-specific guidance
├── scripts/      # Optional deterministic helpers
└── assets/       # Optional templates and output resources
```

Do not add empty directories or documentation that does not support the skill.

## Host adapters

Maintain a small compatibility record for each supported host. Record:

- how the host discovers and installs skills;
- supported frontmatter fields and package layout;
- available tools or integrations the workflow depends on;
- any host-specific files or metadata;
- known behavior differences and workarounds.

Adapters should map the portable skill to host conventions without forking the workflow. If a host requires an incompatible instruction or tool procedure, keep the difference in the adapter and link it clearly.

## Validation approach

Validate at two levels:

### Package checks

- Frontmatter parses and includes required fields.
- Skill name and directory name follow the chosen naming rules.
- Relative links resolve within the package.
- Scripts have documented runtimes and work with declared inputs.
- No instructions depend on undisclosed local paths, credentials, or machine state.

### Behavior checks

- Try representative requests on each target host with the same inputs.
- Confirm the skill is discoverable when expected and does not trigger for unrelated tasks.
- Compare outcomes against explicit acceptance criteria, not identical wording.
- Record host-specific setup and any observed differences.

Use each host's official validator where available. A format validator checks structure; it does not establish that the workflow is useful or portable in practice.

## Current tooling

- **Package checks:** [scripts/validate_skills.py](../scripts/validate_skills.py) checks frontmatter, names, the 1,024-character description limit, one manifest per package, relative links, and that the README lists every first-party skill. CI runs it on every pull request.
- **Host adapters:** [install.sh](../install.sh) links skills into `~/.agents/skills` and `~/.claude/skills`, which Codex, Claude Code, and Cursor discover, and links `agents/*.md` subagents into `~/.claude/agents`, which Claude Code and Cursor discover. Explicit-only skills set `disable-model-invocation: true` (Claude Code, Cursor) and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex).
- **Context budget:** every skill that can be invoked implicitly adds its name and description to each session. Keep descriptions short, mark rarely needed skills explicit-only, and keep repository-specific skills in that repository's own skill directory.
