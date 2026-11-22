---
name: skill-doctor
description: Audit this repository's skills for unique value, discovery and loading cost, overlap, and stale guidance; use when deciding whether to keep, shorten, merge, or retire skills.
---

# Skill Doctor

Improve the skill set without mistaking length for waste. Use the static report as a map, then judge whether each skill changes routing, correctness, safety, or repeatable work.

## Audit

1. Run `python3 skills/skill-doctor/scripts/skill_doctor.py` from the repository root. The report estimates description and entrypoint cost, finds repeated wording, and lists overlap candidates.
2. Read the affected skills and their linked references. Check install profiles, upstream ownership, local overrides, README entries, and any available usage or evaluation data.
3. When outcome evidence matters and the host supports controlled runs, select two to five representative requests. Keep the model, tools, context, and inputs constant; compare the candidate skill enabled with it withheld. Score actual task behavior: correctness, completeness, constraints, and success. Do not treat keyword or source-string checks as evidence that a skill works, unless the exact text is itself the output contract. Also note avoidable calls or turns, noisy output, and human review effort. Record host token counts when available; otherwise use the static character estimate and mark token use approximate. If the host cannot isolate a skill or reproduce the same conditions, mark the outcome effect unknown.
4. Classify each candidate as keep, tighten, merge, or retire. Check whether its trigger points to the right workflow, the default path gets to a useful action without needless lookup or correction, and the output makes status and failure clear. For tool-backed skills, inspect empty results, truncation, actionable errors, and mutation retry behavior where relevant. Prefer removing repeated no-op instructions. Keep guidance that changes tool choice, preserves a domain rule, prevents a real failure, or produces a reusable result. Record the evidence and uncertainty behind each decision.
5. When asked to clean up, edit only clear no-ops and duplication. Preserve unique workflows and safety checks. Update the source of truth, catalog manifests, install profiles, and README as needed, then run the repository validator.

Static size and overlap are review signals, not deletion rules. Do not claim a token saving is an outcome improvement without host usage data or a controlled comparison. Do not delete a skill only because it is long, rarely invoked in available logs, or overlaps in vocabulary.
