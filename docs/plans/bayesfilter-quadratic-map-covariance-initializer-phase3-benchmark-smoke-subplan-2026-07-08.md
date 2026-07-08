# Phase 3 Subplan: Benchmark Adoption Smoke

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Exercise the reusable quadratic MAP-covariance initializer from a
benchmark-facing context with the smallest bounded smoke that proves the API can
replace or support benchmark-local MAP/covariance initialization logic.

## Entry Conditions Inherited From Previous Phase

- Phase 2 status: `PASSED_FOCUSED_VALIDATION`.
- Focused pytest passed: `11 passed`, TFP deprecation warnings only.
- The reusable API is exported and tested on controlled Gaussian targets.

## Required Artifacts

- Either:
  - a focused benchmark/test update that imports and uses
    `estimate_quadratic_map_covariance`, or
  - a Phase 3 result explicitly explaining why broad benchmark refactor is not
    justified now and recording a bounded smoke instead.
- Focused command output or log.
- Phase 3 result record.
- Draft Phase 4 closeout subplan.

## Required Checks, Tests, Reviews

- Candidate checks:
  - `pytest tests/test_identifiable_ssl_lstm_oracle_geometry.py tests/test_quadratic_map_covariance.py -q`
  - or a narrower smoke if the oracle geometry test is too broad for this
    integration question.
- `python -m py_compile docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py` if the benchmark file is changed.
- `git diff --check`
- Codex self-review of any benchmark/result language for unsupported claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the reusable initializer be exercised from the identifiable SSL-LSTM oracle/benchmark-facing layer without breaking existing focused tests? |
| Baseline/comparator | Existing benchmark-local `estimate_map_center`, `dense_negative_hessian`, and low-rank geometry use. |
| Primary pass criterion | A bounded benchmark-facing smoke passes and records that it is integration evidence only, not HMC readiness or posterior correctness. |
| Veto diagnostics | HMC launch, GPU/long benchmark launch, broad refactor without need, unsupported HMC/MAP/posterior claim, failing focused tests, or removal of existing oracle geometry coverage. |
| Explanatory diagnostics | API import path, result status, covariance source, geometry status, mass regularization status. |
| Not concluded | No SSL-LSTM covariance quality claim beyond smoke, no global MAP, no posterior correctness, no HMC readiness, no sampler convergence, no default readiness. |
| Artifact preserving result | Phase 3 result note and test/benchmark diff. |

## Forbidden Claims And Actions

- Do not claim HMC readiness, posterior correctness, global MAP, default
  readiness, sampler convergence, or Zhao-Cui source faithfulness.
- Do not run HMC, GPU benchmarks, long ladders, package installs, commits,
  pushes, or detached supervisors.
- Do not rewrite benchmark architecture broadly.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 smoke passes or a blocker/no-refactor result is written;
- Phase 3 result is written;
- Phase 4 closeout subplan is drafted with final checks and residual gaps.

## Stop Conditions

- Existing oracle tests fail because of the integration and cannot be repaired
  locally.
- The benchmark-facing integration requires broad refactor or long runtime.
- The smoke would be misleading without HMC/GPU/posterior evidence.

## Skeptical Plan Audit

| Risk | Phase 3 audit |
| --- | --- |
| Wrong baseline | Baseline is current benchmark-local geometry plumbing, not HMC output. |
| Proxy metric promoted | Smoke only proves integration; no covariance quality or HMC claim. |
| Missing stop conditions | Stop conditions are explicit above. |
| Unfair comparison | No method ranking occurs. |
| Hidden assumptions | Any smoke-specific tolerances must be recorded in the result. |
| Stale context | Use current tests/benchmark file after Phase 2. |
| Environment mismatch | CPU-safe test/smoke only; no GPU/HMC evidence. |
| Artifact mismatch | Test/benchmark diff and result note answer integration question only. |

Audit status: `PASSED_FOR_PHASE_3_SMOKE`.
