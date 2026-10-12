# Bootstrap a repository for coding-agent work

Use this reference when creating a repository or when the user explicitly asks to make an existing repository agent-ready. First inspect what already exists. Reuse working setup and edit the fewest files needed.

## Decide what the first release must prove

Choose one or two representative user workflows and name their success conditions. Include the real input, expected result, and the important failure case. Separate exact compatibility requirements from approximations and future scope. Avoid starting with a giant feature checklist or a percentage score that counts a stub as complete.

Build the first slice end to end. Use it to test the architecture, setup, checks, and acceptance harness before adding broad parallel work.

## Make a fresh checkout verifiable

- Document the supported runtime and dependency setup in the README.
- Provide concise commands for formatting, focused checks, full checks, and running the product. Use the repository's task runner or package scripts as the source of truth.
- Make the primary checks work from a clean checkout. Document any required external service or test fixture without exposing secrets.
- Keep test output easy for agents to interpret. Put long logs in files and print a concise result with actionable error locations.

## Add a short repository instruction file

Create or update the repository's agent instruction file (for example, `AGENTS.md`) with stable facts that are hard to infer from the code:

- a compact architecture map and module ownership boundaries;
- invariants that protect data, formats, security, or compatibility;
- the commands and test fixtures needed for common changes;
- how to run and inspect the product, including UI automation or a control API when available;
- where current task state belongs, if long-running work needs a handoff.

Keep general advice, duplicated command lists, speculative policies, and stale progress out of this file. Put detailed material behind a link only when a task branch needs it.

## Build an evidence-based test loop

Use checks suited to the product rather than a fixed test stack:

- fast unit or component checks for local iteration;
- integration and end-to-end tests for the representative workflows;
- reference files, golden outputs, protocol fixtures, or external oracles for compatibility claims;
- performance and resource budgets for known hot paths;
- a pull-request CI gate that runs the checks required before merge.

For a visual application, expose a stable way to launch, drive, and inspect it. Use scripted interaction to verify the workflow and a human review for visual quality and usability. Protect the acceptance contract from changes made only to make the implementation pass.

Start with a small representative corpus. Add cases when a real failure reveals a missing invariant. Make expected results reproducible and label approximations honestly.

## Set parallel work boundaries

- Define module or crate ownership before assigning concurrent tasks.
- Use isolated worktrees or branches for independent changes.
- Keep changes to shared interfaces small and coordinate them through explicit contracts.
- Record build and test resource needs. Set a concurrency limit based on actual machine, disk, CI, and review capacity; add remote workers or caching only when local limits justify the operating cost.
- Integrate small changes often and run the relevant checks after each merge.

Do not parallelize tightly coupled design work before its interfaces are clear. More agents can increase contention without increasing accepted output.

## Support reliable handoffs

For work that spans context windows, keep one concise status artifact with:

- the goal and acceptance criteria;
- completed work and checks run;
- current failure or blocker;
- next action and owned files.

Ask each agent to leave a clean tree and update this artifact before it hands off. Do not maintain multiple competing progress files.

## Track quality and cost

For the first agent-assisted workflow, capture elapsed time, human review time, model cost when available, first-pass acceptance, regressions, and workflow completion. Compare against a human or prior-project baseline when one exists. Increase agent concurrency or evaluator complexity only when the measured quality-adjusted throughput improves.

