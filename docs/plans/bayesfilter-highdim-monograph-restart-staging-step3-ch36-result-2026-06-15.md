# Reset memo: restarted staging migration step 3 (staging Chapter 36 from source truth)

## Date
2026-06-15

## Context
After rewriting the staging copies of `ch34` and `ch35` from p47 source truth, the next R3 migration step was to rewrite the staging copy of `ch36` from the p50 retained-object / TT / KR source burden. This chapter is the densest source-fidelity target in the whole restart because it must carry the exact recursive bottleneck, coordinate systems, retained-object flow, TT toolkit, KR transport role, and squared-density / retained-object recursion in a way that the earlier survey-like versions did not.

## Decision / policy
Future sessions should assume the following unless a later restart step replaces it:

1. The staging copy of `ch36` is now no longer primarily a transitional migrated chapter; it has been rewritten from p50 source truth around the retained-object / TT / KR burden.
2. The staging `ch36` now clearly owns:
   - exact recursive bottleneck,
   - coordinate-system and retained-object flow,
   - TT approximation toolkit,
   - rank plausibility,
   - conditional KR maps,
   - squared-density / retained-object recursion,
   - lane-local diagnostics and non-claims.
3. The chapter now functions as the main p50 retained-object lane chapter in staging rather than as a broad survey chapter.
4. The canonical compiled surface remains untouched; this work exists only in the staging surface.

## What changed
- File: `docs/chapters_restart_staging/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - Replaced the transitional architecture with a source-truth rewrite around the p50 retained-object burden.
  - Rebuilt the front and middle of the chapter around:
    - orientation and scope,
    - running example and notation,
    - exact filtering target and recursive bottleneck,
    - coordinate systems and retained objects,
    - TT toolkit and rank plausibility,
    - TT/KR retained-object lane, and
    - squared-density / retained-object recursion.
  - Kept the chapter’s methodological boundary and diagnostics lane-local rather than letting them spill prematurely into the shared fixed-branch or validation chapters.

## Bugs / blockers resolved
- Symptom:
  - The staging copy of `ch36` would otherwise have remained the biggest fidelity gap in the restarted block because the inherited expanded version still behaved too much like a broad survey of non-Gaussian alternatives.
- Root cause:
  - The staging surface initially inherited the same transitional content that had been produced during the failed/non-canonical operation.
- Resolution:
  - Rewrote the staging `ch36` directly from the p50 retained-object / TT / KR source burden and chapter crosswalk.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- The staging build rebuilt successfully after the third restarted migration step.
- `docs/main_highdim_restart_staging.pdf` was written successfully (261 pages).
- No fatal LaTeX errors occurred.
- The remaining undefined-reference warnings are inherited whole-book issues outside this local restart step and do not reflect failure of the staging `ch36` rewrite itself.

## Current policy
- Continue the restarted source-truth migration in `docs/chapters_restart_staging/` only.
- The next source-truth migration target is now the staging copy of `ch37`, which should synthesize p47 same-scalar and p50 fixed-branch derivative theory.
- Do not touch the canonical compiled surface during these migration steps.

## Known limitations / cautions
- Only the staging copies of `ch34`, `ch35`, and `ch36` have now been genuinely rewritten from source truth.
- The remaining staging chapter set (`ch37`, `ch38`) is still transitional and must not yet be treated as source-faithful.
- Whole-book undefined references remain present in the staging build, but they are inherited broad-book issues outside this local restart step.

## Suggested next steps
1. Rewrite `docs/chapters_restart_staging/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex` from the shared p47+p50 fixed-branch source burden.
2. Rebuild the staging driver after that pass.
3. Continue the restarted migration chapter-by-chapter under the R3 staging reintegration subplan.
