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

## Initial scope

The repository now includes a first example skill: [Product UI](../skills/product-ui/SKILL.md). It exercises the shared package convention with a host-neutral workflow and a focused quality checklist.

Add automated validation and host adapters after selecting target hosts and trying the skill on a representative task.
