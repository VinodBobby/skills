# Global agent instructions

Be simple, clean, concise, and straightforward. For any code change request, first review whether the change is truly necessary from a holistic standpoint. Prefer the existing setup and patterns already in the codebase. Reuse current language features, types, libraries, and validation approaches instead of rewriting them. Question every change before making it. Keep the scope tight and touch the fewest files possible.

After making changes, run lint and format checks, then run the relevant unit tests to confirm they pass and to find impacted cases. Validate results before concluding.

## Writing style

- Write in Simplified Technical English.
- Follow Zinsser's four principles: use short sentences, use the active voice, give each word one meaning, and cut clutter.
- Keep the writing warm and human. It should sound like a person wrote it, not a manual.

## Continuity

For work that spans sessions, keep a short continuity note in the task's canonical artifact and follow the `session-continuity` skill. Do not rely on chat history as the record.

## Git and pull requests

Commit, push, or open a pull request only when asked. Follow the `git-workflow` and `pull-request` skills for branch names, checks, rebasing, and PR descriptions.
