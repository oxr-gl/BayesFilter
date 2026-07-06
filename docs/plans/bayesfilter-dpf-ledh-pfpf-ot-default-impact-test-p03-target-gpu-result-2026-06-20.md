# P03 Result: Target-Shape Trusted GPU Smoke

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P03 passed; draft and review P04 performance/memory interpretation subplan. |
| Primary criterion status | Passed: syntax check, trusted `nvidia-smi`, target-shape command, and JSON hard-screen audit all passed. |
| Veto diagnostic status | No P03 veto fired. The target-shape smoke completed before `timeout 420`, emitted finite output, stayed on GPU, and preserved production-default GPU TF32 metadata. |
| Main uncertainty | This is one synthetic LGSSM-shaped target-shape smoke; runtime/memory are descriptive and not a speedup or broad scalability claim. |
| Next justified action | Review P04 performance/memory interpretation subplan. |
| What is not concluded | No posterior correctness, no HMC readiness, no statistical ranking, no broad speedup claim, no precision adequacy beyond P02, no dense Sinkhorn equivalence, and no public API readiness. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the `B=1,T=120,N=5000,D=50,M=50` trusted GPU smoke. |
| Statistically supported ranking | None; one run, no uncertainty analysis, and no ranking criterion. |
| Descriptive-only differences | Runtime, warm-call timing, and memory metadata are descriptive only. |
| Default-readiness | Supports continued engineering viability of the owner-directed default; does not by itself prove scientific/default readiness. |
| Next evidence needed | P04 interpretation, then later HMC mechanics and final synthesis if gates continue. |

## Commands Actually Run

```bash
nvidia-smi
```

```bash
timeout 420 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py --cuda-visible-devices 0 --device-scope visible --device /GPU:0 --expect-device-kind gpu --batch-size 1 --time-steps 120 --num-particles 5000 --state-dim 50 --obs-dim 50 --transport-policy active-all --proposal-mode callback --sinkhorn-iterations 4 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 64 --warmups 0 --repeats 1 --seed 20260620 --dtype float32 --tf32-mode enabled --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.md
```

The JSON hard-screen audit from the P03 subplan exited 0.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | The benchmark artifact inherits the current worktree; latest committed base before uncommitted artifacts was `43bcb2015127712705d7ac77d3f0c9b01d349733`. |
| Python | `3.13.13` |
| TensorFlow | `2.20.0` |
| GPU status | Trusted `nvidia-smi` succeeded; GPU 0 was `NVIDIA GeForce RTX 4080 SUPER`. |
| Device | `/GPU:0`, `CUDA_VISIBLE_DEVICES=0`. |
| Seed | `20260620`. |
| Shape | `B=1`, `T=120`, `N=5000`, `state_dim=50`, `obs_dim=50`. |
| Transport | `active-all`, streaming, `sinkhorn_iterations=4`, row/col chunks `512/512`, particle chunk `64`. |
| Timeout | `420` seconds; command completed before timeout. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-subplan-2026-06-20.md` |
| Result file | This file. |

## Artifacts

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.md`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-subplan-2026-06-20.md`

## Observed Hard Screens

| Screen | Observed |
| --- | --- |
| `finite_output` | `true` |
| Device | `/GPU:0`, output device `/device:GPU:0` |
| GPU metadata | Nonempty physical and logical GPU lists |
| Shape | `B=1,T=120,N=5000,state_dim=50,obs_dim=50` |
| Precision | `float32`, `tf32_mode=enabled`, `tf32_execution_enabled=true` |
| Default metadata | `precision_default_policy=production_ledh_pfpf_ot_gpu_tf32`; `default_algorithm_target=ledh_pfpf_ot_tf32`; `default_execution_target=gpu`; `default_target_status=production_default_by_owner_directive` |
| Storage/streaming | `plan_mode=streaming`, `dense_transport_matrix_materialized=false`, `stores_full_pre_flow_particles=false`, `return_history=false` |

## Descriptive Diagnostics

| Diagnostic | Value |
| --- | ---: |
| Compile plus first call seconds | `112.19805304496549` |
| Warm-call median seconds | `98.53211762499996` |
| GPU memory before current bytes | `2097408` |
| GPU memory after current bytes | `2097664` |
| GPU memory after peak bytes | `73400320` |
| Log likelihood preview | `1215.130859375` |

Historical context only: the 2026-06-15 experimental-metadata artifact at the
same shape also passed with finite GPU output, compile plus first call seconds
`94.80793855385855`, and warm-call median seconds `86.96749837393872`.  This is
not a speed comparison because the run was not paired, repeated, or uncertainty
analyzed, and the metadata/default status changed.

## Interpretation

P03 supports that the production-default GPU TF32 LEDH-PFPF-OT route can execute
the meaningful target-shape synthetic LGSSM smoke finitely on trusted GPU while
preserving the intended streaming/no-dense-storage metadata.

This is useful evidence that the promoted default helps the LEDH engineering
route in the narrow sense of making the target-shape value path operational on
GPU.  It is not evidence of posterior correctness, HMC readiness, or speed
superiority.

## Post-Run Red-Team Note

Strongest alternative explanation: the synthetic fixture may not stress the same
model/data path that will matter for the eventual LEDH filter workload.

What would overturn this phase result: rerunning the exact command and seeing
timeout, nonfinite output, CPU fallback, missing production-default metadata, or
dense/full-history storage metadata.

Weakest part of the evidence: target-shape viability is demonstrated for one
fixture and one seed only.
