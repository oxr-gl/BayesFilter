# P8j TF32 Batched Actual-SIR N50000 Feasibility Result

metadata_date: 2026-06-17
status: PASS_FEASIBLE_BUT_EXPENSIVE
plan: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-feasibility-plan-2026-06-17.md
executor: Codex

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `N=50000` works for the experimental batched TF32/GPU actual-SIR d18 streaming adapter, but the five-seed batch is materially expensive. |
| Primary criterion status | Feasibility passed.  Both `B=1` and `B=5` trusted-GPU probes wrote artifacts, used GPU output tensors, had TF32 enabled, and produced finite outputs. |
| Veto diagnostic status | No OOM, CPU fallback, nonfinite output, or missing actual-SIR semantics metadata. |
| Runtime note | The full `B=5` warm call took `163.35498285200447s`.  It did not satisfy the older 5x speed gate versus scalar `N=64` because speedup was `4.834597942540259x`, but that speed gate was not the primary pass criterion for this `N=50000` feasibility question. |
| Main uncertainty | This remains the experimental streaming adapter route, not scalar Li-Coates Algorithm 1 UKF covariance-lifecycle parity and not MC-SE/leaderboard evidence. |
| Next justified action | Use `N=50000` as a high rung in a planned adjacent particle ladder only if MC-SE at lower rungs justifies the cost. |
| What is not concluded | No selected SIR d18 particle count, no MC-SE adequacy, no leaderboard completion, no exact likelihood correctness, no DPF gradient correctness, no HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production/default readiness. |

## B=1 Smoke

Command:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120 --time-steps 20 --num-particles 50000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b1-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b1-probe-2026-06-17.md
```

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b1-probe-2026-06-17.json`

Summary:

| Field | Value |
| --- | --- |
| Shape | `B=1,T=20,D=18,M=9,N=50000` |
| Finite output | `true` |
| Output device | `/job:localhost/replica:0/task:0/device:GPU:0` |
| Precision | `float32`, TF32 enabled |
| Compile plus first call | `49.78865125216544s` |
| Warm call | `37.02889353688806s` |
| ESS min | `33686.40625` |
| Log likelihood | `-903.0003662109375` |

## B=5 Full Five-Seed Probe

Command:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 50000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b5-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b5-probe-2026-06-17.md
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b5-probe-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b5-probe-2026-06-17.md`

Summary:

| Field | Value |
| --- | --- |
| Shape | `B=5,T=20,D=18,M=9,N=50000` |
| Seeds | `81120,81121,81122,81123,81124` |
| Finite output | `true` |
| Output device | `/job:localhost/replica:0/task:0/device:GPU:0` |
| Precision | `float32`, TF32 enabled |
| Compile plus first call | `171.2960470081307s` |
| Warm call | `163.35498285200447s` |
| Speedup vs old scalar `N=64` five-seed comparator | `4.834597942540259x` |
| Log likelihoods | `[-903.0592041015625, -902.501708984375, -903.0481567382812, -902.8697509765625, -902.8642578125]` |
| ESS minima | `[32286.685546875, 32056.00390625, 32381.6875, 32084.078125, 31872.62109375]` |

## Interpretation

`N=50000` is feasible, but not cheap.  It looks usable as an upper/high rung
for a serious reviewed tuning ladder, not as the first routine diagnostic rung.

The `N=10000` five-seed run took about `7.38s`; `N=50000` took about
`163.35s`, roughly `22.15x` slower for `5x` more particles.  That scaling is
consistent with all-pairs OT compute becoming the dominant cost.

## Boundary

The actual-SIR semantics metadata records:

- actual SIR callback metadata used;
- graph-compatible SIR transition copy used inside XLA;
- nonlinear prior-mean hook used;
- no scalar Algorithm 1 UKF covariance-lifecycle parity claim.

Therefore this result answers "does it run?" for the experimental streaming
adapter.  It does not answer particle adequacy, MC-SE convergence, or
leaderboard promotion.
