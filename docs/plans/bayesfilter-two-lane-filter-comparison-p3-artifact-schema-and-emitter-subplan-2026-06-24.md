# Phase P3 Subplan: Artifact Schema And Emitter Design

metadata_date: 2026-06-24
status: DRAFT_PENDING_P2_CLOSEOUT
master_program: docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md
phase: P3
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Design the durable artifact schema for the two-lane leaderboard outputs so that
accuracy tables, timing tables, blocker/status tables, and nonclaims are all
represented explicitly and cannot collapse back into one misleading table.

## Entry Conditions Inherited From Previous Phase

- P2 result must freeze the high-dimensional lane.
- The benchmark governance backbone still controls machine-readable row and
  algorithm semantics.

## Required Artifacts

- Phase P3 result:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p3-artifact-schema-and-emitter-result-2026-06-24.md`
- Refreshed Phase P4 subplan:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p4-execution-protocol-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

Design checks:

```bash
rg -n "not_performance_evidence|value_error_matrix|gradient_error_matrix|status_matrix|two_lane_comparison_contract" \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json \
  docs/plans/bayesfilter-two-lane-filter-comparison-p3-artifact-schema-and-emitter-subplan-2026-06-24.md -S
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the leaderboard outputs be emitted as separate lowdim/highdim accuracy tables, timing tables, blocker tables, and nonclaims without misreading status artifacts as rankings? |
| Baseline/comparator | Existing preflight/P8 matrix schema and the two-lane comparison contract. |
| Primary pass criterion | The output schema explicitly separates lane, metric family, rankability, blocker status, and nonclaims. |
| Veto diagnostics | One output table mixes lowdim and highdim, timing is not separated from accuracy, or blocker rows are forced into rankable tables. |
| Explanatory diagnostics | Schema field inventory and emitter design notes. |
| Not concluded | No executed leaderboard yet. |
| Artifact preserving result | P3 result and refreshed P4 subplan. |

## Required Output Families

P3 must define durable output families for:
- low-dimensional accuracy table,
- low-dimensional timing table,
- high-dimensional accuracy table,
- high-dimensional timing table,
- blocker/status table,
- nonclaims section,
- optional Pareto/tradeoff summary if justified later.

## Stop Conditions

Stop with a blocked P3 result if the schema still permits one merged overall
leaderboard or if blocker rows cannot be represented durably.
