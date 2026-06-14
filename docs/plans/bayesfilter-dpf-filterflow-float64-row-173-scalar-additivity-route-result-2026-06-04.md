# Result: Row 173 Scalar-Additivity Route Probe

## Decision

`filterflow_float64_row_173_scalar_additivity_sum_route_residual`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_scalar_additivity_sum_route_residual | components match but recomputed sum route differs | {'all_vetoes_clear': True, 'comparator_drift': False, 'path_boundary_clean': True, 'resampling_flags_match': True, 'scalar_value_gate_pass': True, 'gradient_rows_finite': True, 'cpu_only_parent': True} | single row/time diagnostic; no global gradient claim | inspect recomputed-sum graph construction and tape persistence | correctness of either implementation or production readiness |

## Comparison

```json
{
  "bayesfilter_within_side_additivity": {
    "additivity_pass": false,
    "max_abs_gradient_additivity_gap": 1774.8521838055622,
    "post_gradient_minus_component_gradients": [
      -1774.8521838055622,
      349.29805829650934
    ],
    "post_gradient_minus_sum_gradient": [
      0.0,
      0.0
    ],
    "sum_gradient_minus_component_gradients": [
      -1774.8521838055622,
      349.29805829650934
    ],
    "value_post_minus_sum": 0.0,
    "value_sum_minus_components": 0.0
  },
  "filterflow_within_side_additivity": {
    "additivity_pass": false,
    "max_abs_gradient_additivity_gap": 1780.154883478901,
    "post_gradient_minus_component_gradients": [
      -1780.154883478901,
      349.43183425632225
    ],
    "post_gradient_minus_sum_gradient": [
      0.0,
      0.0
    ],
    "sum_gradient_minus_component_gradients": [
      -1780.154883478901,
      349.43183425632225
    ],
    "value_post_minus_sum": 0.0,
    "value_sum_minus_components": 0.0
  },
  "first_gradient_delta_over_tolerance": {
    "field": "post_update_mean",
    "row": {
      "bayesfilter": [
        9110.446610302024,
        56.9898732897215
      ],
      "delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "filterflow": [
        9105.143875898348,
        57.123649814928335
      ],
      "finite": true,
      "max_abs_delta": 5.302734403676368
    },
    "status": "delta",
    "tolerance": 0.0002
  },
  "gradient_rows": {
    "increment_mean": {
      "bayesfilter": [
        11886.758024308658,
        -572.9815240691337
      ],
      "delta": [
        -5.524705193238333e-05,
        -7.156052106438437e-07
      ],
      "filterflow": [
        11886.75807955571,
        -572.9815233535285
      ],
      "finite": true,
      "max_abs_delta": 5.524705193238333e-05
    },
    "post_update_mean": {
      "bayesfilter": [
        9110.446610302024,
        56.9898732897215
      ],
      "delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "filterflow": [
        9105.143875898348,
        57.123649814928335
      ],
      "finite": true,
      "max_abs_delta": 5.302734403676368
    },
    "pre_current_mean": {
      "bayesfilter": [
        -1001.4592302010708,
        280.67333906234586
      ],
      "delta": [
        8.997739007554628e-05,
        1.5021129229353392e-07
      ],
      "filterflow": [
        -1001.4593201784609,
        280.67333891213457
      ],
      "finite": true,
      "max_abs_delta": 8.997739007554628e-05
    },
    "sum_pre_current_plus_increment_mean": {
      "bayesfilter": [
        9110.446610302024,
        56.9898732897215
      ],
      "delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "filterflow": [
        9105.143875898348,
        57.123649814928335
      ],
      "finite": true,
      "max_abs_delta": 5.302734403676368
    }
  },
  "interpretation": "summed_direct_scalar_route_differs_despite_component_gradient_match",
  "max_abs_gradient_delta": 5.302734403676368,
  "max_abs_scalar_value_delta": 6.351314141284092e-09,
  "scalar_value_rows": {
    "increment_mean": {
      "abs_delta": 1.389235393389754e-10,
      "bayesfilter": -0.7603288018870904,
      "delta": -1.389235393389754e-10,
      "filterflow": -0.7603288017481669
    },
    "post_update_mean": {
      "abs_delta": 6.2123888255882775e-09,
      "bayesfilter": -141.71711568080488,
      "delta": 6.2123888255882775e-09,
      "filterflow": -141.71711568701727
    },
    "pre_current_mean": {
      "abs_delta": 6.351314141284092e-09,
      "bayesfilter": -140.9567868789178,
      "delta": 6.351314141284092e-09,
      "filterflow": -140.9567868852691
    },
    "sum_pre_current_plus_increment_mean": {
      "abs_delta": 6.2123888255882775e-09,
      "bayesfilter": -141.71711568080488,
      "delta": 6.2123888255882775e-09,
      "filterflow": -141.71711568701727
    }
  },
  "status": "compared",
  "total_gradient_consistency": {
    "bayesfilter": {
      "delta": [
        0.0,
        0.0
      ],
      "finite": true,
      "max_abs_delta": 0.0,
      "recorded_total_gradient": [
        9110.446610302024,
        56.9898732897215
      ],
      "scalar_post_update_gradient": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    "filterflow": {
      "delta": [
        0.0,
        0.0
      ],
      "finite": true,
      "max_abs_delta": 0.0,
      "recorded_total_gradient": [
        9105.143875898348,
        57.123649814928335
      ],
      "scalar_post_update_gradient": [
        9105.143875898348,
        57.123649814928335
      ]
    }
  }
}
```

## Veto Status

```json
{
  "all_vetoes_clear": true,
  "comparator_drift": false,
  "cpu_only_parent": true,
  "gradient_rows_finite": true,
  "path_boundary_clean": true,
  "resampling_flags_match": true,
  "scalar_value_gate_pass": true
}
```

## FilterFlow Probe

```json
{
  "backend": "executable_filterflow_subprocess",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "resampling_flag": [
    true
  ],
  "scalar_additivity_probe": {
    "contract": "Direct scalar-gradient additivity check for post_update_log_likelihoods = pre_current_log_likelihoods + increment. These gradients use scalar objectives directly, not target-upstream VJPs through intermediate tensors.",
    "gradient_diag_tensors": {
      "increment_mean": [
        11886.75807955571,
        -572.9815233535285
      ],
      "post_update_mean": [
        9105.143875898348,
        57.123649814928335
      ],
      "pre_current_mean": [
        -1001.4593201784609,
        280.67333891213457
      ],
      "sum_pre_current_plus_increment_mean": [
        9105.143875898348,
        57.123649814928335
      ]
    },
    "gradient_matrix_summaries": {
      "increment_mean": {
        "finite": true,
        "max_abs": 12960.056049969087,
        "shape": [
          2,
          2
        ],
        "sum": -1217.0314431990469
      },
      "post_update_mean": {
        "finite": true,
        "max_abs": 9105.143875898348,
        "shape": [
          2,
          2
        ],
        "sum": 8274.802527674565
      },
      "pre_current_mean": {
        "finite": true,
        "max_abs": 6744.555552769788,
        "shape": [
          2,
          2
        ],
        "sum": 5901.88326547387
      },
      "sum_pre_current_plus_increment_mean": {
        "finite": true,
        "max_abs": 9105.143875898348,
        "shape": [
          2,
          2
        ],
        "sum": 8274.802527674565
      }
    },
    "gradient_matrix_tensors": {
      "increment_mean": [
        [
          11886.75807955571,
          429.24805056785937
        ],
        [
          -12960.056049969087,
          -572.9815233535285
        ]
      ],
      "post_update_mean": [
        [
          9105.143875898348,
          226.78699989193615
        ],
        [
          -1114.2519979306471,
          57.123649814928335
        ]
      ],
      "pre_current_mean": [
        [
          -1001.4593201784609,
          -121.88630602959134
        ],
        [
          6744.555552769788,
          280.67333891213457
        ]
      ],
      "sum_pre_current_plus_increment_mean": [
        [
          9105.143875898348,
          226.78699989193615
        ],
        [
          -1114.2519979306471,
          57.123649814928335
        ]
      ]
    },
    "scalar_values": {
      "increment_mean": -0.7603288017481669,
      "post_update_mean": -141.71711568701727,
      "pre_current_mean": -140.9567868852691,
      "sum_pre_current_plus_increment_mean": -141.71711568701727
    }
  },
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
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-04 21:51:21.825948: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780581081.840144     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780581081.844813     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780581081.856613     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780581081.856682     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780581081.856687     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780581081.856689     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-04 21:51:21.860113: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-04 21:51:24.716028: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
  "target_scalar": -141.71711568701727,
  "total_gradient_diag": [
    9105.143875898348,
    57.123649814928335
  ]
}
```

## BayesFilter Probe

```json
{
  "backend": "tensorflow_tensorflow_probability",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "resampling_flag": [
    true
  ],
  "scalar_additivity_probe": {
    "contract": "Direct scalar-gradient additivity check for post_update_log_likelihoods = pre_current_log_likelihoods + increment. These gradients use scalar objectives directly, not target-upstream VJPs through intermediate tensors.",
    "gradient_summaries": {
      "increment_mean": {
        "finite": true,
        "max_abs": 11886.758024308658,
        "shape": [
          2
        ],
        "sum": 11313.776500239524
      },
      "post_update_mean": {
        "finite": true,
        "max_abs": 9110.446610302024,
        "shape": [
          2
        ],
        "sum": 9167.436483591746
      },
      "pre_current_mean": {
        "finite": true,
        "max_abs": 1001.4592302010708,
        "shape": [
          2
        ],
        "sum": -720.785891138725
      },
      "sum_pre_current_plus_increment_mean": {
        "finite": true,
        "max_abs": 9110.446610302024,
        "shape": [
          2
        ],
        "sum": 9167.436483591746
      }
    },
    "gradient_tensors": {
      "increment_mean": [
        11886.758024308658,
        -572.9815240691337
      ],
      "post_update_mean": [
        9110.446610302024,
        56.9898732897215
      ],
      "pre_current_mean": [
        -1001.4592302010708,
        280.67333906234586
      ],
      "sum_pre_current_plus_increment_mean": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    "scalar_values": {
      "increment_mean": -0.7603288018870904,
      "post_update_mean": -141.71711568080488,
      "pre_current_mean": -140.9567868789178,
      "sum_pre_current_plus_increment_mean": -141.71711568080488
    }
  },
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
  ]
}
```

## Non-Implications

- No correctness claim is made for either implementation.
- No global smoothness-gradient agreement is concluded.
- No analytic Kalman-gradient agreement is concluded.
- No production readiness or public API readiness is concluded.
- No posterior correctness or nonlinear SSM validity is concluded.
