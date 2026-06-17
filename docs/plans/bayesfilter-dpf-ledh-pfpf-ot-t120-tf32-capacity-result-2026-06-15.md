# BayesFilter DPF LEDH-PFPF-OT T120 TF32 Capacity Result - 2026-06-15

## Question

With the current streaming TF32 LEDH-PFPF-OT data structure, what
`state_dim`/`num_particles` regime can one 32GB RTX 4080 SUPER handle for
`T=120`, and should we use two GPUs via `MirroredStrategy`?

## Evidence Contract Check

- Baseline: current streaming callback value path, no dense `[N,N]` transport
  matrix, no stored full `[T,N,D]` pre-flow tensor.
- Precision: default experimental LEDH-PFPF-OT GPU policy, `float32` with TF32
  execution enabled.
- Primary criterion: finite GPU-placed JIT-compiled run plus warm-call timing.
- Veto diagnostics: OOM, non-finite output, wrong device, timeout before
  artifact, or missing TF32 metadata.
- Nonclaims: no HMC readiness, no posterior validity, no production default
  proof, and no two-GPU speedup claim.

## Run Manifest

| Field | Value |
| --- | --- |
| GPU | RTX 4080 SUPER, 32GB class, GPU 0 |
| Command family | `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` |
| Shared settings | `B=1,T=120`, active-all, callback proposal, streaming OT, `sinkhorn_iterations=4`, row/col chunks `512/512`, TF32 default |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-t120-tf32-capacity-plan-2026-06-15.md` |

## Results

| Shape | Status | Compile+first | Warm call | TF32 metadata | Artifact |
| --- | --- | ---: | ---: | --- | --- |
| `D=20,N=10000` | finite, GPU, JIT | `51.37s` | `40.29s` | `float32`, TF32 enabled | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-tf32-capacity-gpu0-b1-t120-np10000-d20-m20-activeall-callback-2026-06-15.json` |
| `D=50,N=5000` | finite, GPU, JIT | `94.81s` | `86.97s` | `float32`, TF32 enabled | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-tf32-capacity-gpu0-b1-t120-np5000-d50-m50-activeall-callback-2026-06-15.json` |
| `D=100,N=2000` | timeout, no artifact | `>900s` wall timeout | N/A | N/A | none |
| `D=100,N=1000` | timeout, no artifact | `>420s` wall timeout | N/A | N/A | none |

The successful TensorFlow allocator peak reported by the benchmark was only
about `73 MB`, which is not a whole-process VRAM claim. Still, both successful
runs and the high-dimensional timeouts indicate that current streaming memory
is not the binding constraint; runtime is.

## Interpretation

For `T=120` active-all exact OT on one 32GB RTX 4080 SUPER:

- `D=20,N=10000` is feasible and usable for occasional likelihood evaluations.
- `D=50,N=5000` is feasible but already expensive for repeated HMC-style calls.
- `D=100,N=1000` and `D=100,N=2000` are not practical under the current
  active-all exact OT/LEDH implementation; they timed out before producing
  artifacts.

The limiting cost is not dense matrix storage. It is the compute path:

- streaming OT still does all-pairs work, roughly `O(T N^2 D)`;
- LEDH adds per-particle high-dimensional linear algebra that becomes severe
  around `D=100`.

## Two-GPU Assessment

`tf.distribute.MirroredStrategy` is not an automatic fix for one large particle
filter. It replicates the computation on each GPU and reduces gradients/outputs;
it does not automatically shard a single `[N,N]` all-pairs transport problem
across GPUs.

Two GPUs can help immediately for:

- multiple independent HMC chains;
- multiple independent particle-filter seeds;
- batch rows representing independent parameter points, if the batched runner
  assigns rows to devices.

Two GPUs would help one huge particle cloud only after an explicit multi-GPU
algorithmic implementation:

- shard particles or row chunks across GPUs;
- communicate Sinkhorn softmin/logsumexp reductions;
- combine transported particle blocks;
- preserve deterministic gradients and fixed-branch semantics.

That is a separate distributed-OT implementation, not just a
`MirroredStrategy` wrapper.

## Decision Table

| Field | Status |
| --- | --- |
| Can we build the TF32 batched DPF now? | Yes, for the streaming value path and independent batch rows/chains/seeds. |
| Should the first batched target be `D=100,N=10000` active-all? | No. Current data show high-dimensional active-all exact OT is compute-bound before memory-bound. |
| Primary practical envelope | Around `T=120,D=20,N=10000` or `D=50,N=5000` for single value evaluations on one card. |
| HMC readiness | Not yet. Need JIT-safe score path and HMC energy/acceptance diagnostics. |
| Two-GPU readiness | Ready for embarrassingly parallel independent rows/chains; not ready for sharding one PF without a distributed OT design. |

## Next Step

Build the batched TF32 DPF around independent batch rows first:

1. `B` independent parameter rows/chains/seeds on one GPU.
2. Optional device-level launcher that splits batch rows across GPU 0/GPU 1.
3. Keep FP64/FP32-no-TF32 comparison scripts for audit.
4. Defer single-filter multi-GPU particle sharding until the single-GPU batched
   path and JIT-safe score path are stable.
