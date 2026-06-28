# P01 Subplan: Paired Quality Harness Implementation

## Phase Objective

Add a minimal aggregate harness that reuses the existing streaming precision
wrapper across paired seeds and summarizes downstream output drift without
embedding large output arrays in the parent artifact.

## Entry Conditions Inherited From Previous Phase

- P00 plan/review gate passed.
- The target route is the current streaming GPU TF32 default benchmark.
- The primary P02 quality criterion is fixed before implementation:
  `fp32_tf32_enabled` max-relative drift to FP64 `<= 1.0e-2` for each output
  across paired seeds.

## Required Artifacts

- Benchmark wrapper:
  `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p01-harness-result-2026-06-20.md`
- Refreshed P02 subplan if implementation details differ from this subplan.

## Required Checks, Tests, And Reviews

- `python -m py_compile docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py`
- `python -m py_compile docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py`
- A CPU-hidden or no-execution parser check may be used if needed, but P01
  does not need to run TensorFlow.
- Local static consistency check that the wrapper references the existing
  streaming precision wrapper path.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the repository now have a minimal paired-seed quality aggregator for the current streaming precision harness? |
| Baseline/comparator | Existing `compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py` child wrapper. |
| Primary pass criterion | The new wrapper compiles and its command construction targets the existing streaming precision wrapper with paired seeds, artifact paths, exact tolerance formula metadata, per-seed/per-output drift preservation, and field-level default metadata assertions. |
| Drift formula | For each output array and paired seed, preserve `max_relative_to_max1_abs_reference = max(abs(candidate - reference) / max(1.0, abs(reference)))`, matching the existing streaming precision wrapper. |
| Required default metadata assertions | The wrapper must check the `fp32_tf32_enabled` precision metadata fields: `precision_default_policy=production_ledh_pfpf_ot_gpu_tf32`, `default_execution_target=gpu`, `default_algorithm_target=ledh_pfpf_ot_tf32`, `default_target_status=production_default_by_owner_directive`, `default_dtype=float32`, `active_dtype=float32`, `default_tf32_mode=enabled`, `tf32_mode=enabled`, and `tf32_execution_enabled=true`. |
| Veto diagnostics | Syntax error, wrong child script, missing seed pairing, no tolerance field, missing per-seed/per-output drift records, missing metadata assertions, parent artifact would embed child output arrays, or unsupported claims in the wrapper. |
| Explanatory diagnostics | Markdown formatting and compactness of summaries. |
| Not concluded | No GPU validity, no quality pass, no posterior correctness, no HMC readiness, no speed or statistical ranking. |
| Artifact | P01 result and wrapper source. |

## Forbidden Claims And Actions

- Do not run the medium GPU quality screen in P01.
- Do not add NumPy implementation paths for BayesFilter algorithms; NumPy is
  allowed only for reporting/array drift aggregation in this benchmark wrapper.
- Do not change the existing streaming benchmark behavior unless a focused
  blocker requires it.
- Do not modify unrelated dirty files.

## Exact Next-Phase Handoff Conditions

Proceed to P02 only if:

- the wrapper compiles;
- the P01 result records the actual checks;
- P02 command, shape, seeds, tolerance, and artifact paths are explicit.

## Stop Conditions

Stop and write a blocker result if:

- the existing streaming precision wrapper cannot provide output-array drift;
- the wrapper cannot avoid stale or oversized parent artifacts without
  modifying core benchmark semantics;
- local compile/static checks fail for nontrivial reasons.
