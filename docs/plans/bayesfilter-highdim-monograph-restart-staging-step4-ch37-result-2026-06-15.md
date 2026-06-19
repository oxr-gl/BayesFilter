# Reset memo: restarted staging migration step 4 (staging Chapter 37 from shared p47+p50 source burden)

## Date
2026-06-15

## Context
After rewriting the staging copies of `ch34`, `ch35`, and `ch36` from source truth, the next R3 migration step was to rewrite the staging copy of `ch37` from the shared p47+p50 fixed-branch source burden. This chapter is the cross-method contract chapter of the restarted block: it must not be merely a bridge or an inherited HMC-consequence note. It must explicitly own branch identity, structural ledgers, finite-difference branch-validity logic, and the exact distinction between declared approximate scalar targets and downstream HMC admissibility.

## Decision / policy
Future sessions should assume the following unless a later restart step replaces it:

1. The staging copy of `ch37` is now no longer primarily a transitional bridge chapter; it has been rewritten from the shared p47+p50 fixed-branch source burden.
2. The staging `ch37` now clearly owns:
   - the shared fixed-branch contract,
   - the canonical branch record,
   - fixed structural ledger versus recomputed differentiable ledger,
   - finite-difference branch-validity logic,
   - value-path versus derivative-path distinction,
   - exact-target versus approximate-target HMC admissibility boundary.
3. The chapter now functions as the shared scalar/gradient contract chapter of the restarted block rather than as a generic HMC-consequence summary.
4. The canonical compiled surface remains untouched; this work exists only in the staging surface.

## What changed
- File: `docs/chapters_restart_staging/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - Replaced the transitional content with a source-truth rewrite around the shared p47+p50 fixed-branch burden.
  - Added explicit sections on:
    - why fixed-branch discipline is shared across the two lanes,
    - the canonical branch record,
    - fixed-branch approximate likelihoods across the two lanes,
    - finite-difference branch-validity logic,
    - value path vs derivative path,
    - approximate-target versus exact-target HMC admissibility.
  - Reframed the chapter so it now behaves as the cross-method branch-record / same-scalar contract chapter that the restarted architecture requires.

## Bugs / blockers resolved
- Symptom:
  - The staging copy of `ch37` would otherwise have remained a thin bridge or inherited HMC-consequence chapter, which would have broken the shared fixed-branch architecture of the restart block.
- Root cause:
  - The staging surface initially inherited the same transitional chapter content produced during the failed/non-canonical operation.
- Resolution:
  - Rewrote the staging `ch37` directly from the shared p47 same-scalar and p50 fixed-branch source burdens.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- The staging build rebuilt successfully after the fourth restarted migration step.
- `docs/main_highdim_restart_staging.pdf` was written successfully (259 pages).
- No fatal LaTeX errors occurred.
- The remaining undefined-reference warnings are inherited whole-book issues outside this local restart step and do not reflect failure of the staging `ch37` rewrite itself.

## Current policy
- Continue the restarted source-truth migration in `docs/chapters_restart_staging/` only.
- The next source-truth migration target is now the staging copy of `ch38`, which should become the shared validation / defect / promotion closeout from p47+p50 validation and current synthesis salvage.
- Do not touch the canonical compiled surface during these migration steps.

## Known limitations / cautions
- Only the staging copies of `ch34`, `ch35`, `ch36`, and `ch37` have now been genuinely rewritten from source truth.
- The final staging chapter (`ch38`) is still transitional and must not yet be treated as source-faithful.
- Whole-book undefined references remain present in the staging build, but they are inherited broad-book issues outside this local restart step.

## Suggested next steps
1. Rewrite `docs/chapters_restart_staging/ch38_highdim_validation_defect_calculus_and_promotion.tex` from the shared p47+p50 validation / promotion burden.
2. Rebuild the staging driver after that pass.
3. Then run the first staging whole-block verification under the R4 subplan.
