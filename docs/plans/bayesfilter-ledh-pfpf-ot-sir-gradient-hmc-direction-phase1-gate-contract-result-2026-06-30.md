# Phase 1 Result: SIR Gradient Evidence Contract

Date: 2026-06-30

Status: `PASS`

## Decision

Phase 1 passes.  The SIR gradient program now has a predeclared
HMC-direction gate that does not reuse the LGSSM exact-Kalman standard and does
not treat SIR regression FD as an exact oracle.

## Gate Contract

For each raw theta direction, after route checks pass, define:

```text
combined_se = sqrt(regression_slope_standard_error^2
                   + standard_error_of_batch_mean^2)
direction_scale = max(abs(regression_fd_slope), abs(manual_score), 1.0)
precision_pass = (2 * combined_se <= 0.25 * direction_scale)
```

A direction can be classified as `direction_pass` only if all route and
diagnostic prerequisites pass:

- material run is GPU/XLA/TF32;
- manual reverse score route is used;
- no dense/full transport autodiff is used;
- objective and score are finite;
- FD slope SE is finite;
- seed-gradient MCSE is finite and enters `combined_se`;
- row residual satisfies the predeclared phase threshold;
- `precision_pass` is true.

Then one of two pass arms must hold:

1. `abs(manual_score - regression_fd_slope) <= 2 * combined_se`;
2. `abs(manual_score - regression_fd_slope) <= 4 * combined_se` with a
   separate N/budget ladder certificate showing decreasing MCSE or decreasing
   row residual with no worsening of the gap, while `precision_pass` remains
   true.

Supportive labels do not create a pass:

- `near_equal_supportive` is reported when relative error to regression FD is
  below `1%`, using `max(abs(regression_fd_slope), 1.0)` as scale.
- `near_zero_direction` is reported when both manual and FD slopes are within
  `2 * combined_se` of zero.

For non-negligible directions, manual score and FD slope must have the same
sign.  Non-negligible means either absolute value exceeds `2 * combined_se`.

## Checks Run

Passed:

```bash
rg -n "manual-reverse|regression_slope_standard_error|standard_error_of_batch_mean|row_residual|expect-device-kind|tf32-mode" docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
```

Passed:

```bash
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-execution-ledger-2026-06-30.md docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-result-2026-06-30.md
```

## Claude Review

Claude review converged after three rounds.

- Round 1 found that `<1%` relative error against SIR regression FD was a
  standalone pass and that MCSE was only required to be finite.
- Round 2 found that a huge `combined_se` could turn unresolved disagreement
  into a pass.
- Round 3 returned `VERDICT: AGREE`.

Review ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

## Gate Status

Phase 1 gate: `PASSED`.

Exact next-phase handoff conditions:

- The gate is written with route checks, combined uncertainty, precision veto,
  sign sanity, supportive labels, and nonclaims.
- Claude review converged.
- Phase 2 now needs to implement/report the new gate fields in the SIR
  diagnostic.

## Nonclaims

- No exact SIR gradient proof.
- No posterior correctness.
- No nonlinear-model validation.
- No HMC/NUTS readiness.
- No claim that regression FD is exact truth.

## Next Action

Refresh Phase 2 so the diagnostic reporting plan explicitly includes
`combined_se`, `direction_scale`, `precision_pass`,
`inconclusive_precision_veto`, sign status, and supportive labels.
