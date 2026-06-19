# Reset memo: expanded high-dimensional block migration step 3 (new Chapter 36 normalization)

## Date
2026-06-15

## Context
After normalizing the new `ch34` and `ch35`, the next migration step was to turn
`docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex` into the
true p50 retained-object chapter. The seeded file still looked too much like the
old survey-style `ch35`: it mixed particles, generic transport, TT, and TN
compression with insufficient p50-specific retained-object framing. The goal of
this pass was therefore to recast the front of the chapter so the retained-object
lane became explicit and source-oriented without yet completing every later
section rewrite.

## Decision / policy
Future sessions should assume the following unless a later migration step
replaces it:

1. The new `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
   is now the active p50-oriented low-rank retained-object chapter in the
   expanded block.
2. Its front matter now clearly states the intended role:
   - low-rank non-Gaussian retained objects,
   - TT approximation toolkit,
   - coordinate systems,
   - conditional KR maps,
   - squared-density repair and retained-object recursion.
3. The chapter still contains inherited broad comparator material deeper in the
   body, but its architectural framing no longer presents itself merely as a
   survey chapter.
4. The monograph build remains green after this migration step.

## What changed
- File: `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - Rewrote the front of the chapter to introduce the p50 retained-object lane in
    monograph-native terms.
  - Added a proper orientation/scope section that distinguishes:
    - the exact target,
    - the adaptive low-rank approximation family,
    - and the later fixed-branch scalar/derivative objects.
  - Added a running-example / notation-discipline section so the TT/KR lane now
    begins with its own retained-object bookkeeping rather than falling directly
    into a survey opening.
  - Kept the broad comparative section on “Three Ways To Escape A Gaussian,” but
    repositioned it behind the retained-object framing so the chapter no longer
    opens as if all non-Gaussian lanes are equally central.
  - Added a transitional compatibility proposition label so migrated references
    from the old compressed architecture still resolve while deeper content
    migration continues.

## Bugs / blockers resolved
- Symptom:
  - The new `ch36` still read primarily like the old broad survey chapter rather
    than the p50-heavy retained-object chapter promised by the expanded
    architecture.
- Root cause:
  - The file was seeded directly from the old compressed `ch35`, which distributed
    attention too evenly across particles, generic transport, TT/QTT PDE filters,
    and TN covariance compression.
- Resolution:
  - Recast the opening architecture and chapter purpose around the retained-object
    TT/KR lane before the inherited comparator material.
  - Repaired the only build-visible migrated reference issue (`prop:bf-hd-corrected-proposal`) with a compatibility label so the build stayed green while the substantive migration continues.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after the `ch36` normalization pass.
- `docs/main.pdf` was written successfully (301 pages).
- No fatal LaTeX errors appeared.
- No undefined-reference warnings remained in the final successful pass.

## Current policy
- Continue the migration according to the execution plan, with `new ch37` now the
  next active chapter to normalize into the shared fixed-branch same-scalar
  derivative chapter.
- Preserve the green build after each chapter migration step.
- Treat the current compatibility labels in `new ch36` as transitional aids while
  the rest of the expanded block is still being migrated.

## Known limitations / cautions
- `new ch36` still contains inherited survey-like material in the deeper body;
  this pass normalized the front architecture first rather than completing a full
  p50-only redistribution of every later section.
- The most important remaining structural migration now lies in `new ch37`, where
  shared fixed-branch scalar/gradient material still needs to be synthesized out
  of seeded HMC consequence content.

## Suggested next steps
1. Normalize `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex` into the true shared fixed-branch same-scalar chapter.
2. Rebuild `docs/main.tex` after that pass.
3. Then continue to `new ch38` for the shared validation / defect / promotion closeout.
