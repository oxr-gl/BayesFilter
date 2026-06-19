# Fixed-SGQF KSC-Surrogate Analytic Score Plan

metadata_date: 2026-06-18
program_id: fixed-sgqf-ksc-surrogate-analytic-score
status: PLANNING_READY

## Purpose

Implement a **true analytical outer score** for the KSC Gaussian-mixture
surrogate stochastic-volatility row so that the Fixed-SGQF wrapper is no longer
value-only.

This plan exists because:
- the core Fixed-SGQF lane already has an analytical first-order score contract
  via `tf_fixed_sgqf_score(...)`,
- the current KSC-surrogate SGQF wrapper only has a value route,
- prior wrapper-gradient evidence based on autodiff was explicitly demoted,
- autodiff may be used only as a **validation oracle** for an already
  implemented analytical gradient, not as the SGQF score itself.

## Context

Current same-target KSC-surrogate value routes exist in:
- `bayesfilter/highdim/sv_mixture_cut4.py`
  - `independent_panel_sv_mixture_kalman_filter(...)`
  - `independent_panel_sv_mixture_cut4_filter(...)`
  - `independent_panel_sv_mixture_zhaocui_tt_filter(...)`
  - `independent_panel_sv_mixture_fixed_sgqf_filter(...)`

Current analytical score-bearing kernels already exist for:
- Fixed-SGQF core:
  - `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  - `tf_fixed_sgqf_score(...)`
- SVD UKF / cubature / CUT4 core:
  - `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
  - `tf_svd_ukf_score(...)`
  - `tf_svd_cubature_score(...)`
  - `tf_svd_cut4_score(...)`

What is missing is the **outer mixture-wrapper score contract** for the KSC
surrogate SGQF route, and the same-target KSC surrogate UKF analytical
comparison lane that this project requires for all models.

## Question

Can we implement an analytical outer mixture score for
`independent_panel_sv_mixture_fixed_sgqf_filter(...)` that:
- remains same-target with the declared KSC surrogate row,
- reuses the existing core analytical Fixed-SGQF score API,
- is validated against finite differences (primary),
- and is compared against:
  - a required same-target UKF value + analytical gradient lane,
  - Zhao-Cui autodiff only as a temporary secondary comparison,
  - and CUT4 analytical score only if a true KSC wrapper score route is exposed?

## Skeptical audit

Main failure modes to avoid:
1. quietly reintroducing autodiff as the SGQF score rather than a validation
   oracle;
2. analytically differentiating the inner SGQF kernel but forgetting the outer
   mixture log-sum-exp aggregation;
3. missing the `beta`-dependent observation-centering derivative, producing an
   apparently smooth but wrong score;
4. claiming a wrapper-level score without a clear component failure / branch
   consistency policy;
5. comparing against Zhao-Cui autodiff as if that were stronger than
   finite-difference evidence.

Blocking rule:
- do not promote the route to gradient-valid unless the analytical wrapper score
  matches finite differences on the declared tiny fixture.

## Evidence contract

Baseline / truth anchor:
- `ksc_sv_gaussian_mixture_kalman_enumeration` remains the value truth anchor.

Primary promotion criterion:
- a new analytical SGQF wrapper score exists and matches finite differences for
  dims 1, 2, 3 on the declared tiny KSC-surrogate fixture.
- a same-target UKF wrapper value route exists for the same fixture.
- a same-target UKF analytical score exists and matches finite differences for
  dims 1, 2, 3 on the same fixture.
- SGQF and UKF can therefore be compared on both value and analytical gradient,
  as required by project policy for all models.

Secondary validation criteria:
- the analytical SGQF wrapper score may be compared against:
  - autodiff of the same SGQF wrapper value route,
  - Zhao-Cui wrapper autodiff,
  - CUT4 analytical score if a true KSC wrapper score route is exposed.
- the analytical UKF wrapper score may likewise be validated against finite
  differences and, if convenient, autodiff of the same wrapper value route.
- these are validation / consistency checks only; they are not the primary
  promotion oracle.

Veto diagnostics:
- wrapper/component branch inconsistency,
- any component score failure,
- non-finite finite-difference rows,
- missing stable finite-difference window.

What will not be concluded even if this passes:
- no actual transformed non-Gaussian SV claim,
- no HMC readiness claim,
- no production-readiness claim,
- no source-faithful Zhao-Cui equivalence claim.

## Files to modify

### Primary implementation
- `bayesfilter/highdim/sv_mixture_cut4.py`

### Existing score contracts to reuse unchanged
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`

### Primary tests
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`

### Existing analytical score regression suites to keep green
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_nonlinear_sigma_point_scores_tf.py`

### Governance / result artifacts to update only after passing tests
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json`
- `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md`

## Existing functions and utilities to reuse

### KSC surrogate utilities
- `ksc_1998_log_chi_square_mixture(...)`
- `transformed_sv_panel_observations(...)`
- `_component_tuples(...)`
- `_collapse_gaussian_components(...)`
- `independent_panel_sv_mixture_kalman_filter(...)`
- `independent_panel_sv_mixture_fixed_sgqf_filter(...)`
- existing or new same-target UKF wrapper helpers to be added in
  `bayesfilter/highdim/sv_mixture_cut4.py`

### Fixed-SGQF analytical score kernel
- `tf_fixed_sgqf_filter(...)`
- `tf_fixed_sgqf_score(...)`
- `TFFixedSGQFDerivatives`
- `TFFixedSGQFBranchConfig`
- `tf_fixed_sgqf_same_branch_signature(...)`

### SVD UKF analytical score kernel
- `tf_svd_ukf_score(...)`
- `TFStructuralFirstDerivatives`

### Highdim derivative utilities that may help wrapper/result packaging
- `FixedBranchScoreResult`
- `make_finite_difference_row(...)`
- `FiniteDifferenceTable`
- `retained_filter_quotient_derivative(...)`
- `exact_score_result(...)`

### Existing finite-difference / oracle patterns to mirror
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/test_nonlinear_sigma_point_scores_tf.py`

## Recommended implementation strategy

### 0. Add the required same-target UKF analytical comparison lane
In `bayesfilter/highdim/sv_mixture_cut4.py`, add or expose a same-target KSC
surrogate UKF wrapper route and score route before final promotion of this
program.

Required public functions:
- `independent_panel_sv_mixture_ukf_filter(...)`
- `independent_panel_sv_mixture_ukf_score(...)`

Minimum requirements:
- same transformed observation convention as the SGQF wrapper,
- same KSC mixture tuple conditioning and Gaussian collapse semantics,
- analytical score derived from the existing SVD UKF core score path,
- finite-difference validation on dims 1, 2, 3.

### 1. Add a new public SGQF score route
In `bayesfilter/highdim/sv_mixture_cut4.py`, add:
- `independent_panel_sv_mixture_fixed_sgqf_score(...)`

Suggested contract:
- inputs parallel to `independent_panel_sv_mixture_fixed_sgqf_filter(...)`
- outputs:
  - `log_likelihood`
  - `score`
  - wrapper diagnostics
  - wrapper branch/failure metadata

It may return a new dedicated dataclass, or a score result container compatible
with the repo’s existing score/result vocabulary.

### 2. Build per-component analytical SGQF score inputs
Add helper(s) in `sv_mixture_cut4.py`:
- `_panel_transformed_sv_component_fixed_sgqf_derivatives(...)`
- `_fixed_sgqf_component_value_and_score(...)`

For each mixture tuple and time step:
- reuse the existing component-conditioned affine SGQF model;
- create the corresponding `TFFixedSGQFDerivatives` object.

The derivative object must include:
- `d_initial_mean`
- `d_initial_covariance`
- `d_process_covariance`
- `d_observation_covariance`
- `transition_state_jacobian_fn`
- `d_transition_fn`
- `observation_state_jacobian_fn`
- `d_observation_fn`

### 3. Handle theta dependence correctly
The row’s active theta coordinates are:
- `probit_gamma_j`
- `log_beta_j`

For the current tiny KSC-surrogate row:
- `sigma` is fixed fixture data, so there is no theta derivative through
  `sigma`.
- `gamma` contributes through:
  - transition matrix / predictive mean / predictive covariance.
- `beta` contributes through the component-centered transformed observation
  shift:
  - the wrapper currently evaluates each component against
    `z_t - (log(beta^2) + mixture_mean_component)`.
  - therefore the analytical score must include the derivative of
    `-2 * log_beta_j` in the centered observation term.

This is the most likely place to make a silent analytical mistake; treat it as
explicitly review-critical.

### 4. Analytical outer mixture aggregation
Per component tuple `k`, compute:
- component log term
  - `ell_k(theta) = log(pi_k) + log p_k(y | theta)`
- component analytical score
  - `g_k(theta) = d/dtheta ell_k(theta)`

Then aggregate analytically at the wrapper level using:
- normalized mixture weights
  - `w_k(theta) = exp(ell_k) / sum_j exp(ell_j)`
- outer score
  - `g(theta) = sum_k w_k(theta) * g_k(theta)`

Because the KSC mixture weights are fixed, `log(pi_k)` contributes no theta
score term.

### 5. Wrapper failure / branch policy
Analytical score should be admitted only if:
- all component score calls use the same SGQF cloud,
- all component score calls use the same branch config,
- all component score calls succeed,
- no component branch mismatch is detected,
- no component failure occurs.

If any component lane fails:
- block the wrapper score,
- return explicit diagnostics,
- do not silently drop the component.

Recommended wrapper diagnostics:
- `fixed_sgqf_branch_hash`
- `fixed_sgqf_sparse_level`
- `fixed_sgqf_cloud_point_count`
- `component_tuple_count`
- `wrapper_score_contract = analytic_component_score_logsumexp_aggregation`
- `component_score_failures`

### 6. Testing plan

#### Primary correctness test: finite differences
Add for dims 1, 2, 3:
- analytical SGQF wrapper score vs finite-difference wrapper value score
- analytical UKF wrapper score vs finite-difference wrapper value score

This is the primary promotion oracle.

#### Required cross-method comparison: UKF
Because project policy requires UKF comparison for all models, add:
- SGQF analytical wrapper score vs UKF analytical wrapper score
- SGQF wrapper value vs UKF wrapper value
- both on the same declared KSC surrogate fixture for dims 1, 2, 3

#### Secondary validation test: autodiff
After the analytical wrapper score exists, add:
- analytical SGQF wrapper score vs autodiff of the same wrapper value route
- analytical UKF wrapper score vs autodiff of the same wrapper value route

Label these explicitly as:
- validation oracles only
- not the admitted SGQF or UKF scores themselves

#### Secondary cross-method comparison: Zhao-Cui autodiff
For now, compare:
- analytical SGQF wrapper score vs Zhao-Cui wrapper autodiff score
- analytical UKF wrapper score vs Zhao-Cui wrapper autodiff score if useful

This is useful as a same-target cross-method comparison, but not sufficient for
promotion by itself.

#### Optional secondary comparison: CUT4 analytic score
Only if a true analytical KSC-surrogate CUT4 wrapper score route is exposed,
compare:
- analytical SGQF wrapper score vs analytical CUT4 wrapper score
- analytical UKF wrapper score vs analytical CUT4 wrapper score

#### Contract tests
Add tests that:
- force a component score failure and verify wrapper block behavior;
- confirm branch-policy consistency across component lanes.

## Verification commands

Minimum focused sequence:
1. targeted SGQF wrapper analytic score tests in:
   - `tests/highdim/test_p47_generalized_sv_equality.py`
   - `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
2. targeted UKF wrapper analytic score tests on the same KSC surrogate fixture in:
   - `tests/highdim/test_p47_generalized_sv_equality.py`
   - `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
3. core SGQF analytic score regressions:
   - `tests/test_fixed_sgqf_scores_tf.py`
   - `tests/test_fixed_sgqf_branch_contract_tf.py`
4. sigma-point analytic score regressions:
   - `tests/test_nonlinear_sigma_point_scores_tf.py`
5. governance artifact tests if promotion occurs:
   - `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
   - `tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py`

All runs should remain CPU-only with `CUDA_VISIBLE_DEVICES=-1` set before
TensorFlow import.

## Pass criteria

Promote the KSC-surrogate SGQF wrapper to gradient-valid only if:
- analytical SGQF wrapper score exists,
- analytical UKF wrapper score exists,
- finite-difference tests pass for both SGQF and UKF on dims 1, 2, 3,
- SGQF and UKF value/score comparisons are present on the same surrogate row,
- branch/component failure policy is explicit and covered by tests,
- autodiff and Zhao-Cui comparisons, if included, are treated as secondary
  validation only,
- governance artifacts are updated consistently.

## Nonclaims

Even if this plan succeeds, it still does not establish:
- actual transformed non-Gaussian SV correctness,
- HMC readiness,
- production readiness,
- global scalability,
- source-faithful Zhao-Cui equivalence.
