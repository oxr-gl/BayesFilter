# P50-M7 Subplan: HMC Readiness Tiers

metadata_date: 2026-06-09
phase: P50-M7
status: PLAN_REVIEW_CONVERGED

## Objective

Define and run tiered HMC readiness gates so finite gradients do not become an
unsupported HMC-readiness claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What additional evidence is needed before the deterministic filter can be called HMC-ready? |
| Baseline/comparator | M4 gradient calibration, model ladders from M5/M6, TensorFlow/TFP HMC/NUTS diagnostics where locally available. |
| Primary pass criterion | Tier definitions and focused diagnostics distinguish local value/gradient correctness, Hamiltonian/leapfrog behavior, and short-chain sampler health. |
| Veto diagnostics | Finite gradient existence promoted to HMC readiness; short-chain speed promoted despite divergences or invalid posterior/reference checks; GPU claims made from CPU-only runs. |
| Not concluded | No production HMC readiness unless declared tiers pass. |

## Planned Work

1. Define HMC readiness tiers and their promotion language.
2. Add local deterministic leapfrog or TFP HMC smoke checks where feasible.
3. Record diagnostics that veto readiness.

## Repair Loop

Repair local HMC smoke tests or contract wording.  Stop for package,
environment, GPU, or criterion changes.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p50-m7-hmc-readiness-tiers-result-2026-06-09.md`

Required token:

`PASS_P50_M7_HMC_READINESS_TIERS` or
`BLOCK_P50_M7_HMC_READINESS_TIERS`
