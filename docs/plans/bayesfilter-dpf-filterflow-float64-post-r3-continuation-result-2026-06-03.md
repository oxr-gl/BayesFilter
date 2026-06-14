# Result: FilterFlow Float64 Post-R3 Continuation

## Decision

`filterflow_float64_post_r3_continuation_pass`

## Evidence

The refreshed continuation ladder now consumes the no-runtime-shim float64 R3
trace/replay helper and reports:

- Top-level continuation decision:
  `filterflow_float64_continuation_no_mismatch_observed`.
- First failing cell: none observed.
- First blocked cell: none observed.
- Active FilterFlow reference commit:
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.

## Rung Summary

| Rung | Status | Key Delta |
| --- | --- | --- |
| `R0_controlled_1d_T2` | pass | scalar `0.0`, max field `1.1102230246251565e-16` |
| `R1_controlled_1d_T4` | pass | scalar `0.0`, max field `4.440892098500626e-16` |
| `R2_filterflow_observation_path_T100` | pass | scalar `0.0`, max field `2.9103830456733704e-11` |
| `R3_filterflow_initial_particles_T100` | pass | scalar `0.0`, max field `1.1102230246251565e-14` |
| `R4_filterflow_2d_trace_replay` | pass | particles `0.0`, log weights `2.572270396683507e-09`, log likelihoods `1.5979679801603197e-09` |

## Interpretation

The previous R4 blocker is closed. In the bounded continuation ladder,
BayesFilter matches the local float64 FilterFlow reference through scalar 1D
value replay, the executable FilterFlow observation path, executable initial
particles, and the 2D proposal/transport trace replay.

The next smallest unresolved axis is not another trace replay rung. It is to
compare BayesFilter against the executable FilterFlow full `pf(...)` output for
the same 2D constant-velocity setting without forcing proposal particles from
the trace. That would test whether remaining differences enter through random
stream handling, full `tf.data`/SMC execution semantics, or scalar aggregation
outside the controlled replay.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-plan-2026-06-03.md`
- Refreshed continuation result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-result-2026-06-03.md`
- Refreshed continuation JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_continuation_debug_2026-06-03.json`

## Non-Implications

- No mathematical correctness claim.
- No posterior correctness claim.
- No gradient correctness claim.
- No production BayesFilter claim.
- No paper-authority claim.
- No full smoothness-surface alignment claim.
