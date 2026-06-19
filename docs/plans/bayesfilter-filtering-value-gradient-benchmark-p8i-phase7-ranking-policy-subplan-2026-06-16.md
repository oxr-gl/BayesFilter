# P8i Phase 7 Subplan: Scope, Ranking, And Default-Policy Decision

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Decide what, if anything, P8i supports about filter ranking, high-dimensional
scope, and default sampler policy.

## Entry Conditions

- Phase 6 claim-boundary result is reviewed.
- Phase 6 carries forward these nonclaims: no stochastic PF
  marginal-gradient correctness, no exact nonlinear likelihood correctness, no
  NUTS readiness, no production HMC readiness, no posterior convergence, no
  generic high-dimensional LEDH readiness, no filter ranking, and no default
  sampler policy.

## Required Artifacts

- Phase 7 ranking/default-policy result with an artifact coverage matrix.
- Updated blocked/nonclaim ledger if ranking or default policy remains
  unsupported.

## Required Checks, Tests, Reviews

- Read-only review required.
- No numerical run unless a reviewed subplan is added first.
- Boundary checks:

```bash
rg -n "no filter ranking|not a filter ranking|default sampler policy|generic high-dimensional LEDH readiness|production HMC readiness|posterior convergence|NUTS readiness|exact nonlinear likelihood correctness|stochastic PF marginal-gradient correctness" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Do the collected reviewed P8i artifacts justify any ranking, high-dimensional readiness, or default-policy change? |
| Baseline/comparator | Reviewed P8i results and blockers, including the Phase 6 claim-boundary classification; P8h is used only through artifacts explicitly inherited or re-tested by P8i. |
| Primary criterion | A conservative decision table that either justifies a narrow claim or preserves the nonclaim with explicit missing evidence. |
| Veto diagnostics | Ranking without comparable baselines; default-policy change from diagnostic-only evidence; generic high-dimensional readiness from scalar-SV evidence; production-HMC, posterior, NUTS, exact-likelihood, or stochastic-gradient claims revived after Phase 6 blocked them. |
| Explanatory diagnostics | Artifact coverage matrix, remaining blocker table. |
| Not concluded | Any ranking/default/high-dimensional claim not explicitly supported, plus all Phase 6 blocked or diagnostic-only claims. |

## Forbidden Claims And Actions

- Do not change default policy in code.
- Do not rank filters unless comparable value/gradient/runtime/evidence gates
  exist.
- Do not claim generic high-dimensional LEDH readiness from scalar-SV
  diagnostics.
- Do not revive NUTS, production-HMC, posterior-convergence,
  exact-likelihood, or stochastic-marginal-gradient claims blocked in Phase 6.

## Exact Next-Phase Handoff Conditions

Phase 8 closeout may launch after the decision table is reviewed.

## Stop Conditions

- The decision would require new comparative experiments.
- A narrow ranking or policy claim would require changing code defaults.
- The result cannot preserve the Phase 6 boundary classifications.
