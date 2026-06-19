# Chapter Crosswalk: Restarted P47+P50 Reintegration

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Map p47 and p50 source truth into the intended destination chapters for the
restart, while clearly distinguishing source truth from salvage chapter sets.

## Foundation retained directly

### `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
Retain as the foundation chapter.

Owns:
- exact filtering target,
- likelihood normalizer discipline,
- same-scalar groundwork,
- high-dimensional failure-mode setup.

Source migration policy:
- no major p47/p50 transplant here,
- only light cross-reference adjustment if required later.

## Target destination chapters from source truth

### Destination: deterministic Gaussian / point-rule foundations
**Target chapter file:**
- `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`

**Primary source truth:**
- p47 front deterministic Gaussian / GHQ / point-rule foundations

**Should own:**
- Gaussian carried object,
- Gaussian projection,
- point-rule family language,
- rule-family comparison before sparse-grid specialization.

### Destination: sparse-grid / fixed-cloud method chapter
**Target chapter file:**
- `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`

**Primary source truth:**
- p47 sparse-grid construction and value-path material

**Should own:**
- low-dimensional cloud construction,
- active bands,
- Smolyak structure,
- merged clouds,
- filtering value path,
- fixed-cloud scalar,
- sparse-grid lane non-claims.

### Destination: retained-object TT/KR chapter
**Target chapter file:**
- `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`

**Primary source truth:**
- p50 retained-object / TT / KR / coordinate-system material

**Should own:**
- exact recursive bottleneck,
- coordinate systems,
- retained-object flow,
- TT toolkit,
- rank plausibility,
- conditional KR maps,
- squared-density / retained-object recursion.

### Destination: shared fixed-branch / same-scalar chapter
**Target chapter file:**
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`

**Primary source truth:**
- p47 same-scalar / analytical gradient discipline
- p50 fixed-branch likelihood construction and derivative theory

**Should own:**
- branch identity,
- fixed structural ledger versus recomputed numerical ledger,
- declared approximate scalar,
- finite-difference branch-validity logic,
- exact-target vs approximate-target HMC admissibility consequences.

### Destination: validation / defect / promotion closeout
**Target chapter file:**
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`

**Primary source truth:**
- p47 verification/validation architecture
- p50 validation ladder and benchmark interpretation
- current synthesis lane for defect-calculus / promotion packaging only as salvage

**Should own:**
- benchmark roles,
- validation ledgers,
- defect calculus,
- promotion rules,
- source-risk / non-claim closeout.

## Salvage-only chapter sets

### Old compressed block (salvage only)
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

Use only for:
- equations,
- wording fragments,
- tables,
- existing cross-reference ideas,
- previously repaired claim-discipline text.

### Current expanded block (salvage-only transitional state)
- `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
- `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
- `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`

These are the target filenames, but their current contents are transitional and
must not be assumed source-faithful until the restart integration completes.

## Cutover principle

The canonical compiled book may switch only after the staged versions of the
five destination chapters above are judged complete against p47/p50 source truth
and the whole-block audit passes.