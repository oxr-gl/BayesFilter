# Two-Lane Lowdim Leaderboard Result

Authoritative JSON artifact: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-24.json`.

## Rankable lowdim rows

| Row | Algorithm | Status | Abs error | First s | Steady s | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- |
| lgssm_exact_kalman_dim_1 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.373266 | 0.003284 | exact LGSSM baseline |
| lgssm_exact_kalman_dim_1 | ukf | executed_rankable | 1.110223e-16 | 0.046330 | 0.013376 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_1 | cut4 | executed_rankable | 1.110223e-16 | 0.020571 | 0.013650 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_1 | zhao_cui_scalar_or_multistate | executed_rankable | 0.000000e+00 | 0.148663 | 0.112677 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_2 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.125412 | 0.003639 | exact LGSSM baseline |
| lgssm_exact_kalman_dim_2 | ukf | executed_rankable | 4.440892e-16 | 0.017025 | 0.013426 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_2 | cut4 | executed_rankable | 0.000000e+00 | 0.013975 | 0.014113 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_2 | zhao_cui_scalar_or_multistate | executed_rankable | 0.000000e+00 | 0.145664 | 0.138289 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_3 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.003386 | 0.003588 | exact LGSSM baseline |
| lgssm_exact_kalman_dim_3 | ukf | executed_rankable | 8.881784e-16 | 0.014582 | 0.014146 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_3 | cut4 | executed_rankable | 0.000000e+00 | 0.014697 | 0.013783 | same-target lowdim LGSSM |
| lgssm_exact_kalman_dim_3 | zhao_cui_scalar_or_multistate | executed_rankable | 0.000000e+00 | 0.176715 | 0.173964 | same-target lowdim LGSSM |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.035655 | 0.022450 | declared surrogate reference |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | ukf | executed_rankable | 0.000000e+00 | 0.081365 | 0.082031 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | cut4 | executed_rankable | 0.000000e+00 | 0.089944 | 0.089317 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | fixed_sgqf | executed_rankable | 1.776357e-15 | 0.058318 | 0.059188 | tiny_same_target_surrogate_fixture_only |
| sv_ksc_gaussian_mixture_surrogate_dim_1 | zhao_cui_scalar_or_multistate | executed_rankable | 5.196991e-04 | 0.269943 | 0.236781 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.130706 | 0.125840 | declared surrogate reference |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | ukf | executed_rankable | 0.000000e+00 | 0.585656 | 0.577293 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | cut4 | executed_rankable | 0.000000e+00 | 0.632857 | 1.002668 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | fixed_sgqf | executed_rankable | 1.776357e-15 | 0.390908 | 0.529026 | tiny_same_target_surrogate_fixture_only |
| sv_ksc_gaussian_mixture_surrogate_dim_2 | zhao_cui_scalar_or_multistate | executed_rankable | 6.235128e-04 | 0.483882 | 0.465928 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | kalman_exact_or_mixture_enumeration | reference_only | 0.000000e+00 | 0.888387 | 0.894379 | declared surrogate reference |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | ukf | executed_rankable | 1.776357e-15 | 4.195175 | 4.204696 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | cut4 | executed_rankable | 5.329071e-15 | 4.469071 | 4.515095 | same-target surrogate lane |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | fixed_sgqf | executed_rankable | 0.000000e+00 | 2.642613 | 2.863376 | tiny_same_target_surrogate_fixture_only |
| sv_ksc_gaussian_mixture_surrogate_dim_3 | zhao_cui_scalar_or_multistate | executed_rankable | 4.969389e-04 | 0.715415 | 0.709232 | same-target surrogate lane |

## Status-only and blocked rows

| Row | Algorithm | Status | Reason |
| --- | --- | --- | --- |
| lgssm_exact_kalman_dim_1 | fixed_sgqf | blocked | current fixed SGQF structural adapter only supports the autonomous phase nonlinear growth fixture exactly |
| lgssm_exact_kalman_dim_2 | fixed_sgqf | blocked | current fixed SGQF structural adapter only supports the autonomous phase nonlinear growth fixture exactly |
| lgssm_exact_kalman_dim_3 | fixed_sgqf | blocked | current fixed SGQF structural adapter only supports the autonomous phase nonlinear growth fixture exactly |
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
