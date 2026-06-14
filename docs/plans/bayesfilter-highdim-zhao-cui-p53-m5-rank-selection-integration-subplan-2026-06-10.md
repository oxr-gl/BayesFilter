# P53-M5 Subplan: Rank Selection Integration

metadata_date: 2026-06-10
phase: P53-M5
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Integrate the admitted P53-M4D scaling route with the P52 rank-budget and UKF
scouting protocols.  This phase may not start unless P53-M4D emits
`PASS_P53_M4D_SCALING_ROUTE_ADMISSION`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can rank selection consume real scaling-route metadata and freeze a rank before HMC without adaptive branch changes? |
| Baseline/comparator | P52 rank-budget implementation, P52 UKF scout, P53-M4D admitted scaling-route metadata, and lower-rung tie-out evidence. |
| Primary pass criterion | Rank selection uses the scaling-route metadata, removes infeasible ranks before execution, records selected/block status, and forbids rank adaptation inside likelihood calls. |
| Veto diagnostics | Rank selection runs without `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`; route metadata absent; rank adapts inside likelihood; UKF promoted to truth; memory cap ignored. |
| Not concluded | Rank selection does not prove exact correctness or HMC readiness. |

## Planned Work

1. Wire the scaling-route metadata into the rank-budget protocol.
2. Add tests proving P53-M4D admission is a required prerequisite.
3. Add no-adaptive-rank mutation tests.
4. Emit a rank-selection manifest or blocker.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-result-2026-06-10.md`

Required token:

`PASS_P53_M5_RANK_SELECTION_INTEGRATION` or
`BLOCK_P53_M5_RANK_SELECTION_INTEGRATION`
