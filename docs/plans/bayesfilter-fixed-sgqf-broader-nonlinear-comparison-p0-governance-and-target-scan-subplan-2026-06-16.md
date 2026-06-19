# P0 Subplan: Fixed-SGQF Broader Comparison Governance And Target Scan

metadata_date: 2026-06-16
phase: P0
status: EXECUTION_READY

## Purpose

Inventory the broader repo-wide **literature-backed** nonlinear model families
already present in the benchmark source-paper scope contract and classify where
fixed SGQF is a candidate for admission under the current lane semantics.

The three P44 debugging models and the horizon-4 P44 extension remain available
as engineering/debugging evidence only and are not part of the final
literature-facing leaderboard scope.

## Governing Master Program

`docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-master-program-2026-06-16.md`

## Evidence Contract

Question:
- Which registry families are candidate fixed-SGQF rows, and which are blocked
  under the current additive-state lane?

Primary pass criterion:
- produce a family-level admission table with `admit_exact`,
  `admit_dense_reference_only`, `diagnostic_only`, and
  `blocked_not_same_target` labels.

## Execution Steps

1. Read the target registry and deterministic coverage matrix.
2. Inventory family columns and their reference policies.
3. Classify each family against the current fixed-SGQF lane semantics.
4. Record the result in the broader closeout.

## Exit Criteria

`PASS_P0_FIXED_SGQF_BROADER_SCAN_COMPLETE`
