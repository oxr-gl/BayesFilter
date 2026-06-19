# P8h Phase 4 Subplan: Local Checks And Integration Diagnostics

Date: 2026-06-15

Status: `READY_FOR_EXECUTION`

## Phase Objective

Run focused local unit/integration diagnostics for shape, finite values,
covariance PSD/symmetry/floor, OT residuals, graph-vs-reference where
applicable, and no-regression checks.

## Entry Conditions

- Phase 3 implementation passed local checks and read-only review.

## Required Artifacts

- Diagnostic JSON/CSV artifacts under `docs/plans`, including CPU/GPU P8h
  route-smoke summaries and focused diagnostic extracts.
- Phase 4 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-local-checks-result-2026-06-15.md`.

## Required Checks, Tests, Reviews

- `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- CPU diagnostic smoke:
  `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8h-ledh-ot-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 4 --particles 5 --seeds 81120,81121 --device cpu --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-scalar-sv-ot-cpu-diagnostic-2026-06-15.json`
- Trusted GPU diagnostic smoke after CPU diagnostic passes:
  `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8h-ledh-ot-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 4 --particles 5 --seeds 81120,81121 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-scalar-sv-ot-gpu-diagnostic-2026-06-15.json`
- Required diagnostic fields to verify in both artifacts:
  `filter_bench.p8h_ot_resampled_alg1_smoke.v1`,
  `p8h_sv_scalar_graph_ot_resampled_alg1`,
  `ot_sinkhorn_barycentric_covariance_carry`,
  `target_by_source_row_stochastic`,
  `same_transport_barycentric_covariance_carry`,
  `algorithm1_pfpf_corrected_log_weight_pre_resampling`,
  `p8h_schema_reuses_p8g_metadata: false`,
  finite values, finite covariance carry, finite transport, canonical transport
  shape `[5, 5]`, and no silent CPU fallback for trusted GPU.
- Claude read-only review if diagnostics reveal material interpretation issues.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the new route locally coherent before tuning? |
| Baseline/comparator | Phase 3 code/tests, Phase 3 CPU/GPU smoke artifacts, and P8g no-resampling diagnostics as quarantined historical comparators only. |
| Primary criterion | All declared local tests pass and CPU/GPU diagnostic artifacts are finite with exact P8h route, covariance-carry, canonical-transport, PF-PF correction, and P8g quarantine fields. |
| Veto diagnostics | Nonfinite values; missing covariance/OT diagnostics; missing P8h route/schema fields; P8g metadata reused as P8h evidence; canonical transport shape/residual missing; trusted GPU artifact lacks GPU device evidence. |
| Explanatory diagnostics | ESS, transport residuals, runtime, covariance floors. |
| Not concluded | Particle-count adequacy, value adequacy, gradient correctness, GPU scaling, HMC readiness, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, production readiness, or filter ranking. |

## Forbidden Claims And Actions

- Do not promote smoke diagnostics to tuning or correctness evidence.
- Do not reuse P8g no-resampling/fixed-randomness/G4 artifacts as P8h evidence.
- Do not run long tuning or HMC in Phase 4.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only after local diagnostics pass, result is written, and
the Phase 5 value/filtering tuning subplan is refreshed against the exact P8h
route/counts that survived Phase 4.

## Stop Conditions

- Local diagnostics expose an implementation blocker requiring Phase 3 repair.
