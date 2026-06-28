# P02 Subplan: Trusted GPU Paired Medium Quality Screen

## Phase Objective

Run the paired quality aggregator on a medium GPU shape to test whether the
promoted `fp32_tf32_enabled` default preserves downstream filter outputs within
the predeclared tolerance relative to paired FP64 arms.

## Entry Conditions Inherited From Previous Phase

- P01 harness compile/static checks passed.
- P02 tolerance is fixed before seeing results:
  max-relative drift to FP64 `<= 1.0e-2` for the default arm on every output
  and paired seed.
- GPU/CUDA commands must run in trusted/elevated context.

## Required Artifacts

- Parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.json`
- Parent Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.md`
- Child artifact directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/`
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-result-2026-06-20.md`
- Refreshed P03 closeout subplan.

## Required Checks, Tests, And Reviews

- Trusted `nvidia-smi`.
- Trusted GPU command:

```bash
python docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py --cuda-visible-devices 0 --device-scope visible --device /GPU:0 --expect-device-kind gpu --batch-size 1 --time-steps 12 --num-particles 128 --state-dim 6 --obs-dim 6 --transport-policy active-all --proposal-mode callback --sinkhorn-iterations 3 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 64 --col-chunk-size 64 --particle-chunk-size 64 --num-seeds 3 --base-seed 20260620 --seed-stride 1009 --max-relative-tolerance 0.01 --child-timeout-seconds 900 --artifact-dir docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20 --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.md
```

- JSON audit that parent `overall_passed` is true, the default arm passed the
  tolerance screen, child hard screens passed, GPU placement is recorded,
  paired seed count is three, every required per-seed/per-output drift field is
  preserved, and field-level default precision metadata assertions pass.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the promoted GPU TF32 default preserve downstream filter outputs on a paired medium streaming quality screen? |
| Baseline/comparator | FP64 TF32-disabled arm for the same seed, shape, transport settings, and GPU device; FP32 TF32-disabled is diagnostic. |
| Primary pass criterion | All child hard screens pass, paired seed count is exactly three, every per-seed/per-output drift field is preserved, and default-arm max-relative drift to FP64 is `<= 1.0e-2` for `log_likelihood`, `filtered_means`, `filtered_variances`, and `ess_by_time` across all three seeds. |
| Drift formula | For each output array and paired seed, `max_relative_to_max1_abs_reference = max(abs(candidate - reference) / max(1.0, abs(reference)))`, computed elementwise and maximized over the output array. The same `1.0e-2` bound is used for all four outputs as a gross engineering sanity screen only, not as a scientific accuracy tolerance. |
| Required default metadata assertions | The `fp32_tf32_enabled` child precision metadata must include `precision_default_policy=production_ledh_pfpf_ot_gpu_tf32`, `default_execution_target=gpu`, `default_algorithm_target=ledh_pfpf_ot_tf32`, `default_target_status=production_default_by_owner_directive`, `default_dtype=float32`, `active_dtype=float32`, `default_tf32_mode=enabled`, `tf32_mode=enabled`, and `tf32_execution_enabled=true`. |
| Veto diagnostics | Child failure, timeout, nonfinite output, GPU placement mismatch, missing arrays, config mismatch, paired seed count mismatch, missing per-seed/per-output drift fields, missing precision metadata, default precision policy mismatch, or drift above tolerance. |
| Explanatory diagnostics | Runtime, memory, compile time, warm-call timing, FP32-no-TF32 drift, TF32-vs-no-TF32 extra drift, and per-seed drift spread. |
| Not concluded | No posterior correctness, no HMC readiness, no sampler convergence, no statistical superiority, no speedup, no dense Sinkhorn equivalence, no public API readiness, no target-shape HMC viability. |
| Artifact | P02 JSON/Markdown artifacts, child artifacts, and P02 result note. |

## Forbidden Claims And Actions

- Do not call this an exact Kalman validation.
- Do not rank FP32-no-TF32 versus FP32-TF32 statistically from three seeds.
- Do not infer speedup from timings.
- Do not continue to larger target-shape repeated runs if P02 hard vetoes fire.
- Do not change tolerance after seeing results.

## Exact Next-Phase Handoff Conditions

Proceed to P03 only if:

- P02 parent JSON exists and `overall_passed` is true;
- P02 JSON explicitly records the paired seeds, drift formula,
  per-seed/per-output drift records, worst default-arm drift by output, and
  default metadata assertion results;
- the P02 result records the actual command, manifest, decision table,
  inference-status table, exact comparator definition, tolerance semantics,
  worst per-seed/per-output drifts, artifacts, and nonclaims;
- P03 closeout subplan is refreshed for the observed result.

If P02 fails from a fixable harness or environment issue, write a blocker
result and repair plan rather than interpreting the default route as failed.

## Stop Conditions

Stop if:

- GPU is unavailable in trusted context;
- any child fails or times out in a way that cannot be clearly attributed to a
  fixable command/shape issue;
- paired seed count or per-seed/per-output drift records are missing;
- default drift exceeds tolerance;
- artifacts are missing or stale;
- continuing would require a longer target-shape run not covered by this
  subplan.
