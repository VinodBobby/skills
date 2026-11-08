# Upstream catalog maintenance

Mirrored skill catalogs are configured in `upstreams/<name>/`:

| File | Purpose |
| --- | --- |
| `source.json` | Repository URL, skills path, license location, and install profile (`default` or `science`) |
| `SKILL_NAMES.txt`, `SOURCE_COMMIT` | Mirrored skill names and revision, written by the sync |
| `LOCAL_SKILLS.txt` | Catalog skills retained locally; included in the catalog install profile but not overwritten by sync |
| `skill_name_aliases` in `source.json` | Local names for upstream skills whose source names do not meet the Agent Skills naming rules |
| `local-overrides/` | Whole files copied over mirrored skills after each sync |
| `overlay-bases.json` | Hash of each upstream file a local override replaces |
| `overrides.json` | Targeted edits: `set` or `quote` a frontmatter field, `replace` text, `rename`, `delete`, or `write` a file; `optional: true` skips an edit until its target skill is mirrored |

The [sync workflow](../.github/workflows/sync-upstream-skills.yml) runs daily and on manual dispatch, one catalog at a time. It mirrors the upstream skills, re-applies local fixes, runs the validator, and opens a review pull request. It never merges, force-pushes, or deletes skills. If a sync pull request for a catalog is already open, later runs wait. Enable **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests** so it can open pull requests.

The sync stops for manual review when:

- upstream removes a skill;
- an upstream skill name collides with another skill in the repository;
- upstream changes a file that a local override replaces, or a `replace` override no longer finds its anchor text.

When upstream removes a skill, remove it from `SKILL_NAMES.txt`. Retain it in `LOCAL_SKILLS.txt` only when it still has an active use or a deliberate local override; otherwise remove its folder. Local-only catalog skills stay available with that catalog's install profile and remain excluded from the default install.

## Common tasks

Run a sync locally against a checkout of the upstream repository:

```bash
python3 scripts/sync_upstream.py sync <name> /path/to/upstream-checkout "$(git -C /path/to/upstream-checkout rev-parse HEAD)"
```

Re-apply local fixes after editing them:

```bash
python3 scripts/sync_upstream.py apply-overrides <name>
```

After reconciling a local override with a changed upstream file, record the new base:

```bash
python3 scripts/sync_upstream.py record-bases <name> /path/to/upstream-checkout
```

Do not edit mirrored skill directories directly; the next sync replaces them. Put fixes in the override files, and submit them upstream when practical.

To add a catalog, create `upstreams/<name>/source.json`, run the first sync locally, and add the name to the workflow matrix.
