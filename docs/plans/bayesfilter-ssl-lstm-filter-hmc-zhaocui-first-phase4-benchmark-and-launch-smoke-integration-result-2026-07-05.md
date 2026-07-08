# Phase 4 Result: Shared Benchmark And Launch-Smoke Integration

Date: 2026-07-05

Status: `PASSED_PHASE4_SHARED_BENCHMARK_AND_LAUNCH_SMOKE`

## Phase Objective

Admit `zhaocui_fixed` into the existing shared SSL-LSTM benchmark and launch
smoke surfaces after Phase 3 focused schema/test success, while preserving the
diagnostic roles of benchmark metrics and HMC launch telemetry.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can `zhaocui_fixed` enter the shared benchmark and launch-smoke harnesses without changing benchmark semantics or overclaiming HMC readiness? |
| Baseline/comparator | Existing Phase 6 shared benchmark runner, Phase 7 launch-smoke runner, admitted SGQF/UKF rows, and Phase 2/3 `zhaocui_fixed` artifacts. |
| Primary pass criterion | Benchmark and launch-smoke tests pass with `zhaocui_fixed` admitted, LEDH still blocked, schema fields valid, and nonclaims preserved. |
| Veto diagnostics | Harness test failure, invalid artifact schema, treating heldout score/runtime as promotion criteria, HMC convergence claim, source-faithful parity claim, LEDH leakage, or default-policy change. |
| Explanatory diagnostics | Heldout predictive log score, decoded latent RMSE, runtime, score norm, finite-difference residual, and launch telemetry. |
| Not concluded | Posterior correctness, method superiority, HMC convergence, source-faithful parity, LEDH sufficiency, GPU/XLA production readiness, or default readiness. |

## Implementation Summary

Phase 4 updated:

- `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase6.py`
- `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase7.py`
- `tests/test_ssl_lstm_phase6_benchmark.py`
- `tests/test_ssl_lstm_phase7_hmc_smoke.py`

`zhaocui_fixed` is now admitted by the shared benchmark and launch-smoke
harnesses. `ledh_streaming_ot` remains blocked/status-only.

The Phase 6 finite-difference helper was also corrected to record the residual
between analytic score and finite-difference score, rather than the raw
finite-difference magnitude.

## Output Artifacts

| Artifact | Status |
| --- | --- |
| `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_shared_benchmark_cpu_hidden_2026-07-05.json` | Written |
| `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_shared_benchmark_cpu_hidden_2026-07-05.md` | Written |
| `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_hmc_launch_smoke_cpu_hidden_2026-07-05.json` | Written |
| `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_hmc_launch_smoke_cpu_hidden_2026-07-05.md` | Written |

## Shared Benchmark Summary

| Filter | Status | FD max abs residual | Heldout predictive log score | Role |
| --- | --- | ---: | ---: | --- |
| `fixed_sgqf` | `admitted` | `1.6961268920519522e-10` | `0.624174555480506` | explanatory/proxy only |
| `svd_ukf` | `admitted` | `2.637265906417323e-10` | `0.6241745156376752` | explanatory/proxy only |
| `zhaocui_fixed` | `admitted` | `2.868503600882838e-10` | `0.5626428710176841` | explanatory/proxy only |
| `ledh_streaming_ot` | `blocked` | N/A | N/A | status-only |

`score_finite_all_admitted` is `true`.

No ranking is supported by these descriptive/proxy metrics.

## Launch-Smoke Summary

| Filter | Status | Hard vetoes |
| --- | --- | --- |
| `fixed_sgqf` | `passed_launch_smoke` | none |
| `svd_ukf` | `passed_launch_smoke` | none |
| `zhaocui_fixed` | `passed_launch_smoke` | none |
| `ledh_streaming_ot` | `blocked` | `missing_manual_vjp_streaming_ot_score_path` |

The launch smoke uses two results, one burn-in step, one leapfrog step, and no
JIT. It is an HMC mechanics smoke only: no R-hat/ESS, convergence, ranking, or
posterior-validity claim is made.

## Checks Run

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_phase6_benchmark.py` | Passed: `2 passed in 31.31s` |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_phase7_hmc_smoke.py` | Passed: `2 passed in 15.29s` |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_protocol.py` | Passed: `18 passed in 3.55s` |
| `rg -n 'GradientTape\|tf\\.py_function\|np\\.\|numpy' bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py` | Passed: no hits |
| Forbidden-claims scan over changed Phase 4 files | Passed: hits were nonclaims/veto wording. |
| `git diff --check` | Passed |

CPU-only note: Phase 4 artifact runs were deliberate CPU-hidden debug/smoke
runs with `CUDA_VISIBLE_DEVICES=-1`, `tf32_mode=disabled`, and
`gpu_trust_basis=cpu_hidden_debug`. They are not production GPU/XLA evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `f98be292faabf3d1728f876ad211a70ac1ddf98c` |
| Worktree | Dirty before/during run; unrelated existing changes preserved. |
| Environment | Managed Codex shell, conda env `tfgpu`, TensorFlow `2.20.0`. |
| CPU/GPU status | CPU-hidden debug/smoke, logical GPUs `[]`. |
| Seeds | Phase 6 fixture `20260704`; Phase 7 fixture `20260705`; fixed `zhaocui_fixed` manifests recorded in JSON artifacts. |
| Phase 6 runtime | About `29.1s` in the regenerated artifact. |
| Phase 7 runtime | About `12.6s` in the regenerated artifact. |
| Result file | This file. |

## Skeptical Plan Audit

| Risk | Finding |
| --- | --- |
| Wrong baseline | Passed: Phase 4 used existing shared Phase 6/7 harnesses, not a one-off fixture. |
| Proxy metrics promoted | Passed: heldout score, RMSE, runtime, and launch telemetry remain explanatory only. |
| Missing stop conditions | Passed: harness failure, LEDH leakage, source-faithful claim, HMC convergence claim, and default-policy change remained vetoes. |
| Unfair comparison | Passed: no method ranking is made. |
| Hidden assumptions | Recorded: row admission and launch-smoke pass do not prove posterior correctness or HMC convergence. |
| Environment mismatch | Recorded: CPU-hidden debug/smoke only; no GPU/XLA production claim. |
| Artifact mismatch | Passed: artifacts are written by the shared benchmark and launch-smoke scripts. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Admit `zhaocui_fixed` through Phase 4 | Passed shared benchmark and launch-smoke integration | No Phase 4 hard veto for admitted rows; LEDH remains blocked | Longer HMC evidence, GPU/XLA production evidence, posterior validity, and source-faithful parity remain untested | Execute Phase 5 closeout and LEDH deferral handoff | No posterior correctness, method superiority, HMC convergence, source-faithful parity, LEDH sufficiency, GPU/XLA production readiness, or default readiness |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for `fixed_sgqf`, `svd_ukf`, and `zhaocui_fixed`; LEDH remains blocked/status-only. |
| Statistically supported ranking | Not claimed. |
| Descriptive-only differences | Heldout score, decoded RMSE, runtime, score norm, and launch telemetry are descriptive/proxy only. |
| Default-readiness | Not checked and not claimed. |
| Next evidence needed | Phase 5 closeout/reset memo, plus a separate future LEDH program if requested. |

## Post-Run Red-Team Note

Strongest alternative explanation: the shared fixture and two-step launch smoke
are too small to expose HMC convergence, posterior validity, or scaling
failures.

Result that would overturn this Phase 4 pass: a later review finds that
`zhaocui_fixed` admission changed benchmark semantics, used target autodiff, hid
adaptive randomness, or encoded a source-faithful/HMC convergence claim.

Weakest part of the evidence: all artifacts are CPU-hidden debug/smoke and
short-horizon; they validate harness integration, not scientific adequacy.
