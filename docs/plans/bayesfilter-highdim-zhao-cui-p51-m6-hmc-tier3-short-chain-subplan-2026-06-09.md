# P51-M6 Subplan: HMC Tier 3 Short-Chain Diagnostics

metadata_date: 2026-06-09
phase: P51-M6
status: PLAN_REVIEW_CONVERGED

## Objective

Run or define short-chain HMC/NUTS diagnostics only after Tier 2 prerequisites
are satisfied or explicitly blocked.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do selected deterministic score targets pass short-chain sampler diagnostics against a declared reference for the same target that passed P51-M5 Tier 2? |
| Baseline/comparator | P50 HMC tier manifest, P51-M5 Tier 2 outcome, TensorFlow/TFP HMC/NUTS diagnostics, and a declared analytic/dense posterior reference for the same posterior target used in Tier 2. |
| Primary pass criterion | Short-chain diagnostics meet predeclared divergence, acceptance, posterior/reference, and reproducibility criteria against the declared posterior reference for the same target that passed Tier 2, or a blocker records the missing prerequisite.  If the posterior reference is unavailable, the phase must block rather than pass on internal diagnostics. |
| Veto diagnostics | Short-chain speed promoted despite divergences; no posterior/reference check; unavailable posterior reference hidden by internal diagnostics; single-seed result overinterpreted; Tier 2 failure ignored. |
| Not concluded | No production HMC readiness, GPU readiness, or broad sampler convergence. |

## Planned Work

1. Confirm P51-M5 Tier 2 status.
2. Select the exact same target that passed Tier 2; do not substitute an easier
   posterior target for Tier 3.
3. Record the posterior reference and criteria before execution.
4. Run CPU-only sampler diagnostics only if prerequisites exist.
5. Record pass/block and review with Claude.

## Repair Loop

Repair local sampler configuration, target wiring, or manifest gaps. Stop if
criteria need to change after seeing results.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-result-2026-06-09.md`

Required token:

`PASS_P51_M6_HMC_TIER3_SHORT_CHAIN` or `BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN`

Required manifest:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-manifest-2026-06-09.json`
