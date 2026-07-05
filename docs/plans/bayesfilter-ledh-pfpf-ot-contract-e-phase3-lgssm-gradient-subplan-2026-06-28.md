# Phase 3 Subplan: Contract E LGSSM gradient gate

Date: 2026-06-28

Status: `BLOCKED_IN_PRECHECK_PENDING_REPAIR_SUBPLAN`

## Phase Objective

Test the Contract E LGSSM gradient against the exact Kalman gradient and an
independent same-scalar 13-point finite-difference regression diagnostic.

## Entry Conditions Inherited From Previous Phase

- Phase 2 has a Contract E LGSSM value scalar with recorded seeds and reset
  diagnostics, and Phase 2 result review has returned `VERDICT: AGREE`.
- The Phase 3 scalar is frozen to the Phase 2 transition-first LGSSM log
  marginal likelihood accumulator `sum_t incremental_t`, with the same
  observations, \(T=10\), \(\theta_0=(0.72,\log 0.22,\log 0.30)\), initial
  covariance \(0.7I\), reset arms, and Contract E residual construction.
- Frozen seed schedule: `SEED_COUNT=10`, seed indices `9100..9109`, initial
  seeds `[seed,17]`, transition seeds `[seed,29]`, and Contract E residual
  seeds `[seed,43+t]`, exactly as used in Phase 2.
- Frozen material particle count for the promoted LGSSM gradient gate:
  `N=1000`.  Smaller CPU-hidden or tiny GPU smokes are wiring-only and cannot
  satisfy the primary criterion.

## Required Artifacts

- Gradient diagnostic script:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`
- JSON gradient diagnostic:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-2026-06-28.json`
- Markdown gradient diagnostic:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-2026-06-28.md`
- Phase 3 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-result-2026-06-28.md`
- Refreshed Phase 4 SIR FD subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase4-sir-fd-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Compile/check changed files.
- Tiny CPU-hidden gradient smoke.
- Trusted GPU/XLA gradient run if GPU evidence is claimed.
- Bounded Claude review of gradient result and Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Contract E LGSSM gradient match exact Kalman and same-scalar FD within stated uncertainty? |
| Baseline/comparator | Exact Kalman gradient for LGSSM; 13-point FD regression on the same Contract E scalar. |
| Primary pass criterion | Value and gradient means across seeds are within two combined standard errors of exact Kalman; manual/reverse gradient and 13-point FD regression agree within two combined SE for `theta[0]`, `log_transition_variance`, and `log_observation_variance` on both 1d and 2d fixtures. |
| Veto diagnostics | Central FD used as primary evidence, missing FD SE, fewer than 13 FD points, failure to drop the highest and lowest objective values before regression, fewer than 10 fixed seeds without reviewed repair, nonfinite gradients, wrong scalar, hidden autodiff-full transport, or missing covariance/conditioning diagnostics. |
| Explanatory diagnostics | Central FD sanity, per-parameter z-scores, FD R2, per-seed gradient scatter, runtime and memory. |
| Not concluded | No SIR/SV exact gradient correctness, no HMC readiness, no production readiness. |
| Artifact | Gradient JSON/Markdown plus Phase 3 result. |

## Forbidden Claims And Actions

- Do not use central difference as the promoted gradient evidence.
- Do not use Zhao-Cui as comparator.
- Do not claim AD is the oracle; autodiff may be diagnostic only if explicitly
  labeled.
- Do not use full transport autodiff.
- Do not change \(N=1000\), seed schedule, FD abscissae, targeted parameters,
  scalar, exact Kalman comparator, or Contract E reset policy after seeing
  Phase 3 values.
- Do not execute the material Phase 3 gradient gate until this subplan has
  received bounded review `VERDICT: AGREE`.

## Frozen FD Protocol

- Targeted parameters: all three LGSSM parameters,
  `theta[0]`, `theta[1]=log_transition_variance`, and
  `theta[2]=log_observation_variance`.
- Abscissae: 13 symmetric points
  `[-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6] * h_j` for each coordinate direction
  \(e_j\).
- Step-size rule, frozen before execution:
  \(h_0=5\times 10^{-4}\) for the AR coefficient parameter
  `theta[0]`, and \(h_1=h_2=1\times 10^{-3}\) for
  `log_transition_variance` and `log_observation_variance`.
  These values may not be changed after seeing Phase 3 values, FD regression
  slopes, or gradient errors; any change requires a blocker/replan artifact and
  a fresh bounded review before execution.
- Estimator: evaluate the same Contract E scalar at all 13 points under the
  frozen seed schedule, drop the highest and lowest objective values, and run a
  least-squares regression of the remaining 11 objective values on the signed
  perturbation to estimate the directional derivative and its standard error.
- Replication: use the same 10 fixed seeds as Phase 2 for the promoted
  material gate.  Additional seeds may be explanatory only unless a reviewed
  same-phase repair freezes them before results are inspected.
- Central differences may be reported only as a sanity diagnostic.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- LGSSM gradient result has exact comparator, FD regression, SE, and z-scores;
- Contract E passes the Phase 3 primary gradient gate, or a reviewed repair
  closes Phase 3 as passed after focused reruns;
- Phase 4 preserves FD-only comparator discipline for SIR.

If the gradient gate fails and is not repaired inside Phase 3, classify the
failure in the Phase 3 result and stop rather than advancing to Phase 4.

## Stop Conditions

Stop on wrong scalar, failed covariance/conditioning veto, FD protocol mismatch,
or inability to produce uncertainty estimates.

## End-Of-Phase Protocol

Run checks, write result, refresh Phase 4, review Phase 4, repair review
findings, then advance or stop.
