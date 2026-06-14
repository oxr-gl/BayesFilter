# P44-M2 Subplan: Cubic Additive-Gaussian Observation

metadata_date: 2026-06-07
phase: P44-M2

## Decision Target

Test a clean nonlinear same-target model:

```text
x_t = rho x_{t-1} + eta_t
y_t = x_t + a x_t^3 + epsilon_t
```

with Gaussian initial, transition, and observation noise.

## Evidence Contract

Baseline: dense quadrature refinement on tiny horizons, with exact Kalman used
only for the `a=0` nested linear check.

Primary criteria:

- dims 1, 2, and 3 value agreement for CUT4 and Zhao--Cui against dense
  reference under the same nonlinear additive-Gaussian observation target;
- diagnostic score agreement in the same parameterization;
- at least five directional score checks per dimension;
- dense reference passes refinement before being used as comparator.

Veto diagnostics:

- CUT4 closure differs from the dense/Zhao--Cui likelihood target;
- dense reference has no refinement check;
- cubic coefficient transform mismatch;
- active floors or branch changes are not declared diagnostic-only.

## Implementation Sketch

1. Implement a test-local structural model for the cubic observation fixture.
2. Use tiny horizons first, e.g. `T=2`, then a small horizon extension only
   after local pass.
3. Use product-panel dims 1--3 unless a coupled target is explicitly added.
4. Compare value and diagnostic score for CUT4, Zhao--Cui, and dense reference.
5. Record approximation gaps rather than forcing exact equality when CUT4
   quadrature error is visible.
6. If visible CUT4 quadrature error exceeds the predeclared same-target
   tolerance, the row cannot promote as P42 Class A same-target numerical
   correctness.  It must be downgraded to an approximation-gap or
   diagnostic-only row with the observed gap reported.

## Claim Boundary

This phase can support same-target nonlinear Tier-1 local diagnostics. It does
not show long-horizon stability or HMC usefulness.
