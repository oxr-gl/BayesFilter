# P8h Phase 7 Subplan: GPU Performance And Scaling

Date: 2026-06-15

Status: `READY_FOR_REVIEW_AFTER_PHASE6`

## Phase Objective

Profile trusted GPU performance for the exact selected P8h route/count and one
adjacent comparison rung, using short-prefix diagnostics only, and identify
whether performance is feasible for a small HMC diagnostic.

## Entry Conditions

- Phase 5 has a reviewed Stage 0 passing value/filtering decision for
  `ot_sinkhorn_barycentric_covariance_carry`, `N=5`.
- Phase 6 has a reviewed OT-gradient pass for the same route/count.
- Before execution, verify the Phase 5 and Phase 6 result files have reviewed
  pass statuses and record their paths in the Phase 7 result.

## Required Artifacts

- GPU profile JSON/CSV artifacts:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.json` and
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.csv`.
- Per-run manifest fields in the JSON result or sibling manifest: git commit,
  command, route ID, resampling family/policy, transport settings, CPU/GPU
  context, trusted GPU proof, seeds, particle counts, horizon, environment,
  output paths, and wall time.
- Phase 7 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-result-2026-06-16.md`.

## Required Checks, Tests, Reviews

- `git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
- Trusted GPU profile command:
  `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 4,8 --particles 5,10 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-profile-manifest-phase P8H_PHASE7_GPU_PERFORMANCE_SCALING --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-subplan-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-selected-blocked-2026-06-16.csv`
- Post-run JSON/CSV validation for trusted GPU evidence, route/count, runtime,
  route variant `p8h_sv_scalar_graph_ot_resampled_alg1`, coordinate
  `canonical_unconstrained`, numerical finiteness, transport diagnostics, and
  memory availability if reported.
- Required pre-execution grep checks:
  `rg -n "PASS|N=5|ot_sinkhorn_barycentric_covariance_carry" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md`
- Claude read-only review of the result before Phase 8 because this phase
  affects HMC transit.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the selected OT-resampled route/count practically executable on trusted GPU for a small HMC diagnostic? |
| Baseline/comparator | Phase 5/6 selected route/count and the adjacent `N=10` P8h comparison rung. P8g no-resampling timing is historical context only. |
| Primary criterion | Profile artifacts show finite trusted-GPU execution for `N=5` at horizons `4,8`, no CPU fallback, and no runtime/OOM blocker for a small HMC smoke. |
| Veto diagnostics | Missing reviewed Phase 5 or Phase 6 pass for the profiled route/count; untrusted GPU evidence; missing route/manifest fields; OOM without blocker; CPU fallback treated as GPU success; route/count/configuration mismatch; nonfinite value, covariance, or transport diagnostics. |
| Explanatory diagnostics | Compilation time, step time, memory, particle-count scaling. |
| Not concluded | Production readiness, full GPU scaling law, full-horizon performance, HMC readiness, or high-dimensional readiness beyond tested scope. |

## Forbidden Claims And Actions

- Do not extrapolate beyond measured particle counts/horizons.
- Do not treat Phase 7 runtime as value adequacy or gradient correctness.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 8 only if performance is feasible for a small HMC diagnostic
and the same route/count has a reviewed passing Phase 5 value/filtering
decision and reviewed Phase 6 OT-gradient pass.

## Stop Conditions

- GPU route is too slow or memory-bound for even the smallest HMC smoke.
- GPU artifact lacks trusted GPU evidence or uses the wrong route/count.
- GPU artifact has nonfinite values, covariance diagnostics, or transport
  diagnostics.
- Reviewed Phase 5/6 result statuses or exact route/count/configuration cannot
  be verified before execution.
