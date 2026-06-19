# P8i Phase 6 Result: Gradient And Likelihood Boundary

Date: 2026-06-16

Status: `PASS_BOUNDARY_CLASSIFICATION_REVIEWED`

## Phase Objective

Separate what P8i empirically validates about the relaxed-OT AD graph from
what remains a stochastic particle-filter marginal-gradient or exact
nonlinear-likelihood claim.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What exactly has been shown about gradients and likelihood values, and what remains unproved or untested? |
| Baseline/comparator | P8h/P8i gradient artifacts, value ladders, HMC/NUTS boundary results, and the declared relaxed Sinkhorn OT covariance-carry route. |
| Primary criterion | A reviewed boundary result classifies each gradient/likelihood claim as passed, blocked, diagnostic-only, or out of scope. |
| Veto diagnostics | Calling relaxed-OT AD the exact stochastic PF marginal score without derivation/evidence; calling scalar-SV surrogate likelihood exact nonlinear likelihood without tieout; using Phase 4/5 as posterior, production-HMC, NUTS, ranking, or default-policy evidence. |
| Explanatory diagnostics | Phase 1 value ladder, Phase 2 finite-difference gradient checks, Phase 4 fixed-kernel HMC execution diagnostics, Phase 5 NUTS blocker, runner/test nonclaim strings. |
| Not concluded | NUTS readiness, production HMC readiness, posterior convergence, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, generic high-dimensional LEDH readiness, filter ranking, or default sampler policy. |

## Skeptical Audit

- Wrong-baseline check: Phase 6 treats P8i Phase 2 as an AD graph diagnostic,
  not as proof of the stochastic PF marginal score.
- Proxy-metric check: finite-difference residuals and HMC execution are
  consistency/execution diagnostics only.
- Stop-condition check: stronger gradient or likelihood claims would require a
  derivation, exact-likelihood tieout, stochastic PF marginal-score estimator
  contract, or new empirical artifact outside this phase.
- Artifact-fit check: the boundary can be decided from existing artifacts and
  code/document nonclaim checks; no new numerical run is needed.

## Checks

```bash
rg -n "not the stochastic PF marginal likelihood gradient|AD gradient through declared relaxed Sinkhorn OT graph only|not exact nonlinear likelihood|not NUTS readiness|not posterior convergence|not production HMC readiness|not a default sampler policy" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Results:

- Boundary/nonclaim search: passed; the runner/tests and P8i artifacts preserve
  the relaxed-OT AD graph, not-exact-likelihood, not-stochastic-marginal-score,
  NUTS, posterior, HMC-readiness, ranking, and default-policy boundaries.
- `git diff --check`: passed.

## Classification

| Claim | Classification | Evidence | Boundary |
|---|---|---|---|
| The implemented fixed-seed relaxed Sinkhorn OT graph has finite connected AD gradients at the selected P8i route/count/horizons. | Passed diagnostic. | Phase 2 H16/H32 artifacts passed finite, connected, repeatable, trusted-GPU, FD residual, route/count, and runtime gates. | Applies to the implemented deterministic relaxed-OT graph only. |
| The Phase 2 finite-difference residuals support local consistency of the implemented AD graph. | Passed diagnostic. | Max residuals were about `7.56e-09` at H16 and `1.13e-08` at H32, below the declared `1e-5` threshold. | This is not a proof of stochastic PF marginal-gradient correctness. |
| The relaxed-OT AD gradient is the exact stochastic PF marginal likelihood gradient. | Blocked / not concluded. | No derivation or stochastic PF marginal-score estimator contract exists in P8i. | Requires separate derivation/evidence before any such claim. |
| The scalar-SV value used here is the exact nonlinear likelihood. | Blocked / not concluded. | P8i has no exact nonlinear-likelihood tieout artifact. | Current artifacts are route diagnostics, not exact-likelihood validation. |
| Phase 4 establishes posterior convergence, production HMC readiness, or valid tuning. | Blocked / not concluded. | Phase 4 used a tiny fixed-kernel diagnostic: two retained samples, one burn-in step, one leapfrog step, fixed step size. | Phase 4 is execution evidence only. |
| Phase 5 establishes NUTS readiness. | Blocked / not concluded. | Phase 5 explicitly blocked NUTS because no NUTS command path, adaptation budget, or diagnostics are present. | NUTS requires a separate reviewed implementation and diagnostics plan. |
| P8i supports filter ranking, generic high-dimensional LEDH readiness, or default sampler policy. | Deferred to Phase 7 / currently not concluded. | P8i has no comparable filter baseline ladder or policy-change gate. | Phase 7 must preserve this unless it can justify a narrow non-policy claim. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 6 as a claim-boundary classification, pending review. | Each gradient/likelihood/sampler-policy claim is classified as passed diagnostic, blocked/not concluded, or deferred. | No boundary veto fired; stronger stochastic-gradient and exact-likelihood claims are blocked. | A future derivation or exact-likelihood tieout may support stronger claims, but that evidence is not present in P8i. | Refresh Phase 7 as a conservative ranking/scope/default-policy decision. | No stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, NUTS readiness, production HMC readiness, posterior convergence, generic high-dimensional LEDH readiness, filter ranking, or default sampler policy. |

## Post-Run Red-Team Note

Strongest alternative explanation: the implemented relaxed-OT graph may be a
useful differentiable surrogate even though P8i does not prove it is the exact
stochastic PF marginal score.

What would overturn this result: a reviewed derivation in project notation,
an exact-likelihood tieout for the nonlinear model, or a stochastic
marginal-score estimator contract with matching empirical evidence.

Weakest part of the evidence: the current gradient evidence is computational
and fixed-seed; it is not a mathematical identification result.

## Handoff

Read-only review accepted this boundary after a focused Phase 7 handoff repair.
Phase 7 must preserve all blocked and diagnostic-only classifications unless
it writes a separate blocker or a narrow decision table with explicit missing
evidence.
