# Phase R5 Result: Local Manual Reverse-Scan Integration

Date: 2026-06-29

Status: `R5_LOCAL_INTEGRATION_PASSED_MATERIAL_STILL_BLOCKED`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r5-manual-reverse-scan-integration-execution-subplan-2026-06-29.md`

## Objective

Compose the R4 fixed-ridge Cholesky reset VJP with the existing manual dense
finite stopped-scale/key Sinkhorn transport-matrix VJP and log-normalization
VJP in a local one-step scalar, without reopening hidden autodiff or material
Phase 3.

## Claude Reviews

Plan review:

- Round 1: `VERDICT: REVISE`
- Round 2: `VERDICT: REVISE`
- Round 3: `VERDICT: AGREE`
- Round 4 fixed-chart delta: `VERDICT: AGREE`
- Round 5 stopped-key delta: `VERDICT: AGREE`

Implementation review:

- First broad prompt did not return a verdict; a small Claude probe returned
  `PROBE_OK`, so the prompt was narrowed.
- Narrow implementation review returned `VERDICT: AGREE`.

## Implementation

Added:

- `tests/test_contract_e_phase3_r5_manual_reverse_integration.py`

The test defines a one-step scalar

```text
S(post_flow, corrected_log_weights, residual_noise)
  = <Reset_fixed_ridge(post_flow, weights, M, residual_noise), U>
    + <increment, u_inc>
```

with:

- `increment = logsumexp(corrected_log_weights)`;
- `weights = exp(corrected_log_weights - increment)`;
- `transport_logw = log(max(weights, floor))`, with no post-floor
  renormalization;
- replayed base transport chart: center, scale, stopped key, and `epsilon0`;
- dense finite stopped-scale/key transport matrix `M`;
- fixed ridge `lambda = 0.75`;
- `epsilon = 0.55`, `scaling = 0.82`, `steps = 2`, and `floor = 0.05`;
- frozen upstream particle cotangent `U` from a deterministic linspace fixture;
- frozen increment upstream `u_inc = 0.37`.

The manual reverse composition:

1. calls `contract_e_cholesky_ridge_reset_fixed_ridge_vjp`;
2. sends the reset matrix cotangent through
   `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`;
3. propagates transport-coordinate cotangents through the replayed chart as
   `d post_flow = d x / scale`;
4. combines reset weight, floored-log-weight, and increment cotangents through
   `_normalize_log_weights_vjp`; and
5. compares the resulting cotangents to central finite differences of the same
   scalar.

## Local Evidence

Focused checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_phase3_r5_manual_reverse_integration.py tests/test_contract_e_cholesky_ridge_reset.py tests/test_contract_e_phase3_gradient_route_audit.py -q
python -m py_compile docs/benchmarks/contract_e_reset_tf.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py tests/test_contract_e_phase3_r5_manual_reverse_integration.py
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r5-manual-reverse-scan-integration-execution-subplan-2026-06-29.md tests/test_contract_e_phase3_r5_manual_reverse_integration.py
```

Outcomes:

- Focused pytest passed: `10 passed`.
- Python compile checks passed.
- Diff whitespace check passed.

The R5 parity test used central finite differences with step `1.0e-5` and
tolerances `rtol=2.0e-4`, `atol=2.0e-6`.  It checked the three required
input directions:

- `post_flow`;
- `corrected_log_weights`;
- `residual_noise`.

For each direction, the test also asserted center/`+h`/`-h` stability of:

- `floor_active = weights > floor`;
- realized ridge;
- ridge-attempt count; and
- ridge-failure flag.

The static audit covers the R5 local helpers and the named transitive manual
dense finite transport helper family for hidden generic autodiff,
`ForwardAccumulator`, `tf.gradients`, `tf.linalg.eigh`, and
`transport_ad_mode="full"` tokens.  The test also asserts that
`PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN` remains present in
the Phase 3 gradient diagnostic script.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| Local reset, transport-matrix, and normalization VJPs can be composed. | Passed locally | Same-scalar central-FD parity for one-step fixture. | No full time-loop reverse scan. |
| Replayed stopped chart is required and implemented. | Passed locally | Center, scale, stopped key, and `epsilon0` are replayed from the base fixture. | No claim for branch-changing charts. |
| Floor and ridge branches are fail-closed in the local gate. | Passed locally | Center/`+h`/`-h` replay assertions. | No derivative through branch selection. |
| Hidden autodiff/full transport/eigh audit for local R5 path passes. | Passed locally | Static audit test. | Does not audit unrelated repo files. |
| Material Phase 3 remains blocked. | Preserved | Blocker assertion in R5 static test. | No material LGSSM gradient evidence. |

## Nonclaims

R5 does not certify full LGSSM gradient correctness, Kalman agreement,
SIR/SV/nonlinear correctness, HMC readiness, production readiness, GPU/XLA
readiness, or correctness across floor/ridge/chart branch changes.  R5 does
not remove the material blocker.

## Next Step

The next justified phase is R6: integrate the local one-step reverse
composition into a tiny time-loop/manual reverse-scan fixture under a fresh
reviewed subplan.  R6 must remain local unless its reviewed subplan explicitly
authorizes a narrower material gate.
