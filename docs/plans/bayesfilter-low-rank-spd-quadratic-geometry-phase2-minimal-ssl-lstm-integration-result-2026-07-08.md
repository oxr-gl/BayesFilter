# Phase 2 Result: Minimal SSL-LSTM Integration

Date: 2026-07-08
Status: `PASSED_FOCUSED_INTEGRATION_CHECKS`

## Decision

Phase 2 passed. The minimal scalar SSL-LSTM Phase 5 diagnostic harness now supports an optional `low_rank_spd_quadratic` initial-geometry strategy while preserving the existing `map_candidate_hessian` default.

Accepted low-rank utility geometry is transformed from prior-whitened coordinates back to original parameter coordinates and supplied as a precision/negative-Hessian candidate. Rejected low-rank geometry preserves the utility payload and falls back explicitly to the existing MAP-candidate/initial geometry path.

## Implementation

| Artifact | Path |
| --- | --- |
| Benchmark integration | `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py` |
| Focused integration tests | `tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` |
| Utility tests | `tests/test_quadratic_geometry.py` |

## Checks

| Check | Status |
| --- | --- |
| `py_compile` on utility, benchmark, and focused tests | passed |
| `pytest tests/test_quadratic_geometry.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py -q` | passed: `18 passed, 27 warnings` |
| `git diff --check` | passed |

## Evidence Contract Assessment

| Field | Result |
| --- | --- |
| Question | The minimal diagnostic can consume the reusable low-rank SPD geometry result without hiding failures or changing readiness claims. |
| Baseline/comparator | Existing `map_candidate_hessian` and `initial_covariance` strategies remain available; default remains unchanged. |
| Primary criterion | Passed: integration tests verify accepted precision transformation and rejected-attempt provenance/fallback. |
| Veto diagnostics | No silent default change, no hidden fallback, no missing rejection status, no unsupported readiness/source-faithfulness claim in focused tests. |
| Explanatory only | Actual minimal-target acceptance/rejection and HMC tuning effects remain for Phase 3 diagnostic. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `ADVANCE_TO_PHASE3` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_PHASE2_VETO` |
| Main uncertainty | The real minimal SSL-LSTM target may reject the quadratic fit or still fail to produce a viable HMC `L, epsilon` pair. |
| Next justified action | Run a bounded CPU-hidden diagnostic with `--initial-geometry-strategy low_rank_spd_quadratic`. |
| What is not being concluded | No HMC convergence, posterior correctness, statistical ranking, default readiness, or source-faithful Zhao-Cui parity. |

## Boundary Notes

The new strategy is optional. It is an `extension_or_invention`, not source-faithful Zhao-Cui evidence.
