# KSC-Surrogate Analytic Score Derivative-Carry Subplan

metadata_date: 2026-06-18
program_id: fixed-sgqf-ksc-surrogate-analytic-score-derivative-carry
status: PLANNING_READY
parent_plan: docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md

## Purpose

Resolve the remaining design blocker before implementing analytical outer score
routes for the KSC Gaussian-mixture surrogate lane.

The blocker is not the mixture-score formula itself. The blocker is how to
propagate **carried posterior state derivatives** across time in the wrapper:
- filtered mean derivative
- filtered covariance derivative

Both the SGQF and UKF analytical score kernels currently return score results,
but do not expose the carried derivative state that a sequential
mixture-component wrapper needs at time `t+1`.

## Design question

For the KSC surrogate analytical score wrappers, should we:

### Option A — extend kernel score APIs
Extend the existing analytical score APIs to expose the carried derivative
state, so wrapper code can reuse kernel logic directly.

Relevant kernels:
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  - `tf_fixed_sgqf_score(...)`
- `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
  - `tf_svd_ukf_score(...)`
  - possibly `tf_svd_cut4_score(...)` later

Needed additional outputs:
- `filtered_mean`
- `filtered_covariance`
- `d_filtered_mean`
- `d_filtered_covariance`

#### Pros
- keeps analytical derivative truth close to the kernel implementation;
- avoids duplicating derivative recursion in wrapper code;
- gives a reusable foundation for future multi-step analytical wrappers.

#### Cons
- changes stable derivative-return surfaces for core kernels;
- may require new result containers or compatibility handling;
- larger blast radius if existing tests assume current result shape.

### Option B — wrapper-local derivative recursion
Keep kernel score APIs unchanged, and implement the needed derivative-carry
logic inside `bayesfilter/highdim/sv_mixture_cut4.py` for the KSC wrapper.

That means the wrapper would reproduce enough of the per-component analytical
update to carry:
- component filtered mean / covariance,
- component derivative of filtered mean / covariance,
- then analytically collapse those quantities across components.

#### Pros
- avoids changing core SGQF/UKF score APIs;
- smaller impact on unrelated kernel tests.

#### Cons
- duplicates derivative logic already present in the kernels;
- higher risk of divergence between kernel score behavior and wrapper score
  behavior;
- harder to maintain if kernel derivative formulas change.

## Current code facts

### SGQF analytical kernel
In `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`, the score recursion
already computes internal quantities such as:
- `d_filtered_mean`
- `d_filtered_covariance`

but only returns:
- `log_likelihood`
- `score`
- branch diagnostics / failure status

The carried derivatives are internal and not exposed in the returned result.

### SVD UKF analytical kernel
In `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`, the score
recursion likewise computes internal derivative state such as:
- `d_mean`
- `d_covariance`

but only returns a `TFFilterDerivativeResult` with:
- `log_likelihood`
- `score`
- metadata / diagnostics

Again, carried derivatives are internal only.

### Wrapper consequence
The KSC mixture wrapper is sequential. After analytically collapsing component
posteriors at time `t`, the next time step needs the derivative of the collapsed
mean and covariance as the new prior derivative state.

So a correct wrapper analytical score cannot stop at scalar score increments.
It must also carry state derivatives forward.

## Recommendation

Recommended approach: **Option A — extend kernel score APIs**.

Why:
- the kernels already compute the needed derivative-carry quantities;
- exposing them is less error-prone than re-deriving wrapper-local recursions;
- both SGQF and UKF need the same capability for this lane;
- this creates a reusable primitive for future analytic multi-step wrappers.

### Preferred implementation shape

1. Introduce new internal or public derivative result containers that augment
   the current score outputs with carried posterior derivative state.

   For example:
   - SGQF: an extended result type carrying
     - `filtered_mean`
     - `filtered_covariance`
     - `d_filtered_mean`
     - `d_filtered_covariance`
   - SVD UKF: analogous extended result type carrying the same fields

2. Preserve existing public score entrypoints if possible for backward
   compatibility:
   - either by adding an optional flag such as `return_carry_state=True`, or
   - by introducing companion functions with explicit names, e.g.
     - `tf_fixed_sgqf_score_with_carry(...)`
     - `tf_svd_ukf_score_with_carry(...)`

3. Use those carry-state-aware score functions inside the KSC wrapper score
   routes:
   - `independent_panel_sv_mixture_fixed_sgqf_score(...)`
   - `independent_panel_sv_mixture_ukf_score(...)`

4. Collapse across components not just for value and posterior moments, but also
   for derivative-carry state.

## Required files if this design is approved

### Core derivative kernels
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
- possibly `bayesfilter/results_tf.py` if shared result containers are added

### KSC wrapper implementation
- `bayesfilter/highdim/sv_mixture_cut4.py`

### Tests
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/test_nonlinear_sigma_point_scores_tf.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`

## Verification

Before full wrapper implementation, verify the carry-state design with two
small checks:

1. **SGQF carry-state exposure check**
   - confirm the extended SGQF score result returns finite
     `filtered_mean`, `filtered_covariance`, `d_filtered_mean`, and
     `d_filtered_covariance` on a tiny existing SGQF analytic-score fixture.

2. **UKF carry-state exposure check**
   - confirm the extended UKF score result returns the analogous carried state
     on a tiny existing SVD UKF analytic-score fixture.

Only after those pass should the KSC surrogate wrapper score implementation
begin.

## Claim boundary

This subplan chooses the derivative-carry design only. It does **not** itself
claim that the full KSC surrogate SGQF or UKF analytical wrapper scores are
implemented or validated yet.
