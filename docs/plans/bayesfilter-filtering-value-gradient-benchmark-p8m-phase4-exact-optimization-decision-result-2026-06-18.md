# P8m Phase 4 Result: Exact Optimization Decision

metadata_date: 2026-06-18
status: DEFER_EXACT_IMPLEMENTATION_REPAIR_USE_1024_AS_CANDIDATE
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Defer exact transport implementation repair.  Phase 3 identifies a generic configuration candidate, not a code-level exact-route defect. |
| Primary criterion status | Passed.  The result classifies candidate action as defer implementation, keep 1024 as a configurable benchmark candidate, and reject 4096 for the tested synthetic shape. |
| Veto diagnostic status | No approximate transport mislabeled as exact, no SIR-specific shortcut, no default change, and no code implementation in Phase 4. |
| Main uncertainty | Full-filter behavior may have additional overhead not present in the synthetic transport-core benchmark. |
| Next justified action | Close P8m or start a separate validation/confirmation lane if the user wants full-filter confirmation of chunk 1024. |
| What is not concluded | No implementation success, default change, cross-model speedup, full-filter speedup, particle adequacy, exact likelihood correctness, HMC/NUTS readiness, or production readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a generic exact-route implementation change worth making now? |
| Baseline/comparator | Phase 3 chunk ladder and current transport code anchors. |
| Primary criterion | Result classifies candidate as implement, defer, or reject and lists exact tests required. |
| Veto diagnostics | Approximate transport mislabeled as exact, SIR-specific shortcut, changed outputs without validation, or untestable gradient/shape behavior. |
| Explanatory diagnostics | Code anchors, expected complexity change, benchmark evidence. |
| Not concluded | No implementation success until Phase 5 checks pass. |

## Checks Run

```bash
rg -n "_filterflow_streaming_logsumexp|_filterflow_streaming_sinkhorn_potentials|_filterflow_streaming_transport_from_potentials|_filterflow_streaming_transport|_filterflow_streaming_softmin|_filterflow_streaming_column_log_normalizer" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
git diff --check -- docs/benchmarks/benchmark_p8m_transport_core_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

Results:

- code-anchor inventory passed;
- `git diff --check` passed.

## Decision Rationale

Phase 3 evidence:

- chunk 1024 warm mean: 0.293063 seconds, peak memory counter 84433920 bytes;
- chunk 2048 warm mean: 0.295725 seconds, peak memory counter 211000320 bytes;
- chunk 4096 warm mean: 0.809180 seconds, peak memory counter 715791360 bytes.

Interpretation:

- 1024 and 2048 are tied on synthetic warm runtime for this shape;
- 1024 has substantially lower reported peak memory than 2048;
- 4096 is slower and memory-heavy, so reject it for this shape;
- this does not identify a code-level defect or a small exact implementation
  repair.

## Classification

| Candidate | Classification | Reason |
| --- | --- | --- |
| Set chunk 1024 as future benchmark candidate | `defer_default_change_candidate_config` | Useful memory profile and tied runtime, but not enough for default change. |
| Implement exact streaming transport code repair now | `defer` | No specific exact-route code defect or safe minimal code change was identified. |
| Use chunk 4096 for this shape | `reject_for_tested_shape` | Slower and much higher memory in Phase 3. |
| Lower Sinkhorn iterations or change epsilon | `out_of_phase_validation_required` | This is tuning/validation, not exact implementation repair. |
| Approximate/top-k/local transport | `out_of_scope_extension` | Not an exact implementation repair. |

## Phase 5 Handoff Decision

Phase 5 exact implementation repair is not launched.  Its entry condition
requires an implement-now exact repair with focused tests; Phase 4 does not
identify one.

If future evidence identifies a specific exact-route code defect or redundant
operation, Phase 5 can be refreshed and reviewed before implementation.

## Boundary

No code was changed in Phase 4.  No defaults were changed.  No GPU benchmark
was run in Phase 4.  No scientific or production claim is made.

## Next Suggested Action

Close P8m with Phase 7, or create a separate full-filter confirmation lane for
chunk 1024 if the user wants to test whether the synthetic memory advantage
translates to actual DPF workloads.
