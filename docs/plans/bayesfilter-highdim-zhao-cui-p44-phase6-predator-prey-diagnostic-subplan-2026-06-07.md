# P44-M6 Subplan: Predator-Prey Diagnostic Closure

metadata_date: 2026-06-07
phase: P44-M6

## Decision Target

Create a small predator-prey diagnostic closure for CUT4 and Zhao--Cui while
preserving the existing nonclaims around nonlinear preconditioning usefulness.

## Evidence Contract

Baseline: current predator-prey model-contract tests and matched diagnostic
closure fixtures.

Primary criteria:

- finite value and diagnostic gradient for CUT4 and any matched Zhao--Cui
  diagnostic target;
- explicit fair-comparison settings if linear versus nonlinear preconditioning
  is touched;
- no promotion from raw ESS, wall time, or trajectory plots alone.

Veto diagnostics:

- unmatched budgets or parameter settings;
- ODE domain failure or nonfinite likelihood;
- cost-free ESS promotion;
- diagnostic closure described as paper-scale predator-prey validation.

Resource and stop caps:

- overnight execution is limited to the existing two-state predator-prey
  fixture, one-step or `T <= 2` diagnostic closures, CPU-only tests, and CUT4
  augmented dimension `<= 6`;
- any fair preconditioning comparison, larger trajectory, or paper-scale row
  requires a separate phase-specific experiment plan and Claude pass;
- if matched closure targets are unavailable, record
  `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM` and do not run equality comparisons.

## Implementation Sketch

1. Reuse `p30_predator_prey_fixture_model`.
2. Define a tiny additive-Gaussian closure with fixed observations.
3. Compare only matched targets, or record `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM`.
4. Keep nonlinear preconditioning claims blocked unless a separate fair
   comparison phase is reviewed.

## Claim Boundary

Diagnostic-only for CUT4/Zhao--Cui comparison unless a later native target and
fair comparison evidence contract is approved.
