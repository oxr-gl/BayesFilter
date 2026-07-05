# Phase R6 Subplan: Tiny Time-Loop Manual Reverse-Scan Handoff

Date: 2026-06-29

Status: `DRAFT_HANDOFF_FROM_R5`

## Phase Objective

Extend the R5 one-step local composed VJP into a tiny fixed-branch time-loop
manual reverse-scan fixture, still without running material Phase 3 or claiming
full filter gradient correctness.

R6 should test whether cotangents from a later reset state can be accumulated
back through an earlier step in the same manual route used by R5.

## Entry Conditions Inherited From R5

- R5 local one-step composed VJP parity passed for `post_flow`,
  `corrected_log_weights`, and `residual_noise`.
- R5 replayed center, scale, stopped key, `epsilon0`, floor mask, and fixed
  ridge chart conditions.
- R5 static audit covered the named transitive manual dense finite transport
  helper family and preserved the Phase 3 material blocker.
- The material blocker remains:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- Executable R6 subplan reviewed with Claude before implementation.
- Tiny time-loop fixture, preferably `T=2` and very small `N,D`, with fixed
  deterministic tensors and replayed per-step charts.
- Manual reverse-scan implementation or test helper that accumulates
  next-particle cotangents through at least two local steps.
- Same-scalar finite-difference parity check for the tiny time-loop scalar.
- Static hidden-autodiff/full-transport/eigh audit for any new helpers.
- R6 result / close record.
- R7 handoff only if the tiny time-loop gate passes.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Bounded Claude read-only review before execution.
- Focused CPU-hidden pytest for R6 plus R5/R4 blocker-preserving tests.
- `py_compile` for touched Python modules.
- `git diff --check` on touched paths.
- Bounded Claude implementation/result review before advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the R5 one-step local manual composition be accumulated through a tiny fixed-branch time reverse scan? |
| Baseline/comparator | Central finite differences of the exact same tiny time-loop scalar. |
| Primary pass criterion | Manual reverse-scan cotangent dots match same-scalar central finite differences within frozen tolerances. |
| Veto diagnostics | Nonfinite values/cotangents, floor/ridge/chart branch changes, hidden autodiff, `tf.linalg.eigh` in the fixed-ridge route, `transport_ad_mode="full"`, missing material blocker, or missing replay artifacts. |
| Explanatory diagnostics | Per-step cotangent norms, per-step replayed chart values, transport residuals, ridge values, and branch masks. |
| Not concluded | Material LGSSM gradient correctness, Kalman agreement, SIR/SV correctness, HMC readiness, production readiness, or GPU/XLA readiness. |
| Artifact preserving result | R6 result note and focused tiny-loop test output. |

## Forbidden Claims And Actions

- Do not remove or weaken the material blocker during R6 unless the R6 subplan
  is explicitly rewritten and reviewed to authorize a narrower material gate.
- Do not run material Phase 3, full LGSSM finite differences, SIR, SV, GPU, or
  XLA jobs during default R6.
- Do not claim full filter gradient correctness from a tiny-loop fixture.
- Do not differentiate through floor, ridge, resampling, or chart branch
  selection.
- Do not use generic TensorFlow autodiff as the material implementation.

## Exact Next-Phase Handoff Conditions

Advance beyond R6 only if:

- tiny time-loop same-scalar parity passes;
- per-step floor/ridge/chart replay remains stable;
- static route audit passes;
- focused local checks pass;
- R6 result is written;
- bounded Claude implementation/result review converges; and
- the material blocker remains active unless a later reviewed phase explicitly
  replaces it.

## Stop Conditions

Stop and write an R6 blocker result if:

- the tiny reverse scan requires generic autodiff to pass;
- parity fails after one focused repair attempt;
- branch replay changes appear;
- required per-step auxiliary state cannot be replayed; or
- Claude review does not converge after five rounds for the same blocker.
