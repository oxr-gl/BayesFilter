# P8h Phase 5 Subplan: Value And Filtering Tuning

Date: 2026-06-15

Status: `READY_FOR_REVIEW_AFTER_PHASE4`

## Phase Objective

Create and run trusted GPU multi-seed particle-count tuning for the exact
Phase 4 OT-resampled route with finite values, runtime, transport residuals,
value stability, ESS diagnostics, and adjacent-rung stability.

## Entry Conditions

- Phase 4 local diagnostics passed for
  `ot_sinkhorn_barycentric_covariance_carry` with canonical `[5, 5]`
  transport and trusted GPU tensor evidence.

## Required Artifacts

- P8h-specific tuning runner surface in
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`; the P8g
  no-resampling G4 surface is only a design pattern and historical comparator.
- Focused schema/selection tests in
  `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`.
- Tuning JSON/CSV artifacts under `docs/plans`:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.json`,
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.csv`, and
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-selected-blocked-2026-06-16.csv`.
- Per-run manifest fields in the JSON result or sibling manifest: git commit,
  command, route ID, resampling family/policy, transport settings, CPU/GPU
  context, trusted GPU proof or CPU-only declaration, seeds, particle counts,
  horizon, environment, output paths, and wall time.
- Phase 5 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md`.

## Required Checks, Tests, Reviews

- Pre-run evidence contract restated in ledger.
- `git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h or particle or blocked or uncertainty"`
- Trusted GPU Stage 0 prefix ladder, escalated:
  `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --horizons 4,8 --particles 5,10,20 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-selected-blocked-2026-06-16.csv`
- Post-run JSON/CSV validation and `git diff --check`.
- Claude read-only review of result before Phase 6.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What particle counts are adequate for the OT-resampled scalar-SV route under trusted GPU execution? |
| Baseline/comparator | Phase 4 local diagnostics and within-P8h Stage 0 adjacent-rung comparisons for the exact OT-resampled route. P8g no-resampling G4 is historical context only, not an operative comparator or evidence source. |
| Primary criterion | Select the smallest Stage 0 prefix count or emit explicit blocker using the predeclared deterministic rule below. |
| Veto diagnostics | Nonfinite values; transport residual failure; runtime blowup; unstable adjacent rungs; missing seed uncertainty; missing route/manifest fields; stale P8g no-resampling schema reuse; post-hoc threshold changes. |
| Explanatory diagnostics | ESS, MC SE, runtime, per-seed values. |
| Not concluded | Full-horizon particle-count adequacy, gradient correctness, GPU scaling, HMC readiness, generic high-dimensional readiness, final ranking. |

## Deterministic Stage 0 Selection Rule

Stage 0 evaluates horizons `4,8`, particles `5,10,20`, and seeds
`81120,81121,81122,81123,81124` on trusted GPU. A particle count is selected
only if all of these predeclared conditions hold:

- all per-seed values, ESS summaries, transport diagnostics, and covariance
  diagnostics are finite;
- every evaluated run records route
  `ot_sinkhorn_barycentric_covariance_carry`, route variant
  `p8h_sv_scalar_graph_ot_resampled_alg1`, schema
  `filter_bench.p8h_particle_tuning.v1`, and trusted GPU tensor evidence;
- every first-resampling canonical transport has shape `[N, N]`,
  `target_by_source_row_stochastic`, and row-sum residual at or below its
  recorded row-sum tolerance;
- per-rung runtime is at most `1800` seconds;
- each rung has exactly five seeds and reports sample standard deviation and
  MC standard error of log likelihood;
- MC standard error is at most
  `max(2.0, 0.0025 * abs(mean_log_likelihood))`;
- for the candidate count and its next higher evaluated count at the same
  horizon, adjacent mean log-likelihood delta is at most
  `2 * sqrt(mc_se_candidate^2 + mc_se_next^2) + 1.0`;
- the candidate passes all conditions at both Stage 0 horizons; a terminal
  count with no higher adjacent rung cannot be selected in Stage 0.

If no count passes this exact rule, Phase 5 writes a blocker result. ESS is
reported as explanatory/veto context only if finite ESS is unavailable; ESS is
not by itself a pass criterion for P8h Stage 0.

## Forbidden Claims And Actions

- ESS is diagnostic/veto context, not sole promotion criterion unless
  predeclared.
- Do not change thresholds after seeing results.
- Do not reuse the P8g no-resampling G4 schema, result, or selected count as
  P8h evidence.
- Do not treat Stage 0 prefix tuning as full-horizon adequacy.
- Do not treat Stage 0 trusted GPU runtime as GPU-scaling evidence beyond the
  tested prefix ladder.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 only after a particle-count decision or explicit blocker is
reviewed. Only an explicit reviewed passing value/filtering decision for the
exact route/count may eventually feed Phase 7/8 and HMC transit. An explicit
blocker or diagnostic-only count may feed only Phase 6 diagnostic/repair work,
closeout, or a refreshed plan; it must not pass transitively into Phase 8.

## Stop Conditions

- No particle count passes and the next action requires human direction.
- The P8h-specific tuning runner surface or focused tests are absent or fail;
  implement or repair them before launching the trusted GPU Stage 0 ladder.
