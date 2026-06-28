# P02 Result: Trusted GPU Paired Medium Quality Screen

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P02 passed; proceed to P03 closeout. |
| Primary criterion status | Passed: three paired seeds, all child hard screens, output-array screens, GPU placement screens, default metadata assertions, and default-arm tolerance screens passed. |
| Veto diagnostic status | No P02 veto fired. |
| Main uncertainty | This is a medium synthetic LGSSM-shaped quality screen with three paired seeds; it is not a posterior/scientific validation or statistical ranking. |
| Next justified action | Close out this program and draft a separate target-shape repeated stability subplan, not launched here. |
| What is not concluded | No posterior correctness, no HMC readiness, no sampler convergence, no speedup, no statistical superiority, no dense Sinkhorn equivalence, no public API readiness, and no target-shape scientific validity. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for P02 medium trusted-GPU paired quality rung. |
| Statistically supported ranking | None; three paired seeds are a quality screen only. |
| Descriptive-only differences | FP32-no-TF32 drift, TF32-vs-no-TF32 extra drift, runtime, memory, compile time, and warm timings are descriptive only. |
| Default-readiness | Supports the owner-directed GPU TF32 default through this medium downstream filter-output quality screen. |
| Next evidence needed | A reviewed target-shape repeated stability rung if we want evidence beyond medium synthetic quality. |

## Comparator And Tolerance Contract

| Field | Value |
| --- | --- |
| Comparator | Paired FP64 TF32-disabled streaming arm, same seed, shape, transport settings, and GPU device. |
| Default arm | `fp32_tf32_enabled`. |
| Diagnostic arm | `fp32_tf32_disabled`, descriptive only. |
| Drift formula | `max(abs(candidate - reference) / max(1.0, abs(reference)))` per output array and paired seed. |
| Tolerance | `1.0e-2`, a gross engineering sanity screen only. |
| Required outputs | `log_likelihood`, `filtered_means`, `filtered_variances`, `ess_by_time`. |

## Commands Actually Run

```bash
nvidia-smi
```

```bash
python docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py --cuda-visible-devices 0 --device-scope visible --device /GPU:0 --expect-device-kind gpu --batch-size 1 --time-steps 12 --num-particles 128 --state-dim 6 --obs-dim 6 --transport-policy active-all --proposal-mode callback --sinkhorn-iterations 3 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 64 --col-chunk-size 64 --particle-chunk-size 64 --num-seeds 3 --base-seed 20260620 --seed-stride 1009 --max-relative-tolerance 0.01 --child-timeout-seconds 900 --artifact-dir docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20 --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.md
```

The explicit JSON audit exited 0 and printed:

```text
p02_json_audit_ok
worst {'max_relative_to_max1_abs_reference': 0.0001302131797900768, 'output': 'log_likelihood', 'passed': True, 'seed': 20261629, 'tolerance': 0.01}
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `43bcb2015127712705d7ac77d3f0c9b01d349733` at run time; worktree had unrelated dirty/untracked files. |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`. |
| Host | `ubuntu-MZ72-HB2-00`. |
| GPU status | Trusted `nvidia-smi` succeeded. GPU 0 was `NVIDIA GeForce RTX 4080 SUPER`; CUDA driver report `13.0`. |
| Device | `/GPU:0`, `CUDA_VISIBLE_DEVICES=0`, `expect_device_kind=gpu`. |
| Shape | `B=1`, `T=12`, `N=128`, `state_dim=6`, `obs_dim=6`. |
| Seeds | `20260620`, `20261629`, `20262638`. |
| Transport | `active-all`, callback proposal, streaming transport, no dense transport matrix, row/col/particle chunks `64/64/64`, `sinkhorn_iterations=3`, `epsilon=0.5`. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-subplan-2026-06-20.md`. |
| Result file | This file. |

## Artifacts

- Parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.json`
- Parent Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.md`
- Child directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/`

## Hard Screens

| Screen | Status |
| --- | --- |
| Parent `overall_passed` | `true` |
| Paired seed count | `3` |
| Paired seeds | `[20260620, 20261629, 20262638]` |
| Child precision wrappers | All passed. |
| Seed match checks | All passed. |
| Output array presence | All passed. |
| Default metadata assertions | All passed. |
| Default tolerance screens | All passed. |
| Trusted GPU placement | All child output devices recorded `/device:GPU:0`. |

## Worst Default-Arm Drift By Output

| Output | Seed | Max relative drift | Tolerance | Passed |
| --- | ---: | ---: | ---: | --- |
| `log_likelihood` | `20261629` | `0.0001302131797900768` | `0.01` | true |
| `filtered_means` | `20260620` | `4.222283782952252e-05` | `0.01` | true |
| `filtered_variances` | `20261629` | `3.3208038858826812e-06` | `0.01` | true |
| `ess_by_time` | `20261629` | `4.772058632153245e-06` | `0.01` | true |

Worst overall default-arm drift was `0.0001302131797900768` for
`log_likelihood` at seed `20261629`, below the predeclared `0.01` screen.

## Interpretation

P02 supports that the promoted GPU TF32 streaming LEDH-PFPF-OT default preserves
the tested downstream filter outputs within the predeclared medium-screen
tolerance relative to paired FP64 arms on trusted GPU.

This is evidence that the default helps the LEDH filter more concretely than
the previous smoke ladder: it checks paired downstream filter outputs rather
than only finite execution and tiny precision drift. It remains a medium
synthetic engineering screen, not a posterior correctness or HMC-readiness
result.

## Post-Run Red-Team Note

Strongest alternative explanation: the medium synthetic shape and three seeds
may be too easy and may not stress the future target-shape LEDH workload.

What would overturn this phase result: rerunning the same contract and seeing
CPU fallback, missing arrays, nonfinite outputs, metadata mismatch, paired-seed
loss, or drift above `0.01`.

Weakest part of the evidence: the tolerance is a gross engineering bound and
the comparator is FP64 on the same synthetic route, not an exact Kalman/posterior
oracle.

