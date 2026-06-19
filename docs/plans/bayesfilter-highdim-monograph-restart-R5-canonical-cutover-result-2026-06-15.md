# R5 Canonical Cutover Result: Restarted High-Dimensional Monograph Block

**Date:** 2026-06-15  
**Runbook gate:** `R5` from `docs/plans/bayesfilter-highdim-monograph-restart-runbook-2026-06-15.md`

## Scope

Canonical switch from the non-canonical/intermediate high-dimensional block to
the restarted p47+p50-derived block after the staging surface passed R4
cutover-preflight review.

## What changed
Canonical chapter paths were updated by replacing their contents with the
staging chapter set that had passed R4 verification:
- `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
- `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
- `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`

No change to the canonical driver file was needed because `docs/main.tex` was
already wired to the expanded chapter list.  The cutover therefore consisted of
moving the now-reviewed restarted chapter content into the canonical chapter
paths.

## Verification

Command run:
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- `docs/main.pdf` was written successfully.
- Current canonical PDF length: 274 pages.
- No fatal LaTeX errors occurred.
- No undefined-reference warnings remained.
- No undefined-citation warnings remained.

## Gate result

- `G5` canonical cutover: **PASS**
- Token: `PASS_R5_RESTART_LAUNCH_AUTHORIZED`

## Judgment

The restarted p47+p50 high-dimensional block is now the canonical compiled book
surface.  The earlier failed/non-canonical state has been replaced by a block
that:
- compiles cleanly in the canonical driver,
- carries the intended expanded chapter architecture,
- passed staging-only source-fidelity and cutover-preflight review before
  switch.

## Current policy

- Treat the current `docs/main.tex` + `docs/chapters/ch33` and `ch34`--`ch38`
  block as the accepted canonical high-dimensional section.
- Preserve the restart plans and staging artifacts as historical execution and
  verification evidence.
- Any further work should now be treated as post-cutover refinement rather than
  restart recovery.

## Remaining caution

The cutover succeeded, but the source manuscripts may still remain richer in some
technical detail than the canonical monograph chapters.  That is no longer a
cutover blocker.  It is now only a possible future refinement target.
