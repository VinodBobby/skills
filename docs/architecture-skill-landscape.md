# Software Architecture Skills: Landscape and Recommendation

**Reviewed:** 2026-09-23  
**Scope:** Skills available on this machine and public, maintained skill repositories relevant to application architecture, cloud and native infrastructure, sizing, containers, implementation, operations, and observability.

## Summary

There is no single skill in this scan that covers software architecture across languages, cloud providers, on-premises systems, and native or edge deployments without platform assumptions. The strongest design for this repository is a **portable architecture workflow with optional provider and stack adapters**.

Use the portable skill to discover the current codebase and its constraints, compare viable designs, estimate capacity from stated assumptions, document decisions, and plan implementation and operations. Load AWS, Azure, Google Cloud, Vercel, or framework-specific guidance only when the target is known. Do not prescribe Docker, Kubernetes, microservices, or a cloud migration by default.

This is a reasoned shortlist based on source quality, scope, usefulness for the requested topics, and portability. It is not a measured ranking of skill quality.

## Strong candidates

| Candidate | Best use | Limits |
| --- | --- | --- |
| [Anthropic Engineering `system-design`](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/system-design/SKILL.md) | Best concise, provider-neutral workflow found. It covers requirements, constraints, component and data-flow design, APIs, storage, scaling, reliability, monitoring, and trade-offs. It is a strong starting point for this repo's core skill. | The skill is distributed inside an Anthropic plugin. Adapt its workflow; do not depend on plugin commands or connectors. |
| [Anthropic Engineering `architecture`](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/architecture/SKILL.md) | ADRs and design reviews. Its output includes context, decision, alternatives, cost, complexity, scale, team familiarity, trade-offs, consequences, and actions. Pair it with `system-design`. | It is focused on decision records, not infrastructure implementation or sizing. |
| [Matt Pocock `codebase-design`](https://github.com/mattpocock/skills/tree/main/codebase-design), [`domain-modeling`](https://github.com/mattpocock/skills/tree/main/domain-modeling), and [`improve-codebase-architecture`](https://github.com/mattpocock/skills/tree/main/improve-codebase-architecture) | Strong machine-local skills for code boundaries, deep modules, domain language, and identifying ways to improve an existing repository. They complement system design at the application-code level. | They focus on codebase design and refactoring, not cloud-provider selection, infrastructure sizing, container operations, or multi-cloud architecture. `improve-codebase-architecture` expects its companion design skills and supporting report resources. |
| [Microsoft `cloud-solution-architect`](https://github.com/microsoft/skills/blob/main/.github/skills/cloud-solution-architect/SKILL.md) | Broad Azure architecture reference for service selection, patterns, workload constraints, scale, reliability, cost, and monitoring/tracing. A good Azure adapter or checklist source. | Azure service mappings and guidance must not be treated as provider-neutral. |
| [Google `google-cloud-solution-architecture`](https://github.com/google/skills/blob/main/skills/cloud/google-cloud-solution-architecture/SKILL.md) | GCP-specific discovery and end-to-end architecture, including diagrams and deployment recommendations. Useful if GCP becomes a target. | GCP-focused; check its current tool and MCP requirements before adoption. |
| [AWS Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws) and its [skills catalog](https://github.com/aws/agent-toolkit-for-aws/blob/main/skills/README.md) | Strongest current AWS option in this scan. AWS describes the core skills as covering service selection, architecture decisions, infrastructure as code, containers, security, observability, and cost. It supports several agent environments, including Codex. | AWS-specific. Some workflows gain functionality from AWS tools, live documentation, or credentials. Keep it optional. |
| AWS [`aws-containers`](https://github.com/aws/agent-toolkit-for-aws/blob/main/skills/core-skills/aws-containers/SKILL.md) | AWS container deployment guidance for ECS, EKS, Fargate, and ECR. Use after AWS is selected and the task involves those services. | It is not a general Docker or provider-neutral containerization guide. |
| [AWS sample APEX skills](https://github.com/aws-samples/sample-apex-skills) | Deep operational and implementation guidance for AWS ECS and EKS, including architecture, build, deployment, observability, security, and upgrades. Consider if the chosen runtime is ECS or EKS. | The repository labels itself sample/educational material and requires review before production use. It is more specialized than a general architecture skill. |
| [Netresearch `docker-development`](https://github.com/netresearch/docker-development-skill) | A focused community skill for Dockerfiles, Compose, image build/testing, and container security. It can inform a later containerization reference. | Not a Docker-maintained standard. Review its split content license (CC-BY-SA-4.0) and test any imported instructions against the target stack and current Docker docs. |

### Skills already available on this machine

- `codebase-design`, `domain-modeling`, `improve-codebase-architecture`, `grilling`, `setup-ts-deep-modules`, and `wayfinder` are installed globally. The first three are the closest fit for software design and architecture work; `grilling` helps surface missing constraints, and `wayfinder` helps plan large initiatives.
- Vercel skills such as `nextjs`, `deployments-cicd`, `observability`, `vercel-functions`, and `vercel-services` are available locally. They are useful for Vercel deployments and Next.js, but they are not neutral infrastructure guidance.

## Recommended design for this repository

Create one portable `software-architecture` skill. Keep its entry workflow concise and put detailed checklists or templates in referenced files. Add provider adapters only when there is a concrete target and enough repeated use to justify maintaining them.

The core workflow should:

1. **Inspect before proposing.** Identify languages, frameworks, data stores, deployment files, current architecture, and existing operational conventions from the repository. State what is unknown.
2. **Gather workload and constraints.** Cover users and use cases; average and peak request rates; concurrency; payload and data growth; latency and availability targets; recovery objectives; security, compliance, and data-location needs; budget; team skills; and operational ownership. Ask only for missing information that changes the design.
3. **Compare feasible deployment shapes.** Consider native processes, managed/serverless services, containers, VMs, and orchestration based on workload and operating constraints. Explain why each added layer is justified. Include cloud, on-premises, hybrid, edge, or offline needs where relevant.
4. **Make sizing estimates explicit.** Show inputs, formulas or reasoning, and a range rather than a falsely precise instance size. Include CPU/memory, concurrency, storage, network, retention, redundancy, and expected growth as relevant. State what benchmark, load test, or production measurement would confirm the estimate.
5. **Design for operations.** Describe deployment and rollback, health checks, failure handling, backup and restore, scaling triggers, security boundaries, cost drivers, and ownership. When containers fit, cover image stages and base images, build context, runtime user and secrets, image scanning, and local/CI validation. For telemetry, prefer vendor-neutral instrumentation such as OpenTelemetry for traces, metrics, and logs, then select a backend for the target environment.
6. **Record the decision and next steps.** Produce a system-context and runtime/component diagram, an ADR with alternatives and consequences, an implementation sequence, and a validation plan. Distinguish confirmed facts from assumptions.
7. **Use current sources for changing details.** Check official provider documentation for service limits, instance types, prices, feature support, and security recommendations. Keep those details in provider adapters or cited references, not in the stable core workflow.

## Suggested package shape

```text
skills/software-architecture/
├── SKILL.md
└── references/
    ├── architecture-brief.md
    ├── capacity-estimation.md
    ├── deployment-and-operations.md
    └── adr-template.md
```

Start with the core skill and ADR template. Add detailed references as real use cases reveal gaps. Keep provider-specific service catalogs out of the core. A later `aws-architecture`, `azure-architecture`, or `gcp-architecture` adapter can route to current official sources when that provider is selected.

## Standards and source guidance

- Use a well-architected review as a checklist, not as a template for one cloud's service choices. AWS's framework, for example, groups review concerns into operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Translate those concerns into provider-neutral questions in the core skill.
- Use OpenTelemetry as a portable instrumentation baseline when appropriate. It is vendor-neutral and covers telemetry generation, collection, and export for traces, metrics, and logs; it does not replace the storage or visualization backend.
- Treat upstream skill repositories as guidance, not automatic truth. Review license and dependencies, pin imported versions or commits, and check current vendor docs before using fast-changing service details.

## Sources

- [Anthropic Engineering skills: `system-design`](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/system-design/SKILL.md) and [`architecture`](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/architecture/SKILL.md)
- [Matt Pocock skills repository](https://github.com/mattpocock/skills)
- [Microsoft cloud-solution-architect skill](https://github.com/microsoft/skills/blob/main/.github/skills/cloud-solution-architect/SKILL.md)
- [Google Cloud skills catalog](https://github.com/google/skills) and [Google Cloud solution-architecture skill](https://github.com/google/skills/blob/main/skills/cloud/google-cloud-solution-architecture/SKILL.md)
- [AWS Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws) and [AWS Agent Skills catalog](https://github.com/aws/agent-toolkit-for-aws/blob/main/skills/README.md)
- [AWS `aws-containers` skill](https://github.com/aws/agent-toolkit-for-aws/blob/main/skills/core-skills/aws-containers/SKILL.md)
- [AWS sample APEX skills](https://github.com/aws-samples/sample-apex-skills)
- [Netresearch Docker Development Skill](https://github.com/netresearch/docker-development-skill)
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)
- [AWS Well-Architected Framework pillars](https://docs.aws.amazon.com/wellarchitected/latest/migration-lens/well-architected-framework-pillars.html)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/what-is-opentelemetry/)
