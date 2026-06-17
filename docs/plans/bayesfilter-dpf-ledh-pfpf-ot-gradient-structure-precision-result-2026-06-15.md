# BayesFilter DPF LEDH-PFPF-OT Gradient Structure/Precision Result - 2026-06-15

## Question

For HMC, the key object is the gradient.  This result asks whether the
memory-efficient streaming OT data structure changes the LEDH-PFPF-OT score,
and how FP32/TF32 affect the score on a focused GPU diagnostic.

Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-gradient-structure-precision-plan-2026-06-15.md`

## Main Findings

1. FP64 dense tensor, streaming dense tensor, streaming streaming tensor, and
   equivalent callback routes matched the score to machine precision on the
   focused GPU fixture.
2. FP32 without TF32 had small score drift versus FP64 on the same streaming
   tensor route.
3. FP32 with TF32 had materially larger score drift and failed the strict
   within-FP32 structure tolerance.
4. The current streaming score path did not XLA/JIT compile; the no-JIT score
   diagnostic was used to measure gradient values.  This is an HMC performance
   blocker, separate from gradient correctness.

## GPU Score Results

Fixture: `B=1, T=5, N=32, D=4, M=4`, active-odd transport, 3 Sinkhorn iterations,
raw TensorFlow transport gradients, no-JIT score diagnostic.

FP64 data-structure comparison against original dense tensor:

| arm | value max abs | score max abs | score relative | score cosine | norm ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| streaming dense tensor | 0 | 8.8818e-16 | 1.4944e-16 | 1.0 | 1.0 |
| streaming streaming tensor | 0 | 1.7764e-15 | 2.9888e-16 | 1.0 | 1.0 |
| streaming streaming equivalent callback | 0 | 1.7764e-15 | 2.9888e-16 | 1.0 | 1.0 |

Streaming tensor precision drift versus FP64 dense reference:

| arm | value max abs | score max abs | score relative |
| --- | ---: | ---: | ---: |
| FP32, TF32 disabled | 1.2786e-6 | 7.6743e-7 | 1.2912e-7 |
| FP32, TF32 enabled | 1.9440e-4 | 3.5738e-3 | 9.2621e-4 |

Interpretation: on this diagnostic, the data structure does not change the
mathematical gradient in FP64.  Precision does matter: FP32-no-TF32 looks
compatible with this score screen, while TF32 perturbs the score enough that it
should not be the HMC default without additional energy-error evidence.

## JIT Compile Caveat

The first attempted compiled streaming score run failed with:

`XLA compilation requires a fixed tensor list size... TensorArray in a while loop`

That means the value path can be JIT-ready while the score path is not yet
fully JIT-ready.  For HMC, this is a major implementation issue because HMC
needs repeated score evaluations.  The next engineering repair is to make the
streaming score path XLA-compatible, likely by setting fixed maximum iterations
or restructuring TensorArray/while-loop gradient accumulators.

## Decision Table

| field | status |
| --- | --- |
| decision | Continue with streaming OT data structure; do not use TF32 for the HMC-facing score path by default. |
| primary criterion status | FP64 dense-vs-streaming score equivalence passed in no-JIT diagnostic. |
| veto diagnostic status | JIT score path failed; this blocks performance-readiness, not the no-JIT gradient equivalence result. |
| main uncertainty | Small fixture only; no HMC trajectory/energy-error test yet. |
| next justified action | Repair XLA score compile, then rerun FP32-no-TF32 gradient and HMC energy diagnostics at larger sizes. |
| not concluded | No HMC readiness, posterior validity, production default, or statistical precision ranking. |

## Inference Status

| row | status |
| --- | --- |
| hard veto screen | No-JIT finite score screen passed; JIT score screen failed. |
| statistically supported ranking | None; one deterministic fixture only. |
| descriptive-only differences | FP32-no-TF32 score drift was `7.6743e-7`; TF32 score drift was `3.5738e-3`. |
| default-readiness | Not ready for HMC until score path JITs and HMC energy diagnostics pass. |
| next evidence needed | XLA-compatible score path, multi-shape gradient ladder, and HMC energy/acceptance diagnostics. |

## Run Manifest

| field | value |
| --- | --- |
| git commit | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, TensorFlow 2.20.0 |
| CPU/GPU status | GPU trusted run, `/GPU:0`, NVIDIA GeForce RTX 4080 SUPER, driver 580.159.03, 32760 MiB |
| random seed | `20260615` |
| FP64 artifact | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-gradient-structure-gpu0-b1-t5-np32-d4-m4-fp64-nojit-2026-06-15.json` |
| FP32 artifact | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-gradient-structure-gpu0-b1-t5-np32-d4-m4-fp32-notf32-nojit-2026-06-15.json` |
| TF32 artifact | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-gradient-structure-gpu0-b1-t5-np32-d4-m4-fp32-tf32-nojit-2026-06-15.json` |
| plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-gradient-structure-precision-plan-2026-06-15.md` |
| result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-gradient-structure-precision-result-2026-06-15.md` |

## Post-Run Red Team

- Strongest alternative explanation: the fixture is too small and well-scaled
  to expose gradient pathologies that appear at larger `N`, `D`, sharper
  observations, or active-all transport.
- What would overturn the conclusion: score mismatch between dense and
  streaming on a larger fixed-pre-flow ladder, non-finite gradients, or HMC
  energy instability under FP32.
- Weakest evidence: no-JIT score diagnostics are not enough for HMC performance
  readiness.

## Verification

- Tiny CPU no-JIT score comparison: passed.
- GPU FP64 no-JIT score comparison: passed.
- GPU FP32 no-TF32 no-JIT score comparison: passed.
- GPU FP32+TF32 no-JIT score comparison: finite but failed strict structure
  tolerance, as expected from larger score drift.
