# Phase 5 Result: Synthesis And Handoff

Date: 2026-07-01

Status: `COMPLETED_WITH_UNRESOLVED_FULL_ROUTE_SCORE_MISMATCH`

## Decision

The root-cause program narrowed the SIR gradient problem but did not prove full
score correctness or identify a single repaired bug.

The best-supported current classification is:

- scalar kappa aggregation failure: weakened / ruled out by Phase 1;
- regional infection-vs-recovery geometry: supported as the dominant mismatch
  direction by Phase 2;
- local RHS/RK4 transition VJP bug: weakened / ruled out by Phase 3 local
  algebra;
- local stopped-scale-key transport VJP wrapper bug: weakened / ruled out by
  Phase 4 local algebra;
- remaining live target: full-route score assembly or material-route behavior,
  including interaction among transition-density, LEDH-flow-prior,
  pre-flow-clamp, log-weight normalization, observation-density terms, and
  finite-N / finite-difference noise.

The next smallest justified diagnostic is a tiny full-route score-assembly
parity audit: compare manual per-component score contributions with
TensorFlow autodiff for the same tiny fixed route, one component boundary at a
time, before running another material GPU/TF32 SIR budget ladder.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the best-supported current root-cause classification and next action? |
| Baseline/comparator | Phase 0-4 artifacts plus raw/physics/whitened entry evidence. |
| Primary criterion | Separate implementation bug, numerical/tuning failure, parametrization issue, and unresolved uncertainty with exact evidence. |
| Veto diagnostics | Overclaiming HMC readiness, unsupported root-cause certainty, treating local VJP passes as full-filter correctness, missing phase artifact, or changing thresholds after seeing results. |
| Not concluded | Posterior correctness, production readiness, general nonlinear-model result, or full SIR score correctness. |

## Phase Evidence Map

| Phase | Main result | Artifact |
| --- | --- | --- |
| 0 | Scope, route, baseline, and code anchors frozen. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-result-2026-07-01.md` |
| 1 | Regional kappa scores reconstruct scalar manual kappa exactly; scalar aggregation failure ruled out. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-result-2026-07-01.md` |
| 2 | Mismatch is dominated by regional infection-vs-recovery contrast rho; tau is secondary. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-result-2026-07-01.md` |
| 3 | RHS/RK4 transition VJP matches autodiff at machine precision in local float64 CPU algebra. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-result-2026-07-01.md` |
| 4 | Manual stopped-scale-key transport VJP wrapper matches independent autodiff at machine precision in local float64 CPU algebra. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-result-2026-07-01.md` |

## Key Numbers

| Quantity | Value |
| --- | ---: |
| Phase 1 scalar manual `log_kappa_scale` | `-205.1933135986328` |
| Phase 1 regional manual kappa sum | `-205.1933135986328` |
| Phase 1 regional FD kappa sum | `-263.2179145812988` |
| Phase 1 FD-minus-manual kappa gap | `-58.024600982666016` |
| Phase 2 rho aggregate gap | `-55.164066314697266` |
| Phase 2 tau aggregate gap | `-26.30706238746643` |
| Phase 3 largest local residual | `3.410605131648481e-13` |
| Phase 4 largest local residual | `2.3314683517128287e-15` |

## Interpretation

The mismatch is real in the current material budget-10 diagnostic, but it is
not explained by the two local adjoint primitives audited here.

The direction of the discrepancy is epidemiologically structured rather than
randomly distributed across parameters: kappa/rho carries the largest gap,
nu is smaller, and tau is secondary.  That pattern is consistent with a
full-route score-assembly or representation issue that becomes visible when
the transition, LEDH flow, likelihood correction, and transport recursion are
composed.

The Phase 3 and Phase 4 passes are strong local evidence, but they are not full
filter evidence.  They only say that isolated transition VJP and isolated
transport VJP wrappers match independent autodiff comparators.

## Strongest Alternative Explanations

1. Full-route score assembly bug:
   A cotangent may be wired incorrectly when transition-density,
   LEDH-flow-prior, pre-flow-clamp, observation-density, log-normalization, and
   transport terms are added together across time.

2. Material-route numerical or finite-N issue:
   The budget-10 FD/manual comparison may still be sensitive to finite particle
   count, finite-difference step, TF32, or high Monte Carlo noise in the SIR
   nonlinear route.

3. Representation / parametrization issue:
   The kappa/nu scalar parametrization may produce a poorly conditioned score
   direction even when local derivatives are correct.  Phase 2 supports this
   as a geometry issue, but does not by itself prove that reparameterization
   fixes the full score.

4. Non-centered/process-noise route:
   Phase 3/4 did not test this.  It remains possible later work, but it is no
   longer the smallest justified next diagnostic because the local transition
   and transport adjoints both passed.

## Recommended Next Diagnostic

Create a new focused plan for a tiny full-route score-assembly parity audit.

Minimum proposed scope:

- Use CPU float64 tiny fixed tensors first, not material GPU/TF32 evidence.
- Use `T=1`, `N=2` or `N=3`, one or two seeds, and the same fixed branch.
- Compare manual score contributions from
  `return_score_decomposition=True` against TensorFlow autodiff for matching
  isolated scalar objectives:
  - observation-density covariance;
  - transition-density through `prior_means`;
  - LEDH-flow-prior through `prior_means`;
  - pre-flow-clamp path;
  - log-weight normalization/correction boundary.
- Only after local full-route parity passes, rerun material GPU/TF32 budget
  SIR diagnostics with a particle-count and FD-step ladder.

This should be a new governed plan, not a silent continuation of this root-cause
program, because it changes the diagnostic boundary from local primitive VJPs
to full-route score assembly.

## Decision Table

| Decision item | Status |
| --- | --- |
| Primary criterion | Passed for synthesis: the program separates ruled-out local bugs from unresolved full-route uncertainty. |
| Veto diagnostics | No HMC/posterior/production claim made. |
| Main uncertainty | Full SIR score mismatch remains unresolved. |
| Next justified action | Tiny full-route score-assembly parity plan, then material GPU/TF32 ladder only if local assembly passes. |
| What is not concluded | No SIR gradient correctness, no HMC readiness, no production reparameterization, no posterior correctness. |

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No production/default-policy change.
- No general nonlinear-model conclusion.
