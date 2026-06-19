# P8g-G2 Subplan: Vectorized GPU Algorithm 1 Core

Date: 2026-06-15

Status: `READY_FOR_G2_VECTORIZE_ALG1_CORE`

## Phase Objective

Implement a batched TensorFlow GPU route for Algorithm 1 LEDH sufficient for
real tuning and fixed-randomness gradient work.

## Entry Conditions

- G0 GPU manifest passed and is cited.
- G1 profile identified concrete vectorization targets.
- G1 result recorded the `30` minute projected full-horizon budget and
  concluded that the current GPU route is a vectorization target, not a serious
  implementation pass:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md`.
- Existing CPU Algorithm 1 path remains available as reference.

## Required Artifacts

- Code changes in the Algorithm 1/P8d runner lane.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md`
- CPU/GPU parity table.
- Runtime/profile table showing batched GPU kernels.
- Route identifiers for CPU reference, GPU vectorized value, and GPU
  vectorized fixed-randomness gradient.

## Required Checks/Tests/Reviews

- Focused unit tests for vectorized shape/finite behavior.
- CPU/GPU parity on LGSSM and two SV-style short horizons.
- Profiler evidence that the serious GPU route removes the Python particle
  loop.
- `python -m py_compile ...`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q`
- GPU smoke checks under trusted context.
- `git diff --check`
- Claude read-only implementation/result review.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- G0 result artifact and G1 profile result are cited before any GPU claim;
- TensorFlow/TensorFlow Probability are the implementation backend for
  differentiable or gradient-bearing BayesFilter-owned code;
- NumPy is allowed only for reference checks, serialization, or reporting.

Exact planned commands:

- compile check, non-GPU:
  `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- CPU-focused regression test, deliberate CPU:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q`
- vectorized route focused tests, to be added or confirmed in G2:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8g or vectorized or ledh"`
- trusted GPU parity/profile smoke, to be implemented or confirmed in G2 before
  use:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-vectorized-smoke --rows lgssm,actual_sv,generalized_sv --horizon 50 --particles 32 --seeds 81120,81121,81122,81123,81124 --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --profile-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-profile-2026-06-15.json --parity-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-parity-2026-06-15.json`

If the `--p8g-vectorized-smoke` entry point or focused tests do not exist, G2
must create them before any parity or speed claim, then rerun compile, CPU
focused tests, GPU smoke, and `git diff --check`.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md`;
- parity JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-parity-2026-06-15.json`;
- profile JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-profile-2026-06-15.json`.

Approval boundary:

- trusted GPU parity/profile smoke requires explicit approval;
- no tuning, callback closure, or HMC diagnostic run is authorized in G2.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does P8g have a real batched GPU Algorithm 1 route rather than a CPU loop wrapped in TensorFlow? |
| Baseline/comparator | Current CPU reference Algorithm 1 implementation. |
| Primary criterion | Short-horizon CPU/GPU parity passes and profile shows batched GPU kernels with at least 5x speedup or reviewed feasible exception. |
| Veto diagnostics | Python particle loop remains in serious path; GPU route falls back to CPU; parity fails; non-finite particles, determinants, weights, or covariances. |
| Explanatory diagnostics | Speedup, memory use, kernel placement, parity deltas. |
| Not concluded | Full-horizon accuracy, tuned particle counts, gradient correctness, or HMC readiness. |

## Forbidden Claims/Actions

- Do not claim production GPU implementation from wrapper-only `tf.function`.
- Do not change model definitions or likelihood formulas to make parity pass.
- Do not use NumPy in differentiable algorithmic implementation paths.

## Next-Phase Handoff Conditions

Advance to G3 only if the vectorized route passes parity, finite, device, and
profile gates and records route identifiers.

## Stop Conditions

- Batched route cannot be made finite.
- CPU/GPU parity fails beyond tolerance.
- Speedup/feasibility gate fails without reviewed exception.
