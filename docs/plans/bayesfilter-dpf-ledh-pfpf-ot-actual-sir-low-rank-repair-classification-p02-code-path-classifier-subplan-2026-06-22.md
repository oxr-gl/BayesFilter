# P02 Code-Path Classifier Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Inspect the owned benchmark and low-rank solver source to determine whether the
P03 comparable-but-slow evidence plausibly reflects route/timing implementation
asymmetry before any route-internal repair is planned.

## Entry Conditions Inherited From Previous Phase

P01 passed and wrote an artifact-only classifier summary. The P01 result did not
claim speedup, correctness, or implementation cause.

## Required Artifacts

- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p02-code-path-classifier-result-2026-06-22.md`
- Source-anchor excerpts recorded by path/line in the P02 result.
- Refreshed execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-visible-execution-ledger-2026-06-22.md`

## Required Checks/Tests/Reviews

- Inspect source anchors in
  `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` for:
  - low-rank route calling `low_rank_coupling_solver_resample_tf` inside the
    diagnostic route loop;
  - streaming route using `_run_streaming_compiled_core_timed`;
  - streaming compiled timing using `@tf.function(jit_compile=True,
    reduce_retracing=True)`;
  - paired timing ratio computed as streaming warm median over low-rank warm
    median.
- Inspect source anchors in
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
  for:
  - diagnostic semantic-replacement scope and nonclaims;
  - `.numpy()` diagnostics or Python bool/float conversions that imply eager
    host synchronization and graph-incompatibility risk;
  - nonmaterialized factor transport provenance.
- Inspect wrapper labels in
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py` to confirm
  `freeze-nominated` requires comparability, warm-time pass, low-rank
  provenance, and GPU/TF32 provenance.
- Run a read-only syntax/import-light check that does not initialize GPU:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`.
- Claude read-only review of P01/P02 results before P04 closeout unless P02
  must stop as `UNCLASSIFIED_NEEDS_MICROPROBE`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does source inspection support route-performance repair as a real next lane for comparable-but-slow candidates? |
| Baseline/comparator | P01 artifact classifier plus source anchors from the benchmark and low-rank solver. |
| Primary pass criterion | P02 classifies source evidence as `ROUTE_TIMING_ASYMMETRY_SUPPORTED`, `ROUTE_TIMING_ASYMMETRY_NOT_SUPPORTED`, or `SOURCE_UNCLEAR_NEEDS_MICROPROBE`, with path/line anchors. |
| Veto diagnostics | Missing source file, stale line anchor, unsupported route-cause claim, treating source inspection as speedup proof, or editing route internals. |
| Explanatory diagnostics | `tf.function` coverage, eager `.numpy()` diagnostics, diagnostic loop source, and wrapper label rules. |
| Not concluded | No implementation repair, no compiled low-rank feasibility proof, no speedup claim, no correctness claim, and no dense Sinkhorn equivalence. |
| Artifact | P02 result with source anchors and next-phase recommendation. |

## Forbidden Claims/Actions

- Do not edit source files.
- Do not run GPU benchmarks.
- Do not claim low-rank can be safely compiled until a reviewed implementation
  or microprobe subplan tests it.
- Do not let source inspection override P03 artifact evidence.

## Exact Next-Phase Handoff Conditions

Advance to P04 closeout if P02 can classify the failure as
`ROUTE_TIMING_ASYMMETRY_SUPPORTED` plus P01 has independent
comparability/ESS/tuning evidence. Advance to P03 only if P02 records
`SOURCE_UNCLEAR_NEEDS_MICROPROBE` and the microprobe remains within the
predeclared boundary.

## Stop Conditions

- Stop if source anchors are missing or materially stale.
- Stop if py_compile fails for the inspected benchmark files.
- Stop if classification would require route-internal edits before a reviewed
  implementation subplan.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the P02 phase result.
3. Draft or refresh P03 if a microprobe is needed, otherwise draft or refresh
   P04 closeout.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
