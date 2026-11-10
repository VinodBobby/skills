# Investment skills: decision map

## Destination

Provide portable skills for household portfolio policy, investment research, tax review, and portfolio maintenance. Let the research skill use evidence-backed investor profiles as optional research lenses.

## Decisions

| Question | Depends on | Decision |
| --- | --- | --- |
| How should responsibilities be packaged? | Existing equity research | [Four specialist skills](#package-boundaries) |
| How should the specialists exchange work? | Package boundaries | [A bounded workflow and shared handoff](#workflow-and-handoff) |
| How can the roles run as separate agents? | Workflow and handoff | [An orchestrator skill and role subagents](#pipeline-and-subagents) |
| How should investor styles be represented? | Package boundaries | [Profiles as reference data](#investor-profiles) |
| How can private profiles remain separate? | Investor profiles | [An explicit private source](#private-profile-source) |

Implementation is separate from these decisions: add the skill packages and starter profiles, update the catalog, and validate the packages. Additional investor names are a user preference and do not block the starter set.

### Package boundaries

The repository's `equity-research` skill already handles company due diligence. Keep it focused and add skills for portfolio strategy, investment research, tax planning, and maintenance. The research skill handles fund selection and can use equity research for individual companies. A single agent can use the skills sequentially; a host may assign the roles to separate agents.

### Workflow and handoff

Put the coordination workflow in its own explicit-only `portfolio-review` skill. It first lived inside portfolio strategy, but a policy subagent that loads portfolio strategy would then also load the orchestration steps. A host scheduler or user request can start a review; the skill alone does not schedule work. Each role returns the handoff record in `portfolio-review/references/handoff.md`: identifiers, status, data times, proposed actions with stable IDs, reasoning, effects, assumptions, sources, and unresolved issues. Keep calculations in available tools and route missing data or material disagreements for review.

### Pipeline and subagents

Policy is a gate. Maintenance, vehicle research, and per-company equity research depend only on policy, so they run in parallel. Tax runs on the merged draft trade set, with at most one revision round. Each role is a read-only subagent in `agents/` that loads one skill and returns a record; the orchestrator writes the run directory. Read-only roles keep account actions and private-data writes with the orchestrator. Cursor enforces this with `readonly: true`; Claude Code ignores that field, so each role also has a `tools` allowlist of read and web tools. That allowlist also removes shell calculators and MCP integrations from the roles, so the orchestrator puts the needed data in the snapshot and runs calculations itself. Claude Code and Cursor both load `~/.claude/agents`, so one definition serves both. Without subagent support, the same stages run in one agent.

### Investor profiles

Keep one profile method, an index, a template, and a reference file per person within investment research. A profile records sourced method, historical performance and its limits, and explicitly labeled adaptations. It is evidence for a research lens, not a separate persona, agent, or predicted recommendation. The user confirmed Buffett, Lynch, and Bogle as the starter set.

### Private profile source

Keep specialized private profiles in a separate private repository outside this working tree. Supply its location or connected source at runtime; keep access control in the host. Do not commit a private source path, identifier, or profile into this repository. Git documents that [submodules record paths and URLs](https://git-scm.com/docs/gitmodules) and that [ignore rules do not affect tracked files](https://git-scm.com/docs/gitignore), so neither is a privacy boundary. The skill provides a profile-reading convention; it does not create the private repository or enforce access.

## Research perspectives and source ledger

Assumptions: a household portfolio, with U.S. tax examples where needed. Sources were reviewed on 2026-11-08. Current account, fund, and tax facts must be checked again for each use.

| Perspective and question | Evidence and decision impact | Confidence / gap |
| --- | --- | --- |
| Household policy: what determines an allocation? | [Investor.gov](https://www.investor.gov/introduction-investing/getting-started/asset-allocation) ties allocation to goals, time horizon, and risk tolerance. Keep these inputs with the portfolio policy. | High; individual preferences still need user input. |
| Vehicle selection: is an expense ratio enough? | The [SEC fee bulletin](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/mutual-fund-and-etf-fees-and-expenses-investor-bulletin) describes share-class and other costs. Compare the available share class and total costs. | High; the specific prospectus and account determine actual costs. |
| Taxes: can a harvesting trade be evaluated in isolation? | [IRS Publication 550](https://www.irs.gov/publications/p550) discusses wash sales, related purchases, and capital-loss treatment. Review the tax year and relevant household accounts. | High for the cited U.S. guidance; current-year and personal facts need verification. |
| Cash: is the highest yield the only criterion? | [FINRA](https://syndication.finra.org/content/dont-lose-interest-managing-cash-your-brokerage-account) distinguishes available sweep arrangements. Compare access, liquidity, risks, and yield. | High; broker-specific terms vary. |
| Style and track record: can a public record recreate a person's decisions? | [Berkshire](https://www.berkshirehathaway.com/letters/2025ltr.pdf), [Fidelity](https://www.fidelity.com/myfidelity/InsideFidelity/NewsCenter/quickFacts/Magellan.html), and [Vanguard](https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/50-years-50-facts-indexing-since-1976.html) expose different vehicles and periods. Preserve attribution and benchmark limits. | High for the records shown; exact personal decision rules are incomplete. |
| Holdings: are public filings a complete portfolio? | The [SEC's Form 13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/frequently-asked-questions-about-form-13f) limits reportable securities and excludes short positions. Treat filings as dated, partial evidence. | High for U.S. 13F filings; other disclosures have different limits. |
| Privacy: can public Git configuration safely point to a private catalog? | [Git submodule](https://git-scm.com/docs/gitmodules) configuration records paths and URLs; [ignore rules](https://git-scm.com/docs/gitignore) do not affect tracked files. Pass a private source at runtime. | High for Git behavior; actual access and artifact privacy depend on the host. |

## Status and remaining questions

The four role packages, the `portfolio-review` orchestrator, five role subagents, and the starter profiles are implemented. The repository and skill validators passed; the repository validator reported three existing length warnings in unrelated skills. There are no unit tests under `scripts/`. Add private profiles when the user supplies an authorized private source and asks for them. The skills do not provide a scheduler, market-data connection, access control, or trading integration.
