# Batched Linear Kalman Value+Score Result

Date: 2026-06-14

Owning root: `/home/ubuntu/python/BayesFilter`

Plan:

- `docs/plans/bayesfilter-batched-linear-kalman-value-score-plan-2026-06-14.md`

## Status

`EXPERIMENTAL_FIRST_SLICE_IMPLEMENTED_LOCAL_TESTS_PASS`

## Scope

Implemented an additive experimental first slice only. No existing production
files, package exports, scalar Kalman paths, HMC runtime files, or public result
containers were modified.

New files:

- `bayesfilter/linear/experimental_batched_kalman_tf.py`
- `tests/test_experimental_batched_linear_kalman_tf.py`

## Claude Review Status

The requested Claude review loop did not converge due local Claude worker
failures, not due a substantive review finding.

- Round 1 used the standard stream-json worker. It over-read context after a
  worker `Read` parameter issue, did not emit a verdict, and later surfaced
  wrapper/auth errors after interruption.
- Round 2 used a narrower text-output worker over only the two new files. It
  produced no findings within the bounded polling window and was interrupted;
  the wrapper emitted only `Execution error`.

No Claude verdict is claimed. The implementation below is supported by local
tests only and should receive another read-only review before promotion or
merge.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Engineering question | Supported for a tiny dense, time-invariant, shared-observation fixture. |
| Baseline/comparator | Existing scalar `tf_linear_gaussian_log_likelihood` value and scalar `tf_qr_linear_gaussian_score` analytic score. |
| Primary criterion | Passed on focused local tests. |
| Veto diagnostics | No nonfinite outputs, no row-order drift, no scalar value/score parity failure, no accepted derivative-shape mismatch in the focused tests. |
| Explanatory only | CPU XLA compile/parity and warning count. |
| Not concluded | No GPU speedup, no HMC convergence, no NeuTra readiness, no masked/time-varying/Hessian/nonlinear readiness, no default backend change. |

## Implementation Summary

Added experimental dense batch-native kernels:

- `tf_batched_kalman_filter(...) -> (log_likelihood[B], filtered_means | None, filtered_covariances | None)`
- `tf_batched_kalman_value_and_score(...) -> (log_likelihood[B], score[B, p])`

The leading batch axis indexes independent parameter/model rows. Time remains
sequential, and the observation series is shared across all rows.

The score path propagates first-order sensitivities with shapes:

```text
d_mean:       [B, p, n]
d_covariance: [B, p, n, n]
score:        [B, p]
```

It uses a direct covariance/Joseph update first slice. If wider stress tests
show numerical drift versus QR score, the next repair should be a batched
QR/square-root variant, not relaxed tolerances.

## Tests

Commands run:

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_batched_kalman_pycache CUDA_VISIBLE_DEVICES=-1 \
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile \
bayesfilter/linear/experimental_batched_kalman_tf.py \
tests/test_experimental_batched_linear_kalman_tf.py
```

Result:

- exit code `0`.

Commands run:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q \
tests/test_experimental_batched_linear_kalman_tf.py
```

Initial result:

- `4 failed, 4 passed`.

Failure:

- covariance-derivative update used an invalid repeated `b` Einstein index that
  collided batch and matrix axes.

Repair:

- changed the Joseph derivative update `einsum` equations to use unambiguous
  batch and matrix indices.

First repaired result:

- `8 passed, 6452 warnings in 9.79s`.

Warnings are TensorFlow Probability/GAST deprecations in the local environment;
they are not promotion evidence.

Follow-up timing setup exposed a singleton-batch graph issue:

- `B=1` calls failed with TensorFlow loop shape-invariant drift:
  covariance entered the time loop as shape `(1, 1, 1)` and became
  `(None, 1, 1)` after one iteration.

Repair:

- added explicit `tf.autograph.experimental.set_loop_options` shape invariants
  for value and value+score loop-carried tensors;
- added
  `test_experimental_batched_kalman_value_and_score_supports_singleton_batch`.

Final correctness result after singleton-batch repair:

- `9 passed, 6578 warnings in 10.89s`.

## Timing Diagnostic

### Tiny Fixture

Command shape:

- CPU-only with `CUDA_VISIBLE_DEVICES=-1`;
- TensorFlow `2.20.0`;
- visible GPU list: `[]`;
- experimental value+score kernel only;
- shared tiny fixture with `T=4`, `n=1`, `m=1`, `p=2`;
- 10 warmups, 500 measured warm calls;
- timing is explanatory only.

Results:

| Batch | First call | Warm median | Warm mean | Per-filter warm median |
| --- | ---: | ---: | ---: | ---: |
| `B=1` | `1.1157s` | `0.002852s` | `0.002869s` | `0.002852s` |
| `B=20` | `0.3835s` | `0.003663s` | `0.003671s` | `0.000183s` |

Interpretation:

- one batched `B=20` call was about `1.28x` the wall time of one `B=1` call;
- per filter, `B=20` was about `6.4%` of the `B=1` median time, or roughly
  `15.6x` lower per-filter wall time in this tiny CPU diagnostic;
- this is not a GPU result, not a production benchmark, and not evidence of
  HMC/NeuTra end-to-end speedup.

### Larger CPU Fixture

Command shape:

- CPU-only with `CUDA_VISIBLE_DEVICES=-1`;
- TensorFlow `2.20.0`;
- visible GPU list: `[]`;
- experimental value+score kernel only;
- deterministic synthetic stable LGSSM;
- `T=200`, `state_dim=10`, `obs_dim=10`, `parameter_dim=2`;
- 3 warmups, 30 measured warm calls;
- timing is explanatory only.

Results:

| Batch | First call | Warm median | Warm mean | Per-filter warm median |
| --- | ---: | ---: | ---: | ---: |
| `B=1` | `1.2704s` | `0.06805s` | `0.06840s` | `0.06805s` |
| `B=20` | `0.7557s` | `0.34774s` | `0.34511s` | `0.01739s` |

Finite-output check:

- `B=1`: `value_shape=(1,)`, `score_shape=(1, 2)`,
  `score_abs_max=159.29`;
- `B=20`: `value_shape=(20,)`, `score_shape=(20, 2)`,
  `score_abs_max=163.72`.

Interpretation:

- one batched `B=20` call was about `5.11x` the wall time of one `B=1` call;
- per filter, `B=20` was about `25.5%` of the `B=1` median time, or roughly
  `3.9x` lower per-filter wall time in this larger CPU diagnostic;
- the larger matrix workload reduces the per-filter batching gain relative to
  the tiny fixture, but still amortizes graph/runtime overhead substantially.

## GPU Smoke Diagnostic

Evidence contract:

- Question: can the local TensorFlow environment see GPU devices and execute
  the experimental batched Kalman value+score path on GPU?
- Primary pass criterion: TensorFlow lists at least one GPU and the materialized
  value/score tensors report GPU placement with finite outputs.
- Veto: no visible GPU in trusted context, CUDA initialization failure in the
  direct probe, nonfinite value or score output, or CPU placement for the direct
  value+score tensors.
- Not concluded: no GPU speedup, no XLA-GPU readiness, no production promotion,
  and no HMC/NeuTra end-to-end performance claim.

Trusted probes run:

```bash
nvidia-smi
```

Result:

- driver `580.159.03`, CUDA `13.0`;
- two `NVIDIA GeForce RTX 4080 SUPER` devices visible;
- GPU 0 had desktop/remote processes and was warm, GPU 1 was mostly idle.

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "<TensorFlow GPU list and matmul smoke>"
```

Result:

- TensorFlow `2.20.0`;
- physical GPUs:
  `/physical_device:GPU:0`, `/physical_device:GPU:1`;
- logical GPUs:
  `/device:GPU:0`, `/device:GPU:1`;
- a forced `tf.linalg.matmul` executed on `/device:GPU:0` and materialized a
  finite sum.

Direct experimental batched Kalman value+score smoke:

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "<direct experimental batched Kalman value+score GPU smoke>"
```

Result:

- TensorFlow created both GPU devices;
- `value_device=/job:localhost/replica:0/task:0/device:GPU:0`;
- `score_device=/job:localhost/replica:0/task:0/device:GPU:0`;
- `value=[-0.696081266808817, -0.39219291644195065, -1.065192283909461]`;
- `score_shape=(3, 2)`;
- finite value and score outputs: `True`.

One invalid intermediate smoke imported the CPU-only pytest helper, which sets
`CUDA_VISIBLE_DEVICES=-1`; that run correctly reported CPU placement and is not
used as GPU evidence.

## CPU vs GPU B=20 Timing Diagnostic

Evidence contract:

- Question: for the current experimental batched Kalman value+score kernel, is
  one `B=20` batch faster on GPU than CPU for `T=200`, `n=10`, `m=10`, `p=2`?
- Comparator: same standalone benchmark harness, same deterministic synthetic
  fixture, same shape, same TensorFlow environment.
- Primary diagnostic: warm-call median after three warmups and 30 materialized
  repeats.
- Veto diagnostics: wrong tensor placement, nonfinite value/score output, or
  mismatched shape.
- Explanatory only: first-call time, min/mean/max timing, and per-filter timing.
- Not concluded: no production GPU policy, no HMC/NeuTra end-to-end speedup,
  no broad shape scaling result, and no claim that GPU is generally slower.

Harness:

- `docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py`

Artifacts:

- `docs/benchmarks/experimental-batched-kalman-value-score-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-value-score-gpu1-b20-t200-n10-m10-2026-06-14.json`

Command shape:

- CPU: `--device-scope cpu --device /CPU:0 --expect-device-kind cpu`;
- GPU: `--device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu`;
- TensorFlow `2.20.0`;
- Python `3.13.13`;
- `B=20`, `T=200`, `state_dim=10`, `obs_dim=10`, `parameter_dim=2`;
- experimental value+score kernel only;
- 3 warmups, 30 measured warm calls;
- each call materialized both `value.numpy()` and `score.numpy()`.

Results:

| Device | Visible GPUs | Value device | Score device | First call | Warm median | Warm mean | Per-filter warm median |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| CPU | none (`CUDA_VISIBLE_DEVICES=-1`) | CPU:0 | CPU:0 | `1.6976s` | `0.3346s` | `0.3335s` | `0.01673s` |
| GPU 1 | one logical GPU mapped from physical GPU 1 | GPU:0 | GPU:0 | `2.3007s` | `0.5788s` | `0.5677s` | `0.02894s` |

Finite/output checks:

- CPU: `value_shape=(20,)`, `score_shape=(20, 2)`,
  `value_sum=-1016.7307167769168`, `score_abs_max=1479.100365931203`;
- GPU: `value_shape=(20,)`, `score_shape=(20, 2)`,
  `value_sum=-1016.7307167769156`, `score_abs_max=1479.1003659312034`.

Interpretation:

- For this exact `float64`, small-matrix, sequential-time workload, GPU was
  slower: `0.5788s / 0.3346s = 1.73x` the CPU warm median.
- The likely explanation is not that GPU is unavailable; placement was GPU.
  The current kernel performs `T=200` sequential steps with many relatively
  small `10 x 10` batched linear algebra operations in `float64`, where launch,
  synchronization, and consumer-GPU FP64 throughput can dominate.
- This result argues against expecting a speedup from `B=20` alone on the
  current experimental float64 kernel.  The next discriminating timing would be
  a batch-size ladder such as `B=20, 50, 100, 200` and, if acceptable for the
  model, a separate `float32` diagnostic.

## CPU vs GPU B=200 Timing Diagnostic

Evidence contract:

- Question: does increasing the parameter batch to `B=200` create enough
  batched work for the current experimental value+score kernel to run faster on
  GPU than CPU for `T=200`, `n=10`, `m=10`, `p=2`?
- Comparator: same standalone benchmark harness and deterministic synthetic
  fixture as the `B=20` timing diagnostic, with only `batch_size` and the
  repeat count changed.
- Primary diagnostic: warm-call median after two warmups and 10 materialized
  repeats.
- Veto diagnostics: wrong tensor placement, nonfinite value/score output, or
  mismatched shape.
- Not concluded: no production GPU policy, no HMC/NeuTra end-to-end speedup,
  no broad batch-size crossover estimate, and no claim about `float32`.

Artifacts:

- `docs/benchmarks/experimental-batched-kalman-value-score-cpu-b200-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-value-score-gpu1-b200-t200-n10-m10-2026-06-14.json`

Command shape:

- CPU: `--device-scope cpu --device /CPU:0 --expect-device-kind cpu`;
- GPU: `--device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu`;
- TensorFlow `2.20.0`;
- Python `3.13.13`;
- `B=200`, `T=200`, `state_dim=10`, `obs_dim=10`, `parameter_dim=2`;
- experimental value+score kernel only;
- 2 warmups, 10 measured warm calls;
- each call materialized both `value.numpy()` and `score.numpy()`.

Results:

| Device | Visible GPUs | Value device | Score device | First call | Warm median | Warm mean | Per-filter warm median |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| CPU | none (`CUDA_VISIBLE_DEVICES=-1`) | CPU:0 | CPU:0 | `3.0781s` | `1.7887s` | `1.7710s` | `0.00894s` |
| GPU 1 | one logical GPU mapped from physical GPU 1 | GPU:0 | GPU:0 | `2.1796s` | `0.5480s` | `0.5554s` | `0.00274s` |

Finite/output checks:

- CPU: `value_shape=(200,)`, `score_shape=(200, 2)`,
  `value_sum=-10134.85205457647`, `score_abs_max=1479.100365931203`;
- GPU: `value_shape=(200,)`, `score_shape=(200, 2)`,
  `value_sum=-10134.85205457646`, `score_abs_max=1479.1003659312034`.

Interpretation:

- For this exact `float64`, `B=200`, `T=200`, `n=m=10` workload, GPU was faster:
  `1.7887s / 0.5480s = 3.26x` lower warm-median wall time.
- Relative to `B=20`, this shows the expected batch-axis crossover behavior:
  the same GPU path was slower at `B=20` but faster at `B=200`.
- This supports using GPU for large batches of independent parameter proposals
  or surrogate-training likelihood evaluations, while keeping the caveat that
  time remains sequential and the crossover batch size has not yet been mapped.

## Large GPU Batch Capacity Diagnostic

Evidence contract:

- Question: is `B=4096` feasible for the same experimental batched Kalman
  value+score workload, and does the tested feasible range extend above it?
- Comparator: GPU-only capacity/timing probes on physical GPU 1 through
  `CUDA_VISIBLE_DEVICES=1`.
- Primary diagnostic: successful materialized value and score outputs on GPU
  with finite values.
- Veto diagnostics: CUDA OOM, nonfinite value/score output, CPU placement, or
  shape mismatch.
- Not concluded: no largest-batch maximum, no memory ceiling, no production
  default, and no stable timing claim for rows with one repeat or no warmup.

Artifacts:

- `docs/benchmarks/experimental-batched-kalman-value-score-gpu1-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-value-score-gpu1-b8192-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-value-score-gpu1-b16384-t200-n10-m10-2026-06-14.json`

Results:

| Batch | Warmups | Repeats | First call | Warm median | Per-filter warm median | Value shape | Score shape |
| ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `4096` | `1` | `3` | `4.2407s` | `2.4975s` | `0.000610s` | `(4096,)` | `(4096, 2)` |
| `8192` | `1` | `1` | `6.5238s` | `4.9715s` | `0.000607s` | `(8192,)` | `(8192, 2)` |
| `16384` | `0` | `1` | `11.6789s` | `10.0138s` | `0.000611s` | `(16384,)` | `(16384, 2)` |

All three rows placed `value` and `score` on `/device:GPU:0` after mapping
physical GPU 1 into the process with `CUDA_VISIBLE_DEVICES=1`.  All three rows
had finite outputs and the same `score_abs_max` up to floating-point display.

Interpretation:

- `B=4096` is feasible for the current `T=200`, `n=m=10`, `p=2`, `float64`
  experimental value+score workload on this RTX 4080 SUPER setup.
- The tested feasible range extends at least to `B=16384` for this shape, but
  the true maximum was not searched.
- Per-filter warm timing was essentially flat from `B=4096` to `B=16384`
  (`~0.00061s/filter`), suggesting the GPU is in a throughput regime for this
  workload by `B=4096`.

## Scalar Parity For Realistic Timing Fixture

Evidence contract:

- Question: do selected rows from the experimental batched `T=200`, `n=10`,
  `m=10`, `p=2` value+score workload match the existing non-batched scalar
  APIs?
- Comparator: scalar `tf_linear_gaussian_log_likelihood` for value and scalar
  `tf_qr_linear_gaussian_score` for analytic score.
- Primary criterion: row-sampled value and score agreement within
  `value_atol=value_rtol=1e-9` and `score_atol=score_rtol=5e-8`.
- Veto diagnostics: nonfinite batched outputs or any sampled row failing value
  or score tolerance.
- Not concluded: no exhaustive row-by-row parity for every large batch row, no
  masked/time-varying/Hessian parity, and no nonlinear UKF parity.

Harness:

- `docs/benchmarks/check_experimental_batched_kalman_parity.py`

Artifacts:

- `docs/benchmarks/experimental-batched-kalman-parity-b200-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-parity-b4096-t200-n10-m10-2026-06-14.json`

Results:

| Batch | Rows checked | Passed | Max abs value error | Max abs score error | Max rel value error | Max rel score error |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| `200` | `0, 100, 199` | yes | `3.13e-13` | `6.82e-13` | `3.42e-15` | `4.86e-16` |
| `4096` | `0, 2048, 4095` | yes | `3.13e-13` | `2.27e-13` | `2.90e-15` | `9.51e-16` |

Interpretation:

- The realistic timing fixture is now row-sample verified against the existing
  scalar non-batched value and analytic QR-score implementations.
- This substantially strengthens the timing evidence: the batched kernel is not
  merely finite on the benchmark fixture; sampled rows agree with the scalar
  authority path to roundoff-level error.
- The check is still sampled-row parity.  Before promotion, add a proper pytest
  that covers `n>1`, `m>1`, and multiple rows with bounded runtime.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Keep additive experimental module | Passed focused tests including `B=1` | No focused veto fired | No external review verdict yet | Run another read-only review and wider shape tests | No production readiness |
| Use combined value+score for HMC/NeuTra prototype | Passed tiny value+score parity | Shape mismatch test fails closed | Memory/scaling unknown | Add HMC-style adapter test or benchmark only after review | No sampler convergence |
| Direct covariance first slice | Passed tiny QR-score parity | No drift on tiny fixture | Wider numerical stress unknown | Stress larger `n,m,T,B`; switch to QR if drift appears | No QR-batched readiness |

## Next Steps

1. Retry Claude/read-only review when worker auth is healthy.
2. Add a tiny HMC-style adapter fixture that returns `log_prob[B]` and
   `score[B, p]` from the experimental kernel without editing HMC runtime files.
3. Add wider deterministic stress rows for `n > 1`, `m > 1`, and `B > 3`.
4. Only after review and wider parity, add CPU/GPU timing diagnostics.

## Post-Run Red Team

Strongest alternative explanation: the passing tests may be too friendly because
the fixture has `n=1` and `m=1`. That catches row batching and score signs but
does not stress matrix-axis mistakes enough.

Result that would overturn this first slice: a wider `n > 1`, `m > 1` parity
test fails against scalar QR score while the scalar value path remains correct.
That would indicate the direct sensitivity algebra needs repair or QR batching.

Weakest evidence: no successful Claude review verdict and no GPU/trusted-device
run. This is an additive prototype, not a merge-ready backend.
