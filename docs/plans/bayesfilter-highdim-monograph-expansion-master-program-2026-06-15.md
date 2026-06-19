# High-Dimensional Monograph Expansion Master Program

**Date:** 2026-06-15  
**Program ID:** `bayesfilter-highdim-monograph-expansion-master-program-2026-06-15.md`

## Status

Active governing program for the architectural expansion of the high-dimensional
nonlinear filtering block of the BayesFilter monograph.

This program supersedes the earlier assumption that the high-dimensional block
should be compressed into the current `ch33`--`ch37` arrangement with one p47
chapter, one p50 chapter, one HMC-consequence chapter, and one synthesis
chapter.  That architecture is now considered too cramped for the actual scope
of `p47` and `p50`.

## Governing purpose

The purpose of this expansion is to replace the compressed `ch33`--`ch37`
rewrite target with a larger high-dimensional block that:

1. treats `p47` and `p50` as authored source bases rather than as articles to be
   summarized;
2. synthesizes their shared structure into monograph-native chapters rather than
   assigning source ownership one-for-one at the chapter boundary level;
3. distributes the combined material across a realistic 4--5 chapter treatment
   after the shared foundations chapter;
4. keeps the block inside `\part{Nonlinear Filtering}` as the capstone bridge to
   the later generic HMC part;
5. preserves explicit target/gradient discipline, fixed-branch likelihood
   discipline, and validation/promotion discipline across the block.

## Program diagnosis

The earlier rewrite program improved build stability and claim discipline, but it
still targeted the wrong architectural endpoint.  The problem is not just local
cleanup.  The current architecture forces:

- the deterministic Gaussian/sparse-grid lane,
- the low-rank TT/KR lane,
- the shared fixed-branch likelihood/gradient abstraction,
- and the shared validation/promotion architecture

into too few chapter slots.  The result is compression, lost explanation, and a
monograph block that can read like a summary of the source manuscripts rather
than a canonical monograph treatment.

## Lane boundary

### In scope
- `docs/main.tex`
- the current high-dimensional block files and any new chapter files needed to
  replace them:
  - `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
  - current `docs/chapters/ch34`--`ch37` files as salvage material
  - new expanded block chapter files to be added under `docs/chapters/`
- `docs/plans` architecture plans, rewrite artifacts, reset memos, and result
  notes for this stream
- source manuscripts:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
  - `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

### Out of scope
- production `bayesfilter/` algorithmic code
- unrelated DPF / student baseline / controlled experiment lanes
- unrelated monograph chapters outside the high-dimensional block except where
  cross-references or chapter order must be updated

## Canonical source manuscripts

### p47 owns the strongest current exposition of
- deterministic Gaussian-surrogate filtering,
- standard-normal GHQ family,
- tensor labels,
- sparse-grid level,
- Smolyak combination,
- low-dimensional cloud construction,
- UKF relation,
- fixed-cloud scalar / derivative discipline.

### p50 owns the strongest current exposition of
- TT approximation toolkit,
- coordinate systems and retained coordinates,
- KR transport logic,
- squared-density / retained-object filtering recursion,
- fixed-branch likelihood construction,
- derivative warmups and branch identity,
- validation ladder and benchmark interpretation.

## Target architecture

The expanded high-dimensional block should answer one overarching question:

> Given the exact filtering target and the monograph’s target/gradient
> discipline, which approximation objects remain scientifically and
> computationally viable in the high-dimensional nonlinear regime, and what
> derivative and validation contracts make them usable for downstream inference?

## Preferred block shape

Keep `ch33` as the shared foundations chapter, then expand the current compressed
`ch34`--`ch37` target into **five** chapters after it.

### Chapter 33 — High-dimensional nonlinear filtering foundations
**File retained:**
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`

**Role:**
- exact filtering target,
- high-dimensional bottleneck,
- same-scalar groundwork,
- import of earlier target/derivative/HMC discipline.

### Chapter 34 — Deterministic Gaussian and point-rule foundations
**Planned file:**
- `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`

**Role:**
- deterministic Gaussian carried object,
- Gaussian projection,
- sigma-point / GHQ / rule-family foundations,
- point-rule comparison language needed before sparse-grid specialization.

**Source base:** p47 plus relevant monograph imports from earlier sigma-point chapters.

### Chapter 35 — Sparse-grid quadrature filtering and the fixed-cloud scalar
**Planned file:**
- `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`

**Role:**
- sparse-grid level,
- Smolyak construction,
- merged low-dimensional clouds,
- UKF relation at the rule-family level,
- filtering value path,
- fixed-cloud scalar object.

**Source base:** p47.

### Chapter 36 — Low-rank density filters, TT/KR maps, and retained objects
**Planned file:**
- `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`

**Role:**
- non-Gaussian carried objects,
- TT toolkit,
- rank plausibility,
- coordinate systems,
- conditional KR maps,
- squared-density / retained-object filtering recursion,
- low-rank transport/preconditioning context.

**Source base:** p50.

### Chapter 37 — Fixed-branch approximate likelihoods and same-scalar gradients
**Planned file:**
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`

**Role:**
- shared abstraction behind p47 and p50,
- branch identity,
- fixed-branch approximate scalar,
- analytical derivative of that same declared scalar,
- high-dimensional target/HMC admissibility consequences.

**Source base:** synthesized from p47 and p50, with forward reference to later
HMC chapters for generic sampler doctrine.

### Chapter 38 — Validation, defect calculus, and method promotion
**Planned file:**
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`

**Role:**
- benchmark architecture,
- finite-difference parity,
- rank / PSD / ESS / support / Jacobian diagnostics,
- defect calculus,
- promotion rules,
- industrial synthesis of the high-dimensional block.

**Source base:** synthesized from p47 and p50 plus the current synthesis lane.

## Optional 6th chapter

If Chapter 38 becomes too large, split it into:
- validation and benchmark architecture, and
- industrial synthesis / promotion ladder.

This is allowed, but the default target remains the 5-chapter post-foundation
block above.

## File strategy

This program uses **Option B**: add new chapter files.

The current `ch34`--`ch37` files should be treated as salvage material only.
They are not the fixed target architecture.  Implementation may mine them for
usable text, equations, and tables, but the canonical expanded block should be
built in new chapter files rather than by continuing to compress the source base
into the current file set.

## Rewrite phases

### Phase 0 — Expanded architecture and import/export contract
Purpose:
- define the new multi-chapter high-dimensional block,
- specify what each chapter imports and exports,
- decide how `docs/main.tex` should host the new files.

### Phase 1 — Chapter 34 deterministic Gaussian / point-rule foundations
Purpose:
- build the shared deterministic Gaussian-rule foundation chapter that prepares
  the reader for the sparse-grid specialization.

### Phase 2 — Chapter 35 sparse-grid quadrature and fixed-cloud scalar
Purpose:
- build the p47-heavy sparse-grid method chapter with its filtering scalar and
  cloud construction.

### Phase 3 — Chapter 36 low-rank density / TT / KR retained-object lane
Purpose:
- build the p50-heavy non-Gaussian low-rank method chapter.

### Phase 4 — Chapter 37 fixed-branch likelihoods and same-scalar gradients
Purpose:
- synthesize the shared fixed-branch scalar/gradient abstraction across the two
  method lanes and connect it to HMC admissibility.

### Phase 5 — Chapter 38 validation / defect / promotion chapter and block integration
Purpose:
- synthesize validation and promotion logic,
- update `docs/main.tex` to host the expanded block,
- repair references and verify that the enlarged block reads as one coherent
  monograph sequence.

## Governing editorial rules

1. The source manuscripts `p47` and `p50` are the authored source base.
2. The current compressed `ch34`--`ch37` files are salvage material only.
3. Shared structure between p47 and p50 should become monograph chapters in its
   own right where appropriate; do not force shared material back into source-
   specific method chapters.
4. Every chapter must state or imply clearly:
   - what it imports,
   - what it contributes,
   - what it exports.
5. Validation, fixed-branch derivative discipline, and HMC consequence discipline
   are shared cross-method themes, not leftovers to be compressed into chapter
   tails.
6. The enlarged block should remain inside the existing `\part{Nonlinear Filtering}`
   and should hand off to the later generic HMC part without duplicating its role.

## Verification criteria for the program

The expansion succeeds when:

1. the monograph no longer relies on a compressed two-source-chapter architecture
   for p47 and p50;
2. the expanded block reads as one coherent high-dimensional sequence rather than
   as a summarized digest of the source notes;
3. the deterministic Gaussian lane, non-Gaussian low-rank lane, fixed-branch
   derivative chapter, and validation/promotion chapter each have clear and
   non-overloaded roles;
4. `docs/main.tex` hosts the expanded block coherently inside `\part{Nonlinear Filtering}`;
5. the resulting monograph can replace the need to read the source notes for the
   canonical high-dimensional exposition.
