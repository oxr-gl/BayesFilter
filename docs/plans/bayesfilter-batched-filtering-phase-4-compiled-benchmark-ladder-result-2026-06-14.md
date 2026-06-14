# Phase 4 Result: Compiled Benchmark Ladder

Date: 2026-06-14

## Status

`PASSED_WITH_CAPACITY_AND_FEASIBILITY_LIMITS`

## Objective

Run a bounded JIT-only CPU/GPU benchmark ladder for experimental batched
Kalman and SVD-UKF value+score at `T=200`, `state_dim=10`, `obs_dim=10`,
`parameter_dim=2`, and `B in {20, 256, 4096}`.  Preserve scalar-loop
comparator evidence where feasible and avoid eager GPU timing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | For realistic filtering dimensions, what is the compiled CPU/GPU behavior of experimental batched Kalman and SVD-UKF value+score relative to scalar-loop comparators where feasible? |
| Baseline/comparator | Scalar-loop production authority paths over the same deterministic fixture rows, batched compiled CPU, batched compiled GPU, and prior parity tests. |
| Primary criterion | Harness tests pass; all GPU performance commands are JIT/XLA compiled in trusted context; JSON artifacts record compile time, warm timing, finite outputs, shapes, and device placement; scalar-loop timing or infeasibility artifacts are recorded. |
| Veto diagnostics | Eager GPU benchmark, wrong device placement, nonfinite output, missing artifact without capacity/infeasibility record, Phase 1-3 regression, public export/default edit, unsupported broad speedup/default claim. |
| Explanatory diagnostics | Warm-call median, compile/first-call time, per-filter median, capacity timeouts, scalar comparator infeasibility. |
| Not concluded | No production default readiness, no downstream HMC/NeuTra throughput claim, no sampler convergence/posterior quality claim, no CUT4 readiness, no broad GPU superiority beyond this fixture and these batch sizes. |

## Implementation Summary

Updated experimental benchmark harnesses only:

- `docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py`
- `docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py`
- `tests/test_experimental_batched_benchmark_harness.py`

No public export/default files were edited.

Kalman harness changes:

- added `--mode compiled-timing`;
- added JIT-compiled batched timing;
- added scalar-loop comparator using one reused JIT-compiled scalar QR score
  row call;
- recorded scalar-loop mode as a benchmark comparator, not an HMC-jittable
  production implementation.

SVD harness changes:

- added `--mode scalar-compiled-loop`;
- preserved scalar comparator infeasibility evidence when TensorFlow could not
  trace the scalar `TFStructuralStateSpace` object into an XLA-compiled row
  wrapper.

## Checks Run

### Focused Harness Gate

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_benchmark_harness.py
```

Result:

- `5 passed`

### Full Experimental Gate

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_benchmark_harness.py tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py
```

Result:

- `40 passed`

### Public API Guard

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_v1_public_api.py -k public_api
```

Result:

- `5 passed`

### Post-Benchmark Combined Gate

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_benchmark_harness.py tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py tests/test_v1_public_api.py -k "public_api or experimental_batched"
```

Result:

- `45 passed`

## Benchmark Results

All GPU timing rows below are JIT/XLA-compiled and were run in trusted context
on `CUDA_VISIBLE_DEVICES=1`, TensorFlow logical `/GPU:0`, NVIDIA RTX 4080
SUPER.  Warm medians exclude compile/first-call time.

### Kalman Value+Score

| Path | Device | B | Warm median seconds | Per-filter warm median seconds | Compile/first-call seconds | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Batched | CPU | 20 | 0.2358 | 0.01179 | 1.983 | finite |
| Scalar-loop | CPU | 20 | 0.9561 | 0.04781 | 3.545 | finite |
| Batched | GPU | 20 | 0.04977 | 0.002489 | 2.398 | finite |
| Scalar-loop | GPU | 20 | 3.0688 | 0.15344 | 6.425 | finite |
| Batched | CPU | 256 | 5.8813 | 0.02297 | 7.464 | finite |
| Scalar-loop | CPU | 256 | 12.9452 | 0.05057 | 16.210 | finite, reduced repeats |
| Batched | GPU | 256 | 0.1388 | 0.000542 | 2.417 | finite |
| Batched | CPU | 4096 | N/A | N/A | N/A | 300s timeout |
| Batched | GPU | 4096 | 1.6320 | 0.000398 | 4.386 | finite |

Kalman scalar-loop GPU `B=256` and `B=4096` were not launched after scalar-loop
GPU `B=20` took about 3.07 seconds per warm batch; explicit capacity artifacts
were written.

### SVD-UKF Value+Score

| Path | Device | B | Warm median seconds | Per-filter warm median seconds | Compile/first-call seconds | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Batched | CPU | 20 | 2.4277 | 0.12138 | 5.716 | finite |
| Batched | GPU | 20 | 0.3735 | 0.01868 | 5.581 | finite |
| Batched | CPU | 256 | 35.1051 | 0.13713 | 37.803 | finite, reduced repeats |
| Batched | GPU | 256 | 0.7836 | 0.003061 | 6.021 | finite |
| Batched | CPU | 4096 | N/A | N/A | N/A | 300s timeout |
| Batched | GPU | 4096 | 7.7604 | 0.001895 | 13.960 | finite, one repeat |

SVD-UKF scalar-loop compiled comparator was infeasible at `B=20` before timing:
TensorFlow could not generate a `TraceType` for the scalar
`TFStructuralStateSpace` object captured by the compiled scalar authority
wrapper.  CPU/GPU scalar-loop infeasibility artifacts were written for all
planned SVD-UKF scalar comparator slots.

## Artifact Index

Timing artifacts:

- `docs/benchmarks/experimental-batched-kalman-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`

Capacity or feasibility artifacts:

- `docs/benchmarks/experimental-batched-kalman-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 4 passes with limits | Required harness tests and benchmark artifacts exist; GPU timings are JIT/XLA compiled and device-placed on GPU | No eager GPU benchmark, wrong device placement, nonfinite output, public export/default edit, or Phase 1-3 regression observed | Timings are single-shape descriptive diagnostics with reduced repeats for large `B`; scalar SVD comparator is XLA-infeasible at current wrapper boundary | Move to Phase 5 downstream HMC/NeuTra harness subplan | Production default readiness, sampler convergence, posterior quality, broad GPU superiority |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for completed batched CPU/GPU runs; capacity/infeasibility artifacts written for bounded non-completions |
| Statistically supported ranking | Not established; no uncertainty analysis or multi-run replication was performed |
| Descriptive-only differences | Batched GPU is descriptively much faster than scalar-loop or CPU in this fixture, especially at larger `B` |
| Default-readiness | Not established |
| Next evidence needed | Downstream value+score harness integration and later sampler-validity gates |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `207419e49d2dbbc5c6aa3bca2f2ce450b6e2ffde` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| TensorFlow | `2.20.0` |
| CPU/GPU status | CPU runs used `CUDA_VISIBLE_DEVICES=-1`; GPU runs used trusted `CUDA_VISIBLE_DEVICES=1` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, logical `/GPU:0`, about 30 GB available at run start |
| Data version | Synthetic deterministic benchmark fixtures |
| Random seeds | N/A |
| Plan file | `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-subplan-2026-06-14.md` |
| Result file | `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-result-2026-06-14.md` |
| Claude reviews | `docs/plans/bayesfilter-batched-filtering-phase-4-claude-review-round-01-2026-06-14.md`, `docs/plans/bayesfilter-batched-filtering-phase-4-claude-review-round-02-2026-06-14.md` |

## Handoff To Phase 5

Phase 5 may proceed after its subplan is reviewed.  It must test the batched
value+score path inside an actual downstream target/harness and must first
audit inherited HMC/NeuTra gate status.  Phase 5 must not claim posterior
validity, sampler convergence, or production default readiness unless a
separate sampler-validity plan supplies those criteria.

