# P47 M4b/M5b Production Repair Master Program

metadata_date: 2026-06-09
program: P47-production-repair
status: `REVIEWED_BLOCKER_CLOSEOUT`

## Purpose

Repair the two reviewed P47 blocker rows without weakening the P47 closeout:

- M4b spatial SIR production or near-paper-scale filtering.
- M5b predator-prey production or near-paper-scale filtering.

Codex remains supervisor and execution agent.  Claude is read-only reviewer.
S&P 500 reproduction remains out of scope.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_WITH_ROUTE_RISK`.

- Wrong-baseline risk: M4a/M5a lower-rung evidence is not reused as production
  evidence.  M4b and M5b must have separate production-row artifacts.
- Proxy-metric risk: finite values, fit residuals, CUT4 diagnostics, wall time,
  and preconditioning metrics are explanatory unless downstream
  value/state-quality metrics pass.
- Hidden-assumption risk: the current P46/P47 multistate route retains all state
  axes on tensor-product grids.  This is likely a route-architecture blocker
  for spatial SIR J=9, so M4b begins with a complexity preflight instead of a
  blind long run.
- Unfair-comparison risk: M5b must compare Zhao--Cui against a dense/refined
  same-target reference on the same synthetic observation path and parameter
  vector before emitting the production token.
- Stale-context risk: P47-M7 remains a truthful blocker closeout until these
  continuation rows pass Claude review.  This program does not retroactively
  rewrite P47 closeout.

## Evidence Contract

Question: can the two blocked P47 production rows be repaired under reviewed
model-specific production gates?

Primary pass criteria:

- M4b: `PASS_P47_M2_PAPER_SCALE_READINESS` and
  `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY` are prerequisites; a
  production or near-paper-scale spatial SIR row must preserve the M4a target
  family and M1 route label, report observed/unobserved metrics, pass the
  reviewed production tolerance, and avoid finite-output-as-correctness
  promotion.
- M5b: `PASS_P47_M2_PAPER_SCALE_READINESS` and
  `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING` are prerequisites; a
  production or near-paper-scale predator-prey row must preserve the M5a target
  family and M1 route label, compare against a dense/refined same-target
  reference, report value/state/covariance metrics, and pass the reviewed
  production tolerance.

Veto diagnostics:

- target family or parameterization changes without reviewed amendment;
- M1 route label is absent;
- lower-rung evidence is promoted as production evidence;
- finite output, fit residual, wall time, or CUT4 diagnostics are treated as
  correctness by themselves;
- S&P 500 real-data reproduction is introduced;
- GPU/CUDA commands run outside trusted/escalated policy;
- M4b near-paper row is attempted after a preflight route-complexity veto.

Explanatory-only diagnostics:

- wall time, memory, point counts, TT ranks, basis size, condition number,
  fit residual, holdout residual, branch hashes, replay hashes, CUT4 value
  metadata, and preconditioning metrics.

Not concluded even if a row passes:

- no adaptive MATLAB TT-cross/SIRT reproduction;
- no native non-Gaussian SIR correctness unless separately reviewed;
- no nonlinear preconditioning usefulness unless a matched-budget downstream
  row separately passes;
- no production HMC readiness or production score API.

## Phases

| Phase | Artifact | Goal | Terminal Token |
| --- | --- | --- | --- |
| R0 | this master program | Freeze repair governance and Claude read-only protocol. | `PASS_P47_PRODUCTION_REPAIR_PLAN` |
| R1 | `bayesfilter-highdim-zhao-cui-p47-m4b-spatial-sir-production-row-subplan-2026-06-09.md` | Run spatial SIR production-row preflight, then ladder only if route-complexity permits. | `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` or reviewed blocker |
| R2 | `bayesfilter-highdim-zhao-cui-p47-m5b-predator-prey-production-row-subplan-2026-06-09.md` | Run predator-prey near-paper horizon ladder with dense/refined same-target reference. | `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` or reviewed blocker |
| R3 | execution result | Preserve pass/blocker tokens and decide whether P47-M7 can be revisited. | closeout update token or reviewed blocker |

## Execution Order

1. Run local plan/manifest guards.
2. Ask Claude for read-only review of R0/R1/R2.
3. If Claude passes, run R1 M4b preflight.  If the current all-axes retained-grid
   route is preflight-blocked, record `BLOCKED_M4B_ROUTE_ARCHITECTURE` and do
   not attempt J=9 with that route.
4. Run R2 M5b horizon ladder one axis at a time: horizon 4, 8, 16, then 25.
5. After each repair, ask Claude for read-only review before emitting any
   production token.

## Initial Execution Outcome

Codex executed the first local repair gates before any production token was
emitted:

- M4b: the current P46/P47 all-axes retained-grid route is preflight-blocked
  for the near-paper spatial SIR row.  J=5 and J=9 exceed the CPU
  pairwise-transition cap before execution, so the reviewed outcome should be
  `BLOCKED_M4B_ROUTE_ARCHITECTURE` unless a route amendment is created.
- M5b: the horizon-25 predator-prey same-target production candidate is
  deterministic and finite, but it fails the reviewed value/state/covariance
  tolerances.  Higher-order/high-rank tuning probes hit condition-number
  vetoes.  The reviewed outcome should be
  `BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING` unless a coordinate-map or
  propagation-route amendment is created.

No production token is emitted by this initial execution.

Claude read-only review returned:

```text
PASS_P47_PRODUCTION_REPAIR_BLOCKER_REVIEW
```

The blocker closeout is reviewed.  Follow-on execution requires separate
route-amendment plans for M4b and/or M5b.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_m4b_m5b_production_repair.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_m4b_m5b_production_repair.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-m5b-production-repair-master-program-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-spatial-sir-production-row-subplan-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-predator-prey-production-row-subplan-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-production-row-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-production-row-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-m5b-production-repair-claude-review-ledger-2026-06-09.md tests/highdim/test_p47_m4b_m5b_production_repair.py
```

## Claude Review Token

```text
PASS_P47_PRODUCTION_REPAIR_PLAN
```

or

```text
BLOCK_P47_PRODUCTION_REPAIR_PLAN
```
