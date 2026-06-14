# Batched SVD-UKF Value+Score Result

Date: 2026-06-14

Owning root: `/home/ubuntu/python/BayesFilter`

## Status

`EXPERIMENTAL_B20_SCALAR_PARITY_PASS_GPU_XLA_WHILE_LOOP_BENCHMARK_RECORDED`

## Scope

This pass only tests the additive experimental batched SVD sigma-point module:

- `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py`
- `docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py`

No production nonlinear filter, package export, HMC runtime, or scalar SVD-UKF
implementation was modified.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Does the experimental batched SVD-UKF value+score path match the scalar SVD-UKF analytic score API at `B=20` for a realistic dense fixture? |
| Comparator | Existing scalar `tf_svd_ukf_score` row by row. |
| Primary criterion | All `B=20` rows pass value and score tolerances. |
| Veto diagnostics | Nonfinite batched outputs, wrong device placement for smoke probes, any scalar parity row failure, or treating eager GPU placement timing as a GPU benchmark. |
| Explanatory only | CPU warm timing, eager GPU placement-smoke timings, first-call time, per-filter timing, and value sums. |
| Not concluded | No production readiness, no broad GPU policy, no HMC/NeuTra end-to-end speedup, no CUT4 or cubature parity claim from this run. |

## Fixture

- Backend: `tf_svd_ukf`
- Shape: `B=20`, `T=200`, `state_dim=10`, `obs_dim=10`, `parameter_dim=2`
- Structural law: affine all-stochastic state-space fixture
- Augmented SVD-UKF dimension: `20`
- Sigma points per time step: `41`
- dtype: `float64`

The fixture is affine so scalar SVD-UKF value+score is a direct authority path
for every parameter row.

## Scalar Parity

Artifact:

- `docs/benchmarks/experimental-batched-svd-ukf-parity-b20-t200-n10-m10-2026-06-14.json`

Command shape:

```bash
CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py \
  --mode parity --backend tf_svd_ukf --batch-size 20 --time-steps 200 \
  --state-dim 10 --obs-dim 10 --parameter-dim 2 --rows all \
  --device-scope cpu --device /CPU:0 --expect-device-kind cpu \
  --output docs/benchmarks/experimental-batched-svd-ukf-parity-b20-t200-n10-m10-2026-06-14.json
```

Result:

| Check | Result |
| --- | ---: |
| Rows checked | `0..19` |
| Passed | `true` |
| Max abs value error | `1.7053e-13` |
| Max abs score error | `4.5475e-13` |
| Max rel value error | `1.2206e-15` |
| Max rel score error | `8.3672e-16` |

## CPU Timing And Eager GPU Smoke Diagnostics

Artifacts:

- `docs/benchmarks/experimental-batched-svd-ukf-value-score-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-value-score-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-value-score-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-value-score-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-smoke-b2-t3-n2-m2-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-parity-b20-t200-n10-m10-whileloop-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b20-t200-n10-m10-whileloop-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b256-t200-n10-m10-whileloop-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b4096-t200-n10-m10-whileloop-2026-06-14.json`

Trusted GPU visibility:

- `nvidia-smi` saw two `NVIDIA GeForce RTX 4080 SUPER` GPUs.
- Eager GPU smoke probes used `CUDA_VISIBLE_DEVICES=1`, mapped to TensorFlow
  `/GPU:0`.

Observed timings:

| Batch | Device | First call | Warm median | Warm mean | Per-filter warm median | Placement |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| `20` | CPU | `9.3612s` | `8.8262s` | `8.8146s` | `0.4413s` | CPU:0 |
| `20` | GPU 1 eager smoke | `13.5373s` | `10.9711s` | `10.9845s` | `0.5486s` | GPU:0 |
| `256` | CPU | `27.1055s` | `26.0375s` | `26.1610s` | `0.1017s` | CPU:0 |
| `256` | GPU 1 eager smoke | `35.5016s` | `32.9630s` | `32.6515s` | `0.1288s` | GPU:0 |

Interpretation:

- The CPU timings are valid eager CPU diagnostics for the current harness.
- The GPU rows are **not valid GPU benchmark comparisons** because the SVD-UKF
  path is not compiled with `tf.function` or XLA/JIT.  They are retained only
  as eager GPU placement/materialization smoke evidence.
- No CPU-vs-GPU performance conclusion should be drawn from the eager GPU rows.
- This does not contradict the Kalman `B=200` GPU win.  The current SVD-UKF
  workload has sequential time steps, small dense eigensystem derivative work,
  and consumer-GPU `float64` overheads, but the decisive next gate is a
  compiled/JIT benchmark.
- A `B=4096` GPU warm-timing probe and a first-call-only GPU probe were both
  attempted.  Both were interrupted after several minutes while still inside
  batched eigensystem work, so no valid `B=4096` artifact is claimed.  CPU
  `B=4096` was not attempted because `B=256` already took about `26s` per warm
  batch.

## Compiled GPU XLA Attempt

The benchmark harness now has a `compiled-timing` mode that wraps the
value+score call in `tf.function(jit_compile=True)` and separates compile/first
call from warm calls.  The experimental batched SVD sigma-point recursion was
also repaired to use `tf.while_loop` instead of a Python `for t in range(T)`
time loop.

Post-repair scalar parity:

| Shape | Rows checked | Passed | Max abs value error | Max abs score error |
| --- | --- | --- | ---: | ---: |
| `B=20`, `T=200`, `n=m=10` | `0..19` | yes | `1.7053e-13` | `4.5475e-13` |

GPU XLA results after the `tf.while_loop` repair:

| Batch | Compile + first call | Warm median | Warm mean | Per-filter warm median | Placement | Repeats |
| ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `2` smoke, `T=3`, `n=m=2` | `6.2516s` | `0.00106s` | `0.00106s` | `0.000530s` | GPU:0 | `2` |
| `20`, `T=200`, `n=m=10` | `5.5382s` | `0.3721s` | `0.3721s` | `0.01860s` | GPU:0 | `5` |
| `256`, `T=200`, `n=m=10` | `6.0503s` | `0.7841s` | `0.7880s` | `0.003063s` | GPU:0 | `3` |
| `4096`, `T=200`, `n=m=10` | `14.1392s` | `7.7642s` | `7.7642s` | `0.001896s` | GPU:0 | `1` |

Interpretation:

- The functions can be JIT compiled for the realistic shape after the loop
  repair.
- The old Python time loop caused full-shape XLA to build a huge unrolled graph;
  replacing it with `tf.while_loop` reduced compile+first-call time from a
  multi-minute blocked attempt to about `5.5s` for `B=20`.
- `B=4096` is feasible on GPU for the repaired compiled path, but the `B=4096`
  row has only one repeat and should be treated as a capacity/timing probe, not
  a stable benchmark.
- XLA still ignores the embedded `tf.debugging.assert_*` checks, so scalar/eager
  parity and validity checks remain required before compiled timing.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Keep additive batched SVD-UKF harness | B=20 all-row scalar parity passed | No nonfinite outputs or placement veto | Only one affine fixture | Add pytest-sized B=3/B=5 parity and larger B timing ladder | No production readiness |
| Treat repaired GPU XLA rows as first valid GPU timing | Compiled timing artifacts recorded | GPU placement verified; finite outputs | Low repeats for `B=4096`; no compiled CPU comparator yet | Add compiled CPU baseline and more repeats | No end-to-end HMC speedup claim |
| Defer CUT4/cubature claims | Not tested in this run | N/A | CUT4 has more points and may differ in scaling | Run separate scalar parity first | No CUT4 readiness |

## Post-Run Red Team

Strongest alternative explanation: the affine fixture is friendlier than a truly
nonlinear model because sigma-point approximation error cancels between scalar
and batched implementations.  That is acceptable for this parity question, but
not sufficient for nonlinear accuracy claims.

Result that would overturn this first slice: a non-affine fixture with analytic
derivatives passes scalar score checks but fails batched row parity, indicating
a batching error in point-dependent derivative propagation.

Weakest evidence: the compiled GPU benchmark currently has no matching compiled
CPU comparator in the repaired harness, and the `B=4096` row has only one
measured repeat.
