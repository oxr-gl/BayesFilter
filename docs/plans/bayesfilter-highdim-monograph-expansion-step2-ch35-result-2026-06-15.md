# Reset memo: expanded high-dimensional block migration step 2 (new Chapter 35 normalization)

## Date
2026-06-15

## Context
After normalizing the new `ch34` into a true deterministic Gaussian / point-rule foundations chapter, the next migration step was to normalize the new `ch35` into the real p47 sparse-grid method chapter. The seeded file had been copied from the sparse-grid-heavy body of the old compressed `ch34`, so it already contained much of the right mathematical material, but its opening, chapter role, and monograph voice still needed to be aligned with the new expanded architecture.

## Decision / policy
Future sessions should assume the following unless a later migration step replaces it:

1. The new `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex` is now the active sparse-grid / fixed-cloud method chapter in the expanded block.
2. Its role is now explicitly:
   - low-dimensional cloud construction,
   - active bands and Smolyak structure,
   - merged cloud geometry,
   - sparse-grid value path,
   - fixed-cloud scalar,
   - bridge into the shared fixed-branch derivative chapter.
3. The chapter no longer needs to pretend to be the whole deterministic lane; that shared deterministic role now belongs to the normalized `new ch34`.
4. The monograph build remains green after this second migration step.

## What changed
- File: `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - Rewrote the opening so the chapter now clearly reads as the sparse-grid specialization of the deterministic Gaussian lane rather than as a transplanted continuation of the old compressed chapter.
  - Added an explicit architecture-level bridge from `new ch34` into `new ch35`, making clear that the shared point-rule foundation ends where sparse-grid specialization begins.
  - Replaced lingering imported-note voice in the touched parts of the file (`this note/report`) with chapter-local monograph language.
  - Reframed implementer-facing text so it is explicitly chapter-scoped and sparse-grid-lane-scoped.
  - Replaced the later defaults pointer with a reference to the shared fixed-branch chapter, which is where the architecture now wants those downstream constants/contracts to live.
  - Fixed the migrated worked-example cross-reference that had pointed to an equation label living only in the old compressed derivative chapter structure.

## Bugs / blockers resolved
- Symptom:
  - The new `ch35` still read like a seeded fragment of the old compressed `ch34`, with incomplete architectural framing and lingering note/report voice.
- Root cause:
  - The file was seeded directly from the p47-heavy body of the old compressed chapter without enough role-specific rewriting for the new expanded architecture.
- Resolution:
  - Narrowed and clarified the chapter role so `ch35` now presents itself as the true sparse-grid / fixed-cloud method chapter and no longer as the whole deterministic Gaussian lane.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after the `ch35` normalization pass.
- `docs/main.pdf` was written successfully (304 pages).
- No new fatal LaTeX errors appeared.
- No new undefined-reference warnings appeared in the final successful pass.

## Current policy
- Continue the migration according to the execution plan, with `new ch36` now the next active chapter to normalize into the true low-rank TT/KR retained-object method chapter.
- Preserve the green build after each chapter migration step.
- Do not let `new ch35` reacquire shared deterministic-foundation material that now belongs in `new ch34` or shared fixed-branch derivative material that now belongs in `new ch37`.

## Known limitations / cautions
- `new ch35` still contains inherited source-local labels and broader material that may later be redistributed into `new ch37`/`new ch38`; the present pass normalized role and voice first rather than completing all downstream redistribution at once.
- The major substantive migration challenge still lies ahead in `new ch36`, which remains the most survey-like seeded chapter in the expanded block.

## Suggested next steps
1. Normalize `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex` into the true p50 retained-object lane chapter.
2. Rebuild `docs/main.tex` after that pass.
3. Then continue to `new ch37` for the shared fixed-branch same-scalar chapter migration.
