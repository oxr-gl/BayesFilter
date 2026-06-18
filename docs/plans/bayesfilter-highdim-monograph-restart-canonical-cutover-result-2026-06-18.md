# Cutover result: staged high-dimensional part promoted to canonical monograph surface

**Date:** 2026-06-18  
**Artifact ID:** `bayesfilter-highdim-monograph-restart-canonical-cutover-result-2026-06-18.md`

## Context

The restart-governed execution phase rebuilt the high-dimensional nonlinear
filtering block on the staging surface:
- `docs/main_highdim_restart_staging.tex`
- `docs/chapters_restart_staging/`

The work was governed by:
- `docs/plans/bayesfilter-highdim-monograph-restart-source-restoration-reset-memo-2026-06-15.md`
- `docs/plans/bayesfilter-highdim-monograph-restart-execution-master-program-2026-06-18.md`

That governance required a staging-first source-restoration process because the
previous canonical cutover had been judged premature: architectural plausibility
and clean builds had been allowed to stand in for full source-fidelity
sufficiency.

## What changed before cutover

The staged high-dimensional block was promoted into its own separate part and
expanded into the following 8-chapter sequence:
1. `ch33_highdim_nonlinear_filtering_foundations.tex`
2. `ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
3. `ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
4. `ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
5. `ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
6. `ch36b_highdim_squared_tt_recursion_and_fixed_branch_likelihoods.tex`
7. `ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
8. `ch38_highdim_validation_defect_calculus_and_promotion.tex`

The restoration passes added, among other things:
- raw-to-merged 2D/3D SGQF cloud walkthroughs,
- explicit merge / prune / order policy,
- SGQF value-path and derivative framework,
- SGQF implementation contract and end-to-end algorithm,
- TT/KR coordinate walkthrough and retained-object chain,
- fixed-branch stored-field and next-step closure contract,
- explicit forward/derivative core-update and sweep-recomputation semantics,
- fixed-branch failure / stopping / branch-mismatch vocabulary,
- derivative block checklists,
- explicit validation veto ledger,
- benchmark backbone and benchmark-specific claim boundaries,
- derivative reporting object and branch-status reporting.

## Why the staged part is now trusted canonically

A fresh whole-part skeptical audit judged:
- the p47 SGQF source burden to be non-blocking,
- the remaining p50 differences to be narrow enough that they no longer
  constitute structurally explanatory blockers,
- the staged part to carry the useful operational middle well enough that a
  careful implementation reader no longer needs to reopen the source notes for
  the core monograph argument.

The cutover judgment is therefore:

> The staged high-dimensional part is now source-sufficient enough to become the
> canonical monograph surface.

This does **not** mean the canonical chapters are a word-for-word substitute for
p47 or p50.  It means the remaining differences are now better classified as
compression, polish, provenance convenience, or optional pedagogical detail,
rather than as missing structural explanation.

## Canonical cutover action

The canonical driver `docs/main.tex` should now mirror the staged high-dimensional
part as its authoritative high-dimensional nonlinear filtering block, including
its separate part boundary and expanded chapter sequence.

## Post-cutover expectation

Future work may still refine the canonical chapters, but it should now be treated
as canonical editorial / maintenance work unless a new skeptical audit finds a
fresh structural gap.  Any future topology change should be recorded in the
restart execution master program before it becomes the new baseline.
