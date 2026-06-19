# R4 Staging Verification Result: Restarted High-Dimensional Block

**Date:** 2026-06-15  
**Runbook gate:** `R4` from `docs/plans/bayesfilter-highdim-monograph-restart-runbook-2026-06-15.md`

## Scope

Whole-block review of the restarted staging surface:
- `docs/main_highdim_restart_staging.tex`
- `docs/chapters_restart_staging/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
- `docs/chapters_restart_staging/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
- `docs/chapters_restart_staging/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
- `docs/chapters_restart_staging/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters_restart_staging/ch38_highdim_validation_defect_calculus_and_promotion.tex`

## Build result

Command run:
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- `docs/main_highdim_restart_staging.pdf` was written successfully.
- Current staged PDF length: 259 pages.
- No fatal LaTeX errors occurred.

## Source-fidelity status by chapter

### Staging `ch34`
Status: materially source-truth-driven for the p47 foundations role.
- It now clearly owns deterministic Gaussian carried object, exact filtering / Gaussian projection, deterministic point-rule family language, and export to sparse-grid specialization.
- It no longer reads mainly like a front fragment of a previously switched expanded block.

### Staging `ch35`
Status: materially source-truth-driven for the p47 sparse-grid / fixed-cloud method role.
- It now clearly owns low-dimensional cloud construction, active bands, Smolyak structure, merged cloud object, filtering value path, and fixed-cloud scalar export.
- The derivative burden is no longer incorrectly retained here.

### Staging `ch36`
Status: materially source-truth-driven for the p50 retained-object / TT / KR role.
- It now clearly owns exact recursive bottleneck, coordinate systems, retained-object flow, TT toolkit, rank plausibility, conditional KR maps, and squared-density / retained-object recursion.
- This is the single largest fidelity recovery compared with the failed/non-canonical state.

### Staging `ch37`
Status: materially source-truth-driven for the shared p47+p50 fixed-branch same-scalar role.
- It now clearly owns branch identity, fixed structural vs recomputed numerical ledgers, branch-valid finite differences, and exact-target vs approximate-target HMC admissibility boundaries.

### Staging `ch38`
Status: materially source-truth-driven for the shared p47+p50 validation / promotion role.
- It now clearly owns validation ledgers, finite-difference parity as a first shared gate, and downstream promotion logic.

## Whole-block integration judgment

The restarted staging block now has the right chapter-role architecture **and** materially source-truth-driven content in all five destination chapters. It no longer reads merely as structural plausibility.

However, cutover is still **blocked** for two reasons:

1. The staging build still has inherited whole-book undefined-reference warnings outside the local block:
   - `ch:bf-prediction-error-decomposition`
   - `eq:bf-ped-loglik`
   - `ch:bf-kalman-hessian`
   - `ch:bf-structural-derivatives`
   - `ch:bf-factor-derivatives`
   - `ch:bf-custom-gradient-wrappers`
   - `ch:bf-derivative-validation`
   - `eq:bf-solve-hessian-w-dot`
   - `eq:bf-solve-hessian-quadratic`
   - `ch:bf-kalman-score`
   - `ch:bf-state-space-contracts`
   - `ch:bf-api-design`
   - `def:bf-filtering-target`

   These are broad-book consistency issues. Even though they do not invalidate the local restarted high-dimensional work, they prevent the staged surface from meeting the runbook’s clean pre-cutover standard.

2. The staged block still needs an explicit whole-book boundary review against:
   - `ch20_filter_choice.tex`
   - the later generic HMC part
   to confirm that the restarted block does not over-duplicate generic HMC or sigma-point burden after the source-truth rewrite.

## Gate status

- `G4` staging verification: **BLOCKED**
- Token: `BLOCK_R4_CUTOVER_PREFLIGHT_READY`

## What passed

- The staged high-dimensional block now materially carries p47 and p50 for its intended chapter roles.
- The chapter crosswalk and restart architecture are functioning.
- The source-truth migration in staging is no longer in an architecture-only state; it is a real candidate block.

## What remains before cutover

1. Resolve or explicitly gate the inherited whole-book undefined-reference warnings in the staging surface.
2. Perform the whole-book boundary audit against the surrounding monograph context.
3. Only then revisit R5 canonical cutover.

## Recommendation

Do **not** cut over yet.

The next step should be:
- a targeted staging verification / cleanup pass for the inherited whole-book reference warnings and whole-book boundary review,
- not further chapter-local source migration inside the restarted high-dimensional block.
