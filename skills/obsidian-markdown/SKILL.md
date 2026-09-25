---
name: obsidian-markdown
description: Create and edit Obsidian Markdown notes with vault links, embeds, callouts, tags, and properties. Use when editing notes for an Obsidian vault or when Obsidian-specific syntax matters.
---

# Purpose

Edit Obsidian notes while preserving their plain-text structure, vault links, and existing metadata.

# Workflow

1. Inspect the target note and nearby notes to learn the vault's naming, frontmatter, and linking conventions.
2. Preserve existing properties and their types. Add only properties needed for the user's request. Keep YAML values valid and avoid duplicate keys.
3. Use `[[wikilinks]]` for notes inside the vault when the target note exists. Use standard Markdown links for external sources. Embed notes or files only when the user wants their content shown inline.
4. Use Obsidian syntax such as callouts or inline tags when it improves the note. Keep ordinary prose in standard Markdown so it remains readable outside Obsidian.
5. Check links, headings, lists, and frontmatter after editing. If the Obsidian app is available, inspect the rendered note when layout or plugin behavior matters.

# Requirements

This skill can edit Markdown files directly. Rendering checks require Obsidian or another compatible preview. Consult [Obsidian Flavored Markdown](https://obsidian.md/help/obsidian-flavored-markdown) when syntax or compatibility is uncertain.
