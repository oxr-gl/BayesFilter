# High-Dimensional Monograph Expansion Integration Plan For P47 And P50

**Date:** 2026-06-15  
**Target monograph:** `docs/main.tex` and the expanded high-dimensional filtering block in `docs/chapters/`

## Context

The current `ch33`--`ch37` arrangement is now judged too compressed for the
combined explanatory and methodological scope of `p47` and `p50`.  The monograph
should therefore stop treating those source manuscripts as material to squeeze
into two source-heavy chapters plus one consequence chapter and one synthesis
chapter.

Instead, the expanded block should synthesize p47 and p50 into a larger,
monograph-native sequence that keeps shared foundations, shared fixed-branch
likelihood/gradient discipline, and shared validation/promotion logic visible as
chapters in their own right.

## Current monograph location

The high-dimensional block remains at the end of `\part{Nonlinear Filtering}` in
`docs/main.tex`, after the generic sigma-point, square-root, particle, and DPF
chapters, and before the later generic HMC part.

This placement remains correct.  The expansion should happen **inside** this
existing part boundary, not by moving the block elsewhere in the book.

## Recommended expanded chapter map

### Retained shared foundation
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
  - exact target,
  - bottleneck,
  - same-scalar groundwork,
  - import of earlier target/derivative/HMC discipline.

### New Chapter 34
- `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - deterministic Gaussian carried object,
  - Gaussian projection,
  - point-rule family foundations,
  - comparator language needed before sparse-grid specialization.

### New Chapter 35
- `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - p47-heavy sparse-grid lane,
  - low-dimensional cloud construction,
  - UKF relation at the rule-family level,
  - filtering value path,
  - fixed-cloud scalar.

### New Chapter 36
- `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - p50-heavy non-Gaussian low-rank lane,
  - TT toolkit,
  - rank plausibility,
  - coordinate systems,
  - conditional KR maps,
  - squared-density / retained-object filtering recursion.

### New Chapter 37
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - shared fixed-branch approximate scalar abstraction,
  - same-scalar derivative discipline across both lanes,
  - branch identity,
  - HMC-admissibility consequences.

### New Chapter 38
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
  - validation,
  - finite-difference parity,
  - defect calculus,
  - promotion rules,
  - industrial synthesis.

## Optional sixth chapter

If Chapter 38 is too large, split it into:
- validation / benchmark architecture, and
- industrial synthesis / promotion ladder.

That is allowed, but the default planning target remains the five post-foundation
chapters above.

## What existing files mean under this plan

### Retain directly
- `ch33_highdim_nonlinear_filtering_foundations.tex`

### Treat as salvage material only
- `ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `ch35_highdim_particle_transport_tensor_filters.tex`
- `ch36_nonlinear_ssm_hmc_research_program.tex`
- `ch37_highdim_filtering_candidate_synthesis.tex`

These files are no longer the fixed architecture target.  They may be mined for:
- equations,
- tables,
- validated wording,
- transition paragraphs,
- and boundary sections,

but the canonical expanded block should be built in the new chapter files.

## Source-manuscript ownership under the expanded plan

### p47 primarily owns
- deterministic Gaussian-surrogate filtering,
- GHQ family and point-rule logic,
- sparse-grid level,
- Smolyak construction,
- merged cloud pedagogy,
- fixed-cloud scalar/gradient contract.

### p50 primarily owns
- TT approximation toolkit,
- retained-object / coordinate-system logic,
- KR conditional maps,
- squared-density sequential recursion,
- fixed-branch likelihood construction,
- derivative warmups,
- validation framing.

### Shared material to synthesize rather than source-own chapter-by-chapter
- exact-target vs approximate-target discipline,
- fixed-branch same-scalar derivative discipline,
- validation/defect/promotion logic,
- HMC-admissibility consequences.

## Recommended implementation order

1. Finalize the expanded architecture plan and file strategy.
2. Add the new chapter files under `docs/chapters/`.
3. Update `docs/main.tex` to host the expanded block.
4. Build the expanded `ch34` deterministic Gaussian foundation chapter.
5. Build the expanded `ch35` sparse-grid/fixed-cloud chapter.
6. Build the expanded `ch36` low-rank TT/KR chapter.
7. Build the expanded `ch37` fixed-branch same-scalar chapter.
8. Build the expanded `ch38` validation/promotion chapter.
9. Re-run integration, labels, bibliography, and block-to-HMC handoff cleanup.

## Verification plan

### Structural verification
1. Confirm the expanded chapter order still makes sense inside `\part{Nonlinear Filtering}`.
2. Confirm the block now has distinct shared chapters rather than compressing all
   shared material into tails of the method chapters.
3. Confirm the handoff to the later generic HMC part remains clear and non-duplicative.

### Content verification
4. Read the deterministic Gaussian lane chapters alone and confirm they replace
   the need to consult p47 for the canonical monograph treatment.
5. Read the low-rank TT/KR lane chapter alone and confirm it replaces the need to
   consult p50 for the canonical monograph treatment of that lane.
6. Read the fixed-branch same-scalar chapter and confirm it synthesizes the
   shared scalar/gradient abstraction across both lanes.
7. Read the final validation/promotion chapter and confirm it consumes the prior
   chapters rather than reopening derivations.

### Build verification
8. Rebuild `docs/main.tex` throughout the expansion.
9. Run BibTeX and rebuild as needed.
10. Fix labels, cross-references, bibliography issues, and part/chapter continuity
    problems introduced by the expansion.

## Deliverable

A larger high-dimensional monograph block in which:
- p47 and p50 are synthesized into a holistic chapter sequence,
- the shared target/gradient/validation logic becomes visible as part of the
  architecture itself,
- and the resulting monograph no longer reads like a compressed digest of the
  standalone notes.