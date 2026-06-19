# Reset memo: restarted staging migration step 2 (staging Chapter 35 from source truth)

## Date
2026-06-15

## Context
After the first true source-truth restart step rewrote the staging copy of `ch34`, the next R3 migration step was to rewrite the staging copy of `ch35` from the p47 sparse-grid / fixed-cloud source burden. This chapter owns the low-dimensional cloud construction, active-band and Smolyak structure, filtering value path, and fixed-cloud scalar. Under the restart crosswalk, it must become a self-contained p47-heavy method chapter rather than a transitional migrated copy of the previously expanded `new ch35`.

## Decision / policy
Future sessions should assume the following unless a later restart step replaces it:

1. The staging copy of `ch35` is now no longer primarily a transitional migrated chapter; it has been rewritten from source truth around the p47 sparse-grid method burden.
2. The staging `ch35` now clearly owns:
   - low-dimensional cloud construction,
   - tensor-product growth explanation,
   - active bands and Smolyak structure,
   - fixed merged cloud object,
   - filtering value path,
   - worked fixed-cloud scalar example,
   - explicit export of the fixed-cloud scalar forward.
3. The chapter now stops at the forward sparse-grid method burden; the shared fixed-branch derivative contract remains the responsibility of the later staging `ch37`.
4. The canonical compiled book remains untouched; this work exists only in the staging surface.

## What changed
- File: `docs/chapters_restart_staging/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - Replaced the transitional architecture with a source-truth rewrite around the p47 sparse-grid lane.
  - Rewrote the opening and scope so the chapter clearly reads as the sparse-grid specialization of the deterministic Gaussian lane.
  - Rebuilt the chapter around:
    - low-dimensional cloud construction,
    - one-dimensional/tensor-product rule family,
    - 3D sparse-grid preview,
    - source-order sparse-grid reconstruction,
    - value path and worked fixed-cloud scalar example,
    - explicit forward export contract and non-claims.
  - Kept the derivative burden out of this chapter on purpose so the later shared fixed-branch chapter can own it cleanly.

## Bugs / blockers resolved
- Symptom:
  - The staging chapter copies were initially isolated but still transitional; `ch35` was not yet a genuine p47 source-truth chapter.
- Root cause:
  - The staging surface was created by copying the active expanded files, not by re-authoring them from the source manuscripts.
- Resolution:
  - Rewrote the staging `ch35` directly from the p47 sparse-grid / fixed-cloud method burden under the restart crosswalk.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- The staging build rebuilt successfully after the second restarted migration step.
- `docs/main_highdim_restart_staging.pdf` was written successfully (259 pages).
- No fatal LaTeX errors occurred.
- The remaining undefined-reference warnings are inherited whole-book issues outside this local restart step and do not reflect failure of the staging `ch35` rewrite itself.

## Current policy
- Continue the restarted source-truth migration in `docs/chapters_restart_staging/` only.
- The next most important source-truth migration target is now the staging copy of `ch36`, which owns the p50 retained-object / TT / KR burden.
- Do not touch the canonical compiled surface during these migration steps.

## Known limitations / cautions
- Only the staging copies of `ch34` and `ch35` have now been genuinely rewritten from source truth.
- The remaining staging chapter set is still transitional and must not yet be treated as source-faithful.
- Whole-book undefined references remain present in the staging build, but they are inherited broad-book issues outside this local restart step.

## Suggested next steps
1. Rewrite `docs/chapters_restart_staging/ch36_highdim_low_rank_density_filters_and_kr_maps.tex` from the p50 retained-object / TT / KR source burden.
2. Rebuild the staging driver after that pass.
3. Continue the restarted migration chapter-by-chapter under the R3 staging reintegration subplan.
