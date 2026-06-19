# Reset memo: expanded high-dimensional block deep rewrite of new Chapter 35

## Date
2026-06-15

## Context
The post-migration integration audit identified `new ch35` as the second highest-value deep rewrite target after `new ch36`. The role normalization sweep had already made `new ch35` architecturally clear, but the chapter still carried the largest inherited body from the old compressed `ch34`, and it still mixed forward sparse-grid method content with material that properly belongs to the later shared fixed-branch chapter. The goal of this pass was therefore to make `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex` read as the true p47 sparse-grid / fixed-cloud method chapter.

## Decision / policy
Future sessions should assume the following unless a later pass replaces it:

1. `new ch35` is now explicitly a forward-method sparse-grid chapter, not a compressed whole-lane chapter.
2. The chapter now ends where the fixed-cloud scalar has been defined and exported, rather than carrying the full same-scalar derivative burden itself.
3. Shared fixed-branch derivative logic should now be treated as belonging to `new ch37`, not as a tail section that `new ch35` must still contain.
4. The monograph build remains green after this deep rewrite.

## What changed
- File: `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - Deep-trimmed the chapter so it now stops after the sparse-grid forward-method burden: low-dimensional cloud construction, active bands and Smolyak structure, value path, and worked fixed-cloud scalar example.
  - Removed the inherited downstream derivative/validation burden from the active chapter body by cutting the file at the start of the old derivative-tail material.
  - Added a new closing `What The Fixed-Cloud Scalar Exports Forward` section that explicitly names:
    - the carried Gaussian object,
    - the stored cloud,
    - the declared scalar,
    - and the forward runtime map exported to later chapters.
  - Added a `Methodological Boundary And Non-Claims` section so the chapter now closes with a proper lane-local scope boundary rather than flowing directly into inherited derivative material.

## Bugs / blockers resolved
- Symptom:
  - The chapter still read like the largest surviving seeded packet from the old compressed `ch34`, and it carried too much material that really belonged in the shared fixed-branch derivative chapter.
- Root cause:
  - `new ch35` had been seeded directly from the p47-heavy body of the old compressed chapter and still included the old combined lane burden.
- Resolution:
  - Re-cut the chapter around the fixed-cloud scalar and exported-object contract so it now functions as a true forward sparse-grid method chapter.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after the deep rewrite of `new ch35`.
- `docs/main.pdf` was written successfully (297 pages).
- No fatal LaTeX errors appeared.
- No undefined-reference or undefined-citation warnings remained in the final successful pass.

## Current policy
- Treat `new ch35` as a completed deep rewrite at the chapter-role level: it now carries the p47 sparse-grid / fixed-cloud method burden and exports the scalar forward.
- Preserve the green build while deeper source migration continues.
- The next most valuable rewrite target is now `new ch37`, because the two method chapters have both been structurally clarified and the shared fixed-branch chapter can now be strengthened against their clearer exports.

## Known limitations / cautions
- `new ch35` still contains inherited label namespaces and some source-local naming residue; this pass focused on chapter role and burden separation first.
- The chapter is now cleaner, but final prose/label normalization across the whole expanded block still lies ahead.

## Suggested next steps
1. Return to `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex` and strengthen it into a fuller shared branch-record / scalar-identity chapter now that both method chapters are more stable.
2. Rebuild `docs/main.tex` after that pass.
3. Then perform the next whole-block integration audit or a final normalization pass, depending on how complete the fixed-branch chapter becomes.
