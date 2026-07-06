# P02 Result: Trusted GPU Precision Drift Screen

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P02 passed; draft and review P03 target-shape trusted GPU subplan. |
| Primary criterion status | Passed: syntax checks, trusted `nvidia-smi`, precision comparison, and JSON hard-screen audit all passed. |
| Veto diagnostic status | No P02 veto fired. All three arms ran on GPU, emitted finite outputs, preserved matching configs/output arrays, and stayed below the predeclared `1.0e-2` max-relative drift bound. |
| Main uncertainty | This was a tiny deterministic fixture; it does not establish target-shape capacity, posterior correctness, HMC readiness, or statistical ranking. |
| Next justified action | Review P03 target-shape trusted GPU smoke subplan. |
| What is not concluded | No posterior correctness, no HMC readiness, no target-shape viability, no statistical superiority, no broad speedup claim, no dense Sinkhorn equivalence, and no public API readiness. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the tiny P02 deterministic GPU fixture. |
| Statistically supported ranking | None; single deterministic run and timing values are descriptive only. |
| Descriptive-only differences | TF32-enabled drift and timing were descriptively recorded but not ranked. |
| Default-readiness | Not established by P02 alone; default status remains by owner directive and requires later validation. |
| Next evidence needed | P03 target-shape trusted GPU smoke under production-default metadata. |

## Commands Actually Run

```bash
nvidia-smi
```

```bash
python docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py --cuda-visible-devices 0 --device-scope visible --device /GPU:0 --expect-device-kind gpu --batch-size 1 --time-steps 5 --num-particles 32 --state-dim 4 --obs-dim 4 --transport-policy active-odd --proposal-mode callback --sinkhorn-iterations 2 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --warmups 0 --repeats 1 --seed 20260620 --child-timeout-seconds 300 --artifact-dir docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-children-2026-06-20 --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.md
```

The JSON hard-screen audit from the P02 subplan exited 0.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `43bcb2015127712705d7ac77d3f0c9b01d349733` as recorded by child artifacts. |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`. |
| TensorFlow | `2.20.0` in child artifacts. |
| GPU status | Trusted `nvidia-smi` succeeded; GPU 0 was `NVIDIA GeForce RTX 4080 SUPER`. |
| Device | `/GPU:0`, `CUDA_VISIBLE_DEVICES=0`. |
| Seed | `20260620`. |
| Shape | `B=1`, `T=5`, `N=32`, `state_dim=4`, `obs_dim=4`. |
| Transport | `active-odd`, streaming, `sinkhorn_iterations=2`, row/col/particle chunks `16/16/16`. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-subplan-2026-06-20.md` |
| Result file | This file. |

## Artifacts

- Parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json`
- Parent Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.md`
- Child directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-children-2026-06-20/`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-subplan-2026-06-20.md`

## Observed Hard Screens

| Screen | Status |
| --- | --- |
| Parent `overall_passed` | `true` |
| Child arms | `fp64_reference`, `fp32_tf32_disabled`, `fp32_tf32_enabled` all passed. |
| GPU placement | All child outputs recorded `/device:GPU:0`. |
| GPU enumeration | All child artifacts recorded nonempty physical/logical GPU lists. |
| Config match | All three hard-screen config matches were `true`. |
| Output arrays | All three output-array presence checks were `true`. |
| Finite outputs | All three finite-output checks were `true`. |
| Precision metadata | FP64 had TF32 disabled; FP32-no-TF32 had TF32 disabled; FP32+TF32 had TF32 enabled. |
| Drift bound | Every reported max-relative drift was finite and `<= 1.0e-2`. |

## Drift Summary

| Arm | Largest max-relative drift |
| --- | ---: |
| `fp32_tf32_disabled` | `3.6488536461420185e-07` |
| `fp32_tf32_enabled` | `3.580009806270103e-05` |

The largest TF32-enabled absolute drift was log likelihood max abs
`0.00014452418137622658` on this tiny deterministic fixture.

## Interpretation

P02 supports that the promoted production-default TF32 route can run a tiny
deterministic precision screen on trusted GPU with finite outputs and no gross
drift relative to FP64 under the predeclared sanity bound.

It does not establish that the route helps the LEDH filter at target shape.  It
only removes the tiny-fixture precision/GPU-placement veto and justifies the
next target-shape smoke.

## Post-Run Red-Team Note

Strongest alternative explanation: the fixture is too small and too benign to
surface target-shape memory/runtime or numerical issues.

What would overturn this phase result: rerunning the same command with the same
environment and seed producing CPU fallback, nonfinite output, missing arrays,
or drift above the predeclared bound.

Weakest part of the evidence: the drift threshold is an engineering sanity
bound, not a mathematically derived accuracy guarantee.
