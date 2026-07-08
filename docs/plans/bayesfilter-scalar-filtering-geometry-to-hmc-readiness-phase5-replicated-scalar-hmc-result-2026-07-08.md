# Phase 5 Result: Replicated Scalar HMC Diagnostic

Date: 2026-07-08
Status: `PASSED_FINITE_TELEMETRY_SCREEN`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Subplan: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-subplan-2026-07-08.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 5 replicated finite-telemetry screen passes | Passed: 3/3 fixed seeds produced finite retained samples, finite target-log-prob traces, finite log-accept ratios, no runtime exception, and structured artifacts | No hard vetoes; native divergence telemetry remains not exposed, not zero divergences | Three seeds with 16 retained samples each cannot establish convergence, posterior correctness, tuning quality, ranking, or default readiness; large finite negative log-accept tails were observed descriptively | Draft and review Phase 6 closeout subplan | No HMC convergence, posterior correctness, zero divergences, tuned kernel readiness, sampler superiority, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Across three fixed seeds, the Phase 4 fixed kernel continued to produce finite short-chain telemetry without hard vetoes. |
| Baseline/comparator | Phase 4 short-smoke artifact `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json`. |
| Primary criterion | Passed for seeds `(20260708, 5501)`, `(20260708, 5502)`, and `(20260708, 5503)` with `num_results = 16`, `num_burnin_steps = 4`, `L = 4`, `epsilon = 0.3925`. |
| Veto diagnostics | Final artifact vetoes are `[]`; `git diff --check` passed. |
| Explanatory diagnostics | Acceptance rates were `[0.9375, 0.9375, 0.75]`; max abs `u` values were about `[4.32, 5.45, 6.24]`; target log-probability overall range was about `[-42.32, -37.85]`; max abs finite log-accept ratios were about `[1.88, 77.76, 178.00]`. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, tuned kernel, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or source-faithful Zhao-Cui behavior. |
| Preserving artifacts | JSON/Markdown/log artifacts listed below plus this result and ledger entry. |

## Final Artifacts

- Script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_2026_07_08.py`
- Tests: `tests/test_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic.py`
- JSON: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.json`
- Markdown: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.md`
- Log: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.log`

## Seed Summary

| Seed index | Seed | Status | Acceptance | Finite samples | Nonfinite samples | Max abs `u` | Max abs finite log-accept |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `(20260708, 5501)` | `passed_short_smoke` | 0.9375 | 16 | 0 | 4.324986106081894 | 1.8844156046382514 |
| 1 | `(20260708, 5502)` | `passed_short_smoke` | 0.9375 | 16 | 0 | 5.454314651674424 | 77.7561559421061 |
| 2 | `(20260708, 5503)` | `passed_short_smoke` | 0.75 | 16 | 0 | 6.235419774840722 | 178.0000990804594 |

The large finite log-accept tails are descriptive caution and do not constitute convergence or tuning evidence. They also did not fire the Phase 5 hard veto because the predeclared hard screen was finite telemetry, runtime completion, and artifact integrity.

## Checks

- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_2026_07_08.py`: passed.
- `pytest tests/test_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic.py -q`: passed, `6 passed`.
- CPU-hidden replicated diagnostic command with `timeout 480`: passed and wrote structured artifacts.
- `git diff --check`: passed.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | Passed for Phase 5 replicated finite-telemetry diagnostic. |
| Statistically supported ranking | None; no method comparison and no uncertainty interval. |
| Descriptive-only differences | Per-seed acceptance, target-log-prob range, log-accept range, sample range, and runtime. |
| Default readiness | Not assessed. |
| HMC readiness | Not assessed; Phase 5 is a replicated finite-telemetry diagnostic only. |
| Next evidence needed | Phase 6 closeout may summarize boundaries; longer validation requires a new reviewed plan. |

## Handoff

Phase 6 may close the scalar filtering geometry-to-HMC readiness runbook by summarizing which gates passed and which scientific/runtime claims remain open. It must not promote the scalar finite-telemetry results into posterior correctness, convergence, tuned-kernel readiness, default readiness, GPU/XLA readiness, or source-faithful Zhao-Cui behavior.
