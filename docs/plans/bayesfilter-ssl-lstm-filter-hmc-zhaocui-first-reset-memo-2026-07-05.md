# Reset Memo: SSL-LSTM Zhao-Cui-First HMC Adapter Program

Date: 2026-07-05

Status: `RESET_MEMO_CURRENT`

## Current State

The Zhao-Cui-first master program completed its stated scope after crash
recovery. `zhaocui_fixed` is implemented as a deterministic fixed-variant
clean-room SSL-LSTM adapter with manual analytic score support.

`zhaocui_fixed` is admitted in:

- the focused adapter/schema tests;
- the shared Phase 6 SSL-LSTM benchmark harness;
- the Phase 7 launch-smoke harness.

`ledh_streaming_ot` remains blocked/status-only and deferred to a separate
future program.

## Main Files To Know

| File | Note |
| --- | --- |
| `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py` | New internal adapter. Target score path is manual TensorFlow chain rule, not autodiff. |
| `tests/test_ssl_lstm_zhaocui_fixed_adapter.py` | Focused tests, finite-difference checks, manifest and schema checks. |
| `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase6.py` | Shared benchmark admits `fixed_sgqf`, `svd_ukf`, and `zhaocui_fixed`; LEDH blocked. |
| `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase7.py` | Launch smoke runs the same three admitted filters; LEDH blocked. |
| `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase5-closeout-and-ledh-deferral-result-2026-07-05.md` | Final closeout result. |

## Evidence Limits

Do not claim:

- source-faithful SSL-LSTM Zhao-Cui parity;
- posterior correctness;
- method superiority or ranking;
- HMC convergence;
- LEDH sufficiency;
- GPU/XLA production readiness;
- default readiness.

Current evidence is CPU-hidden debug/smoke and short-horizon harness evidence.

## Most Recent Passing Checks

- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_phase6_benchmark.py`
  passed: `2 passed in 31.29s`.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_phase7_hmc_smoke.py`
  passed: `2 passed in 15.29s`.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_protocol.py`
  passed: `18 passed in 3.55s`.
- `git diff --check` passed.

## Generated Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-debug-value-score-artifact-2026-07-05.json`
- `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_shared_benchmark_cpu_hidden_2026-07-05.json`
- `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_shared_benchmark_cpu_hidden_2026-07-05.md`
- `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_hmc_launch_smoke_cpu_hidden_2026-07-05.json`
- `docs/benchmarks/ssl_lstm_filter_hmc_zhaocui_first_phase4_hmc_launch_smoke_cpu_hidden_2026-07-05.md`

## Worktree Note

The worktree was already dirty at recovery. Preserve unrelated existing changes
in HMC kernel tuning, inference, and earlier SSL-LSTM July 4 artifacts. The
Zhao-Cui-first changes are concentrated in the files named above plus the
July 5 Zhao-Cui-first plan/result artifacts.

## Next Sensible Work

Possible future work requires a new plan:

- longer replicated HMC evidence with predeclared diagnostics;
- reviewed GPU/XLA production-target benchmark evidence;
- separate LEDH implementation program;
- deeper source-route Zhao-Cui/TTSIRT work with fresh source anchors and
  explicit source-faithfulness scope.
