# P01 Result: Small Deterministic Correctness Gate

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P01 passed; draft and review P02 trusted GPU precision subplan. |
| Primary criterion status | Passed: exact P01 command exited 0, wrote JSON/MD, and JSON reported `overall_passed: true`. |
| Veto diagnostic status | No P01 veto fired. Outputs were finite, value parity held, CPU placement matched, JIT smoke passed, and source diagnostics passed. |
| Main uncertainty | This was intentionally CPU-hidden and cannot establish GPU behavior or TF32 adequacy. |
| Next justified action | Review P02 trusted GPU precision drift subplan, then run P02 only if the subplan converges. |
| What is not concluded | No GPU evidence, no TF32 precision adequacy, no target-shape viability, no speedup, no posterior correctness, and no HMC readiness. |

## Command Actually Run

```bash
python docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py --cuda-visible-devices -1 --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 2 --time-steps 2 --num-particles 3 --transport-policy no-resampling --sinkhorn-iterations 2 --row-chunk-size 2 --col-chunk-size 2 --particle-chunk-size 2 --skip-score-fd --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.md
```

## Required Artifacts

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.md`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-subplan-2026-06-20.md`

## Observed Gate Metadata

| Field | Observed |
| --- | --- |
| `overall_passed` | `true` |
| `cuda_visible_devices` | `"-1"` |
| `device` | `"/CPU:0"` |
| `device_scope` | `"cpu"` |
| `expect_device_kind` | `"cpu"` |
| `physical_gpus` | `[]` |
| `logical_gpus` | `[]` |
| shape | `batch_size=2`, `time_steps=2`, `num_particles=3`, `state_dim=1`, `obs_dim=1` |

## Checks

| Check | Status |
| --- | --- |
| `finite_outputs` | passed |
| `streaming_vs_baseline_parity` | passed |
| `likelihood_only_omits_history` | passed |
| `device_placement` | passed |
| `jit_compile_smoke` | passed |
| `source_uses_tf_while_loop_not_python_time_loop` | passed |

## Interpretation

The deterministic streaming LEDH-PFPF-OT correctness gate still passes with
GPUs intentionally hidden.  The CUDA initialization warning in stderr is
consistent with CPU-hidden execution and is not trusted GPU evidence.

This result supports advancing to a trusted GPU precision screen.  It does not
support any posterior, HMC, target-shape, speed, or statistical ranking claim.

## Next Subplan Review

P02 is material because it crosses from CPU-hidden correctness into trusted GPU
precision evidence.  It requires local consistency checks and Claude read-only
review before execution.
