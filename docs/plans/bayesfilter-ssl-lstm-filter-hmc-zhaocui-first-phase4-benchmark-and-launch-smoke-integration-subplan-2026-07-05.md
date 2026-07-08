# Phase 4 Subplan: Shared Benchmark And Launch-Smoke Integration

Date: 2026-07-05

Status: `READY_FOR_EXECUTION`

## Phase Objective

Admit `zhaocui_fixed` into the existing shared SSL-LSTM benchmark and launch
smoke surfaces after Phase 3 focused schema/test success, while keeping all
benchmark metrics and HMC launch telemetry in their stated diagnostic roles.

## Entry Conditions

- Phase 2 adapter implementation result passed.
- Phase 3 focused schema/test result passed.
- `zhaocui_fixed` remains a clean-room fixed adaptation, not source-faithful
  SSL-LSTM Zhao-Cui parity.
- LEDH remains blocked/out of scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can `zhaocui_fixed` enter the shared benchmark and launch-smoke harnesses without changing benchmark semantics or overclaiming HMC readiness? |
| Baseline/comparator | Existing Phase 6 shared benchmark runner, Phase 7 launch-smoke runner, admitted SGQF/UKF rows, and Phase 2/3 `zhaocui_fixed` artifacts. |
| Primary pass criterion | Benchmark and launch-smoke tests pass with `zhaocui_fixed` admitted, LEDH still blocked, schema fields valid, and nonclaims preserved. |
| Veto diagnostics | Harness test failure, invalid artifact schema, treating heldout score/runtime as promotion criteria, HMC convergence claim, source-faithful parity claim, LEDH leakage, or default-policy change. |
| Explanatory diagnostics | Heldout predictive log score, decoded latent RMSE, runtime, score norm, finite-difference residual, and launch telemetry. |
| Not concluded | Posterior correctness, method superiority, HMC convergence, source-faithful parity, LEDH sufficiency, GPU/XLA production readiness, or default readiness. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase4-benchmark-and-launch-smoke-integration-result-2026-07-05.md` |

## Planned Edits

- Update `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase6.py` so
  `zhaocui_fixed` is admitted and evaluated by the shared fixture.
- Update `tests/test_ssl_lstm_phase6_benchmark.py` expected admitted/blocked
  rows and status fields.
- Inspect and update Phase 7 launch-smoke code/tests only if they still block
  `zhaocui_fixed`.
- Do not change public APIs, package metadata, default policy, model files, or
  LEDH code.

## Planned Checks

- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_phase6_benchmark.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_phase7_hmc_smoke.py`
- Focused benchmark command if the tests do not already execute the runner.
- `git diff --check`
- Forbidden-claims scan over changed Phase 4 files.

## Skeptical Plan Audit

| Risk | Pre-run finding |
| --- | --- |
| Wrong baseline | Passed: integration uses the existing shared benchmark and launch-smoke harnesses. |
| Proxy metrics promoted | Passed: heldout score, RMSE, runtime, and launch telemetry are explanatory only. |
| Missing stop conditions | Passed: harness failure, LEDH leakage, source-faithful claim, and HMC convergence claim are vetoes. |
| Unfair comparison | Passed: no method ranking is planned. |
| Hidden assumptions | Recorded: Phase 4 can admit a row without proving HMC convergence or posterior correctness. |
| Stale context | Phase 2/3 artifacts were written and checked in this session. |
| Environment mismatch | CPU-hidden debug/smoke checks only unless a later reviewed GPU run is explicitly planned. |
| Artifact mismatch | Planned tests must inspect shared benchmark rows, not a one-off fixture. |

## Stop Conditions

Stop and write a blocker result if admitting `zhaocui_fixed` requires changing
benchmark semantics, promotion criteria, default policy, public API, LEDH code,
package installs, network fetches, or unsupported source-faithfulness/HMC
readiness claims.
