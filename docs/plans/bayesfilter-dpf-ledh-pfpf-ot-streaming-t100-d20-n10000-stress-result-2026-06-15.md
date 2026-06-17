# BayesFilter DPF LEDH-PFPF-OT Streaming T100 D20 N10000 Stress Result

Date: 2026-06-15

Plan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-streaming-t100-d20-n10000-stress-plan-2026-06-15.md`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | The streaming path can run the requested `T=100,D=20,N=10000` active-all GPU case, but it is compute-bound. |
| Primary criterion | Passed: finite GPU-placed likelihood emitted before timeout. |
| Veto diagnostic status | No veto fired. |
| Main uncertainty | Single run only; no statistical timing ranking. |
| Next justified action | Try chunk-size tuning and ESS/active-odd policies; exact active-all OT is too slow for routine use at this size. |
| What is not concluded | No production readiness, no posterior validity, no CPU/GPU superiority, no `N=100000` practicality claim. |

## Run

Command class: trusted GPU benchmark with 900s timeout.

Shape: `B=1,T=100,N=10000,state_dim=20,obs_dim=20`.

Settings:

- GPU: `GPU:0`, RTX 4080 SUPER.
- XLA: `tf.function(jit_compile=True)`.
- Transport: active-all, streaming, raw gradient, no dense transport matrix.
- Proposal: callback, no full `[B,T,N,D]` pre-flow tensor.
- Chunks: row `512`, col `512`, particle `128`.
- Sinkhorn iterations: `4`.

## Result

| Metric | Value |
| --- | ---: |
| Compile plus first call | 269.354 s |
| Warm call | 251.385 s |
| Peak GPU allocator memory | 20,504,576 bytes |
| Finite output | true |
| GPU output placement | true |
| Dense transport matrix materialized | false |
| Full pre-flow tensor stored | false |

Artifact:
`docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t100-np10000-d20-m20-activeall-callback-2026-06-15.json`

## Interpretation

- Memory is not the binding constraint for this streaming implementation at the
  tested shape.
- Runtime is the binding constraint: exact active-all OT remains all-pairs
  computation, and chunking trades memory for repeated block work.
- The result supports the engineering claim that streaming removes avoidable
  dense storage, but it does not make active-all exact OT cheap at `N=10000`.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Compile time, warm time, allocator memory. |
| Default-readiness | Not ready. |
| Next evidence needed | Scaling ladder with chunk-size tuning and non-active-all transport policies. |
