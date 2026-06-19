# P8h Phase 3 Result: Scalar-SV GPU OT Implementation

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_REVIEWED`: implemented a TensorFlow/TFP P8h OT-resampled Algorithm 1 path and P8h scalar-SV smoke adapter; repaired the first review's fail-closed transport-validation gap; focused read-only re-review converged. |
| Primary criterion | Pass locally: route exists, focused tests pass, CPU smoke is finite, trusted GPU smoke is finite and places result tensors on GPU, route emits canonical transport, covariance carry, PF-PF correction, ESS, finite, row-sum tolerance, and P8g quarantine diagnostics. |
| Veto diagnostics | First review found that canonical transport shape/row-sum validity was diagnosed but not enforced before state mutation. The implementation now fails closed on rank, `[N, N]` shape, finite transport, and row-sum residual before particle/covariance carry. NumPy was not introduced into the algorithmic path; P8g no-resampling artifacts are quarantined; no long tuning/HMC was run. |
| Main uncertainty | This is still implementation smoke only. Phase 4 must run integration diagnostics; Phase 5/6 must separately test value/filtering and gradient behavior. |
| Next justified action | Launch Phase 4 local integration diagnostics under the refreshed subplan. |
| Not concluded | No value adequacy, particle-count tuning, gradient correctness, GPU scaling, HMC readiness, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, production readiness, or filter ranking. |

## Implemented Artifacts

- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
  - Added P8h route identifiers:
    `ot_sinkhorn_barycentric_covariance_carry` and
    `ot_annealed_transport_covariance_carry`.
  - Added canonical transport helpers using `A[target, source]`.
  - Added covariance carry through the same canonical transport matrix.
  - Added OT resampling branch after PF-PF corrected weights and before the next
    time step.
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
  - Added P8h scalar-SV prefix smoke schema:
    `filter_bench.p8h_ot_resampled_alg1_smoke.v1`.
  - Added `--profile-p8h-ledh-ot-prefix` and `--p8h-resampling-route`.
  - Preserved P8g schema/route quarantine.
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`
  - Added canonical transport, covariance carry, route metadata, and triggered
    Algorithm 1 OT-resampling tests.
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
  - Added P8h smoke schema and P8g quarantine test.
- CPU smoke:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-ot-cpu-smoke-2026-06-15.json`
- Trusted GPU smoke:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-ot-gpu-smoke-2026-06-15.json`

## Checks Run

| Check | Outcome | Notes |
|---|---|---|
| `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*` | Pass | No whitespace errors. |
| `PYTHONDONTWRITEBYTECODE=1 python -m py_compile ...` for Phase 3 touched modules/tests | Pass | Syntax/import compilation passed. |
| `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_pfpf_alg1_ukf_tf.py -k "sinkhorn_canonical or apply_ot_resampling or triggers_p8h_sinkhorn or route_identifier"` | Pass | `5 passed, 15 deselected`. |
| `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_ot_resampled_prefix"` | Pass | `1 passed, 17 deselected`. |
| `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py` | Pass | `38 passed, 2 warnings` in 96.99s. |
| `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --help` | Pass | CLI exposes `--profile-p8h-ledh-ot-prefix` and `--p8h-resampling-route`. TensorFlow emitted non-escalated CUDA init noise during import; not GPU evidence. |
| CPU P8h smoke command | Pass | Wrote finite CPU artifact with `CUDA_VISIBLE_DEVICES=-1`. |
| Trusted `nvidia-smi` | Pass | NVIDIA GeForce RTX 4080 SUPER visible; CUDA 13.1; 16GB class GPU. |
| Trusted GPU P8h smoke command | Pass | Wrote finite GPU artifact; result tensors and marker on `/device:GPU:0`. |
| Focused repair regression | Pass | Added malformed-canonical-transport test; `6 passed, 15 deselected`. |

## Smoke Commands

CPU smoke:

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8h-ledh-ot-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 2 --particles 3 --seeds 81120 --device cpu --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-ot-cpu-smoke-2026-06-15.json
```

Trusted GPU smoke:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8h-ledh-ot-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 2 --particles 3 --seeds 81120 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-ot-gpu-smoke-2026-06-15.json
```

## Artifact Highlights

- CPU artifact status: `executed_p8h_ot_resampled_alg1_smoke`.
- GPU artifact status: `executed_p8h_ot_resampled_alg1_smoke`.
- GPU artifact device evidence:
  - marker device: `/job:localhost/replica:0/task:0/device:GPU:0`;
  - log likelihood device: `/job:localhost/replica:0/task:0/device:GPU:0`;
  - ESS device: `/job:localhost/replica:0/task:0/device:GPU:0`;
  - `no_silent_cpu_fallback_claim: true`.
- Route diagnostics:
  - `route_variant: p8h_sv_scalar_graph_ot_resampled_alg1`;
  - `resampling_route: ot_sinkhorn_barycentric_covariance_carry`;
  - `covariance_carry_route: same_transport_barycentric_covariance_carry`;
  - `pfpf_correction_route: algorithm1_pfpf_corrected_log_weight_pre_resampling`;
  - `canonical_transport_matrix_convention: target_by_source_row_stochastic`;
  - `canonical_transport_row_sum_tolerance: 0.005`;
  - `relaxed_resampling_not_categorical: true`.
- P8g quarantine:
  - `p8h_schema_reuses_p8g_metadata: false`;
  - P8g fixed-randomness and particle-tuning artifacts remain historical
    no-resampling diagnostics only.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c`; dirty worktree. |
| Environment | `/home/chakwong/BayesFilter`, TensorFlow/TensorFlow Probability. |
| CPU/GPU status | CPU smoke used `CUDA_VISIBLE_DEVICES=-1`; GPU smoke ran trusted/escalated and used `/device:GPU:0`. |
| Data version | Existing P8d synthetic SV row from repository generator/import path. |
| Random seeds | Smoke seed `81120`; tests also exercise deterministic fixtures. |
| Wall time | Focused CPU pytest: 96.99s; CPU smoke artifact wall time 1.13s; GPU smoke artifact wall time 8.08s. |
| Output paths | CPU/GPU smoke JSONs listed above. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-gpu-ot-implementation-subplan-2026-06-15.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: the route can be locally finite while still
having poor value/filtering behavior, weak particle-count behavior, or unusable
gradients at realistic scale. The Phase 3 artifacts deliberately do not answer
those questions. They establish only the implementation route, canonical
transport/covariance carry wiring, P8h schema separation, and CPU/GPU smoke
execution.

## Handoff

Phase 4 may proceed. Read-only review accepted this result and the Phase 4
subplan after the fail-closed transport-validation repair. Phase 4 should run
local integration diagnostics over the exact P8h route and must not promote
smoke success into value adequacy, gradient correctness, or HMC readiness.
