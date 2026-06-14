# P44-M5 Subplan: Spatial SIR Diagnostic Closure

metadata_date: 2026-06-07
phase: P44-M5

## Decision Target

Create a small spatial-SIR diagnostic closure for CUT4 and Zhao--Cui without
claiming native SIR TT/SIRT likelihood correctness.

## Evidence Contract

Baseline: SIR model-contract tests, RK4/small-step checks, and finite closure
diagnostics.

Primary criteria:

- finite value and diagnostic gradient for declared additive-Gaussian closure
  fixtures;
- explicit nonclaims recorded in test diagnostics and result ledger;
- no CUT4-versus-Zhao--Cui equality row unless M0/M5 identifies a matched
  shared closure target for both methods;
- no native SIR equality claim unless a later phase defines a shared native
  likelihood.

Veto diagnostics:

- negative populations silently accepted;
- closure diagnostics described as native SIR filtering;
- observed-only accuracy promoted as full state recovery;
- no source/model-contract anchor.

Resource and stop caps:

- overnight execution is limited to the smallest diagnostic SIR closure, with
  `J <= 1`, CPU-only tests, and CUT4 augmented dimension `<= 6`;
- any expansion to larger `J`, longer horizons, or paper-scale SIR requires a
  separate phase-specific experiment plan and Claude pass;
- if the closure target cannot be matched for both methods, record
  `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM` and do not run equality comparisons.

## Implementation Sketch

1. Reuse `SpatialSIRSSM` small fixtures.
2. Define a clean-room additive-Gaussian observation closure for CUT4.
3. Define the matched Zhao--Cui diagnostic target or explicitly block if no
   same target exists.
4. Test finite value/score and nonclaim metadata.

## Claim Boundary

Diagnostic-only unless a later reviewed common SIR likelihood target is
implemented.
