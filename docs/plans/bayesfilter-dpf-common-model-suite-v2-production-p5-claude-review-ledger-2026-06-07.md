# DPF Common Model Suite V2 P5 Claude Review Ledger

metadata_date: 2026-06-07
phase: P5
ledger_status: PASS_P5_GRADIENTS_READY_FOR_P6

## Round 7 Corrected P5 Result Governance Review

review_type: `P5_FD_DIAGNOSTIC_ONLY_RESULT_GOVERNANCE_REVIEW`

verdict: `PASS`

Summary:

- Claude reviewed the corrected P5 amendment, runner, JSON artifact, and result
  ledger after the FD diagnostic-only rerun.
- Claude found no material blocker and required no patches.
- P5 local result is `PENDING_CLAUDE_REVIEW` with five P5-ready rows
  `MATCHED`, SIR `CONTRACT_BLOCKED`, max BF/FF scalar delta `0.0`, and max
  BF/FF AD-gradient delta `0.0`.
- The range-bearing FD discrepancy remains preserved as diagnostic-only
  evidence and does not control row status or promotion.
- Inactive zero gradients for `sv_1d_h18_rich:sigma` and
  `structural_ar1_quadratic_h16:sigma` are derivation-backed under the frozen
  fixed-additive-innovation scalar, not FD-gated.
- Claude confirmed P5 may advance to P6 under the corrected contract.

## Round 5 FD Diagnostic-Only Contract Amendment Review

review_type: `P5_FD_DIAGNOSTIC_ONLY_CONTRACT_REVIEW`

verdict: `BLOCK`

Summary:

- Claude agreed with the user-directed correction that FD should not be a P5
  gate in ordinary AD-vs-FD comparisons.
- Claude blocked the first amendment draft because the disconnected-zero
  gradient repair still allowed FD-zero or FD-nonzero checks to decide
  promotion/veto status for inactive knobs.
- Required patch: supersede the older disconnected-zero FD guard wherever it
  acted as a promotion or veto condition, and handle disconnected gradients by
  predeclared contract classification, derivation, or reviewed exclusion.

## Round 6 FD Diagnostic-Only Contract Amendment Review

review_type: `P5_FD_DIAGNOSTIC_ONLY_CONTRACT_REVIEW_R2`

verdict: `PASS`

Summary:

- Claude confirmed FD is now diagnostic-only across the amendment and P5
  subplan.
- Row status and promotion depend on BF/FF scalar agreement, BF/FF AD-gradient
  agreement, and finiteness of executed scalar/AD values, not FD.
- The previous disconnected-zero FD guard is superseded to the extent it used
  FD-zero or FD-nonzero as a promotion/veto condition.
- Fixtures, scalar, branch, tolerances, comparators, `.localsource/filterflow`,
  and student-command boundaries remain unchanged.
- FD discrepancies remain preserved as explanatory evidence and non-claims are
  adequate.

## Round 1 Repair Amendment Review

review_type: `P5_DISCONNECTED_ZERO_GRADIENT_REPAIR_REVIEW`

verdict: `PASS`

Summary:

- Claude classified disconnected AD `None` gradients for inactive knobs as an
  acceptable implementation-encoding repair, not a scientific-contract change.
- The repair is valid only when same-implementation central finite difference
  is zero within the frozen tolerance.
- The implementation records `disconnected_zero_gradient_knobs` and vetoes
  `None` plus nonzero FD.

## Round 2 FD-Ladder Amendment Review

review_type: `P5_RANGE_BEARING_FD_VETO_DIAGNOSTIC_REVIEW`

verdict: `PASS`

Summary:

- Claude approved adding an explanatory finite-difference ladder for the
  range-bearing FD veto.
- The original `1e-5` FD step and `5e-5` tolerance remained the primary veto.
- The ladder was explicitly not allowed to promote P5.

## Round 3 Blocked Result Review

review_type: `P5_BLOCKED_RESULT_GOVERNANCE_REVIEW`

verdict: `BLOCK`

Summary:

- P5 cannot pass because `range_bearing_4d_h20_rich` failed the primary
  AD-vs-FD self-check at the frozen `1e-5` step.
- BF/FF scalar agreement and BF/FF AD-gradient agreement were exact within
  recorded precision for every executed row.
- SIR remained `CONTRACT_BLOCKED` as required by P1.
- Claude denied promotion to P6 and recommended a separate reviewed
  scale-aware or analytic diagnostic if continuing self-recovery.

## Round 4 Scale-Aware Diagnostic Amendment Review

review_type: `P5_RANGE_BEARING_SCALE_AWARE_DIAGNOSTIC_REVIEW`

verdict: `PASS_FOR_EXECUTION_AS_SELF_RECOVERY_DIAGNOSTIC`

Summary:

- Claude approved adding smaller explanatory ladder steps while keeping P5
  blocked.
- Required guardrails: no tolerance relaxation, no pass promotion, no
  reparameterization, no clipping, no one-sided FD substitution, no scalar or
  fixture changes, no `.localsource/filterflow` mutation, and no student
  implementation command.

## Superseded Round 3--4 P5 Evidence

Status: `SUPERSEDED_BY_USER_DIRECTED_FD_DIAGNOSTIC_ONLY_AMENDMENT`

The following Round 3--4 interpretation treated FD as a primary/veto condition.
It is retained as historical evidence but no longer controls P5 promotion after
the user clarified that FD is numerically unstable and must not be a gate.

## Current P5 Evidence

Artifact:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_gradients_2026-06-07.json`
- `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p5-fixed-branch-gradients-result-2026-06-07.md`

Observed status:

- `lgssm_2d_h25_rich`: `MATCHED`
- `sv_1d_h18_rich`: `MATCHED`
- `range_bearing_4d_h20_rich`: `MATCHED`
- `structural_ar1_quadratic_h16`: `MATCHED`
- `spatial_sir_j3_rk4`: `CONTRACT_BLOCKED`
- `predator_prey_rk4`: `MATCHED`

Key diagnostics:

- max BF/FF scalar delta: `0.0`
- max BF/FF AD-gradient delta: `0.0`
- range-bearing AD-vs-FD diagnostic delta at `1e-5`: `1.1556379445210041e-4`
- frozen FD diagnostic tolerance field retained: `5e-5`
- explanatory range-bearing ladder decreases to about `2.5282474780397024e-8`
  at step `1e-7`.
- inactive zero-gradient reasons are recorded for `sv_1d_h18_rich:sigma` and
  `structural_ar1_quadratic_h16:sigma` by fixed-branch scalar derivation, not
  by FD pass/fail.

Decision:

- Claude result/governance review returned `PASS`.
- P5 is closed as `PASS_P5_GRADIENTS_READY_FOR_P6`.
- Next allowed action: proceed to P6 retirement/regression.

Non-claims:

- This does not prove stochastic-filter gradient correctness.
- This does not prove range-bearing scientific correctness.
- This does not validate student repositories.
- This does not treat finite differences as a primary gradient oracle.
