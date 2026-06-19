# Reset memo: restarted staging migration step 1 (staging Chapter 34 from source truth)

## Date
2026-06-15

## Context
After the restart-safe governance spine and isolated staging surface were created, the first actual source-truth migration step in staging was to rewrite the staging copy of `ch34` from the p47 source manuscript rather than continuing to trust the transitional migrated chapter body. This step intentionally begins with the deterministic Gaussian / point-rule foundations chapter because the restart crosswalk assigns it the front deterministic Gaussian / GHQ / point-rule burden from p47 and because later sparse-grid specialization depends on it.

## Decision / policy
Future sessions should assume the following unless a later restart step replaces it:

1. The restart has now begun real source-truth migration in staging.
2. The staging copy of `ch34` is no longer primarily a salvage/transitional file; it has been rewritten from scratch around the p47 foundations role.
3. The canonical compiled surface remains frozen; only the staging surface has been updated.
4. The next restart migration step should move to the staging copy of `ch35`, which owns the p47 sparse-grid / fixed-cloud method burden in the restart crosswalk.

## What changed
- File: `docs/chapters_restart_staging/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - Replaced the transitional inherited content with a fresh source-truth rewrite built from the p47 foundations burden.
  - The staging chapter now explicitly owns:
    - deterministic Gaussian carried object,
    - exact filtering and Gaussian projection,
    - deterministic point-rule family language,
    - rule-family comparison discipline,
    - export to sparse-grid specialization.
  - The staging chapter now reads as a true foundations chapter rather than as a front slice of a previously switched expanded block.

## Bugs / blockers resolved
- Symptom:
  - Even after the reset-safe staging split, the staging chapter copies still inherited the transitional expanded-block content and could not yet be trusted as source-truth integration.
- Root cause:
  - The staging surface was initially isolated by copying the current expanded chapters, but no source-truth rewrite had yet occurred there.
- Resolution:
  - Rewrote the staging `ch34` directly from the p47 foundations role defined in the restart crosswalk.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- The staging build rebuilt successfully after the first restarted migration step.
- `docs/main_highdim_restart_staging.pdf` was written successfully (281 pages).
- No fatal LaTeX errors occurred.
- The remaining undefined-reference warnings are inherited whole-book issues outside the specific high-dimensional restart step and do not reflect a failure of the chapter-local source-truth rewrite.

## Current policy
- Continue the restarted source-truth migration in `docs/chapters_restart_staging/` only.
- Do not touch the canonical compiled surface during these migration steps.
- Use `main_highdim_restart_staging.tex` as the active review/compile surface.

## Known limitations / cautions
- Only the staging copy of `ch34` has now been genuinely rewritten from source truth.
- The rest of the staging chapter set is still transitional and must not yet be treated as source-faithful.
- Whole-book undefined references remain present in the staging build, but they are inherited broad-book issues outside this local step.

## Suggested next steps
1. Rewrite `docs/chapters_restart_staging/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex` from the p47 sparse-grid / fixed-cloud source burden.
2. Rebuild the staging driver after that pass.
3. Continue the restarted migration chapter-by-chapter under the R3 staging reintegration subplan.
