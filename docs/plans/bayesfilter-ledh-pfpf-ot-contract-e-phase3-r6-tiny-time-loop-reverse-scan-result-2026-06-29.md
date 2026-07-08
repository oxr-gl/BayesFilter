# Phase R6 Result: Tiny Time-Loop Manual Reverse Scan

Date: 2026-06-29

Status: `R6_TINY_TIME_LOOP_PASSED_MATERIAL_STILL_BLOCKED`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r6-tiny-time-loop-reverse-scan-execution-subplan-2026-06-29.md`

## Objective

Test whether the R5 one-step Contract E manual VJP composition can be
accumulated through a tiny fixed-branch time reverse scan before reopening any
material Phase 3 LGSSM gradient evidence.

## Claude Reviews

Plan review:

- `VERDICT: AGREE`
- Claude agreed that the subplan safely scoped R6 as a `T=2` local plumbing
  gate and did not authorize Phase 3 material evidence.  Claude's only caution
  was to use deterministic directions strong enough that cross-time cotangent
  bugs could not hide.

Implementation review:

- `VERDICT: AGREE`
- Claude confirmed that the implementation uses:
  - a two-step forward path;
  - a deterministic affine step-0 to step-1 transition;
  - an explicit transition VJP;
  - frozen replayed charts for the center, plus, and minus finite-difference
    scalar evaluations;
  - static route audits for hidden generic autodiff, full transport, and
    `tf.linalg.eigh`; and
  - an explicit preserved-blocker assertion.

## Implementation

Added:

- `tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py`

The R6 scalar is

```text
S =
  <particles_0, U_0>
  + <particles_1, U_1>
  + <increment_0, u_0>
  + <increment_1, u_1>,
```

where each `particles_t` is produced by the same local Contract E step used in
R5:

```text
corrected_log_weights_t
  -> normalize
  -> floored transport log weights
  -> replayed stopped-scale/key finite Sinkhorn matrix
  -> fixed-ridge Cholesky Contract E reset.
```

Step 1 receives its `post_flow` from a deterministic affine transition applied
to step-0 reset particles.  The manual reverse scan sends the step-1
`post_flow` cotangent through the explicit transpose of that transition and
adds it to the direct step-0 particle cotangent before running the step-0 VJP.

The finite-difference comparator uses the exact same frozen per-step charts as
the manual route.  The test checks deterministic directions for:

- initial `post_flow0`;
- `corrected_log_weights0`;
- `corrected_log_weights1`;
- `residual_noise0`; and
- `residual_noise1`.

For each direction, the test also asserts center/`+h`/`-h` stability of:

- step-0 and step-1 floor masks;
- step-0 and step-1 realized ridge values;
- step-0 and step-1 ridge-attempt counts; and
- step-0 and step-1 ridge-failure flags.

## Local Evidence

Focused checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py -q
```

Outcome: `2 passed`.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
```

Outcome: `12 passed`.

```bash
python -m py_compile \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  docs/benchmarks/contract_e_reset_tf.py
```

Outcome: passed.

```bash
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r6-tiny-time-loop-reverse-scan-execution-subplan-2026-06-29.md \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py
```

Outcome: passed.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| R5 local VJP composition can be accumulated through a tiny two-step reverse scan. | Passed locally | Same-scalar central-FD parity for five deterministic directions across both steps. | No full LGSSM gradient correctness. |
| Cross-time cotangent plumbing is active. | Passed locally | The test asserts nonzero step-1 `post_flow` and transition-backprop cotangent norms. | No claim for nonlinear transition VJPs beyond this affine fixture. |
| Frozen chart replay is enforced. | Passed locally | Base charts are captured once and reused for center, plus, minus, and manual evaluations. | No derivative through chart construction. |
| Branch stability is fail-closed. | Passed locally | Floor masks, ridge values, ridge attempts, and ridge failures are checked for center/plus/minus. | No correctness across branch changes. |
| Hidden autodiff/full-transport/eigh audit passes for the R6 local route. | Passed locally | Static audit covers new R6 helpers, reset fixed-ridge helpers, and manual finite transport helper family. | Does not audit unrelated repo code. |
| Material Phase 3 remains blocked. | Preserved | R6 static audit asserts `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN` remains present. | No material Phase 3 evidence. |

## Nonclaims

R6 does not certify exact Kalman agreement, material LGSSM gradient
correctness, SIR/SV correctness, HMC readiness, production readiness,
GPU/XLA/TF32 readiness, or correctness across floor/ridge/chart branch changes.
R6 does not remove or weaken the material Phase 3 blocker.

## Next Step

The next justified phase is R7: plan and implement the smallest real LGSSM
diagnostic integration of the manual likelihood reverse-scan route.  R7 must
still preserve the material blocker until a reviewed same-scalar FD and exact
Kalman-gradient gate passes.
