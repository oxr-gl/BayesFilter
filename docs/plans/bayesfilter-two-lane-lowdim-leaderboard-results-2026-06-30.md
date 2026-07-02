# Two-Lane Lowdim Leaderboard Result

Authoritative JSON artifact: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.json`.

## Rankable lowdim rows

| Row | Algorithm | Status | Abs error | First s | Steady s | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- |
| lgssm_exact_kalman_dim_1 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.356578 | 0.003136 | exact LGSSM baseline |
| lgssm_exact_kalman_dim_1 | ukf | executed_rankable | 1.110223e-16 | 0.042176 | 0.012968 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_1 | cut4 | executed_rankable | 1.110223e-16 | 0.019979 | 0.013230 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_1 | zhao_cui_scalar_or_multistate | executed_rankable | 0.000000e+00 | 0.130439 | 0.094799 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_1 | fixed_sgqf | executed_rankable | 8.881784e-16 | 0.017634 | 0.010431 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_2 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.121074 | 0.002798 | exact LGSSM baseline |
| lgssm_exact_kalman_dim_2 | ukf | executed_rankable | 4.440892e-16 | 0.013376 | 0.012685 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_2 | cut4 | executed_rankable | 0.000000e+00 | 0.013675 | 0.012802 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_2 | zhao_cui_scalar_or_multistate | executed_rankable | 0.000000e+00 | 0.129484 | 0.124205 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_2 | fixed_sgqf | executed_rankable | 1.332268e-15 | 0.012898 | 0.010361 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_3 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.003074 | 0.002601 | exact LGSSM baseline |
| lgssm_exact_kalman_dim_3 | ukf | executed_rankable | 8.881784e-16 | 0.013813 | 0.014110 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_3 | cut4 | executed_rankable | 0.000000e+00 | 0.016555 | 0.016876 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_3 | zhao_cui_scalar_or_multistate | executed_rankable | 0.000000e+00 | 0.168616 | 0.165867 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_3 | fixed_sgqf | executed_rankable | 2.664535e-15 | 0.012800 | 0.013356 | same-target lowdim LGSSM |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.033709 | 0.020054 | declared surrogate reference |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | ukf | executed_rankable | 0.000000e+00 | 0.075452 | 0.086124 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | cut4 | executed_rankable | 0.000000e+00 | 0.085503 | 0.083422 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | fixed_sgqf | executed_rankable | 1.776357e-15 | 0.053208 | 0.053361 | tiny_same_target_surrogate_fixture_only |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | zhao_cui_scalar_or_multistate | executed_rankable | 5.196991e-04 | 0.244355 | 0.229453 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.125368 | 0.125898 | declared surrogate reference |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | ukf | executed_rankable | 0.000000e+00 | 0.637486 | 0.613367 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | cut4 | executed_rankable | 0.000000e+00 | 0.639966 | 0.665609 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | fixed_sgqf | executed_rankable | 1.776357e-15 | 0.344774 | 0.352673 | tiny_same_target_surrogate_fixture_only |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | zhao_cui_scalar_or_multistate | executed_rankable | 6.235128e-04 | 0.453928 | 0.464059 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.910337 | 1.022252 | declared surrogate reference |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | ukf | executed_rankable | 1.776357e-15 | 4.157743 | 3.897071 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | cut4 | executed_rankable | 5.329071e-15 | 4.289373 | 4.439291 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | fixed_sgqf | executed_rankable | 0.000000e+00 | 2.472235 | 2.722064 | tiny_same_target_surrogate_fixture_only |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | zhao_cui_scalar_or_multistate | executed_rankable | 4.969389e-04 | 0.691560 | 0.683900 | same-target surrogate lane |

## Status-only and blocked rows

| Row | Algorithm | Status | Reason |
| --- | --- | --- | --- |
| fixed_sgqf_model_c_autonomous_nonlinear_growth_fixture | fixed_sgqf | executed_status_only | SGQF-exact-eligible local fixture; not one of the frozen four-way lowdim rankable rows |
| fixed_sgqf_model_c_autonomous_nonlinear_growth_fixture | ukf | executed_status_only | local SGQF-exact-eligible fixture; auxiliary status-only timing row |
| fixed_sgqf_model_c_autonomous_nonlinear_growth_fixture | cut4 | executed_status_only | local SGQF-exact-eligible fixture; auxiliary status-only timing row |
| p44_cubic_additive_gaussian_dim_1_2_3 | fixed_sgqf | blocked | fixed SGQF not same-target or adapter not admitted on this diagnostic-only P44 row |
| p44_cubic_additive_gaussian_dim_1_2_3 | ukf | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_cubic_additive_gaussian_dim_1_2_3 | cut4 | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_cubic_additive_gaussian_dim_1_2_3 | zhao_cui_scalar_or_multistate | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_nonlinear_transition_h2_dim_1_2_3 | fixed_sgqf | blocked | fixed SGQF not same-target or adapter not admitted on this diagnostic-only P44 row |
| p44_nonlinear_transition_h2_dim_1_2_3 | ukf | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_nonlinear_transition_h2_dim_1_2_3 | cut4 | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_nonlinear_transition_h2_dim_1_2_3 | zhao_cui_scalar_or_multistate | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3 | fixed_sgqf | blocked | fixed SGQF not same-target or adapter not admitted on this diagnostic-only P44 row |
| p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3 | ukf | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3 | cut4 | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3 | zhao_cui_scalar_or_multistate | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_quadratic_observation_dim_1_2_3 | fixed_sgqf | blocked | fixed SGQF not same-target or adapter not admitted on this diagnostic-only P44 row |
| p44_quadratic_observation_dim_1_2_3 | ukf | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_quadratic_observation_dim_1_2_3 | cut4 | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
| p44_quadratic_observation_dim_1_2_3 | zhao_cui_scalar_or_multistate | diagnostic_only | diagnostic-only row; not rankable in lowdim leaderboard |
