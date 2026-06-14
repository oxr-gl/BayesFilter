# P40 Claude Review Ledger: SV Kalman--CUT4--Zhao-Cui Tests

metadata_date: 2026-06-07
phase: P40

## Plan Review Iteration 1

status: `BLOCKED_P40_PLAN_GOVERNANCE`

Reviewer summary:
- The plan treated the existing P39 dense transformed-mixture reference as a
  primary exact baseline instead of a secondary comparator.
- The `7^d` component enumeration needed to be pinned to tiny deterministic
  `T=2` fixtures.
- The independent-panel dimension convention needed explicit factorized
  observation and diagonal dynamics language.
- CUT4 exactness non-claims needed to be repeated in the implementation steps.

Response:
- Made the component-enumerated Kalman-mixture oracle the only primary exact
  reference.
- Demoted the P39 dense scalar reference to a secondary corroborating
  comparator.
- Pinned dimensions 1, 2, and 3 to independent-product transformed-mixture SV
  panels on tiny deterministic `T=2` fixtures.
- Added explicit non-claim language that the ladder validates Gaussian
  component reduction, bookkeeping, and collapse, not nonlinear CUT4 accuracy.

## Plan Review Iteration 2

status: `PASS_P40_PLAN_GOVERNANCE`

Reviewer summary:
- The Kalman-mixture oracle is now the only primary exact reference.
- P39 dense scalar reference is explicitly secondary.
- Dimensions 1, 2, and 3 are pinned to tiny independent-product
  transformed-mixture `T=2` fixtures.
- CUT4 non-claims and generalized SV boundaries are explicit enough.

## Code Review Iteration 1

status: `PASS_P40_CODE_GOVERNANCE`

Reviewer summary:
- The sole primary exact oracle is the component-enumerated Kalman-mixture
  reference; the dimension 1/2/3 tests use it as the primary comparator.
- Dimensions 1, 2, and 3 are pinned to tiny deterministic `T=2`
  independent-product fixtures, with `7**dim` component enumeration asserted.
- CUT4 agreement is bounded by explicit non-claims, including the statement
  that linear-Gaussian component fixtures do not validate nonlinear CUT4
  accuracy.
- Existing Zhao--Cui/BayesFilter SV coverage remains scalar-only, and the
  dimension 2/3 tests exercise the scalar-lane rejection instead of silently
  routing through it.
- Generalized SV coverage remains diagnostic/approximate only; the
  moment-matched comparator is labeled non-exact and no equivalence is claimed.
- New symbols remain scoped to `bayesfilter.highdim` with a no-top-level-export
  test.

Response:
- No code changes were required after Claude review iteration 1.
