# Reset memo: expanded high-dimensional block strengthening of new Chapter 37

## Date
2026-06-15

## Context
After the first deep source-migration pass on `new ch36` and the prior deep rewrite of `new ch35`, the next most valuable target was `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`. The chapter’s architectural role had already been corrected, but it still read more like a bridge chapter than a fully inhabited shared fixed-branch same-scalar chapter. The goal of this pass was therefore to strengthen `new ch37` with more of the concrete branch-record, finite-difference, and value-path-versus-derivative-path logic that the expanded architecture requires.

## Decision / policy
Future sessions should assume the following unless a later pass replaces it:

1. `new ch37` now carries a stronger shared fixed-branch / same-scalar abstraction than before.
2. The chapter no longer relies only on a thin front introduction plus inherited HMC-consequence residue; it now contains explicit sections on:
   - a canonical branch record and finite-difference contract,
   - the distinction between value-path and derivative-path objects,
   - shared fixed-branch same-scalar workflow across the two method lanes.
3. The monograph build remains green after this strengthening pass.
4. The next logical work is either a final whole-block integration/normalization pass or a targeted return to whichever chapter still most visibly carries inherited source-local residue.

## What changed
- File: `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - Added `A Canonical Branch Record And Finite-Difference Contract`.
  - Added `Value Path, Derivative Path, And What Is Actually Differentiated`.
  - Made the chapter more explicit about:
    - the frozen fixed ledger,
    - the recomputed differentiable ledger,
    - branch-valid finite-difference rows,
    - and the difference between objects needed to close the current scalar derivative and objects needed only to propagate the branch-consistent state to the next step.

## Bugs / blockers resolved
- Symptom:
  - Even after role normalization, `new ch37` still felt too thin for its architectural importance and relied too heavily on inherited HMC-consequence material.
- Root cause:
  - The chapter had been seeded from the old compressed `ch36`, so it inherited some policy conclusions but not enough of the shared fixed-branch contract mechanics.
- Resolution:
  - Strengthened the chapter with explicit branch-record and derivative-workflow sections so it now more fully inhabits the shared same-scalar role.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after strengthening `new ch37`.
- `docs/main.pdf` was written successfully (299 pages).
- No fatal LaTeX errors appeared.
- No undefined-reference or undefined-citation warnings remained in the final successful pass.

## Current policy
- Treat `new ch37` as materially strengthened and no longer merely a thin bridge chapter.
- Preserve the green build while any further whole-block normalization proceeds.
- The expanded block now has both method chapters and the shared fixed-branch chapter in a materially better state than after the first architecture sweep.

## Known limitations / cautions
- Some compatibility labels remain in place while the expanded block continues to stabilize.
- `new ch34`, `new ch35`, and `new ch36` still retain inherited label namespaces and some seeded wording; the architecture is now strong, but full monograph-native normalization is not complete.
- The next best move may now be a whole-block integration/normalization pass rather than another single-chapter deep rewrite.

## Suggested next steps
1. Run a fresh whole-block integration audit across `ch33` plus the new `ch34`--`ch38` sequence.
2. Decide from that audit whether the next priority is:
   - final normalization of labels/voice across the whole block, or
   - one more source-heavy deep rewrite in the chapter that still most visibly reads inherited.
3. Preserve the green build after that decision-driven pass.
