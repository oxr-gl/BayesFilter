# Phase 3 Result: RK4 Loop Hygiene

Date: 2026-07-02

Status: `PASS_TO_PHASE4_REVIEW`

## Phase Objective

Replace P8p SIR RK4 forward aux-list storage and reverse `reversed(aux)` with
TensorFlow loop state, without changing the local RK4 transition or VJP
semantics.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 3 passed. The RK4 forward and VJP helper no longer trigger RK4 static audit rows. |
| Primary criterion status | Met: RK4 primal, aux, and VJP parity passed against an independent reference; RK4 audit rows are `ABSENT_CLEAN_OR_MOVED`. |
| Veto diagnostic status | No Phase 3 veto fired. Local RK4 VJP agrees with tape on the independent reference after reducing per-batch kappa/nu contributions. |
| Main uncertainty | Manual time scan and Sinkhorn surfaces remain unclean. |
| Next justified action | Phase 4 manual scan hygiene: move forward/reverse time scan records to TensorFlow loop state. |
| What is not concluded | No clean-XLA claim, no HLO evidence, no GPU runtime evidence, no full FD/numerical rerun, no HMC readiness. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded as a clean baseline; worktree is heavily dirty. |
| Commands | `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-static-audit-2026-07-02.json`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py::test_streaming_module_source_is_gpu_oriented tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r12_gpu_manual_score_route_is_explicit_reverse_scan tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r14_manual_dense_sinkhorn_recursions_use_tf_while_loop` |
| Environment | Local repo, CPU-hidden source/static/local parity checks. |
| CPU/GPU status | CPU-hidden by `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence. |
| Data version | N/A. |
| Random seeds | N/A for RK4 parity; deterministic tensors used. |
| Wall time | Audit tests: 4.10s; nearby static checks: 3.37s reported by pytest. |
| Output artifact paths | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-static-audit-2026-07-02.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-result-2026-07-02.md` |
| Execution ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-execution-ledger-2026-07-02.md` |
| Claude review ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md` |

## Artifacts Changed

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-static-audit-2026-07-02.json`

## Local Check Results

Static audit artifact summary:

| Field | Value |
| --- | --- |
| Decision | `FAIL_CURRENT_ROUTE` |
| Current-veto findings | 12 |
| Warning findings | 2 |
| `SIR-RK4-FWD-LIST` | `ABSENT_CLEAN_OR_MOVED` |
| `SIR-RK4-FWD-RANGE` | `ABSENT_CLEAN_OR_MOVED` |
| `SIR-RK4-REV-REVERSED` | `ABSENT_CLEAN_OR_MOVED` |
| `SIR-MANUAL-SEED-LOOP` | `ABSENT_CLEAN_OR_MOVED` |

Test results:

```text
tests/test_audit_ledh_clean_xla.py
......                                                                   [100%]
6 passed, 2 warnings in 4.10s

nearby existing static checks
...                                                                      [100%]
3 passed in 3.37s
```

The new RK4 test uses an independent reference implementation in the test file.
It compares:

- primal RK4 state;
- aux tensors needed by the reverse pass;
- VJP for points;
- batch-summed VJP for kappa and nu against `tf.GradientTape` on the independent
  reference.

## Implementation Summary

`_sir_transition_mean_with_aux_tf` now uses `tf.while_loop` and `TensorArray`
storage for per-substep RK4 tensors. `_sir_transition_mean_vjp_tf` now uses a
reverse `tf.while_loop` over stacked aux tensors.

## Post-Run Red-Team Note

The strongest misleading interpretation would be to say the whole manual score
route is now clean. That is wrong. Phase 3 fixed only RK4 substep loop hygiene.
The audit still reports `FAIL_CURRENT_ROUTE` because manual time-scan and
Sinkhorn findings remain.

The local VJP comparison required reducing per-batch kappa/nu contributions
before comparing to tape, because the manual VJP intentionally preserves
per-batch contributions while tape on a scalar returns the batch-summed
gradient.

## Next Handoff

Drafted next subplan:

`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-hygiene-subplan-2026-07-02.md`

Phase 4 may begin only after Claude read-only review of this Phase 3 result and
the Phase 4 subplan returns `VERDICT: AGREE`, or fixable findings are patched
and rereviewed.
