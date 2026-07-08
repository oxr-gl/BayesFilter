# Phase 2 Subplan: Minimal SSL-LSTM Integration

Date: 2026-07-08
Status: `DRAFT_READY_FOR_LOCAL_REVIEW`
Master program: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`

## Phase Objective

Integrate the low-rank SPD quadratic geometry utility as an optional initial-geometry strategy in the minimal scalar SSL-LSTM `zhaocui_fixed` Phase 5 diagnostic harness.

## Entry Conditions Inherited From Phase 1

- Phase 1 utility and tests exist.
- `py_compile`, `pytest tests/test_quadratic_geometry.py -q`, and `git diff --check` passed.
- Utility remains classified as `extension_or_invention`.

## Required Artifacts

- Integration edits: `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
- Focused integration tests: `tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` and/or `tests/test_quadratic_geometry.py`
- Phase 2 result: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-result-2026-07-08.md`
- Phase 3 subplan: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-subplan-2026-07-08.md`

## Required Checks, Tests, Reviews

- Add `initial_geometry_strategy="low_rank_spd_quadratic"` or equivalent without changing the existing default unless explicitly reviewed.
- Ensure accepted utility geometry passes precision as `negative_hessian` and records covariance source/provenance.
- Ensure rejected utility geometry falls back explicitly to existing `map_candidate_hessian` or initial covariance path with rejection diagnostics preserved.
- Run:
  - `py_compile` on utility, benchmark, and focused tests.
  - `pytest tests/test_quadratic_geometry.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py -q`
  - `git diff --check`
- Codex local review of integration boundary and artifact fields.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal diagnostic consume the reusable low-rank SPD geometry result without hiding failures or changing readiness claims? |
| Baseline/comparator | Existing `map_candidate_hessian` and `initial_covariance` strategies. |
| Primary criterion | Focused integration tests pass and geometry diagnostics preserve selected source, fallback status, utility payload, nonclaims, and position role. |
| Veto diagnostics | Default strategy changed silently, rejected utility geometry loses diagnostics, accepted utility geometry lacks SPD provenance, fallback hides failure, unsupported MAP/HMC-readiness/source-faithfulness claim. |
| Explanatory only | Whether the utility accepts on the minimal target, residuals, condition number, center refinement, step/tau effects. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |

## Forbidden Claims And Actions

- Do not make low-rank SPD quadratic the default HMC policy.
- Do not describe an accepted quadratic fit as a true MAP covariance.
- Do not remove the existing MAP-candidate or covariance fallback paths.
- Do not run long HMC diagnostics in Phase 2.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- Integration tests pass.
- Phase 2 result records commands and nonclaims.
- Phase 3 subplan declares exact bounded CPU-hidden diagnostic commands/artifacts.

## Stop Conditions

- Integration would require changing public/default HMC policy.
- Focused tests fail after local repair.
- Utility diagnostics cannot be serialized into the benchmark artifact.
- The minimal target cannot be evaluated without crossing runtime or package-install boundaries.

## Local Review

Codex local review result before execution: `AGREE_WITH_BOUNDARIES`.

The subplan keeps the new strategy optional, preserves fallbacks, and treats acceptance/residuals as explanatory diagnostics only.
