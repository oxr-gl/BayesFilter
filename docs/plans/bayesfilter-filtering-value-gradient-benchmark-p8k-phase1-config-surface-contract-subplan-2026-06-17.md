# P8k Phase 1 Subplan: Generic Configuration Surface Contract

metadata_date: 2026-06-17
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 1

## Phase Objective

Define the generic opt-in configuration surface before any implementation
changes.  The contract must cover both engine-level options and benchmark
harness options.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result passed or explicitly authorized this phase.
- P8k remains generic and configurable.
- P8j actual-SIR remains a downstream stress case only.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-result-2026-06-17.md`
- Updated execution ledger and stop handoff.

## Required Checks/Tests/Reviews

```bash
rg -n "def streaming_batched_ledh_pfpf_ot_value_core_tf|def batched_ledh_flow_streaming_particles_tf|return_history|skip_transport_when_no_active|transport_plan_mode|row_chunk_size|col_chunk_size|particle_chunk_size|sinkhorn_iterations" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
rg -n "--return-history|--transport-policy|--sinkhorn-iterations|--row-chunk-size|--col-chunk-size|--particle-chunk-size|--tf32-mode|--proposal-mode" docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

Claude review is required for the Phase 1 result and Phase 2 subplan before
implementation begins.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What generic knobs are safe to expose or repair before GPU profiling? |
| Baseline/comparator | Current function signatures and benchmark CLI arguments. |
| Primary criterion | Result artifact lists each approved knob, owner surface, default behavior, required tests, and forbidden claim. |
| Veto diagnostics | A knob is SIR-specific, changes defaults silently, or lacks a test/artifact route. |
| Explanatory diagnostics | Inventory of current knobs and missing plumbing. |
| Not concluded | No implementation, performance, statistical adequacy, or production readiness. |

## Required Configuration Contract

The Phase 1 result must classify:

- `return_history` or `diagnostic_level`;
- `skip_transport_when_no_active`;
- `transport_plan_mode`;
- `transport_policy`;
- `sinkhorn_iterations`;
- `sinkhorn_epsilon`;
- `row_chunk_size`;
- `col_chunk_size`;
- `particle_chunk_size`;
- `tf32_mode`;
- optional future `linear_observation_matrix`;
- optional future transition/prior-mean cache surface.

## Forbidden Claims/Actions

- Do not implement code before the contract is written.
- Do not change defaults.
- Do not run long benchmarks.
- Do not claim that a configuration knob is validated merely because it exists.

## Exact Next-Phase Handoff Conditions

Phase 2 may proceed only if Phase 1 records a concrete implementation checklist
for harness plumbing and focused tests.

## Stop Conditions

Stop if the contract cannot distinguish generic engine controls from
SIR-specific callbacks, or if a required default change appears necessary.
