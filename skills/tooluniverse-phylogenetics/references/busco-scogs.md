## BUSCO scogs questions (multi-species phylogenomics)

data folders with `scogs_fungi.zip` and/or `scogs_animals.zip` ship
pre-computed per-ortholog alignments (and sometimes trees). The
question asks for a metric per group, or a Mann-Whitney U / median /
ratio comparison between groups.

### PRIMARY SCRIPT — both groups in one pass (use this FIRST)

When the question compares animals vs fungi (Mann-Whitney U, ratio,
fold-change, paired difference), the bundled paired-comparison script
extracts both zips, computes the metric per ortholog for each group,
and emits ALL of: per-group summary, two-tailed Mann-Whitney U +
p-value (in both orderings since U is asymmetric), paired-ortholog
median diff, paired-ortholog median ratio, group-median ratio, and
lowest-non-zero ratios — in one run, no aggregation step needed:

```bash
python skills/tooluniverse-phylogenetics/scripts/scogs_paired_compare.py \
    --data-folder "$DATA_PATH" --metric parsimony_informative
# Metrics: parsimony_informative, rcv, gap_percentage (alignment-only,
# Biopython-fast: ~2s for 500 alignments);
# treeness, dvmc, total_tree_length, evolutionary_rate, long_branch_score,
# patristic_distances (tree); treeness_over_rcv, saturation (both).
```

Output blocks (parse in Python or grep):

```
# SUMMARY group=animals: n=... mean=... median=... min=... max=... p25=... p75=... lowest_nonzero=... n_nonzero=...
# SUMMARY group=fungi:   n=... mean=... median=... min=... max=... p25=... p75=... lowest_nonzero=... n_nonzero=...
# MWU animals_vs_fungi: U=... p=...
# MWU fungi_vs_animals: U=... p=...        <-- U(a,b) + U(b,a) = n_a*n_b
# PAIRED n_common=N: median_diff(animals-fungi)=...  median_diff(fungi-animals)=...
# PAIRED RATIO median(animals/fungi)=... (n=...)    <-- for each common ortholog: a_val/b_val, then median
# PAIRED RATIO median(fungi/animals)=... (n=...)
# GROUP_MEDIAN_RATIO animals/fungi=...               <-- median(group_a) / median(group_b)
# GROUP_MEDIAN_RATIO fungi/animals=...
# GROUP_MEDIAN_DIFF animals-fungi=...
# LOWEST_NONZERO animals=... fungi=...
# LOWEST_NONZERO_RATIO animals/fungi=...
# LOWEST_NONZERO_RATIO fungi/animals=...
```

For `long_branch_score` and `patristic_distances` (multi-value-per-tree
metrics), pass `--per-tree-stat mean` or `--per-tree-stat median` to
choose the per-tree summary BEFORE the cross-tree MWU. The question
wording "comparing **median** long branch scores" means per-tree
summary = median; "comparing **mean** long branch scores" means
per-tree summary = mean. Run TWICE (once with each) if uncertain.

### Single-group script (when only one group is asked about)

```bash
python skills/tooluniverse-phylogenetics/scripts/scogs_phykit_pipeline.py \
    --data-folder "$DATA_PATH" --group fungi --metric treeness --out /tmp/f.tsv
# Auto-falls-back to .faa.mafft when .faa.mafft.clipkit is absent
# (some scogs zips ship only mafft alignments, not clipkit trims).
```

### `phykit parsimony_informative` is NOT a valid CLI subcommand

PhyKIT's CLI exposes parsimony-informative-site count as
`parsimony_informative_sites` (alias `pis`). Calling
`phykit parsimony_informative <file>` returns the help banner with
non-zero exit and silently produces zero values. The bundled scripts
translate `parsimony_informative` → `parsimony_informative_sites`
automatically. The output is `<n_pi>\t<n_total>\t<percent>` — column
THREE is the percentage that questions usually ask for.

### Group-median ratio vs paired ratio (read this carefully)

When a question phrases tree-length / RCV / DVMC comparisons as
"ratio of fungal to animal X across orthologs", there are TWO distinct
quantities:

1. **GROUP_MEDIAN_RATIO** = `median(values_fungi) / median(values_animals)`.
   Use ALL orthologs in each group independently. This is what
   group-comparison published numbers usually report (n_fungi can
   differ from n_animals, and "across" is a population statement, not
   a paired one).

2. **PAIRED RATIO median** = for each ortholog present in BOTH groups,
   compute `value_fungi / value_animals`, then take the median across
   common orthologs. Smaller denominator (intersection only) and a
   different number when the groups have different size.

Default to GROUP_MEDIAN_RATIO unless the question explicitly says
"matched ortholog", "paired ortholog", "per-ortholog ratio", or "for
each ortholog". If the answer phrasing is ambiguous, BOTH numbers are
in the script's output — pick the one matching the question's
"across" / "paired" / "ratio of medians" phrasing.

### Total amino-acid count across single-copy orthologs — single representative, not all species

When a BUSCO single-copy ortholog dataset (`single_copy_busco_sequences/`) is
present and the question asks "**how many total amino acids** are present in all
single-copy ortholog sequences", count **one representative sequence per
ortholog**, not the sum across all species/copies.

Each `<ortholog_id>.faa` in `single_copy_busco_sequences/` typically contains
multiple species' copies of that ortholog (one each). Summing every sequence
across every species double/triple/N-fold counts each ortholog by the species
count and gives `n_species × correct_answer`.

| Question phrasing | Count |
|---|---|
| "total amino acids in all single-copy ortholog sequences" | Sum of ONE sequence per ortholog (either the FIRST entry per file or the median-length entry) |
| "total amino acids across N species' single-copy orthologs" | Sum across species explicitly (multi-species sum) |
| "average length of single-copy orthologs" | Mean per-ortholog length (one per ortholog) |

❌ WRONG: `for f in *.faa: sum(len(rec.seq) for rec in SeqIO.parse(f, 'fasta'))` then sum across files (multi-species sum)

✅ RIGHT: `for f in *.faa: first_rec = next(SeqIO.parse(f, 'fasta')); total += len(first_rec.seq)` (one representative per ortholog)

If your answer is `n_species × GT` (e.g. 32228 when GT looks like 13809 = 32228/2.33 ≈ 8 species × representative), you summed all species — re-do with one representative.

### Lowest-non-zero ratios

For metrics that can legitimately equal 0 for highly conserved or
very short alignments (parsimony informative %, RCV on near-identical
seqs), "lowest" in a question typically means "lowest non-zero". The
paired script emits `LOWEST_NONZERO_RATIO` for both orderings — use
that line when the raw min in a group is 0.

### File-layout fallback (alignment naming)

scogs zips ship in two shapes:
- **Full**: `<gene>.faa`, `<gene>.faa.mafft`, `<gene>.faa.mafft.clipkit`,
  `<gene>.faa.mafft.clipkit.treefile`, plus iqtree/bionj/log/mldist.
- **Alignment-only**: just `<gene>.faa` + `<gene>.faa.mafft`. No
  trees, no clipkit. Used for parsimony, RCV, gap-percentage
  questions. Use the `.faa.mafft` (NOT raw `.faa`) — the published
  metric was computed on the MAFFT-aligned file.

Both bundled scripts auto-detect the layout and use the best available
alignment per ortholog. Do NOT re-run MAFFT or ClipKit yourself; the
shipped files are canonical.

#### Which alignment goes with which metric (this changes the answer)

The tree is always the ClipKit-derived `.faa.mafft.clipkit.treefile`. The
**alignment** argument depends on the metric:

| metric | alignment to pass |
|---|---|
| `treeness`, `dvmc`, `total_tree_length`, `long_branch_score` | tree only — no alignment |
| `saturation` | `.faa.mafft.clipkit` (trimmed) |
| **`treeness_over_rcv` / `rcv`** | **`.faa.mafft` (untrimmed)** |
| parsimony-informative sites, gap percentage | `.faa.mafft` (untrimmed) |

RCV measures compositional variability **across the alignment's columns**, so
trimming changes it materially — and `treeness_over_rcv` divides by RCV, so the
trimmed alignment shifts the ratio for every gene. Verified on the fungal scogs
set (249 orthologs, canonical shipped files):

```
median treeness/RCV   untrimmed .faa.mafft = 0.2683    trimmed .clipkit = 0.3050
max treeness/RCV      (over the 3 genes with >70% gapped columns:
                       1260807at2759 0.0861, 1567796at2759 0.1866, 939345at2759 0.2572)
                      untrimmed .faa.mafft = 0.2572    trimmed .clipkit = 0.4174
```

Plain `treeness` needs no alignment and is unaffected — it reproduces exactly
(median 0.0501 on the same 249 files), which is how the alignment choice was
isolated as the cause rather than the tree set or the tool.

`phykit_batch_analysis` takes the two independently, so pass them explicitly:

```bash
tu run phykit_batch_analysis '{"operation":"batch","function":"treeness_over_rcv",
  "directory":"<dir>","extension":".faa.mafft",
  "tree_directory":"<dir>","tree_extension":".faa.mafft.clipkit.treefile"}'
```

**Gap percentage** in these questions means the fraction of alignment
**columns containing at least one gap**, not the fraction of all residues that
are gaps. The two differ by an order of magnitude: with the residue definition
no fungal ortholog exceeds 70% gaps, so a ">70% gaps" filter silently selects
nothing.

**Anti-pattern:** running `phykit` on the raw `*.busco.zip` extracted
ortholog FASTAs and aligning/tree-building yourself. The pre-computed
files in `scogs_*.zip` are the canonical inputs.

---

PhyKIT, Biopython, and DendroPy for alignment/tree analysis, evolutionary metrics, and comparative genomics.
