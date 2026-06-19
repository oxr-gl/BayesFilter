# P8m Phase 1 Subplan: Transport Instrumentation Design

metadata_date: 2026-06-18
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 1

## Phase Objective

Design generic transport-core instrumentation or microbenchmarking that can
separate Sinkhorn potential updates, final transport application, chunk
overhead, and whole-call timing without changing algorithm semantics.

## Entry Conditions Inherited From Previous Phase

- Phase 0 closed with generic boundary review.
- P8m remains implementation-neutral until the design is reviewed.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-result-2026-06-18.md`

## Required Checks/Tests/Reviews

```bash
rg -n "_filterflow_streaming_transport|_filterflow_streaming_sinkhorn_potentials|_filterflow_streaming_transport_from_potentials|batched_annealed_transport_core_tf" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

Claude review is required before implementation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the smallest generic instrumentation surface that can profile transport-core bottlenecks? |
| Baseline/comparator | Current streaming transport functions and P8l whole-call evidence. |
| Primary criterion | Design result names concrete artifacts, commands, fields, and tests for Phase 2 without requiring SIR-specific code. |
| Veto diagnostics | SIR-only data path, intrusive timing inside differentiable math, hidden semantic change, or inability to test finite/matched outputs. |
| Explanatory diagnostics | Code anchors, proposed benchmark shapes, timing fields. |
| Not concluded | No speedup, no optimization, no accepted iteration count. |

## Forbidden Claims/Actions

- Do not implement before design review.
- Do not add SIR callbacks to the transport microbenchmark.
- Do not instrument by adding side-effect timing inside compiled differentiable
  math unless the design justifies it.

## Exact Next-Phase Handoff Conditions

Phase 2 may proceed only if the design identifies a generic benchmark or
instrumentation route with focused checks.

## Stop Conditions

Stop if the only feasible profiling route is SIR-specific or would change
algorithm outputs.
