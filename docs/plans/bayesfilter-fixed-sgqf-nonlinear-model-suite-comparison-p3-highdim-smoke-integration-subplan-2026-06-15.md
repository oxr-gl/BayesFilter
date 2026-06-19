# P3 Subplan: Fixed-SGQF High-Dimensional Smoke Integration

metadata_date: 2026-06-15
phase: P3
status: EXECUTION_READY

## Purpose

Integrate fixed SGQF into the existing high-dimensional nonlinear smoke harness
where cubature / UKF / CUT4 are already recorded and CUT4 can hit point-count
caps.

## Governing Master Program

`docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`

## Evidence Contract

Question:
- How does fixed SGQF level 2 fit into the existing high-dimensional smoke
  diagnostic rows in terms of point count, runtime, and execution viability?

Primary pass criterion:
- fixed SGQF smoke rows are emitted where eligible,
- the harness records point-count/timing/finite-status under the same diagnostic
  schema,
- results remain explicitly diagnostic-only.

## Execution Steps

1. Add fixed SGQF rows to the smoke harness on Model B and/or block-replicated
   Model B rows.
2. Record point count and timing next to cubature / UKF / CUT4.
3. Preserve the current smoke non-implication wording.

## Exit Criteria

`PASS_P3_FIXED_SGQF_HIGHDIM_SMOKE_INTEGRATED`
