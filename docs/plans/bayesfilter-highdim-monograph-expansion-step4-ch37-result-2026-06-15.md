# Reset memo: expanded high-dimensional block migration step 4 (new Chapter 37 normalization)

## Date
2026-06-15

## Context
After normalizing the deterministic Gaussian foundation (`new ch34`), the sparse-grid method chapter (`new ch35`), and the retained-object lane chapter (`new ch36`), the next migration step was to turn `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex` into the true shared fixed-branch same-scalar chapter. The seeded file still read too much like the old HMC consequence chapter, with generic HMC exposition dominating the front of the chapter instead of the cross-method fixed-branch scalar/gradient abstraction that the expanded architecture requires.

## Decision / policy
Future sessions should assume the following unless a later migration step replaces it:

1. The new `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex` is now the active shared fixed-branch same-scalar chapter in the expanded block.
2. Its front architecture now states the cross-method role explicitly:
   - branch identity,
   - declared approximate scalar,
   - analytical derivative of that same scalar,
   - exact sense in which downstream HMC or gradient-based inference may consume it.
3. The generic sampler doctrine remains in the later HMC part; `new ch37` is now framed as a high-dimensional fixed-branch target-discipline chapter rather than a second general HMC chapter.
4. Transitional compatibility labels remain in the chapter so migrated references from the old compressed architecture continue to resolve while the deeper content migration proceeds.
5. The monograph build remains green after this migration step.

## What changed
- File: `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - Rewrote the front of the chapter to define the shared fixed-branch abstraction across the two method lanes rather than opening directly with generic HMC exposition.
  - Added three new architecture-level front sections:
    - `Why Fixed-Branch Discipline Is Shared Across The Two Lanes`
    - `Branch Identity And Scalar-Defining Structure`
    - `Fixed-Branch Approximate Likelihoods Across The Two Lanes`
  - Kept the later exported-defects and implementation-boundary material, but moved the chapter’s conceptual center to the cross-method scalar/gradient contract.
  - Added transitional compatibility equation/proposition labels so migrated references to the old HMC-consequence structure still resolve during the architecture transition.

## Bugs / blockers resolved
- Symptom:
  - The new `ch37` still read like a seeded HMC-consequence chapter rather than the shared fixed-branch derivative chapter promised by the expanded architecture.
- Root cause:
  - The file was seeded directly from the old compressed `ch36`, whose role was downstream HMC consequence framing rather than a shared scalar/gradient abstraction across both method lanes.
- Resolution:
  - Recast the front architecture and chapter purpose around the shared fixed-branch same-scalar logic before the inherited HMC-admissibility/export material.
  - Repaired the build-visible migrated label drift by adding transitional compatibility labels for the old HMC target/proposition references.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after the `ch37` normalization pass.
- `docs/main.pdf` was written successfully (296 pages).
- No fatal LaTeX errors appeared.
- No undefined-reference warnings remained in the final successful pass.

## Current policy
- Continue the migration according to the execution plan, with `new ch38` now the next active chapter to normalize into the shared validation / defect / promotion closeout chapter.
- Preserve the green build after each chapter migration step.
- Treat the compatibility labels in `new ch37` as transitional aids until the expanded block is fully normalized.

## Known limitations / cautions
- `new ch37` still contains inherited downstream HMC consequence material later in the chapter; the present pass normalized the front architecture first rather than finishing every later redistribution into `new ch38`.
- The final architectural payoff now depends on `new ch38` successfully becoming the true shared validation/promotion closeout chapter rather than just a reseeded synthesis chapter.

## Suggested next steps
1. Normalize `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex` into the true shared validation / defect / promotion closeout chapter.
2. Rebuild `docs/main.tex` after that pass.
3. Then perform the first post-migration integration audit across the whole expanded block.
