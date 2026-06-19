# P8i Phase 5 Subplan: NUTS Readiness Decision

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Decide whether a bounded NUTS diagnostic is justified after Phase 4 Tier-1, or
write a blocker that preserves why NUTS is not yet warranted.

## Entry Conditions

- Phase 4 HMC Tier-1 result exists and passed a tiny fixed-kernel execution
  diagnostic, pending read-only review.
- The runner currently has no NUTS command path.

## Required Artifacts

- NUTS readiness decision result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase5-nuts-readiness-result-2026-06-16.md`.
- Refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase6-gradient-likelihood-boundary-subplan-2026-06-16.md`.
- No NUTS diagnostic artifact is authorized in this subplan.

## Required Checks, Tests, Reviews

- Local checks:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.json
rg -n "NoUTurn|NUTS|nuts|tfp.mcmc" scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

- Read-only review of Phase 5 decision result and refreshed Phase 6 subplan.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is a NUTS diagnostic scientifically and computationally justified for the selected P8i route now? |
| Baseline/comparator | Phase 4 HMC diagnostics and Phase 1-3 value/gradient/GPU gates. |
| Primary criterion | Write a blocker decision if NUTS lacks implementation path, adaptation budget, or diagnostics; otherwise require a separate reviewed NUTS subplan before any run. |
| Veto diagnostics | NUTS readiness claimed from two-sample fixed-kernel HMC; no NUTS command path; no adaptation/tuning diagnostics; no posterior convergence evidence; runtime budget not reviewed for NUTS. |
| Explanatory diagnostics | HMC acceptance, runtime, gradient cost, chain stability, projected NUTS cost. |
| Not concluded | NUTS readiness unless a NUTS diagnostic is actually run and passes; production HMC readiness; posterior convergence; default sampler policy. |

## Forbidden Claims And Actions

- Do not run adaptive NUTS in Phase 5.
- Do not claim NUTS readiness from HMC alone.

## Exact Next-Phase Handoff Conditions

Phase 6 may launch after the NUTS readiness decision is reviewed. If NUTS is
blocked, Phase 6 must preserve that boundary.

## Stop Conditions

- Any attempt to run NUTS under this subplan.
- Any attempt to claim NUTS readiness from Phase 4 alone.
