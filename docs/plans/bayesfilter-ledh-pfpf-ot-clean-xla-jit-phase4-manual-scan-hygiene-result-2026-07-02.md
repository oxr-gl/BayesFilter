# Phase 4 Result: Manual Scan Hygiene

Date: 2026-07-02

Status: `PASS_TO_PHASE5_REVIEW`

## Phase Objective

Replace the live P8p SIR manual score route's Python forward/reverse time scans
and Python `records` list with TensorFlow loop state.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 4 passed. The live `_manual_value_and_score_from_components` route no longer triggers manual-scan audit rows. |
| Primary criterion status | Met: manual-scan audit rows are `ABSENT_CLEAN_OR_MOVED`; same-input parity against the pre-edit fixture and renamed Python-record reference has zero max absolute difference. |
| Veto diagnostic status | No Phase 4 veto fired. Existing manual, regional, and audit tests pass. |
| Main uncertainty | Sinkhorn helper findings remain and still block clean-XLA status. |
| Next justified action | Phase 5 streaming Sinkhorn loop hygiene. |
| What is not concluded | No clean-XLA claim, no HLO evidence, no GPU runtime evidence, no full FD/numerical rerun, no HMC readiness. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded as a clean baseline; worktree is heavily dirty. |
| Commands | `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-static-audit-2026-07-02.json`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_p8p_regional_kappa_gradient_decomposition.py tests/test_p8p_regional_orthogonal_gradient_decomposition.py tests/test_audit_ledh_clean_xla.py`; nearby static checks. |
| Environment | Local repo, CPU-hidden source/static/local parity checks. |
| CPU/GPU status | CPU-hidden by `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence. |
| Data version | N/A. |
| Random seeds | Pre-edit fixture uses batch seed `81120`. |
| Wall time | Combined manual/regional/audit tests: 36.53s; nearby static checks: 3.20s. |
| Output artifacts | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-static-audit-2026-07-02.json`; `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-preedit-manual-scan-baseline-2026-07-02.json`; `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-parity-2026-07-02.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-hygiene-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-hygiene-result-2026-07-02.md` |
| Execution ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-execution-ledger-2026-07-02.md` |
| Claude review ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md` |

## Artifacts Changed

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-static-audit-2026-07-02.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-preedit-manual-scan-baseline-2026-07-02.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-parity-2026-07-02.json`

## Local Check Results

Static audit artifact summary:

| Field | Value |
| --- | --- |
| Decision | `FAIL_CURRENT_ROUTE` |
| Current-veto findings | 7 |
| Warning findings | 2 |
| Remaining current-veto IDs | `SINK-STOPPED-VALUE-KEY`, `SINK-STOPPED-VALUE-RANGE`, `SINK-TOTAL-VALUE-RANGE`, `SINK-STOPPED-VJP-KEY`, `SINK-STOPPED-VJP-STATES` |
| Warning ID | `SINK-TOTAL-CUSTOM-TAPE` |

Parity artifact summary:

| Comparator | Objective | Log likelihood | Gradient tensor | Per-seed gradient |
| --- | --- | --- | --- | --- |
| Loop route vs pre-edit JSON fixture | 0.0 | 0.0 | 0.0 | 0.0 |
| Loop route vs Python-record reference | 0.0 | 0.0 | 0.0 | 0.0 |

Test results:

```text
tests/test_audit_ledh_clean_xla.py
........                                                                 [100%]
8 passed, 2 warnings in 6.23s

manual/regional/audit combined
....................                                                     [100%]
20 passed, 2 warnings in 36.53s

nearby existing static checks
...                                                                      [100%]
3 passed in 3.20s
```

## Implementation Summary

The live `_manual_value_and_score_from_components` now uses TensorFlow
`tf.while_loop` and `TensorArray` state for forward and reverse time recursion.
It restores static shapes on TensorArray reads before calling existing VJP
primitives.

The old Python-record implementation was renamed to
`_manual_value_and_score_from_components_python_record_reference` and retained
only as a comparator. Static audit checks target the live route symbol, not the
reference helper.

## Post-Run Red-Team Note

The strongest misleading interpretation would be to claim the score route is
now clean XLA. That remains wrong. Phase 4 fixed the manual time scan only. The
static audit still reports `FAIL_CURRENT_ROUTE` because Sinkhorn helper
findings remain.

The comparator evidence is strong for same-input semantic preservation on the
focused fixture, but it is not a full FD ladder, not GPU/HLO evidence, and not a
scientific correctness proof.

## Next Handoff

Drafted next subplan:

`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-streaming-sinkhorn-loop-hygiene-subplan-2026-07-02.md`

Phase 5 may begin only after Claude read-only review of this Phase 4 result and
the Phase 5 subplan returns `VERDICT: AGREE`, or fixable findings are patched
and rereviewed.
