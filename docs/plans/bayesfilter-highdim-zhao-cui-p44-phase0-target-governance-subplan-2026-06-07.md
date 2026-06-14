# P44-M0 Subplan: Target Governance Matrix

metadata_date: 2026-06-07
phase: P44-M0

## Decision Target

Build the target-governance matrix for all P44 model families before any new
implementation work begins.

## Evidence Contract

Question: for each planned model, are CUT4, Zhao--Cui/fixed-design TT, and the
reference route evaluating the same likelihood and score target?

Primary criterion:

- every P44 phase receives one of these labels:
  - `SAME_TARGET_EXACT_OR_DENSE_REFERENCE`;
  - `SAME_TARGET_APPROXIMATION_WITH_EXPLICIT_REFERENCE_GAP`;
  - `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM`;
  - `BLOCKED_TARGET_UNSPECIFIED`.

Veto diagnostics:

- missing parameterization;
- missing observation/noise contract;
- missing horizon/dimension convention;
- comparing transformed and native targets without Jacobian accounting;
- using diagnostic closures as native-model evidence.

## Implementation Steps

1. Add a test-local or validation manifest row for each P44 phase.
2. Record state dimension, observation dimension, parameter vector, transform,
   and fixed parameters.
3. Record whether dimensions 2 and 3 are coupled or independent product panels.
4. Require the matrix schema to include these columns:
   - `phase_id`;
   - `model_family`;
   - `target_identity`;
   - `reference_route`;
   - `candidate_cut4_route`;
   - `candidate_zhao_cui_route`;
   - `parameterization`;
   - `fixed_parameters`;
   - `dimension_convention`;
   - `panel_structure`, with values `factorized_product`,
     `coupled_multivariate`, or `not_applicable`;
   - `claim_class`, using P42 Class A/B/C/D language;
   - `promotion_status`, using the labels in this subplan.
5. Require later phase tests to import or reproduce this matrix before any
   result can be promoted.

## Claude Gate

- Plan token: `PASS_P44_M0_PLAN_GOVERNANCE` or
  `BLOCKED_P44_M0_PLAN_GOVERNANCE`.
- Code/result token: `PASS_P44_M0_CODE_GOVERNANCE` or
  `BLOCKED_P44_M0_CODE_GOVERNANCE`.
