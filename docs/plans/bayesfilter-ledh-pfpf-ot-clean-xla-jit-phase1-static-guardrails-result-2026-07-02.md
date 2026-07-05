# Phase 1 Result: Static Guardrails

Date: 2026-07-02

Status: `PASS_TO_PHASE2_REVIEW`

## Phase Objective

Add static guardrails that mechanically detect the current unclean
compiled-path patterns before any implementation refactor claims clean XLA.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 1 passed. The static audit exists, tests pass, and the current source is correctly reported as `FAIL_CURRENT_ROUTE`. |
| Primary criterion status | Met: all current-veto Phase 0 pattern classes were detected with line-anchored findings; warning-only rows were reported separately. |
| Veto diagnostic status | No Phase 1 veto fired. The audit did not miss required current-veto patterns, did not treat stopped partial derivatives as scores, and did not use a whole-file fallback for required findings. |
| Main uncertainty | Static detection is necessary but does not prove runtime HLO loop representation. That remains deferred. |
| Next justified action | Phase 2 fixed randomness tensorization: move SIR process noise out of the compiled route into fixed tensors while preserving the current stateless seed policy. |
| What is not concluded | The route is not clean XLA yet. No compiler-time improvement, HLO evidence, numerical correctness, posterior correctness, or HMC readiness is claimed. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded as a clean baseline; worktree is heavily dirty. |
| Commands | `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-audit-2026-07-02.json`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py::test_streaming_module_source_is_gpu_oriented tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r12_gpu_manual_score_route_is_explicit_reverse_scan tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r14_manual_dense_sinkhorn_recursions_use_tf_while_loop` |
| Environment | Local repo, CPU-hidden source/static checks. |
| CPU/GPU status | CPU-hidden by `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence. |
| Data version | N/A. |
| Random seeds | N/A. |
| Wall time | Audit test: 0.09s; nearby static checks: 6.57s reported by pytest. |
| Output artifact paths | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-audit-2026-07-02.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-result-2026-07-02.md` |

## Artifacts Created

- `scripts/audit_ledh_clean_xla.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-audit-2026-07-02.json`

## Local Check Results

Static audit artifact summary:

| Field | Value |
| --- | --- |
| Decision | `FAIL_CURRENT_ROUTE` |
| Current-veto findings | 19 |
| Warning findings | 2 |
| Missing required patterns | 0 |
| Missing warning symbols | 0 |
| SIR source findings | 12 current veto |
| Transport source findings | 7 current veto, 2 current warning |

Test results:

```text
tests/test_audit_ledh_clean_xla.py
....                                                                     [100%]
4 passed in 0.09s

nearby existing static checks
...                                                                      [100%]
3 passed in 6.57s
```

## Interpretation

The current route is still unclean for the frozen clean-XLA target. The audit
now makes that plain and machine-readable. It finds:

- Python RK4 aux list and Python RK4 substep loop;
- Python reverse over RK4 aux records;
- Python time length binding and Python forward/reverse time scans;
- Python seed loop for process noise;
- stopped-key Sinkhorn helpers that must not be called scores;
- Python Sinkhorn iteration loops;
- warning-only local `GradientTape` use in the total streaming transport helper.

This is guardrail evidence only. It says future repairs cannot silently lose
coverage of these problems. It does not say the problems are fixed.

## Post-Run Red-Team Note

The strongest misleading interpretation would be to treat a passing Phase 1
pytest run as clean-XLA evidence. That is wrong. Phase 1 says the audit catches
the current problem; it does not say the compiled graph is clean.

The weakest part of the evidence is intentional: no HLO or GPU/XLA runtime
metric is present. Those gates belong to later phases after code is refactored.

## Next Handoff

Drafted next subplan:

`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-subplan-2026-07-02.md`

Phase 2 may begin only after Claude read-only review of this Phase 1 result and
the Phase 2 subplan returns `VERDICT: AGREE`, or fixable findings are patched
and rereviewed.
