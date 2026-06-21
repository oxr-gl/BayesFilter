# P06 Large-Particle Efficiency Closeout And Default Certification

Date: 2026-06-21

Status: CERTIFIED_ACCEPTABLE_DEFAULT

## Certification

The BayesFilter DPF LEDH-PFPF-OT default is the GPU-oriented streaming TF32
route. It is certified as acceptable and should be used whenever possible for
BayesFilter DPF LEDH-PFPF-OT work when GPU execution and the streaming
fixed-branch contract are applicable.

This certification is operational and engineering-scoped. It certifies the
route as the default large-particle storage/capacity path, not as a proof of
posterior correctness, dense Sinkhorn equivalence, HMC readiness, public API
readiness, or statistically supported speed superiority.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Promote/certify GPU streaming TF32 LEDH-PFPF-OT as the acceptable default route for BayesFilter DPF LEDH-PFPF-OT work whenever applicable. |
| Primary criterion status | Passed: P03 clean GPU1 large-`N` ladder passed mandatory `N=1000`, `5000`, `10000`; optional `N=20000` also passed. |
| Veto diagnostic status | No certification veto remains: clean run had finite output, GPU placement, streaming plan mode, no dense transport matrix, no full pre-flow storage, `return_history=False`, and production-default TF32 metadata. |
| Main uncertainty | Runtime evidence remains mostly descriptive; posterior/scientific and HMC-readiness questions remain separate gates. |
| Next justified action | Use this route by default in future DPF LEDH-PFPF-OT work unless a reviewed artifact or owner directive supersedes it. |
| What is not concluded | No posterior correctness, no dense Sinkhorn equivalence, no HMC readiness, no public API readiness, no statistical speedup, no claim that dense/non-streaming is never useful at small `N`. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the GPU streaming TF32 LEDH-PFPF-OT route be certified as the default operational large-particle route? |
| Baseline/comparator | Storage/capacity comparison is against dense/full-history storage surfaces; P04 comparator is same-route FP32 with TF32 disabled. |
| Primary pass criterion | Clean trusted-GPU large-`N` ladder passes hard finite/device/storage/default-metadata gates through at least `N=10000`; same-route TF32 runtime context is recorded or justifiably blocked. |
| Veto diagnostics | Non-finite output, CPU fallback, missing artifact, dense matrix materialized, full pre-flow storage, `return_history=True`, wrong TF32/default metadata, selected-GPU contamination, or route/config mismatch. |
| Explanatory diagnostics | Warm-call timings, compile plus first-call timings, allocator memory metadata, and TF32-on/off ratio. |
| Not concluded | Scientific validity, posterior correctness, HMC readiness, public API readiness, dense equivalence, or statistical speedup. |
| Artifact | This closeout plus P03/P04/P05 result artifacts. |

## Supporting Evidence

P03 clean GPU1 large-particle ladder:

| N | Hard gate | Warm median s | Peak GPU allocator bytes | Explicit storage avoided |
| ---: | --- | ---: | ---: | ---: |
| `1000` | passed | `0.9543289658613503` | `75761408` | dense transport/history avoided |
| `5000` | passed | `5.236748277908191` | `76401408` | dense transport/history avoided |
| `10000` | passed | `11.879786128178239` | `77677056` | about `442 MiB` explicit dense/history storage avoided |
| `20000` | passed | `29.24114408181049` | `79290624` | about `1.61 GiB` explicit dense/history storage avoided |

P04 same-route TF32 context at `N=10000`:

| Arm | Hard gate | Warm median s | Interpretation |
| --- | --- | ---: | --- |
| TF32 enabled | passed | `11.870695133926347` | default arm |
| TF32 disabled | passed | `12.24538614996709` | same-route comparator |

The P04 warm-median ratio `enabled / disabled` was
`0.9694014536208195`, meaning TF32-enabled was descriptively about `3.06%`
lower in that one run. This remains descriptive only.

P05 dense breakpoint context was skipped with justification because it was not
a promotion criterion and could not alter the P03/P04 default-certification
decision.

## Operational Default Guidance

Use GPU streaming TF32 LEDH-PFPF-OT by default when:

- the task is BayesFilter DPF LEDH-PFPF-OT transport work;
- TensorFlow/TensorFlow Probability is the backend;
- GPU execution is available or expected;
- the streaming fixed-branch contract is applicable;
- dense `[B,N,N]` transport storage or full `[B,T,N,D]` pre-flow storage would
  be wasteful or risky.

Use explicit non-default/reference modes when:

- FP64 reference behavior is required;
- FP32 with TF32 disabled is required for a precision diagnostic;
- dense/non-streaming behavior is required as a small-reference comparator;
- posterior correctness, HMC readiness, or public API exposure is being tested
  under a separate reviewed plan.

## Artifacts

- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-ladder-result-2026-06-21.md`
- P03 parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.json`
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-result-2026-06-21.md`
- P04 parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json`
- P05 skip result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-result-2026-06-21.md`

## Post-Run Red-Team Note

Strongest alternative explanation: the route is operationally useful for
large-particle memory/capacity but may still need further model-specific
posterior, gradient, and HMC evidence before being used for claims beyond
default DPF transport execution.

What would overturn the certification: a human owner directive superseding the
default, or a reviewed hard-veto artifact showing the streaming GPU TF32 route
is invalid for the intended DPF LEDH-PFPF-OT default target.

Weakest part of the evidence: speed evidence is descriptive and single-repeat.
The certification rests primarily on storage/capacity feasibility and default
route governance, not on speed superiority.
