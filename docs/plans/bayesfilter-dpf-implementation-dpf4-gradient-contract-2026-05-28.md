# DPF4 Gradient Contract

## Status

DPF4 execution artifact.  This contract defines what a gradient means in the
BayesFilter-owned DPF implementation lane.

## Core Rule

The gradient supplied to any optimizer, diagnostic, or future sampler must be
the derivative of the same scalar value named in the artifact.  A finite
gradient is only evidence about that scalar and computational path.

## Required Gradient Fields

| Field | Requirement |
| --- | --- |
| `scalar_id` | Stable id for the scalar value. |
| `scalar_formula_or_source` | Equation, implementation expression, or component objective. |
| `target_status` | One of the DPF4 target-status labels. |
| `parameter_coordinates` | Structural or unconstrained coordinates; transform and Jacobian policy if applicable. |
| `randomness_policy` | Fresh randomness, fixed seed, common random numbers, extended-space variable, or deterministic. |
| `resampling_policy` | Hard, soft, EOT, finite Sinkhorn, learned, or none. |
| `gradient_path` | Reparameterized, stopped-gradient, branchwise, unrolled solver, implicit solver, learned-map autodiff, finite-difference, or analytic. |
| `same_scalar_check` | Evidence that value and gradient refer to the same scalar. |
| `finite_check` | Value and gradient finite under stated fixture. |
| `non_implications` | Explicit limits: posterior/HMC/production claims not concluded. |

## Same-Scalar Evidence Ladder

| Level | Evidence | Allowed claim |
| --- | --- | --- |
| G0 | Scalar named only | Objective is classified; no gradient validity claim. |
| G1 | Finite value and finite gradient | Computational path is finite on the fixture. |
| G2 | Finite-difference or analytic parity for same scalar | Gradient-valid for the named controlled scalar. |
| G3 | Eager/compiled/repeated parity and seed policy | Gradient path is implementation-stable under declared conditions. |
| G4 | Downstream posterior/reference and sampler diagnostics | Candidate for HMC/posterior interpretation under separate plan. |

DPF4 authorizes G0-G3 specifications only.  G4 remains a future evidence gate.

## Stop Rules

Stop or label `blocked_unclassified` if:

- the scalar value cannot be named;
- value and gradient refer to different objects;
- fixed randomness is confused with pseudo-marginal validity;
- finite gradient is used as posterior or HMC evidence;
- soft/EOT/learned gradients are called original likelihood scores without a
  correction or equivalence argument;
- vendored student code or notebooks are required as authority;
- high-dimensional or external HMC lanes are needed as authority.

## Banned Wording

- "validated DPF-HMC pipeline" unless target status, same-scalar
  value-gradient, posterior/reference, and sampler diagnostics have passed.
- "gradient of the likelihood" for a relaxed, learned, or fixed-randomness
  scalar unless the likelihood object is exactly identified and proved.
- "posterior preserving" for soft, EOT, Sinkhorn, or learned resampling without
  correction or posterior-error evidence.
