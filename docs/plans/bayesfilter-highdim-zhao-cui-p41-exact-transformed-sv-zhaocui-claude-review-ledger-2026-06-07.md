# P41 Claude Review Ledger: Exact Transformed SV Zhao-Cui Ladder

metadata_date: 2026-06-07
phase: P41

## Plan Review Iteration 1

status: `PASS_P41_PLAN_GOVERNANCE`

Reviewer summary:
- Exact transformed `z=log(y^2)` log-chi-square is the primary target.
- Exact lanes forbid offsets except in the separate KSC diagnostic lane.
- Raw native SV is only compared after the Jacobian correction.
- KSC Kalman/CUT4 is consistently approximation-only.
- Dimensions 1, 2, and 3 are independent-product deterministic `T=2`
  fixtures.
- The Zhao--Cui panel lane is constrained to summed scalar fixed-design TT
  lanes and is not claimed as a coupled multivariate TT implementation.

## Code Review Iteration 1

status: `PASS_P41_CODE_GOVERNANCE`

Reviewer summary:
- The exact transformed `z=log(y^2)` log-chi-square lane is the governed
  primary target in plan and implementation.
- Exact lanes use no offset and reject zero observations.
- Raw native SV is compared only after the Jacobian correction
  `native = transformed - sum(log(abs(y)))`.
- KSC mixture Kalman/CUT4 remains a separate approximation-only comparator.
- Dimension 1, 2, and 3 fixtures are deterministic independent-product `T=2`
  panels.
- The Zhao--Cui panel lane is a factorized sum of scalar fixed-design TT lanes,
  with explicit non-claims against coupled multivariate TT.
- New exports remain highdim-only.

Response:
- No code changes were required after Claude review iteration 1.
