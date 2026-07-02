# Phase R6 Execution Subplan: Tiny Time-Loop Manual Reverse Scan

Date: 2026-06-29

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Test whether the R5 one-step Contract E manual VJP composition can be
accumulated through a tiny fixed-branch time reverse scan.  R6 is a local
engineering gate only: it checks cotangent plumbing through time before any
material LGSSM Phase 3 gradient evidence can be reopened.

## Entry Conditions Inherited From R5

- R5 local one-step same-scalar central finite-difference parity passed for
  `post_flow`, `corrected_log_weights`, and `residual_noise`.
- R5 uses a replayed smooth chart: center, scale, stopped key, and `epsilon0`.
- R5 uses fixed-ridge Cholesky Contract E reset VJP and explicitly audits that
  `tf.linalg.eigh`, generic autodiff, and `transport_ad_mode="full"` are absent
  from the local route.
- The material Phase 3 blocker remains active:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- This executable R6 subplan, reviewed with Claude before implementation.
- A focused tiny-loop test artifact, expected path:
  `tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py`.
- A two-step fixed-branch scalar with:
  - step-0 initial `post_flow`;
  - step-0 and step-1 `corrected_log_weights`;
  - step-0 and step-1 residual noises;
  - deterministic differentiable transition from step-0 reset particles into
    step-1 `post_flow`;
  - frozen per-step chart replays from the base forward pass; and
  - scalar contributions from both log-normalization increments and downstream
    particle contractions.
- A manual reverse-scan helper that pushes the step-1 `post_flow` cotangent
  through the deterministic transition and accumulates it into the step-0 reset
  particle cotangent.
- Same-scalar central finite-difference parity checks for selected directions
  in initial `post_flow`, both corrected-log-weight tensors, and both residual
  noise tensors.
- Static route audit for new R6 helpers and the preserved material blocker.
- R6 result / close record and R7 handoff if R6 passes.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Bounded Claude read-only review of this subplan before code edits.
- Focused CPU-hidden local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
python -m py_compile \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  docs/benchmarks/contract_e_reset_tf.py
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r6-tiny-time-loop-reverse-scan-execution-subplan-2026-06-29.md \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py
```

- Bounded Claude read-only implementation/result review before advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the R5 one-step local Contract E manual VJP be accumulated through a tiny two-step reverse scan? |
| Baseline/comparator | Central finite differences of the exact same frozen-chart two-step scalar. |
| Primary pass criterion | Manual reverse-scan cotangent dots match same-scalar central finite differences for initial `post_flow`, both corrected-log-weight tensors, and both residual-noise tensors within frozen tolerances. |
| Veto diagnostics | Nonfinite scalar/cotangents, per-step floor/ridge/chart branch changes under the finite-difference perturbations, hidden generic autodiff in new helpers, `tf.linalg.eigh` in the fixed-ridge route, `transport_ad_mode="full"`, missing per-step replay artifacts, or missing Phase 3 material blocker. |
| Explanatory diagnostics | Per-step floor masks, realized ridge values, ridge attempts, cotangent norms, chart scales, and scalar components. |
| Not concluded | Full LGSSM gradient correctness, exact Kalman agreement, SIR/SV correctness, HMC readiness, production readiness, GPU/XLA/TF32 readiness, or correctness across branch-changing charts. |
| Artifact preserving result | R6 result note plus focused pytest output. |

## Forbidden Claims And Actions

- Do not remove, weaken, or bypass
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN` during R6.
- Do not run material Phase 3, full LGSSM FD, SIR/SV, GPU, or XLA commands in
  R6.
- Do not use generic TensorFlow autodiff as the implementation under test.
- Do not claim full filter gradient correctness from the two-step local fixture.
- Do not differentiate through floor decisions, ridge escalation, or chart
  construction.  The finite-difference scalar must use the same replayed charts
  as the manual route.

## Skeptical Plan Audit

- Wrong baseline risk: comparing manual stopped-chart cotangents to a finite
  difference scalar that recomputes center, scale, key, or `epsilon0` would be
  the wrong derivative.  Mitigation: record base charts for both steps and pass
  those exact charts into every center, plus, and minus scalar evaluation.
- Proxy metric risk: a tiny `T=2` parity pass is only a plumbing gate.  It is
  not a Phase 3 material gradient result and cannot remove the blocker.
- Hidden assumption risk: the deterministic transition must have an explicit
  manual transpose/VJP.  A transition with nonlinear or branchy behavior would
  confuse the gate, so R6 uses a fixed affine row-wise map.
- Environment risk: this is intentionally CPU-hidden local evidence.  No GPU or
  XLA status will be inferred.
- Artifact-risk check: the planned tests directly preserve the evidence needed
  for the stated engineering question: same-scalar FD parity and branch replay
  stability for a two-step reverse scan.

The plan passes this skeptical audit because each diagnostic answers the stated
R6 plumbing question, while the forbidden-claims section prevents promotion of
local evidence into material Phase 3 correctness.

## Exact Next-Phase Handoff Conditions

Advance to R7 only if:

- Claude plan review converges or all material review concerns are patched;
- the two-step same-scalar central finite-difference parity test passes;
- per-step floor/ridge/chart replay remains stable for all finite-difference
  directions;
- static route audits pass;
- focused local checks pass;
- Claude implementation/result review converges; and
- the material Phase 3 blocker remains active unless a later reviewed phase
  explicitly replaces it.

R7 should then plan the smallest real Phase 3 integration target: wiring the
manual reverse-scan route into the LGSSM diagnostic path while preserving the
material blocker until same-scalar FD and Kalman-gradient gates pass.

## Stop Conditions

Stop and write an R6 blocker result if:

- the two-step reverse scan requires generic autodiff to pass;
- same-scalar finite-difference parity fails after one focused repair attempt;
- a branch replay changes under the finite-difference perturbations;
- required per-step replay artifacts cannot be captured cleanly;
- static audit finds a hidden full-transport/autodiff/eigensystem path; or
- Claude review does not converge after five rounds for the same blocker.
