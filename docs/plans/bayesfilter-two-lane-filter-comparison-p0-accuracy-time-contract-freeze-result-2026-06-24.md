# Phase Result: Two-Lane Comparison P0 Accuracy-Time Contract Freeze

metadata_date: 2026-06-24
plan_reference: `docs/plans/bayesfilter-two-lane-filter-comparison-p0-accuracy-time-contract-freeze-subplan-2026-06-24.md`
master_program: `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
status: PASS_P0_TWO_LANE_ACCURACY_TIME_CONTRACT_FROZEN

## Phase Objective

Freeze the exact accuracy/time leaderboard contract before any comparison table
is treated as evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for planning scope: the leaderboard contract is now explicitly two-lane, metric-separated, and blocker-aware |
| Primary criterion status | satisfied |
| Veto diagnostic status | no merged overall leaderboard remains in scope; CUT4 remains excluded from the high-dimensional lane; actual transformed SV and KSC surrogate SV remain separated |
| Main uncertainty | later phases still need actual execution artifacts and durable timing outputs |
| Next justified action | freeze row eligibility lane-by-lane in P1 and P2 |
| What is not concluded | no numeric ranking, no time winner, no performance result |

## Frozen Contract

P0 freezes the following:
- two distinct leaderboard lanes,
- separate accuracy and timing tables,
- explicit blocker/status tables,
- actual-vs-surrogate SV separation,
- SGQF autodiff remains diagnostic-only,
- CUT4 remains low-dimensional only,
- preflight/runner matrices remain governance and not performance evidence.

## Focused Grounding Used

The contract freeze was grounded against:
- `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-fixed-sgqf-promotion-closeout-and-two-lane-comparison-reset-memo-2026-06-23.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json`

## Audit Of Result Just Produced

P0 passes the skeptical audit because it does not pretend that governance
matrices are performance evidence, does not widen SGQF family admission, and
does not collapse the lane split into prose-only ambiguity.

## Next-Phase Review

P1 may proceed unchanged. Its current subplan already asks for row-by-row
low-dimensional rankability classification and same-target checks.

## Nonclaims

- No benchmark run was executed by P0.
- No algorithm was ranked by P0.
- No timing result was produced by P0.
