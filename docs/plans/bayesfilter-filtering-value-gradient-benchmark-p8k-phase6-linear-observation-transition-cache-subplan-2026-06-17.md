# P8k Phase 6 Subplan: Linear-Observation And Transition-Cache Design

metadata_date: 2026-06-17
status: DRAFT_NOT_LAUNCHED_PHASE5_STOP
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 6

## Current Launch Disposition

Phase 5 did not satisfy this subplan's entry condition.  The matched trusted-GPU
history-mode comparison preserved log likelihoods but did not show a material
runtime or memory benefit, and therefore did not provide a reviewed engineering
reason to continue.  Do not launch Phase 6 under the current P8k runbook unless
the entry condition is revised and reviewed, or independent bottleneck evidence
is added.

## Phase Objective

Design and, only if justified by Phase 5, implement generic opt-in fast paths
for constant linear observations and transition/prior-mean reuse.

## Entry Conditions Inherited From Previous Phase

- Phase 5 identified a generic bottleneck that these designs could address.
- The implementation remains opt-in and does not change defaults.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase6-linear-observation-transition-cache-result-2026-06-17.md`
- If implementation occurs, focused tests and diff summary.

## Required Checks/Tests/Reviews

Design-only check:

```bash
rg -n "observation_fn|observation_jacobian_fn|prior_mean_fn|pre_flow_step_fn|transition_log_density_fn" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

If implementation is authorized by the Phase 6 design:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q -k "linear or cache or streaming"
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

Claude review is required before implementation and again after material
implementation diffs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are constant-linear observation and transition-cache fast paths generic, safe, and worth implementing now? |
| Baseline/comparator | Current callback route that recomputes observation Jacobians and transition means through generic callbacks. |
| Primary criterion | Design result classifies each candidate as implement-now, defer, or reject with explicit tests and boundaries. |
| Veto diagnostics | SIR-only shortcut, changed callback semantics, stale transition cache across time/particles, broken gradients, or default-policy change. |
| Explanatory diagnostics | Code anchor inventory and Phase 5 bottleneck evidence. |
| Not concluded | No speedup unless benchmarked in Phase 5-style trusted GPU run, no scientific adequacy. |

## Forbidden Claims/Actions

- Do not implement a SIR-only selector as an engine path.
- Do not cache stochastic noise or random draws.
- Do not change gradient-bearing semantics without focused gradient tests.

## Exact Next-Phase Handoff Conditions

Phase 7 may proceed if Phase 6 writes a reviewed decision and any implemented
path passes focused checks.

## Stop Conditions

Stop if a proposed fast path is not generic, if correctness tests cannot be
specified, or if Phase 5 does not justify further implementation.
