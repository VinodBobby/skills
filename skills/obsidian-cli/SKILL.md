---
name: obsidian-cli
description: Read, search, create, or update notes in an Obsidian vault through the Obsidian command-line interface. Use when the user asks to operate on a live vault or manage notes from the terminal.
---

# Purpose

Use Obsidian's CLI for a requested vault operation while targeting the intended vault and minimizing unintended changes.

# Workflow

1. Confirm which vault and notes the user means. Read the CLI help first because available commands and options can change.
2. Prefer read, search, and list commands to identify the exact target before editing. Use a vault name or path explicitly when more than one vault may be active.
3. Make only the requested changes. Avoid overwrite, delete, move, or bulk operations unless the user requested them. For broad changes, report the planned scope before applying them.
4. Re-read or search the affected notes after writing. Confirm the intended property, content, and file path changed.
5. If the CLI is unavailable, use direct Markdown file edits only when the vault path is known and authorized. State when the live Obsidian view could not be checked.

# Requirements

Direct CLI use requires an installed Obsidian CLI and access to the target vault. Run `obsidian help` to inspect current syntax. See the [official CLI guide](https://obsidian.md/help/cli).
