# P8g-G2 Result: Vectorized GPU Algorithm 1 Core

Date: 2026-06-15

Status: `BLOCK_P8G_VECTORIZE_ALG1_SPEED_FEASIBILITY_REVIEWED`

## Phase Objective

Implement a batched TensorFlow GPU route for Algorithm 1 LEDH sufficient for
real tuning and fixed-randomness gradient work.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does P8g have a real batched GPU Algorithm 1 route rather than a CPU loop wrapped in TensorFlow? |
| Baseline/comparator | Current CPU reference Algorithm 1 implementation. |
| Primary criterion | Short-horizon CPU/GPU parity passes and profile shows batched GPU kernels with at least 5x speedup or reviewed feasible exception. |
| Veto diagnostics | Python particle loop remains in serious path; GPU route falls back to CPU; parity fails; non-finite particles, determinants, weights, or covariances. |
| Explanatory diagnostics | Speedup, memory use, kernel placement, parity deltas. |
| Not concluded | Full-horizon accuracy, tuned particle counts, gradient correctness, or HMC readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `eae3f22fb8fe4a7740d7dc67066522303aaaf083` |
| Worktree state | Dirty before/during G2; unrelated Zhao-Cui/SGQF work and P8g artifacts preserved. |
| G0 manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| G1 result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md` |
| CPU vectorized smoke JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-smoke-cpu-2026-06-15.json` |
| GPU vectorized smoke JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-smoke-gpu-2026-06-15.json` |
| GPU looped smoke JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-looped-alg1-smoke-gpu-2026-06-15.json` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md` |
| Row/algorithm | `zhao_cui_sv_actual_nongaussian_T1000`, `ledh_pfpf_alg1_ukf_current` |
| Smoke horizon/particles/seeds | prefix horizon `10`, particles `32`, seed `81120` |

## Code Changes

Added an opt-in vectorized particle route:

- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
  - `li_coates_ledh_alg1_time_step_vectorized_particles_tf(...)`;
  - `run_ledh_pfpf_alg1_ukf_tf(..., vectorized_particles=False)`;
  - existing looped/source-reference route remains default.
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
  - `--p8g-vectorized-particles` profile flag;
  - profile JSON records `route_variant` and `vectorized_particles`.
- Tests:
  - `tests/test_ledh_pfpf_alg1_ukf_tf.py` looped-vs-vectorized time-step
    parity;
  - `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
    P8g profile payload contract and vectorized-route parity smoke.

## Commands Run

Local checks and focused tests:

```bash
git diff --check
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "vectorized_particle_time_step or p8g_profile"
```

Trusted GPU and CPU smoke profiles:

```bash
MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 10 --particles 32 --seeds 81120 --device gpu --p8g-vectorized-particles --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-smoke-gpu-2026-06-15.json

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 10 --particles 32 --seeds 81120 --device cpu --p8g-vectorized-particles --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-smoke-cpu-2026-06-15.json

MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 10 --particles 32 --seeds 81120 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-looped-alg1-smoke-gpu-2026-06-15.json
```

## Local Check Results

- `git diff --check`: passed.
- `python -m py_compile ...`: passed.
- Focused pytest for vectorized time-step/profile payload: `2 passed, 26 deselected, 2 warnings`.

## Smoke Results

| Metric | CPU vectorized | GPU looped | GPU vectorized |
|---|---:|---:|---:|
| Status | `executed_p8g_prefix_profile` | `executed_p8g_prefix_profile` | `executed_p8g_prefix_profile` |
| Route variant | `p8g_vectorized_particles` | `current_looped_particles` | `p8g_vectorized_particles` |
| Wall seconds | `5.006954` | `20.262948` | `11.332614` |
| Seconds per seed-time-particle | `0.015646732` | `0.063321712` | `0.035414418` |
| Mean log likelihood | `-7.826827591365667` | `-7.82682759136567` | `-7.82682759136567` |
| GPU vectorized vs GPU looped speedup | N/A | N/A | `1.788021x` |
| GPU vectorized minus GPU looped value | N/A | N/A | `0.0` |
| GPU vectorized minus CPU vectorized value | N/A | N/A | about `-2.66e-15` |
| Result tensor device | `/device:CPU:0` | `/device:GPU:0` | `/device:GPU:0` |

TensorFlow emitted retracing warnings during the vectorized route. The result is
finite and parity-preserving, but the time-loop/eager/retracing overhead remains
dominant.

## Gate Assessment

Decision: `BLOCK_P8G_VECTORIZE_ALG1_SPEED_FEASIBILITY_REVIEWED`.

| Criterion | Status | Evidence |
|---|---|---|
| CPU/GPU parity | Pass | GPU vectorized mean equals GPU looped and matches CPU vectorized to floating precision. |
| Finite values/ESS/covariances | Pass | Smoke profile status is `executed_p8g_prefix_profile`; focused tests pass. |
| Real GPU placement | Pass | GPU looped and vectorized profile tensors record `/device:GPU:0`. |
| Python particle loop removed from opt-in route | Partial pass | Per-particle Algorithm 1 time-step uses `tf.vectorized_map`; default looped reference remains available. |
| G1/G2 speed gate | Fail | GPU vectorized is only about `1.79x` faster than GPU looped on the tiny smoke, below the G1/G2 minimum `5x` target. |
| Full-horizon feasibility projection | Fail | Tiny-smoke speed does not justify the G1 `30` minute projected full-horizon budget. |
| Review gate | Pass | Claude read-only review returned `VERDICT: AGREE` and is recorded in the canonical review ledger. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Block G2 after partial vectorization and review | Failed speed/feasibility gate despite passing parity, finiteness, GPU placement, and review. | No silent fallback and no nonfinite result; speed/feasibility veto fires. | Whether graphing/XLA of the time loop, hoisting `tf.vectorized_map` tracing, or deeper batched linear algebra can reach the recorded 5x/30-minute gate. | Stop for repair planning or human direction before G3; do not run tuning, gradients, or HMC on this route. | No serious GPU implementation, no tuned particle count, no gradient correctness, no HMC readiness, no callback closure, no filter ranking. |

## Blocker Detail

`tf.vectorized_map` removes the explicit Python particle loop from the opt-in
time-step route and preserves values, but it does not yet produce a serious GPU
implementation. Remaining likely bottlenecks:

- Python/eager time loop over observations;
- retracing from `tf.vectorized_map` inside the time loop;
- small per-particle matrix operations launched as many tiny kernels;
- five-seed orchestration outside a graph/kernel.

This is a programming/performance blocker, not a conceptual objection to the
LEDH/DPF plan. The next repair should target graphing/XLA of the time loop and
kernel coalescing before any G3 gradient or G4 tuning work.

## Next-Phase Handoff

G2 does not hand off to G3. The safe next action is either:

1. write a G2 repair subplan/amendment for graph/XLA time-loop vectorization and
   kernel coalescing; or
2. ask for human direction if the recorded `30` minute/5x feasibility gate
   should be changed.

No G3 fixed-randomness gradient, G4 tuning, or G6 HMC command is launched by
this result.
