# Phase R8 Handoff: Material Script Manual Route Integration

Date: 2026-06-29

Status: `DRAFT_HANDOFF_FROM_R7`

## Phase Objective

Move the verified fixed-ridge manual LGSSM route from the tiny R7 test into a
shared implementation used by the Phase 3 diagnostic, then decide whether the
material blocker can be replaced by a same-scalar FD and no-outer-tape gate.

## Entry Conditions Inherited From R7

- R5 one-step Contract E local VJP composition passed same-scalar FD.
- R6 two-step reverse scan passed same-scalar FD.
- R7 tiny LGSSM fixed-ridge manual route passed same-scalar FD for all three
  LGSSM parameters.
- The Phase 3 material blocker remains active:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- Executable R8 subplan reviewed with Claude before implementation.
- A shared fixed-ridge manual LGSSM route implementation or a carefully scoped
  material diagnostic helper.
- A route audit proving the material score path no longer calls outer
  `tf.GradientTape`.
- Same-scalar FD parity on the material helper before exact Kalman comparison.
- If blocker replacement is proposed, a new static audit that ties
  `--gate-mode material` to the verified manual route and fails if an outer tape
  remains.
- R8 result / close record.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the verified fixed-ridge manual route become the actual Phase 3 material score path? |
| Baseline/comparator | Same-scalar FD on the shared/material helper, followed by exact Kalman gradient only after route parity passes. |
| Primary pass criterion | No-outer-tape material score route plus same-scalar FD parity under a reviewed fixture and tolerances. |
| Veto diagnostics | Any hidden outer tape in material score, route label mismatch, branchy reset fallback, missing replay state, nonfinite values/cotangents, or failed blocker/audit reconciliation. |
| Not concluded | SIR/SV correctness, HMC readiness, production readiness, GPU/XLA/TF32 readiness, or broad scientific validity. |

## Stop Conditions

Stop if the material script cannot share the fixed-ridge route without changing
the scalar, if same-scalar FD parity fails after one focused repair attempt, or
if blocker replacement would require trusting an outer `tf.GradientTape` score.
