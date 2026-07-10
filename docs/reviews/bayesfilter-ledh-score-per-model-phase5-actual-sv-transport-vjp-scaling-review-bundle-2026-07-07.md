# Claude Read-Only Review Bundle: Phase 5 Actual-SV Transport VJP Scaling

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is read-only reviewer only.

## Objective

Review whether the Phase 5 transport VJP scaling subplan is boundary-safe after
the value-score-only `T=20,N=1024` diagnostic showed the single no-tape reverse
pass is itself a runtime/memory blocker.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-full-row-scaling-repair-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-transport-vjp-scaling-subplan-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-visible-execution-ledger-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`

## Evidence Summary

- Same-forward-scalar streaming-flow parity is repaired at tiny scale.
- Coordinate-FD `T=20,N=1024` was interrupted after long runtime and near-budget
  GPU memory.
- Value-score-only `T=20,N=1024` was also interrupted after long runtime and
  near-budget GPU memory.
- Both tracebacks identify the manual streaming finite transport total pullback
  and its column-normalizer / softmin VJP internals as the blocker.
- Full `N=10000,T=1000` score remains not admitted.

## Boundary Requirements

The next phase must not:

- run full `N=10000,T=1000`;
- use `GradientTape`, `ForwardAccumulator`, hidden autodiff, or stopped partials;
- switch to stopped-scale/stabilized derivative as admission evidence without a
  reviewed target-derivative contract change;
- change the forward scalar or transport primal;
- promote runtime/memory diagnostics into correctness or admission evidence;
- broaden validator semantics without a separate strict artifact contract.

## Review Questions

1. Is it correct to target the transport VJP total-pullback implementation
   rather than rerunning larger actual-SV ladders?
2. Does the subplan preserve same-forward-scalar and no-tape constraints?
3. Does it correctly forbid stopped-scale/partial derivative shortcuts unless a
   reviewed contract explicitly changes the target derivative?
4. Are the tiny standalone transport VJP diagnostics and candidate comparison
   sequence logically ordered?
5. Is this subplan boundary-safe to execute?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
