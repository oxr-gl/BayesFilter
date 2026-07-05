# Phase 2 Result: Fixed Randomness Tensorization

Date: 2026-07-02

Status: `PASS_TO_PHASE3_REVIEW`

## Phase Objective

Move P8p SIR process-noise generation out of the compiled value/score route and
into a fixed tensor while preserving the existing stateless seed policy.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 2 passed. The manual score route no longer builds process noise with a Python seed loop or `tf.random.stateless_normal`. |
| Primary criterion status | Met: `SIR-MANUAL-SEED-LOOP` is now `ABSENT_CLEAN_OR_MOVED`; the fixed tensor parity test passes. |
| Veto diagnostic status | No Phase 2 veto fired. The old seed formula, shape, dtype, and time/seed ordering are preserved by test. |
| Main uncertainty | The route still fails clean-XLA static audit because RK4, time scan, reverse scan, and Sinkhorn findings remain. |
| Next justified action | Phase 3 RK4 loop hygiene: replace RK4 forward aux list and reverse `reversed(aux)` with TensorFlow loop state. |
| What is not concluded | No clean-XLA claim, no HLO evidence, no GPU runtime evidence, no FD/numerical rerun, no HMC readiness. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded as a clean baseline; worktree is heavily dirty. |
| Commands | `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-static-audit-2026-07-02.json`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py::test_streaming_module_source_is_gpu_oriented tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r12_gpu_manual_score_route_is_explicit_reverse_scan tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r14_manual_dense_sinkhorn_recursions_use_tf_while_loop`; targeted AST check for `_manual_value_and_score_from_components`. |
| Environment | Local repo, CPU-hidden source/static/semantic checks. |
| CPU/GPU status | CPU-hidden by `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence. |
| Data version | N/A. |
| Random seeds | `101,202` in fixed-noise parity test; production builder uses `args.batch_seeds`. |
| Wall time | Audit tests: 7.57s; nearby static checks: 3.57s reported by pytest. |
| Output artifact paths | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-static-audit-2026-07-02.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-result-2026-07-02.md` |
| Execution ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-execution-ledger-2026-07-02.md` |
| Claude review ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md` |

## Artifacts Changed

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-static-audit-2026-07-02.json`

## Local Check Results

Static audit artifact summary:

| Field | Value |
| --- | --- |
| Decision | `FAIL_CURRENT_ROUTE` |
| Current-veto findings | 16 |
| Warning findings | 2 |
| `SIR-MANUAL-SEED-LOOP` | `ABSENT_CLEAN_OR_MOVED` |
| Missing required patterns | 0 |

Test results:

```text
tests/test_audit_ledh_clean_xla.py
.....                                                                    [100%]
5 passed, 2 warnings in 7.57s

nearby existing static checks
...                                                                      [100%]
3 passed in 3.57s
```

Targeted source check:

```text
_manual_value_and_score_from_components contains tf.random.stateless_normal: False
_manual_value_and_score_from_components contains for seed in args.batch_seeds: False
_manual_value_and_score_from_components reads transition_noise[:, time_index, :, :]: True
```

## Implementation Summary

Added `_make_transition_noise_tensor(...)` with shape:

```text
[batch_size, time_steps, num_particles, state_dim]
```

The builder preserves the previous stateless seed formula:

```text
seed = [batch_seed % 2147483647, (1140 + time_index) % 2147483647]
```

Both the value callback path and the manual score route now consume
`tensors["transition_noise"]`. The manual score route no longer creates
`noise_rows` or calls `tf.random.stateless_normal`.

## Post-Run Red-Team Note

The strongest misleading interpretation would be to say the route is now clean
XLA. That is wrong. Phase 2 removed only the process-noise Python seed loop from
the manual route. The audit still reports `FAIL_CURRENT_ROUTE`, which is the
correct status.

The weakest part of this phase is that parity was checked for fixed noise
construction, not for the full likelihood/score after all future refactors.
Full numerical validation remains deferred.

## Next Handoff

Drafted next subplan:

`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-subplan-2026-07-02.md`

Phase 3 may begin only after Claude read-only review of this Phase 2 result and
the Phase 3 subplan returns `VERDICT: AGREE`, or fixable findings are patched
and rereviewed.
