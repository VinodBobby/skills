---
name: replace-with-skill-name
description: State what the skill does and its result. Use when <the requests that should activate it>; not for <the nearest related requests, naming the skill that handles them>. Keep it under 1,024 characters.
---

# Purpose

State the outcome this skill helps produce.

# Workflow

Describe the key decisions and steps. Focus on guidance that changes the result; leave routine choices to the agent.

# Requirements

List required inputs, tools, access, and runtime dependencies. Mark optional capabilities and state a fallback when one is practical.

# Resources

Link supporting files with paths relative to this skill directory. Remove this section if the skill needs no additional files.

<!--
Explicit-only skills (publishing, destructive, or rarely needed): add `disable-model-invocation: true`
to the frontmatter and an `agents/openai.yaml` containing:

policy:
  allow_implicit_invocation: false
-->
