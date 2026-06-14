# P44-M7 Subplan: Generalized SV Target Definition

metadata_date: 2026-06-07
phase: P44-M7

## Decision Target

Decide whether generalized SV can enter the CUT4/Zhao--Cui same-target ladder,
or whether it remains diagnostic-only.

Generalized SV form under discussion:

```text
y_t = beta s_t + exp(h_t / 2) epsilon_t
```

with latent states `(s_t, h_t)`.

Before value or gradient tests, M7 must fill this target-definition table:

| Field | Required content |
| --- | --- |
| `state_law_s` | transition law, innovation law, fixed/estimated parameters, and initial law for `s_t` |
| `state_law_h` | transition law, innovation law, fixed/estimated parameters, and initial law for `h_t` |
| `state_dependence` | whether `s_t` and `h_t` are independent a priori, correlated, or coupled |
| `observation_law` | exact density for `y_t | s_t,h_t,theta` |
| `target_route` | native, mixture, transformed-residual, moment-matched, or diagnostic-only |
| `parameterization` | unconstrained vector, transforms, ordering, and fixed parameters |
| `jacobian_terms` | required transform/Jacobian accounting, or `none` with justification |
| `reference_route` | dense, Kalman/mixture, SMC with uncertainty, or blocked |
| `claim_class` | P42 Class A/B/C/D |

## Evidence Contract

Question: can we define a shared target for CUT4 and Zhao--Cui that preserves
the generalized SV likelihood rather than only a transformed-residual
diagnostic?

Primary criteria:

- a written target decision before implementation;
- clear distinction between:
  - exact native generalized SV likelihood;
  - transformed-residual approximation;
  - Gaussian-mixture/KSC style approximation;
  - moment-matched Kalman diagnostic;
- value and gradient criteria if and only if a shared target is selected.

Veto diagnostics:

- transformed residual described as exact native likelihood;
- Gaussian mixture approximation described as exact;
- `s_t` and `h_t` independence assumptions used after the observation couples
  them without disclosure;
- no Jacobian/transform accounting.

Resource and stop caps:

- overnight execution may write the target-definition table and, at most, tiny
  finite diagnostic checks with dims 1--3, `T <= 2`, CPU-only tests, and CUT4
  augmented dimension `<= 6`;
- no same-target generalized-SV value/gradient equality test may run until the
  target-definition table is complete and Claude-reviewed;
- any native generalized-SV dense, SMC, mixture, or long-horizon route requires
  a separate phase-specific experiment plan and Claude pass.

## Implementation Sketch

1. Write a target note choosing among native, mixture, transformed-residual, or
   diagnostic-only routes.
2. If same-target route exists, create dims 1--3 tiny fixtures with dense
   reference and directional score checks.
3. If no route exists, keep only finite diagnostic tests and explicit blockers.

## Claim Boundary

No exact generalized-SV CUT4/Zhao--Cui comparison until this phase passes a
target-definition review.
