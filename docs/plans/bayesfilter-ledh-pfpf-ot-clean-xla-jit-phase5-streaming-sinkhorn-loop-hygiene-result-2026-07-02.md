# Phase 5 Result: Streaming Sinkhorn Loop Hygiene

Date: 2026-07-02

Status: `PASS_TO_PHASE6_REVIEW`

## Phase Objective

Replace the targeted streaming finite Sinkhorn Python step loops and Python
state list with TensorFlow loop state while preserving focused finite-helper
outputs.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 5 passed for loop/state hygiene. |
| Primary criterion status | Met: the targeted `SINK-STOPPED-VALUE-RANGE`, `SINK-TOTAL-VALUE-RANGE`, and `SINK-STOPPED-VJP-STATES` audit rows are `ABSENT_CLEAN_OR_MOVED`; focused parity against the pre-edit fixture has overall max absolute difference `0.0`. |
| Veto diagnostic status | No Phase 5 veto fired. Focused static, parity, manual/regional/audit, and nearby static checks passed. |
| Main uncertainty | The stopped-key helper rows `SINK-STOPPED-VALUE-KEY` and `SINK-STOPPED-VJP-KEY` remain true. Those helpers compute partial derivatives and must not be called scores. |
| Next justified action | Phase 6 compiler metrics gate for the actual full route, with route evidence that `transport_ad_mode=full` uses the total-VJP transport helper rather than the stopped-key helper. |
| What is not concluded | No clean-XLA final claim, no GPU/HLO evidence, no FD ladder rerun, no HMC readiness, and no claim that stopped-key helpers compute the score. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded as a clean baseline; worktree is heavily dirty. |
| Commands | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py::test_phase5_sinkhorn_target_helpers_have_no_python_step_loop_or_state_list tests/test_audit_ledh_clean_xla.py::test_phase5_streaming_sinkhorn_loop_state_matches_preedit_fixture`; `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-static-audit-2026-07-02.json`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py::test_streaming_sinkhorn_recursion_vjp_matches_manual_and_tiny_autodiff`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_p8p_regional_kappa_gradient_decomposition.py tests/test_p8p_regional_orthogonal_gradient_decomposition.py tests/test_audit_ledh_clean_xla.py`; nearby static checks. |
| Environment | Local repo, CPU-hidden source/static/local parity checks. |
| CPU/GPU status | CPU-hidden by `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence. TensorFlow still emitted CUDA initialization noise in two CPU-hidden artifact scripts; that is not GPU evidence. |
| Data version | N/A. |
| Random seeds | Phase 5 deterministic tensor fixture, no random sampling. |
| Wall time | Focused Phase 5 tests: 4.86s; audit tests: 7.63s; streaming recursion tests: 8.69s; manual/regional/audit combined: 42.76s; nearby static checks: 3.63s. |
| Output artifacts | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-preedit-sinkhorn-loop-baseline-2026-07-02.json`; `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-sinkhorn-loop-parity-2026-07-02.json`; `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-static-audit-2026-07-02.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-streaming-sinkhorn-loop-hygiene-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-streaming-sinkhorn-loop-hygiene-result-2026-07-02.md` |

## Artifacts Changed

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-preedit-sinkhorn-loop-baseline-2026-07-02.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-sinkhorn-loop-parity-2026-07-02.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-static-audit-2026-07-02.json`

## Local Check Results

Static audit artifact summary:

| Field | Value |
| --- | --- |
| Decision | `FAIL_CURRENT_ROUTE` |
| Current-veto findings | 2 |
| Warning findings | 2 |
| Remaining current-veto IDs | `SINK-STOPPED-VALUE-KEY`, `SINK-STOPPED-VJP-KEY` |
| Phase 5 cleaned IDs | `SINK-STOPPED-VALUE-RANGE`, `SINK-TOTAL-VALUE-RANGE`, `SINK-STOPPED-VJP-STATES` |
| Warning ID | `SINK-TOTAL-CUSTOM-TAPE` |

Parity artifact summary:

| Comparator | Max Absolute Difference |
| --- | --- |
| stopped-key potential value helper vs pre-edit fixture | `0.0` |
| total-route potential value helper vs pre-edit fixture | `0.0` |
| stopped-key potential VJP helper vs pre-edit fixture | `0.0` |
| overall | `0.0` |

Test results:

```text
focused Phase 5 tests
..                                                                       [100%]
2 passed, 2 warnings in 4.86s

tests/test_audit_ledh_clean_xla.py
..........                                                               [100%]
10 passed, 2 warnings in 7.63s

streaming recursion VJP tests
..                                                                       [100%]
2 passed in 8.69s

manual/regional/audit combined
......................                                                   [100%]
22 passed, 2 warnings in 42.76s

nearby existing static checks
...                                                                      [100%]
3 passed in 3.63s
```

## Implementation Summary

The stopped-key streaming potential value helper and total-route potential
value helper now use `tf.while_loop` for finite Sinkhorn step iteration.

The stopped-key potential VJP helper now stores forward recursion state in
`TensorArray` objects and runs the reverse recursion with `tf.while_loop`.

The stopped-key helpers still contain `tf.stop_gradient(x)`. That is correct
as a statement about what those helpers currently compute: they are partial
derivative helpers. It would be wrong to call their output the score of the
executed finite-Sinkhorn scalar unless the missing total terms are included
elsewhere and verified.

## Post-Run Red-Team Note

The strongest misleading interpretation would be to say the route is now clean
XLA because the Python Sinkhorn loops are gone. That is still unsupported.
Phase 5 only fixed loop/state mechanics in targeted Sinkhorn helpers.

The actual score route must be checked in Phase 6. In the current code,
`transport_ad_mode="full"` routes through
`_filterflow_manual_streaming_finite_transport_total_vjp`; the stabilized route
routes through stopped-key helpers. Phase 6 must prove which route is compiled
and must not use stopped-key partial derivatives as score evidence.

## Next Handoff

Drafted next subplan:

`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-gate-subplan-2026-07-02.md`

Phase 6 may begin only after Claude read-only review of this Phase 5 result and
the Phase 6 subplan returns `VERDICT: AGREE`, or fixable findings are patched
and rereviewed.
