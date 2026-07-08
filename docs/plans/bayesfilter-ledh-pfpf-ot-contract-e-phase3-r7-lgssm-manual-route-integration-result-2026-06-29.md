# Phase R7 Result: Tiny LGSSM Manual Route Integration

Date: 2026-06-29

Status: `R7_TINY_LGSSM_ROUTE_PASSED_MATERIAL_STILL_BLOCKED`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r7-lgssm-manual-route-integration-subplan-2026-06-29.md`

## Objective

Wire the Contract E fixed-ridge manual reverse-scan route into the smallest
LGSSM diagnostic path that shares the Phase 3 scalar structure, while
preserving the material Phase 3 blocker.

## Claude Reviews

Plan review:

- Round 1: `VERDICT: REVISE`
- Claude required exact commands/environment, concrete tiny fixture scope,
  explicit FD tolerances and step, a fail-closed fixed-ridge route label, and
  explicit separation from branchy ridge escalation.
- Round 2: `VERDICT: AGREE`

Implementation review:

- `VERDICT: AGREE`
- Claude confirmed the tiny fixed-ridge route uses `D=1`, `T=2`, `N=4`,
  `batch=1`, deterministic fixture tensors, frozen charts, all three parameter
  FD checks, explicit route label, no audited generic autodiff/full
  transport/eigh/branchy reset path, and preserved blocker assertion.

## Implementation

Added:

- `tests/test_contract_e_phase3_r7_lgssm_manual_route.py`

The new test implements route label:

```text
contract_e_cholesky_fixed_ridge_manual_lgssm_tiny
```

The route is a tiny LGSSM scalar with:

- `state_dim=1`;
- `time_steps=2`;
- `num_particles=4`;
- `batch_size=1`;
- `dtype=tf.float64`;
- deterministic initial particles, transition noise, Contract E residual
  noise, and observations;
- fixed ridge `lambda=0.75`; and
- replayed per-time transport charts.

The forward path uses the same conceptual Phase 3 scalar components:

```text
prior_mean -> transition noise -> LEDH flow
  -> transition/observation log-density correction
  -> normalize corrected weights
  -> finite dense stopped-scale/key transport matrix
  -> fixed-ridge Cholesky Contract E reset
  -> next particles.
```

The manual reverse scan:

1. runs the fixed-ridge Contract E reset VJP;
2. pushes the reset matrix cotangent through the manual dense finite Sinkhorn
   transport-matrix VJP;
3. pushes normalized-weight and increment cotangents through log
   normalization;
4. distributes corrected-log-weight cotangents through the log-weight
   correction identity;
5. uses the existing LGSSM transition-density, observation-density, and LEDH
   flow VJPs; and
6. accumulates parameter scores for
   `ar_coefficient`, `log_transition_variance`, and
   `log_observation_variance`.

## Local Evidence

Focused checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_phase3_r7_lgssm_manual_route.py -q
```

Outcome: `2 passed`.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
```

Outcome: `14 passed`.

```bash
python -m py_compile \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  docs/benchmarks/contract_e_reset_tf.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py
```

Outcome: passed.

```bash
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r7-lgssm-manual-route-integration-subplan-2026-06-29.md \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r6-tiny-time-loop-reverse-scan-result-2026-06-29.md
```

Outcome: passed.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| The Contract E manual reverse-scan route can be wired through a tiny LGSSM scalar. | Passed locally | Same-scalar central FD parity for all three LGSSM parameters. | No material Phase 3 correctness. |
| Fixed-ridge forward and VJP comparator are separated from branchy ridge escalation. | Passed locally | Explicit route label and static audit forbid `contract_e_cholesky_ridge_reset(` in the audited R7 route. | No claim about branchy reset derivatives. |
| Frozen-chart replay is enforced. | Passed locally | Charts are built once at the center fixture and reused for manual, center, plus, and minus evaluations. | No derivative through chart construction. |
| Route uses existing manual LGSSM VJP primitives. | Passed locally | Test calls existing transition-density, observation-density, flow, normalization, transport, and reset VJPs. | No public API or production route claim. |
| Hidden autodiff/full-transport/eigh audit passes for the R7 local route. | Passed locally | Static audit covers local helpers plus reset, transport, and LEDH VJP helpers. | Does not audit unrelated repo paths. |
| Material Phase 3 remains blocked. | Preserved | Static audit asserts `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN` remains in the material diagnostic script, and the R7 route label is not in that script yet. | Phase 3 not unblocked. |

## Nonclaims

R7 does not certify material Phase 3 gradient correctness, exact Kalman
agreement, broad LGSSM correctness, SIR/SV correctness, HMC readiness,
production readiness, GPU/XLA/TF32 readiness, or correctness across
floor/ridge/chart branch changes.

R7 does not remove or weaken the material Phase 3 blocker.

## Next Step

The next justified phase is R8: refactor or share the tiny verified fixed-ridge
manual route into the Phase 3 LGSSM diagnostic path, then prove that the
material score path no longer uses the outer `tf.GradientTape` wrapper before
any blocker replacement is considered.
