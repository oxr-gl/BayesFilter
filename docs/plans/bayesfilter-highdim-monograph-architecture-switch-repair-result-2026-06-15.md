# Reset memo: architecture-switch reference repair and expanded block activation

## Date
2026-06-15

## Context
After the user approved the architecture-expansion strategy, the high-dimensional
block was switched from the compressed `ch33`--`ch37` arrangement to a new
expanded block with fresh target chapter files and an updated `docs/main.tex`
chapter list. The first post-switch build succeeded but exposed inherited label
and chapter-reference drift from the old compressed architecture. That drift had
to be repaired before the expanded block could be treated as a stable active
structure.

## Decision / policy
Future sessions should assume the following unless a later reset memo supersedes
it:

1. The expanded high-dimensional block is now the active monograph structure in
   `docs/main.tex`.
2. The new chapter files are live and compiled:
   - `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
   - `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
   - `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
   - `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
   - `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
3. The old compressed `ch34`--`ch37` files remain salvage material only; they are
   no longer the active monograph architecture target.
4. Compatibility labels were added in the new chapters so the architecture switch
   can compile while deeper content migration proceeds.
5. The monograph currently builds cleanly after the architecture switch and the
   immediate reference-drift repair.

## What changed
- File: `docs/main.tex`
  - Replaced the old compressed high-dimensional block inputs with the new
    expanded block chapter list.
- File: `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - Seeded from the front/shared-foundation portion of the old `ch34` so the new
    chapter is no longer an empty scaffold.
- File: `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - Seeded from the sparse-grid/value-path portion of the old `ch34`.
  - Repaired a migrated reference so the worked derivative example no longer
    points to an equation label that lives in the old chapter file.
- File: `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - Seeded from the old `ch35` content.
  - Added compatibility label `ch:bf-highdim-particle-transport-tensor` so old
    references continue to resolve while migration proceeds.
- File: `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - Seeded from the old `ch36` content.
  - Added compatibility label `ch:bf-highdim-hmc-research`.
  - Repaired one migrated equation reference from the old `eq:p31-score` target
    to the local worked-score equation now present in the expanded structure.
- File: `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
  - Seeded from the old `ch37` content.
  - Added compatibility label `ch:bf-highdim-candidate-synthesis`.

## Bugs / blockers resolved
- Symptom:
  - The first build after switching `docs/main.tex` to the expanded chapter list
    still produced undefined-reference warnings due to inherited references to
    old chapter labels and moved equation labels.
- Root cause:
  - The new expanded files had seeded content copied from the old compressed
    chapters, so the text still referred to old labels such as
    `ch:bf-highdim-hmc-research`, `ch:bf-highdim-particle-transport-tensor`,
    `ch:bf-highdim-candidate-synthesis`, and a moved equation label inside the
    derivative example.
- Resolution:
  - Added compatibility chapter labels to the new expanded files where the same
    conceptual chapter role still exists under the new architecture.
  - Repaired the remaining migrated equation reference that no longer had a local
    target.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The expanded chapter list now compiles successfully.
- `docs/main.pdf` was written successfully (304 pages).
- No fatal LaTeX errors remain after the reference repair.
- The previous undefined-reference warnings from the architecture switch were
  cleared in the final successful build pass.

## Current policy
- Continue migration/rewrite work against the new expanded chapter files, not the
  old compressed chapter files.
- Preserve the green build after each migration step.
- Treat compatibility labels as transitional aids; they may later be removed once
  the new block is fully normalized and all references are updated semantically.

## Known limitations / cautions
- The new chapter files are seeded from old material; they are structurally live
  but not yet fully rewritten into their final architecture-specific roles.
- The current success is an architecture activation and reference-repair result,
  not the final substantive migration of p47 and p50 into the new block.
- Some chapter labels currently exist both in old salvage files and in new active
  files; the active `main.tex` no longer inputs the old ones, but future cleanup
  should still keep the distinction clear.

## Suggested next steps
1. Begin the actual chapter-by-chapter migration into the new expanded files,
   starting with the deterministic Gaussian / sparse-grid side (`new ch34` and
   `new ch35`).
2. Rebuild `docs/main.tex` after each migration step.
3. As the new chapters become fully native, replace transitional compatibility
   references with semantically final labels and remove no-longer-needed legacy
   assumptions.
