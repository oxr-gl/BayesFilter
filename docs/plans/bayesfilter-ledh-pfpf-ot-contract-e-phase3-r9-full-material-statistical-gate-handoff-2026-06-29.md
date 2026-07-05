# Phase R9 Handoff: Full Phase 3 Material Statistical Gate

Date: 2026-06-29

Status: `DRAFT_HANDOFF_FROM_R8`

## Phase Objective

Run the full Phase 3 LGSSM material statistical gate with the verified manual
score route, replacing the current full-scope blocker only if the reviewed
material run passes its value, same-scalar FD, route, and exact Kalman-gradient
criteria.

## Entry Conditions Inherited From R8

- The real Phase 3 material entrypoint can execute the tiny fixed-ridge manual
  route.
- Tiny material same-scalar FD passed for all three LGSSM parameters.
- Material route audits show no outer `tf.GradientTape` in the material score
  path.
- The full material gate remains blocked with:
  `PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION`.

## Required Artifacts

- Executable R9 subplan reviewed with Claude before implementation/run.
- A full-scope material route decision: whether to allow
  `state_dim in {1,2}`, `time_steps=10`, `seed_count=10`, and the reviewed
  particle count.
- A run manifest with command, environment, seeds, device, dtype, TF32/XLA
  policy, output paths, and git status.
- A same-scalar FD gate on the material helper or exact same emitted route.
- Exact Kalman value/gradient comparison only after same-scalar FD route parity
  passes.
- R9 result / close record.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Does the full Phase 3 LGSSM material gate pass with the no-autodiff manual Contract E route? |
| Baseline/comparator | Same-scalar FD on the material scalar; exact FP64 Kalman value/gradient for LGSSM. |
| Primary pass criterion | Reviewed Phase 3 material criteria pass for `D=1,2`, `T=10`, `seed_count=10`, and the selected particle count. |
| Veto diagnostics | Any outer-tape material route, failed same-scalar FD, nonfinite values/scores, reset covariance/conditioning failure, branch replay failure, wrong device/precision claim, or exact Kalman gate failure. |
| Not concluded | SIR/SV correctness, HMC readiness, production readiness, GPU/XLA/TF32 readiness unless separately run, or broad scientific validity. |

## Stop Conditions

Stop and write a blocker result if the full material route cannot share the
verified manual implementation, if same-scalar FD fails after one focused
repair attempt, if exact Kalman comparison fails after route parity passes, or
if the full run requires reverting to outer `tf.GradientTape`.
