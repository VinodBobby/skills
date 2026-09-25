---
name: obsidian-bases
description: Create or edit Obsidian Bases files and views that filter, group, summarize, or display vault notes. Use when working with `.base` files or database-like views in Obsidian.
---

# Purpose

Create a Base definition that selects vault files and displays their properties in useful views.

# Workflow

1. Inspect the vault's note properties and existing Base files. Choose filters and columns that match real property names.
2. Define the smallest useful view. Use filters to select notes, formulas for derived values, and summaries or grouping only when they answer a clear question.
3. Preserve existing Base structure when editing. Keep YAML valid, quote expressions where needed, and reference only defined formulas and properties.
4. Review the result for empty filters, misspelled properties, incompatible value types, and formulas that fail on missing values.
5. If Obsidian is available, open the Base and verify that the view renders and returns the expected notes.

# Requirements

A Base file can be authored as text, but rendering requires Obsidian with the Bases feature available. Use the current [Bases syntax reference](https://obsidian.md/help/bases/syntax) for schema and formula details; do not rely on remembered function lists.
