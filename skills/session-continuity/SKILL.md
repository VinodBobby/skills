---
name: session-continuity
description: Keep long-running work recoverable across agent sessions with a short continuity note in the task's canonical artifact. Use when work spans sessions, agents, or handoffs, or when resuming earlier work; not for one-session tasks.
---

# Session continuity

Make the next session able to resume from durable artifacts, not from chat history.

## Resume

1. Find the continuity note in the task's canonical artifact: the issue, pull request description, planning document, or a file the repository already uses for this purpose. Ask when there is none and the location matters.
2. Read the note, then open only the sources it points to that the next action needs.
3. Recheck status-sensitive facts before acting on them: branch state, CI, ticket status, deployments, and anything dated.

## Maintain the note

Keep it short. Include:

- the goal and acceptance contract;
- current status and the next action;
- confirmed decisions, each with a source link;
- open questions and who can answer them;
- facts that can change, with their source and date.

Keep source facts in their authoritative documents or systems and point to them. Do not copy whole histories, logs, or transcripts into the note. Separate confirmed facts from assumptions and record conflicts between sources instead of choosing silently.

## Hand off

Before the session ends, update the note so a fresh agent can continue with only the current working set. Remove resolved questions and stale status. Leave the working tree in a clean, explainable state and state what was verified and what was not.

Write to external systems, such as issue trackers or pull requests, only when the user authorized that kind of change.
