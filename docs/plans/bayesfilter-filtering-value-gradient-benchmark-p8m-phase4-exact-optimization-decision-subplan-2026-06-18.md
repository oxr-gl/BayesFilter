# P8m Phase 4 Subplan: Exact Optimization Decision

metadata_date: 2026-06-18
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 4

## Phase Objective

Decide whether exact transport implementation repair is justified by Phase 3
evidence, and if so, define the smallest safe change.

## Entry Conditions Inherited From Previous Phase

- Phase 3 writes trusted-GPU profiling artifacts.
- Candidate bottleneck is generic and exact-route preserving.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase4-exact-optimization-decision-result-2026-06-18.md`

## Required Checks/Tests/Reviews

```bash
rg -n "_filterflow_streaming_logsumexp|_filterflow_streaming_sinkhorn_potentials|_filterflow_streaming_transport_from_potentials|_filterflow_streaming_transport" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

Claude review is required before any implementation repair.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a generic exact-route implementation change worth making now? |
| Baseline/comparator | Phase 3 chunk ladder and current transport code anchors. |
| Primary criterion | Result classifies candidate as implement, defer, or reject and lists exact tests required. |
| Veto diagnostics | Approximate transport mislabeled as exact, SIR-specific shortcut, changed outputs without validation, or untestable gradient/shape behavior. |
| Explanatory diagnostics | Code anchors, expected complexity change, benchmark evidence. |
| Not concluded | No implementation success until Phase 5 checks pass. |

## Forbidden Claims/Actions

- Do not implement in Phase 4.
- Do not choose approximate/top-k/local transport as an exact repair.
- Do not change defaults.

## Exact Next-Phase Handoff Conditions

Phase 5 may proceed only if Phase 4 identifies a small exact implementation
repair with focused tests.

## Stop Conditions

Stop if there is no safe exact repair or if only approximate/tuning changes are
promising.
