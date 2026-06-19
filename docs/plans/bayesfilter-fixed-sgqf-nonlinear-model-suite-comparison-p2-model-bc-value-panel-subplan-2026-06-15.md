# P2 Subplan: Fixed-SGQF Model B/C Value Panel

metadata_date: 2026-06-15
phase: P2
status: EXECUTION_READY

## Purpose

Add fixed SGQF as a peer backend to the existing nonlinear Model B/C benchmark
panel under the same dense one-step Gaussian projection reference policy already
used by the harness.

## Governing Master Program

`docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`

## Evidence Contract

Question:
- How does fixed SGQF level 2 compare to cubature / UKF / CUT4 on Models B/C
  under the current dense one-step benchmark policy?

Primary pass criterion:
- fixed SGQF rows are emitted beside the existing algorithms,
- first-step dense projection errors are reported under the same semantics,
- no wording implies full exact nonlinear likelihood certification.

## Execution Steps

1. Add fixed SGQF level-2 value rows to the existing benchmark harness for
   Models B and C.
2. Reuse `dense_projection_first_step()` as already used by the harness.
3. Emit benchmark rows with point count, first-step errors, and timing.

## Exit Criteria

`PASS_P2_FIXED_SGQF_MODEL_BC_VALUE_PANEL_INTEGRATED`
