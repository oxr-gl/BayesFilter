# Result: FilterFlow Float64 Row 173 VJP Decomposition

## Decision

`filterflow_float64_row_173_vjp_gradient_difference_localized`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_vjp_gradient_difference_localized | first VJP delta: {'status': 'delta', 'field': 'manual_proposal_mean', 'row': {'filterflow_max_abs': 0.0, 'bayesfilter_max_abs': 0.7827423714161357, 'max_abs_delta': 0.7827423714161357, 'sum_delta': 0.4898093699805401, 'shape_match': True, 'finite': True}, 'tolerance': 0.0002} | scalar/value path stayed within tolerance | single row and single time index; no correctness claim | inspect exact arithmetic for the first VJP-delta field and patch only if the executable FilterFlow rule is unambiguous | correctness of either implementation, analytic gradient correctness, production readiness |

## Model Contract

| Key | Value |
| --- | --- |
| `model` | `filterflow_simple_linear_smoothness_constant_velocity_lgssm` |
| `mesh_index` | `173` |
| `theta` | `[0.9710526315789474, 0.9842105263157894]` |
| `target_time_index` | `93` |
| `artifact_tag` | `row-173-time-93` |
| `transition_matrix` | `A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]` |
| `transition_covariance` | `[[0.3333333333333333, 0.5], [0.5, 1.0]]` |
| `observation_matrix` | `[[1.0, 0.0]]` |
| `observation_covariance` | `[[0.01]]` |
| `T` | `100` |
| `batch_size` | `1` |
| `num_particles` | `50` |
| `data_seed` | `123` |
| `filter_seed` | `1234` |
| `epsilon` | `0.25` |
| `scaling` | `0.85` |
| `convergence_threshold` | `1e-06` |
| `max_iter` | `500` |
| `resampling_neff` | `0.9999` |
| `dtype` | `float64` |

## Comparison

```json
{
  "adjoint_decomposition": {
    "bayesfilter_full_recorded_state_identity_holds": false,
    "bayesfilter_full_recorded_state_identity_max_abs": 15.29031158182802,
    "bayesfilter_post_state_identity_holds": false,
    "bayesfilter_post_state_identity_max_abs": 0.6735763083742867,
    "bayesfilter_same_tape_identity_holds": false,
    "bayesfilter_same_tape_identity_max_abs": 0.6735763083742867,
    "filterflow_full_recorded_state_identity_holds": true,
    "filterflow_full_recorded_state_identity_max_abs": 1.0805911720979111e-11,
    "filterflow_post_state_identity_holds": true,
    "filterflow_post_state_identity_max_abs": 3.490541189421492e-13,
    "filterflow_same_tape_identity_holds": true,
    "filterflow_same_tape_identity_max_abs": 3.4869329645914604e-13,
    "full_recorded_state_identity_contract": "pre_particles_adjoint == post-state VJP plus recorded carryover VJPs through pre_log_weights, pre_current_log_likelihoods, and log_ess",
    "post_state_identity_contract": "pre_particles_adjoint == VJP(post_particles wrt pre_particles) + VJP(post_log_weights wrt pre_particles)",
    "rows": {
      "carryover_pre_particle_adjoint": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.0,
        "status": "compared"
      },
      "current_increment_pre_particle_adjoint": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.0,
        "status": "compared"
      },
      "direct_pre_particle_adjoint": {
        "bayesfilter_max_abs": 0.032745181880207294,
        "filterflow_max_abs": 0.03274518187397153,
        "max_abs_delta": 3.268496931441156e-11,
        "status": "compared"
      },
      "implicit_pre_particle_adjoint": {
        "bayesfilter_max_abs": 15.029585354730424,
        "filterflow_max_abs": 1.075672535392472,
        "max_abs_delta": 14.961877181675323,
        "status": "compared"
      },
      "same_tape_full_recorded_state_residual": {
        "bayesfilter_max_abs": 15.29031158182802,
        "filterflow_max_abs": 1.0805911720979111e-11,
        "max_abs_delta": 15.290311581838825,
        "status": "compared"
      },
      "same_tape_full_recorded_state_vjp": {
        "bayesfilter_max_abs": 30.301169268454217,
        "filterflow_max_abs": 1.0755389718368409,
        "max_abs_delta": 30.252188763517033,
        "status": "compared"
      },
      "same_tape_identity_residual": {
        "bayesfilter_max_abs": 0.6735763083742867,
        "filterflow_max_abs": 3.4869329645914604e-13,
        "max_abs_delta": 0.673576308374117,
        "status": "compared"
      },
      "same_tape_log_ess_carryover_vjp": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.0,
        "status": "compared"
      },
      "same_tape_post_log_weights_vjp": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.0,
        "status": "compared"
      },
      "same_tape_post_particles_vjp": {
        "bayesfilter_max_abs": 15.33929208686093,
        "filterflow_max_abs": 1.075538971836846,
        "max_abs_delta": 15.290311581913166,
        "status": "compared"
      },
      "same_tape_post_state_identity_residual": {
        "bayesfilter_max_abs": 0.6735763083742867,
        "filterflow_max_abs": 3.490541189421492e-13,
        "max_abs_delta": 0.6735763083741171,
        "status": "compared"
      },
      "same_tape_post_state_vjp": {
        "bayesfilter_max_abs": 15.33929208686093,
        "filterflow_max_abs": 1.075538971836846,
        "max_abs_delta": 15.290311581913166,
        "status": "compared"
      },
      "same_tape_pre_current_ll_carryover_vjp": {
        "bayesfilter_max_abs": 0.6735763083742855,
        "filterflow_max_abs": 3.49220652395843e-13,
        "max_abs_delta": 0.6735763083741158,
        "status": "compared"
      },
      "same_tape_pre_log_weights_carryover_vjp": {
        "bayesfilter_max_abs": 15.290311581828018,
        "filterflow_max_abs": 1.0810907724589924e-11,
        "max_abs_delta": 15.290311581838829,
        "status": "compared"
      },
      "same_tape_reconstructed_pre_particle_adjoint": {
        "bayesfilter_max_abs": 15.33929208686093,
        "filterflow_max_abs": 1.075538971836846,
        "max_abs_delta": 15.290311581913164,
        "status": "compared"
      },
      "same_tape_transport_matrix_vjp": {
        "bayesfilter_max_abs": 15.358019754965156,
        "filterflow_max_abs": 1.0756725353924719,
        "max_abs_delta": 15.29031158191028,
        "status": "compared"
      }
    },
    "same_tape_identity_contract": "pre_particles_adjoint == T^T post_particles_adjoint + VJP(transport_matrix wrt pre_particles)"
  },
  "filterflow_proposal_mean_internal_probe": {
    "adjoint_delta": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "adjoint_delta_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "manual_proposal_mean_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "proposal_mean_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "value_delta": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "value_delta_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ]
  },
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
  "gradient_deltas": {
    "fresh_dist_log_prob": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "fresh_proposal_loc": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "fresh_proposal_mean": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "increment": {
      "bayesfilter_max_abs": 1.0,
      "filterflow_max_abs": 1.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "log_ess": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "manual_dist_log_prob": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "manual_proposal_mean": {
      "bayesfilter_max_abs": 0.7827423714161357,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.7827423714161357,
      "shape_match": true,
      "sum_delta": 0.4898093699805401
    },
    "normalized": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "observation_ll": {
      "bayesfilter_max_abs": 0.02912639608646427,
      "filterflow_max_abs": 0.029126396082423307,
      "finite": true,
      "max_abs_delta": 1.487546544276519e-11,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "post_log_weights": {
      "bayesfilter_max_abs": 0.02912639608646427,
      "filterflow_max_abs": 0.029126396082423307,
      "finite": true,
      "max_abs_delta": 1.487546544276519e-11,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "post_particles": {
      "bayesfilter_max_abs": 0.030135380107735612,
      "filterflow_max_abs": 0.030135380102742214,
      "finite": true,
      "max_abs_delta": 6.456676859833976e-11,
      "shape_match": true,
      "sum_delta": 6.286444698133664e-10
    },
    "post_update_log_likelihoods": {
      "bayesfilter_max_abs": 1.0,
      "filterflow_max_abs": 1.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "post_update_log_weights": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "pre_current_log_likelihoods": {
      "bayesfilter_max_abs": 1.0,
      "filterflow_max_abs": 1.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "pre_log_weights": {
      "bayesfilter_max_abs": 1.1695816018044372,
      "filterflow_max_abs": 1.1695816019013177,
      "finite": true,
      "max_abs_delta": 1.5881858050903475e-09,
      "shape_match": true,
      "sum_delta": 3.98580155547279e-08
    },
    "pre_particles": {
      "bayesfilter_max_abs": 15.010857686626197,
      "filterflow_max_abs": 1.0755389718368462,
      "finite": true,
      "max_abs_delta": 14.961877181678206,
      "shape_match": true,
      "sum_delta": 44.1999619102195
    },
    "proposal_dist_log_prob": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "proposal_ll": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.029126396082423307,
      "finite": true,
      "max_abs_delta": 0.029126396082423307,
      "shape_match": true,
      "sum_delta": 1.0
    },
    "proposal_loc": {
      "bayesfilter_max_abs": 0.7827423714161357,
      "filterflow_max_abs": 5.445643935786393e-13,
      "finite": true,
      "max_abs_delta": 0.7827423714163882,
      "shape_match": true,
      "sum_delta": 0.48980936997425867
    },
    "proposal_mean": {
      "bayesfilter_max_abs": 0.7827423714161357,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.7827423714161357,
      "shape_match": true,
      "sum_delta": 0.4898093699805401
    },
    "proposed_particles": {
      "bayesfilter_max_abs": 0.7827423714161357,
      "filterflow_max_abs": 5.445643935786393e-13,
      "finite": true,
      "max_abs_delta": 0.7827423714163882,
      "shape_match": true,
      "sum_delta": 0.48980936997425867
    },
    "transition_ll": {
      "bayesfilter_max_abs": 0.02912639608646427,
      "filterflow_max_abs": 0.029126396082423307,
      "finite": true,
      "max_abs_delta": 1.487546544276519e-11,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "transport_matrix": {
      "bayesfilter_max_abs": 15.683856022178455,
      "filterflow_max_abs": 15.683856019586806,
      "finite": true,
      "max_abs_delta": 3.360472966562611e-08,
      "shape_match": true,
      "sum_delta": 8.271588740171865e-06
    },
    "unnormalized": {
      "bayesfilter_max_abs": 0.02912639608646427,
      "filterflow_max_abs": 0.029126396082423307,
      "finite": true,
      "max_abs_delta": 1.487546544276519e-11,
      "shape_match": true,
      "sum_delta": 0.0
    }
  },
  "interpretation": "first_vjp_difference_field_manual_proposal_mean",
  "local_post_particle_adjoint": {
    "first_delta_over_tolerance": {
      "field": "manual_proposal_mean_to_post_particles",
      "row": {
        "finite": true,
        "max_abs_delta": 0.2638596946097245,
        "shape_match": true,
        "sum_delta": -1.5262070898616025
      },
      "status": "delta",
      "tolerance": 0.0002
    },
    "interpretation": "first_local_post_particle_adjoint_delta_manual_proposal_mean_to_post_particles",
    "rows": {
      "fresh_proposal_loc_to_post_particles": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.0,
        "status": "compared",
        "sum_delta": 0.0
      },
      "fresh_proposal_mean_to_post_particles": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.0,
        "status": "compared",
        "sum_delta": 0.0
      },
      "increment_to_post_particles": {
        "bayesfilter_max_abs": 0.030135380107735612,
        "filterflow_max_abs": 0.030135380102742214,
        "max_abs_delta": 6.456676859833976e-11,
        "status": "compared",
        "sum_delta": -6.286442234013177e-10
      },
      "manual_proposal_mean_to_post_particles": {
        "bayesfilter_max_abs": 0.2638596946097245,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.2638596946097245,
        "status": "compared",
        "sum_delta": -1.5262070898616025
      },
      "observation_ll_to_post_particles": {
        "bayesfilter_max_abs": 0.014874061645584816,
        "filterflow_max_abs": 0.01487406164244211,
        "max_abs_delta": 5.293279703444398e-12,
        "status": "compared",
        "sum_delta": -3.714896931196997e-11
      },
      "proposal_ll_to_post_particles": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.0,
        "status": "compared",
        "sum_delta": 0.0
      },
      "proposal_loc_to_post_particles": {
        "bayesfilter_max_abs": 0.2638596946097245,
        "filterflow_max_abs": 3.7558963348749376e-14,
        "max_abs_delta": 0.26385969460972303,
        "status": "compared",
        "sum_delta": -1.5262070898617979
      },
      "proposal_mean_to_post_particles": {
        "bayesfilter_max_abs": 0.2638596946097245,
        "filterflow_max_abs": 0.0,
        "max_abs_delta": 0.2638596946097245,
        "status": "compared",
        "sum_delta": -1.5262070898616025
      },
      "proposed_particles_to_post_particles": {
        "bayesfilter_max_abs": 0.2638596946097245,
        "filterflow_max_abs": 3.7558963348749376e-14,
        "max_abs_delta": 0.26385969460972303,
        "status": "compared",
        "sum_delta": -1.5262070898617979
      },
      "transition_ll_to_post_particles": {
        "bayesfilter_max_abs": 0.035592916948155556,
        "filterflow_max_abs": 0.035592916940351535,
        "max_abs_delta": 6.438450467216583e-11,
        "status": "compared",
        "sum_delta": -5.914950525903739e-10
      },
      "unnormalized_to_post_particles": {
        "bayesfilter_max_abs": 0.030135380107735612,
        "filterflow_max_abs": 0.030135380102742214,
        "max_abs_delta": 6.456676859833976e-11,
        "status": "compared",
        "sum_delta": -6.286442234013177e-10
      }
    },
    "status": "compared"
  },
  "max_abs_total_gradient_delta": 5.302734403676368,
  "parameter_path_adjoint": {
    "first_delta_over_tolerance": {
      "field": "manual_proposal_mean",
      "row": {
        "bayesfilter_max_abs": 16020.8501301383,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 16020.8501301383,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 15337.646304417973
      },
      "status": "delta",
      "tolerance": 0.0002
    },
    "interpretation": "first_parameter_path_delta_manual_proposal_mean",
    "rows": {
      "fresh_dist_log_prob": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "fresh_proposal_loc": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "fresh_proposal_mean": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "increment": {
        "bayesfilter_max_abs": 11886.758024308658,
        "filterflow_max_abs": 11886.75807955571,
        "finite": true,
        "max_abs_delta": 5.524705193238333e-05,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -5.596265714302717e-05
      },
      "log_ess": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "manual_dist_log_prob": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "manual_proposal_mean": {
        "bayesfilter_max_abs": 16020.8501301383,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 16020.8501301383,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 15337.646304417973
      },
      "normalized": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "observation_ll": {
        "bayesfilter_max_abs": 9950.289261741085,
        "filterflow_max_abs": 9950.289320089687,
        "finite": true,
        "max_abs_delta": 5.834860166942235e-05,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -5.880881360553758e-05
      },
      "post_log_weights": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "post_particles": {
        "bayesfilter_max_abs": 11600.390548457051,
        "filterflow_max_abs": 11600.3906035415,
        "finite": true,
        "max_abs_delta": 5.508444883162156e-05,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -5.58000540422654e-05
      },
      "post_update_log_likelihoods": {
        "bayesfilter_max_abs": 9110.446610302024,
        "filterflow_max_abs": 9105.143875898348,
        "finite": true,
        "max_abs_delta": 5.302734403676368,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 5.168957878469534
      },
      "post_update_log_weights": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "pre_current_log_likelihoods": {
        "bayesfilter_max_abs": 1001.4592302010708,
        "filterflow_max_abs": 1001.4593201784609,
        "finite": true,
        "max_abs_delta": 8.997739007554628e-05,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 9.012760136783982e-05
      },
      "pre_log_weights": {
        "bayesfilter_max_abs": 10711.480505784251,
        "filterflow_max_abs": 10711.474356632394,
        "finite": true,
        "max_abs_delta": 0.006149151857243851,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -0.005965334844745485
      },
      "pre_particles": {
        "bayesfilter_max_abs": 7155.78166007807,
        "filterflow_max_abs": 12879.778839173718,
        "finite": true,
        "max_abs_delta": 20035.560499251787,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -19379.173698334445
      },
      "proposal_dist_log_prob": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "proposal_ll": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "proposal_loc": {
        "bayesfilter_max_abs": 16020.8501301383,
        "filterflow_max_abs": 8012.192846756851,
        "finite": true,
        "max_abs_delta": 24033.04297689515,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 22864.454026339823
      },
      "proposal_mean": {
        "bayesfilter_max_abs": 16020.8501301383,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 16020.8501301383,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 15337.646304417973
      },
      "proposed_particles": {
        "bayesfilter_max_abs": 16020.8501301383,
        "filterflow_max_abs": 8012.192846756851,
        "finite": true,
        "max_abs_delta": 24033.04297689515,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 22864.454026339823
      },
      "transition_ll": {
        "bayesfilter_max_abs": 12100.902535469098,
        "filterflow_max_abs": 12100.902593110097,
        "finite": true,
        "max_abs_delta": 5.764099842053838e-05,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -5.8236949598722276e-05
      },
      "transport_matrix": {
        "bayesfilter_max_abs": 10068.711930779455,
        "filterflow_max_abs": 10068.711052550034,
        "finite": true,
        "max_abs_delta": 0.0008782294207776431,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0008423570302511507
      },
      "unnormalized": {
        "bayesfilter_max_abs": 11886.758024308658,
        "filterflow_max_abs": 11886.75807955571,
        "finite": true,
        "max_abs_delta": 5.524705193238333e-05,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -5.596265714302717e-05
      }
    },
    "status": "compared"
  },
  "proposal_sample_gradient_contract": {
    "bayesfilter_contract": "Probe BayesFilter proposal_dist.sample and a manual distribution built from the explicit proposal mean under the downstream upstream gradient for proposed_particles.",
    "filterflow_contract": "Probe actual FilterFlow proposal_dist.sample and a manual distribution built from the explicit proposal mean under the downstream upstream gradient for proposed_particles.",
    "first_value_delta_over_tolerance": {
      "status": "no_delta",
      "tolerance": 5e-08
    },
    "first_vjp_delta_over_tolerance": {
      "field": "actual_sample_to_manual_proposal_mean",
      "row": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.7827423714161357,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699805404
      },
      "status": "delta",
      "tolerance": 0.0002
    },
    "interpretation": "proposal_sample_gradient_contract_differs",
    "status": "compared",
    "value_rows": {
      "actual_sample_minus_manual_mean": {
        "bayesfilter_max_abs": 1.2039904106672097,
        "filterflow_max_abs": 1.2039904106672097,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "manual_probe_minus_actual_sample": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "manual_probe_minus_manual_mean": {
        "bayesfilter_max_abs": 1.2039904106672097,
        "filterflow_max_abs": 1.2039904106672097,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      }
    },
    "vjp_rows": {
      "actual_sample_to_fresh_proposal_loc": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "actual_sample_to_fresh_proposal_mean": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "actual_sample_to_manual_proposal_mean": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.7827423714161357,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699805404
      },
      "actual_sample_to_post_particles": {
        "bayesfilter_max_abs": 0.2638596946097245,
        "filterflow_max_abs": 3.7558963348749376e-14,
        "finite": true,
        "max_abs_delta": 0.26385969460972303,
        "shape_match": true,
        "status": "compared",
        "sum_delta": -1.5262070898617979
      },
      "actual_sample_to_proposal_loc": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 5.445643935786393e-13,
        "finite": true,
        "max_abs_delta": 0.7827423714163882,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699742584
      },
      "actual_sample_to_proposal_mean": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.7827423714161357,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699805404
      },
      "manual_probe_sample_to_manual_proposal_mean": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 5.445643935786393e-13,
        "finite": true,
        "max_abs_delta": 0.7827423714163882,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699742584
      },
      "manual_probe_sum_to_manual_proposal_mean": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      }
    }
  },
  "proposal_topology_probe": {
    "bayesfilter_contract": "Difference-audit probe for the optimal-proposal graph topology. BayesFilter constructs the proposal distribution in the replay loop and exposes explicit loc/mean/log-prob paths for comparison against executable FilterFlow.",
    "filterflow_contract": "Difference-audit probe for the optimal-proposal graph topology. The executable FilterFlow scalar samples from one proposal distribution and evaluates proposal log probability through the proposal-model loglikelihood method, which constructs a fresh proposal distribution.",
    "first_gradient_delta_over_tolerance": {
      "field": "target_to_manual_proposal_mean",
      "row": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.7827423714161357,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699805404
      },
      "status": "delta",
      "tolerance": 0.0002
    },
    "first_log_prob_parameter_delta_over_tolerance": {
      "status": "no_delta",
      "tolerance": 0.0002
    },
    "first_value_delta_over_tolerance": {
      "status": "no_delta",
      "tolerance": 5e-08
    },
    "gradient_rows": {
      "target_to_fresh_proposal_loc": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "target_to_fresh_proposal_mean": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "target_to_manual_proposal_mean": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.7827423714161357,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699805404
      },
      "target_to_proposal_loc": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 5.445643935786393e-13,
        "finite": true,
        "max_abs_delta": 0.7827423714163882,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699742584
      },
      "target_to_proposal_mean": {
        "bayesfilter_max_abs": 0.7827423714161357,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.7827423714161357,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.4898093699805404
      }
    },
    "interpretation": "proposal_topology_probe_differs",
    "proposal_log_prob_parameter_rows": {
      "first_dist_log_prob": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "fresh_dist_log_prob": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "manual_dist_log_prob": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "official_proposal_ll": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      }
    },
    "status": "compared",
    "value_rows": {
      "fresh_loc_minus_proposal_loc": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "fresh_mean_minus_fresh_loc": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "manual_minus_proposal_loc": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      },
      "official_proposal_ll_minus_first_dist_log_prob": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 8.890665981198254e-13,
        "finite": true,
        "max_abs_delta": 8.890665981198254e-13,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 7.285283487590277e-13
      },
      "official_proposal_ll_minus_fresh_dist_log_prob": {
        "bayesfilter_max_abs": 8.890665981198254e-13,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 8.890665981198254e-13,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 7.285283487590277e-13
      },
      "official_proposal_ll_minus_manual_dist_log_prob": {
        "bayesfilter_max_abs": 1.7763568394002505e-15,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 1.7763568394002505e-15,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 5.551115123125783e-15
      },
      "proposal_loc_minus_proposal_mean": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 0.0,
        "finite": true,
        "max_abs_delta": 0.0,
        "shape_match": true,
        "status": "compared",
        "sum_delta": 0.0
      }
    }
  },
  "resampling_flags_match": true,
  "scalar_delta": 6.2123888255882775e-09,
  "status": "compared",
  "total_gradient_delta": [
    5.302734403676368,
    -0.1337765252068337
  ],
  "transport_upstream_clip_fraction_delta": 0.0,
  "value_deltas": {
    "fresh_dist_log_prob": {
      "bayesfilter_max_abs": 4.717860757900072,
      "filterflow_max_abs": 4.717860757900072,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "fresh_proposal_loc": {
      "bayesfilter_max_abs": 519.2188441084146,
      "filterflow_max_abs": 519.218844108408,
      "finite": true,
      "max_abs_delta": 7.015614755800925e-10,
      "shape_match": true,
      "sum_delta": 1.3242242857813835e-09
    },
    "fresh_proposal_mean": {
      "bayesfilter_max_abs": 519.2188441084146,
      "filterflow_max_abs": 519.218844108408,
      "finite": true,
      "max_abs_delta": 7.015614755800925e-10,
      "shape_match": true,
      "sum_delta": 1.3242242857813835e-09
    },
    "increment": {
      "bayesfilter_max_abs": 0.7603288018870904,
      "filterflow_max_abs": 0.7603288017481669,
      "finite": true,
      "max_abs_delta": 1.389235393389754e-10,
      "shape_match": true,
      "sum_delta": 1.389235393389754e-10
    },
    "log_ess": {
      "bayesfilter_max_abs": 3.8274888177225184,
      "filterflow_max_abs": 3.827488817906256,
      "finite": true,
      "max_abs_delta": 1.837374696833649e-10,
      "shape_match": true,
      "sum_delta": 1.837374696833649e-10
    },
    "manual_dist_log_prob": {
      "bayesfilter_max_abs": 4.71786075790059,
      "filterflow_max_abs": 4.717860757900072,
      "finite": true,
      "max_abs_delta": 8.895106873296754e-13,
      "shape_match": true,
      "sum_delta": 7.212008767965017e-13
    },
    "manual_proposal_mean": {
      "bayesfilter_max_abs": 519.2188441084146,
      "filterflow_max_abs": 519.218844108408,
      "finite": true,
      "max_abs_delta": 7.015614755800925e-10,
      "shape_match": true,
      "sum_delta": 1.3242242857813835e-09
    },
    "normalized": {
      "bayesfilter_max_abs": 5.016766134437026,
      "filterflow_max_abs": 5.01676613455824,
      "finite": true,
      "max_abs_delta": 1.1451586345856413e-09,
      "shape_match": true,
      "sum_delta": 4.819838750336203e-09
    },
    "observation_ll": {
      "bayesfilter_max_abs": 1.383508147383262,
      "filterflow_max_abs": 1.383508147384548,
      "finite": true,
      "max_abs_delta": 2.0132562283947664e-10,
      "shape_match": true,
      "sum_delta": 8.258638217739644e-11
    },
    "post_log_weights": {
      "bayesfilter_max_abs": 3.912023005428146,
      "filterflow_max_abs": 3.912023005428146,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "post_particles": {
      "bayesfilter_max_abs": 509.3920006641104,
      "filterflow_max_abs": 509.3920006636405,
      "finite": true,
      "max_abs_delta": 6.703722021939029e-10,
      "shape_match": true,
      "sum_delta": 3.081368049606681e-09
    },
    "post_update_log_likelihoods": {
      "bayesfilter_max_abs": 141.71711568080488,
      "filterflow_max_abs": 141.71711568701727,
      "finite": true,
      "max_abs_delta": 6.2123888255882775e-09,
      "shape_match": true,
      "sum_delta": 6.2123888255882775e-09
    },
    "post_update_log_weights": {
      "bayesfilter_max_abs": 5.016766134437026,
      "filterflow_max_abs": 5.01676613455824,
      "finite": true,
      "max_abs_delta": 1.1451586345856413e-09,
      "shape_match": true,
      "sum_delta": 4.819838750336203e-09
    },
    "pre_current_log_likelihoods": {
      "bayesfilter_max_abs": 140.9567868789178,
      "filterflow_max_abs": 140.9567868852691,
      "finite": true,
      "max_abs_delta": 6.351314141284092e-09,
      "shape_match": true,
      "sum_delta": 6.351314141284092e-09
    },
    "pre_log_weights": {
      "bayesfilter_max_abs": 7.591460570276422,
      "filterflow_max_abs": 7.591460567082821,
      "finite": true,
      "max_abs_delta": 3.193600939255248e-09,
      "shape_match": true,
      "sum_delta": 9.822258562053321e-09
    },
    "pre_particles": {
      "bayesfilter_max_abs": 509.5286014281429,
      "filterflow_max_abs": 509.5286014281523,
      "finite": true,
      "max_abs_delta": 8.847109711496159e-10,
      "shape_match": true,
      "sum_delta": 6.693881005048752e-09
    },
    "proposal_dist_log_prob": {
      "bayesfilter_max_abs": 4.7178607579005885,
      "filterflow_max_abs": 4.7178607579005885,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "proposal_ll": {
      "bayesfilter_max_abs": 4.7178607579005885,
      "filterflow_max_abs": 4.717860757900072,
      "finite": true,
      "max_abs_delta": 8.890665981198254e-13,
      "shape_match": true,
      "sum_delta": 7.265299473147024e-13
    },
    "proposal_loc": {
      "bayesfilter_max_abs": 519.2188441084146,
      "filterflow_max_abs": 519.218844108408,
      "finite": true,
      "max_abs_delta": 7.015614755800925e-10,
      "shape_match": true,
      "sum_delta": 1.3242242857813835e-09
    },
    "proposal_mean": {
      "bayesfilter_max_abs": 519.2188441084146,
      "filterflow_max_abs": 519.218844108408,
      "finite": true,
      "max_abs_delta": 7.015614755800925e-10,
      "shape_match": true,
      "sum_delta": 1.3242242857813835e-09
    },
    "proposed_particles": {
      "bayesfilter_max_abs": 519.3668650770353,
      "filterflow_max_abs": 519.3668650770238,
      "finite": true,
      "max_abs_delta": 7.015614755800925e-10,
      "shape_match": true,
      "sum_delta": 1.3242242857813835e-09
    },
    "transition_ll": {
      "bayesfilter_max_abs": 4.948835414176724,
      "filterflow_max_abs": 4.94883541438441,
      "finite": true,
      "max_abs_delta": 1.325650700323422e-09,
      "shape_match": true,
      "sum_delta": 1.184788800401293e-08
    },
    "transport_matrix": {
      "bayesfilter_max_abs": 0.3191070692332988,
      "filterflow_max_abs": 0.3191070695507616,
      "finite": true,
      "max_abs_delta": 3.1746283379874285e-10,
      "shape_match": true,
      "sum_delta": 1.4210854715202004e-14
    },
    "unnormalized": {
      "bayesfilter_max_abs": 5.777094936324116,
      "filterflow_max_abs": 5.777094936306407,
      "finite": true,
      "max_abs_delta": 1.2840821739246167e-09,
      "shape_match": true,
      "sum_delta": 1.1766047691708081e-08
    }
  }
}
```

## Boundary Mode Comparison

```json
{
  "best_value_valid_mode": {
    "bayesfilter_gradient_diag": [
      9110.446610301125,
      56.989873289774025
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_delta": [
      5.302734402777787,
      -0.13377652515431038
    ],
    "gradient_within_tolerance": false,
    "max_abs_gradient_delta": 5.302734402777787,
    "mode": "target_proposal_sample_filterflow_contract",
    "mode_description": "At the target time only, keep proposal sample values but stop the sampled particle path back through the proposal mean while preserving proposal log-probability dependence on the proposal distribution.",
    "resampling_flag": [
      true
    ],
    "scalar_delta": 6.212417247297708e-09,
    "scalar_within_tolerance": true
  },
  "filterflow_gradient_diag": [
    9105.143875898348,
    57.123649814928335
  ],
  "filterflow_target_scalar": -141.71711568701727,
  "interpretation": "tested_boundary_modes_do_not_explain_row_gradient_delta",
  "matching_modes": [],
  "rows": [
    {
      "bayesfilter_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.302734403676368,
      "mode": "raw",
      "mode_description": "No extra BayesFilter graph boundary.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.302734403676368,
      "mode": "filterflow_custom_transport_gradient",
      "mode_description": "Use a whole-transport-call custom gradient matching FilterFlow's transport(x, logw, ...) backward signature.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        15042.87849408244,
        -80.45039383216313
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5937.734618184093,
        -137.57404364709146
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5937.734618184093,
      "mode": "carry_log_weights_stop_gradient",
      "mode_description": "Stop gradient through carried log weights after each update.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        0.0,
        0.0
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        -9105.143875898348,
        -57.123649814928335
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 9105.143875898348,
      "mode": "carry_log_likelihoods_stop_gradient",
      "mode_description": "Stop gradient through carried cumulative log likelihoods after each update.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        0.0,
        0.0
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        -9105.143875898348,
        -57.123649814928335
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 9105.143875898348,
      "mode": "carry_both_stop_gradient",
      "mode_description": "Stop gradient through both carried log weights and cumulative log likelihoods.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        -3121.107441725726,
        460.2743623868574
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        -12226.251317624074,
        403.15071257192903
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 12226.251317624074,
      "mode": "proposal_mean_stop_gradient",
      "mode_description": "Stop gradient through the optimal-proposal mean at each step.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        10667.890734428043,
        82.69798787149296
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        1562.7468585296956,
        25.57433805656462
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 1562.7468585296956,
      "mode": "target_transport_log_weights_stop_gradient",
      "mode_description": "At the target time only, stop gradient through log weights as an input to the transport solve.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        15042.87849408244,
        -80.45039383216313
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5937.734618184093,
        -137.57404364709146
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5937.734618184093,
      "mode": "all_times_transport_log_weights_stop_gradient",
      "mode_description": "At every time, stop gradient through log weights as an input to the transport solve.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        9110.44997649539,
        56.98978836779012
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5.3061005970430415,
        -0.1338614471382158
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.3061005970430415,
      "mode": "proposal_sample_noise_stop_gradient",
      "mode_description": "Keep proposal sample values, but stop the reparameterized sample-noise path from sampled particles back through proposal mean.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2095750763546675e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        5374.88199423692,
        7.969535101293168e-11
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        -3730.2618816614277,
        -57.12364981484864
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 3730.2618816614277,
      "mode": "all_times_proposal_sample_filterflow_contract",
      "mode_description": "At every time, keep proposal sample values but stop the sampled particle path back through proposal mean while preserving proposal log-probability dependence on the proposal distribution.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2095750763546675e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        9110.446610301125,
        56.989873289774025
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5.302734402777787,
        -0.13377652515431038
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.302734402777787,
      "mode": "target_proposal_sample_filterflow_contract",
      "mode_description": "At the target time only, keep proposal sample values but stop the sampled particle path back through the proposal mean while preserving proposal log-probability dependence on the proposal distribution.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.212417247297708e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        5374.88199423692,
        7.969535101293168e-11
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        -3730.2618816614277,
        -57.12364981484864
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 3730.2618816614277,
      "mode": "proposal_sample_stop_gradient",
      "mode_description": "Stop gradient through sampled proposal particles at each step.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2095750763546675e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.302734403676368,
      "mode": "proposal_log_prob_stop_gradient",
      "mode_description": "Stop gradient through proposal log probability at each step.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true
    },
    {
      "bayesfilter_gradient_diag": [
        0.0,
        0.0
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        -9105.143875898348,
        -57.123649814928335
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 9105.143875898348,
      "mode": "carry_both_proposal_sample_stop_gradient",
      "mode_description": "Stop carried log weights/log likelihoods and sampled proposal particles.",
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2095750763546675e-09,
      "scalar_within_tolerance": true
    }
  ],
  "status": "compared"
}
```

## BayesFilter Boundary Modes

```json
{
  "boundary_contract": "BayesFilter-only diagnostic stop-gradient modes at the carried-state and optimal-proposal graph boundaries; values must remain aligned before any gradient interpretation.",
  "modes": [
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "raw",
      "mode_description": "No extra BayesFilter graph boundary.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "filterflow_custom_transport_gradient",
      "mode_description": "Use a whole-transport-call custom gradient matching FilterFlow's transport(x, logw, ...) backward signature.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "carry_log_weights_stop_gradient",
      "mode_description": "Stop gradient through carried log weights after each update.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        15042.87849408244,
        -80.45039383216313
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "carry_log_likelihoods_stop_gradient",
      "mode_description": "Stop gradient through carried cumulative log likelihoods after each update.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        0.0,
        0.0
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "carry_both_stop_gradient",
      "mode_description": "Stop gradient through both carried log weights and cumulative log likelihoods.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        0.0,
        0.0
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "proposal_mean_stop_gradient",
      "mode_description": "Stop gradient through the optimal-proposal mean at each step.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        -3121.107441725726,
        460.2743623868574
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "target_transport_log_weights_stop_gradient",
      "mode_description": "At the target time only, stop gradient through log weights as an input to the transport solve.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        10667.890734428043,
        82.69798787149296
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "all_times_transport_log_weights_stop_gradient",
      "mode_description": "At every time, stop gradient through log weights as an input to the transport solve.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        15042.87849408244,
        -80.45039383216313
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "proposal_sample_noise_stop_gradient",
      "mode_description": "Keep proposal sample values, but stop the reparameterized sample-noise path from sampled particles back through proposal mean.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        9110.44997649539,
        56.98978836779012
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "all_times_proposal_sample_filterflow_contract",
      "mode_description": "At every time, keep proposal sample values but stop the sampled particle path back through proposal mean while preserving proposal log-probability dependence on the proposal distribution.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        5374.88199423692,
        7.969535101293168e-11
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "target_proposal_sample_filterflow_contract",
      "mode_description": "At the target time only, keep proposal sample values but stop the sampled particle path back through the proposal mean while preserving proposal log-probability dependence on the proposal distribution.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080485,
      "total_gradient_diag": [
        9110.446610301125,
        56.989873289774025
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "proposal_sample_stop_gradient",
      "mode_description": "Stop gradient through sampled proposal particles at each step.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        5374.88199423692,
        7.969535101293168e-11
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "proposal_log_prob_stop_gradient",
      "mode_description": "Stop gradient through proposal log probability at each step.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    {
      "finite_gradient": true,
      "finite_scalar": true,
      "mode": "carry_both_proposal_sample_stop_gradient",
      "mode_description": "Stop carried log weights/log likelihoods and sampled proposal particles.",
      "resampling_flag": [
        true
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        0.0,
        0.0
      ]
    }
  ],
  "status": "executed"
}
```

## FilterFlow VJP

```json
{
  "backend": "executable_filterflow_subprocess",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "filterflow_proposal_mean_internal_probe": {
    "adjoint_delta": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "adjoint_delta_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "manual_proposal_mean_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "proposal_mean_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "value_delta": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "value_delta_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ]
  },
  "gradient_summaries": {
    "fresh_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "fresh_proposal_loc": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "increment": {
      "finite": true,
      "max_abs": 1.0,
      "shape": [
        1
      ],
      "sum": 1.0
    },
    "log_ess": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1
      ],
      "sum": 0.0
    },
    "manual_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "manual_proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "normalized": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 0.029126396082423307,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 0.029126396082423307,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_particles": {
      "finite": true,
      "max_abs": 0.030135380102742214,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.108354429572037
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 1.0,
      "shape": [
        1
      ],
      "sum": 1.0
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "pre_current_log_likelihoods": {
      "finite": true,
      "max_abs": 1.0,
      "shape": [
        1
      ],
      "sum": 1.0
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 1.1695816019013177,
      "shape": [
        1,
        50
      ],
      "sum": 26.13115017062465
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 1.0755389718368462,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -6.490278653863614
    },
    "proposal_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 0.029126396082423307,
      "shape": [
        1,
        50
      ],
      "sum": -1.0
    },
    "proposal_loc": {
      "finite": true,
      "max_abs": 5.445643935786393e-13,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 6.281424816054204e-12
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 5.445643935786393e-13,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 6.281424816054204e-12
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 0.029126396082423307,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 15.683856019586806,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 14590.183146020285
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 0.029126396082423307,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    }
  },
  "graph_embedding_probe": null,
  "local_post_particle_adjoint_probe": {
    "fresh_proposal_loc_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_mean_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "increment_to_post_particles": {
      "finite": true,
      "max_abs": 0.030135380102742214,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.108354429572037
    },
    "manual_proposal_mean_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "observation_ll_to_post_particles": {
      "finite": true,
      "max_abs": 0.01487406164244211,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.08186897206087934
    },
    "proposal_ll_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "proposal_loc_to_post_particles": {
      "finite": true,
      "max_abs": 3.7558963348749376e-14,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.955062783681125e-13
    },
    "proposal_mean_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "proposed_particles_to_post_particles": {
      "finite": true,
      "max_abs": 3.7558963348749376e-14,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.955062783681125e-13
    },
    "transition_ll_to_post_particles": {
      "finite": true,
      "max_abs": 0.035592916940351535,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.0264854575111573
    },
    "unnormalized_to_post_particles": {
      "finite": true,
      "max_abs": 0.030135380102742214,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.108354429572037
    }
  },
  "parameter_path_adjoint_probe": {
    "fresh_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_loc": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "increment": {
      "finite": true,
      "max_abs": 11886.75807955571,
      "shape": [
        2
      ],
      "sum": 11313.776556202181
    },
    "log_ess": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "manual_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "manual_proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "normalized": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 9950.289320089687,
      "shape": [
        2
      ],
      "sum": 9505.073065537394
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "post_particles": {
      "finite": true,
      "max_abs": 11600.3906035415,
      "shape": [
        2
      ],
      "sum": 11027.409080187972
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 9105.143875898348,
      "shape": [
        2
      ],
      "sum": 9162.267525713276
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "pre_current_log_likelihoods": {
      "finite": true,
      "max_abs": 1001.4593201784609,
      "shape": [
        2
      ],
      "sum": -720.7859812663263
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 10711.474356632394,
      "shape": [
        2
      ],
      "sum": -10305.315171907774
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 12879.778839173718,
      "shape": [
        2
      ],
      "sum": 12343.006445705332
    },
    "proposal_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "proposal_loc": {
      "finite": true,
      "max_abs": 8012.192846756851,
      "shape": [
        2
      ],
      "sum": -7526.80772192185
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 8012.192846756851,
      "shape": [
        2
      ],
      "sum": -7526.80772192185
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 12100.902593110097,
      "shape": [
        2
      ],
      "sum": 11516.177316937552
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 10068.711052550034,
      "shape": [
        2
      ],
      "sum": 9543.437749961005
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 11886.75807955571,
      "shape": [
        2
      ],
      "sum": 11313.776556202181
    }
  },
  "proposal_sample_gradient_contract": {
    "contract": "Probe actual FilterFlow proposal_dist.sample and a manual distribution built from the explicit proposal mean under the downstream upstream gradient for proposed_particles.",
    "value_probe": {
      "actual_sample_minus_manual_mean": {
        "finite": true,
        "max_abs": 1.2039904106672097,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -9.423168004290485
      },
      "manual_probe_minus_actual_sample": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "manual_probe_minus_manual_mean": {
        "finite": true,
        "max_abs": 1.2039904106672097,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -9.423168004290485
      }
    },
    "value_probe_tensors": {
      "actual_sample_minus_manual_mean": [
        [
          [
            -0.039827018934943226,
            -0.6889266147975874
          ],
          [
            -0.06983374152832766,
            -0.2591341393234572
          ],
          [
            0.05042471963292883,
            0.05231066918351246
          ],
          [
            0.01214327059506104,
            0.06059718961104821
          ],
          [
            -0.14769575675575197,
            -0.4276804744628464
          ],
          [
            0.04122359852351565,
            -0.8016100424202435
          ],
          [
            -0.01370822510580183,
            -0.8523795572448272
          ],
          [
            0.05015836559698528,
            0.09086937236442694
          ],
          [
            0.06651707654759775,
            0.5299856873737347
          ],
          [
            -0.01645973749498353,
            0.46287434621731194
          ],
          [
            -0.04363175183561907,
            -0.18170274210598336
          ],
          [
            0.05826177908261343,
            0.6414997770995257
          ],
          [
            0.050576680579752065,
            0.3904928673893977
          ],
          [
            -0.1284079200394217,
            -0.48240268152906296
          ],
          [
            -0.053760975379418596,
            1.1064198446869042
          ],
          [
            0.020474395648079735,
            -0.5633088776998392
          ],
          [
            -0.031653208878424266,
            0.3706781623579758
          ],
          [
            -0.11449504035329028,
            0.4831817955529587
          ],
          [
            -0.11084134702014126,
            -0.35848947164071276
          ],
          [
            0.08736451454558392,
            -0.8168944616344689
          ],
          [
            -0.00831180068314552,
            0.1754260755476018
          ],
          [
            0.09424544953969871,
            0.21361575062433502
          ],
          [
            -0.14293083820700758,
            -0.31616833529056265
          ],
          [
            -0.04318508117341935,
            -0.18539893962458365
          ],
          [
            0.026184031571119704,
            -0.5857779984711087
          ],
          [
            0.023618031386945404,
            -0.05594826453745938
          ],
          [
            0.08554084772390524,
            -1.1065265609274633
          ],
          [
            -0.1469698082682953,
            -0.6489911124229621
          ],
          [
            -0.11292990663309865,
            0.24727310506675693
          ],
          [
            0.03360733603085464,
            -0.32311628095884615
          ],
          [
            0.03193565110984764,
            -0.10873633290318452
          ],
          [
            -0.0003642933924083991,
            -0.06215786530638212
          ],
          [
            -0.02874157914141051,
            -0.45155889939025684
          ],
          [
            0.0769362392632047,
            0.47988897302154854
          ],
          [
            -0.01620777658604311,
            0.13629828143561085
          ],
          [
            0.08822507610682351,
            0.001987009968772213
          ],
          [
            -0.07691024178586758,
            -0.3273194302204949
          ],
          [
            -0.07317142783801955,
            -1.0165646089651261
          ],
          [
            0.06452044561910952,
            0.04746974275883176
          ],
          [
            -0.14134521052642413,
            -0.41673051487595103
          ],
          [
            -0.07851934302505015,
            -0.28051638601720086
          ],
          [
            -0.053582346723601404,
            -0.9658630581454339
          ],
          [
            -0.09352685170881614,
            -0.25390252180896766
          ],
          [
            0.1754513954867889,
            -1.2039904106672097
          ],
          [
            0.04980658164470242,
            -0.1484498501318967
          ],
          [
            -0.11825992662068074,
            -1.0138302765985436
          ],
          [
            0.009038690649504133,
            -0.4572484595980022
          ],
          [
            0.10417334522253441,
            0.37495251853305334
          ],
          [
            0.04865849560906099,
            0.7110651821647096
          ],
          [
            0.058125280531385215,
            -0.14066932813602762
          ]
        ]
      ],
      "manual_probe_minus_actual_sample": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "manual_probe_minus_manual_mean": [
        [
          [
            -0.039827018934943226,
            -0.6889266147975874
          ],
          [
            -0.06983374152832766,
            -0.2591341393234572
          ],
          [
            0.05042471963292883,
            0.05231066918351246
          ],
          [
            0.01214327059506104,
            0.06059718961104821
          ],
          [
            -0.14769575675575197,
            -0.4276804744628464
          ],
          [
            0.04122359852351565,
            -0.8016100424202435
          ],
          [
            -0.01370822510580183,
            -0.8523795572448272
          ],
          [
            0.05015836559698528,
            0.09086937236442694
          ],
          [
            0.06651707654759775,
            0.5299856873737347
          ],
          [
            -0.01645973749498353,
            0.46287434621731194
          ],
          [
            -0.04363175183561907,
            -0.18170274210598336
          ],
          [
            0.05826177908261343,
            0.6414997770995257
          ],
          [
            0.050576680579752065,
            0.3904928673893977
          ],
          [
            -0.1284079200394217,
            -0.48240268152906296
          ],
          [
            -0.053760975379418596,
            1.1064198446869042
          ],
          [
            0.020474395648079735,
            -0.5633088776998392
          ],
          [
            -0.031653208878424266,
            0.3706781623579758
          ],
          [
            -0.11449504035329028,
            0.4831817955529587
          ],
          [
            -0.11084134702014126,
            -0.35848947164071276
          ],
          [
            0.08736451454558392,
            -0.8168944616344689
          ],
          [
            -0.00831180068314552,
            0.1754260755476018
          ],
          [
            0.09424544953969871,
            0.21361575062433502
          ],
          [
            -0.14293083820700758,
            -0.31616833529056265
          ],
          [
            -0.04318508117341935,
            -0.18539893962458365
          ],
          [
            0.026184031571119704,
            -0.5857779984711087
          ],
          [
            0.023618031386945404,
            -0.05594826453745938
          ],
          [
            0.08554084772390524,
            -1.1065265609274633
          ],
          [
            -0.1469698082682953,
            -0.6489911124229621
          ],
          [
            -0.11292990663309865,
            0.24727310506675693
          ],
          [
            0.03360733603085464,
            -0.32311628095884615
          ],
          [
            0.03193565110984764,
            -0.10873633290318452
          ],
          [
            -0.0003642933924083991,
            -0.06215786530638212
          ],
          [
            -0.02874157914141051,
            -0.45155889939025684
          ],
          [
            0.0769362392632047,
            0.47988897302154854
          ],
          [
            -0.01620777658604311,
            0.13629828143561085
          ],
          [
            0.08822507610682351,
            0.001987009968772213
          ],
          [
            -0.07691024178586758,
            -0.3273194302204949
          ],
          [
            -0.07317142783801955,
            -1.0165646089651261
          ],
          [
            0.06452044561910952,
            0.04746974275883176
          ],
          [
            -0.14134521052642413,
            -0.41673051487595103
          ],
          [
            -0.07851934302505015,
            -0.28051638601720086
          ],
          [
            -0.053582346723601404,
            -0.9658630581454339
          ],
          [
            -0.09352685170881614,
            -0.25390252180896766
          ],
          [
            0.1754513954867889,
            -1.2039904106672097
          ],
          [
            0.04980658164470242,
            -0.1484498501318967
          ],
          [
            -0.11825992662068074,
            -1.0138302765985436
          ],
          [
            0.009038690649504133,
            -0.4572484595980022
          ],
          [
            0.10417334522253441,
            0.37495251853305334
          ],
          [
            0.04865849560906099,
            0.7110651821647096
          ],
          [
            0.058125280531385215,
            -0.14066932813602762
          ]
        ]
      ]
    },
    "vjp_probe": {
      "actual_sample_to_fresh_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "actual_sample_to_fresh_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "actual_sample_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "actual_sample_to_post_particles": {
        "finite": true,
        "max_abs": 3.7558963348749376e-14,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 1.955062783681125e-13
      },
      "actual_sample_to_proposal_loc": {
        "finite": true,
        "max_abs": 5.445643935786393e-13,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 6.281424816054204e-12
      },
      "actual_sample_to_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "manual_probe_sample_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 5.445643935786393e-13,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 6.281424816054204e-12
      },
      "manual_probe_sum_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      }
    },
    "vjp_tensors": {
      "actual_sample_to_fresh_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "actual_sample_to_fresh_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "actual_sample_to_manual_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "actual_sample_to_post_particles": [
        [
          [
            2.499040910973652e-15,
            1.5354795374768001e-15
          ],
          [
            1.5160570167681363e-16,
            1.8344335553512414e-15
          ],
          [
            -2.0851303605623142e-15,
            1.512166376385613e-15
          ],
          [
            -5.641007749058301e-15,
            -1.837057402170388e-15
          ],
          [
            -5.751792756950288e-15,
            1.821207551995085e-15
          ],
          [
            -2.6562888960462065e-15,
            -7.003325983632233e-16
          ],
          [
            -1.7819606610424786e-14,
            -4.610197564076918e-15
          ],
          [
            -8.779638280439383e-15,
            -1.931173197779244e-15
          ],
          [
            -4.929295027853161e-15,
            -3.776580762758037e-16
          ],
          [
            -9.207813995175166e-15,
            -1.990524009176429e-15
          ],
          [
            1.2945458769848232e-14,
            8.089854121575549e-15
          ],
          [
            1.7731096356112492e-14,
            1.1006914592851666e-14
          ],
          [
            -7.619535750941554e-15,
            -3.5954169508777546e-15
          ],
          [
            5.3655661926784826e-15,
            3.8591582095973e-15
          ],
          [
            7.394825681789515e-15,
            8.05234491474093e-15
          ],
          [
            1.3642550617558328e-14,
            1.0894087539751902e-14
          ],
          [
            -5.465655393785506e-15,
            -1.162204806928491e-15
          ],
          [
            6.859446582534686e-15,
            4.605369058344495e-15
          ],
          [
            3.7558963348749376e-14,
            2.3257974635513422e-14
          ],
          [
            4.760320905984247e-15,
            5.653454057591025e-15
          ],
          [
            -4.652626888126443e-15,
            -8.431152766091195e-16
          ],
          [
            -8.791070037232491e-15,
            -3.062102589176632e-15
          ],
          [
            -1.6862773473175185e-14,
            -7.997321028453333e-15
          ],
          [
            1.8304156095784076e-14,
            8.400929841065543e-15
          ],
          [
            2.100499449898968e-14,
            1.3422302076356867e-14
          ],
          [
            2.0266591324156e-15,
            2.365369741470506e-15
          ],
          [
            8.997822926185921e-15,
            4.704056652522437e-15
          ],
          [
            -9.302211849552574e-15,
            -3.436529044922866e-15
          ],
          [
            -2.4669044272848767e-14,
            -9.451115300582225e-15
          ],
          [
            1.6984156161184396e-14,
            1.553726984690969e-14
          ],
          [
            -1.3884530980234722e-14,
            -4.231996998906225e-15
          ],
          [
            4.166605502750864e-15,
            7.443403833808282e-15
          ],
          [
            1.832024886929541e-15,
            1.8900527611515976e-15
          ],
          [
            -3.3814449707333668e-15,
            1.018283212250243e-15
          ],
          [
            -3.4387018813666496e-15,
            -1.0305772781886901e-15
          ],
          [
            -3.736418191326169e-15,
            -7.344800139260906e-16
          ],
          [
            1.9663799204155564e-14,
            1.2177711998393706e-14
          ],
          [
            2.1593361998830583e-14,
            1.3563814382119578e-14
          ],
          [
            1.553536497516022e-14,
            1.1512461102023442e-14
          ],
          [
            1.466316608884671e-14,
            8.436558331089238e-15
          ],
          [
            -5.184228110672815e-15,
            -2.3475238955941137e-15
          ],
          [
            5.75895600369619e-15,
            5.240869624385714e-15
          ],
          [
            -4.384790148497405e-15,
            6.013752666514286e-16
          ],
          [
            -1.4915253498301585e-15,
            4.4738243655315295e-15
          ],
          [
            -8.80333587070149e-15,
            -1.4886216159708825e-15
          ],
          [
            -1.0411631955156506e-14,
            -3.68779341362787e-15
          ],
          [
            -2.075496774955763e-14,
            -9.183321153422787e-15
          ],
          [
            1.0397305461664715e-14,
            1.1106768183585706e-14
          ],
          [
            6.1540139680656745e-15,
            4.247691238092149e-15
          ],
          [
            -1.1157002123400577e-14,
            -4.189039324357021e-15
          ]
        ]
      ],
      "actual_sample_to_proposal_loc": [
        [
          [
            3.5622546579183734e-14,
            -1.0547118733938987e-15
          ],
          [
            9.06219543850284e-14,
            1.7052331768852014e-15
          ],
          [
            1.1218456719142011e-13,
            3.718162930321789e-15
          ],
          [
            2.3436114160446664e-15,
            4.035834166860042e-15
          ],
          [
            1.900701818158268e-13,
            7.868705687030797e-15
          ],
          [
            9.471590178833367e-15,
            2.067790383364354e-15
          ],
          [
            6.800809915219475e-14,
            1.3961054534661343e-14
          ],
          [
            5.079270337660091e-14,
            7.224255915705413e-15
          ],
          [
            6.44137521099708e-14,
            4.773959005888173e-15
          ],
          [
            5.5039306445792135e-14,
            7.61196661258623e-15
          ],
          [
            1.9143020502099262e-13,
            -5.325601071248798e-15
          ],
          [
            2.5845992013273644e-13,
            -7.369105325949477e-15
          ],
          [
            -5.342948306008566e-14,
            4.31946145518225e-15
          ],
          [
            1.0505485370515544e-13,
            -1.6930901125533637e-15
          ],
          [
            2.836619827917275e-13,
            4.440892098500626e-16
          ],
          [
            3.22068760549854e-13,
            -3.2057689836051395e-15
          ],
          [
            3.365363543395006e-14,
            4.538036613155327e-15
          ],
          [
            1.1762812945903534e-13,
            -2.4980018054066022e-15
          ],
          [
            5.445643935786393e-13,
            -1.5668022435022522e-14
          ],
          [
            2.064737270046635e-13,
            7.632783294297951e-16
          ],
          [
            3.607530940641368e-14,
            4.0115480381963664e-15
          ],
          [
            -6.467049118441537e-15,
            6.087144677202616e-15
          ],
          [
            -1.202926647181357e-13,
            9.51842771268474e-15
          ],
          [
            1.163513729807164e-13,
            -1.061650767297806e-14
          ],
          [
            3.2564229091036623e-13,
            -8.340550472496489e-15
          ],
          [
            8.579421895138495e-14,
            2.8275992658421956e-16
          ],
          [
            8.637535131583718e-14,
            -4.6351811278100286e-15
          ],
          [
            -1.6819878823071122e-14,
            6.241535066564552e-15
          ],
          [
            -6.175615574477433e-14,
            1.6209256159527285e-14
          ],
          [
            5.01279573406066e-13,
            -1.9845236565174673e-15
          ],
          [
            2.0483614804334138e-14,
            1.0227929614359255e-14
          ],
          [
            3.074762666699371e-13,
            3.2031668983911743e-15
          ],
          [
            6.494804694057166e-14,
            3.469446951953614e-18
          ],
          [
            1.0907941216942163e-13,
            4.5727310826748635e-15
          ],
          [
            5.963979310408263e-15,
            2.550910871423895e-15
          ],
          [
            2.6055546609171643e-14,
            3.1632682584437077e-15
          ],
          [
            2.8516078387497146e-13,
            -8.201772594418344e-15
          ],
          [
            3.228528555609955e-13,
            -8.81239525796218e-15
          ],
          [
            3.213818100533672e-13,
            -4.557985933129061e-15
          ],
          [
            1.7991164114050662e-13,
            -6.770625726737478e-15
          ],
          [
            -3.1336044870045043e-14,
            3.039235529911366e-15
          ],
          [
            1.6857695794847416e-13,
            -7.008282842946301e-16
          ],
          [
            1.0491607582707729e-13,
            5.198966257502491e-15
          ],
          [
            2.525757381022231e-13,
            6.106226635438361e-15
          ],
          [
            7.367717547168695e-14,
            7.69870278638507e-15
          ],
          [
            -1.0769163338864018e-14,
            7.147060721024445e-15
          ],
          [
            -1.145333827778927e-13,
            1.2385925618474403e-14
          ],
          [
            3.879119248040297e-13,
            4.0592529337857286e-16
          ],
          [
            1.1142128886199032e-13,
            -2.123301534595612e-15
          ],
          [
            -2.3592239273284576e-14,
            7.417677583276827e-15
          ]
        ]
      ],
      "actual_sample_to_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "manual_probe_sample_to_manual_proposal_mean": [
        [
          [
            3.5622546579183734e-14,
            -1.0547118733938987e-15
          ],
          [
            9.06219543850284e-14,
            1.7052331768852014e-15
          ],
          [
            1.1218456719142011e-13,
            3.718162930321789e-15
          ],
          [
            2.3436114160446664e-15,
            4.035834166860042e-15
          ],
          [
            1.900701818158268e-13,
            7.868705687030797e-15
          ],
          [
            9.471590178833367e-15,
            2.067790383364354e-15
          ],
          [
            6.800809915219475e-14,
            1.3961054534661343e-14
          ],
          [
            5.079270337660091e-14,
            7.224255915705413e-15
          ],
          [
            6.44137521099708e-14,
            4.773959005888173e-15
          ],
          [
            5.5039306445792135e-14,
            7.61196661258623e-15
          ],
          [
            1.9143020502099262e-13,
            -5.325601071248798e-15
          ],
          [
            2.5845992013273644e-13,
            -7.369105325949477e-15
          ],
          [
            -5.342948306008566e-14,
            4.31946145518225e-15
          ],
          [
            1.0505485370515544e-13,
            -1.6930901125533637e-15
          ],
          [
            2.836619827917275e-13,
            4.440892098500626e-16
          ],
          [
            3.22068760549854e-13,
            -3.2057689836051395e-15
          ],
          [
            3.365363543395006e-14,
            4.538036613155327e-15
          ],
          [
            1.1762812945903534e-13,
            -2.4980018054066022e-15
          ],
          [
            5.445643935786393e-13,
            -1.5668022435022522e-14
          ],
          [
            2.064737270046635e-13,
            7.632783294297951e-16
          ],
          [
            3.607530940641368e-14,
            4.0115480381963664e-15
          ],
          [
            -6.467049118441537e-15,
            6.087144677202616e-15
          ],
          [
            -1.202926647181357e-13,
            9.51842771268474e-15
          ],
          [
            1.163513729807164e-13,
            -1.061650767297806e-14
          ],
          [
            3.2564229091036623e-13,
            -8.340550472496489e-15
          ],
          [
            8.579421895138495e-14,
            2.8275992658421956e-16
          ],
          [
            8.637535131583718e-14,
            -4.6351811278100286e-15
          ],
          [
            -1.6819878823071122e-14,
            6.241535066564552e-15
          ],
          [
            -6.175615574477433e-14,
            1.6209256159527285e-14
          ],
          [
            5.01279573406066e-13,
            -1.9845236565174673e-15
          ],
          [
            2.0483614804334138e-14,
            1.0227929614359255e-14
          ],
          [
            3.074762666699371e-13,
            3.2031668983911743e-15
          ],
          [
            6.494804694057166e-14,
            3.469446951953614e-18
          ],
          [
            1.0907941216942163e-13,
            4.5727310826748635e-15
          ],
          [
            5.963979310408263e-15,
            2.550910871423895e-15
          ],
          [
            2.6055546609171643e-14,
            3.1632682584437077e-15
          ],
          [
            2.8516078387497146e-13,
            -8.201772594418344e-15
          ],
          [
            3.228528555609955e-13,
            -8.81239525796218e-15
          ],
          [
            3.213818100533672e-13,
            -4.557985933129061e-15
          ],
          [
            1.7991164114050662e-13,
            -6.770625726737478e-15
          ],
          [
            -3.1336044870045043e-14,
            3.039235529911366e-15
          ],
          [
            1.6857695794847416e-13,
            -7.008282842946301e-16
          ],
          [
            1.0491607582707729e-13,
            5.198966257502491e-15
          ],
          [
            2.525757381022231e-13,
            6.106226635438361e-15
          ],
          [
            7.367717547168695e-14,
            7.69870278638507e-15
          ],
          [
            -1.0769163338864018e-14,
            7.147060721024445e-15
          ],
          [
            -1.145333827778927e-13,
            1.2385925618474403e-14
          ],
          [
            3.879119248040297e-13,
            4.0592529337857286e-16
          ],
          [
            1.1142128886199032e-13,
            -2.123301534595612e-15
          ],
          [
            -2.3592239273284576e-14,
            7.417677583276827e-15
          ]
        ]
      ],
      "manual_probe_sum_to_manual_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ]
    }
  },
  "proposal_topology_probe": {
    "contract": "Difference-audit probe for the optimal-proposal graph topology. The executable FilterFlow scalar samples from one proposal distribution and evaluates proposal log probability through the proposal-model loglikelihood method, which constructs a fresh proposal distribution.",
    "gradient_summaries": {
      "target_to_fresh_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "target_to_fresh_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "target_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "target_to_proposal_loc": {
        "finite": true,
        "max_abs": 5.445643935786393e-13,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 6.281424816054204e-12
      },
      "target_to_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      }
    },
    "gradient_tensors": {
      "target_to_fresh_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "target_to_fresh_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "target_to_manual_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "target_to_proposal_loc": [
        [
          [
            3.5622546579183734e-14,
            -1.0547118733938987e-15
          ],
          [
            9.06219543850284e-14,
            1.7052331768852014e-15
          ],
          [
            1.1218456719142011e-13,
            3.718162930321789e-15
          ],
          [
            2.3436114160446664e-15,
            4.035834166860042e-15
          ],
          [
            1.900701818158268e-13,
            7.868705687030797e-15
          ],
          [
            9.471590178833367e-15,
            2.067790383364354e-15
          ],
          [
            6.800809915219475e-14,
            1.3961054534661343e-14
          ],
          [
            5.079270337660091e-14,
            7.224255915705413e-15
          ],
          [
            6.44137521099708e-14,
            4.773959005888173e-15
          ],
          [
            5.5039306445792135e-14,
            7.61196661258623e-15
          ],
          [
            1.9143020502099262e-13,
            -5.325601071248798e-15
          ],
          [
            2.5845992013273644e-13,
            -7.369105325949477e-15
          ],
          [
            -5.342948306008566e-14,
            4.31946145518225e-15
          ],
          [
            1.0505485370515544e-13,
            -1.6930901125533637e-15
          ],
          [
            2.836619827917275e-13,
            4.440892098500626e-16
          ],
          [
            3.22068760549854e-13,
            -3.2057689836051395e-15
          ],
          [
            3.365363543395006e-14,
            4.538036613155327e-15
          ],
          [
            1.1762812945903534e-13,
            -2.4980018054066022e-15
          ],
          [
            5.445643935786393e-13,
            -1.5668022435022522e-14
          ],
          [
            2.064737270046635e-13,
            7.632783294297951e-16
          ],
          [
            3.607530940641368e-14,
            4.0115480381963664e-15
          ],
          [
            -6.467049118441537e-15,
            6.087144677202616e-15
          ],
          [
            -1.202926647181357e-13,
            9.51842771268474e-15
          ],
          [
            1.163513729807164e-13,
            -1.061650767297806e-14
          ],
          [
            3.2564229091036623e-13,
            -8.340550472496489e-15
          ],
          [
            8.579421895138495e-14,
            2.8275992658421956e-16
          ],
          [
            8.637535131583718e-14,
            -4.6351811278100286e-15
          ],
          [
            -1.6819878823071122e-14,
            6.241535066564552e-15
          ],
          [
            -6.175615574477433e-14,
            1.6209256159527285e-14
          ],
          [
            5.01279573406066e-13,
            -1.9845236565174673e-15
          ],
          [
            2.0483614804334138e-14,
            1.0227929614359255e-14
          ],
          [
            3.074762666699371e-13,
            3.2031668983911743e-15
          ],
          [
            6.494804694057166e-14,
            3.469446951953614e-18
          ],
          [
            1.0907941216942163e-13,
            4.5727310826748635e-15
          ],
          [
            5.963979310408263e-15,
            2.550910871423895e-15
          ],
          [
            2.6055546609171643e-14,
            3.1632682584437077e-15
          ],
          [
            2.8516078387497146e-13,
            -8.201772594418344e-15
          ],
          [
            3.228528555609955e-13,
            -8.81239525796218e-15
          ],
          [
            3.213818100533672e-13,
            -4.557985933129061e-15
          ],
          [
            1.7991164114050662e-13,
            -6.770625726737478e-15
          ],
          [
            -3.1336044870045043e-14,
            3.039235529911366e-15
          ],
          [
            1.6857695794847416e-13,
            -7.008282842946301e-16
          ],
          [
            1.0491607582707729e-13,
            5.198966257502491e-15
          ],
          [
            2.525757381022231e-13,
            6.106226635438361e-15
          ],
          [
            7.367717547168695e-14,
            7.69870278638507e-15
          ],
          [
            -1.0769163338864018e-14,
            7.147060721024445e-15
          ],
          [
            -1.145333827778927e-13,
            1.2385925618474403e-14
          ],
          [
            3.879119248040297e-13,
            4.0592529337857286e-16
          ],
          [
            1.1142128886199032e-13,
            -2.123301534595612e-15
          ],
          [
            -2.3592239273284576e-14,
            7.417677583276827e-15
          ]
        ]
      ],
      "target_to_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ]
    },
    "proposal_log_prob_parameter_path_summaries": {
      "first_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      },
      "fresh_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      },
      "manual_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      },
      "official_proposal_ll": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      }
    },
    "proposal_log_prob_parameter_path_tensors": {
      "first_dist_log_prob": [
        0.0,
        0.0
      ],
      "fresh_dist_log_prob": [
        0.0,
        0.0
      ],
      "manual_dist_log_prob": [
        0.0,
        0.0
      ],
      "official_proposal_ll": [
        0.0,
        0.0
      ]
    },
    "value_summaries": {
      "fresh_loc_minus_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "fresh_mean_minus_fresh_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "manual_minus_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "official_proposal_ll_minus_first_dist_log_prob": {
        "finite": true,
        "max_abs": 8.890665981198254e-13,
        "shape": [
          1,
          50
        ],
        "sum": -7.285283487590277e-13
      },
      "official_proposal_ll_minus_fresh_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50
        ],
        "sum": 0.0
      },
      "official_proposal_ll_minus_manual_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50
        ],
        "sum": 0.0
      },
      "proposal_loc_minus_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      }
    },
    "value_tensors": {
      "fresh_loc_minus_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "fresh_mean_minus_fresh_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "manual_minus_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "official_proposal_ll_minus_first_dist_log_prob": [
        [
          1.9539925233402755e-14,
          2.5268676040468563e-13,
          1.4588330543574557e-13,
          1.1102230246251565e-14,
          -7.460698725481052e-14,
          3.26405569239796e-13,
          1.687538997430238e-13,
          -2.020605904817785e-13,
          1.9539925233402755e-14,
          -2.5623947408348613e-13,
          7.815970093361102e-14,
          4.3076653355456074e-14,
          -6.838973831690964e-14,
          2.9620750296999176e-13,
          -4.0945025148175773e-13,
          2.957634137601417e-13,
          8.615330671091215e-14,
          8.890665981198254e-13,
          -1.554312234475219e-14,
          -4.75175454539567e-13,
          -7.993605777301127e-15,
          -4.991562718714704e-13,
          -1.9539925233402755e-13,
          -2.0339285811132868e-13,
          1.3278267374516872e-13,
          -2.9531932455029164e-14,
          -5.444533712761768e-13,
          -5.235811784132238e-13,
          -1.9051427102567686e-13,
          -1.8340884366807586e-13,
          -7.038813976123492e-14,
          1.1102230246251565e-14,
          -2.4868995751603507e-14,
          -2.673417043297377e-13,
          6.838973831690964e-14,
          5.080380560684716e-13,
          3.5083047578154947e-14,
          -8.43769498715119e-15,
          4.04121180963557e-14,
          -3.419486915845482e-13,
          -1.0347278589506459e-13,
          1.2878587085651816e-14,
          7.149836278586008e-14,
          5.160316618457728e-13,
          1.127986593019159e-13,
          2.4069635173873394e-13,
          -3.730349362740526e-14,
          -4.1300296516055823e-13,
          -2.7533531010703882e-14,
          6.261657858885883e-14
        ]
      ],
      "official_proposal_ll_minus_fresh_dist_log_prob": [
        [
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "official_proposal_ll_minus_manual_dist_log_prob": [
        [
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "proposal_loc_minus_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ]
    }
  },
  "resampling_adjoint_decomposition": {
    "carryover_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "carryover_pre_particle_adjoint_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "current_increment_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "current_increment_pre_particle_adjoint_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "direct_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 0.03274518187397153,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.108360676196574
    },
    "direct_pre_particle_adjoint_tensor": [
      [
        [
          -0.024319103368599996,
          -0.025044063089615175
        ],
        [
          0.01294461045354914,
          0.013330493149996408
        ],
        [
          0.028841739106841218,
          0.029701519947424558
        ],
        [
          0.024084452901541993,
          0.02480241762218417
        ],
        [
          0.0040130431235199035,
          0.004132673135332151
        ],
        [
          0.028947340968733276,
          0.029810269832299847
        ],
        [
          0.0065776522279099095,
          0.006773734001641643
        ],
        [
          -0.024355092580927735,
          -0.025081125151090893
        ],
        [
          0.023708450091541638,
          0.024415206056330144
        ],
        [
          0.017788370746516905,
          0.018318647381236914
        ],
        [
          0.005904001499250984,
          0.006080001543944103
        ],
        [
          0.023756373194476803,
          0.02446455776124982
        ],
        [
          0.021101955777597853,
          0.021731011369883965
        ],
        [
          0.031565485625329265,
          0.032506462161585696
        ],
        [
          0.0035307839520740004,
          0.0036360376742225493
        ],
        [
          0.018092589707323747,
          0.018631935199953997
        ],
        [
          0.02399593693049952,
          0.024711262963658037
        ],
        [
          -0.012714799381474228,
          -0.013093831341355576
        ],
        [
          0.006343289826800031,
          0.0065323851874905465
        ],
        [
          0.008071735303901519,
          0.008312356139519183
        ],
        [
          0.031797295030251305,
          0.03274518187397153
        ],
        [
          0.017259487007897867,
          0.017773997460707826
        ],
        [
          0.005135456011074363,
          0.005288545485659239
        ],
        [
          0.008329224717895333,
          0.00857752138970251
        ],
        [
          -0.005203745099488077,
          -0.005358870292155742
        ],
        [
          0.025295720247590053,
          0.026049793208900315
        ],
        [
          0.015584148077748236,
          0.016048716177626914
        ],
        [
          0.030140178010839725,
          0.031038665702219772
        ],
        [
          -0.01743486863874036,
          -0.017954607270247523
        ],
        [
          0.01436225381723789,
          0.014790396884960429
        ],
        [
          0.009721322860817552,
          0.010011118393253847
        ],
        [
          0.015258775365845736,
          0.01571364400818802
        ],
        [
          0.023493860455788284,
          0.024194219439565175
        ],
        [
          0.004472594313051071,
          0.0046059236828168235
        ],
        [
          0.027109635345632484,
          0.027917781656748897
        ],
        [
          0.022671615179763464,
          0.023347462786748277
        ],
        [
          0.021834286158561235,
          0.022485172737813735
        ],
        [
          -0.0022377536623266405,
          -0.002304461766081634
        ],
        [
          0.003129446517677017,
          0.003222736251266306
        ],
        [
          0.028186153843669088,
          0.02902639149212535
        ],
        [
          0.009408489130271914,
          0.00968895899594398
        ],
        [
          -0.018727668107109706,
          -0.019285945476156332
        ],
        [
          0.006206209495520394,
          0.006391218450671405
        ],
        [
          0.0013235903762376777,
          0.0013630469999195605
        ],
        [
          0.018278642823847925,
          0.01882353461534474
        ],
        [
          -0.013266641870036807,
          -0.013662124419008095
        ],
        [
          0.002163248451593169,
          0.0022277355328059758
        ],
        [
          0.005039991359285511,
          0.005190235004142259
        ],
        [
          0.028961441948130242,
          0.0298247911660962
        ],
        [
          -0.0001296972421736008,
          -0.00013356355562593034
        ]
      ]
    ],
    "implicit_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 1.075672535392472,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -7.598639330060187
    },
    "implicit_pre_particle_adjoint_tensor": [
      [
        [
          0.06403292707171893,
          0.2415218940141686
        ],
        [
          -0.00047920785550295726,
          0.19700746734359886
        ],
        [
          0.006342801416643524,
          0.06950006115805896
        ],
        [
          0.005635186767182408,
          0.10015045687785544
        ],
        [
          -0.12181527845072893,
          -0.8765478342911533
        ],
        [
          0.003755605549427249,
          0.06423114076998238
        ],
        [
          -0.10014642738147966,
          -0.7082085939415882
        ],
        [
          -0.045535423719738496,
          -0.25108489142863727
        ],
        [
          0.006656261450849649,
          0.09487899856155706
        ],
        [
          -0.04889672842086465,
          -0.4099824763438259
        ],
        [
          -0.07359968106503868,
          -0.36618532327094383
        ],
        [
          -0.008570282811097434,
          -0.040978473653421776
        ],
        [
          0.006879105730584284,
          0.0912859467911006
        ],
        [
          0.005810015050531442,
          0.0633593855819391
        ],
        [
          -0.07515635728270635,
          -0.313070607206551
        ],
        [
          -0.0425657239414976,
          -0.3382628132366038
        ],
        [
          0.005433190686621861,
          0.09934476498832902
        ],
        [
          -0.007212663106210394,
          0.17914583255435282
        ],
        [
          -0.11622381492189231,
          -0.9017876786667163
        ],
        [
          -0.07249052443913859,
          -0.429145743542684
        ],
        [
          0.00349240726798572,
          0.057672488705531474
        ],
        [
          0.008234983902829895,
          0.1438609594283289
        ],
        [
          -0.12674853624532237,
          -0.9751529766873124
        ],
        [
          -0.0026671284867491145,
          0.3013876008522702
        ],
        [
          -0.14996667709589417,
          -0.9616917671622083
        ],
        [
          0.004537626221767149,
          0.08084083520696829
        ],
        [
          -0.06510201472326659,
          -0.551717021538567
        ],
        [
          0.0054159615071189375,
          0.06733775454493154
        ],
        [
          -0.09487745344464824,
          -0.521959563232984
        ],
        [
          -0.0788529026502033,
          -0.6814519689324569
        ],
        [
          -0.004408075714295126,
          0.24694995030307076
        ],
        [
          -0.03583400100806277,
          -0.19807212499814952
        ],
        [
          0.006151387802285736,
          0.10246488263776338
        ],
        [
          -0.12661295411889212,
          -0.9576721496151912
        ],
        [
          0.004729544974618419,
          0.04280326758381876
        ],
        [
          0.006315081202008185,
          0.09188956242735112
        ],
        [
          -0.0044535876418609135,
          0.02709663664257367
        ],
        [
          -0.050625941680017,
          0.04285622606869316
        ],
        [
          -0.1022397820355341,
          -0.6245949963622078
        ],
        [
          0.0036618457334229686,
          0.061115261682803484
        ],
        [
          6.9160696884462e-05,
          0.28841056718480335
        ],
        [
          0.06770817305510093,
          0.3346611638301383
        ],
        [
          -0.014424997532836985,
          0.2722429243574476
        ],
        [
          -0.031763654749050005,
          0.2686066472680081
        ],
        [
          -0.05652301802528568,
          -0.5066366475944358
        ],
        [
          -0.011915242782513416,
          0.10112583710387106
        ],
        [
          -0.09486157627208787,
          -0.5122722919943059
        ],
        [
          -0.029037827086911557,
          0.1658763989086723
        ],
        [
          0.005842149370553249,
          0.07381384337631676
        ],
        [
          0.05362939072417291,
          1.075672535392472
        ]
      ]
    ],
    "same_tape_full_recorded_state_residual": {
      "finite": true,
      "max_abs": 1.0805911720979111e-11,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 9.099476380725058e-12
    },
    "same_tape_full_recorded_state_residual_tensor": [
      [
        [
          6.9383665479705314e-12,
          9.051093208256589e-14
        ],
        [
          -9.298117831235686e-15,
          -6.0285110237146e-14
        ],
        [
          4.3520742565306136e-13,
          -1.5987211554602254e-13
        ],
        [
          -1.211461486683163e-12,
          -3.9968028886505635e-15
        ],
        [
          1.2945200467129325e-13,
          1.9761969838327786e-14
        ],
        [
          -2.395764142626433e-12,
          2.370048601818553e-13
        ],
        [
          4.983374823908093e-13,
          -1.9984014443252818e-15
        ],
        [
          1.2752854328113017e-12,
          1.8884893648873913e-13
        ],
        [
          -1.0447198661722723e-13,
          3.3084646133829665e-14
        ],
        [
          -4.758034244378706e-13,
          1.6653345369377348e-15
        ],
        [
          1.390665360645471e-12,
          -4.1799896877137144e-14
        ],
        [
          2.1151136397890014e-13,
          -1.8197943152387097e-13
        ],
        [
          2.5249247137537623e-13,
          -1.2176371022576404e-13
        ],
        [
          -6.096623206275353e-12,
          8.523737271559639e-14
        ],
        [
          6.640243910283061e-13,
          3.552713678800501e-15
        ],
        [
          -9.058032102160496e-13,
          3.2307490016592055e-14
        ],
        [
          -1.1532406973824294e-12,
          -1.4835355166553654e-13
        ],
        [
          -6.058487045379479e-13,
          2.6881274983736603e-13
        ],
        [
          1.1207701433590955e-12,
          -4.1744385725905886e-14
        ],
        [
          2.2362667273512216e-13,
          7.216449660063518e-15
        ],
        [
          -1.7576495814353166e-12,
          9.298117831235686e-16
        ],
        [
          -8.14071032806396e-14,
          1.9484414082171497e-14
        ],
        [
          6.536993168992922e-13,
          -2.2537527399890678e-14
        ],
        [
          -4.4364512064021255e-13,
          1.326716514427062e-14
        ],
        [
          4.813927034774679e-12,
          -2.4347190930029683e-13
        ],
        [
          -3.2481795031458205e-12,
          -8.751332991607796e-14
        ],
        [
          -1.611905053877649e-14,
          -1.1102230246251565e-15
        ],
        [
          -3.562511396992818e-12,
          -8.076872504148014e-14
        ],
        [
          4.4207415506036796e-12,
          1.7930101847696278e-13
        ],
        [
          2.2598589666245061e-13,
          5.551115123125783e-16
        ],
        [
          -9.789669075388474e-13,
          1.5210055437364645e-14
        ],
        [
          -2.6556534749033744e-13,
          -3.452793606584237e-14
        ],
        [
          -1.5396017793989358e-12,
          -2.4369395390522186e-14
        ],
        [
          1.1353418205573007e-12,
          -8.22675261247241e-14
        ],
        [
          -1.464051102573194e-12,
          -6.972200594645983e-14
        ],
        [
          -7.835468385231081e-13,
          1.5275281040061373e-13
        ],
        [
          -7.34412530789541e-14,
          -5.773159728050814e-15
        ],
        [
          3.73603925574173e-13,
          -1.6181500583911657e-14
        ],
        [
          4.589106872288085e-13,
          4.7406523151494184e-14
        ],
        [
          4.39870362356487e-13,
          -1.87586057798228e-13
        ],
        [
          -5.884043252635252e-13,
          2.2315482794965646e-14
        ],
        [
          1.0805911720979111e-11,
          1.1102230246251565e-15
        ],
        [
          -2.645453300864631e-15,
          -6.827871601444713e-15
        ],
        [
          4.648087470471296e-13,
          1.1879386363489175e-14
        ],
        [
          -3.948508187079369e-13,
          -1.1046719095020308e-14
        ],
        [
          1.1380341113920167e-12,
          -1.3766765505351941e-14
        ],
        [
          1.1138867606064196e-12,
          -8.548717289613705e-14
        ],
        [
          2.041769531224702e-13,
          -9.103828801926284e-15
        ],
        [
          -1.668387650255454e-12,
          -1.4968581929508673e-13
        ],
        [
          -5.8772431366094224e-15,
          5.329070518200751e-15
        ]
      ]
    ],
    "same_tape_full_recorded_state_vjp": {
      "finite": true,
      "max_abs": 1.0755389718368409,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -6.4902786538727115
    },
    "same_tape_full_recorded_state_vjp_tensor": [
      [
        [
          0.03971382369618057,
          0.2164778309244629
        ],
        [
          0.01246540259805548,
          0.21033796049365555
        ],
        [
          0.035184540523049534,
          0.0992015811056434
        ],
        [
          0.029719639669935863,
          0.12495287450004361
        ],
        [
          -0.11780223532733847,
          -0.872415161155841
        ],
        [
          0.03270294652055629,
          0.09404141060204521
        ],
        [
          -0.0935687751540681,
          -0.7014348599399446
        ],
        [
          -0.06989051630194151,
          -0.276166016579917
        ],
        [
          0.03036471154249576,
          0.11929420461785412
        ],
        [
          -0.031108357673871944,
          -0.39166382896259067
        ],
        [
          -0.06769567956717837,
          -0.3601053217269579
        ],
        [
          0.015186090383167858,
          -0.016513915891989972
        ],
        [
          0.027981061507929644,
          0.11301695816110632
        ],
        [
          0.03737550068195733,
          0.09586584774343956
        ],
        [
          -0.07162557333129638,
          -0.309434569532332
        ],
        [
          -0.02447313423326805,
          -0.3196308780366821
        ],
        [
          0.029429127618274622,
          0.12405602795213541
        ],
        [
          -0.019927462487078773,
          0.16605200121272842
        ],
        [
          -0.10988052509621304,
          -0.895255293479184
        ],
        [
          -0.0644187891354607,
          -0.420833387403172
        ],
        [
          0.035289702299994674,
          0.09041767057950208
        ],
        [
          0.02549447091080917,
          0.16163495688901725
        ],
        [
          -0.1216130802349017,
          -0.9698644312016306
        ],
        [
          0.005662096231589864,
          0.30996512224195943
        ],
        [
          -0.15517042220019617,
          -0.9670506374541206
        ],
        [
          0.029833346472605382,
          0.10689062841595612
        ],
        [
          -0.049517866645502236,
          -0.535668305360939
        ],
        [
          0.035556139521521174,
          0.09837642024723209
        ],
        [
          -0.11231232208780934,
          -0.5399141705034108
        ],
        [
          -0.06449064883319139,
          -0.666661572047497
        ],
        [
          0.005313247147501393,
          0.2569610686963094
        ],
        [
          -0.020575225641951467,
          -0.182358480989927
        ],
        [
          0.02964524825961362,
          0.12665910207735293
        ],
        [
          -0.12214035980697638,
          -0.9530662259322921
        ],
        [
          0.031839180321714955,
          0.07072104924063738
        ],
        [
          0.028986696382555195,
          0.11523702521394664
        ],
        [
          0.017380698516773763,
          0.04958180938039318
        ],
        [
          -0.052863695342717246,
          0.040551764302627705
        ],
        [
          -0.099110335518316,
          -0.6213722601109889
        ],
        [
          0.031847999576652186,
          0.09014165317511642
        ],
        [
          0.00947764982774478,
          0.298099526180725
        ],
        [
          0.04898050493718531,
          0.31537521835398086
        ],
        [
          -0.008218788037313947,
          0.2786341428081259
        ],
        [
          -0.030440064373277134,
          0.2699696942679158
        ],
        [
          -0.0382443752010429,
          -0.4878131129790801
        ],
        [
          -0.025181884653688258,
          0.08746371268487674
        ],
        [
          -0.09269832782160858,
          -0.5100445564614144
        ],
        [
          -0.023997835727830222,
          0.17106663391282367
        ],
        [
          0.03480359132035188,
          0.10363863454256264
        ],
        [
          0.05349969348200519,
          1.0755389718368409
        ]
      ]
    ],
    "same_tape_identity_residual": {
      "finite": true,
      "max_abs": 3.4869329645914604e-13,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 5.0437987120233174e-12
    },
    "same_tape_identity_residual_tensor": [
      [
        [
          1.4288570326925765e-13,
          1.3600232051658168e-15
        ],
        [
          8.586881206085195e-16,
          7.438494264988549e-15
        ],
        [
          -2.646494134950217e-14,
          1.049160758270773e-14
        ],
        [
          8.192752032343265e-14,
          2.636779683484747e-16
        ],
        [
          1.5987211554602254e-14,
          2.220446049250313e-15
        ],
        [
          1.6034396033148823e-13,
          -1.5765166949677223e-14
        ],
        [
          8.487655023259322e-14,
          -4.440892098500626e-16
        ],
        [
          3.5985103785662886e-14,
          4.829470157119431e-15
        ],
        [
          7.344819197285801e-15,
          -2.067790383364354e-15
        ],
        [
          2.0456900062804095e-13,
          -7.216449660063518e-16
        ],
        [
          2.694372502887177e-13,
          -8.049116928532385e-15
        ],
        [
          -2.3130802828674746e-14,
          1.9904217163357885e-14
        ],
        [
          -1.5182299861749016e-14,
          7.230327447871332e-15
        ],
        [
          3.4869329645914604e-13,
          -4.773959005888173e-15
        ],
        [
          9.144074386568946e-14,
          3.885780586188048e-16
        ],
        [
          2.879918525877656e-13,
          -1.0269562977782698e-14
        ],
        [
          8.014422459012849e-14,
          1.0255685189974884e-14
        ],
        [
          -2.2662427490161008e-14,
          8.68749516769185e-15
        ],
        [
          1.69711467101763e-13,
          -6.439293542825908e-15
        ],
        [
          6.242228955954943e-14,
          1.9984014443252818e-15
        ],
        [
          9.736655925962623e-14,
          1.5265566588595902e-16
        ],
        [
          4.829470157119431e-15,
          -1.1934897514720433e-15
        ],
        [
          8.638922910364499e-14,
          -2.886579864025407e-15
        ],
        [
          8.386694116957472e-14,
          -2.4980018054066022e-15
        ],
        [
          3.036459972349803e-13,
          -1.532107773982716e-14
        ],
        [
          1.849909114781667e-13,
          5.23192600354605e-15
        ],
        [
          5.2062520961015935e-14,
          4.107825191113079e-15
        ],
        [
          2.0468349237745542e-13,
          4.468647674116255e-15
        ],
        [
          1.537936444861998e-13,
          6.328271240363392e-15
        ],
        [
          2.337435800470189e-13,
          6.661338147750939e-16
        ],
        [
          1.758957562936203e-13,
          -2.7200464103316335e-15
        ],
        [
          9.914985499293039e-14,
          1.2850831510036187e-14
        ],
        [
          1.1134496102904734e-13,
          1.7208456881689926e-15
        ],
        [
          1.4228895839352163e-13,
          -1.0658141036401503e-14
        ],
        [
          7.716050021144838e-14,
          3.5110803153770576e-15
        ],
        [
          4.540465226021695e-14,
          -8.840150833577809e-15
        ],
        [
          7.73686670285656e-15,
          6.036837696399289e-16
        ],
        [
          2.483430128208397e-14,
          -1.0824674490095276e-15
        ],
        [
          5.370703881624195e-14,
          5.551115123125783e-15
        ],
        [
          -3.076705556992465e-14,
          1.3239409568654992e-14
        ],
        [
          9.049358484780612e-14,
          -3.497202527569243e-15
        ],
        [
          2.2595120219293108e-13,
          -1.6653345369377348e-16
        ],
        [
          1.880440247958859e-15,
          4.773959005888173e-15
        ],
        [
          5.613565168260948e-14,
          1.3877787807814457e-15
        ],
        [
          1.9941687190438984e-13,
          5.717648576819556e-15
        ],
        [
          3.632510958695434e-14,
          -4.0245584642661925e-16
        ],
        [
          1.2194412146726563e-13,
          -9.43689570931383e-15
        ],
        [
          9.933026623443197e-14,
          -4.413136522884997e-15
        ],
        [
          1.0044742815296104e-13,
          8.951173136040325e-15
        ],
        [
          -3.400058012914542e-16,
          2.220446049250313e-16
        ]
      ]
    ],
    "same_tape_log_ess_carryover_vjp": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "same_tape_log_ess_carryover_vjp_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "same_tape_post_log_weights_vjp": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "same_tape_post_log_weights_vjp_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "same_tape_post_particles_vjp": {
      "finite": true,
      "max_abs": 1.075538971836846,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -6.490278653868659
    },
    "same_tape_post_particles_vjp_tensor": [
      [
        [
          0.039713823702976825,
          0.21647783092455253
        ],
        [
          0.012465402598045294,
          0.21033796049358783
        ],
        [
          0.03518454052351139,
          0.09920158110547302
        ],
        [
          0.029719639668642522,
          0.12495287450003933
        ],
        [
          -0.117802235327225,
          -0.8724151611558234
        ],
        [
          0.03270294651800021,
          0.09404141060229798
        ],
        [
          -0.09356877515365464,
          -0.7014348599399461
        ],
        [
          -0.0698905163007022,
          -0.2761660165797326
        ],
        [
          0.030364711542383738,
          0.11929420461788931
        ],
        [
          -0.03110835767455232,
          -0.3916638289625883
        ],
        [
          -0.06769567956605704,
          -0.3601053217269916
        ],
        [
          0.015186090383402462,
          -0.016513915892191852
        ],
        [
          0.02798106150819768,
          0.11301695816097723
        ],
        [
          0.03737550067551165,
          0.09586584774352946
        ],
        [
          -0.07162557333072361,
          -0.3094345695323289
        ],
        [
          -0.024473134234461846,
          -0.31963087803663953
        ],
        [
          0.029429127617041223,
          0.12405602795197679
        ],
        [
          -0.019927462487663306,
          0.16605200121298858
        ],
        [
          -0.10988052509526192,
          -0.8952552934792193
        ],
        [
          -0.06441878913529947,
          -0.4208333874031669
        ],
        [
          0.03528970229814021,
          0.090417670579503
        ],
        [
          0.02549447091072299,
          0.16163495688903795
        ],
        [
          -0.1216130802343344,
          -0.96986443120165
        ],
        [
          0.005662096231062397,
          0.30996512224197525
        ],
        [
          -0.155170422195686,
          -0.9670506374543488
        ],
        [
          0.02983334646917246,
          0.10689062841586339
        ],
        [
          -0.04951786664557041,
          -0.5356683053609442
        ],
        [
          0.03555613951775394,
          0.09837642024714688
        ],
        [
          -0.11231232208354314,
          -0.5399141705032378
        ],
        [
          -0.06449064883319916,
          -0.6666615720474971
        ],
        [
          0.005313247146346539,
          0.25696106869632734
        ],
        [
          -0.020575225642316175,
          -0.18235848098997437
        ],
        [
          0.029645248257962997,
          0.1266591020773268
        ],
        [
          -0.12214035980598337,
          -0.9530662259323639
        ],
        [
          0.031839180320172744,
          0.0707210492405641
        ],
        [
          0.02898669638172624,
          0.11523702521410828
        ],
        [
          0.01738069851669255,
          0.0495818093803868
        ],
        [
          -0.05286369534236843,
          0.040551764302612606
        ],
        [
          -0.09911033551791082,
          -0.621372260110947
        ],
        [
          0.03184799957712292,
          0.09014165317491551
        ],
        [
          0.009477649827065893,
          0.29809952618075075
        ],
        [
          0.04898050494776385,
          0.31537521835398197
        ],
        [
          -0.008218788037318472,
          0.2786341428081143
        ],
        [
          -0.030440064372868503,
          0.2699696942679263
        ],
        [
          -0.03824437520163715,
          -0.48781311297909674
        ],
        [
          -0.02518188465258664,
          0.08746371268486341
        ],
        [
          -0.09269832782061638,
          -0.5100445564614905
        ],
        [
          -0.023997835727725375,
          0.171066633912819
        ],
        [
          0.03480359131858268,
          0.10363863454240407
        ],
        [
          0.05349969348199965,
          1.075538971836846
        ]
      ]
    ],
    "same_tape_post_state_identity_residual": {
      "finite": true,
      "max_abs": 3.490541189421492e-13,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 5.045450168772447e-12
    },
    "same_tape_post_state_identity_residual_tensor": [
      [
        [
          1.4210854715202004e-13,
          8.881784197001252e-16
        ],
        [
          8.881784197001252e-16,
          7.438494264988549e-15
        ],
        [
          -2.6645352591003757e-14,
          1.0505485370515544e-14
        ],
        [
          8.18789480661053e-14,
          2.7755575615628914e-16
        ],
        [
          1.5987211554602254e-14,
          2.220446049250313e-15
        ],
        [
          1.603162047558726e-13,
          -1.5765166949677223e-14
        ],
        [
          8.487655023259322e-14,
          -4.440892098500626e-16
        ],
        [
          3.597122599785507e-14,
          4.440892098500626e-15
        ],
        [
          7.549516567451064e-15,
          -2.1094237467877974e-15
        ],
        [
          2.045724700749929e-13,
          -7.216449660063518e-16
        ],
        [
          2.69340105774063e-13,
          -8.104628079763643e-15
        ],
        [
          -2.3092638912203256e-14,
          1.990074771640593e-14
        ],
        [
          -1.554312234475219e-14,
          7.327471962526033e-15
        ],
        [
          3.490541189421492e-13,
          -4.6629367034256575e-15
        ],
        [
          9.126033262418787e-14,
          4.440892098500626e-16
        ],
        [
          2.879918525877656e-13,
          -1.0269562977782698e-14
        ],
        [
          8.01581023779363e-14,
          1.0269562977782698e-14
        ],
        [
          -2.1316282072803006e-14,
          8.659739592076221e-15
        ],
        [
          1.6964207816272392e-13,
          -6.439293542825908e-15
        ],
        [
          6.23945339839338e-14,
          2.1094237467877974e-15
        ],
        [
          9.681144774731365e-14,
          0.0
        ],
        [
          4.773959005888173e-15,
          -1.2212453270876722e-15
        ],
        [
          8.640310689145281e-14,
          -3.1086244689504383e-15
        ],
        [
          8.382183835919932e-14,
          -2.55351295663786e-15
        ],
        [
          3.0375701953744283e-13,
          -1.5210055437364645e-14
        ],
        [
          1.8474111129762605e-13,
          5.218048215738236e-15
        ],
        [
          5.205558206711203e-14,
          4.107825191113079e-15
        ],
        [
          2.0472512574087887e-13,
          4.440892098500626e-15
        ],
        [
          1.545430450278218e-13,
          6.217248937900877e-15
        ],
        [
          2.337574578348267e-13,
          6.661338147750939e-16
        ],
        [
          1.7588708267624042e-13,
          -2.7200464103316335e-15
        ],
        [
          9.914291609902648e-14,
          1.2850831510036187e-14
        ],
        [
          1.1102230246251565e-13,
          1.7486012637846216e-15
        ],
        [
          1.4233059175694507e-13,
          -1.0436096431476471e-14
        ],
        [
          7.815970093361102e-14,
          3.552713678800501e-15
        ],
        [
          4.54081217071689e-14,
          -8.881784197001252e-15
        ],
        [
          7.771561172376096e-15,
          6.036837696399289e-16
        ],
        [
          2.478572902475662e-14,
          -1.0824674490095276e-15
        ],
        [
          5.3734794391857577e-14,
          5.551115123125783e-15
        ],
        [
          -3.086420008457935e-14,
          1.3322676295501878e-14
        ],
        [
          9.048317650695026e-14,
          -3.4416913763379853e-15
        ],
        [
          2.2737367544323206e-13,
          0.0
        ],
        [
          1.880440247958859e-15,
          4.718447854656915e-15
        ],
        [
          5.617728504603292e-14,
          1.3877787807814457e-15
        ],
        [
          1.9939605522267811e-13,
          5.6066262743570405e-15
        ],
        [
          3.6415315207705135e-14,
          -4.440892098500626e-16
        ],
        [
          1.2168044349891716e-13,
          -9.43689570931383e-15
        ],
        [
          9.933026623443197e-14,
          -4.440892098500626e-15
        ],
        [
          1.0080825063596421e-13,
          8.881784197001252e-15
        ],
        [
          -3.400058012914542e-16,
          2.220446049250313e-16
        ]
      ]
    ],
    "same_tape_post_state_vjp": {
      "finite": true,
      "max_abs": 1.075538971836846,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -6.490278653868659
    },
    "same_tape_post_state_vjp_tensor": [
      [
        [
          0.039713823702976825,
          0.21647783092455253
        ],
        [
          0.012465402598045294,
          0.21033796049358783
        ],
        [
          0.03518454052351139,
          0.09920158110547302
        ],
        [
          0.029719639668642522,
          0.12495287450003933
        ],
        [
          -0.117802235327225,
          -0.8724151611558234
        ],
        [
          0.03270294651800021,
          0.09404141060229798
        ],
        [
          -0.09356877515365464,
          -0.7014348599399461
        ],
        [
          -0.0698905163007022,
          -0.2761660165797326
        ],
        [
          0.030364711542383738,
          0.11929420461788931
        ],
        [
          -0.03110835767455232,
          -0.3916638289625883
        ],
        [
          -0.06769567956605704,
          -0.3601053217269916
        ],
        [
          0.015186090383402462,
          -0.016513915892191852
        ],
        [
          0.02798106150819768,
          0.11301695816097723
        ],
        [
          0.03737550067551165,
          0.09586584774352946
        ],
        [
          -0.07162557333072361,
          -0.3094345695323289
        ],
        [
          -0.024473134234461846,
          -0.31963087803663953
        ],
        [
          0.029429127617041223,
          0.12405602795197679
        ],
        [
          -0.019927462487663306,
          0.16605200121298858
        ],
        [
          -0.10988052509526192,
          -0.8952552934792193
        ],
        [
          -0.06441878913529947,
          -0.4208333874031669
        ],
        [
          0.03528970229814021,
          0.090417670579503
        ],
        [
          0.02549447091072299,
          0.16163495688903795
        ],
        [
          -0.1216130802343344,
          -0.96986443120165
        ],
        [
          0.005662096231062397,
          0.30996512224197525
        ],
        [
          -0.155170422195686,
          -0.9670506374543488
        ],
        [
          0.02983334646917246,
          0.10689062841586339
        ],
        [
          -0.04951786664557041,
          -0.5356683053609442
        ],
        [
          0.03555613951775394,
          0.09837642024714688
        ],
        [
          -0.11231232208354314,
          -0.5399141705032378
        ],
        [
          -0.06449064883319916,
          -0.6666615720474971
        ],
        [
          0.005313247146346539,
          0.25696106869632734
        ],
        [
          -0.020575225642316175,
          -0.18235848098997437
        ],
        [
          0.029645248257962997,
          0.1266591020773268
        ],
        [
          -0.12214035980598337,
          -0.9530662259323639
        ],
        [
          0.031839180320172744,
          0.0707210492405641
        ],
        [
          0.02898669638172624,
          0.11523702521410828
        ],
        [
          0.01738069851669255,
          0.0495818093803868
        ],
        [
          -0.05286369534236843,
          0.040551764302612606
        ],
        [
          -0.09911033551791082,
          -0.621372260110947
        ],
        [
          0.03184799957712292,
          0.09014165317491551
        ],
        [
          0.009477649827065893,
          0.29809952618075075
        ],
        [
          0.04898050494776385,
          0.31537521835398197
        ],
        [
          -0.008218788037318472,
          0.2786341428081143
        ],
        [
          -0.030440064372868503,
          0.2699696942679263
        ],
        [
          -0.03824437520163715,
          -0.48781311297909674
        ],
        [
          -0.02518188465258664,
          0.08746371268486341
        ],
        [
          -0.09269832782061638,
          -0.5100445564614905
        ],
        [
          -0.023997835727725375,
          0.171066633912819
        ],
        [
          0.03480359131858268,
          0.10363863454240407
        ],
        [
          0.05349969348199965,
          1.075538971836846
        ]
      ]
    ],
    "same_tape_pre_current_ll_carryover_vjp": {
      "finite": true,
      "max_abs": 3.49220652395843e-13,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 5.047498009835838e-12
    },
    "same_tape_pre_current_ll_carryover_vjp_tensor": [
      [
        [
          1.4041545703946667e-13,
          1.8596235662471372e-15
        ],
        [
          1.0824674490095276e-15,
          7.424616477180734e-15
        ],
        [
          -2.842170943040401e-14,
          1.0516761073109393e-14
        ],
        [
          8.183557997920587e-14,
          2.706168622523819e-16
        ],
        [
          1.5765166949677223e-14,
          2.435551760271437e-15
        ],
        [
          1.6044110484614293e-13,
          -1.5855372570428017e-14
        ],
        [
          8.469613899109163e-14,
          -3.122502256758253e-16
        ],
        [
          3.522182545623309e-14,
          5.245803791353865e-15
        ],
        [
          6.328271240363392e-15,
          -1.9914625504213745e-15
        ],
        [
          2.0455512284023314e-13,
          -7.129713486264677e-16
        ],
        [
          2.69562150378988e-13,
          -8.101158632811689e-15
        ],
        [
          -2.310651670001107e-14,
          1.9888604652074093e-14
        ],
        [
          -1.4460654895742664e-14,
          6.9735883734267645e-15
        ],
        [
          3.49220652395843e-13,
          -4.864164626638967e-15
        ],
        [
          9.137135492665038e-14,
          4.961309141293668e-16
        ],
        [
          2.8796409701215e-13,
          -1.0277369233424594e-14
        ],
        [
          8.007136620413746e-14,
          1.0297318553398327e-14
        ],
        [
          -1.942890293094024e-14,
          8.628514569508638e-15
        ],
        [
          1.6975310046518644e-13,
          -6.265821195228227e-15
        ],
        [
          6.236677840831817e-14,
          1.970645868709653e-15
        ],
        [
          9.586775817638227e-14,
          -4.163336342344337e-17
        ],
        [
          5.245803791353865e-15,
          -1.2628786905111156e-15
        ],
        [
          8.642739302011648e-14,
          -2.9629076969683865e-15
        ],
        [
          8.382183835919932e-14,
          -2.5222879340702775e-15
        ],
        [
          3.0331293032759277e-13,
          -1.534883331544279e-14
        ],
        [
          1.857403120197887e-13,
          5.0306980803327406e-15
        ],
        [
          5.2062520961015935e-14,
          3.990731356484645e-15
        ],
        [
          2.0386470289679437e-13,
          4.6074255521944e-15
        ],
        [
          1.5693002453076588e-13,
          6.342149028171207e-15
        ],
        [
          2.337574578348267e-13,
          7.461479351045242e-16
        ],
        [
          1.759703494030873e-13,
          -2.7373936450914016e-15
        ],
        [
          9.892087149410145e-14,
          1.2852566233512164e-14
        ],
        [
          1.1052270210143433e-13,
          1.74946862552261e-15
        ],
        [
          1.420807915764044e-13,
          -1.029037965949442e-14
        ],
        [
          7.494005416219807e-14,
          3.552713678800501e-15
        ],
        [
          4.547057175230407e-14,
          -8.867906409193438e-15
        ],
        [
          7.605027718682322e-15,
          5.993469609499869e-16
        ],
        [
          2.468858451010192e-14,
          -1.0685896612017132e-15
        ],
        [
          5.4012350148013866e-14,
          5.5892790395972725e-15
        ],
        [
          -3.086420008457935e-14,
          1.317002062961592e-14
        ],
        [
          9.035827641667993e-14,
          -3.4243441415782172e-15
        ],
        [
          2.3236967905404526e-13,
          2.7755575615628914e-17
        ],
        [
          1.8752360775309285e-15,
          4.763550665032312e-15
        ],
        [
          5.6218918409456364e-14,
          1.4456751767921716e-15
        ],
        [
          1.9945156637390937e-13,
          5.585809592645319e-15
        ],
        [
          3.702593787124897e-14,
          -4.510281037539698e-16
        ],
        [
          1.220135104063047e-13,
          -9.343220641611083e-15
        ],
        [
          9.932332734052807e-14,
          -4.399258735077183e-15
        ],
        [
          9.942047185518277e-14,
          8.909539772616881e-15
        ],
        [
          -3.480288973678469e-16,
          3.0899761915836876e-16
        ]
      ]
    ],
    "same_tape_pre_log_weights_carryover_vjp": {
      "finite": true,
      "max_abs": 1.0810907724589924e-11,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -9.101422198364018e-12
    },
    "same_tape_pre_log_weights_carryover_vjp_tensor": [
      [
        [
          -6.936673457857978e-12,
          -9.14823772291129e-14
        ],
        [
          9.103828801926284e-15,
          6.0285110237146e-14
        ],
        [
          -4.334310688136611e-13,
          1.5985823775821473e-13
        ],
        [
          1.2115031200465864e-12,
          3.9968028886505635e-15
        ],
        [
          -1.2922996006636822e-13,
          -1.9984014443252818e-14
        ],
        [
          2.3956392425361628e-12,
          -2.369215934550084e-13
        ],
        [
          -4.981570711493077e-13,
          1.8596235662471372e-15
        ],
        [
          -1.2745360322696797e-12,
          -1.8962609260597674e-13
        ],
        [
          1.056932319443149e-13,
          -3.319566843629218e-14
        ],
        [
          4.758207716726304e-13,
          -1.654926196081874e-15
        ],
        [
          -1.3908874052503961e-12,
          4.178601908932933e-14
        ],
        [
          -2.1149748619109232e-13,
          1.8199330931167879e-13
        ],
        [
          -2.5357493882438575e-13,
          1.2212453270876722e-13
        ],
        [
          6.0964566728216596e-12,
          -8.504308368628699e-14
        ],
        [
          -6.641354133307686e-13,
          -3.594347042223944e-15
        ],
        [
          9.058309657916652e-13,
          -3.232830669830378e-14
        ],
        [
          1.1533274335562282e-12,
          1.4832579608992091e-13
        ],
        [
          6.039613253960852e-13,
          -2.687849942617504e-13
        ],
        [
          -1.120881165661558e-12,
          4.1466829969749597e-14
        ],
        [
          -2.2359891715950653e-13,
          -7.077671781985373e-15
        ],
        [
          1.758593271006248e-12,
          -8.881784197001252e-16
        ],
        [
          8.093525849517391e-14,
          -1.942890293094024e-14
        ],
        [
          -6.537270724749078e-13,
          2.2426505097428162e-14
        ],
        [
          4.4364512064021255e-13,
          -1.3350431871117507e-14
        ],
        [
          -4.813482945564829e-12,
          2.4358293160275934e-13
        ],
        [
          3.247180302423658e-12,
          8.770761894538737e-14
        ],
        [
          1.6115581091824538e-14,
          1.2353399553299838e-15
        ],
        [
          3.5633718198369024e-12,
          8.060219158778636e-14
        ],
        [
          -4.423128530106624e-12,
          -1.794120407794253e-13
        ],
        [
          -2.2598589666245061e-13,
          -7.213197053546061e-16
        ],
        [
          9.788836408120005e-13,
          -1.522393322517246e-14
        ],
        [
          2.657873920952625e-13,
          3.452620134236639e-14
        ],
        [
          1.5401013797600172e-12,
          2.4376334284426093e-14
        ],
        [
          -1.13509202037676e-12,
          8.221201497349284e-14
        ],
        [
          1.4672707493446069e-12,
          6.972200594645983e-14
        ],
        [
          7.83484388477973e-13,
          -1.5276668818842154e-13
        ],
        [
          7.360778653264788e-14,
          5.780098621954721e-15
        ],
        [
          -3.735067810595183e-13,
          1.6167622796103842e-14
        ],
        [
          -4.591882429849647e-13,
          -4.7406523151494184e-14
        ],
        [
          -4.39870362356487e-13,
          1.8773871346411397e-13
        ],
        [
          5.885292253537955e-13,
          -2.2287727219350018e-14
        ],
        [
          -1.0810907724589924e-11,
          -1.1102230246251565e-15
        ],
        [
          2.6506574712925612e-15,
          6.789707684973223e-15
        ],
        [
          -4.64850380410553e-13,
          -1.1955714196432154e-14
        ],
        [
          3.9479530755670567e-13,
          1.1060596882828122e-14
        ],
        [
          -1.1386447340555605e-12,
          1.3766765505351941e-14
        ],
        [
          -1.1142198275138071e-12,
          8.537615059367454e-14
        ],
        [
          -2.041700142285663e-13,
          9.048317650695026e-15
        ],
        [
          1.6697754290362354e-12,
          1.496580637194711e-13
        ],
        [
          5.880712583561376e-15,
          -5.218048215738236e-15
        ]
      ]
    ],
    "same_tape_reconstructed_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 1.075538971836846,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -6.490278653868656
    },
    "same_tape_reconstructed_pre_particle_adjoint_tensor": [
      [
        [
          0.03971382370297605,
          0.21647783092455206
        ],
        [
          0.012465402598045324,
          0.21033796049358783
        ],
        [
          0.03518454052351121,
          0.09920158110547303
        ],
        [
          0.029719639668642474,
          0.12495287450003935
        ],
        [
          -0.117802235327225,
          -0.8724151611558234
        ],
        [
          0.03270294651800018,
          0.09404141060229798
        ],
        [
          -0.09356877515365464,
          -0.7014348599399461
        ],
        [
          -0.06989051630070221,
          -0.276166016579733
        ],
        [
          0.030364711542383942,
          0.11929420461788927
        ],
        [
          -0.031108357674552316,
          -0.3916638289625883
        ],
        [
          -0.06769567956605714,
          -0.36010532172699167
        ],
        [
          0.0151860903834025,
          -0.016513915892191856
        ],
        [
          0.02798106150819732,
          0.11301695816097733
        ],
        [
          0.03737550067551201,
          0.09586584774352958
        ],
        [
          -0.0716255733307238,
          -0.30943456953232884
        ],
        [
          -0.024473134234461846,
          -0.31963087803663953
        ],
        [
          0.029429127617041237,
          0.1240560279519768
        ],
        [
          -0.01992746248766196,
          0.16605200121298855
        ],
        [
          -0.10988052509526199,
          -0.8952552934792193
        ],
        [
          -0.0644187891352995,
          -0.4208333874031668
        ],
        [
          0.03528970229813966,
          0.09041767057950285
        ],
        [
          0.025494470910722933,
          0.16163495688903792
        ],
        [
          -0.12161308023433438,
          -0.9698644312016502
        ],
        [
          0.005662096231062352,
          0.3099651222419752
        ],
        [
          -0.1551704221956859,
          -0.9670506374543487
        ],
        [
          0.02983334646917221,
          0.10689062841586337
        ],
        [
          -0.04951786664557042,
          -0.5356683053609442
        ],
        [
          0.03555613951775398,
          0.09837642024714685
        ],
        [
          -0.11231232208354239,
          -0.5399141705032379
        ],
        [
          -0.06449064883319915,
          -0.6666615720474971
        ],
        [
          0.0053132471463465305,
          0.25696106869632734
        ],
        [
          -0.020575225642316182,
          -0.18235848098997437
        ],
        [
          0.029645248257962675,
          0.12665910207732684
        ],
        [
          -0.12214035980598333,
          -0.9530662259323637
        ],
        [
          0.03183918032017374,
          0.07072104924056415
        ],
        [
          0.028986696381726244,
          0.11523702521410824
        ],
        [
          0.017380698516692585,
          0.0495818093803868
        ],
        [
          -0.052863695342368476,
          0.040551764302612606
        ],
        [
          -0.09911033551791079,
          -0.621372260110947
        ],
        [
          0.031847999577122824,
          0.0901416531749156
        ],
        [
          0.009477649827065882,
          0.2980995261807508
        ],
        [
          0.04898050494776527,
          0.31537521835398213
        ],
        [
          -0.008218788037318472,
          0.27863414280811427
        ],
        [
          -0.03044006437286846,
          0.2699696942679263
        ],
        [
          -0.03824437520163717,
          -0.48781311297909685
        ],
        [
          -0.02518188465258655,
          0.08746371268486337
        ],
        [
          -0.09269832782061664,
          -0.5100445564614905
        ],
        [
          -0.023997835727725375,
          0.17106663391281898
        ],
        [
          0.034803591318583044,
          0.103638634542404
        ],
        [
          0.05349969348199965,
          1.075538971836846
        ]
      ]
    ],
    "same_tape_transport_matrix_vjp": {
      "finite": true,
      "max_abs": 1.0756725353924719,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -7.598639330065231
    },
    "same_tape_transport_matrix_vjp_tensor": [
      [
        [
          0.06403292707157604,
          0.24152189401416724
        ],
        [
          -0.00047920785550381595,
          0.19700746734359142
        ],
        [
          0.006342801416669985,
          0.06950006115804847
        ],
        [
          0.005635186767100481,
          0.10015045687785518
        ],
        [
          -0.12181527845074491,
          -0.8765478342911556
        ],
        [
          0.003755605549266905,
          0.06423114076999814
        ],
        [
          -0.10014642738156454,
          -0.7082085939415877
        ],
        [
          -0.04553542371977448,
          -0.2510848914286421
        ],
        [
          0.006656261450842305,
          0.09487899856155912
        ],
        [
          -0.04889672842106922,
          -0.4099824763438252
        ],
        [
          -0.07359968106530812,
          -0.3661853232709358
        ],
        [
          -0.008570282811074303,
          -0.04097847365344168
        ],
        [
          0.006879105730599466,
          0.09128594679109336
        ],
        [
          0.0058100150501827486,
          0.06335938558194387
        ],
        [
          -0.07515635728279779,
          -0.3130706072065514
        ],
        [
          -0.042565723941785594,
          -0.3382628132365935
        ],
        [
          0.005433190686541717,
          0.09934476498831876
        ],
        [
          -0.007212663106187733,
          0.17914583255434413
        ],
        [
          -0.11622381492206202,
          -0.9017876786667098
        ],
        [
          -0.07249052443920101,
          -0.429145743542686
        ],
        [
          0.0034924072678883533,
          0.05767248870553132
        ],
        [
          0.008234983902825066,
          0.1438609594283301
        ],
        [
          -0.12674853624540874,
          -0.9751529766873095
        ],
        [
          -0.0026671284868329814,
          0.3013876008522727
        ],
        [
          -0.14996667709619782,
          -0.961691767162193
        ],
        [
          0.004537626221582158,
          0.08084083520696306
        ],
        [
          -0.06510201472331865,
          -0.5517170215385712
        ],
        [
          0.0054159615069142575,
          0.06733775454492708
        ],
        [
          -0.09487745344480203,
          -0.5219595632329903
        ],
        [
          -0.07885290265043704,
          -0.6814519689324575
        ],
        [
          -0.004408075714471021,
          0.24694995030307348
        ],
        [
          -0.03583400100816192,
          -0.19807212499816237
        ],
        [
          0.006151387802174391,
          0.10246488263776166
        ],
        [
          -0.1266129541190344,
          -0.9576721496151805
        ],
        [
          0.0047295449745412554,
          0.04280326758381525
        ],
        [
          0.00631508120196278,
          0.09188956242735996
        ],
        [
          -0.00445358764186865,
          0.027096636642573068
        ],
        [
          -0.050625941680041836,
          0.04285622606869424
        ],
        [
          -0.10223978203558781,
          -0.6245949963622134
        ],
        [
          0.003661845733453739,
          0.061115261682790245
        ],
        [
          6.916069679396841e-05,
          0.28841056718480684
        ],
        [
          0.06770817305487498,
          0.33466116383013844
        ],
        [
          -0.014424997532838865,
          0.27224292435744285
        ],
        [
          -0.03176365474910614,
          0.2686066472680067
        ],
        [
          -0.056523018025485094,
          -0.5066366475944416
        ],
        [
          -0.01191524278254974,
          0.10112583710387146
        ],
        [
          -0.09486157627220981,
          -0.5122722919942965
        ],
        [
          -0.029037827087010887,
          0.16587639890867673
        ],
        [
          0.005842149370452798,
          0.07381384337630781
        ],
        [
          0.05362939072417325,
          1.0756725353924719
        ]
      ]
    ]
  },
  "resampling_flag": [
    true
  ],
  "settings": {
    "T": 100,
    "batch_size": 1,
    "convergence_threshold": 1e-06,
    "data_seed": 123,
    "dtype": "float64",
    "epsilon": 0.25,
    "filter_seed": 1234,
    "max_iter": 500,
    "mesh_index": 173,
    "n_particles": 50,
    "resampling_neff": 0.9999,
    "scaling": 0.85,
    "target_time_index": 93,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ],
    "transport_backward": "FilterFlow custom gradient clips d_transport to [-1,1]"
  },
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-04 05:17:31.393698: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780521451.410971     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780521451.417226     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780521451.430874     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780521451.430934     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780521451.430939     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780521451.430941     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-04 05:17:31.434788: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-04 05:17:33.629147: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
  "target_scalar": -141.71711568701727,
  "total_gradient_diag": [
    9105.143875898348,
    57.123649814928335
  ],
  "transport_upstream_clip_fraction": 0.88,
  "value_summaries": {
    "fresh_dist_log_prob": {
      "finite": true,
      "max_abs": 4.717860757900072,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709028291
    },
    "fresh_proposal_loc": {
      "finite": true,
      "max_abs": 519.218844108408,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.41668017897
    },
    "fresh_proposal_mean": {
      "finite": true,
      "max_abs": 519.218844108408,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.41668017897
    },
    "increment": {
      "finite": true,
      "max_abs": 0.7603288017481669,
      "shape": [
        1
      ],
      "sum": -0.7603288017481669
    },
    "log_ess": {
      "finite": true,
      "max_abs": 3.827488817906256,
      "shape": [
        1
      ],
      "sum": 3.827488817906256
    },
    "manual_dist_log_prob": {
      "finite": true,
      "max_abs": 4.717860757900072,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709028291
    },
    "manual_proposal_mean": {
      "finite": true,
      "max_abs": 519.218844108408,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.41668017897
    },
    "normalized": {
      "finite": true,
      "max_abs": 5.01676613455824,
      "shape": [
        1,
        50
      ],
      "sum": -200.45945262137084
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 1.383508147384548,
      "shape": [
        1,
        50
      ],
      "sum": 53.39734671638709
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 3.912023005428146,
      "shape": [
        1,
        50
      ],
      "sum": -195.60115027140728
    },
    "post_particles": {
      "finite": true,
      "max_abs": 509.3920006636405,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 26682.33828065031
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 141.71711568701727,
      "shape": [
        1
      ],
      "sum": -141.71711568701727
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 5.01676613455824,
      "shape": [
        1,
        50
      ],
      "sum": -200.45945262137084
    },
    "pre_current_log_likelihoods": {
      "finite": true,
      "max_abs": 140.9567868852691,
      "shape": [
        1
      ],
      "sum": -140.9567868852691
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 7.591460567082821,
      "shape": [
        1,
        50
      ],
      "sum": -200.4151594423704
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 509.5286014281523,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 26683.72920399584
    },
    "proposal_dist_log_prob": {
      "finite": true,
      "max_abs": 4.7178607579005885,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709029018
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 4.717860757900072,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709028291
    },
    "proposal_loc": {
      "finite": true,
      "max_abs": 519.218844108408,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.41668017897
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 519.218844108408,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.41668017897
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 519.3668650770238,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27168.99351217468
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 4.94883541438441,
      "shape": [
        1,
        50
      ],
      "sum": -82.30866844473067
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 0.3191070695507616,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 49.999999999999986
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 5.777094936306407,
      "shape": [
        1,
        50
      ],
      "sum": -238.47589270877918
    }
  }
}
```

## BayesFilter VJP

```json
{
  "backend": "tensorflow_tensorflow_probability",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "filterflow_proposal_mean_internal_probe": null,
  "gradient_summaries": {
    "fresh_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "fresh_proposal_loc": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "increment": {
      "finite": true,
      "max_abs": 1.0,
      "shape": [
        1
      ],
      "sum": 1.0
    },
    "log_ess": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1
      ],
      "sum": 0.0
    },
    "manual_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "manual_proposal_mean": {
      "finite": true,
      "max_abs": 0.7827423714161357,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.4898093699805401
    },
    "normalized": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 0.02912639608646427,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 0.02912639608646427,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_particles": {
      "finite": true,
      "max_abs": 0.030135380107735612,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.1083544289433924
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 1.0,
      "shape": [
        1
      ],
      "sum": 1.0
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "pre_current_log_likelihoods": {
      "finite": true,
      "max_abs": 1.0,
      "shape": [
        1
      ],
      "sum": 1.0
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 1.1695816018044372,
      "shape": [
        1,
        50
      ],
      "sum": 26.131150130766635
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 15.010857686626197,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 37.70968325635589
    },
    "proposal_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50
      ],
      "sum": 0.0
    },
    "proposal_loc": {
      "finite": true,
      "max_abs": 0.7827423714161357,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.4898093699805401
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 0.7827423714161357,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.4898093699805401
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 0.7827423714161357,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.4898093699805401
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 0.02912639608646427,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 15.683856022178455,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 14590.183137748696
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 0.02912639608646427,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    }
  },
  "graph_embedding_probe": {
    "contract": "BayesFilter-only same-tape graph embedding probe. Compare the recorded transport matrix VJP in the full persistent tape with a fresh local transport derivative that treats pre-particles and pre-log-weights as independent inputs.",
    "summaries": {
      "local_transport_log_weights_vjp_clipped_upstream": {
        "finite": true,
        "max_abs": 1.1695816018044372,
        "shape": [
          1,
          50
        ],
        "sum": 26.131150130766635
      },
      "local_transport_log_weights_vjp_manual_clipped_upstream": {
        "finite": true,
        "max_abs": 1.1695816018044372,
        "shape": [
          1,
          50
        ],
        "sum": 26.131150130766635
      },
      "local_transport_log_weights_vjp_raw_upstream": {
        "finite": true,
        "max_abs": 14.634532991149952,
        "shape": [
          1,
          50
        ],
        "sum": 291.3686439533235
      },
      "local_transport_particles_vjp_clipped_upstream": {
        "finite": true,
        "max_abs": 1.0756725359001307,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -7.598639322386266
      },
      "local_transport_particles_vjp_manual_clipped_upstream": {
        "finite": true,
        "max_abs": 1.0756725359001307,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -7.598639322386266
      },
      "local_transport_particles_vjp_raw_upstream": {
        "finite": true,
        "max_abs": 13.357873807116519,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -66.73543425621781
      },
      "post_particles_to_pre_particles_vjp": {
        "finite": true,
        "max_abs": 15.33929208686093,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 35.82648627304192
      },
      "pre_log_weights_to_pre_particles_vjp": {
        "finite": true,
        "max_abs": 15.290311581828018,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 42.316764919860944
      },
      "recorded_minus_local_clipped_particles_vjp": {
        "finite": true,
        "max_abs": 15.290311581828018,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 42.31676491986094
      },
      "recorded_transport_vjp_clipped_upstream": {
        "finite": true,
        "max_abs": 15.358019754965156,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 34.718125597474675
      },
      "recorded_transport_vjp_raw_upstream": {
        "finite": true,
        "max_abs": 15.358019754965156,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 34.718125597474675
      }
    },
    "tensors": {
      "local_transport_log_weights_vjp_clipped_upstream": [
        [
          -0.4881572454275016,
          0.4596273859900515,
          1.0197900416496097,
          0.8459544490989186,
          0.43700900200260606,
          1.0172519575103345,
          0.46893915792419877,
          -0.2624208409430303,
          0.8494269624561539,
          0.7123854033373449,
          0.3861821023399225,
          0.8373831540385743,
          0.7664454902380158,
          1.1453096237119946,
          0.3184864385255938,
          0.7051883142842341,
          0.8408650300050833,
          -0.08225588985637905,
          0.5108396953796058,
          0.44659256257002056,
          1.1695816018044372,
          0.6095064698887948,
          0.4869092494141889,
          0.30949656372495776,
          0.2581481769639048,
          0.9149687234471656,
          0.6749241063214306,
          1.092819101580915,
          -0.05095642240039755,
          0.6621584377987461,
          0.3588845848005094,
          0.6057565500858078,
          0.8227824834524455,
          0.4704275804006213,
          1.0426649601079183,
          0.8182118042951884,
          0.7666932285715018,
          0.13965303306704088,
          0.3649906276487769,
          0.9869656373299991,
          0.3423761005872329,
          -0.34060354075123583,
          0.2565865154764171,
          0.15044852004106596,
          0.7389513144818738,
          -0.07820423881560157,
          0.3298236265531238,
          0.2485181178126216,
          1.0391582506060817,
          0.004666171635752741
        ]
      ],
      "local_transport_log_weights_vjp_manual_clipped_upstream": [
        [
          -0.4881572454275016,
          0.4596273859900515,
          1.0197900416496097,
          0.8459544490989186,
          0.43700900200260606,
          1.0172519575103345,
          0.46893915792419877,
          -0.2624208409430303,
          0.8494269624561539,
          0.7123854033373449,
          0.3861821023399225,
          0.8373831540385743,
          0.7664454902380158,
          1.1453096237119946,
          0.3184864385255938,
          0.7051883142842341,
          0.8408650300050833,
          -0.08225588985637905,
          0.5108396953796058,
          0.44659256257002056,
          1.1695816018044372,
          0.6095064698887948,
          0.4869092494141889,
          0.30949656372495776,
          0.2581481769639048,
          0.9149687234471656,
          0.6749241063214306,
          1.092819101580915,
          -0.05095642240039755,
          0.6621584377987461,
          0.3588845848005094,
          0.6057565500858078,
          0.8227824834524455,
          0.4704275804006213,
          1.0426649601079183,
          0.8182118042951884,
          0.7666932285715018,
          0.13965303306704088,
          0.3649906276487769,
          0.9869656373299991,
          0.3423761005872329,
          -0.34060354075123583,
          0.2565865154764171,
          0.15044852004106596,
          0.7389513144818738,
          -0.07820423881560157,
          0.3298236265531238,
          0.2485181178126216,
          1.0391582506060817,
          0.004666171635752741
        ]
      ],
      "local_transport_log_weights_vjp_raw_upstream": [
        [
          -7.284743236845949,
          5.346637323494694,
          12.50416381429502,
          10.350132344336647,
          4.045027368616827,
          12.457453521151471,
          4.561544554940404,
          -4.88900592064935,
          10.519513764282143,
          7.822186827687948,
          3.8055444989143155,
          9.824870620807818,
          9.540032714688369,
          14.247181233051489,
          3.0075109170086236,
          7.815764401557762,
          10.260145289758714,
          -2.0494667890125307,
          4.8902916092121975,
          4.527340624373327,
          14.634532991149952,
          7.4880633192839445,
          4.571649060747293,
          3.506587301766804,
          1.6631388884308764,
          11.389649835423542,
          7.233094011663502,
          13.598890138215229,
          -2.193849477678109,
          6.979509577930332,
          4.077266000860734,
          6.677073370795744,
          10.005243124928677,
          4.370892046980157,
          13.137479770727047,
          10.166589101276545,
          9.033177461164193,
          0.9580562202243232,
          3.3563553498624197,
          12.030167173019967,
          3.9246940527467604,
          -5.2196353693541795,
          2.78789166746621,
          1.387827758361163,
          8.083506742974834,
          -2.0362222661534934,
          2.973213480377447,
          2.579131771464135,
          12.875817564360052,
          0.02672780263749075
        ]
      ],
      "local_transport_particles_vjp_clipped_upstream": [
        [
          [
            0.06403292707707071,
            0.2415218940381026
          ],
          [
            -0.0004792076741009629,
            0.1970074677000562
          ],
          [
            0.006342801493889971,
            0.06950006074461225
          ],
          [
            0.005635186847187305,
            0.10015045673105226
          ],
          [
            -0.12181527760660084,
            -0.8765478354192887
          ],
          [
            0.003755605633484389,
            0.06423114049874867
          ],
          [
            -0.10014642664742018,
            -0.7082085950284341
          ],
          [
            -0.04553542327376908,
            -0.25108488998775813
          ],
          [
            0.006656261492177479,
            0.09487899852934513
          ],
          [
            -0.04889672789580372,
            -0.40998247812426336
          ],
          [
            -0.07359968052470779,
            -0.3661853239321641
          ],
          [
            -0.008570282556874986,
            -0.04097847465874207
          ],
          [
            0.006879105766615872,
            0.091285946997707
          ],
          [
            0.0058100150788183745,
            0.06335938547103574
          ],
          [
            -0.07515635673971767,
            -0.31307060721084257
          ],
          [
            -0.04256572344613307,
            -0.33826281462242513
          ],
          [
            0.005433190773068386,
            0.09934476475683161
          ],
          [
            -0.007212662515953333,
            0.17914583483613647
          ],
          [
            -0.11622381412145942,
            -0.9017876801667765
          ],
          [
            -0.07249052388771228,
            -0.42914574509068476
          ],
          [
            0.003492407282715668,
            0.0576724887241854
          ],
          [
            0.008234983970633873,
            0.14386095987109468
          ],
          [
            -0.12674853545804338,
            -0.9751529786374213
          ],
          [
            -0.0026671283197933046,
            0.3013876013312607
          ],
          [
            -0.14996667622398563,
            -0.961691767419002
          ],
          [
            0.004537626244364038,
            0.08084083523113096
          ],
          [
            -0.06510201405982403,
            -0.5517170230565371
          ],
          [
            0.00541596153547727,
            0.06733775447002902
          ],
          [
            -0.09487745282931091,
            -0.5219595615583024
          ],
          [
            -0.07885290203089192,
            -0.6814519712867668
          ],
          [
            -0.0044080755262941845,
            0.24694995101208703
          ],
          [
            -0.035834000601813645,
            -0.19807212585485862
          ],
          [
            0.006151387894927673,
            0.10246488225949524
          ],
          [
            -0.12661295325161295,
            -0.9576721508528547
          ],
          [
            0.004729544985707861,
            0.04280326769468407
          ],
          [
            0.0063150812323601,
            0.09188956244086639
          ],
          [
            -0.004453587410981241,
            0.027096636051445955
          ],
          [
            -0.050625941170007654,
            0.042856227429904366
          ],
          [
            -0.1022397813293461,
            -0.6245949973064868
          ],
          [
            0.0036618458352018265,
            0.06111526130496479
          ],
          [
            6.91608571416393e-05,
            0.2884105679760818
          ],
          [
            0.06770817313713785,
            0.3346611640047005
          ],
          [
            -0.014424997335448752,
            0.2722429246060361
          ],
          [
            -0.031763654489928475,
            0.2686066479036396
          ],
          [
            -0.05652301742775208,
            -0.5066366491366315
          ],
          [
            -0.0119152422187549,
            0.10112583951834317
          ],
          [
            -0.09486157562944786,
            -0.5122722921124088
          ],
          [
            -0.029037826811141705,
            0.1658763994286233
          ],
          [
            0.005842149415740667,
            0.0738138433199254
          ],
          [
            0.05362939075503884,
            1.0756725359001307
          ]
        ]
      ],
      "local_transport_particles_vjp_manual_clipped_upstream": [
        [
          [
            0.06403292707707071,
            0.2415218940381026
          ],
          [
            -0.0004792076741009629,
            0.1970074677000562
          ],
          [
            0.006342801493889971,
            0.06950006074461225
          ],
          [
            0.005635186847187305,
            0.10015045673105226
          ],
          [
            -0.12181527760660084,
            -0.8765478354192887
          ],
          [
            0.003755605633484389,
            0.06423114049874867
          ],
          [
            -0.10014642664742018,
            -0.7082085950284341
          ],
          [
            -0.04553542327376908,
            -0.25108488998775813
          ],
          [
            0.006656261492177479,
            0.09487899852934513
          ],
          [
            -0.04889672789580372,
            -0.40998247812426336
          ],
          [
            -0.07359968052470779,
            -0.3661853239321641
          ],
          [
            -0.008570282556874986,
            -0.04097847465874207
          ],
          [
            0.006879105766615872,
            0.091285946997707
          ],
          [
            0.0058100150788183745,
            0.06335938547103574
          ],
          [
            -0.07515635673971767,
            -0.31307060721084257
          ],
          [
            -0.04256572344613307,
            -0.33826281462242513
          ],
          [
            0.005433190773068386,
            0.09934476475683161
          ],
          [
            -0.007212662515953333,
            0.17914583483613647
          ],
          [
            -0.11622381412145942,
            -0.9017876801667765
          ],
          [
            -0.07249052388771228,
            -0.42914574509068476
          ],
          [
            0.003492407282715668,
            0.0576724887241854
          ],
          [
            0.008234983970633873,
            0.14386095987109468
          ],
          [
            -0.12674853545804338,
            -0.9751529786374213
          ],
          [
            -0.0026671283197933046,
            0.3013876013312607
          ],
          [
            -0.14996667622398563,
            -0.961691767419002
          ],
          [
            0.004537626244364038,
            0.08084083523113096
          ],
          [
            -0.06510201405982403,
            -0.5517170230565371
          ],
          [
            0.00541596153547727,
            0.06733775447002902
          ],
          [
            -0.09487745282931091,
            -0.5219595615583024
          ],
          [
            -0.07885290203089192,
            -0.6814519712867668
          ],
          [
            -0.0044080755262941845,
            0.24694995101208703
          ],
          [
            -0.035834000601813645,
            -0.19807212585485862
          ],
          [
            0.006151387894927673,
            0.10246488225949524
          ],
          [
            -0.12661295325161295,
            -0.9576721508528547
          ],
          [
            0.004729544985707861,
            0.04280326769468407
          ],
          [
            0.0063150812323601,
            0.09188956244086639
          ],
          [
            -0.004453587410981241,
            0.027096636051445955
          ],
          [
            -0.050625941170007654,
            0.042856227429904366
          ],
          [
            -0.1022397813293461,
            -0.6245949973064868
          ],
          [
            0.0036618458352018265,
            0.06111526130496479
          ],
          [
            6.91608571416393e-05,
            0.2884105679760818
          ],
          [
            0.06770817313713785,
            0.3346611640047005
          ],
          [
            -0.014424997335448752,
            0.2722429246060361
          ],
          [
            -0.031763654489928475,
            0.2686066479036396
          ],
          [
            -0.05652301742775208,
            -0.5066366491366315
          ],
          [
            -0.0119152422187549,
            0.10112583951834317
          ],
          [
            -0.09486157562944786,
            -0.5122722921124088
          ],
          [
            -0.029037826811141705,
            0.1658763994286233
          ],
          [
            0.005842149415740667,
            0.0738138433199254
          ],
          [
            0.05362939075503884,
            1.0756725359001307
          ]
        ]
      ],
      "local_transport_particles_vjp_raw_upstream": [
        [
          [
            1.1981436787302553,
            3.7626946364395497
          ],
          [
            0.21964558201719478,
            2.16356993851677
          ],
          [
            0.30825882380493935,
            0.4971866298600191
          ],
          [
            0.2200359830248742,
            1.0569403926410894
          ],
          [
            -0.3573441617601872,
            -10.197847704352409
          ],
          [
            0.20578558972970773,
            0.3944256065058308
          ],
          [
            -0.1934846056798003,
            -8.619028149480648
          ],
          [
            0.2438494279097332,
            -2.686256990376368
          ],
          [
            0.25295576043005846,
            1.6923738286992303
          ],
          [
            0.10069089204170258,
            -7.122790040902414
          ],
          [
            -0.09844027522473252,
            -4.391785115384883
          ],
          [
            0.21137799869224072,
            -2.620218523511461
          ],
          [
            0.26659199134005207,
            1.93112767999707
          ],
          [
            0.3392352818794693,
            1.598656191562335
          ],
          [
            -0.14758071815579332,
            -3.354114007649551
          ],
          [
            0.0938365026670817,
            -6.087392932408063
          ],
          [
            0.2231439515733148,
            0.9002229101560999
          ],
          [
            0.3967515462190364,
            2.2317248848269693
          ],
          [
            -0.19943222062318464,
            -11.079253652603525
          ],
          [
            -0.08852221990154796,
            -5.401555280810619
          ],
          [
            0.2567988521095442,
            1.8976907603433288
          ],
          [
            0.22739272713704897,
            2.138199294332179
          ],
          [
            -0.32861619863258795,
            -11.618615951318967
          ],
          [
            0.21175270917184114,
            4.003340345896315
          ],
          [
            -0.6371344091994919,
            -10.644175203473699
          ],
          [
            0.19743960102589012,
            1.771216665150412
          ],
          [
            0.03753314907503812,
            -8.471860011493838
          ],
          [
            0.29832652853395014,
            1.6462750708009142
          ],
          [
            -0.1777155047500434,
            -5.684078241375212
          ],
          [
            -0.037593468084040106,
            -9.716489037597338
          ],
          [
            0.20912072025354758,
            3.081678172844081
          ],
          [
            0.14890255664393937,
            -4.070159192997096
          ],
          [
            0.25993303611150786,
            0.7469208178519084
          ],
          [
            -0.3202761675714559,
            -11.335025342755566
          ],
          [
            0.475059872976309,
            2.190403601664101
          ],
          [
            0.24357391015861923,
            1.840848790016478
          ],
          [
            0.21774298904929448,
            -1.287904421219007
          ],
          [
            -0.04562877773686041,
            1.2500076648511034
          ],
          [
            -0.30210444463260644,
            -6.998692527833443
          ],
          [
            0.22165630283537754,
            0.05792039664131255
          ],
          [
            0.23670724833824863,
            3.701855998713399
          ],
          [
            1.1226353488133622,
            4.395992706453895
          ],
          [
            0.1142302381838299,
            3.8518982451515886
          ],
          [
            -0.02958019056896104,
            4.018848971752786
          ],
          [
            0.04793286072632369,
            -8.257994742776622
          ],
          [
            0.4283571917403997,
            1.4667410646322598
          ],
          [
            -0.230244369538115,
            -5.6136570754560156
          ],
          [
            0.02442277054834015,
            2.5466390319474157
          ],
          [
            0.2806001401370851,
            1.394782592493513
          ],
          [
            0.5886791601307152,
            13.357873807116519
          ]
        ]
      ],
      "post_particles_to_pre_particles_vjp": [
        [
          [
            2.5260674285031204,
            6.095955642968497
          ],
          [
            -1.660443784207069,
            0.5292371548283952
          ],
          [
            9.814683694996665,
            0.20153262110544062
          ],
          [
            -0.37168807624590994,
            0.510710603386948
          ],
          [
            0.8446662516071439,
            -0.5821988860672042
          ],
          [
            -2.5618018052605684,
            0.838714716158976
          ],
          [
            -0.6835444970389001,
            -0.6036308499139642
          ],
          [
            -3.6103960800365855,
            3.540730815208073
          ],
          [
            2.0046550868458497,
            0.5543625542719248
          ],
          [
            0.005456297646158435,
            -0.41127685647659623
          ],
          [
            -1.4912869145128456,
            -0.2787945714311374
          ],
          [
            0.8686177801123294,
            0.04827186690047325
          ],
          [
            1.638997148949179,
            1.1539159965231485
          ],
          [
            5.8052090515794905,
            1.020877889289757
          ],
          [
            -1.52252763201391,
            -0.20459354204514052
          ],
          [
            -0.7576724230407887,
            -0.302919618124177
          ],
          [
            0.10056681454046537,
            0.45873825448621275
          ],
          [
            8.912044227022017,
            0.8339003792660764
          ],
          [
            -4.558031065458771,
            -0.4900821980032409
          ],
          [
            -0.014944060894954703,
            -0.3087501739547366
          ],
          [
            -9.725255122549314,
            2.1093944155775666
          ],
          [
            -0.9347608960301632,
            0.9557539403497797
          ],
          [
            -0.8379804247763568,
            -0.6680992386752795
          ],
          [
            0.22396255974481757,
            0.3985323980782294
          ],
          [
            1.7786752195651299,
            -0.10308014437764512
          ],
          [
            -6.300807441412935,
            1.1746538738204122
          ],
          [
            -0.06047336662554699,
            -0.5344974365534937
          ],
          [
            1.707457971593639,
            1.0663571699854655
          ],
          [
            -13.9178868384009,
            2.138684238631564
          ],
          [
            0.12779078066813815,
            -0.6671564902663425
          ],
          [
            -0.14500590430516938,
            0.38148655753738897
          ],
          [
            0.5880111744262401,
            -0.1700971248766467
          ],
          [
            4.255585054048362,
            0.18714568294783815
          ],
          [
            -2.085615959374363,
            -0.6286308573732382
          ],
          [
            7.798141411035818,
            1.5902494360675001
          ],
          [
            0.6799511572149766,
            0.6538720312002853
          ],
          [
            0.6124911234183816,
            0.09275888775894958
          ],
          [
            0.427416566647802,
            0.15922537742253684
          ],
          [
            1.811021336246557,
            -0.3588437044468357
          ],
          [
            -0.9253944567985909,
            0.9316862740024985
          ],
          [
            0.49465312609694156,
            0.410990622962218
          ],
          [
            15.33929208686093,
            2.3049850932560805
          ],
          [
            -0.08882316961842769,
            0.30243173642154186
          ],
          [
            -0.5671457262310396,
            0.2782124212032753
          ],
          [
            -0.7274323968234401,
            -0.4493436379986684
          ],
          [
            -6.047666584313859,
            1.6438397789953945
          ],
          [
            -2.736491141774307,
            -0.25508043297956035
          ],
          [
            0.13007706117560403,
            0.14367575248920395
          ],
          [
            1.592546522241694,
            1.213972368328584
          ],
          [
            0.09871662533626692,
            1.0650276947965935
          ]
        ]
      ],
      "pre_log_weights_to_pre_particles_vjp": [
        [
          [
            2.4863536047941945,
            5.879477812019541
          ],
          [
            -1.6729091869681012,
            0.31889919399730743
          ],
          [
            9.779499154388084,
            0.10233104040531872
          ],
          [
            -0.4014077159977325,
            0.3857577290305261
          ],
          [
            0.9624684860946057,
            0.2902162762212638
          ],
          [
            -2.59450475186808,
            0.7446733058224757
          ],
          [
            -0.5899757226071108,
            0.09780401112547338
          ],
          [
            -3.5405055641685643,
            3.816896830360644
          ],
          [
            1.9742903752610323,
            0.43506834968511837
          ],
          [
            0.03656465479486018,
            -0.019613025734172302
          ],
          [
            -1.4235912354741171,
            0.08131075097075
          ],
          [
            0.8534316894680518,
            0.06478578379109076
          ],
          [
            1.6110160874260118,
            1.0408990381772314
          ],
          [
            5.767833550868766,
            0.9250120416503627
          ],
          [
            -1.4509020592090656,
            0.1048410275091932
          ],
          [
            -0.733199289304897,
            0.016711261295289652
          ],
          [
            0.07113768682896549,
            0.33468222675755466
          ],
          [
            8.931971688923479,
            0.6678483757754503
          ],
          [
            -4.4481505411546625,
            0.4051730969857756
          ],
          [
            0.049474727690355935,
            0.11208321499797358
          ],
          [
            -9.760544824868337,
            2.0189767449731737
          ],
          [
            -0.960255366976956,
            0.7941189830506621
          ],
          [
            -0.7163673453059671,
            0.30176519450060135
          ],
          [
            0.21830046335857725,
            0.08856727536948153
          ],
          [
            1.9338456408977927,
            0.8639704933429756
          ],
          [
            -6.330640787912568,
            1.0677632453724732
          ],
          [
            -0.010955500649316037,
            0.0011708703193974584
          ],
          [
            1.6719018320383088,
            0.9679807498039347
          ],
          [
            -13.805574516918355,
            2.67859840747504
          ],
          [
            0.19228142890249436,
            -0.000494915843216766
          ],
          [
            -0.15031915161293233,
            0.12452548815960622
          ],
          [
            0.608586399688508,
            0.012261356997107908
          ],
          [
            4.225939805685711,
            0.06048658123648686
          ],
          [
            -1.9634756004283513,
            0.3244353698044715
          ],
          [
            7.766302230716338,
            1.5195283867282823
          ],
          [
            0.6509644607963803,
            0.5386350059660049
          ],
          [
            0.5951104246658152,
            0.04317707896455473
          ],
          [
            0.4802802614932452,
            0.11867361177221385
          ],
          [
            1.910131671060952,
            0.26252855661119195
          ],
          [
            -0.9572424564793375,
            0.8415446212034766
          ],
          [
            0.4851754761352166,
            0.1128910960166466
          ],
          [
            15.290311581828018,
            1.9896098747245676
          ],
          [
            -0.0806043817710809,
            0.02379759337247396
          ],
          [
            -0.5367056621060442,
            0.00824272631135767
          ],
          [
            -0.689188022218534,
            0.038469476523650126
          ],
          [
            -6.022484700220142,
            1.5563760639011321
          ],
          [
            -2.6437928145792333,
            0.25496412361777504
          ],
          [
            0.15407489664436896,
            -0.02739088192614885
          ],
          [
            1.5577429308874717,
            1.1103337338524988
          ],
          [
            0.04521693182403536,
            -0.010511277547258677
          ]
        ]
      ],
      "recorded_minus_local_clipped_particles_vjp": [
        [
          [
            2.486353604794194,
            5.879477812019541
          ],
          [
            -1.6729091869681012,
            0.3188991939973075
          ],
          [
            9.779499154388084,
            0.10233104040531872
          ],
          [
            -0.40140771599773245,
            0.3857577290305261
          ],
          [
            0.9624684860946057,
            0.2902162762212638
          ],
          [
            -2.59450475186808,
            0.7446733058224757
          ],
          [
            -0.5899757226071107,
            0.09780401112547332
          ],
          [
            -3.5405055641685643,
            3.816896830360644
          ],
          [
            1.9742903752610323,
            0.4350683496851184
          ],
          [
            0.03656465479486018,
            -0.019613025734172285
          ],
          [
            -1.423591235474117,
            0.08131075097075002
          ],
          [
            0.8534316894680518,
            0.06478578379109076
          ],
          [
            1.6110160874260118,
            1.0408990381772314
          ],
          [
            5.767833550868766,
            0.9250120416503627
          ],
          [
            -1.4509020592090653,
            0.10484102750919322
          ],
          [
            -0.733199289304897,
            0.01671126129528966
          ],
          [
            0.07113768682896549,
            0.33468222675755466
          ],
          [
            8.931971688923479,
            0.6678483757754503
          ],
          [
            -4.448150541154662,
            0.4051730969857756
          ],
          [
            0.04947472769035595,
            0.11208321499797358
          ],
          [
            -9.760544824868337,
            2.0189767449731737
          ],
          [
            -0.9602553669769559,
            0.7941189830506621
          ],
          [
            -0.7163673453059671,
            0.30176519450060135
          ],
          [
            0.21830046335857725,
            0.08856727536948156
          ],
          [
            1.9338456408977929,
            0.8639704933429756
          ],
          [
            -6.330640787912568,
            1.0677632453724732
          ],
          [
            -0.010955500649316038,
            0.0011708703193974435
          ],
          [
            1.6719018320383088,
            0.9679807498039347
          ],
          [
            -13.805574516918357,
            2.67859840747504
          ],
          [
            0.19228142890249433,
            -0.0004949158432168144
          ],
          [
            -0.15031915161293233,
            0.1245254881596062
          ],
          [
            0.608586399688508,
            0.012261356997107897
          ],
          [
            4.225939805685711,
            0.06048658123648687
          ],
          [
            -1.9634756004283513,
            0.3244353698044715
          ],
          [
            7.766302230716339,
            1.5195283867282823
          ],
          [
            0.6509644607963802,
            0.5386350059660049
          ],
          [
            0.5951104246658152,
            0.043177078964554735
          ],
          [
            0.4802802614932452,
            0.11867361177221386
          ],
          [
            1.910131671060952,
            0.26252855661119195
          ],
          [
            -0.9572424564793375,
            0.8415446212034766
          ],
          [
            0.4851754761352166,
            0.1128910960166466
          ],
          [
            15.290311581828018,
            1.9896098747245676
          ],
          [
            -0.0806043817710809,
            0.023797593372473946
          ],
          [
            -0.5367056621060443,
            0.008242726311357695
          ],
          [
            -0.689188022218534,
            0.038469476523650126
          ],
          [
            -6.022484700220143,
            1.5563760639011321
          ],
          [
            -2.6437928145792333,
            0.25496412361777504
          ],
          [
            0.15407489664436896,
            -0.027390881926148858
          ],
          [
            1.5577429308874717,
            1.1103337338524988
          ],
          [
            0.04521693182403536,
            -0.010511277547258668
          ]
        ]
      ],
      "recorded_transport_vjp_clipped_upstream": [
        [
          [
            2.550386531871265,
            6.120999706057644
          ],
          [
            -1.6733883946422021,
            0.5159066616973637
          ],
          [
            9.785841955881974,
            0.17183110114993097
          ],
          [
            -0.39577252915054517,
            0.48590818576157835
          ],
          [
            0.8406532084880048,
            -0.5863315591980249
          ],
          [
            -2.5907491462345957,
            0.8089044463212244
          ],
          [
            -0.690122149254531,
            -0.6104045839029608
          ],
          [
            -3.5860409874423333,
            3.565811940372886
          ],
          [
            1.9809466367532098,
            0.5299473482144635
          ],
          [
            -0.012332073100943534,
            -0.42959550385843565
          ],
          [
            -1.4971909159988248,
            -0.28487457296141405
          ],
          [
            0.8448614069111768,
            0.023807309132348693
          ],
          [
            1.6178951931926275,
            1.1321849851749384
          ],
          [
            5.773643565947585,
            0.9883714271213984
          ],
          [
            -1.526058415948783,
            -0.20822957970164935
          ],
          [
            -0.77576501275103,
            -0.3215515533271355
          ],
          [
            0.07657087760203388,
            0.4340269915143863
          ],
          [
            8.924759026407525,
            0.8469942106115868
          ],
          [
            -4.564374355276121,
            -0.4966145831810009
          ],
          [
            -0.02301579619735633,
            -0.3170625300927112
          ],
          [
            -9.757052417585621,
            2.076649233697359
          ],
          [
            -0.9520203830063221,
            0.9379799429217568
          ],
          [
            -0.8431158807640106,
            -0.67338778413682
          ],
          [
            0.21563333503878396,
            0.38995487670074225
          ],
          [
            1.7838789646738071,
            -0.09772127407602638
          ],
          [
            -6.326103161668204,
            1.1486040806036042
          ],
          [
            -0.07605751470914007,
            -0.5505461527371397
          ],
          [
            1.677317793573786,
            1.0353185042739637
          ],
          [
            -13.900451969747667,
            2.1566388459167376
          ],
          [
            0.11342852687160243,
            -0.6819468871299836
          ],
          [
            -0.15472722713922651,
            0.37147543917169323
          ],
          [
            0.5727523990866944,
            -0.18581076885775072
          ],
          [
            4.232091193580639,
            0.1629514634959821
          ],
          [
            -2.0900885536799643,
            -0.6332367810483832
          ],
          [
            7.771031775702046,
            1.5623316544229664
          ],
          [
            0.6572795420287403,
            0.6305245684068713
          ],
          [
            0.590656837254834,
            0.07027371501600069
          ],
          [
            0.4296543203232376,
            0.16152983920211822
          ],
          [
            1.8078918897316059,
            -0.36206644069529487
          ],
          [
            -0.9535806106441357,
            0.9026598825084414
          ],
          [
            0.48524463699235826,
            0.4013016639927284
          ],
          [
            15.358019754965156,
            2.324271038729268
          ],
          [
            -0.09502937910652964,
            0.29604051797851005
          ],
          [
            -0.5684693165959728,
            0.2768493742149973
          ],
          [
            -0.7457110396462862,
            -0.4681671726129814
          ],
          [
            -6.034399942438897,
            1.6575019034194753
          ],
          [
            -2.7386543902086813,
            -0.2573081684946337
          ],
          [
            0.12503706983322727,
            0.13848551750247445
          ],
          [
            1.5635850803032123,
            1.1841475771724241
          ],
          [
            0.0988463225790742,
            1.065161258352872
          ]
        ]
      ],
      "recorded_transport_vjp_raw_upstream": [
        [
          [
            2.550386531871265,
            6.120999706057644
          ],
          [
            -1.6733883946422021,
            0.5159066616973637
          ],
          [
            9.785841955881974,
            0.17183110114993097
          ],
          [
            -0.39577252915054517,
            0.48590818576157835
          ],
          [
            0.8406532084880048,
            -0.5863315591980249
          ],
          [
            -2.5907491462345957,
            0.8089044463212244
          ],
          [
            -0.690122149254531,
            -0.6104045839029608
          ],
          [
            -3.5860409874423333,
            3.565811940372886
          ],
          [
            1.9809466367532098,
            0.5299473482144635
          ],
          [
            -0.012332073100943534,
            -0.42959550385843565
          ],
          [
            -1.4971909159988248,
            -0.28487457296141405
          ],
          [
            0.8448614069111768,
            0.023807309132348693
          ],
          [
            1.6178951931926275,
            1.1321849851749384
          ],
          [
            5.773643565947585,
            0.9883714271213984
          ],
          [
            -1.526058415948783,
            -0.20822957970164935
          ],
          [
            -0.77576501275103,
            -0.3215515533271355
          ],
          [
            0.07657087760203388,
            0.4340269915143863
          ],
          [
            8.924759026407525,
            0.8469942106115868
          ],
          [
            -4.564374355276121,
            -0.4966145831810009
          ],
          [
            -0.02301579619735633,
            -0.3170625300927112
          ],
          [
            -9.757052417585621,
            2.076649233697359
          ],
          [
            -0.9520203830063221,
            0.9379799429217568
          ],
          [
            -0.8431158807640106,
            -0.67338778413682
          ],
          [
            0.21563333503878396,
            0.38995487670074225
          ],
          [
            1.7838789646738071,
            -0.09772127407602638
          ],
          [
            -6.326103161668204,
            1.1486040806036042
          ],
          [
            -0.07605751470914007,
            -0.5505461527371397
          ],
          [
            1.677317793573786,
            1.0353185042739637
          ],
          [
            -13.900451969747667,
            2.1566388459167376
          ],
          [
            0.11342852687160243,
            -0.6819468871299836
          ],
          [
            -0.15472722713922651,
            0.37147543917169323
          ],
          [
            0.5727523990866944,
            -0.18581076885775072
          ],
          [
            4.232091193580639,
            0.1629514634959821
          ],
          [
            -2.0900885536799643,
            -0.6332367810483832
          ],
          [
            7.771031775702046,
            1.5623316544229664
          ],
          [
            0.6572795420287403,
            0.6305245684068713
          ],
          [
            0.590656837254834,
            0.07027371501600069
          ],
          [
            0.4296543203232376,
            0.16152983920211822
          ],
          [
            1.8078918897316059,
            -0.36206644069529487
          ],
          [
            -0.9535806106441357,
            0.9026598825084414
          ],
          [
            0.48524463699235826,
            0.4013016639927284
          ],
          [
            15.358019754965156,
            2.324271038729268
          ],
          [
            -0.09502937910652964,
            0.29604051797851005
          ],
          [
            -0.5684693165959728,
            0.2768493742149973
          ],
          [
            -0.7457110396462862,
            -0.4681671726129814
          ],
          [
            -6.034399942438897,
            1.6575019034194753
          ],
          [
            -2.7386543902086813,
            -0.2573081684946337
          ],
          [
            0.12503706983322727,
            0.13848551750247445
          ],
          [
            1.5635850803032123,
            1.1841475771724241
          ],
          [
            0.0988463225790742,
            1.065161258352872
          ]
        ]
      ]
    }
  },
  "local_post_particle_adjoint_probe": {
    "fresh_proposal_loc_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_mean_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "increment_to_post_particles": {
      "finite": true,
      "max_abs": 0.030135380107735612,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.1083544289433924
    },
    "manual_proposal_mean_to_post_particles": {
      "finite": true,
      "max_abs": 0.2638596946097245,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.526207089861602
    },
    "observation_ll_to_post_particles": {
      "finite": true,
      "max_abs": 0.014874061645584816,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.08186897202373036
    },
    "proposal_ll_to_post_particles": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "proposal_loc_to_post_particles": {
      "finite": true,
      "max_abs": 0.2638596946097245,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.526207089861602
    },
    "proposal_mean_to_post_particles": {
      "finite": true,
      "max_abs": 0.2638596946097245,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.526207089861602
    },
    "proposed_particles_to_post_particles": {
      "finite": true,
      "max_abs": 0.2638596946097245,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.526207089861602
    },
    "transition_ll_to_post_particles": {
      "finite": true,
      "max_abs": 0.035592916948155556,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.0264854569196622
    },
    "unnormalized_to_post_particles": {
      "finite": true,
      "max_abs": 0.030135380107735612,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.1083544289433924
    }
  },
  "parameter_path_adjoint_probe": {
    "fresh_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_loc": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "fresh_proposal_mean": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "increment": {
      "finite": true,
      "max_abs": 11886.758024308658,
      "shape": [
        2
      ],
      "sum": 11313.776500239524
    },
    "log_ess": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "manual_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "manual_proposal_mean": {
      "finite": true,
      "max_abs": 16020.8501301383,
      "shape": [
        2
      ],
      "sum": 15337.646304417973
    },
    "normalized": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 9950.289261741085,
      "shape": [
        2
      ],
      "sum": 9505.07300672858
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "post_particles": {
      "finite": true,
      "max_abs": 11600.390548457051,
      "shape": [
        2
      ],
      "sum": 11027.409024387918
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 9110.446610302024,
      "shape": [
        2
      ],
      "sum": 9167.436483591746
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "pre_current_log_likelihoods": {
      "finite": true,
      "max_abs": 1001.4592302010708,
      "shape": [
        2
      ],
      "sum": -720.785891138725
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 10711.480505784251,
      "shape": [
        2
      ],
      "sum": -10305.321137242618
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 7155.78166007807,
      "shape": [
        2
      ],
      "sum": -7036.167252629115
    },
    "proposal_dist_log_prob": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        2
      ],
      "sum": 0.0
    },
    "proposal_loc": {
      "finite": true,
      "max_abs": 16020.8501301383,
      "shape": [
        2
      ],
      "sum": 15337.646304417973
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 16020.8501301383,
      "shape": [
        2
      ],
      "sum": 15337.646304417973
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 16020.8501301383,
      "shape": [
        2
      ],
      "sum": 15337.646304417973
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 12100.902535469098,
      "shape": [
        2
      ],
      "sum": 11516.177258700603
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 10068.711930779455,
      "shape": [
        2
      ],
      "sum": 9543.438592318034
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 11886.758024308658,
      "shape": [
        2
      ],
      "sum": 11313.776500239524
    }
  },
  "proposal_sample_gradient_contract": {
    "contract": "Probe BayesFilter proposal_dist.sample and a manual distribution built from the explicit proposal mean under the downstream upstream gradient for proposed_particles.",
    "value_probe": {
      "actual_sample_minus_manual_mean": {
        "finite": true,
        "max_abs": 1.2039904106672097,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -9.423168004290485
      },
      "manual_probe_minus_actual_sample": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "manual_probe_minus_manual_mean": {
        "finite": true,
        "max_abs": 1.2039904106672097,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -9.423168004290485
      }
    },
    "value_probe_tensors": {
      "actual_sample_minus_manual_mean": [
        [
          [
            -0.039827018934943226,
            -0.6889266147975874
          ],
          [
            -0.06983374152832766,
            -0.2591341393234572
          ],
          [
            0.05042471963292883,
            0.05231066918351246
          ],
          [
            0.01214327059506104,
            0.06059718961104821
          ],
          [
            -0.14769575675575197,
            -0.4276804744628464
          ],
          [
            0.04122359852351565,
            -0.8016100424202435
          ],
          [
            -0.01370822510580183,
            -0.8523795572448272
          ],
          [
            0.05015836559698528,
            0.09086937236442694
          ],
          [
            0.06651707654759775,
            0.5299856873737347
          ],
          [
            -0.01645973749498353,
            0.46287434621731194
          ],
          [
            -0.04363175183561907,
            -0.18170274210598336
          ],
          [
            0.05826177908261343,
            0.6414997770995257
          ],
          [
            0.050576680579752065,
            0.3904928673893977
          ],
          [
            -0.1284079200394217,
            -0.48240268152906296
          ],
          [
            -0.053760975379418596,
            1.1064198446869042
          ],
          [
            0.020474395648079735,
            -0.5633088776998392
          ],
          [
            -0.031653208878424266,
            0.3706781623579758
          ],
          [
            -0.11449504035329028,
            0.4831817955529587
          ],
          [
            -0.11084134702014126,
            -0.35848947164071276
          ],
          [
            0.08736451454558392,
            -0.8168944616344689
          ],
          [
            -0.00831180068314552,
            0.1754260755476018
          ],
          [
            0.09424544953969871,
            0.21361575062433502
          ],
          [
            -0.14293083820700758,
            -0.31616833529056265
          ],
          [
            -0.04318508117341935,
            -0.18539893962458365
          ],
          [
            0.026184031571119704,
            -0.5857779984711087
          ],
          [
            0.023618031386945404,
            -0.05594826453745938
          ],
          [
            0.08554084772390524,
            -1.1065265609274633
          ],
          [
            -0.1469698082682953,
            -0.6489911124229621
          ],
          [
            -0.11292990663309865,
            0.24727310506675693
          ],
          [
            0.03360733603085464,
            -0.32311628095884615
          ],
          [
            0.03193565110984764,
            -0.10873633290318452
          ],
          [
            -0.0003642933924083991,
            -0.06215786530638212
          ],
          [
            -0.02874157914141051,
            -0.45155889939025684
          ],
          [
            0.0769362392632047,
            0.47988897302154854
          ],
          [
            -0.01620777658604311,
            0.13629828143561085
          ],
          [
            0.08822507610682351,
            0.001987009968772213
          ],
          [
            -0.07691024178586758,
            -0.3273194302204949
          ],
          [
            -0.07317142783801955,
            -1.0165646089651261
          ],
          [
            0.06452044561910952,
            0.04746974275883176
          ],
          [
            -0.14134521052642413,
            -0.41673051487595103
          ],
          [
            -0.07851934302505015,
            -0.28051638601720086
          ],
          [
            -0.053582346723601404,
            -0.9658630581454339
          ],
          [
            -0.09352685170881614,
            -0.25390252180896766
          ],
          [
            0.1754513954867889,
            -1.2039904106672097
          ],
          [
            0.04980658164470242,
            -0.1484498501318967
          ],
          [
            -0.11825992662068074,
            -1.0138302765985436
          ],
          [
            0.009038690649504133,
            -0.4572484595980022
          ],
          [
            0.10417334522253441,
            0.37495251853305334
          ],
          [
            0.04865849560906099,
            0.7110651821647096
          ],
          [
            0.058125280531385215,
            -0.14066932813602762
          ]
        ]
      ],
      "manual_probe_minus_actual_sample": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "manual_probe_minus_manual_mean": [
        [
          [
            -0.039827018934943226,
            -0.6889266147975874
          ],
          [
            -0.06983374152832766,
            -0.2591341393234572
          ],
          [
            0.05042471963292883,
            0.05231066918351246
          ],
          [
            0.01214327059506104,
            0.06059718961104821
          ],
          [
            -0.14769575675575197,
            -0.4276804744628464
          ],
          [
            0.04122359852351565,
            -0.8016100424202435
          ],
          [
            -0.01370822510580183,
            -0.8523795572448272
          ],
          [
            0.05015836559698528,
            0.09086937236442694
          ],
          [
            0.06651707654759775,
            0.5299856873737347
          ],
          [
            -0.01645973749498353,
            0.46287434621731194
          ],
          [
            -0.04363175183561907,
            -0.18170274210598336
          ],
          [
            0.05826177908261343,
            0.6414997770995257
          ],
          [
            0.050576680579752065,
            0.3904928673893977
          ],
          [
            -0.1284079200394217,
            -0.48240268152906296
          ],
          [
            -0.053760975379418596,
            1.1064198446869042
          ],
          [
            0.020474395648079735,
            -0.5633088776998392
          ],
          [
            -0.031653208878424266,
            0.3706781623579758
          ],
          [
            -0.11449504035329028,
            0.4831817955529587
          ],
          [
            -0.11084134702014126,
            -0.35848947164071276
          ],
          [
            0.08736451454558392,
            -0.8168944616344689
          ],
          [
            -0.00831180068314552,
            0.1754260755476018
          ],
          [
            0.09424544953969871,
            0.21361575062433502
          ],
          [
            -0.14293083820700758,
            -0.31616833529056265
          ],
          [
            -0.04318508117341935,
            -0.18539893962458365
          ],
          [
            0.026184031571119704,
            -0.5857779984711087
          ],
          [
            0.023618031386945404,
            -0.05594826453745938
          ],
          [
            0.08554084772390524,
            -1.1065265609274633
          ],
          [
            -0.1469698082682953,
            -0.6489911124229621
          ],
          [
            -0.11292990663309865,
            0.24727310506675693
          ],
          [
            0.03360733603085464,
            -0.32311628095884615
          ],
          [
            0.03193565110984764,
            -0.10873633290318452
          ],
          [
            -0.0003642933924083991,
            -0.06215786530638212
          ],
          [
            -0.02874157914141051,
            -0.45155889939025684
          ],
          [
            0.0769362392632047,
            0.47988897302154854
          ],
          [
            -0.01620777658604311,
            0.13629828143561085
          ],
          [
            0.08822507610682351,
            0.001987009968772213
          ],
          [
            -0.07691024178586758,
            -0.3273194302204949
          ],
          [
            -0.07317142783801955,
            -1.0165646089651261
          ],
          [
            0.06452044561910952,
            0.04746974275883176
          ],
          [
            -0.14134521052642413,
            -0.41673051487595103
          ],
          [
            -0.07851934302505015,
            -0.28051638601720086
          ],
          [
            -0.053582346723601404,
            -0.9658630581454339
          ],
          [
            -0.09352685170881614,
            -0.25390252180896766
          ],
          [
            0.1754513954867889,
            -1.2039904106672097
          ],
          [
            0.04980658164470242,
            -0.1484498501318967
          ],
          [
            -0.11825992662068074,
            -1.0138302765985436
          ],
          [
            0.009038690649504133,
            -0.4572484595980022
          ],
          [
            0.10417334522253441,
            0.37495251853305334
          ],
          [
            0.04865849560906099,
            0.7110651821647096
          ],
          [
            0.058125280531385215,
            -0.14066932813602762
          ]
        ]
      ]
    },
    "vjp_probe": {
      "actual_sample_to_fresh_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "actual_sample_to_fresh_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "actual_sample_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 0.7827423714161357,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.4898093699805401
      },
      "actual_sample_to_post_particles": {
        "finite": true,
        "max_abs": 0.2638596946097245,
        "shape": [
          1,
          50,
          2
        ],
        "sum": -1.526207089861602
      },
      "actual_sample_to_proposal_loc": {
        "finite": true,
        "max_abs": 0.7827423714161357,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.4898093699805401
      },
      "actual_sample_to_proposal_mean": {
        "finite": true,
        "max_abs": 0.7827423714161357,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.4898093699805401
      },
      "manual_probe_sample_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 0.7827423714161357,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.4898093699805401
      },
      "manual_probe_sum_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      }
    },
    "vjp_tensors": {
      "actual_sample_to_fresh_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "actual_sample_to_fresh_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "actual_sample_to_manual_proposal_mean": [
        [
          [
            0.0026468908081875827,
            0.020367567026992977
          ],
          [
            0.1252948141207208,
            0.012347068531093767
          ],
          [
            -0.060705970304802806,
            0.001061965353856471
          ],
          [
            -0.012268562488561006,
            -0.0020872610745535374
          ],
          [
            0.4070659071088484,
            0.024016092921263627
          ],
          [
            -0.11543792594500943,
            0.04229446826813596
          ],
          [
            -0.10366957885918988,
            0.09637909789459483
          ],
          [
            -0.08328253073918244,
            -0.0010265963878369198
          ],
          [
            -0.04335102961008747,
            -0.017470778798833256
          ],
          [
            0.11752496910002225,
            -0.049603292683141106
          ],
          [
            0.10940488403467612,
            0.013400494272966348
          ],
          [
            -0.049775107617577294,
            -0.04122187903987288
          ],
          [
            -0.03048617999021792,
            -0.011550712405397056
          ],
          [
            0.10573297539848053,
            0.010669355254843705
          ],
          [
            0.36826370199866487,
            -0.13812331208100254
          ],
          [
            -0.14133176928711205,
            0.05919561262244074
          ],
          [
            0.07339324203522132,
            -0.021278387719953874
          ],
          [
            0.3088836677827404,
            -0.05146636555966472
          ],
          [
            0.297798387477351,
            0.022310585574755622
          ],
          [
            -0.4189551762935966,
            0.10816823742742539
          ],
          [
            0.017488689304194605,
            -0.006626775120499224
          ],
          [
            -0.10720910058461362,
            -0.0033408532194766443
          ],
          [
            0.4108278158768298,
            0.011851768960003091
          ],
          [
            0.08435809131673994,
            0.010928536673115124
          ],
          [
            -0.17934160354257567,
            0.06954759409070864
          ],
          [
            -0.028980801662859212,
            0.003553452576747258
          ],
          [
            -0.4349470408888506,
            0.1324532328195342
          ],
          [
            0.1173418962167676,
            0.01600591608356549
          ],
          [
            0.30985197978488327,
            -0.036543257594823776
          ],
          [
            -0.15718790728395637,
            0.041183140138142754
          ],
          [
            -0.09512258608691895,
            0.014092448020264057
          ],
          [
            -0.008294149301780181,
            0.006154087044209059
          ],
          [
            0.006619344918176583,
            0.021217422596160856
          ],
          [
            -0.1670908115126207,
            -0.042458746856806104
          ],
          [
            0.017446447836165332,
            -0.004256754257515961
          ],
          [
            -0.09541696553949604,
            0.0050409557584019824
          ],
          [
            0.12003397565624635,
            0.015303201625031562
          ],
          [
            0.0588487206063614,
            0.10184969368888955
          ],
          [
            -0.20214259841938173,
            0.005743934099964266
          ],
          [
            0.17161050410933973,
            0.010541668501258008
          ],
          [
            0.15177745978636792,
            0.01389375801144244
          ],
          [
            0.001971486043932359,
            0.03389035670208604
          ],
          [
            0.23362117572731222,
            0.01186033738140255
          ],
          [
            -0.7827423714161357,
            0.17092994836254657
          ],
          [
            -0.16716207648041886,
            0.02306608972569028
          ],
          [
            0.14465669708835777,
            0.06757581981154692
          ],
          [
            -0.1093573200051336,
            0.05483338418879946
          ],
          [
            -0.2637450245596155,
            -0.024498152075867037
          ],
          [
            -0.011859763374011198,
            -0.025579518599865837
          ],
          [
            -0.20247948749582162,
            0.025094436600709206
          ]
        ]
      ],
      "actual_sample_to_post_particles": [
        [
          [
            -0.02872802061367905,
            -0.00953843760867253
          ],
          [
            -0.013916936228012315,
            -0.002179689428204623
          ],
          [
            -0.003218735091041706,
            -0.002269489063771974
          ],
          [
            0.002604716448689353,
            0.0006280595017537239
          ],
          [
            -0.02244938129847845,
            0.0005182874068721914
          ],
          [
            -0.06307584575019037,
            -0.023329494640672653
          ],
          [
            -0.13922701308796498,
            -0.048520089187424675
          ],
          [
            -0.0009037212943664152,
            -0.0019410484667403524
          ],
          [
            0.02348027636017001,
            0.006985306001260641
          ],
          [
            0.07347067937673954,
            0.026840779432118232
          ],
          [
            -0.01585605905422333,
            -0.0031398253800802647
          ],
          [
            0.05688630456628275,
            0.01801109499782151
          ],
          [
            0.015472246560796014,
            0.004565146107258011
          ],
          [
            -0.012097659928193186,
            -0.0019574030261812585
          ],
          [
            0.20574331225845718,
            0.07593416404985295
          ],
          [
            -0.08770902982250713,
            -0.03206271709312132
          ],
          [
            0.03216671127318439,
            0.012183197348223311
          ],
          [
            0.08151756652945674,
            0.033293890753291006
          ],
          [
            -0.02312795341403414,
            -0.0018590914288746652
          ],
          [
            -0.16481592544110904,
            -0.06326881942152958
          ],
          [
            0.00986591675982053,
            0.0036378808503670567
          ],
          [
            0.0016922777555152,
            -0.0015453778456047565
          ],
          [
            -0.005140751654586621,
            0.006370636772014533
          ],
          [
            -0.013068730142291545,
            -0.0027023320527526287
          ],
          [
            -0.10342336453863964,
            -0.03805697168233653
          ],
          [
            -0.0058447968207395486,
            -0.0025216865255185327
          ],
          [
            -0.19961095582077612,
            -0.0751995519328729
          ],
          [
            -0.019316044356499446,
            -0.0041386703041647495
          ],
          [
            0.06044137581745943,
            0.02627689245763723
          ],
          [
            -0.06268507460422948,
            -0.02402085533409077
          ],
          [
            -0.02261925653346538,
            -0.009423607630493793
          ],
          [
            -0.008937412906848293,
            -0.0031469226010966914
          ],
          [
            -0.029817494273711866,
            -0.009823952006263143
          ],
          [
            0.0553173763459312,
            0.015178058234432197
          ],
          [
            0.00651314680398936,
            0.002517763303618
          ],
          [
            -0.009827375627996217,
            -0.00515897090492533
          ],
          [
            -0.01824615735549393,
            -0.003728508619806146
          ],
          [
            -0.1423667606532651,
            -0.04636921559765077
          ],
          [
            -0.013840025776271789,
            -0.00859936066676635
          ],
          [
            -0.010053871320786707,
            2.1640881921353508e-05
          ],
          [
            -0.015355182880680378,
            -0.0021385425748332715
          ],
          [
            -0.04787043455313821,
            -0.015942220670696568
          ],
          [
            -0.010164819431029556,
            0.0012052331680015155
          ],
          [
            -0.2638596946097245,
            -0.10349437632236927
          ],
          [
            -0.037346869825773656,
            -0.015758302839524344
          ],
          [
            -0.09147129951181172,
            -0.02768925303518234
          ],
          [
            -0.0806358295374485,
            -0.029072013741606798
          ],
          [
            0.027184644231265872,
            0.0038836874312700442
          ],
          [
            0.035837955964423705,
            0.011730664651046205
          ],
          [
            -0.04121415070278818,
            -0.017744548166917264
          ]
        ]
      ],
      "actual_sample_to_proposal_loc": [
        [
          [
            0.0026468908081875827,
            0.020367567026992977
          ],
          [
            0.1252948141207208,
            0.012347068531093767
          ],
          [
            -0.060705970304802806,
            0.001061965353856471
          ],
          [
            -0.012268562488561006,
            -0.0020872610745535374
          ],
          [
            0.4070659071088484,
            0.024016092921263627
          ],
          [
            -0.11543792594500943,
            0.04229446826813596
          ],
          [
            -0.10366957885918988,
            0.09637909789459483
          ],
          [
            -0.08328253073918244,
            -0.0010265963878369198
          ],
          [
            -0.04335102961008747,
            -0.017470778798833256
          ],
          [
            0.11752496910002225,
            -0.049603292683141106
          ],
          [
            0.10940488403467612,
            0.013400494272966348
          ],
          [
            -0.049775107617577294,
            -0.04122187903987288
          ],
          [
            -0.03048617999021792,
            -0.011550712405397056
          ],
          [
            0.10573297539848053,
            0.010669355254843705
          ],
          [
            0.36826370199866487,
            -0.13812331208100254
          ],
          [
            -0.14133176928711205,
            0.05919561262244074
          ],
          [
            0.07339324203522132,
            -0.021278387719953874
          ],
          [
            0.3088836677827404,
            -0.05146636555966472
          ],
          [
            0.297798387477351,
            0.022310585574755622
          ],
          [
            -0.4189551762935966,
            0.10816823742742539
          ],
          [
            0.017488689304194605,
            -0.006626775120499224
          ],
          [
            -0.10720910058461362,
            -0.0033408532194766443
          ],
          [
            0.4108278158768298,
            0.011851768960003091
          ],
          [
            0.08435809131673994,
            0.010928536673115124
          ],
          [
            -0.17934160354257567,
            0.06954759409070864
          ],
          [
            -0.028980801662859212,
            0.003553452576747258
          ],
          [
            -0.4349470408888506,
            0.1324532328195342
          ],
          [
            0.1173418962167676,
            0.01600591608356549
          ],
          [
            0.30985197978488327,
            -0.036543257594823776
          ],
          [
            -0.15718790728395637,
            0.041183140138142754
          ],
          [
            -0.09512258608691895,
            0.014092448020264057
          ],
          [
            -0.008294149301780181,
            0.006154087044209059
          ],
          [
            0.006619344918176583,
            0.021217422596160856
          ],
          [
            -0.1670908115126207,
            -0.042458746856806104
          ],
          [
            0.017446447836165332,
            -0.004256754257515961
          ],
          [
            -0.09541696553949604,
            0.0050409557584019824
          ],
          [
            0.12003397565624635,
            0.015303201625031562
          ],
          [
            0.0588487206063614,
            0.10184969368888955
          ],
          [
            -0.20214259841938173,
            0.005743934099964266
          ],
          [
            0.17161050410933973,
            0.010541668501258008
          ],
          [
            0.15177745978636792,
            0.01389375801144244
          ],
          [
            0.001971486043932359,
            0.03389035670208604
          ],
          [
            0.23362117572731222,
            0.01186033738140255
          ],
          [
            -0.7827423714161357,
            0.17092994836254657
          ],
          [
            -0.16716207648041886,
            0.02306608972569028
          ],
          [
            0.14465669708835777,
            0.06757581981154692
          ],
          [
            -0.1093573200051336,
            0.05483338418879946
          ],
          [
            -0.2637450245596155,
            -0.024498152075867037
          ],
          [
            -0.011859763374011198,
            -0.025579518599865837
          ],
          [
            -0.20247948749582162,
            0.025094436600709206
          ]
        ]
      ],
      "actual_sample_to_proposal_mean": [
        [
          [
            0.0026468908081875827,
            0.020367567026992977
          ],
          [
            0.1252948141207208,
            0.012347068531093767
          ],
          [
            -0.060705970304802806,
            0.001061965353856471
          ],
          [
            -0.012268562488561006,
            -0.0020872610745535374
          ],
          [
            0.4070659071088484,
            0.024016092921263627
          ],
          [
            -0.11543792594500943,
            0.04229446826813596
          ],
          [
            -0.10366957885918988,
            0.09637909789459483
          ],
          [
            -0.08328253073918244,
            -0.0010265963878369198
          ],
          [
            -0.04335102961008747,
            -0.017470778798833256
          ],
          [
            0.11752496910002225,
            -0.049603292683141106
          ],
          [
            0.10940488403467612,
            0.013400494272966348
          ],
          [
            -0.049775107617577294,
            -0.04122187903987288
          ],
          [
            -0.03048617999021792,
            -0.011550712405397056
          ],
          [
            0.10573297539848053,
            0.010669355254843705
          ],
          [
            0.36826370199866487,
            -0.13812331208100254
          ],
          [
            -0.14133176928711205,
            0.05919561262244074
          ],
          [
            0.07339324203522132,
            -0.021278387719953874
          ],
          [
            0.3088836677827404,
            -0.05146636555966472
          ],
          [
            0.297798387477351,
            0.022310585574755622
          ],
          [
            -0.4189551762935966,
            0.10816823742742539
          ],
          [
            0.017488689304194605,
            -0.006626775120499224
          ],
          [
            -0.10720910058461362,
            -0.0033408532194766443
          ],
          [
            0.4108278158768298,
            0.011851768960003091
          ],
          [
            0.08435809131673994,
            0.010928536673115124
          ],
          [
            -0.17934160354257567,
            0.06954759409070864
          ],
          [
            -0.028980801662859212,
            0.003553452576747258
          ],
          [
            -0.4349470408888506,
            0.1324532328195342
          ],
          [
            0.1173418962167676,
            0.01600591608356549
          ],
          [
            0.30985197978488327,
            -0.036543257594823776
          ],
          [
            -0.15718790728395637,
            0.041183140138142754
          ],
          [
            -0.09512258608691895,
            0.014092448020264057
          ],
          [
            -0.008294149301780181,
            0.006154087044209059
          ],
          [
            0.006619344918176583,
            0.021217422596160856
          ],
          [
            -0.1670908115126207,
            -0.042458746856806104
          ],
          [
            0.017446447836165332,
            -0.004256754257515961
          ],
          [
            -0.09541696553949604,
            0.0050409557584019824
          ],
          [
            0.12003397565624635,
            0.015303201625031562
          ],
          [
            0.0588487206063614,
            0.10184969368888955
          ],
          [
            -0.20214259841938173,
            0.005743934099964266
          ],
          [
            0.17161050410933973,
            0.010541668501258008
          ],
          [
            0.15177745978636792,
            0.01389375801144244
          ],
          [
            0.001971486043932359,
            0.03389035670208604
          ],
          [
            0.23362117572731222,
            0.01186033738140255
          ],
          [
            -0.7827423714161357,
            0.17092994836254657
          ],
          [
            -0.16716207648041886,
            0.02306608972569028
          ],
          [
            0.14465669708835777,
            0.06757581981154692
          ],
          [
            -0.1093573200051336,
            0.05483338418879946
          ],
          [
            -0.2637450245596155,
            -0.024498152075867037
          ],
          [
            -0.011859763374011198,
            -0.025579518599865837
          ],
          [
            -0.20247948749582162,
            0.025094436600709206
          ]
        ]
      ],
      "manual_probe_sample_to_manual_proposal_mean": [
        [
          [
            0.0026468908081875827,
            0.020367567026992977
          ],
          [
            0.1252948141207208,
            0.012347068531093767
          ],
          [
            -0.060705970304802806,
            0.001061965353856471
          ],
          [
            -0.012268562488561006,
            -0.0020872610745535374
          ],
          [
            0.4070659071088484,
            0.024016092921263627
          ],
          [
            -0.11543792594500943,
            0.04229446826813596
          ],
          [
            -0.10366957885918988,
            0.09637909789459483
          ],
          [
            -0.08328253073918244,
            -0.0010265963878369198
          ],
          [
            -0.04335102961008747,
            -0.017470778798833256
          ],
          [
            0.11752496910002225,
            -0.049603292683141106
          ],
          [
            0.10940488403467612,
            0.013400494272966348
          ],
          [
            -0.049775107617577294,
            -0.04122187903987288
          ],
          [
            -0.03048617999021792,
            -0.011550712405397056
          ],
          [
            0.10573297539848053,
            0.010669355254843705
          ],
          [
            0.36826370199866487,
            -0.13812331208100254
          ],
          [
            -0.14133176928711205,
            0.05919561262244074
          ],
          [
            0.07339324203522132,
            -0.021278387719953874
          ],
          [
            0.3088836677827404,
            -0.05146636555966472
          ],
          [
            0.297798387477351,
            0.022310585574755622
          ],
          [
            -0.4189551762935966,
            0.10816823742742539
          ],
          [
            0.017488689304194605,
            -0.006626775120499224
          ],
          [
            -0.10720910058461362,
            -0.0033408532194766443
          ],
          [
            0.4108278158768298,
            0.011851768960003091
          ],
          [
            0.08435809131673994,
            0.010928536673115124
          ],
          [
            -0.17934160354257567,
            0.06954759409070864
          ],
          [
            -0.028980801662859212,
            0.003553452576747258
          ],
          [
            -0.4349470408888506,
            0.1324532328195342
          ],
          [
            0.1173418962167676,
            0.01600591608356549
          ],
          [
            0.30985197978488327,
            -0.036543257594823776
          ],
          [
            -0.15718790728395637,
            0.041183140138142754
          ],
          [
            -0.09512258608691895,
            0.014092448020264057
          ],
          [
            -0.008294149301780181,
            0.006154087044209059
          ],
          [
            0.006619344918176583,
            0.021217422596160856
          ],
          [
            -0.1670908115126207,
            -0.042458746856806104
          ],
          [
            0.017446447836165332,
            -0.004256754257515961
          ],
          [
            -0.09541696553949604,
            0.0050409557584019824
          ],
          [
            0.12003397565624635,
            0.015303201625031562
          ],
          [
            0.0588487206063614,
            0.10184969368888955
          ],
          [
            -0.20214259841938173,
            0.005743934099964266
          ],
          [
            0.17161050410933973,
            0.010541668501258008
          ],
          [
            0.15177745978636792,
            0.01389375801144244
          ],
          [
            0.001971486043932359,
            0.03389035670208604
          ],
          [
            0.23362117572731222,
            0.01186033738140255
          ],
          [
            -0.7827423714161357,
            0.17092994836254657
          ],
          [
            -0.16716207648041886,
            0.02306608972569028
          ],
          [
            0.14465669708835777,
            0.06757581981154692
          ],
          [
            -0.1093573200051336,
            0.05483338418879946
          ],
          [
            -0.2637450245596155,
            -0.024498152075867037
          ],
          [
            -0.011859763374011198,
            -0.025579518599865837
          ],
          [
            -0.20247948749582162,
            0.025094436600709206
          ]
        ]
      ],
      "manual_probe_sum_to_manual_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ]
    }
  },
  "proposal_topology_probe": {
    "contract": "Difference-audit probe for the optimal-proposal graph topology. BayesFilter constructs the proposal distribution in the replay loop and exposes explicit loc/mean/log-prob paths for comparison against executable FilterFlow.",
    "gradient_summaries": {
      "target_to_fresh_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "target_to_fresh_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "target_to_manual_proposal_mean": {
        "finite": true,
        "max_abs": 0.7827423714161357,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.4898093699805401
      },
      "target_to_proposal_loc": {
        "finite": true,
        "max_abs": 0.7827423714161357,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.4898093699805401
      },
      "target_to_proposal_mean": {
        "finite": true,
        "max_abs": 0.7827423714161357,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.4898093699805401
      }
    },
    "gradient_tensors": {
      "target_to_fresh_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "target_to_fresh_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "target_to_manual_proposal_mean": [
        [
          [
            0.0026468908081875827,
            0.020367567026992977
          ],
          [
            0.1252948141207208,
            0.012347068531093767
          ],
          [
            -0.060705970304802806,
            0.001061965353856471
          ],
          [
            -0.012268562488561006,
            -0.0020872610745535374
          ],
          [
            0.4070659071088484,
            0.024016092921263627
          ],
          [
            -0.11543792594500943,
            0.04229446826813596
          ],
          [
            -0.10366957885918988,
            0.09637909789459483
          ],
          [
            -0.08328253073918244,
            -0.0010265963878369198
          ],
          [
            -0.04335102961008747,
            -0.017470778798833256
          ],
          [
            0.11752496910002225,
            -0.049603292683141106
          ],
          [
            0.10940488403467612,
            0.013400494272966348
          ],
          [
            -0.049775107617577294,
            -0.04122187903987288
          ],
          [
            -0.03048617999021792,
            -0.011550712405397056
          ],
          [
            0.10573297539848053,
            0.010669355254843705
          ],
          [
            0.36826370199866487,
            -0.13812331208100254
          ],
          [
            -0.14133176928711205,
            0.05919561262244074
          ],
          [
            0.07339324203522132,
            -0.021278387719953874
          ],
          [
            0.3088836677827404,
            -0.05146636555966472
          ],
          [
            0.297798387477351,
            0.022310585574755622
          ],
          [
            -0.4189551762935966,
            0.10816823742742539
          ],
          [
            0.017488689304194605,
            -0.006626775120499224
          ],
          [
            -0.10720910058461362,
            -0.0033408532194766443
          ],
          [
            0.4108278158768298,
            0.011851768960003091
          ],
          [
            0.08435809131673994,
            0.010928536673115124
          ],
          [
            -0.17934160354257567,
            0.06954759409070864
          ],
          [
            -0.028980801662859212,
            0.003553452576747258
          ],
          [
            -0.4349470408888506,
            0.1324532328195342
          ],
          [
            0.1173418962167676,
            0.01600591608356549
          ],
          [
            0.30985197978488327,
            -0.036543257594823776
          ],
          [
            -0.15718790728395637,
            0.041183140138142754
          ],
          [
            -0.09512258608691895,
            0.014092448020264057
          ],
          [
            -0.008294149301780181,
            0.006154087044209059
          ],
          [
            0.006619344918176583,
            0.021217422596160856
          ],
          [
            -0.1670908115126207,
            -0.042458746856806104
          ],
          [
            0.017446447836165332,
            -0.004256754257515961
          ],
          [
            -0.09541696553949604,
            0.0050409557584019824
          ],
          [
            0.12003397565624635,
            0.015303201625031562
          ],
          [
            0.0588487206063614,
            0.10184969368888955
          ],
          [
            -0.20214259841938173,
            0.005743934099964266
          ],
          [
            0.17161050410933973,
            0.010541668501258008
          ],
          [
            0.15177745978636792,
            0.01389375801144244
          ],
          [
            0.001971486043932359,
            0.03389035670208604
          ],
          [
            0.23362117572731222,
            0.01186033738140255
          ],
          [
            -0.7827423714161357,
            0.17092994836254657
          ],
          [
            -0.16716207648041886,
            0.02306608972569028
          ],
          [
            0.14465669708835777,
            0.06757581981154692
          ],
          [
            -0.1093573200051336,
            0.05483338418879946
          ],
          [
            -0.2637450245596155,
            -0.024498152075867037
          ],
          [
            -0.011859763374011198,
            -0.025579518599865837
          ],
          [
            -0.20247948749582162,
            0.025094436600709206
          ]
        ]
      ],
      "target_to_proposal_loc": [
        [
          [
            0.0026468908081875827,
            0.020367567026992977
          ],
          [
            0.1252948141207208,
            0.012347068531093767
          ],
          [
            -0.060705970304802806,
            0.001061965353856471
          ],
          [
            -0.012268562488561006,
            -0.0020872610745535374
          ],
          [
            0.4070659071088484,
            0.024016092921263627
          ],
          [
            -0.11543792594500943,
            0.04229446826813596
          ],
          [
            -0.10366957885918988,
            0.09637909789459483
          ],
          [
            -0.08328253073918244,
            -0.0010265963878369198
          ],
          [
            -0.04335102961008747,
            -0.017470778798833256
          ],
          [
            0.11752496910002225,
            -0.049603292683141106
          ],
          [
            0.10940488403467612,
            0.013400494272966348
          ],
          [
            -0.049775107617577294,
            -0.04122187903987288
          ],
          [
            -0.03048617999021792,
            -0.011550712405397056
          ],
          [
            0.10573297539848053,
            0.010669355254843705
          ],
          [
            0.36826370199866487,
            -0.13812331208100254
          ],
          [
            -0.14133176928711205,
            0.05919561262244074
          ],
          [
            0.07339324203522132,
            -0.021278387719953874
          ],
          [
            0.3088836677827404,
            -0.05146636555966472
          ],
          [
            0.297798387477351,
            0.022310585574755622
          ],
          [
            -0.4189551762935966,
            0.10816823742742539
          ],
          [
            0.017488689304194605,
            -0.006626775120499224
          ],
          [
            -0.10720910058461362,
            -0.0033408532194766443
          ],
          [
            0.4108278158768298,
            0.011851768960003091
          ],
          [
            0.08435809131673994,
            0.010928536673115124
          ],
          [
            -0.17934160354257567,
            0.06954759409070864
          ],
          [
            -0.028980801662859212,
            0.003553452576747258
          ],
          [
            -0.4349470408888506,
            0.1324532328195342
          ],
          [
            0.1173418962167676,
            0.01600591608356549
          ],
          [
            0.30985197978488327,
            -0.036543257594823776
          ],
          [
            -0.15718790728395637,
            0.041183140138142754
          ],
          [
            -0.09512258608691895,
            0.014092448020264057
          ],
          [
            -0.008294149301780181,
            0.006154087044209059
          ],
          [
            0.006619344918176583,
            0.021217422596160856
          ],
          [
            -0.1670908115126207,
            -0.042458746856806104
          ],
          [
            0.017446447836165332,
            -0.004256754257515961
          ],
          [
            -0.09541696553949604,
            0.0050409557584019824
          ],
          [
            0.12003397565624635,
            0.015303201625031562
          ],
          [
            0.0588487206063614,
            0.10184969368888955
          ],
          [
            -0.20214259841938173,
            0.005743934099964266
          ],
          [
            0.17161050410933973,
            0.010541668501258008
          ],
          [
            0.15177745978636792,
            0.01389375801144244
          ],
          [
            0.001971486043932359,
            0.03389035670208604
          ],
          [
            0.23362117572731222,
            0.01186033738140255
          ],
          [
            -0.7827423714161357,
            0.17092994836254657
          ],
          [
            -0.16716207648041886,
            0.02306608972569028
          ],
          [
            0.14465669708835777,
            0.06757581981154692
          ],
          [
            -0.1093573200051336,
            0.05483338418879946
          ],
          [
            -0.2637450245596155,
            -0.024498152075867037
          ],
          [
            -0.011859763374011198,
            -0.025579518599865837
          ],
          [
            -0.20247948749582162,
            0.025094436600709206
          ]
        ]
      ],
      "target_to_proposal_mean": [
        [
          [
            0.0026468908081875827,
            0.020367567026992977
          ],
          [
            0.1252948141207208,
            0.012347068531093767
          ],
          [
            -0.060705970304802806,
            0.001061965353856471
          ],
          [
            -0.012268562488561006,
            -0.0020872610745535374
          ],
          [
            0.4070659071088484,
            0.024016092921263627
          ],
          [
            -0.11543792594500943,
            0.04229446826813596
          ],
          [
            -0.10366957885918988,
            0.09637909789459483
          ],
          [
            -0.08328253073918244,
            -0.0010265963878369198
          ],
          [
            -0.04335102961008747,
            -0.017470778798833256
          ],
          [
            0.11752496910002225,
            -0.049603292683141106
          ],
          [
            0.10940488403467612,
            0.013400494272966348
          ],
          [
            -0.049775107617577294,
            -0.04122187903987288
          ],
          [
            -0.03048617999021792,
            -0.011550712405397056
          ],
          [
            0.10573297539848053,
            0.010669355254843705
          ],
          [
            0.36826370199866487,
            -0.13812331208100254
          ],
          [
            -0.14133176928711205,
            0.05919561262244074
          ],
          [
            0.07339324203522132,
            -0.021278387719953874
          ],
          [
            0.3088836677827404,
            -0.05146636555966472
          ],
          [
            0.297798387477351,
            0.022310585574755622
          ],
          [
            -0.4189551762935966,
            0.10816823742742539
          ],
          [
            0.017488689304194605,
            -0.006626775120499224
          ],
          [
            -0.10720910058461362,
            -0.0033408532194766443
          ],
          [
            0.4108278158768298,
            0.011851768960003091
          ],
          [
            0.08435809131673994,
            0.010928536673115124
          ],
          [
            -0.17934160354257567,
            0.06954759409070864
          ],
          [
            -0.028980801662859212,
            0.003553452576747258
          ],
          [
            -0.4349470408888506,
            0.1324532328195342
          ],
          [
            0.1173418962167676,
            0.01600591608356549
          ],
          [
            0.30985197978488327,
            -0.036543257594823776
          ],
          [
            -0.15718790728395637,
            0.041183140138142754
          ],
          [
            -0.09512258608691895,
            0.014092448020264057
          ],
          [
            -0.008294149301780181,
            0.006154087044209059
          ],
          [
            0.006619344918176583,
            0.021217422596160856
          ],
          [
            -0.1670908115126207,
            -0.042458746856806104
          ],
          [
            0.017446447836165332,
            -0.004256754257515961
          ],
          [
            -0.09541696553949604,
            0.0050409557584019824
          ],
          [
            0.12003397565624635,
            0.015303201625031562
          ],
          [
            0.0588487206063614,
            0.10184969368888955
          ],
          [
            -0.20214259841938173,
            0.005743934099964266
          ],
          [
            0.17161050410933973,
            0.010541668501258008
          ],
          [
            0.15177745978636792,
            0.01389375801144244
          ],
          [
            0.001971486043932359,
            0.03389035670208604
          ],
          [
            0.23362117572731222,
            0.01186033738140255
          ],
          [
            -0.7827423714161357,
            0.17092994836254657
          ],
          [
            -0.16716207648041886,
            0.02306608972569028
          ],
          [
            0.14465669708835777,
            0.06757581981154692
          ],
          [
            -0.1093573200051336,
            0.05483338418879946
          ],
          [
            -0.2637450245596155,
            -0.024498152075867037
          ],
          [
            -0.011859763374011198,
            -0.025579518599865837
          ],
          [
            -0.20247948749582162,
            0.025094436600709206
          ]
        ]
      ]
    },
    "proposal_log_prob_parameter_path_summaries": {
      "first_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      },
      "fresh_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      },
      "manual_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      },
      "official_proposal_ll": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          2
        ],
        "sum": 0.0
      }
    },
    "proposal_log_prob_parameter_path_tensors": {
      "first_dist_log_prob": [
        0.0,
        0.0
      ],
      "fresh_dist_log_prob": [
        0.0,
        0.0
      ],
      "manual_dist_log_prob": [
        0.0,
        0.0
      ],
      "official_proposal_ll": [
        0.0,
        0.0
      ]
    },
    "value_summaries": {
      "fresh_loc_minus_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "fresh_mean_minus_fresh_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "manual_minus_proposal_loc": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      },
      "official_proposal_ll_minus_first_dist_log_prob": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50
        ],
        "sum": 0.0
      },
      "official_proposal_ll_minus_fresh_dist_log_prob": {
        "finite": true,
        "max_abs": 8.890665981198254e-13,
        "shape": [
          1,
          50
        ],
        "sum": 7.285283487590277e-13
      },
      "official_proposal_ll_minus_manual_dist_log_prob": {
        "finite": true,
        "max_abs": 1.7763568394002505e-15,
        "shape": [
          1,
          50
        ],
        "sum": 5.551115123125783e-15
      },
      "proposal_loc_minus_proposal_mean": {
        "finite": true,
        "max_abs": 0.0,
        "shape": [
          1,
          50,
          2
        ],
        "sum": 0.0
      }
    },
    "value_tensors": {
      "fresh_loc_minus_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "fresh_mean_minus_fresh_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "manual_minus_proposal_loc": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ],
      "official_proposal_ll_minus_first_dist_log_prob": [
        [
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "official_proposal_ll_minus_fresh_dist_log_prob": [
        [
          -1.9539925233402755e-14,
          -2.5268676040468563e-13,
          -1.4588330543574557e-13,
          -1.1102230246251565e-14,
          7.460698725481052e-14,
          -3.26405569239796e-13,
          -1.687538997430238e-13,
          2.020605904817785e-13,
          -1.9539925233402755e-14,
          2.5623947408348613e-13,
          -7.815970093361102e-14,
          -4.3076653355456074e-14,
          6.838973831690964e-14,
          -2.9620750296999176e-13,
          4.0945025148175773e-13,
          -2.957634137601417e-13,
          -8.615330671091215e-14,
          -8.890665981198254e-13,
          1.554312234475219e-14,
          4.75175454539567e-13,
          7.993605777301127e-15,
          4.991562718714704e-13,
          1.9539925233402755e-13,
          2.0339285811132868e-13,
          -1.3278267374516872e-13,
          2.9531932455029164e-14,
          5.444533712761768e-13,
          5.235811784132238e-13,
          1.9051427102567686e-13,
          1.8340884366807586e-13,
          7.038813976123492e-14,
          -1.1102230246251565e-14,
          2.4868995751603507e-14,
          2.673417043297377e-13,
          -6.838973831690964e-14,
          -5.080380560684716e-13,
          -3.5083047578154947e-14,
          8.43769498715119e-15,
          -4.04121180963557e-14,
          3.419486915845482e-13,
          1.0347278589506459e-13,
          -1.2878587085651816e-14,
          -7.149836278586008e-14,
          -5.160316618457728e-13,
          -1.127986593019159e-13,
          -2.4069635173873394e-13,
          3.730349362740526e-14,
          4.1300296516055823e-13,
          2.7533531010703882e-14,
          -6.261657858885883e-14
        ]
      ],
      "official_proposal_ll_minus_manual_dist_log_prob": [
        [
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          -4.440892098500626e-16,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          4.440892098500626e-16,
          0.0,
          8.881784197001252e-16,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          2.220446049250313e-16,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          4.440892098500626e-16,
          0.0,
          0.0,
          0.0,
          4.440892098500626e-16,
          0.0,
          1.7763568394002505e-15,
          0.0,
          8.881784197001252e-16,
          4.440892098500626e-16,
          0.0,
          4.440892098500626e-16,
          0.0
        ]
      ],
      "proposal_loc_minus_proposal_mean": [
        [
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ],
          [
            0.0,
            0.0
          ]
        ]
      ]
    }
  },
  "resampling_adjoint_decomposition": {
    "carryover_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "carryover_pre_particle_adjoint_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "current_increment_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "current_increment_pre_particle_adjoint_tensor": [
      [
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "direct_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 0.032745181880207294,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.1083606755672504
    },
    "direct_pre_particle_adjoint_tensor": [
      [
        [
          -0.024319103368144617,
          -0.02504406308914622
        ],
        [
          0.012944610435133307,
          0.013330493131031592
        ],
        [
          0.02884173911469225,
          0.029701519955509636
        ],
        [
          0.024084452904635272,
          0.02480241762536966
        ],
        [
          0.004013043119139134,
          0.004132673130820789
        ],
        [
          0.02894734097402721,
          0.0298102698377516
        ],
        [
          0.006577652215630924,
          0.006773733988996618
        ],
        [
          -0.024355092594252514,
          -0.025081125164812885
        ],
        [
          0.023708450092640058,
          0.024415206057461305
        ],
        [
          0.01778837074710197,
          0.018318647381839432
        ],
        [
          0.005904001485979223,
          0.006080001530276707
        ],
        [
          0.023756373201152533,
          0.02446455776812456
        ],
        [
          0.021101955756551466,
          0.02173101134821018
        ],
        [
          0.031565485631906205,
          0.03250646216835869
        ],
        [
          0.003530783934873055,
          0.0036360376565088364
        ],
        [
          0.018092589710241247,
          0.01863193520295846
        ],
        [
          0.02399593693843151,
          0.024711262971826485
        ],
        [
          -0.012714799385508733,
          -0.013093831345510348
        ],
        [
          0.006343289817351173,
          0.006532385177760015
        ],
        [
          0.008071735302401649,
          0.008312356137974599
        ],
        [
          0.031797295036306544,
          0.032745181880207294
        ],
        [
          0.01725948697615904,
          0.017773997428022856
        ],
        [
          0.005135455987653716,
          0.005288545461540412
        ],
        [
          0.008329224706033617,
          0.008577521377487194
        ],
        [
          -0.005203745108677112,
          -0.005358870301618706
        ],
        [
          0.025295720255268796,
          0.02604979321680797
        ],
        [
          0.015584148083593083,
          0.016048716183645985
        ],
        [
          0.03014017801985298,
          0.03103866571150172
        ],
        [
          -0.017434868653234237,
          -0.01795460728517347
        ],
        [
          0.014362253796535713,
          0.01479039686364111
        ],
        [
          0.009721322834057158,
          0.01001111836569572
        ],
        [
          0.015258775339545755,
          0.015713643981104027
        ],
        [
          0.02349386046772338,
          0.024194219451856052
        ],
        [
          0.0044725943056013575,
          0.00460592367514503
        ],
        [
          0.02710963533377107,
          0.02791778164453388
        ],
        [
          0.02267161518623621,
          0.023347462793413976
        ],
        [
          0.02183428616354774,
          0.02248517274294889
        ],
        [
          -0.002237753675435588,
          -0.0023044617795813637
        ],
        [
          0.003129446514951148,
          0.0032227362484591768
        ],
        [
          0.028186153845544855,
          0.029026391494057033
        ],
        [
          0.009408489104583336,
          0.009688958969489616
        ],
        [
          -0.01872766810422684,
          -0.01928594547318753
        ],
        [
          0.00620620948810195,
          0.006391218443031819
        ],
        [
          0.001323590364933088,
          0.0013630469882779774
        ],
        [
          0.018278642822846067,
          0.01882353461431303
        ],
        [
          -0.013266641874962678,
          -0.013662124424080812
        ],
        [
          0.0021632484343739205,
          0.002227735515073415
        ],
        [
          0.005039991342376802,
          0.005190234986729499
        ],
        [
          0.028961441938481505,
          0.029824791156159824
        ],
        [
          -0.00012969724280729506,
          -0.00013356355627851518
        ]
      ]
    ],
    "implicit_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 15.029585354730424,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 36.60132258078865
    },
    "implicit_pre_particle_adjoint_tensor": [
      [
        [
          2.5000451532430024,
          6.0019574997919545
        ],
        [
          -1.879447157818339,
          0.5551867218493705
        ],
        [
          10.429224058105326,
          0.17856334365635168
        ],
        [
          -0.42288705683224864,
          0.511965578794572
        ],
        [
          0.7232954693205805,
          -0.6217188228217073
        ],
        [
          -2.764491113531979,
          0.8587717688051347
        ],
        [
          -0.5898081487099875,
          -0.6270342709381218
        ],
        [
          -3.488127432474286,
          3.460254716740999
        ],
        [
          2.0991091288698454,
          0.5559864562828845
        ],
        [
          0.0033870870716870907,
          -0.43802715170838935
        ],
        [
          -1.2213023946310078,
          -0.3006323988721334
        ],
        [
          0.9381260520413379,
          0.03088722332972466
        ],
        [
          1.7097280130882981,
          1.1915193981883008
        ],
        [
          6.104086354734528,
          1.0413659450818569
        ],
        [
          -1.326489619838844,
          -0.222650262000732
        ],
        [
          -1.0088438584019335,
          -0.3162391620729522
        ],
        [
          0.08150951237910482,
          0.4572618387242254
        ],
        [
          8.638087024757064,
          0.8255595893039557
        ],
        [
          -3.890798046901835,
          -0.5579692959757283
        ],
        [
          -0.036815579370403466,
          -0.34832544222009937
        ],
        [
          -10.289656922478727,
          2.1868189146876458
        ],
        [
          -1.0142069483284473,
          0.9894074420134691
        ],
        [
          -0.7484215667634293,
          -0.7132771624979758
        ],
        [
          0.2568821147293997,
          0.4066900314196445
        ],
        [
          1.6620115347061089,
          -0.1521671209238397
        ],
        [
          -6.688387163742365,
          1.209709038973669
        ],
        [
          -0.11144827870898287,
          -0.5467637609985382
        ],
        [
          1.7729414677392916,
          1.0906817283843682
        ],
        [
          -13.41090519318344,
          2.061655532148628
        ],
        [
          -0.08547046963883254,
          -0.6814349382374941
        ],
        [
          -0.18174961010403587,
          0.3938609794958791
        ],
        [
          0.7993143336331161,
          -0.1812461634658936
        ],
        [
          4.5354266997248525,
          0.16729315518539453
        ],
        [
          -1.8442238330699592,
          -0.6738622981342988
        ],
        [
          8.166913547170832,
          1.6397885408104038
        ],
        [
          0.6950571298985259,
          0.6617833121526194
        ],
        [
          0.6522690242532548,
          0.07474386736579963
        ],
        [
          0.3979017999177592,
          0.1536840321150784
        ],
        [
          1.5829388799297037,
          -0.3929839893980158
        ],
        [
          -1.0207535989250847,
          0.9617139566307972
        ],
        [
          0.5597342555522716,
          0.418633980020068
        ],
        [
          15.029585354730424,
          2.281534412833242
        ],
        [
          -0.1516052272343286,
          0.31274394028465635
        ],
        [
          -0.5035686527345117,
          0.27585262972838936
        ],
        [
          -1.093925717967689,
          -0.44873033395499906
        ],
        [
          -5.838668526988613,
          1.606919510084516
        ],
        [
          -2.44917553736102,
          -0.28522515261501363
        ],
        [
          0.05007597276815722,
          0.15181183219410893
        ],
        [
          1.6563265464660195,
          1.2502521804196616
        ],
        [
          0.09616862662500268,
          1.0657837244120454
        ]
      ]
    ],
    "same_tape_full_recorded_state_residual": {
      "finite": true,
      "max_abs": 15.29031158182802,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -42.316764919860944
    },
    "same_tape_full_recorded_state_residual_tensor": [
      [
        [
          -2.4863536047941937,
          -5.879477812019542
        ],
        [
          1.6729091869681012,
          -0.3188991939973074
        ],
        [
          -9.779499154388088,
          -0.10233104040531876
        ],
        [
          0.4014077159977325,
          -0.3857577290305261
        ],
        [
          -0.9624684860946056,
          -0.29021627622126384
        ],
        [
          2.5945047518680795,
          -0.7446733058224754
        ],
        [
          0.5899757226071107,
          -0.09780401112547332
        ],
        [
          3.5405055641685643,
          -3.816896830360645
        ],
        [
          -1.974290375261032,
          -0.43506834968511854
        ],
        [
          -0.03656465479486015,
          0.01961302573417223
        ],
        [
          1.4235912354741176,
          -0.08131075097074994
        ],
        [
          -0.8534316894680518,
          -0.06478578379109076
        ],
        [
          -1.611016087426011,
          -1.0408990381772312
        ],
        [
          -5.767833550868767,
          -0.9250120416503627
        ],
        [
          1.4509020592090651,
          -0.10484102750919322
        ],
        [
          0.733199289304897,
          -0.01671126129528966
        ],
        [
          -0.07113768682896546,
          -0.3346822267575547
        ],
        [
          -8.931971688923479,
          -0.6678483757754503
        ],
        [
          4.448150541154664,
          -0.40517309698577575
        ],
        [
          -0.04947472769035598,
          -0.11208321499797361
        ],
        [
          9.760544824868337,
          -2.0189767449731737
        ],
        [
          0.960255366976956,
          -0.7941189830506623
        ],
        [
          0.7163673453059669,
          -0.30176519450060135
        ],
        [
          -0.21830046335857728,
          -0.0885672753694815
        ],
        [
          -1.933845640897793,
          -0.8639704933429756
        ],
        [
          6.330640787912567,
          -1.0677632453724732
        ],
        [
          0.010955500649315969,
          -0.0011708703193974435
        ],
        [
          -1.6719018320383086,
          -0.9679807498039348
        ],
        [
          13.805574516918352,
          -2.6785984074750386
        ],
        [
          -0.1922814289024947,
          0.0004949158432168144
        ],
        [
          0.1503191516129324,
          -0.12452548815960629
        ],
        [
          -0.6085863996885083,
          -0.012261356997107897
        ],
        [
          -4.2259398056857105,
          -0.06048658123648687
        ],
        [
          1.9634756004283513,
          -0.32443536980447163
        ],
        [
          -7.766302230716338,
          -1.519528386728282
        ],
        [
          -0.6509644607963803,
          -0.5386350059660048
        ],
        [
          -0.595110424665815,
          -0.043177078964554694
        ],
        [
          -0.48028026149324515,
          -0.11867361177221386
        ],
        [
          -1.9101316710609524,
          -0.262528556611192
        ],
        [
          0.9572424564793376,
          -0.8415446212034767
        ],
        [
          -0.4851754761352166,
          -0.1128910960166466
        ],
        [
          -15.29031158182802,
          -1.989609874724568
        ],
        [
          0.08060438177108079,
          -0.02379759337247389
        ],
        [
          0.5367056621060441,
          -0.008242726311357695
        ],
        [
          0.6891880222185334,
          -0.03846947652365007
        ],
        [
          6.022484700220141,
          -1.5563760639011326
        ],
        [
          2.6437928145792338,
          -0.25496412361777504
        ],
        [
          -0.15407489664436888,
          0.027390881926148858
        ],
        [
          -1.5577429308874717,
          -1.1103337338524986
        ],
        [
          -0.04521693182403538,
          0.010511277547258668
        ]
      ]
    ],
    "same_tape_full_recorded_state_vjp": {
      "finite": true,
      "max_abs": 30.301169268454217,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 80.02644817621685
    },
    "same_tape_full_recorded_state_vjp_tensor": [
      [
        [
          4.9620796546690515,
          11.85639124872235
        ],
        [
          -3.5394117343513067,
          0.8874164089777095
        ],
        [
          20.237564951608107,
          0.31059590401718007
        ],
        [
          -0.8002103199253459,
          0.9225257254504677
        ],
        [
          1.6897769985343252,
          -0.3273698734696227
        ],
        [
          -5.330048524426031,
          1.6332553444653617
        ],
        [
          -1.1732062191014674,
          -0.5224565258236519
        ],
        [
          -7.052988089237103,
          7.252070421936831
        ],
        [
          4.097107954223517,
          1.0154700120254643
        ],
        [
          0.05774011261364921,
          -0.43932153006072217
        ],
        [
          -2.638989628619146,
          -0.21324164637110674
        ],
        [
          1.8153141147105423,
          0.12013756488893998
        ],
        [
          3.3418460562708607,
          2.254149447713742
        ],
        [
          11.9034853912352,
          1.9988844489005781
        ],
        [
          -2.773860895113036,
          -0.11417319683502997
        ],
        [
          -1.7239505579965893,
          -0.2808959655747041
        ],
        [
          0.1766431361465018,
          0.8166553284536066
        ],
        [
          17.557343914295036,
          1.4803141337338956
        ],
        [
          -8.332605298239148,
          -0.14626381381219258
        ],
        [
          0.02073088362235416,
          -0.22792987108415116
        ],
        [
          -20.018404452310758,
          4.238540841541027
        ],
        [
          -1.9572028283292442,
          1.8013004224921543
        ],
        [
          -1.4596534560817425,
          -0.406223422535834
        ],
        [
          0.4835118027940106,
          0.5038348281666132
        ],
        [
          3.590653430495225,
          0.7064445021175172
        ],
        [
          -12.993732231399663,
          2.3035220775629504
        ],
        [
          -0.10681963127470576,
          -0.5295441744954947
        ],
        [
          3.474983477797453,
          2.0897011438998048
        ],
        [
          -27.233914578755027,
          4.722299332338493
        ],
        [
          0.12117321306019788,
          -0.6671394572170698
        ],
        [
          -0.3223474388829111,
          0.5283975860211811
        ],
        [
          1.4231595086611701,
          -0.15327116248768166
        ],
        [
          8.784860365878286,
          0.25197395587373744
        ],
        [
          -3.803226839192709,
          -0.34482100465468213
        ],
        [
          15.960325413220941,
          3.18723470918322
        ],
        [
          1.3686932058811423,
          1.2237657809120381
        ],
        [
          1.2692137350826176,
          0.14040611907330322
        ],
        [
          0.8759443077355688,
          0.2700531821077109
        ],
        [
          3.4961999975056073,
          -0.12723269653836464
        ],
        [
          -1.9498099015588775,
          1.832284969328331
        ],
        [
          1.0543182207920716,
          0.5412140350062042
        ],
        [
          30.301169268454217,
          4.251858342084622
        ],
        [
          -0.22600339951730744,
          0.34293275210016205
        ],
        [
          -1.0389507244756226,
          0.28545840302802505
        ],
        [
          -1.7648350973633762,
          -0.39143732281703597
        ],
        [
          -11.874419869083717,
          3.1496334495615677
        ],
        [
          -5.09080510350588,
          -0.02803329348216513
        ],
        [
          0.2091908607549029,
          0.12961118525468956
        ],
        [
          3.243030919291973,
          2.39041070542832
        ],
        [
          0.14125586120623077,
          1.0551388833085082
        ]
      ]
    ],
    "same_tape_identity_residual": {
      "finite": true,
      "max_abs": 0.6735763083742867,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.883196983313975
    },
    "same_tape_identity_residual_tensor": [
      [
        [
          -0.05034137862826249,
          -0.11904220626568929
        ],
        [
          -0.2060587631761368,
          0.0392800601520068
        ],
        [
          0.6433821022233523,
          0.00673224250642071
        ],
        [
          -0.02711452768170347,
          0.026057393032993703
        ],
        [
          -0.11735773916742431,
          -0.035387263623682386
        ],
        [
          -0.17374196729738323,
          0.04986732248391035
        ],
        [
          0.10031400054454342,
          -0.01662968703516099
        ],
        [
          0.09791355496804721,
          -0.10555722363188691
        ],
        [
          0.11816249211663576,
          0.026039108068420913
        ],
        [
          0.015719160172630624,
          -0.008431647849953705
        ],
        [
          0.27588852136781705,
          -0.015757825910719336
        ],
        [
          0.09326464513016108,
          0.007079914197375969
        ],
        [
          0.0918328198956706,
          0.0593344130133624
        ],
        [
          0.330442788786943,
          0.05299451796045851
        ],
        [
          0.19956879610993905,
          -0.014420682299082666
        ],
        [
          -0.23307884565090353,
          0.005312391254183257
        ],
        [
          0.0049386347770709466,
          0.023234847209839093
        ],
        [
          -0.2866720016504605,
          -0.021434621307631074
        ],
        [
          0.6735763083742867,
          -0.06135471279472743
        ],
        [
          -0.013799783173047135,
          -0.03126291212738819
        ],
        [
          -0.5326045048931061,
          0.11016968099028679
        ],
        [
          -0.06218656532212519,
          0.05142749909171229
        ],
        [
          0.09469431400058126,
          -0.0398893783611558
        ],
        [
          0.04124877969061577,
          0.016735154718902245
        ],
        [
          -0.12186742996769828,
          -0.054445846847813326
        ],
        [
          -0.3622840020741611,
          0.06110495837006491
        ],
        [
          -0.0353907639998428,
          0.0037823917386015093
        ],
        [
          0.09562367416550566,
          0.05536322411040451
        ],
        [
          0.48954677656422696,
          -0.09498331376810976
        ],
        [
          -0.19889899651043497,
          0.000511948892489511
        ],
        [
          -0.027022382964809355,
          0.022385540324185882
        ],
        [
          0.2265619345464217,
          0.0045646053918571294
        ],
        [
          0.30333550614421334,
          0.004341691689412425
        ],
        [
          0.24586472061000508,
          -0.04062551708591555
        ],
        [
          0.3958817714687859,
          0.07745688638743742
        ],
        [
          0.03777758786978558,
          0.03125874374574811
        ],
        [
          0.06161218699842086,
          0.004470152349798945
        ],
        [
          -0.03175252040547838,
          -0.00784580708703983
        ],
        [
          -0.22495300980190214,
          -0.030917548702720954
        ],
        [
          -0.06717298828094909,
          0.05905407412235575
        ],
        [
          0.07448961855991337,
          0.017332316027339645
        ],
        [
          -0.32843440023473214,
          -0.042736625896026226
        ],
        [
          -0.056575848127798964,
          0.0167034223061463
        ],
        [
          0.0649006638614611,
          -0.0009967444866079145
        ],
        [
          -0.34821467832140274,
          0.019436838657982347
        ],
        [
          0.19573141545028427,
          -0.0505823933349594
        ],
        [
          0.2894788528476613,
          -0.027916984120379906
        ],
        [
          -0.07496109706507006,
          0.013326314691634478
        ],
        [
          0.0927414661628072,
          0.06610460324723744
        ],
        [
          -0.002677695954071524,
          0.0006224660591733766
        ]
      ]
    ],
    "same_tape_log_ess_carryover_vjp": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "same_tape_log_ess_carryover_vjp_tensor": [
      [
        [
          0.0,
          -0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "same_tape_post_log_weights_vjp": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 0.0
    },
    "same_tape_post_log_weights_vjp_tensor": [
      [
        [
          0.0,
          -0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          -0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          -0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ]
    ],
    "same_tape_post_particles_vjp": {
      "finite": true,
      "max_abs": 15.33929208686093,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 35.82648627304192
    },
    "same_tape_post_particles_vjp_tensor": [
      [
        [
          2.5260674285031204,
          6.095955642968497
        ],
        [
          -1.660443784207069,
          0.5292371548283952
        ],
        [
          9.814683694996665,
          0.20153262110544062
        ],
        [
          -0.37168807624590994,
          0.510710603386948
        ],
        [
          0.8446662516071439,
          -0.5821988860672042
        ],
        [
          -2.5618018052605684,
          0.838714716158976
        ],
        [
          -0.6835444970389001,
          -0.6036308499139642
        ],
        [
          -3.6103960800365855,
          3.540730815208073
        ],
        [
          2.0046550868458497,
          0.5543625542719248
        ],
        [
          0.005456297646158435,
          -0.41127685647659623
        ],
        [
          -1.4912869145128456,
          -0.2787945714311374
        ],
        [
          0.8686177801123294,
          0.04827186690047325
        ],
        [
          1.638997148949179,
          1.1539159965231485
        ],
        [
          5.8052090515794905,
          1.020877889289757
        ],
        [
          -1.52252763201391,
          -0.20459354204514052
        ],
        [
          -0.7576724230407887,
          -0.302919618124177
        ],
        [
          0.10056681454046537,
          0.45873825448621275
        ],
        [
          8.912044227022017,
          0.8339003792660764
        ],
        [
          -4.558031065458771,
          -0.4900821980032409
        ],
        [
          -0.014944060894954703,
          -0.3087501739547366
        ],
        [
          -9.725255122549314,
          2.1093944155775666
        ],
        [
          -0.9347608960301632,
          0.9557539403497797
        ],
        [
          -0.8379804247763568,
          -0.6680992386752795
        ],
        [
          0.22396255974481757,
          0.3985323980782294
        ],
        [
          1.7786752195651299,
          -0.10308014437764512
        ],
        [
          -6.300807441412935,
          1.1746538738204122
        ],
        [
          -0.06047336662554699,
          -0.5344974365534937
        ],
        [
          1.707457971593639,
          1.0663571699854655
        ],
        [
          -13.9178868384009,
          2.138684238631564
        ],
        [
          0.12779078066813815,
          -0.6671564902663425
        ],
        [
          -0.14500590430516938,
          0.38148655753738897
        ],
        [
          0.5880111744262401,
          -0.1700971248766467
        ],
        [
          4.255585054048362,
          0.18714568294783815
        ],
        [
          -2.085615959374363,
          -0.6286308573732382
        ],
        [
          7.798141411035818,
          1.5902494360675001
        ],
        [
          0.6799511572149766,
          0.6538720312002853
        ],
        [
          0.6124911234183816,
          0.09275888775894958
        ],
        [
          0.427416566647802,
          0.15922537742253684
        ],
        [
          1.811021336246557,
          -0.3588437044468357
        ],
        [
          -0.9253944567985909,
          0.9316862740024985
        ],
        [
          0.49465312609694156,
          0.410990622962218
        ],
        [
          15.33929208686093,
          2.3049850932560805
        ],
        [
          -0.08882316961842769,
          0.30243173642154186
        ],
        [
          -0.5671457262310396,
          0.2782124212032753
        ],
        [
          -0.7274323968234401,
          -0.4493436379986684
        ],
        [
          -6.047666584313859,
          1.6438397789953945
        ],
        [
          -2.736491141774307,
          -0.25508043297956035
        ],
        [
          0.13007706117560403,
          0.14367575248920395
        ],
        [
          1.592546522241694,
          1.213972368328584
        ],
        [
          0.09871662533626692,
          1.0650276947965935
        ]
      ]
    ],
    "same_tape_post_state_identity_residual": {
      "finite": true,
      "max_abs": 0.6735763083742867,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.8831969833139721
    },
    "same_tape_post_state_identity_residual_tensor": [
      [
        [
          -0.05034137862826249,
          -0.11904220626568929
        ],
        [
          -0.20605876317613658,
          0.03928006015200691
        ],
        [
          0.6433821022233541,
          0.0067322425064206826
        ],
        [
          -0.027114527681703415,
          0.026057393032993703
        ],
        [
          -0.11735773916742431,
          -0.035387263623682386
        ],
        [
          -0.17374196729738323,
          0.04986732248391035
        ],
        [
          0.10031400054454342,
          -0.01662968703516099
        ],
        [
          0.09791355496804677,
          -0.10555722363188691
        ],
        [
          0.11816249211663576,
          0.026039108068420913
        ],
        [
          0.015719160172630624,
          -0.008431647849953705
        ],
        [
          0.27588852136781705,
          -0.01575782591071928
        ],
        [
          0.09326464513016108,
          0.007079914197375969
        ],
        [
          0.0918328198956706,
          0.0593344130133624
        ],
        [
          0.330442788786943,
          0.05299451796045851
        ],
        [
          0.19956879610993905,
          -0.014420682299082666
        ],
        [
          -0.23307884565090353,
          0.005312391254183257
        ],
        [
          0.0049386347770709604,
          0.023234847209839093
        ],
        [
          -0.2866720016504605,
          -0.021434621307631074
        ],
        [
          0.6735763083742867,
          -0.06135471279472743
        ],
        [
          -0.013799783173047114,
          -0.03126291212738819
        ],
        [
          -0.5326045048931078,
          0.11016968099028634
        ],
        [
          -0.062186565322124965,
          0.05142749909171229
        ],
        [
          0.09469431400058126,
          -0.0398893783611558
        ],
        [
          0.04124877969061577,
          0.0167351547189023
        ],
        [
          -0.12186742996769806,
          -0.054445846847813284
        ],
        [
          -0.3622840020741611,
          0.06110495837006491
        ],
        [
          -0.0353907639998428,
          0.0037823917386015093
        ],
        [
          0.09562367416550543,
          0.05536322411040451
        ],
        [
          0.4895467765642252,
          -0.09498331376810931
        ],
        [
          -0.19889899651043497,
          0.000511948892489511
        ],
        [
          -0.027022382964809327,
          0.022385540324185882
        ],
        [
          0.22656193454642182,
          0.0045646053918571294
        ],
        [
          0.30333550614421334,
          0.004341691689412425
        ],
        [
          0.24586472061000508,
          -0.04062551708591555
        ],
        [
          0.395881771468785,
          0.07745688638743764
        ],
        [
          0.03777758786978547,
          0.03125874374574811
        ],
        [
          0.06161218699842097,
          0.004470152349798945
        ],
        [
          -0.03175252040547838,
          -0.007845807087039802
        ],
        [
          -0.22495300980190214,
          -0.0309175487027209
        ],
        [
          -0.06717298828094898,
          0.05905407412235575
        ],
        [
          0.07448961855991343,
          0.017332316027339645
        ],
        [
          -0.32843440023473214,
          -0.042736625896026226
        ],
        [
          -0.056575848127798964,
          0.0167034223061463
        ],
        [
          0.0649006638614611,
          -0.0009967444866079145
        ],
        [
          -0.34821467832140274,
          0.019436838657982347
        ],
        [
          0.19573141545028339,
          -0.0505823933349594
        ],
        [
          0.28947885284766084,
          -0.02791698412037985
        ],
        [
          -0.07496109706507001,
          0.013326314691634478
        ],
        [
          0.0927414661628072,
          0.06610460324723744
        ],
        [
          -0.002677695954071538,
          0.0006224660591733766
        ]
      ]
    ],
    "same_tape_post_state_vjp": {
      "finite": true,
      "max_abs": 15.33929208686093,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 35.82648627304192
    },
    "same_tape_post_state_vjp_tensor": [
      [
        [
          2.5260674285031204,
          6.095955642968497
        ],
        [
          -1.660443784207069,
          0.5292371548283952
        ],
        [
          9.814683694996665,
          0.20153262110544062
        ],
        [
          -0.37168807624590994,
          0.510710603386948
        ],
        [
          0.8446662516071439,
          -0.5821988860672042
        ],
        [
          -2.5618018052605684,
          0.838714716158976
        ],
        [
          -0.6835444970389001,
          -0.6036308499139642
        ],
        [
          -3.6103960800365855,
          3.540730815208073
        ],
        [
          2.0046550868458497,
          0.5543625542719248
        ],
        [
          0.005456297646158435,
          -0.41127685647659623
        ],
        [
          -1.4912869145128456,
          -0.2787945714311374
        ],
        [
          0.8686177801123294,
          0.04827186690047325
        ],
        [
          1.638997148949179,
          1.1539159965231485
        ],
        [
          5.8052090515794905,
          1.020877889289757
        ],
        [
          -1.52252763201391,
          -0.20459354204514052
        ],
        [
          -0.7576724230407887,
          -0.302919618124177
        ],
        [
          0.10056681454046537,
          0.45873825448621275
        ],
        [
          8.912044227022017,
          0.8339003792660764
        ],
        [
          -4.558031065458771,
          -0.4900821980032409
        ],
        [
          -0.014944060894954703,
          -0.3087501739547366
        ],
        [
          -9.725255122549314,
          2.1093944155775666
        ],
        [
          -0.9347608960301632,
          0.9557539403497797
        ],
        [
          -0.8379804247763568,
          -0.6680992386752795
        ],
        [
          0.22396255974481757,
          0.3985323980782294
        ],
        [
          1.7786752195651299,
          -0.10308014437764512
        ],
        [
          -6.300807441412935,
          1.1746538738204122
        ],
        [
          -0.06047336662554699,
          -0.5344974365534937
        ],
        [
          1.707457971593639,
          1.0663571699854655
        ],
        [
          -13.9178868384009,
          2.138684238631564
        ],
        [
          0.12779078066813815,
          -0.6671564902663425
        ],
        [
          -0.14500590430516938,
          0.38148655753738897
        ],
        [
          0.5880111744262401,
          -0.1700971248766467
        ],
        [
          4.255585054048362,
          0.18714568294783815
        ],
        [
          -2.085615959374363,
          -0.6286308573732382
        ],
        [
          7.798141411035818,
          1.5902494360675001
        ],
        [
          0.6799511572149766,
          0.6538720312002853
        ],
        [
          0.6124911234183816,
          0.09275888775894958
        ],
        [
          0.427416566647802,
          0.15922537742253684
        ],
        [
          1.811021336246557,
          -0.3588437044468357
        ],
        [
          -0.9253944567985909,
          0.9316862740024985
        ],
        [
          0.49465312609694156,
          0.410990622962218
        ],
        [
          15.33929208686093,
          2.3049850932560805
        ],
        [
          -0.08882316961842769,
          0.30243173642154186
        ],
        [
          -0.5671457262310396,
          0.2782124212032753
        ],
        [
          -0.7274323968234401,
          -0.4493436379986684
        ],
        [
          -6.047666584313859,
          1.6438397789953945
        ],
        [
          -2.736491141774307,
          -0.25508043297956035
        ],
        [
          0.13007706117560403,
          0.14367575248920395
        ],
        [
          1.592546522241694,
          1.213972368328584
        ],
        [
          0.09871662533626692,
          1.0650276947965935
        ]
      ]
    ],
    "same_tape_pre_current_ll_carryover_vjp": {
      "finite": true,
      "max_abs": 0.6735763083742855,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 1.883196983313978
    },
    "same_tape_pre_current_ll_carryover_vjp_tensor": [
      [
        [
          -0.05034137862826332,
          -0.1190422062656886
        ],
        [
          -0.2060587631761367,
          0.03928006015200694
        ],
        [
          0.6433821022233541,
          0.006732242506420721
        ],
        [
          -0.02711452768170336,
          0.026057393032993682
        ],
        [
          -0.1173577391674243,
          -0.035387263623682316
        ],
        [
          -0.1737419672973829,
          0.04986732248391006
        ],
        [
          0.10031400054454347,
          -0.016629687035161097
        ],
        [
          0.09791355496804682,
          -0.10555722363188678
        ],
        [
          0.11816249211663551,
          0.026039108068420976
        ],
        [
          0.0157191601726306,
          -0.008431647849953651
        ],
        [
          0.2758885213678167,
          -0.015757825910719333
        ],
        [
          0.09326464513016111,
          0.007079914197375972
        ],
        [
          0.09183281989567002,
          0.05933441301336222
        ],
        [
          0.3304427887869437,
          0.05299451796045857
        ],
        [
          0.19956879610993952,
          -0.01442068229908265
        ],
        [
          -0.2330788456509033,
          0.00531239125418328
        ],
        [
          0.004938634777070929,
          0.023234847209839104
        ],
        [
          -0.2866720016504609,
          -0.021434621307631168
        ],
        [
          0.6735763083742855,
          -0.06135471279472728
        ],
        [
          -0.013799783173047073,
          -0.03126291212738815
        ],
        [
          -0.5326045048931063,
          0.11016968099028611
        ],
        [
          -0.06218656532212499,
          0.05142749909171251
        ],
        [
          0.09469431400058148,
          -0.03988937836115582
        ],
        [
          0.04124877969061583,
          0.016735154718902287
        ],
        [
          -0.12186742996769792,
          -0.054445846847813256
        ],
        [
          -0.36228400207416045,
          0.06110495837006504
        ],
        [
          -0.03539076399984273,
          0.003782391738601462
        ],
        [
          0.09562367416550563,
          0.05536322411040482
        ],
        [
          0.4895467765642287,
          -0.09498331376811019
        ],
        [
          -0.19889899651043466,
          0.0005119488924894993
        ],
        [
          -0.02702238296480939,
          0.022385540324185948
        ],
        [
          0.22656193454642204,
          0.00456460539185712
        ],
        [
          0.30333550614421295,
          0.004341691689412422
        ],
        [
          0.24586472061000517,
          -0.040625517085915455
        ],
        [
          0.39588177146878456,
          0.07745688638743735
        ],
        [
          0.037777587869785446,
          0.03125874374574814
        ],
        [
          0.06161218699842083,
          0.004470152349798923
        ],
        [
          -0.031752520405478414,
          -0.007845807087039823
        ],
        [
          -0.22495300980190175,
          -0.030917548702720874
        ],
        [
          -0.06717298828094909,
          0.059054074122355936
        ],
        [
          0.07448961855991332,
          0.017332316027339638
        ],
        [
          -0.3284344002347315,
          -0.042736625896026344
        ],
        [
          -0.05657584812779883,
          0.016703422306146222
        ],
        [
          0.06490066386146126,
          -0.0009967444866079082
        ],
        [
          -0.3482146783214022,
          0.01943683865798229
        ],
        [
          0.19573141545028389,
          -0.05058239333495937
        ],
        [
          0.289478852847661,
          -0.027916984120379826
        ],
        [
          -0.07496109706507009,
          0.013326314691634483
        ],
        [
          0.09274146616280712,
          0.06610460324723724
        ],
        [
          -0.002677695954071518,
          0.0006224660591733505
        ]
      ]
    ],
    "same_tape_pre_log_weights_carryover_vjp": {
      "finite": true,
      "max_abs": 15.290311581828018,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 42.316764919860944
    },
    "same_tape_pre_log_weights_carryover_vjp_tensor": [
      [
        [
          2.4863536047941945,
          5.879477812019541
        ],
        [
          -1.6729091869681012,
          0.31889919399730743
        ],
        [
          9.779499154388084,
          0.10233104040531872
        ],
        [
          -0.4014077159977325,
          0.3857577290305261
        ],
        [
          0.9624684860946057,
          0.2902162762212638
        ],
        [
          -2.59450475186808,
          0.7446733058224757
        ],
        [
          -0.5899757226071108,
          0.09780401112547338
        ],
        [
          -3.5405055641685643,
          3.816896830360644
        ],
        [
          1.9742903752610323,
          0.43506834968511837
        ],
        [
          0.03656465479486018,
          -0.019613025734172302
        ],
        [
          -1.4235912354741171,
          0.08131075097075
        ],
        [
          0.8534316894680518,
          0.06478578379109076
        ],
        [
          1.6110160874260118,
          1.0408990381772314
        ],
        [
          5.767833550868766,
          0.9250120416503627
        ],
        [
          -1.4509020592090656,
          0.1048410275091932
        ],
        [
          -0.733199289304897,
          0.016711261295289652
        ],
        [
          0.07113768682896549,
          0.33468222675755466
        ],
        [
          8.931971688923479,
          0.6678483757754503
        ],
        [
          -4.4481505411546625,
          0.4051730969857756
        ],
        [
          0.049474727690355935,
          0.11208321499797358
        ],
        [
          -9.760544824868337,
          2.0189767449731737
        ],
        [
          -0.960255366976956,
          0.7941189830506621
        ],
        [
          -0.7163673453059671,
          0.30176519450060135
        ],
        [
          0.21830046335857725,
          0.08856727536948153
        ],
        [
          1.9338456408977927,
          0.8639704933429756
        ],
        [
          -6.330640787912568,
          1.0677632453724732
        ],
        [
          -0.010955500649316037,
          0.0011708703193974584
        ],
        [
          1.6719018320383088,
          0.9679807498039347
        ],
        [
          -13.805574516918355,
          2.67859840747504
        ],
        [
          0.19228142890249436,
          -0.000494915843216766
        ],
        [
          -0.15031915161293233,
          0.12452548815960622
        ],
        [
          0.608586399688508,
          0.012261356997107908
        ],
        [
          4.225939805685711,
          0.06048658123648686
        ],
        [
          -1.9634756004283513,
          0.3244353698044715
        ],
        [
          7.766302230716338,
          1.5195283867282823
        ],
        [
          0.6509644607963803,
          0.5386350059660049
        ],
        [
          0.5951104246658152,
          0.04317707896455473
        ],
        [
          0.4802802614932452,
          0.11867361177221385
        ],
        [
          1.910131671060952,
          0.26252855661119195
        ],
        [
          -0.9572424564793375,
          0.8415446212034766
        ],
        [
          0.4851754761352166,
          0.1128910960166466
        ],
        [
          15.290311581828018,
          1.9896098747245676
        ],
        [
          -0.0806043817710809,
          0.02379759337247396
        ],
        [
          -0.5367056621060442,
          0.00824272631135767
        ],
        [
          -0.689188022218534,
          0.038469476523650126
        ],
        [
          -6.022484700220142,
          1.5563760639011321
        ],
        [
          -2.6437928145792333,
          0.25496412361777504
        ],
        [
          0.15407489664436896,
          -0.02739088192614885
        ],
        [
          1.5577429308874717,
          1.1103337338524988
        ],
        [
          0.04521693182403536,
          -0.010511277547258677
        ]
      ]
    ],
    "same_tape_reconstructed_pre_particle_adjoint": {
      "finite": true,
      "max_abs": 15.33929208686093,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 35.82648627304192
    },
    "same_tape_reconstructed_pre_particle_adjoint_tensor": [
      [
        [
          2.5260674285031204,
          6.095955642968497
        ],
        [
          -1.6604437842070687,
          0.5292371548283953
        ],
        [
          9.814683694996667,
          0.2015326211054406
        ],
        [
          -0.3716880762459099,
          0.510710603386948
        ],
        [
          0.8446662516071439,
          -0.5821988860672042
        ],
        [
          -2.5618018052605684,
          0.838714716158976
        ],
        [
          -0.6835444970389001,
          -0.6036308499139642
        ],
        [
          -3.610396080036586,
          3.540730815208073
        ],
        [
          2.0046550868458497,
          0.5543625542719248
        ],
        [
          0.005456297646158435,
          -0.41127685647659623
        ],
        [
          -1.4912869145128456,
          -0.27879457143113734
        ],
        [
          0.8686177801123294,
          0.04827186690047325
        ],
        [
          1.638997148949179,
          1.1539159965231485
        ],
        [
          5.8052090515794905,
          1.020877889289757
        ],
        [
          -1.52252763201391,
          -0.20459354204514052
        ],
        [
          -0.7576724230407887,
          -0.302919618124177
        ],
        [
          0.10056681454046539,
          0.45873825448621275
        ],
        [
          8.912044227022017,
          0.8339003792660764
        ],
        [
          -4.558031065458771,
          -0.4900821980032409
        ],
        [
          -0.014944060894954682,
          -0.3087501739547366
        ],
        [
          -9.725255122549315,
          2.109394415577566
        ],
        [
          -0.934760896030163,
          0.9557539403497797
        ],
        [
          -0.8379804247763568,
          -0.6680992386752795
        ],
        [
          0.22396255974481757,
          0.39853239807822943
        ],
        [
          1.77867521956513,
          -0.10308014437764508
        ],
        [
          -6.300807441412935,
          1.1746538738204122
        ],
        [
          -0.06047336662554699,
          -0.5344974365534937
        ],
        [
          1.7074579715936389,
          1.0663571699854655
        ],
        [
          -13.917886838400902,
          2.1386842386315643
        ],
        [
          0.12779078066813815,
          -0.6671564902663425
        ],
        [
          -0.14500590430516935,
          0.38148655753738897
        ],
        [
          0.5880111744262402,
          -0.1700971248766467
        ],
        [
          4.255585054048362,
          0.18714568294783815
        ],
        [
          -2.085615959374363,
          -0.6286308573732382
        ],
        [
          7.798141411035817,
          1.5902494360675004
        ],
        [
          0.6799511572149765,
          0.6538720312002853
        ],
        [
          0.6124911234183817,
          0.09275888775894958
        ],
        [
          0.427416566647802,
          0.15922537742253687
        ],
        [
          1.811021336246557,
          -0.35884370444683567
        ],
        [
          -0.9253944567985908,
          0.9316862740024985
        ],
        [
          0.4946531260969416,
          0.410990622962218
        ],
        [
          15.33929208686093,
          2.3049850932560805
        ],
        [
          -0.08882316961842769,
          0.30243173642154186
        ],
        [
          -0.5671457262310396,
          0.2782124212032753
        ],
        [
          -0.7274323968234401,
          -0.4493436379986684
        ],
        [
          -6.04766658431386,
          1.6438397789953945
        ],
        [
          -2.7364911417743074,
          -0.2550804329795603
        ],
        [
          0.13007706117560408,
          0.14367575248920395
        ],
        [
          1.592546522241694,
          1.213972368328584
        ],
        [
          0.0987166253362669,
          1.0650276947965935
        ]
      ]
    ],
    "same_tape_transport_matrix_vjp": {
      "finite": true,
      "max_abs": 15.358019754965156,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 34.718125597474675
    },
    "same_tape_transport_matrix_vjp_tensor": [
      [
        [
          2.550386531871265,
          6.120999706057644
        ],
        [
          -1.6733883946422021,
          0.5159066616973637
        ],
        [
          9.785841955881974,
          0.17183110114993097
        ],
        [
          -0.39577252915054517,
          0.48590818576157835
        ],
        [
          0.8406532084880048,
          -0.5863315591980249
        ],
        [
          -2.5907491462345957,
          0.8089044463212244
        ],
        [
          -0.690122149254531,
          -0.6104045839029608
        ],
        [
          -3.5860409874423333,
          3.565811940372886
        ],
        [
          1.9809466367532098,
          0.5299473482144635
        ],
        [
          -0.012332073100943534,
          -0.42959550385843565
        ],
        [
          -1.4971909159988248,
          -0.28487457296141405
        ],
        [
          0.8448614069111768,
          0.023807309132348693
        ],
        [
          1.6178951931926275,
          1.1321849851749384
        ],
        [
          5.773643565947585,
          0.9883714271213984
        ],
        [
          -1.526058415948783,
          -0.20822957970164935
        ],
        [
          -0.77576501275103,
          -0.3215515533271355
        ],
        [
          0.07657087760203388,
          0.4340269915143863
        ],
        [
          8.924759026407525,
          0.8469942106115868
        ],
        [
          -4.564374355276121,
          -0.4966145831810009
        ],
        [
          -0.02301579619735633,
          -0.3170625300927112
        ],
        [
          -9.757052417585621,
          2.076649233697359
        ],
        [
          -0.9520203830063221,
          0.9379799429217568
        ],
        [
          -0.8431158807640106,
          -0.67338778413682
        ],
        [
          0.21563333503878396,
          0.38995487670074225
        ],
        [
          1.7838789646738071,
          -0.09772127407602638
        ],
        [
          -6.326103161668204,
          1.1486040806036042
        ],
        [
          -0.07605751470914007,
          -0.5505461527371397
        ],
        [
          1.677317793573786,
          1.0353185042739637
        ],
        [
          -13.900451969747667,
          2.1566388459167376
        ],
        [
          0.11342852687160243,
          -0.6819468871299836
        ],
        [
          -0.15472722713922651,
          0.37147543917169323
        ],
        [
          0.5727523990866944,
          -0.18581076885775072
        ],
        [
          4.232091193580639,
          0.1629514634959821
        ],
        [
          -2.0900885536799643,
          -0.6332367810483832
        ],
        [
          7.771031775702046,
          1.5623316544229664
        ],
        [
          0.6572795420287403,
          0.6305245684068713
        ],
        [
          0.590656837254834,
          0.07027371501600069
        ],
        [
          0.4296543203232376,
          0.16152983920211822
        ],
        [
          1.8078918897316059,
          -0.36206644069529487
        ],
        [
          -0.9535806106441357,
          0.9026598825084414
        ],
        [
          0.48524463699235826,
          0.4013016639927284
        ],
        [
          15.358019754965156,
          2.324271038729268
        ],
        [
          -0.09502937910652964,
          0.29604051797851005
        ],
        [
          -0.5684693165959728,
          0.2768493742149973
        ],
        [
          -0.7457110396462862,
          -0.4681671726129814
        ],
        [
          -6.034399942438897,
          1.6575019034194753
        ],
        [
          -2.7386543902086813,
          -0.2573081684946337
        ],
        [
          0.12503706983322727,
          0.13848551750247445
        ],
        [
          1.5635850803032123,
          1.1841475771724241
        ],
        [
          0.0988463225790742,
          1.065161258352872
        ]
      ]
    ]
  },
  "resampling_flag": [
    true
  ],
  "settings": {
    "T": 100,
    "batch_size": 1,
    "convergence_threshold": 1e-06,
    "data_seed": 123,
    "dtype": "float64",
    "epsilon": 0.25,
    "filter_seed": 1234,
    "max_iter": 500,
    "mesh_index": 173,
    "n_particles": 50,
    "resampling_neff": 0.9999,
    "scaling": 0.85,
    "target_time_index": 93,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ],
    "transport_backward": "FilterFlow custom gradient clips d_transport to [-1,1]"
  },
  "status": "executed",
  "stderr_excerpt": "",
  "target_scalar": -141.71711568080488,
  "total_gradient_diag": [
    9110.446610302024,
    56.9898732897215
  ],
  "transport_upstream_clip_fraction": 0.88,
  "value_summaries": {
    "fresh_dist_log_prob": {
      "finite": true,
      "max_abs": 4.717860757900072,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709028291
    },
    "fresh_proposal_loc": {
      "finite": true,
      "max_abs": 519.2188441084146,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.416680177645
    },
    "fresh_proposal_mean": {
      "finite": true,
      "max_abs": 519.2188441084146,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.416680177645
    },
    "increment": {
      "finite": true,
      "max_abs": 0.7603288018870904,
      "shape": [
        1
      ],
      "sum": -0.7603288018870904
    },
    "log_ess": {
      "finite": true,
      "max_abs": 3.8274888177225184,
      "shape": [
        1
      ],
      "sum": 3.8274888177225184
    },
    "manual_dist_log_prob": {
      "finite": true,
      "max_abs": 4.71786075790059,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709029013
    },
    "manual_proposal_mean": {
      "finite": true,
      "max_abs": 519.2188441084146,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.416680177645
    },
    "normalized": {
      "finite": true,
      "max_abs": 5.016766134437026,
      "shape": [
        1,
        50
      ],
      "sum": -200.45945262619068
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 1.383508147383262,
      "shape": [
        1,
        50
      ],
      "sum": 53.39734671646968
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 3.912023005428146,
      "shape": [
        1,
        50
      ],
      "sum": -195.60115027140728
    },
    "post_particles": {
      "finite": true,
      "max_abs": 509.3920006641104,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 26682.338280653392
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 141.71711568080488,
      "shape": [
        1
      ],
      "sum": -141.71711568080488
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 5.016766134437026,
      "shape": [
        1,
        50
      ],
      "sum": -200.45945262619068
    },
    "pre_current_log_likelihoods": {
      "finite": true,
      "max_abs": 140.9567868789178,
      "shape": [
        1
      ],
      "sum": -140.9567868789178
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 7.591460570276422,
      "shape": [
        1,
        50
      ],
      "sum": -200.41515945219265
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 509.5286014281429,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 26683.729204002535
    },
    "proposal_dist_log_prob": {
      "finite": true,
      "max_abs": 4.7178607579005885,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709029018
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 4.7178607579005885,
      "shape": [
        1,
        50
      ],
      "sum": 13.963420709029018
    },
    "proposal_loc": {
      "finite": true,
      "max_abs": 519.2188441084146,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.416680177645
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 519.2188441084146,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27178.416680177645
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 519.3668650770353,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 27168.993512173354
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 4.948835414176724,
      "shape": [
        1,
        50
      ],
      "sum": -82.30866845657856
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 0.3191070692332988,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 50.0
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 5.777094936324116,
      "shape": [
        1,
        50
      ],
      "sum": -238.47589272054523
    }
  }
}
```

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No gradient correctness beyond this fixed 1D scalar fixture is concluded.
- No correctness claim is made for either implementation.
- No analytic smoothness-gradient correctness is concluded.
- No full mesh_size=20 surface agreement is concluded.
- No production dtype default is concluded.
- Finite VJPs alone are smoke evidence only.
