# Claude Read-Only Review Bundle: Phase 5 Actual-SV Scaling Repair

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is read-only reviewer only.

## Objective

Review whether the Phase 5 actual-SV full-row scaling repair subplan is
boundary-safe after the repaired route passed tiny parity/FD but the
`T=20,N=1024` all-coordinate FD ladder rung was interrupted for runtime/memory
pressure.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-full-row-score-refresh-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-full-row-scaling-repair-subplan-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-visible-execution-ledger-2026-07-07.md`
- `bayesfilter/highdim/ledh_score_contract.py`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`

## Evidence Summary

The streaming-flow parity repair passed tiny checks. The full-row refresh then
ran a reviewed GPU ladder:

- `T=5,N=256` passed as non-admission diagnostic evidence;
- `T=20,N=1024` was manually interrupted after roughly 15 minutes;
- GPU memory was near budget during the interrupted rung;
- traceback showed execution inside the manual streaming finite transport total
  pullback, not a forward-scalar parity failure.

Current score validator admits correctness only as:

```text
same_scalar_finite_difference
exact_reference
```

Therefore the next phase must not simply rerun full all-coordinate FD. It must
either make correctness feasible through instrumentation/checkpointing or
define a reviewed strict exact-reference route.

## Review Questions

1. Is it correct to block full actual-SV score admission on the current
   runtime/memory scaling evidence?
2. Does the scaling repair subplan avoid promoting timing/memory probes to
   correctness or admission evidence?
3. Does it preserve no-tape, same-target, same-algorithm, and validator
   boundaries?
4. Is it correct that any `exact_reference` route or validator-semantics change
   needs a separate reviewed strict artifact contract?
5. Is this subplan boundary-safe to execute?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
