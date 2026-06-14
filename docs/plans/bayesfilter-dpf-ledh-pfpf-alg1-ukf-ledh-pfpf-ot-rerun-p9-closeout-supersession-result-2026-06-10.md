# P9 Result: Closeout And Supersession Ledger

metadata_date: 2026-06-10
phase: P9
status: PASS_P9_CLOSEOUT_SUPERSESSION_CLAUDE_REVIEWED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After P0-P8, is every previous LEDH-PFPF-OT-related test either redone with Algorithm 1 UKF or explicitly classified? |
| Baseline/comparator | P0 rerun registry and P1-P8 result artifacts. |
| Primary criterion | A closeout ledger indexes every old lane, replacement artifact, remaining blocker, historical-only row, manifest, and nonclaim. |
| Promotion policy | No new P9 numerical promotion; promoted row list must be empty. |

## Guardrail Rerun

- Command: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q`
- Status: `passed`.
- Summary: `15 passed, 2 warnings in 6.29s`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_P9_CLOSEOUT_SUPERSESSION_CLAUDE_REVIEWED` | 21 registry lanes closed; 0 promoted rows emitted | `no structural vetoes` | diagnostic rows remain bounded by small particle ladders and fixed-branch gradients | Final closeout complete; old LEDH-PFPF-OT evidence remains superseded/quarantined | no production default, HMC readiness, universal superiority, or stochastic-score correctness |

## Old Lane Dispositions

| Old lane | Planned | Final | Route class | Source |
| --- | --- | --- | --- | --- |
| `direct_lgssm_value` | `RERUN_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P1_lane_status` |
| `direct_lgssm_multiseed` | `RERUN_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P1_lane_status` |
| `direct_range_bearing_value` | `BLOCKED_REQUIRES_ADAPTER` | `BLOCKED_REQUIRES_ADAPTER` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P1_lane_status` |
| `direct_range_bearing_stress` | `BLOCKED_REQUIRES_ADAPTER` | `BLOCKED_REQUIRES_ADAPTER` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P1_lane_status` |
| `direct_gradient_checks` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P1_lane_status` |
| `v2_contracts` | `RERUN_ALG1` | `RERUN_ALG1` | `SOURCE_ALGORITHM1_CORE` | `P2_contract_freeze` |
| `v2_values` | `RERUN_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P3_value_replacement` |
| `v2_gradients` | `RERUN_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P4_gradient_replacement` |
| `v2_live_gate_and_closeout_consumers` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P9_quarantine_closeout` |
| `filter_oracle_p0_registry_consumer` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P9_quarantine_closeout` |
| `filter_oracle_p2_tiny_nonlinear_dense_oracle_consumer` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P9_quarantine_closeout` |
| `filter_oracle_p3_conditional_gaussian_mixture_consumer` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P9_quarantine_closeout` |
| `filter_oracle_p4_zhaocui_route_classification_consumer` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P9_quarantine_closeout` |
| `filter_oracle_p1_lgssm_exact` | `RERUN_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P5_filter_oracle_replacement` |
| `filter_oracle_p5_statistical_closeness` | `RERUN_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P5_filter_oracle_replacement` |
| `filter_oracle_p6_cross_filter_calibration` | `RERUN_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P6_cross_filter_calibration` |
| `filter_oracle_p7_closeout` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P9_quarantine_closeout` |
| `filter_oracle_p8_p44_blocker_closure` | `BLOCKED_REQUIRES_ADAPTER` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `SOURCE_ALGORITHM1_CORE` | `P7_p44_blocker_closure` |
| `source_faithful_repair_auxiliary_flow_only` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P8_auxiliary_flow_classification` |
| `annealed_transport_ledh_lgssm` | `BLOCKED_REQUIRES_SEPARATE_PLAN` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `NOT_CURRENT_ALGORITHM1_EVIDENCE` | `P8_extension_classification` |
| `filterflow_matched_ledh_pfpf_ot` | `BLOCKED_REQUIRES_SEPARATE_PLAN` | `SCAFFOLDING_ONLY` | `BAYESFILTER_EXTENSION_OR_SCAFFOLDING_NOT_SOURCE_CORE` | `P8_filterflow_scaffolding_classification` |

## Value Table

| Phase | Target | Dim | Particles | Seeds | Status | RMSE | SE | Band |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| `P1` | `direct_lgssm` |  | 8 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.4400073375211782` | `0.4433609690412701` | `N/A_DIAGNOSTIC_ONLY_IN_P1` |
| `P1` | `direct_lgssm` |  | 16 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.0313446531019403` | `0.2533858571197173` | `N/A_DIAGNOSTIC_ONLY_IN_P1` |
| `P1` | `direct_lgssm` |  | 32 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.8660014445239481` | `0.34829564404897045` | `N/A_DIAGNOSTIC_ONLY_IN_P1` |
| `P3` | `lgssm_2d_h25_rich` |  | 8 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.5460296492923338` | `0.26150468671406357` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `lgssm_2d_h25_rich` |  | 16 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.45796931675642605` | `0.22739998304309836` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `lgssm_2d_h25_rich` |  | 32 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.41825736258132357` | `0.20582366822077328` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `predator_prey_rk4` |  | 8 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.13173341111037257` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `predator_prey_rk4` |  | 16 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.0920296256699032` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `predator_prey_rk4` |  | 32 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.07581189616226446` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `range_bearing_4d_h20_rich` |  | 8 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `2.0123283981866087` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `range_bearing_4d_h20_rich` |  | 16 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.5039957061912675` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `range_bearing_4d_h20_rich` |  | 32 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.7908012028888805` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `spatial_sir_j3_rk4` |  | 8 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.7517062354948472` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `spatial_sir_j3_rk4` |  | 16 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.4857966760223286` | `N/A_DIAGNOSTIC_ONLY` |
| `P3` | `spatial_sir_j3_rk4` |  | 32 | 5 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `0.38796876526950913` | `N/A_DIAGNOSTIC_ONLY` |
| `P7` | `p44_m2_cubic_additive_gaussian_panel` | 1 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.004767727528876053` | `0.003356715624260612` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m2_cubic_additive_gaussian_panel` | 2 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.013639326092868232` | `0.007936174521988028` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m2_cubic_additive_gaussian_panel` | 3 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.023486147218207788` | `0.0094604737329115` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m3_quadratic_observation_panel` | 1 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.019193705886081124` | `0.009752325667818997` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m3_quadratic_observation_panel` | 2 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.03129321843506539` | `0.020412476900283038` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m3_quadratic_observation_panel` | 3 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.04382014587030869` | `0.024759927152400538` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m4_nonlinear_transition_h2_panel` | 1 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.003959973468382497` | `0.0027845473251795513` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m4_nonlinear_transition_h2_panel` | 2 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.011803179526921333` | `0.00672650194376382` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m4_nonlinear_transition_h2_panel` | 3 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.019947969296938727` | `0.007317420543624172` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |

## Gradient Table

| Phase | Target | Dim | Particles | Seeds | Status | Mean grad err | Error-norm SE | Component SE | Uncertainty status | Band |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| `P1` | `direct_lgssm` |  | 4 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.926386260369295` | `1.207083658284481` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P1` |
| `P1` | `direct_lgssm` |  | 8 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.536590433427743` | `1.094375340541418` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P1` |
| `P1` | `direct_lgssm` |  | 16 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.0657898692896937` | `0.9318296506783856` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P1` |
| `P4` | `lgssm_2d_h25_rich` |  | 4 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.9263862603692952` | `1.2070836582844808` | `[1.3009205704948628, 0.6446499050518739]` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `lgssm_2d_h25_rich` |  | 8 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.5365904334277432` | `1.094375340541418` | `[1.1853360122037346, 0.44832163208069165]` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `lgssm_2d_h25_rich` |  | 16 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `1.065789869289693` | `0.9318296506783853` | `[0.8789267879165555, 0.4082857453229335]` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `predator_prey_rk4` |  | 4 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `None` | `[5.156918779547913]` | `component_uncertainty_no_reference_error_norm` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `predator_prey_rk4` |  | 8 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `None` | `[3.5626807432569527]` | `component_uncertainty_no_reference_error_norm` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `predator_prey_rk4` |  | 16 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `None` | `[0.8468858656543369]` | `component_uncertainty_no_reference_error_norm` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `range_bearing_4d_h20_rich` |  | 4 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `None` | `[16.895385592729657, 27.637881126248967]` | `component_uncertainty_no_reference_error_norm` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `range_bearing_4d_h20_rich` |  | 8 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `None` | `[14.928771120943312, 25.52145421045497]` | `component_uncertainty_no_reference_error_norm` | `N/A_DIAGNOSTIC_ONLY` |
| `P4` | `range_bearing_4d_h20_rich` |  | 16 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `None` | `None` | `[1.6383604663640128, 15.97536121845927]` | `component_uncertainty_no_reference_error_norm` | `N/A_DIAGNOSTIC_ONLY` |
| `P7` | `p44_m2_cubic_additive_gaussian_panel` | 1 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.029524084910676` | `0.01847405043235101` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m2_cubic_additive_gaussian_panel` | 2 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.06499442984563299` | `0.030992911409683854` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m2_cubic_additive_gaussian_panel` | 3 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.06362164595336371` | `0.02961618341911951` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m3_quadratic_observation_panel` | 1 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.06461331234951341` | `0.01916535783184411` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m3_quadratic_observation_panel` | 2 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.07784242317898067` | `0.015861513646255692` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m3_quadratic_observation_panel` | 3 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.1621731104857757` | `0.024876350827301125` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m4_nonlinear_transition_h2_panel` | 1 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.02568950031410824` | `0.015995308926548508` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m4_nonlinear_transition_h2_panel` | 2 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.06170757323925261` | `0.028894086841633547` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |
| `P7` | `p44_m4_nonlinear_transition_h2_panel` | 3 | 32 | 3 | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.05756962054882275` | `0.027403197391748572` | `None` | `reference_error_norm_uncertainty` | `N/A_DIAGNOSTIC_ONLY_IN_P7` |

## Blocked Adapter Table

| Phase | Target | Status | Missing item count |
| --- | --- | --- | ---: |
| `P1` | `direct_range_bearing_value` | `BLOCKED_REQUIRES_ADAPTER` | 5 |
| `P1` | `direct_range_bearing_stress` | `BLOCKED_REQUIRES_ADAPTER` | 3 |
| `P2` | `sv_1d_h18_rich` | `BLOCKED_REQUIRES_ADAPTER` | 4 |
| `P2` | `structural_ar1_quadratic_h16` | `BLOCKED_REQUIRES_ADAPTER` | 4 |
| `P6` | `p44_m2_cubic_additive_gaussian_panel` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `p44_m3_quadratic_observation_panel` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `p44_m4_nonlinear_transition_h2_panel` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `generalized_sv_native_raw_observation,generalized_sv_transformed_residual_diagnostic,generalized_sv_gaussian_mixture_or_moment_matched_approximation` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `spatial_sir_additive_gaussian_closure,spatial_sir_native_or_nongaussian_route` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `predator_prey_additive_gaussian_rk4_closure,predator_prey_native_or_nongaussian_route` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `generalized_sv_gaussian_mixture_or_moment_matched_approximation` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `generalized_sv_gaussian_mixture_or_moment_matched_approximation` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `generalized_sv_native_raw_observation` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `generalized_sv_native_raw_observation` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `generalized_sv_transformed_residual_diagnostic` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `generalized_sv_transformed_residual_diagnostic` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `predator_prey_native_or_nongaussian_route` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `predator_prey_native_or_nongaussian_route` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `spatial_sir_native_or_nongaussian_route` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `spatial_sir_native_or_nongaussian_route` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `sv_exact_transformed_log_chi_square_panel` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `sv_exact_transformed_log_chi_square_panel` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `sv_ksc_transformed_mixture_panel` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |
| `P6` | `sv_ksc_transformed_mixture_panel` | `BLOCKED_OR_UNSTRUCTURED_CALIBRATION_CONTEXT` | 1 |

## Historical-Only Table

| Group | Disposition | Replacement phase |
| --- | --- | --- |
| `historical_ledh_pfpf_ot_plan_family_2026_05_29` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `P9` |
| `old_v2_ledh_pfpf_ot_reports_outputs_2026_06_07` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `P2/P3/P4/P9` |
| `old_filter_oracle_ledh_rows` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `P5/P6/P7/P9` |
| `archival_mentions` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `P0/P9` |
| `annealed_transport_lgssm` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `P8` |
| `filterflow_matched_ledh_pfpf_ot` | `SCAFFOLDING_ONLY` | `P8` |
| `auxiliary_flow_source_faithful_repair` | `HISTORICAL_ONLY_NOT_EVIDENCE` | `P8` |

## Veto Diagnostics

| Diagnostic | Status |
| --- | --- |
| `guardrail_not_rerun_or_failed` | `False` |
| `registry_lane_missing_from_closeout` | `False` |
| `phase_result_missing` | `False` |
| `phase_json_missing` | `False` |
| `artifact_veto_not_clean` | `False` |
| `old_ledh_row_current_evidence` | `False` |
| `source_algorithm1_route_missing_from_value_or_gradient` | `False` |
| `promoted_row_without_threshold_status` | `False` |
| `missing_value_uncertainty` | `False` |
| `missing_gradient_uncertainty` | `False` |
| `unresolved_blocker_without_reason` | `False` |
| `historical_only_table_empty` | `False` |
| `run_manifest_missing` | `False` |
| `claude_review_not_converged` | `False` |
| `unsupported_superiority_or_default_claim` | `False` |

## Supersession Rule

- Old LEDH-PFPF-OT, dpf_ledh_pfpf_ot, and ledh_pfpf_ot artifacts are historical coverage only.
- Current source Algorithm 1 evidence must carry li_coates_algorithm1_ukf_covariance_lifecycle route identifiers.
- OT, annealed transport, and FilterFlow-matched residuals are not source Li-Coates Algorithm 1 core evidence.
- Finite diagnostic rows without reviewed promotion bands remain diagnostic-only.
- Future extension reruns require a separate reviewed plan.

## Nonclaims

- No production default or public API promotion is concluded.
- No HMC readiness is concluded.
- No universal Algorithm 1, DPF, OT, or FilterFlow superiority is concluded.
- No stochastic-resampling gradient correctness is concluded.
- Diagnostic rows without reviewed bands are not statistical-closeness certifications.
- Historical-only and scaffolding rows cannot be cited as current Algorithm 1 UKF evidence.
