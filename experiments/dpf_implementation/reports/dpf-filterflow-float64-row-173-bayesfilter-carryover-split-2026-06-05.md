# Result: Row 173 BayesFilter Carryover Split Probe

## Decision

`filterflow_float64_row_173_bayesfilter_carryover_split_carried_log_weight_edge`

## Hypothesis Classification

`h3_carried_log_weight_edge`

carried log-weight boundary materially reduces raw full-state/log-weight residual

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_bayesfilter_carryover_split_carried_log_weight_edge | h3_carried_log_weight_edge | {"all_vetoes_clear": true, "comparator_drift": false, "cpu_only_pass": true, "identity_tensors_finite": true, "mode_resampling_flags_match": true, "mode_scalar_gates_pass": true, "path_boundary_clean": true, "path_boundary_manifest": {"dsge_nawm_code_used": false, "filterflow_source_mutated": false, "highdim_lane_used_or_edited": false, "monograph_chapters_used_or_edited": false, "production_bayesfilter_code_used": false, "student_or_vendored_code_used_as_authority": false, "tests_code_used": false}, "raw_resampling_flags_match": true, "reference_status_validated": true, "required_identity_tensors_present": true, "scalar_gate_pass": true, "value_path_gate_pass": true} | single row and target time; no correctness claim | inspect BayesFilter carried log-weight update boundary and previous-time carryover | correctness, posterior correctness, production readiness, global agreement |

## Carryover Split Comparison

```json
{
  "classification": "h3_carried_log_weight_edge",
  "classification_evidence": {
    "collapse": true,
    "field": "same_tape_full_recorded_state_residual",
    "filterflow_max_abs": 1.0805911720979111e-11,
    "mode": "carry_log_weights_stop_gradient",
    "mode_gradient_delta": [
      5937.734618184093,
      -137.57404364709146
    ],
    "mode_max_abs": 1.1102230246251565e-16,
    "mode_max_abs_gradient_delta": 5937.734618184093,
    "raw_bayesfilter_max_abs": 15.29031158182802,
    "reduction_from_raw": 15.29031158182802
  },
  "classification_reason": "carried log-weight boundary materially reduces raw full-state/log-weight residual",
  "decision_precedence": [
    "h1 if missing/non-finite raw or mode identity tensors",
    "h2 if target transport-log-weight input mode reduces raw identity residuals",
    "h3 if carried log-weight mode reduces raw full-state/log-weight residuals",
    "h4 if carried log-likelihood mode reduces raw likelihood residuals",
    "h5 if proposal sample/post-particle modes reduce raw identity residuals",
    "h6 if custom transport gradient leaves residuals material",
    "h7 otherwise"
  ],
  "filterflow_identity_max_abs": {
    "same_tape_full_recorded_state_residual": 1.0805911720979111e-11,
    "same_tape_identity_residual": 3.4869329645914604e-13,
    "same_tape_post_log_weights_vjp": 0.0,
    "same_tape_post_particles_vjp": 1.075538971836846,
    "same_tape_post_state_identity_residual": 3.490541189421492e-13,
    "same_tape_pre_current_ll_carryover_vjp": 3.49220652395843e-13,
    "same_tape_pre_log_weights_carryover_vjp": 1.0810907724589924e-11,
    "same_tape_reconstructed_pre_particle_adjoint": 1.075538971836846,
    "same_tape_transport_matrix_vjp": 1.0756725353924719
  },
  "mode_summary": {
    "all_times_transport_log_weights_stop_gradient": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": true,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 1.1102230246251565e-16,
          "mode_minus_filterflow_max_abs_delta": 1.0805911720979111e-11,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 15.29031158182802
        },
        "same_tape_identity_residual": {
          "collapse": false,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 1.2212453270876722e-15
        },
        "same_tape_post_state_identity_residual": {
          "collapse": false,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741159,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 1.2212453270876722e-15
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 1.0810907724589924e-11,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 15.290311581828018
        }
      },
      "gradient_delta": [
        5937.734618184093,
        -137.57404364709146
      ],
      "max_abs_gradient_delta": 5937.734618184093,
      "scalar_delta": 6.2123888255882775e-09,
      "value_valid": true
    },
    "carry_both_stop_gradient": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": true,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 1.0805911720979111e-11,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 15.29031158182802
        },
        "same_tape_identity_residual": {
          "collapse": true,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 3.4869329645914604e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083742867
        },
        "same_tape_post_state_identity_residual": {
          "collapse": true,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 3.490541189421492e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083742867
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 3.49220652395843e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083742855
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 1.0810907724589924e-11,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 15.290311581828018
        }
      },
      "gradient_delta": [
        -9105.143875898348,
        -57.123649814928335
      ],
      "max_abs_gradient_delta": 9105.143875898348,
      "scalar_delta": 6.2123888255882775e-09,
      "value_valid": true
    },
    "carry_log_likelihoods_stop_gradient": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": true,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 1.0805911720979111e-11,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 15.29031158182802
        },
        "same_tape_identity_residual": {
          "collapse": true,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 3.4869329645914604e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083742867
        },
        "same_tape_post_state_identity_residual": {
          "collapse": true,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 3.490541189421492e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083742867
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 3.49220652395843e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083742855
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 1.0810907724589924e-11,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 15.290311581828018
        }
      },
      "gradient_delta": [
        -9105.143875898348,
        -57.123649814928335
      ],
      "max_abs_gradient_delta": 9105.143875898348,
      "scalar_delta": 6.2123888255882775e-09,
      "value_valid": true
    },
    "carry_log_weights_stop_gradient": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": true,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 1.1102230246251565e-16,
          "mode_minus_filterflow_max_abs_delta": 1.0805911720979111e-11,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 15.29031158182802
        },
        "same_tape_identity_residual": {
          "collapse": false,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 1.2212453270876722e-15
        },
        "same_tape_post_state_identity_residual": {
          "collapse": false,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741159,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 1.2212453270876722e-15
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 1.0810907724589924e-11,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 15.290311581828018
        }
      },
      "gradient_delta": [
        5937.734618184093,
        -137.57404364709146
      ],
      "max_abs_gradient_delta": 5937.734618184093,
      "scalar_delta": 6.2123888255882775e-09,
      "value_valid": true
    },
    "filterflow_custom_transport_gradient": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": false,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 15.29031158182802,
          "mode_minus_filterflow_max_abs_delta": 15.290311581838825,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_identity_residual": {
          "collapse": false,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742867,
          "mode_minus_filterflow_max_abs_delta": 0.673576308374117,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_post_state_identity_residual": {
          "collapse": false,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742867,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741171,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 15.290311581828018,
          "mode_minus_filterflow_max_abs_delta": 15.290311581838829,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 0.0
        }
      },
      "gradient_delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "max_abs_gradient_delta": 5.302734403676368,
      "scalar_delta": 6.2123888255882775e-09,
      "value_valid": true
    },
    "proposal_sample_noise_stop_gradient": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": true,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 5.131145508485702e-12,
          "mode_minus_filterflow_max_abs_delta": 1.0204226352783508e-11,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 15.290311581822888
        },
        "same_tape_identity_residual": {
          "collapse": true,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 4.103939410526891e-13,
          "mode_minus_filterflow_max_abs_delta": 3.612110610617947e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083738764
        },
        "same_tape_post_state_identity_residual": {
          "collapse": true,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 4.1033842990145786e-13,
          "mode_minus_filterflow_max_abs_delta": 3.610445276081009e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083738764
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 4.101996520233797e-13,
          "mode_minus_filterflow_max_abs_delta": 3.610445276081009e-13,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.6735763083738753
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 5.132338998237174e-12,
          "mode_minus_filterflow_max_abs_delta": 1.021049911287264e-11,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 15.290311581822886
        }
      },
      "gradient_delta": [
        5.3061005970430415,
        -0.1338614471382158
      ],
      "max_abs_gradient_delta": 5.3061005970430415,
      "scalar_delta": 6.2095750763546675e-09,
      "value_valid": true
    },
    "raw": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": false,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 15.29031158182802,
          "mode_minus_filterflow_max_abs_delta": 15.290311581838825,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_identity_residual": {
          "collapse": false,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742867,
          "mode_minus_filterflow_max_abs_delta": 0.673576308374117,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_post_state_identity_residual": {
          "collapse": false,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742867,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741171,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 15.290311581828018,
          "mode_minus_filterflow_max_abs_delta": 15.290311581838829,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 0.0
        }
      },
      "gradient_delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "max_abs_gradient_delta": 5.302734403676368,
      "scalar_delta": 6.2123888255882775e-09,
      "value_valid": true
    },
    "target_proposal_sample_filterflow_contract": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": false,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 15.290311581827403,
          "mode_minus_filterflow_max_abs_delta": 15.290311581838209,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 6.163958232718869e-13
        },
        "same_tape_identity_residual": {
          "collapse": false,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742867,
          "mode_minus_filterflow_max_abs_delta": 0.673576308374117,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_post_state_identity_residual": {
          "collapse": false,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742867,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741171,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 15.2903115818274,
          "mode_minus_filterflow_max_abs_delta": 15.29031158183821,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 6.181721801112872e-13
        }
      },
      "gradient_delta": [
        5.302734402777787,
        -0.13377652515431038
      ],
      "max_abs_gradient_delta": 5.302734402777787,
      "scalar_delta": 6.212417247297708e-09,
      "value_valid": true
    },
    "target_transport_log_weights_stop_gradient": {
      "field_rows": {
        "same_tape_full_recorded_state_residual": {
          "collapse": true,
          "field": "same_tape_full_recorded_state_residual",
          "filterflow_max_abs": 1.0805911720979111e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 1.1102230246251565e-16,
          "mode_minus_filterflow_max_abs_delta": 1.0805911720979111e-11,
          "raw_bayesfilter_max_abs": 15.29031158182802,
          "raw_material": true,
          "reduction_from_raw": 15.29031158182802
        },
        "same_tape_identity_residual": {
          "collapse": false,
          "field": "same_tape_identity_residual",
          "filterflow_max_abs": 3.4869329645914604e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 1.2212453270876722e-15
        },
        "same_tape_post_state_identity_residual": {
          "collapse": false,
          "field": "same_tape_post_state_identity_residual",
          "filterflow_max_abs": 3.490541189421492e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741159,
          "raw_bayesfilter_max_abs": 0.6735763083742867,
          "raw_material": true,
          "reduction_from_raw": 1.2212453270876722e-15
        },
        "same_tape_pre_current_ll_carryover_vjp": {
          "collapse": false,
          "field": "same_tape_pre_current_ll_carryover_vjp",
          "filterflow_max_abs": 3.49220652395843e-13,
          "gradient_tolerance": 0.0002,
          "material_reduction": false,
          "mode_material": true,
          "mode_max_abs": 0.6735763083742855,
          "mode_minus_filterflow_max_abs_delta": 0.6735763083741158,
          "raw_bayesfilter_max_abs": 0.6735763083742855,
          "raw_material": true,
          "reduction_from_raw": 0.0
        },
        "same_tape_pre_log_weights_carryover_vjp": {
          "collapse": true,
          "field": "same_tape_pre_log_weights_carryover_vjp",
          "filterflow_max_abs": 1.0810907724589924e-11,
          "gradient_tolerance": 0.0002,
          "material_reduction": true,
          "mode_material": false,
          "mode_max_abs": 0.0,
          "mode_minus_filterflow_max_abs_delta": 1.0810907724589924e-11,
          "raw_bayesfilter_max_abs": 15.290311581828018,
          "raw_material": true,
          "reduction_from_raw": 15.290311581828018
        }
      },
      "gradient_delta": [
        1562.7468585296956,
        25.57433805656462
      ],
      "max_abs_gradient_delta": 1562.7468585296956,
      "scalar_delta": 6.2123888255882775e-09,
      "value_valid": true
    }
  },
  "ordered_rule_audit": {
    "h2_did_not_fire_reason": "target_transport_log_weights_stop_gradient did not materially reduce same_tape_identity_residual or same_tape_post_state_identity_residual under the accepted ordered rule, even though it collapses the full-recorded-state/log-weight fields as explanatory evidence",
    "h2_target_transport_fields": {
      "same_tape_identity_residual": {
        "collapse": false,
        "material_reduction": false,
        "mode_max_abs": 0.6735763083742855,
        "raw_bayesfilter_max_abs": 0.6735763083742867,
        "reduction_from_raw": 1.2212453270876722e-15
      },
      "same_tape_post_state_identity_residual": {
        "collapse": false,
        "material_reduction": false,
        "mode_max_abs": 0.6735763083742855,
        "raw_bayesfilter_max_abs": 0.6735763083742867,
        "reduction_from_raw": 1.2212453270876722e-15
      }
    },
    "target_transport_log_weight_fields_explanatory_only": {
      "same_tape_full_recorded_state_residual": {
        "collapse": true,
        "material_reduction": true,
        "mode_max_abs": 1.1102230246251565e-16,
        "raw_bayesfilter_max_abs": 15.29031158182802,
        "reduction_from_raw": 15.29031158182802
      },
      "same_tape_pre_log_weights_carryover_vjp": {
        "collapse": true,
        "material_reduction": true,
        "mode_max_abs": 0.0,
        "raw_bayesfilter_max_abs": 15.290311581828018,
        "reduction_from_raw": 15.290311581828018
      }
    }
  },
  "raw_bayesfilter_identity_max_abs": {
    "same_tape_full_recorded_state_residual": 15.29031158182802,
    "same_tape_identity_residual": 0.6735763083742867,
    "same_tape_post_log_weights_vjp": 0.0,
    "same_tape_post_particles_vjp": 15.33929208686093,
    "same_tape_post_state_identity_residual": 0.6735763083742867,
    "same_tape_pre_current_ll_carryover_vjp": 0.6735763083742855,
    "same_tape_pre_log_weights_carryover_vjp": 15.290311581828018,
    "same_tape_reconstructed_pre_particle_adjoint": 15.33929208686093,
    "same_tape_transport_matrix_vjp": 15.358019754965156
  }
}
```

## Veto Status

```json
{
  "all_vetoes_clear": true,
  "comparator_drift": false,
  "cpu_only_pass": true,
  "cpu_rows": {
    "filterflow": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:all_times_transport_log_weights_stop_gradient": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:carry_both_stop_gradient": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:carry_log_likelihoods_stop_gradient": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:carry_log_weights_stop_gradient": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:filterflow_custom_transport_gradient": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:proposal_sample_noise_stop_gradient": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:raw": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:target_proposal_sample_filterflow_contract": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "mode:target_transport_log_weights_stop_gradient": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "parent": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    },
    "raw_bayesfilter": {
      "cuda_visible_devices": "-1",
      "gpu_devices_visible": [],
      "pass": true,
      "pre_import_cuda_visible_devices": "-1"
    }
  },
  "identity_tensors_finite": true,
  "mode_resampling_flags_match": true,
  "mode_scalar_gates_pass": true,
  "path_boundary_clean": true,
  "path_boundary_manifest": {
    "dsge_nawm_code_used": false,
    "filterflow_source_mutated": false,
    "highdim_lane_used_or_edited": false,
    "monograph_chapters_used_or_edited": false,
    "production_bayesfilter_code_used": false,
    "student_or_vendored_code_used_as_authority": false,
    "tests_code_used": false
  },
  "raw_resampling_flags_match": true,
  "reference_status_validated": true,
  "required_identity_tensors_present": true,
  "scalar_gate_pass": true,
  "value_path_gate_pass": true
}
```

## Base VJP Comparison

```json
{
  "first_gradient_delta_over_tolerance": {
    "field": "manual_proposal_mean",
    "row": {
      "bayesfilter_max_abs": 0.7827423714161357,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.7827423714161357,
      "shape_match": true,
      "sum_delta": 0.4898093699805401
    },
    "status": "delta",
    "tolerance": 0.0002
  },
  "first_value_delta_over_tolerance": {
    "status": "no_delta",
    "tolerance": 5e-08
  },
  "max_abs_total_gradient_delta": 5.302734403676368,
  "resampling_flags_match": true,
  "scalar_delta": 6.2123888255882775e-09,
  "total_gradient_delta": [
    5.302734403676368,
    -0.1337765252068337
  ]
}
```

## Prior Identity Route

```json
{
  "decision": "filterflow_float64_row_173_state_update_identity_route_bayesfilter_identity_residual",
  "hypothesis_classification": "h2_bayesfilter_identity_residual_filterflow_identity_clean",
  "path": "/home/chakwong/BayesFilter/experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_state_update_identity_route_2026-06-05.json",
  "reproducibility_digest": "ff6b7ac7f2646b502b736d1d71d74f6f879cf14d3590dad6f89d4d5ade8857f6",
  "status": "loaded"
}
```

## Model Contract

```json
{
  "T": 100,
  "artifact_tag": "row-173-bayesfilter-carryover-split",
  "batch_size": 1,
  "convergence_threshold": 1e-06,
  "data_seed": 123,
  "dtype": "float64",
  "epsilon": 0.25,
  "filter_seed": 1234,
  "gradient_tolerance": 0.0002,
  "identity_fields": [
    "same_tape_identity_residual",
    "same_tape_post_state_identity_residual",
    "same_tape_full_recorded_state_residual",
    "same_tape_pre_log_weights_carryover_vjp",
    "same_tape_pre_current_ll_carryover_vjp",
    "same_tape_post_particles_vjp",
    "same_tape_post_log_weights_vjp",
    "same_tape_transport_matrix_vjp",
    "same_tape_reconstructed_pre_particle_adjoint"
  ],
  "max_iter": 500,
  "mesh_index": 173,
  "model": "filterflow_simple_linear_smoothness_constant_velocity_lgssm",
  "num_particles": 50,
  "observation_covariance": [
    [
      0.01
    ]
  ],
  "observation_matrix": [
    [
      1.0,
      0.0
    ]
  ],
  "resampling_neff": 0.9999,
  "scaling": 0.85,
  "split_modes": [
    "raw",
    "target_transport_log_weights_stop_gradient",
    "all_times_transport_log_weights_stop_gradient",
    "carry_log_weights_stop_gradient",
    "carry_log_likelihoods_stop_gradient",
    "carry_both_stop_gradient",
    "target_proposal_sample_filterflow_contract",
    "proposal_sample_noise_stop_gradient",
    "filterflow_custom_transport_gradient"
  ],
  "target_time_index": 93,
  "theta": [
    0.9710526315789474,
    0.9842105263157894
  ],
  "transition_covariance": [
    [
      0.3333333333333333,
      0.5
    ],
    [
      0.5,
      1.0
    ]
  ],
  "transition_matrix": "A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]",
  "value_tolerance": 5e-08
}
```

## Run Manifest

```json
{
  "branch": "main",
  "command": "CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_bayesfilter_carryover_split_tf",
  "commit": "7ccb9c39883471c2d5ec2891cbf33b9ed436bada",
  "cpu_only": true,
  "cuda_visible_devices": "-1",
  "dirty_state_summary": "M docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md\n M docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md\n M docs/references.bib\n M experiments/controlled_dpf_baseline/README.md\n?? .cache/\n?? .claude/\n?? .local_sources/\n?? .localenv/\n?? .localsource/\n?? AGENTS.md\n?? CLAUDE.md\n?? bayesfilter/highdim/\n?? docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-review-loop-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-review-loop-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-exact-arithmetic-continuation-debug-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-exact-arithmetic-continuation-debug-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-surface-window-coverage-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-result-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-review-loop-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-plan-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-result-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-review-loop-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-matrix-gradient-parameterization-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-matrix-gradient-parameterization-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-debug-summary-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-historical-transport-vjp-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-historical-transport-vjp-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-historical-transport-vjp-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-plan-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-result-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-review-loop-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-plan-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-result-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-review-loop-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-boundary-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-plan-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-result-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-review-loop-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-scalar-additivity-route-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-scalar-additivity-route-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-plan-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-result-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-review-loop-2026-06-05.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-92-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-94-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-clipping-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-clipping-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-clipping-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-gradient-discrepancy-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-0-19-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-100-119-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-120-139-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-140-159-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-160-179-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-180-199-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-20-39-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-200-219-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-220-239-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-240-259-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-260-279-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-280-299-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-300-319-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-320-339-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-340-359-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-360-379-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-380-399-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-40-59-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-60-79-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-80-99-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-py311-compat-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-py311-compat-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-citation-coverage-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-extraction-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-doc-patch-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-baseline-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-reference-test-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-student-comparison-context-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-bias-proxy-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-deferred-neural-path-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-differentiable-resampling-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-resampling-test-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-excluded-flow-risk-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-kernel-pff-exclusion-check-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-particle-flow-pfpf-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-differentiable-objective-gradient-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-downstream-evidence-requirements-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-objective-classification-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-benchmark-ladder-matrix-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-cpu-gpu-runtime-policy-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-seed-uncertainty-policy-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-benchmark-ladder-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-api-review-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-decision-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf7-final-audit-implementation-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-final-audit-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-handoff-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-sv-test-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-master-program-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-ladder-master-program-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ot-backend-governance-correction-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-backend-governance-correction-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p0-scope-and-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p0-scope-and-contract-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-structural-ar1-linear-mle-test-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ar1-linear-mle-test-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ssm-interface-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ssm-interface-result-2026-05-29.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase-subplans-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-result-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-result-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-addenda-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-claude-review-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-promotion-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-filtering-scalar-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-gradient-feasibility-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-mathdevmcp-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-octave-compatibility-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-octave-compatibility-result-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-reproducibility-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-result-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-claude-review-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-derivation-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-mathdevmcp-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claim-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-coverage-and-omission-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-proposition-proof-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-anchor-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-proposition-humanization-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-reader-comprehension-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-gradient-teaching-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-reader-panel-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-algorithm-choices-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-backward-snowball-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-citation-venue-metadata-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-claim-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-forward-snowball-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-gradient-derivation-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-omitted-paper-risk-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-reference-example-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-backward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-bayesfilter-translation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claim-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-code-crosswalk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-equation-by-equation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-fixed-branch-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-forward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-gradient-derivation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-fixed-branch-derivative-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-inventory-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section1-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section2-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section3-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section5-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-backward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-claim-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-eight-issue-control-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-equation-count-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-fixed-branch-gradient-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-forward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section1-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section2-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section3-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section5-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-inventory-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-finite-difference-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-fixed-branch-scalar-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-gradient-equation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-gradient-teaching-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-equation-and-size-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-merge-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-teachability-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-equation-to-specification-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-finite-difference-protocol-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-fixed-branch-implementation-ready-spec-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-full-algorithm-gap-register-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-implementation-readiness-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-implementation-specification-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integration-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-readable-orientation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-eleven-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-p22-preservation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-backward-snowball-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-chair-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-citation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-citation-venue-metadata-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-claim-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-forward-snowball-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-cleanup-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-implementation-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-omitted-paper-risk-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-source-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-claim-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-five-gap-closure-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-source-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-chemist-gap-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-human-facing-cleanup-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-implementation-gap-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-validation-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-chair-reader-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-equation-audit-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-implementation-readiness-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-notation-dimension-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-numerical-sanity-test-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-source-fidelity-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-submission-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-submission-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-algorithm-provenance-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-critical-equation-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-critical-equation-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-kr-preconditioning-jacobian-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-mass-normalizer-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-notation-shape-contract-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-proposition2-derivative-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-expansion-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-gradient-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-chair-perspective-punch-list-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-junior-reader-2026-06-05.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-gradient-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-source-support-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-validation-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-junior-reader-remediation-plan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-mathematical-expansion-pass-plan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-gap-remediation-plan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-standard-upgrade-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-scholarly-grounding-and-engineering-exposition-remediation-plan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-section20-mathematical-selection-argument-plan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-conclusion-and-panel-positioning-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-gradient-path-implementation-completeness-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-neighboring-method-comparison-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-opening-and-conceptual-spine-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-value-path-implementation-completeness-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-worked-example-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-substantial-scholarly-remediation-plan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-result-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-result-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-result-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-result-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase7-integration-closeout-subplan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-source-governance-claude-review-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-audit-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-result-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-review-2026-05-27.md\n?? experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md\n?? experiments/dpf_implementation/\n?? tests/highdim/\n?? third_party/",
  "gpu_devices_visible": [],
  "json_path": "/home/chakwong/BayesFilter/experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_bayesfilter_carryover_split_2026-06-05.json",
  "modes": [
    "raw",
    "target_transport_log_weights_stop_gradient",
    "all_times_transport_log_weights_stop_gradient",
    "carry_log_weights_stop_gradient",
    "carry_log_likelihoods_stop_gradient",
    "carry_both_stop_gradient",
    "target_proposal_sample_filterflow_contract",
    "proposal_sample_noise_stop_gradient",
    "filterflow_custom_transport_gradient"
  ],
  "package_versions": {
    "tensorflow": "2.19.1",
    "tensorflow_probability": "0.25.0"
  },
  "plan_path": "docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md",
  "pre_import_cuda_visible_devices": "-1",
  "python_version": "3.11.14",
  "report_path": "/home/chakwong/BayesFilter/experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-bayesfilter-carryover-split-2026-06-05.md",
  "result_path": "docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-result-2026-06-05.md",
  "target_time_index": 93,
  "wall_time_seconds": 436.58850761991926
}
```

## Non-Implications

- no correctness claim for FilterFlow or BayesFilter
- no analytic-gradient correctness claim
- no posterior correctness claim
- no global smoothness-surface agreement claim
- no claim that either implementation is mathematically authoritative
- no claim that any boundary mode is a code fix
- no production readiness or public API readiness
- no monograph, highdim, DSGE, NAWM, or banking/model-risk claim

## Reproducibility Digest

`01fbbff57a67a274ed1f4734112f7caded905e71e489a9f7ad0ac9de3bd57633`
