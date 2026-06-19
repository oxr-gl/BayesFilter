# P8i Phase 6 Subplan: Stochastic-Gradient And Likelihood Boundary

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Separate what P8i empirically validates about the relaxed-OT AD graph from
what remains a stochastic PF marginal-gradient or exact nonlinear-likelihood
claim.

## Entry Conditions

- Phases 1-4 results exist.
- Phase 5 blocks NUTS, pending read-only review.
- Phase 5 nonclaims carry forward: no NUTS readiness, no production HMC
  readiness, no posterior convergence, and no default sampler policy.

## Required Artifacts

- Boundary result documenting gradient and likelihood claim status:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase6-gradient-likelihood-boundary-result-2026-06-16.md`.
- Any derivation or reference tieout notes needed to justify a stronger claim,
  or an explicit blocker preserving the nonclaim.

## Required Checks, Tests, Reviews

- Document/code consistency checks:

```bash
rg -n "not the stochastic PF marginal likelihood gradient|AD gradient through declared relaxed Sinkhorn OT graph only|not exact nonlinear likelihood|not NUTS readiness|not posterior convergence" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

- Read-only review for scientific claim boundary.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What exactly has been shown about gradients and likelihood values, and what remains unproved or untested? |
| Baseline/comparator | P8h/P8i gradient artifacts, value ladders, and the design contract for relaxed Sinkhorn OT covariance carry. |
| Primary criterion | A reviewed boundary result classifies each gradient/likelihood claim as passed, blocked, diagnostic-only, or out of scope. |
| Veto diagnostics | Calling relaxed-OT AD the exact stochastic PF marginal score without derivation/evidence; calling scalar-SV surrogate likelihood exact nonlinear likelihood without tieout; hiding negative or blocked diagnostics. |
| Explanatory diagnostics | References to phase artifacts, finite-difference checks, value tieouts, derivation notes. |
| Not concluded | Any claim not explicitly classified as passed by this phase, including NUTS readiness, production HMC readiness, posterior convergence, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, filter ranking, or default sampler policy. |

## Forbidden Claims And Actions

- Do not promote a scientific claim without either a derivation in project
  notation or an artifact-backed empirical gate.
- Do not revise historical artifacts to make claims look stronger.
- Do not use Phase 4 fixed-kernel HMC execution or the Phase 5 NUTS blocker as
  evidence for posterior convergence, production HMC readiness, NUTS readiness,
  filter ranking, or default sampler policy.

## Exact Next-Phase Handoff Conditions

Phase 7 may launch after the claim boundary is reviewed. Phase 7 must preserve
any blocked or diagnostic-only classifications from Phase 6.

## Stop Conditions

- The claim boundary requires literature/source work outside the DPF lane.
- A stronger gradient or likelihood claim would require a derivation, exact
  nonlinear-likelihood tieout, stochastic PF marginal-score estimator contract,
  or new empirical artifact not already authorized by this subplan.
- The boundary result cannot preserve the Phase 5 nonclaims exactly.
