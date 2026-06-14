# P44-M4 Subplan: Nonlinear Additive-Gaussian Transition

metadata_date: 2026-06-07
phase: P44-M4

## Decision Target

Test same-target filtering when nonlinearity enters the transition:

```text
x_t = f(x_{t-1}; theta) + eta_t
y_t = H x_t + epsilon_t
```

with additive Gaussian transition and observation noise.

## Evidence Contract

Baseline: dense/sequential quadrature refinement on tiny horizons.

Primary criteria:

- dims 1, 2, and 3 value and diagnostic score checks for CUT4 and Zhao--Cui
  against dense/sequential reference;
- at least a two-horizon check, e.g. `T=2` and `T=4`, before any statement
  about error accumulation;
- at least five deterministic directional score checks per dimension.

Veto diagnostics:

- transition and observation targets differ across methods;
- horizon growth hides accumulated score error;
- reference refinement is absent;
- branch/floor/clipping events are not surfaced.

Resource and stop caps:

- overnight execution is limited to dims 1--3, horizons `T <= 4`, CPU-only
  tests, and CUT4 augmented dimension `<= 6`;
- any command expected to exceed five minutes or any expansion beyond those
  caps requires a phase-specific experiment plan with wall-time, memory, and
  early-stop rules;
- if the nested `c=0` LGSSM check fails, stop before nonlinear `c != 0` rows.

## Implementation Sketch

1. Use a bounded smooth nonlinear transition, e.g.
   `f(x)=rho*x + c*tanh(x)`, to avoid explosive fixtures.
2. Compare `c=0` against the LGSSM nested check.
3. Add nonlinear `c != 0` value and gradient checks.
4. Run horizon scaling diagnostics before expanding dimensions.

## Claim Boundary

This phase can diagnose same-target nonlinear transition behavior on tiny
fixtures. It does not prove large-horizon HMC readiness.
