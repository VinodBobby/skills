---
name: product-ui
description: Design and implement polished, responsive user interfaces with working interactions and accessible defaults. Use for web pages, components, and user-facing product features; adapt to the current project and its design system.
---

# Product UI

Create a cohesive, usable interface that fits the user's product and the existing project. Aim for the finish of a strong interactive prototype while keeping the code consistent with the host project.

## Workflow

1. Inspect the existing app, framework, components, styling, and nearby patterns before choosing an implementation. Reuse the design system and dependencies already present.
2. Identify the user, their main task, the page hierarchy, and the primary action. If the request leaves routine details open, make sensible choices and continue.
3. Plan the key interaction and data states before building. Include the expected loading, empty, error, success, and disabled states where they apply.
4. Implement the complete interface in the existing stack. Make controls work. Connect to existing data and services when available. Do not present fake data or unfinished controls as production functionality.
5. Make the layout responsive and accessible. Use semantic HTML, clear labels, keyboard support, visible focus, readable contrast, and reduced-motion support where relevant.
6. Use available preview or browser tools to inspect the result and refine obvious layout or interaction problems. If visual inspection is unavailable, review the implementation against the checklist in [references/ui-quality-checklist.md](references/ui-quality-checklist.md).

## Scope and capability boundaries

- This skill guides design and implementation. It does not require v0 or any specific agent host.
- Use the tools and integrations available in the current environment. Do not claim a service is connected unless the project provides working configuration and credentials.
- If a request depends on an unavailable external service, build the useful interface boundary and explain what setup remains. Use clearly identified sample data only when it helps demonstrate the interface.
- Follow the user's requested stack, visual direction, and scope. Avoid replacing existing project conventions to impose a preferred framework or component library.

## Quality checklist

Before finishing, check [references/ui-quality-checklist.md](references/ui-quality-checklist.md). Report what works and identify any external integration that remains unconnected.
