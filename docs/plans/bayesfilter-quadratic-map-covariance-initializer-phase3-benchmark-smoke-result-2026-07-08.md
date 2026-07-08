# Phase 3 Result: Benchmark Adoption Smoke

Date: 2026-07-08

## Status

`PASSED_BOUNDED_BENCHMARK_SMOKE`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 3 passes. Proceed to Phase 4 closeout. |
| Primary criterion status | Passed: a bounded identifiable SSL-LSTM oracle smoke exercises `estimate_quadratic_map_covariance` and verifies covariance provenance, optimizer role, geometry status, mass-matrix SPD summaries, and nonclaims. |
| Veto diagnostic status | No HMC launch, GPU/long benchmark launch, broad benchmark refactor, unsupported MAP/HMC/posterior claim, focused test failure, or removal of existing oracle coverage occurred. |
| Main uncertainty | The smoke is integration evidence only; it does not validate SSL-LSTM covariance quality for HMC or posterior correctness. |
| Next justified action | Close out with final checks, residual gaps, and next HMC-readiness gates. |
| Not concluded | No global MAP, posterior covariance correctness, HMC readiness, sampler convergence, statistical superiority, default readiness, or Zhao-Cui source faithfulness. |

## Changes

- Added `test_reusable_quadratic_map_covariance_smoke_on_oracle_target` to
  `tests/test_identifiable_ssl_lstm_oracle_geometry.py`.
- The smoke uses a bounded `horizon=40` identifiable oracle target and asserts
  integration/provenance fields only.

## Checks Run

| Check | Result |
| --- | --- |
| `pytest tests/test_identifiable_ssl_lstm_oracle_geometry.py tests/test_quadratic_map_covariance.py -q` | Passed: `12 passed`, TFP/gast deprecation warnings only. |
| `python -m py_compile docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py bayesfilter/inference/quadratic_map_covariance.py` | Passed, exit 0. |
| `git diff --check` | Passed, exit 0. |

## Plain-Language Gate

| Item | Status |
| --- | --- |
| Claimed target | Correct: benchmark-facing integration smoke only. |
| Computed quantity | Correct: bounded oracle test result and source compile/diff checks. |
| Unsupported claims | None accepted; HMC/posterior/default-readiness remain unsupported. |
| Mismatches | None found. |
| Remaining unevaluated | Longer SSL-LSTM covariance quality, HMC tuning, posterior/reference agreement, sampler convergence. |

## Handoff To Phase 4

Phase 4 should run final focused checks, inspect the worktree, write a closeout
result, and state remaining gaps before HMC can be claimed.
