# P8j TF32 Batched Actual-SIR N10000 Feasibility Result

metadata_date: 2026-06-17
status: PASS_ENGINEERING_FEASIBILITY
plan: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-feasibility-plan-2026-06-17.md
executor: Codex

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `N=10000` works for the experimental batched TF32/GPU actual-SIR d18 streaming adapter. |
| Primary criterion status | Passed.  Both `B=1` and `B=5` trusted-GPU probes wrote artifacts, used GPU output tensors, had TF32 enabled, and produced finite outputs. |
| Veto diagnostic status | No OOM, no CPU fallback, no nonfinite output, no missing actual-SIR semantics metadata. |
| Main uncertainty | This is still the experimental streaming adapter route, not scalar Li-Coates Algorithm 1 UKF covariance-lifecycle parity and not MC-SE/leaderboard evidence. |
| Next justified action | Use this as permission to plan a real batched particle-count / MC-SE feasibility ladder, likely including adjacent rungs around `N=10000`. |
| What is not concluded | No selected SIR d18 particle count, no MC-SE adequacy, no leaderboard completion, no exact likelihood correctness, no DPF gradient correctness, no HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production/default readiness. |

## Checks

Trusted GPU preflight:

```bash
nvidia-smi
```

Result: NVIDIA GeForce RTX 4080 SUPER visible in trusted context.

Script syntax:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
```

Result: passed.

## B=1 Smoke

Command:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 512 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b1-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b1-probe-2026-06-17.md
```

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b1-probe-2026-06-17.json`

Summary:

| Field | Value |
| --- | --- |
| Shape | `B=1,T=20,D=18,M=9,N=10000` |
| Finite output | `true` |
| Output device | `/job:localhost/replica:0/task:0/device:GPU:0` |
| Precision | `float32`, TF32 enabled |
| Compile plus first call | `17.15657041501254s` |
| Warm call | `4.972724597901106s` |
| ESS min | `6751.9677734375` |
| Log likelihood | `-902.333251953125` |

## B=5 Full Five-Seed Probe

Command:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 512 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b5-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b5-probe-2026-06-17.md
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b5-probe-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b5-probe-2026-06-17.md`

Summary:

| Field | Value |
| --- | --- |
| Shape | `B=5,T=20,D=18,M=9,N=10000` |
| Seeds | `81120,81121,81122,81123,81124` |
| Finite output | `true` |
| Output device | `/job:localhost/replica:0/task:0/device:GPU:0` |
| Precision | `float32`, TF32 enabled |
| Compile plus first call | `20.731176869012415s` |
| Warm call | `7.375597111880779s` |
| Speedup vs old scalar `N=64` five-seed comparator | `107.07684435851894x` |
| Log likelihoods | `[-902.4349975585938, -902.6803588867188, -903.4465942382812, -903.185546875, -902.4032592773438]` |
| ESS minima | `[6441.296875, 6432.78173828125, 6482.1669921875, 6511.61083984375, 6437.65673828125]` |

The actual-SIR semantics block confirms:

- actual SIR callback metadata used;
- graph-compatible SIR transition copy used inside XLA;
- nonlinear prior-mean hook used;
- no scalar Algorithm 1 UKF covariance-lifecycle parity claim.

## Interpretation

`N=10000` is feasible on this GPU for the experimental batched TF32/GPU
actual-SIR adapter.  Runtime is no longer the immediate blocker for a serious
SIR d18 particle-count investigation.

The next scientific gate is not "can it run?" but whether a reviewed adjacent
particle ladder gives stable five-seed MC-SE evidence under the route we intend
to promote.
