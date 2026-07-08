# Generic Nonlinear-SSM Likelihood And Analytical-Gradient Target-And-Authority Contract

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Role

This artifact freezes the exact target language, the declared approximate-scalar
language, the same-scalar derivative contract, the route taxonomy, and the
allowed API-scope authority for the generic nonlinear-SSM program.

No implementation or promotion phase may advance unless this contract is
reviewed and accepted.

## Three-Layer Contract

Every route in this program must be classified against exactly one object at a
time:

1. **Exact target**
   - the exact filtering normalizer or exact cumulative likelihood implied by the
     declared state-space model.

2. **Declared approximate scalar**
   - a reviewed Gaussian-projection, fixed-cloud, or other declared approximate
     scalar whose target relation is stated explicitly.

3. **Same-scalar derivative**
   - a derivative that differentiates the same declared scalar on the same saved
     branch.

Only after that declaration does the same-scalar derivative contract become
meaningful.

## Route Taxonomy

Every route/result must be labeled as exactly one of:

- `EXACT_TARGET_STRUCTURAL_LANE`
- `GAUSSIAN_PROJECTION_STRUCTURAL_APPROXIMATION`
- `FIXED_CLOUD_SAME_BRANCH_SGQF_LANE`
- `DIRECT_LIKELIHOOD_POINTWISE_REWEIGHTING_LANE`
- `DIAGNOSTIC_ONLY_FALLBACK_LANE`
- `BLOCKED_MISSING_EVALUATOR_OR_DERIVATIVE`

## Exact-Target And Surrogate Boundary

- A Gaussian-projection or Gaussian-closure route may be scientifically useful,
  but it must not be promoted as same-target evidence unless a reviewed artifact
  explicitly shows that the declared scalar is the intended target for the claim
  being made.
- Internal consistency of a Gaussian-closure scalar does not repair a target
  mismatch.
- Tests passed on the wrong scalar do not advance the program.

## Structural Admission Boundary

A model may enter a generic likelihood/gradient lane only after a reviewed
structural-admission artifact classifies it as:

- exact eligible,
- approximate eligible, or
- ineligible with explicit reason.

No fixture-specific workaround may be silently promoted as generic support.

## Exact Scalar Naming Rule

The reviewed contract must name explicitly, for every admitted claim, whether
its scalar authority is:

- a one-step exact filtering normalizer,
- a cumulative exact likelihood,
- a declared one-step approximate scalar, or
- a declared cumulative approximate scalar.

One-step and cumulative evidence are not interchangeable unless a reviewed
artifact explicitly states the relation being claimed.

## Same Saved Branch Rule

For this program, “same saved branch” means equality of the reviewed fixed ledger
that defines the scalar together with equality of the realized accepted/failure
stage-time pattern needed by the lane-specific same-scalar contract.

At minimum, the saved branch includes the reviewed structural route by which the
value is produced. Depending on the lane, it may also include fixed-cloud,
merge/order policy, factor branch, thresholds, replay tape, retained-object
construction policy, or other reviewed lane-specific frozen structure.

## Structural Admission Unit

Structural admission is route-level, not just model-level. A model may be:

- exact eligible for one lane,
- approximate eligible for another lane, and
- ineligible for a third lane.

Therefore every admission artifact must classify at the level of
`model × lane × claim`.

## API-Scope Authority Boundary

At launch, passing value/score work may support:

- scoped subpackage-level value/score APIs, and
- reviewed lane-specific likelihood/gradient claims.

At launch, passing value/score work does **not** support:

- top-level API promotion,
- HMC readiness,
- production readiness,
- benchmark/leaderboard promotion,
- default-policy change.

## Explicit Vetoes

The following are contract violations:

- promoting Gaussian-closure surrogate evidence as same-target evidence without
  reviewed authorization;
- claiming analytical-gradient support before the value gate passes;
- using a derivative whose branch identity or accepted/failure pattern differs
  from the corresponding value path as same-scalar evidence;
- promoting subpackage-scoped score APIs as top-level, HMC-ready, or production-
  ready by implication;
- changing exact target semantics, declared approximate-scalar semantics, or the
  route taxonomy without a reviewed reset artifact.

## What This Contract Does Not Conclude

- It does not admit any particular model to any lane yet.
- It does not yet validate any value path.
- It does not yet validate any analytical gradient.
- It does not conclude HMC readiness, production readiness, benchmark
  promotion, or default-policy change.
