# Phase 4 Result: Short HMC Smoke

Date: 2026-07-08
Status: `PASSED`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Subplan: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-subplan-2026-07-08.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 4 short fixed-kernel HMC smoke passes | Passed: final artifact reports `short_smoke_passed: true`, 8/8 retained samples finite, finite target-log-prob trace, finite log-accept ratios, and no runtime exception | No final artifact vetoes; native divergence telemetry is not exposed by this TFP kernel, so no zero-divergence claim is made | Eight retained samples are smoke evidence only and cannot assess convergence, posterior correctness, or tuning quality | Draft and review Phase 5 replicated scalar HMC diagnostic subplan | No HMC convergence, posterior correctness, tuned kernel readiness, sampler superiority, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | A short fixed-kernel smoke can produce finite retained samples and finite target/acceptance telemetry using the repaired Phase 3 coordinate composition. |
| Baseline/comparator | Phase 3 mechanics canary artifact `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json`. |
| Primary criterion | Passed for fixed `L = 4`, `epsilon = 0.3925`, `num_results = 8`, `num_burnin_steps = 2`. |
| Veto diagnostics | Final artifact vetoes are `[]`; `git diff --check` passed. |
| Explanatory diagnostics | Acceptance was 1.0 for 8/8 decisions; target log probability ranged from about `-43.93` to `-37.82`; max finite log-accept absolute value was about `1.22`; max absolute `u` sample was about `5.03`. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, tuned kernel, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or source-faithful Zhao-Cui behavior. |
| Preserving artifacts | JSON/Markdown/log artifacts listed below plus this result and ledger entry. |

## Final Artifacts

- Script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py`
- Tests: `tests/test_scalar_ssl_lstm_filtering_hmc_short_smoke.py`
- JSON: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json`
- Markdown: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.md`
- Log: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.log`

## Smoke Summary

| Field | Value |
| --- | --- |
| Kernel | fixed TFP HMC, no adaptation |
| Coordinate | `u`, with `z = u @ chol(M_z).T` and `free = center + scale * z` |
| Leapfrog steps | 4 |
| Step size | 0.3925 |
| Trajectory length | 1.57 |
| Retained samples | 8 |
| Burn-in steps | 2 |
| Retained finite samples | 8 |
| Retained nonfinite samples | 0 |
| Acceptance | 1.0 |
| Native divergence telemetry | Not exposed by kernel; not a zero-divergence claim |

## Checks

- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py`: passed.
- `pytest tests/test_scalar_ssl_lstm_filtering_hmc_short_smoke.py -q`: passed, `6 passed`.
- CPU-hidden short-smoke command with `timeout 240`: passed and wrote structured artifacts.
- `git diff --check`: passed.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | Passed for Phase 4 short smoke. |
| Statistically supported ranking | None; single short-smoke kernel only. |
| Descriptive-only differences | Acceptance, target-log-prob range, log-accept range, sample range, and runtime. |
| Default readiness | Not assessed. |
| HMC readiness | Not assessed; Phase 4 is short-smoke evidence only. |
| Next evidence needed | Reviewed Phase 5 replicated scalar HMC diagnostic if continuing. |

## Handoff

Phase 5 may be drafted as a small replicated scalar HMC diagnostic. It must include Monte Carlo uncertainty discipline, must not rank or promote the kernel using descriptive diagnostics alone, and must not claim convergence or posterior correctness unless the Phase 5 contract explicitly supports that claim with adequate diagnostics.
