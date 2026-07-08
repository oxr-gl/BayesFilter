# Phase Result: Two-Lane Comparison P4 Execution Protocol

metadata_date: 2026-06-24
plan_reference: `docs/plans/bayesfilter-two-lane-filter-comparison-p4-execution-protocol-subplan-2026-06-24.md`
master_program: `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
status: PASS_P4_TWO_LANE_EXECUTION_PROTOCOL_FROZEN

## Phase Objective

Freeze the first-pass execution protocol for the leaderboard program.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for the initial overnight pass: the execution environment and timing policy are now explicit enough to support honest first-pass runs |
| Primary criterion status | satisfied |
| Veto diagnostic status | no mixed lane timing policy remains; no preflight/smoke artifact is treated as leaderboard evidence |
| Main uncertainty | low-dimensional and high-dimensional execution still require harnesses that populate the frozen output families for all intended algorithms/rows |
| Next justified action | begin low-dimensional execution in P5 |
| What is not concluded | no performance leaderboard result yet |

## Frozen First-Pass Protocol

The initial overnight pass freezes:
- CPU-only execution with `CUDA_VISIBLE_DEVICES=-1` unless a later reviewed GPU lane is explicitly opened,
- timing reported as first-call and steady-call means where the harness supports it,
- warmup/repeat policy must be recorded in the run manifest,
- stochastic methods require explicit seed accounting,
- every output row must retain lane, target identity, and blocker/status provenance.

## Audit Of Result Just Produced

P4 passes the skeptical audit for an initial reference pass because it avoids
silently mixing CPU and GPU timing and does not overclaim production-target
performance from unreviewed GPU behavior. It remains a reference timing policy,
not a production-GPU claim.

## Next-Phase Review

P5 may proceed, but it should prefer an existing benchmark harness only where it
matches the frozen low-dimensional lane exactly. If not, a dedicated lowdim
leaderboard harness is required.

## Nonclaims

- This is not a production-GPU timing conclusion.
- No final computation-time leaderboard exists yet.
