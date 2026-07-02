# Phase 3 Subplan: Tiny GPU/XLA Value And Score Gates

Date: 2026-07-03

Status: `DRAFT_PENDING_PHASE2`

## Phase Objective

Run the smallest trusted GPU/XLA/TF32 LEDH checks that can veto bad execution:
LGSSM value and score against Kalman, plus one feasible nonlinear value-only
smoke if admitted by Phase 1.

## Entry Conditions Inherited From Previous Phase

- Phase 2 runner exists and emits dry-run artifacts.
- Phase 1 admission ledger says which rows can be tested.
- GPU commands will be run with escalated trusted execution.

## Required Artifacts

- Tiny GPU/XLA JSON and MD artifacts under `docs/plans/`.
- Logs under `docs/plans/logs/`.
- Phase 3 result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-result-2026-07-03.md`.
- Updated Phase 4 subplan.

## Required Checks, Tests, Reviews

- Trusted `nvidia-smi`.
- Trusted TensorFlow GPU device probe if no fresh probe exists in this program.
- LGSSM LEDH value check against Kalman.
- LGSSM LEDH total derivative score check against Kalman or finite difference.
- One admitted nonlinear LEDH value smoke, if Phase 1 admits one.
- Claude read-only review of Phase 3 result before particle ladders.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the LEDH runner execute on real GPU/XLA/TF32 and pass tiny value/score gates before expensive ladders? |
| Baseline/comparator | Kalman for LGSSM; finite difference only where it differentiates the same deterministic objective and random numbers are fixed. |
| Primary pass criterion | LGSSM value and score pass their stated tolerances; device metadata confirms GPU; nonlinear smoke is finite or explicitly blocked. |
| Veto diagnostics | GPU device missing in trusted context; score is partial derivative; nonfinite value; XLA compile failure; random seed not fixed for finite difference score check. |
| Explanatory diagnostics | compile time, steady time, memory, ESS, warnings. |
| Not concluded | No all-model leaderboard, no HMC readiness, no nonlinear score correctness unless separately checked. |
| Artifact | Phase 3 JSON/MD, logs, and result. |

## Forbidden Claims And Actions

- Do not use CPU-only output as LEDH production evidence.
- Do not use a nonlinear smoke as all-model evidence.
- Do not hide score failure behind value success.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- GPU/XLA execution is trusted;
- LGSSM value and score gates pass or are blocked with a direct reason and user
  approval to continue value-only;
- nonlinear smoke is finite or its row is removed from the ladder scope.

## Stop Conditions

- Trusted GPU probe fails.
- LGSSM score gate fails and no reviewed repair plan exists.
- XLA compile is unbounded or hangs without producing a log artifact.
