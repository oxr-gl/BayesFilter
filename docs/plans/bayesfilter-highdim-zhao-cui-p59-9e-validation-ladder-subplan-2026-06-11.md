# P59-9e Subplan: Validation Ladder

metadata_date: 2026-06-11
status: PLAN_DRAFT_FOR_CLAUDE_REVIEW

## Launch Gate

P59-9e must not run unless P59-9a, P59-9c, P59-9b, and P59-9d have pass
tokens.  Claude review cannot waive missing prerequisite artifacts; it can only
confirm that each prerequisite artifact exists and is source-faithful.

## Question

After Phase 9 preparation artifacts exist, what can be honestly concluded from
the d=18 author-SIR source-route run?

## Comparator Tiers

- `d18_execution_only`: may report finite values, ESS, replay, normalizer,
  rank, memory, and wall time.  It cannot claim accuracy.
- `d18_same_route_rank_convergence`: requires a strictly higher feasible
  fixed-TT/SIRT rank comparator on the same source route.  It can claim
  same-route stability, not exact correctness.
- `d18_correctness_candidate`: requires same-target reference evidence or a
  documented lower-rung-to-d18 bridge strong enough for the stated tolerance.

## Tasks

1. Run the d=18 source-route row with the declared tier.
2. Preserve all run-manifest fields: git status, command, environment, CPU/GPU
   status, seeds/frozen draws, wall time, artifact paths, source anchors,
   ranks, basis, ESS, normalizer, value diagnostics, gradient diagnostics where
   applicable, and nonclaims.
3. Attempt d=50 only after d=18 reaches at least
   `d18_same_route_rank_convergence`.
4. Attempt d=100 only after d=50 has non-veto scaling evidence and memory
   budget permits.

## Pass Criteria

Pass token is tier-specific:

- `PASS_P59_9E_D18_EXECUTION_ONLY`;
- `PASS_P59_9E_D18_SAME_ROUTE_RANK_CONVERGENCE`;
- `PASS_P59_9E_D18_CORRECTNESS_CANDIDATE`.

## Vetoes

- validation launched before 9a-9d;
- d=50/d=100 attempted before d=18 tier gate;
- UKF or memory used as correctness comparator;
- contract-double or synthetic TT/SIRT transports used as correctness evidence;
- old local/operator/all-grid route used for validation.

## Initial Token

`PLAN_P59_9E_VALIDATION_LADDER`
