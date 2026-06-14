# P51-M5 Subplan: HMC Tier 2 Leapfrog Diagnostics

metadata_date: 2026-06-09
phase: P51-M5
status: PLAN_REVIEW_CONVERGED

## Objective

Run or define HMC Tier 2 Hamiltonian/leapfrog diagnostics for the most mature
P51-supported deterministic targets.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do selected deterministic score targets pass energy and reversibility checks under a fixed Hamiltonian integrator? |
| Baseline/comparator | P50 HMC tier manifest, stable score API from P51-M1 if passed, strict M5 SV rows from P50, and TensorFlow/TFP CPU-only deterministic score paths. |
| Primary pass criterion | Predeclared energy-error and reversibility diagnostics pass for the declared target(s), or a blocker records why Tier 2 cannot run. |
| Veto diagnostics | Finite gradient treated as leapfrog stability; CPU-only smoke treated as GPU readiness; target identity changes between value and gradient. |
| Not concluded | No short-chain sampler health, production HMC readiness, GPU readiness, or model production readiness. |

## Planned Work

1. Select the smallest mature target from P51-M1/M2 outcomes.
2. Implement or reuse fixed-mass leapfrog diagnostics.
3. Run CPU-only deterministic checks.
4. Record pass/block and review with Claude.

## Repair Loop

Repair local integrator, mass-matrix, dtype, or target-wiring bugs. Stop for
new sampler-policy decisions or GPU claims.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-result-2026-06-09.md`

Required token:

`PASS_P51_M5_HMC_TIER2_LEAPFROG` or `BLOCK_P51_M5_HMC_TIER2_LEAPFROG`

Required manifest:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-manifest-2026-06-09.json`
