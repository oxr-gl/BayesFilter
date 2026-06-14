# P52-M0 Subplan: Governance, Target Lock, And Claim Boundaries

metadata_date: 2026-06-10
phase: P52-M0
status: PLAN_REVIEW_CONVERGED

## Objective

Lock P52 to the real P51 blocker: replacing the dense all-pairs multistate
spatial SIR route with a memory-bounded fixed-rank factorized route.  Prevent
UKF, lower-rung tests, or d=100 smoke rows from being promoted beyond their
evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the P52 targets, baselines, nonclaims, and dimension roles explicit enough to prevent another false production-route pass? |
| Baseline/comparator | P51-M3 route blocker, P50/P51 closeouts, existing spatial SIR lower-rung fixtures, and P52 master plan. |
| Primary pass criterion | A target-lock manifest records the dense-route blocker, the fixed-rank replacement target, the role of UKF, and the allowed claims for d=18/d=50/d=100. |
| Veto diagnostics | Dense all-pairs route retained; UKF declared correctness reference; d=100 declared production filtering before d=18/d=50 pass; adaptive ranks allowed inside HMC. |
| Not concluded | No implementation, filtering correctness, HMC readiness, or production spatial SIR readiness. |

## Planned Work

1. Build a P52 target-lock manifest listing source artifacts and forbidden
   claims.
2. Define allowed evidence classes: correctness reference,
   rank self-convergence, scout baseline, memory preflight, and scaling stress.
   HMC readiness remains a forbidden overclaim for M0, not an allowed evidence
   class.
3. Add static tests that reject unsupported claims in P52 artifacts, including
   the M0 manifest, M0 result, visible runbook, visible execution ledger, and
   source blocker manifest.
4. Review the governance artifact with Claude.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-result-2026-06-10.md`

Required token:

`PASS_P52_M0_GOVERNANCE_TARGET_LOCK` or
`BLOCK_P52_M0_GOVERNANCE_TARGET_LOCK`
