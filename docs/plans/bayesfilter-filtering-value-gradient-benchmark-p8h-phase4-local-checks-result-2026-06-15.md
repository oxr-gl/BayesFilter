# P8h Phase 4 Result: Local Checks And Integration Diagnostics

Date: 2026-06-16

Status: `PASS_REVIEWED`

## Phase Objective

Run focused local diagnostics for the OT-resampled Algorithm 1 route before
particle-count tuning.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the new P8h route locally coherent before tuning? |
| Baseline/comparator | Phase 3 implementation result and smoke artifacts; P8g no-resampling diagnostics remain quarantined historical comparators only. |
| Primary criterion | All declared local tests pass and CPU/GPU diagnostic artifacts are finite with exact P8h route, covariance carry, canonical transport, PF-PF correction, and P8g quarantine fields. |
| Veto diagnostics | Nonfinite values; missing covariance/OT diagnostics; missing P8h route/schema fields; reused P8g metadata; missing canonical transport shape/residual; trusted GPU artifact lacks GPU device evidence. |
| Explanatory diagnostics | ESS, transport residuals, runtime, covariance floors. |
| Not concluded | Particle-count adequacy, value adequacy, gradient correctness, GPU scaling, HMC readiness, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, production readiness, or filter ranking. |

## Skeptical Audit

- Wrong-baseline check: P8g remains historical no-resampling evidence only and
  is not promoted by this gate.
- Proxy-metric check: finite local smokes and focused tests validate route
  plumbing, schema, and local coherence only; they do not validate tuning,
  gradients, GPU scaling, or HMC.
- Stop-condition check: no long tuning or HMC was run in Phase 4.
- Artifact-fit check: the CPU/GPU JSON artifacts directly exercise the exact
  pinned P8h Sinkhorn route and preserve route/covariance/PF-PF/transport
  diagnostics needed for Phase 5 entry.

## Commands Run

```bash
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*
PYTHONDONTWRITEBYTECODE=1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8h-ledh-ot-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 4 --particles 5 --seeds 81120,81121 --device cpu --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-scalar-sv-ot-cpu-diagnostic-2026-06-15.json
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8h-ledh-ot-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 4 --particles 5 --seeds 81120,81121 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-scalar-sv-ot-gpu-diagnostic-2026-06-15.json
```

The GPU command was run with trusted/escalated permissions.

## Check Results

- `git diff --check`: passed.
- `py_compile`: passed.
- Focused CPU pytest: `39 passed, 2 warnings`.
- CPU diagnostic smoke wrote:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-scalar-sv-ot-cpu-diagnostic-2026-06-15.json`.
- Trusted GPU diagnostic smoke wrote:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-scalar-sv-ot-gpu-diagnostic-2026-06-15.json`.
- Programmatic artifact validation passed for both CPU and GPU JSON files.

## Diagnostic Artifact Summary

| Artifact | Device evidence | Route | Runs | Canonical transport | Finite gate |
|---|---|---|---:|---|---|
| CPU diagnostic JSON | `/device:CPU:0` tensors; `CUDA_VISIBLE_DEVICES=-1` | `ot_sinkhorn_barycentric_covariance_carry` | 2 | `[5, 5]`, `target_by_source_row_stochastic` | Pass |
| GPU diagnostic JSON | `/device:GPU:0` tensors and TensorFlow GPU list | `ot_sinkhorn_barycentric_covariance_carry` | 2 | `[5, 5]`, `target_by_source_row_stochastic` | Pass |

Required route and boundary markers were present:

- `filter_bench.p8h_ot_resampled_alg1_smoke.v1`;
- `p8h_sv_scalar_graph_ot_resampled_alg1`;
- `same_transport_barycentric_covariance_carry`;
- `algorithm1_pfpf_corrected_log_weight_pre_resampling`;
- `p8h_schema_reuses_p8g_metadata: false`;
- P8g no-resampling evidence status:
  `quarantined_historical_diagnostic_only`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 4 local diagnostics, pending review | Passed locally. | No Phase 4 veto fired. | Phase 4 is a very small prefix smoke and does not establish particle-count adequacy. | Review this result and the refreshed Phase 5 subplan, then launch P8h-specific particle/value tuning if review agrees. | No value adequacy, gradient correctness, GPU scaling, HMC readiness, production readiness, or filter ranking. |

## Handoff

Proceed to Phase 5 only after review accepts this result and the refreshed
Phase 5 subplan. Phase 5 must use a P8h-specific tuning surface for the exact
route `ot_sinkhorn_barycentric_covariance_carry`; the P8g no-resampling G4
tuning harness may be used only as a design pattern and historical comparator.
