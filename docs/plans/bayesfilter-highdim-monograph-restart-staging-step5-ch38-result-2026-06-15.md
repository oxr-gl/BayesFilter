# Reset memo: restarted staging migration step 5 (staging Chapter 38 from shared p47+p50 validation and promotion burden)

## Date
2026-06-15

## Context
After rewriting the staging copies of `ch34`, `ch35`, `ch36`, and `ch37` from source truth, the final R3 chapter migration step was to rewrite the staging copy of `ch38` from the shared p47+p50 validation, defect, and promotion burden. This chapter is the closeout of the restarted high-dimensional block: it should no longer be a salvage synthesis chapter first and a validation chapter second. It must explicitly own the validation architecture, benchmark-role ladder, defect calculus, and promotion logic that the previous chapters feed into.

## Decision / policy
Future sessions should assume the following unless a later restart step replaces it:

1. The staging copy of `ch38` is now no longer primarily a transitional synthesis carryover; it has been rewritten from the shared p47+p50 validation and promotion burden.
2. The staging `ch38` now clearly owns:
   - validation architecture and benchmark roles,
   - finite-difference parity as a first shared gate,
   - downstream defect calculus,
   - promotion logic and non-claims.
3. The chapter now functions as the proper closeout of the restarted high-dimensional block.
4. The canonical compiled surface remains untouched; this work exists only in the staging surface.

## What changed
- File: `docs/chapters_restart_staging/ch38_highdim_validation_defect_calculus_and_promotion.tex`
  - Replaced the transitional content with a source-truth rewrite around the shared p47+p50 validation and promotion burden.
  - Rebuilt the front and body around:
    - validation architecture and benchmark roles,
    - finite-difference verification as the first shared gate,
    - defect calculus and promotion rules,
    - non-claim boundaries.
  - Reframed the chapter so it now acts as the shared validation / defect / promotion closeout for the restarted block rather than as a repackaged inherited synthesis note.

## Bugs / blockers resolved
- Symptom:
  - The staging copy of `ch38` would otherwise have remained a salvage synthesis chapter and would not have carried the validation architecture required by the restart crosswalk.
- Root cause:
  - The staging surface initially inherited the same transitional chapter content created during the failed/non-canonical operation.
- Resolution:
  - Rewrote the staging `ch38` directly from the shared p47+p50 validation/promotion burden.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- The staging build rebuilt successfully after the fifth restarted migration step.
- `docs/main_highdim_restart_staging.pdf` was written successfully (250 pages).
- No fatal LaTeX errors occurred.
- The remaining undefined-reference warnings are inherited whole-book issues outside this local restart step and do not reflect failure of the staging `ch38` rewrite itself.

## Current policy
- The chapter-level source-truth migration in staging is now complete for the restarted high-dimensional block.
- The next restart phase should move from chapter migration to R4 staging-only verification and whole-block staged review.
- Do not touch the canonical compiled surface during these verification phases.

## Known limitations / cautions
- Whole-book undefined references remain present in the staging build, but they are inherited broad-book issues outside the local restarted block.
- The staged block still needs a dedicated whole-block review against p47 and p50 before any cutover can be considered.
- Transitional compatibility assumptions may still remain inside the staged chapters even after source-truth rewriting; those must be handled in R4.

## Suggested next steps
1. Run the first full R4 staging-only verification pass on the staged block.
2. Review the staged PDF for source-fidelity, whole-block coherence, labels, and source-map consistency.
3. Decide from that review whether the block is ready for cutover-preflight or whether another targeted staging refinement pass is needed.
