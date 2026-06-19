# Reset memo: expanded high-dimensional block deep rewrite of new Chapter 36

## Date
2026-06-15

## Context
The first post-migration integration audit identified `new ch36` as the chapter with the largest remaining fidelity gap to the p50 source manuscript. The front architecture had already been improved, but the chapter still behaved too much like the old broad survey chapter rather than the true retained-object / TT / KR chapter promised by the expanded architecture. This pass therefore targeted `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex` as the first deep source-migration rewrite after the architecture sweep.

## Decision / policy
Future sessions should assume the following unless a later pass replaces it:

1. `new ch36` is now explicitly organized around the retained-object lane rather than around a generic survey of non-Gaussian alternatives.
2. The chapter now front-loads the p50-specific burdens that were previously under-carried:
   - exact filtering target and recursive bottleneck,
   - coordinate systems,
   - retained-object flow,
   - TT/KR lane identity.
3. The monograph build remains green after this deeper rewrite.
4. The next highest-value deep rewrite target is now `new ch35`, followed by strengthening `new ch37`.

## What changed
- File: `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - Rewrote the front structure again so the chapter now includes:
    - `Orientation And Scope`
    - `Running Example And Notation Discipline`
    - `Exact Filtering Target And Recursive Bottleneck`
    - `Coordinate Systems, Conditional Maps, And Retained Objects`
  - Repositioned the chapter so the later TT and KR sections now sit under an explicitly retained-object architecture rather than under a broad alternatives-first survey framing.
  - Kept the later seeded TT/KR body for now, but made its conceptual placement much more faithful to the p50 source manuscript.

## Bugs / blockers resolved
- Symptom:
  - The chapter still read like a survey of particles/transports/tensors even after the first architecture normalization pass.
- Root cause:
  - The file had been seeded from the old compressed `ch35`, which spread focus too evenly across broad non-Gaussian alternatives instead of centering the p50 retained-object logic.
- Resolution:
  - Rewrote the front architecture to restore the p50 explanatory burden before the inherited TT/KR body begins.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after the deep rewrite of `new ch36`.
- `docs/main.pdf` was written successfully (297 pages).
- No fatal LaTeX errors appeared.
- No undefined-reference or undefined-citation warnings remained in the final successful pass.

## Current policy
- Treat `new ch36` as the first expanded chapter that has gone beyond role-normalization into a genuine source-directed deep rewrite.
- Preserve the green build while deeper source migration continues.
- The next deep source rewrite should target `new ch35`, not `new ch34`.

## Known limitations / cautions
- `new ch36` still contains inherited seeded body material deeper in the chapter; this pass restored the p50 architecture and object flow first rather than rewriting every later section line-by-line.
- Transitional compatibility labels remain in place while the expanded block is still normalizing.

## Suggested next steps
1. Deep-rewrite `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex` so the sparse-grid lane carries more of the p47 explanatory and method-contract burden.
2. Rebuild `docs/main.tex` after that pass.
3. Then return to `new ch37` to strengthen the shared fixed-branch chapter once the two method chapters are more source-faithful.
