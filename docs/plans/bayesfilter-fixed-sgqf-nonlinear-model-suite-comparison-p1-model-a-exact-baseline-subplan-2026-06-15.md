# P1 Subplan: Fixed-SGQF Model A Exact Baseline Integration

metadata_date: 2026-06-15
phase: P1
status: EXECUTION_READY

## Purpose

Add fixed SGQF as a peer backend to the existing nonlinear benchmark harness on
Model A, where exact Kalman remains the authoritative reference.

## Governing Master Program

`docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`

## Evidence Contract

Question:
- How does fixed SGQF level 2 compare to cubature / UKF / CUT4 on the affine
  Gaussian oracle when exact Kalman is available?

Primary pass criterion:
- fixed SGQF rows are emitted using the same benchmark schema as the existing
  nonlinear backends,
- exact-reference parity fields are recorded consistently.

## Execution Steps

1. Add fixed SGQF value rows to the benchmark harness for Model A.
2. Reuse exact Kalman reference logic already present in the harness.
3. Emit rows with point count, timing, exact-reference errors, and branch
   diagnostics.

## Exit Criteria

`PASS_P1_FIXED_SGQF_MODEL_A_INTEGRATED`
