# Phase 2 Result: Local Checks And Comparator Mechanics

Date: 2026-07-06

Status: `PASSED`

## Phase Objective

Rerun focused local checks, validate the generated minimal smoke artifacts, and
confirm that comparator mechanics remain descriptive-only before deciding
whether an optional launch-smoke bridge is needed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the Phase 1 harness and artifacts satisfy local boundary and schema checks without unsupported claims? |
| Baseline/comparator | Phase 1 generated artifact and existing scalar adapter tests. |
| Primary pass criterion | Focused compile/test/artifact validations pass and artifacts preserve primary/comparator role boundaries. |
| Veto diagnostics | Missing artifact, invalid schema, wrong dimensions, failed primary gate, nonfinite comparator row, unsupported claim, target-path autodiff/NumPy hit, or CPU-hidden run mislabeled as GPU/production evidence. |
| Explanatory diagnostics | Runtime, score norm, FD residual, comparator values, TensorFlow CUDA warning under CPU-hidden execution. |
| Not concluded | Posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Skeptical Plan Audit

Result: `PASSED`

This phase re-checks local artifacts only. It does not run a new experiment and
does not broaden the research question. The checks answer the artifact-boundary
question directly: whether the generated harness output still matches the stated
scalar mechanics scope and preserves nonclaims. The CUDA warning remains an
environment note under CPU-hidden execution, not evidence about GPU health or
production readiness.

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | Quiet log: `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_smoke_2026-07-06/compile.log` |
| Focused pytest | `PASSED` | Quiet log: `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_smoke_2026-07-06/pytest.log`; summary `3 passed in 7.17s`. |
| Harness rerun | `PASSED` | Quiet log: `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_smoke_2026-07-06/harness.log`; JSON summary reports `status=passed`. |
| JSON artifact validation | `PASSED` | Scalar dimensions, `primary_filter=zhaocui_fixed`, primary gate diagnostics, comparator roles, and CPU-hidden manifest were asserted. |
| Markdown/nonclaim scan | `PASSED_WITH_EXPECTED_NEGATED_HITS` | Matches were limited to explicit negative/nonclaim language. |
| Target-path forbidden scan | `PASSED` | No `GradientTape`, `tf.py_function`, `np.`, or `numpy` hits in `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`. |
| `git diff --check` | `PASSED` | Command returned exit status 0. |

## Local Artifact Snapshot

| Field | Value |
| --- | --- |
| JSON artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json` |
| Markdown artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md` |
| Primary filter | `zhaocui_fixed` |
| Primary FD max abs error | `8.616574120878795e-11` |
| Comparator rows | `fixed_sgqf`, `svd_ukf` |
| CPU-hidden manifest | `CUDA_VISIBLE_DEVICES=-1` |

Environment note: the quiet harness log still records TensorFlow attempting
CUDA initialization before reporting no visible device. The artifact remains
explicitly labeled as CPU-hidden debug evidence only.

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `PASS_ADVANCE_TO_PHASE3_DECISION` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_VETO_OBSERVED` |
| Main uncertainty | The artifact is intentionally narrow and does not establish scientific or runtime-production claims. |
| Next justified action | Decide whether the optional launch-smoke bridge is still needed for the program's narrow objective. |
| What is not being concluded | No posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Handoff

Phase 3 should not launch more work by inertia. It must decide explicitly
whether another smoke layer answers a still-open question or merely repeats the
same evidence under a broader runtime scope.
