---
name: diagram-design
description: Design clear flowcharts, architecture diagrams, sequences, state machines, ER diagrams, and data flows from requirements or source code. Use when a visual diagram will explain relationships or process better than prose.
---

# Purpose

Produce a correct, readable diagram whose nodes and connections reflect the supplied evidence or requirements.

# Workflow

1. Identify the reader, purpose, and source of truth. For an existing system, inspect its code, configuration, or documentation before naming components or flows.
2. Choose the diagram type that matches the question: flowchart for decisions, sequence for ordered messages, state machine for state transitions, ER diagram for data structure, and architecture or data flow for components and connections.
3. Use one node per distinct concept and one edge per meaningful relationship. Label non-obvious edges. Group related nodes and mark system or trust boundaries when they affect the explanation.
4. Keep the diagram focused. Split it when one view mixes unrelated concerns or becomes hard to scan. Add a legend only when symbols or colors need explanation.
5. Prefer an editable text format such as Mermaid when it can represent the diagram clearly. Use SVG or another requested format when layout, branding, or precise styling matters.
6. Validate syntax with an available renderer. Compare every node and edge with the source, and include the editable source with rendered output where practical.

# Requirements

Use only formats and renderers available in the current environment. If no renderer is available, provide the editable source and state that rendering was not checked. Do not invent system details to fill visual gaps.
