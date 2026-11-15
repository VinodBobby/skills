### Step 7: Visualize — annotated DMS heatmap with hotspot callouts

The publication-style figure: DMS effect heatmap, sequence strip, structural
annotation track, with per-hotspot mechanism callouts above the heatmap.

**Align everything to one position axis.** Heatmap column `p`, sequence
letter `p`, every annotation bar covering residue `p` — all share `x = p`.
Verify a landmark before drawing:

```python
landmark_col = positions.index(12)  # column for KRAS pos 12
assert sequence[landmark_col] == "G", f"alignment broken at col {landmark_col}"
```

A 1-2 residue misalignment between heatmap and annotation track is a common,
visually subtle error. If you've cross-joined two coordinate systems and any
join was off-by-N, the whole figure is silently wrong. Verify here.

**Heatmap + sequence + annotation track + callouts:**

```python
import matplotlib.pyplot as plt
import numpy as np

vlim = max(abs(np.nanmin(dms_matrix)), abs(np.nanmax(dms_matrix)))

fig, axes = plt.subplots(
    nrows=4, ncols=1, figsize=(max(8, 0.15 * len(positions)), 6),
    gridspec_kw={"height_ratios": [0.5, 4, 0.3, 0.5]}, sharex=True,
)
ax_callouts, ax_heat, ax_seq, ax_anno = axes

# Heatmap — symmetric diverging (RdBu_r); center on 0 for ΔΔG-style data
im = ax_heat.imshow(
    dms_matrix, aspect="auto", cmap="RdBu_r",
    vmin=-vlim, vmax=vlim,
    extent=(0, len(positions), 20, 0),
)
ax_heat.set_yticks(np.arange(20) + 0.5)
ax_heat.set_yticklabels(list(amino_acid_order))
ax_heat.set_ylabel("Substitution")

# Mark WT cells (box, no fill) — distinguish "WT" from "not measured"
for col, p in enumerate(positions):
    wt_aa = sequence[col]
    if wt_aa in amino_acid_order:
        row = amino_acid_order.index(wt_aa)
        ax_heat.add_patch(plt.Rectangle(
            (col, row), 1, 1, fill=False, edgecolor='black', linewidth=0.5,
        ))

# Sequence strip — one monospace letter per column
ax_seq.set_xlim(0, len(positions))
ax_seq.set_ylim(0, 1)
ax_seq.set_yticks([])
for col, letter in enumerate(sequence):
    ax_seq.text(col + 0.5, 0.5, letter, ha="center", va="center",
                family="monospace", fontsize=8)

# Annotation track — region colors (top half) + core bar (bottom half)
anno_by_pos = {a["position"]: a for a in struct["data"]["annotations"]}
region_colors = {"interface": "#1f77b4", "ligand": "#ff7f0e",
                 "both": "#2ca02c", "other": "#cccccc"}
for col, p in enumerate(positions):
    a = anno_by_pos.get(p, {})
    ax_anno.add_patch(plt.Rectangle(
        (col, 0.5), 1, 0.5, facecolor=region_colors.get(a.get("region", "other"), "#cccccc"),
    ))
    if a.get("is_core"):
        ax_anno.add_patch(plt.Rectangle((col, 0.0), 1, 0.5, facecolor="black"))
ax_anno.set_xlim(0, len(positions))
ax_anno.set_ylim(0, 1)
ax_anno.set_yticks([0.25, 0.75])
ax_anno.set_yticklabels(["core", "region"])
ax_anno.set_xlabel("Residue position")

# Callout row — per-hotspot mechanism boxes linked to clusters by brackets
for cluster, mechanism, top_features in hotspot_results:
    cluster_cols = [positions.index(p) for p in cluster if p in positions]
    if not cluster_cols:
        continue
    c_left, c_right = min(cluster_cols), max(cluster_cols)
    center = (c_left + c_right) / 2
    ax_heat.plot([c_left, c_right + 1], [0, 0], "k-", lw=2)
    label_lines = [f"MECHANISM: {mechanism}"] + [f"  {fl}" for fl in top_features[:3]]
    ax_callouts.text(center, 0.5, "\n".join(label_lines),
                     ha="center", va="center", fontsize=7,
                     bbox=dict(facecolor="white", edgecolor="black"))
    ax_callouts.plot([center, center], [0, -0.3], "k-", lw=0.5)
ax_callouts.set_xlim(0, len(positions))
ax_callouts.set_ylim(0, 1)
ax_callouts.axis("off")

fig.colorbar(im, ax=ax_heat, label="DMS effect (ΔΔG kcal/mol)")
plt.savefig("dms_hotspots_annotated.png", dpi=200, bbox_inches="tight")
```

**Three cell-color rules to get right:**
- Real measurement → diverging colour
- WT cell → boxed (the black outline above), value-cell colour = centre
- Not measured → distinct colour (e.g. light grey, not white — white reads
  as "neutral" against the diverging palette)

**Long proteins**: for >300 residues, split into multiple horizontal panels
(one panel per domain) rather than shrinking column width — the per-residue
detail disappears below ~3 pixels per column.

**Reproducing a published panel**: verify *its* track alignment before
treating it as ground truth. Published DMS panels do carry registration
errors (the KRAS Fig 1i in the original paper is shifted +2 relative to its
own sequence — see `tooluniverse-protein-structural-annotation-pdb` pitfalls).

---
