# Phase 2 Result: Minimal Oracle Implementation And Checks

Date: 2026-07-06

Status: `PASSED`

## Phase Objective

Implement and run the reviewed CPU-hidden minimal reference oracle for the
scalar-dimension `zhaocui_fixed` HMC target, without HMC runtime, GPU/XLA
runtime, full posterior claims, convergence claims, ranking claims, readiness
claims, source-faithful parity claims, or LEDH claims.

## Artifacts

| Artifact | Path |
| --- | --- |
| Harness | `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py` |
| Tests | `tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py` |
| JSON result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json` |
| Markdown result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.md` |
| Quiet log | `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase2_oracle_cpu_hidden_2026-07-06.log` |
| Phase 3 handoff subplan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-subplan-2026-07-06.md` |

## Review Record

Phase 2 subplan review used fresh visible Codex substitute review because the
external Claude gate was blocked earlier by the escalation reviewer for
private repository context transfer risk.

Review outcomes:

- Initial Phase 2 review: `VERDICT: AGREE`, no blockers.
- Focused grid-width repair review: `VERDICT: AGREE`, no blockers.

## Implementation Repairs Before Final Run

Two repairs were made before the final artifact run:

1. The grid width ladder was expanded from maximum half-width `2.0` to
   `20.0`, because `2.0` is only `0.4` prior standard deviations when
   `prior_scale = 5.0` and could cause predictable domain failures for
   prior-dominated directions.
2. The target/reference value gate was repaired from absolute-only
   `1.0e-9` to absolute `<= 1.0e-9` or relative `<= 1.0e-12`. A reduced-grid
   diagnostic found an absolute difference near `1.4e-9` on an extreme
   log-density near `-3.25e6`, with relative error around `4e-16`.

These repairs preserve the evidence boundary: they do not change the target,
do not run HMC, and do not convert conditional-slice evidence into full
posterior evidence.

## Checks Run

| Check | Result |
| --- | --- |
| `python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py` | passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py` | passed: `3 passed` |
| Full Phase 2 CLI artifact with default reviewed grid | passed |
| `git diff --check` | passed |
| Claim-boundary scan over new Phase 2 files | passed; hits were explicit nonclaims or forbidden-claim text |

The full CLI command was:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.md
```

Stdout/stderr were captured in the quiet log on the final rerun.

## Result Summary

| Diagnostic | Result | Role |
| --- | --- | --- |
| Artifact status | `passed` | primary criterion |
| Hard vetoes | `[]` | promotion veto |
| Base target/reference absolute error | `0.0` | promotion veto |
| Max target/reference absolute error | `1.862645149230957e-09` | promotion veto with relative tolerance |
| Max target/reference relative error | `8.881784197001252e-16` | promotion veto with absolute tolerance |
| Finite-difference score max absolute error | `9.438116954640918e-11` | promotion veto for local score consistency |
| Conditional slice edge-mass failures | none | promotion veto for selected slice adequacy |
| Wall time | `57.205707725006505` seconds | explanatory |

Selected passing widths:

| Index | Selected width |
| --- | --- |
| 0 | `20.0` |
| 4 | `20.0` |
| 8 | `20.0` |
| 12 | `20.0` |
| 13 | `5.0` |
| 14 | `10.0` |
| 15 | `2.0` |
| 16 | `5.0` |
| 19 | `20.0` |
| 22 | `20.0` |
| 23 | `5.0` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `f98be292faabf3d1728f876ad211a70ac1ddf98c` |
| Environment | Python/TensorFlow environment recorded in JSON artifact |
| CPU/GPU status | `CUDA_VISIBLE_DEVICES=-1`, no GPU devices visible |
| Trust basis | `cpu_hidden_debug_reference_no_gpu_claim` |
| TF32 enabled flag | recorded in JSON artifact; this is CPU-hidden non-JIT reference evidence |
| Seeds | initial `[20260705, 41]`, process `[20260705, 43]` |
| Data version | `frozen_inline_scalar_fixture_2026-07-06` |
| Plan file | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-master-program-2026-07-06.md` |
| Subplan file | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-subplan-2026-07-06.md` |

The quiet log contains TensorFlow CPU-hidden CUDA initialization noise and
retrace warnings. These are runtime/performance diagnostics only; the artifact
records CPU-hidden execution and no GPU claim is made.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 2 passed; conditional-slice target/reference oracle is available for later HMC diagnostics. |
| Primary criterion status | Passed: JSON status `passed`, no hard vetoes. |
| Veto diagnostic status | No hard vetoes fired. |
| Main uncertainty | Selected conditional one-dimensional slices do not establish full 24D posterior correctness. |
| Next justified action | Review Phase 3 longer-HMC diagnostics subplan and request explicit runtime approval before any longer HMC run. |
| What is not concluded | Full posterior correctness, HMC convergence, R-hat/ESS, ranking/superiority, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, or LEDH evidence. |

## Handoff

Phase 3 may proceed only after review of:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-subplan-2026-07-06.md`

Longer HMC runtime remains a human-required boundary. If the next phase is
approved, it must use the Phase 2 JSON artifact as a predeclared conditional
slice comparator and must not claim convergence or posterior correctness unless
its own reviewed criteria are satisfied.
