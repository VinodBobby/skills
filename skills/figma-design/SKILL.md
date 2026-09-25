---
name: figma-design
description: Plan, create, or revise product screens and design systems in Figma using existing components, styles, and design tokens. Use when the requested artifact must be created or edited in a Figma file.
---

# Purpose

Make a Figma design that follows the product's visual system and reflects the requested content, states, and interactions.

# Workflow

1. Confirm whether the task creates a new file or edits an existing one. For an existing file, use the provided file and target frame; do not guess which file to change.
2. Review the product brief and available design system. Reuse existing components, variables, typography, and spacing patterns when they fit. If no design system is available, establish a small consistent set of styles before building repeated elements.
3. Define the screen structure and key states before making detailed components. Include loading, empty, error, responsive, and accessibility states when they matter to the request.
4. Use the Figma integration available in the current host to create or edit the file. If no Figma integration is available, provide a design specification or implementation-ready handoff instead of claiming that the file changed.
5. Inspect the result at the relevant viewport sizes. Check hierarchy, spacing, text fit, contrast, reusable components, and consistency with the source.
6. Report the file or frames changed and any requested states that remain unimplemented.

# Requirements

Direct Figma changes require a Figma connector or an equivalent authorized integration. Tool names and capabilities vary by host; use that host's current documentation rather than assuming a particular API.
