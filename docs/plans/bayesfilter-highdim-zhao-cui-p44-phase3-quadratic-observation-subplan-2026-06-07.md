# P44-M3 Subplan: Quadratic Observation Multimodality Stress

metadata_date: 2026-06-07
phase: P44-M3

## Decision Target

Test a same-target nonlinear additive-Gaussian observation model:

```text
x_t = rho x_{t-1} + eta_t
y_t = x_t^2 + epsilon_t
```

This model stresses posterior multimodality and symmetric observation maps.

## Evidence Contract

Baseline: dense quadrature refinement on tiny horizons.

Primary criteria:

- dims 1, 2, and 3 value and diagnostic score checks for CUT4 and Zhao--Cui
  against dense reference;
- explicit multimodality diagnostic, such as symmetric mode coverage on scalar
  fixtures;
- dense reference demonstrates symmetric-mode coverage before any CUT4 or
  Zhao--Cui comparison is interpreted;
- at least five deterministic directional score checks per dimension.

Veto diagnostics:

- a one-mode approximation is promoted as full target correctness;
- dense grid misses the symmetric mode;
- score checks are performed near a symmetry-induced stationary point without
  absolute and directional tolerances;
- CUT4 point count exceeds the phase cap.

Resource cap:

- the tiny-fixture CUT4 augmented dimension must stay at or below 6 unless the
  M3 result note records a separate reviewed cap;
- any individual focused M3 test command expected to exceed five minutes must
  create a separate experiment plan with wall-time, memory, and early-stop
  rules before execution.

## Implementation Sketch

1. Start with scalar `T=1`/`T=2` fixtures and symmetric observations.
2. Add independent product-panel dims 2 and 3.
3. Use dense quadrature refinement as the reference.
4. Demonstrate symmetric-mode coverage in the dense reference before comparing
   CUT4 and Zhao--Cui values and diagnostic gradients.
5. Record whether failures are quadrature-order, TT-fit, or approximation
   failures rather than scientific failures.

## Claim Boundary

This phase is a same-target nonlinear stress diagnostic. It does not prove
global posterior recovery for long horizons.
