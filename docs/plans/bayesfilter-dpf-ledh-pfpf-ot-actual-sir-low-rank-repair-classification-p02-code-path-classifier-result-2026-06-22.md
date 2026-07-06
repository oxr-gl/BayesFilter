# P02 Code-Path Classifier Result

Date: 2026-06-22
Status: `PASS_ROUTE_TIMING_ASYMMETRY_SUPPORTED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Source inspection supports `ROUTE_TIMING_ASYMMETRY_SUPPORTED`: P03 compared low-rank diagnostic-loop timing against streaming compiled-core timing. Combined with P01, the repair classification should preserve both route-performance and tuning/comparability/ESS lanes. |
| Primary criterion status | Passed: source anchors identify the streaming compiled timing path, low-rank diagnostic path, paired warm-ratio calculation, solver eager diagnostics, and wrapper label rules. |
| Veto diagnostic status | No missing source file, stale anchor, py_compile failure, or route-internal edit. |
| Main uncertainty | Source inspection does not prove compiled low-rank feasibility or future speedup; it only supports a route-performance repair lane as the next smallest discriminating implementation question. |
| Next justified action | Do not run the conditional microprobe. Write P03 `NOT_LAUNCHED_NOT_NEEDED`, then proceed to P04 closeout and next repair handoff. |
| What is not concluded | No speedup, compiled low-rank feasibility, route repair correctness, candidate freeze, posterior correctness, dense Sinkhorn equivalence, HMC readiness, default readiness, or statistical ranking. |

## Source Anchors

| Evidence | Anchor | Interpretation |
| --- | --- | --- |
| Low-rank route is called inside diagnostic loop | `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py:428` | Low-rank timing in P03 follows the diagnostic loop route and calls `low_rank_coupling_solver_resample_tf` per active step. |
| Diagnostic loop host sync before route decision | `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py:400` | The loop checks active masks through `.numpy()`, which is not an XLA-compiled low-rank full-route path. |
| Streaming compiled timing path exists | `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py:476` and `:481` | Streaming has `_run_streaming_compiled_core_timed` and an inner `@tf.function(jit_compile=True, reduce_retracing=True)` path. |
| P03 uses compiled streaming source | `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py:612` and `:617` | With `--streaming-timing-source compiled_core`, streaming timing uses compiled-core output while diagnostic-loop seconds are explanatory. |
| Warm-time ratio definition | `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py:785` to `:815` | The support ratio is streaming warm median divided by low-rank warm median, threshold `1.25`. |
| Low-rank solver scope is diagnostic | `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py:1` to `:7` | The solver declares diagnostic semantic-replacement scope and forbids dense Sinkhorn/default claims. |
| Low-rank diagnostics host-sync tensors | `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py:173` and `:194` to `:197` | Returned diagnostics use `.numpy()` and Python bool/int conversion. |
| Projection loop has Python break on tensor value | `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py:334` | Projection convergence uses `bool(... .numpy())`, a source-level barrier to direct XLA graph compilation. |
| Low-rank nonmaterialized provenance | `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py:164` to `:166` | Transport remains factor/nonmaterialized in the diagnostic route. |
| Wrapper freeze label requires both comparability and speed | `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py:588` to `:606` | `freeze-nominated` requires comparable, speed pass, low-rank provenance, and GPU/TF32 provenance; comparable-but-slow is a separate label. |
| Wrapper aggregate records no-freeze count | `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py:732` to `:741` | P03 aggregate no-freeze status is derived from row labels. |

## P02 Classifier

`ROUTE_TIMING_ASYMMETRY_SUPPORTED`

Reason:

- The streaming comparator in P03 has a compiled-core timing route.
- The low-rank route in P03 is timed through the diagnostic loop and diagnostic
  solver path.
- The low-rank solver contains multiple eager host-synchronizing diagnostics
  and a Python break condition on tensor values.
- Therefore, the comparable-but-slow rows can reasonably trigger a
  route-performance implementation repair plan.

This is not a speedup claim. It only says the current comparison is sufficient
to justify the next smallest route-performance repair question.

## Combined With P01

P01 found:

- 7 comparable-but-slow candidates with descriptive low-rank/streaming warm
  median ratio median `60.55817737444639`.
- 11 incomparable candidates.
- 2 ESS hard-vetoed candidates.

P02 adds:

- source-supported route timing asymmetry for the comparable-but-slow lane.

Together these support final classifier `BOTH_REPAIRS`, with a
route-performance-first next subplan because source inspection identifies a
specific implementation asymmetry to repair before more tuning or held-out
support.

## Local Checks

| Check | Result |
| --- | --- |
| Source anchor inspection | `PASS` |
| Wrapper label inspection | `PASS` |
| Benchmark syntax check | `PASS`: `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` |

## Handoff

Write P03 conditional microprobe result as `NOT_LAUNCHED_NOT_NEEDED`, then
proceed to:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p04-closeout-subplan-2026-06-22.md`

P04 must preserve the tuning/comparability/ESS lane even if the immediate next
implementation subplan is route-performance-first.
