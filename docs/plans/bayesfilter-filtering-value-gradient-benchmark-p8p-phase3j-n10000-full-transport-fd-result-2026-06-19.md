# P8p Phase 3j Result: N=10000 Full-Transport FD Validation

Date: 2026-06-19

Status: `BLOCKED_RUNTIME_FEASIBILITY_RUN_ABORTED`

## Question

Does the Phase 3i candidate transport AD contract,
`transport_ad_mode=full`, still agree with regression finite differences for
SIR d18 at a meaningful particle count (`N=10000`)?

## Short Answer

Not answered.  Phase 3j exposed a runtime-feasibility failure in the diagnostic
harness, not a mathematical disproof of the `full` transport AD contract.

The exact five-seed, three-direction, 9-point FD protocol at `N=10000`,
streaming active transport, `full` AD, and TF32 remained active for more than
six hours with no result artifact.  The run was killed after explicit user
authorization.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Primary criterion | Not evaluated; no Phase 3j JSON artifact was produced. |
| Veto status | Vetoed by missing artifact and unbounded runtime. |
| Engineering conclusion | The exact Phase 3j harness is currently too expensive for `N=10000`. |
| Scientific conclusion | No conclusion about HMC readiness, posterior validity, full-horizon stability, or correctness of `transport_ad_mode=full`. |
| Next justified action | Replace the full diagnostic with a bounded, observable Phase 3j-b: first AD/JVP-only at `N=10000`, then one targeted FD direction with progress logging. |

## What Happened

1. Reverse-gradient `N=10000` attempts with `transport_ad_mode=full` OOMed
   under chunk sizes `4096`, `1024`, and `512`.
2. A streaming full-AD epsilon broadcast bug was found and fixed for non-full
   column chunks in
   `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
3. Seed microbatching and forward-mode JVP were added to
   `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`.
4. A small trusted-GPU forward-JVP microbatch smoke passed, showing the new
   execution route was mechanically viable.
5. The full Phase 3j command was launched with:
   - `T=3`, `N=10000`;
   - seeds `81120,81121,81122,81123,81124`;
   - `--seed-microbatch-size 1`;
   - `--ad-evaluation-mode forward-jvp`;
   - `--transport-policy active-all`;
   - `--transport-plan-mode streaming`;
   - `--transport-ad-mode full`;
   - chunk sizes `512`;
   - float32 with TF32 enabled;
   - semantic-orthogonal 9-point FD.
6. PID `3937030` remained active after approximately `06:21:49`, with CPU time
   approximately `06:16:47`, CPU around `98.6%`, GPU memory around
   `15714 MiB / 16376 MiB`, and GPU utilization around `36%`.
7. The expected artifact was still absent:
   `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-streaming-fd-gpu-tf32-2026-06-19.json`.
8. The user authorized killing the process; `kill 3937030` succeeded.
9. After the kill, trusted `nvidia-smi` showed GPU memory near
   `2119 MiB / 16376 MiB`.

## Root Cause Assessment

The likely failure mode is diagnostic-harness explosion:

- five fixed seeds are evaluated as sequential microbatches;
- forward JVP computes directional AD over the raw parameter basis;
- semantic-orthogonal FD then evaluates three directions;
- each direction uses a 9-point OLS finite-difference line;
- each objective value is a full `N=10000`, active-all, streaming Sinkhorn,
  `full` transport-AD evaluation;
- the process holds memory close to the 16 GB GPU ceiling and does not expose
  intermediate progress in the current Phase 3j command.

This is compatible with the earlier Phase 3i observation that `full` transport
AD is much more expensive than the stabilized contract.  It is not evidence
that the `full` gradient is wrong.

## Checks And Patches

Checks after the local harness patch:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
```

Both checks passed.

A tiny trusted-GPU mechanics smoke also passed after adding:

- `--direction-filter`, to evaluate selected FD directions only;
- `--progress-output`, to write a JSON progress record after AD and after each
  completed FD window.

The smoke was not used as scientific evidence because the one-seed semantic
metric is degenerate.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 3j as a runtime-feasibility blocker and do not keep waiting. | Not evaluated; no JSON artifact. | Failed missing-artifact/runtime veto. | Whether `full` AD agrees with FD at `N=10000` under a bounded targeted diagnostic. | Execute Phase 3j-b with AD/JVP-only first, then a single semantic direction FD with progress logging. | No HMC/NUTS readiness, no posterior validity, no exact likelihood correctness, no default promotion, no leaderboard ranking. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `06947b1917c8000d930d52f0027c76a4c6a08c6c` |
| Host | `DESKTOP-RF1Q5IJ` |
| Device | NVIDIA GeForce RTX 4080 SUPER, trusted `nvidia-smi` |
| Environment | Python 3.11.14, TensorFlow 2.19.1 in the runner output |
| Precision | float32, TF32 enabled |
| Seeds | `81120,81121,81122,81123,81124` |
| State/observation dimension | SIR d18, obs dim 9 |
| Time steps / particles | `T=3`, `N=10000` |
| Transport settings | active-all, streaming, full transport AD, Sinkhorn epsilon `1.0`, iterations `10`, chunks `512` |
| PID stopped | `3937030` |
| Elapsed at stop check | about `06:21:49` |
| Output artifact | Missing |

## Boundary Notes

- This is DPF/SIR d18 work only.
- This is not Zhao-Cui source-faithfulness evidence.
- This is not monograph rewrite work.
- TF32 was not disabled.
- The default transport AD mode was not changed.
