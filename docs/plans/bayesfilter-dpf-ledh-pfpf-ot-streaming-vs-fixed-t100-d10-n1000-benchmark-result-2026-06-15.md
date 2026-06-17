# BayesFilter DPF LEDH-PFPF-OT Streaming Vs Fixed Benchmark Result

Date: 2026-06-15

Plan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-streaming-vs-fixed-t100-d10-n1000-benchmark-plan-2026-06-15.md`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Streaming is better for compile/memory shape, but not faster on warm-call runtime at `T=100,N=1000,D=10` with current chunks. |
| Primary criterion | Passed: all compared runs emitted finite GPU-placed likelihoods. |
| Veto diagnostic status | No veto fired. |
| Main uncertainty | Single repeat only; warm-call differences are descriptive, not statistically ranked. |
| Next justified action | Tune streaming chunk sizes and run a scaling ladder where dense `[N,N]` storage becomes costly. |
| What is not concluded | No production readiness, no statistically supported speed ranking, no posterior validity, no `N=100000` practicality claim. |

## Run Matrix

Shared shape: `B=1,T=100,N=1000,state_dim=10,obs_dim=10`, GPU:0,
`tf.function(jit_compile=True)`, active-all transport, `sinkhorn_iterations=4`.

| Run | Proposal | Transport storage | Compile+first call | Warm call | Peak GPU allocator memory | Finite |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Fixed baseline | full `[B,T,N,D]` tensor | dense `[B,N,N]` | 113.004 s | 0.724 s | 75,591,936 bytes | true |
| Streaming | callback | no dense matrix | 13.540 s | 3.930 s | 2,097,152 bytes | true |
| Streaming | full `[B,T,N,D]` tensor | no dense matrix | 15.868 s | 5.849 s | 10,485,760 bytes | true |

## Interpretation

- Streaming improved compile-plus-first-call time by about `7x-8x`.
- Streaming reduced reported peak allocator memory substantially.
- Streaming did not improve warm-call speed at `N=1000`; it was slower than the
  dense fixed baseline in this single-repeat diagnostic.
- This is expected: streaming avoids dense `O(N^2)` storage, but exact OT still
  performs all-pairs `O(N^2)` computation in chunks. At `N=1000`, the dense
  matrix fits on the RTX 4080 SUPER and is faster after compilation.

## Artifacts

- Fixed baseline:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-fixed-lgssm-gpu0-b1-t100-np1000-d10-m10-activeall-dense-2026-06-15.json`
- Streaming callback:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t100-np1000-d10-m10-activeall-callback-2026-06-15.json`
- Streaming tensor:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t100-np1000-d10-m10-activeall-tensor-2026-06-15.json`

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for all three runs. |
| Statistically supported ranking | None; one repeat only. |
| Descriptive-only differences | Compile time, warm-call time, memory. |
| Default-readiness | Not ready. |
| Next evidence needed | Repeated warm-call ladder over chunk sizes and larger `N` values. |
