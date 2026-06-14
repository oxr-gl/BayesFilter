# Result: FilterFlow Float64 Row 173 Full-Path Gradient Scan

## Decision

`filterflow_float64_row_173_full_path_scan_gradient_residual_localized`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_full_path_scan_gradient_residual_localized | first gradient residual: {'status': 'failure', 'time_index': 93, 'scalar_delta': 6.2123888255882775e-09, 'max_abs_gradient_delta': 5.302734403676368, 'relative_gradient_delta': 0.0005823888645749906, 'gradient_delta': [5.302734403676368, -0.1337765252068337], 'filterflow_gradient_diag': [9105.143875898348, 57.123649814928335], 'bayesfilter_gradient_diag': [9110.446610302024, 56.9898732897215], 'resampling_flag': [True], 'transport_status': 'computed_with_clipped_upstream_gradient_filterflow_all_rows'} | scalar path stayed aligned before residual | single mesh row only; no correctness claim | run a VJP decomposition at the first true residual time | correctness of either implementation, analytic gradient correctness, production readiness |

## Model Contract

| Key | Value |
| --- | --- |
| `model` | `filterflow_simple_linear_smoothness_constant_velocity_lgssm` |
| `mesh_index` | `173` |
| `theta` | `[0.9710526315789474, 0.9842105263157894]` |
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
  "final_row": {
    "bayesfilter_gradient_diag": [
      7025.174608954654,
      713.4652966764394
    ],
    "bayesfilter_gradient_max_abs": 7025.174608954654,
    "filterflow_gradient_diag": [
      7019.871884959112,
      713.5990729926672
    ],
    "filterflow_gradient_max_abs": 7019.871884959112,
    "gradient_delta": [
      5.302723995541783,
      -0.13377631622779518
    ],
    "gradient_within_tolerance": false,
    "max_abs_gradient_delta": 5.302723995541783,
    "relative_gradient_delta": 0.0007553875743663474,
    "resampling_flag": [
      true
    ],
    "scalar_delta": 7.408061719615944e-09,
    "scalar_within_tolerance": true,
    "time_index": 99,
    "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
  },
  "finite_values": true,
  "first_gradient_failure": {
    "bayesfilter_gradient_diag": [
      9110.446610302024,
      56.9898732897215
    ],
    "filterflow_gradient_diag": [
      9105.143875898348,
      57.123649814928335
    ],
    "gradient_delta": [
      5.302734403676368,
      -0.1337765252068337
    ],
    "max_abs_gradient_delta": 5.302734403676368,
    "relative_gradient_delta": 0.0005823888645749906,
    "resampling_flag": [
      true
    ],
    "scalar_delta": 6.2123888255882775e-09,
    "status": "failure",
    "time_index": 93,
    "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
  },
  "first_scalar_failure": {
    "status": "no_failure"
  },
  "interpretation": "first_true_full_path_gradient_residual_time_93",
  "sample_rows": [
    {
      "bayesfilter_gradient_diag": [
        0.008924445612040184,
        0.0
      ],
      "bayesfilter_gradient_max_abs": 0.008924445612040184,
      "filterflow_gradient_diag": [
        0.008924445612040184,
        5.795395272864551e-20
      ],
      "filterflow_gradient_max_abs": 0.008924445612040184,
      "gradient_delta": [
        0.0,
        -5.795395272864551e-20
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 5.795395272864551e-20,
      "relative_gradient_delta": 5.795395272864551e-20,
      "resampling_flag": [
        false
      ],
      "scalar_delta": 0.0,
      "scalar_within_tolerance": true,
      "time_index": 0,
      "transport_status": "not_triggered"
    },
    {
      "bayesfilter_gradient_diag": [
        -8.844738225000961,
        -0.010466566493996424
      ],
      "bayesfilter_gradient_max_abs": 8.844738225000961,
      "filterflow_gradient_diag": [
        -8.844738225016581,
        -0.010466566494080693
      ],
      "filterflow_gradient_max_abs": 8.844738225016581,
      "gradient_delta": [
        1.5619505688846402e-11,
        8.426939701600134e-14
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 1.5619505688846402e-11,
      "relative_gradient_delta": 1.7659658535362838e-12,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.8406609569865395e-11,
      "scalar_within_tolerance": true,
      "time_index": 1,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        -6.332502147276955,
        -0.9347283384324467
      ],
      "bayesfilter_gradient_max_abs": 6.332502147276955,
      "filterflow_gradient_diag": [
        -6.3325021473024945,
        -0.9347283384311086
      ],
      "filterflow_gradient_max_abs": 6.3325021473024945,
      "gradient_delta": [
        2.55395704584771e-11,
        -1.3381518115807012e-12
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 2.55395704584771e-11,
      "relative_gradient_delta": 4.0330930593298564e-12,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.5511147921642987e-11,
      "scalar_within_tolerance": true,
      "time_index": 2,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        -46.85485326359639,
        50.73284126858788
      ],
      "bayesfilter_gradient_max_abs": 50.73284126858788,
      "filterflow_gradient_diag": [
        -46.8548532635973,
        50.732841268587705
      ],
      "filterflow_gradient_max_abs": 50.732841268587705,
      "gradient_delta": [
        9.094947017729282e-13,
        1.7763568394002505e-13
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 9.094947017729282e-13,
      "relative_gradient_delta": 1.792713908842438e-14,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 2.2442492308982764e-11,
      "scalar_within_tolerance": true,
      "time_index": 3,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        7.268058775833268,
        -7.900398612096756
      ],
      "bayesfilter_gradient_max_abs": 7.900398612096756,
      "filterflow_gradient_diag": [
        7.268058776233275,
        -7.900398612576443
      ],
      "filterflow_gradient_max_abs": 7.900398612576443,
      "gradient_delta": [
        -4.00007138523506e-10,
        4.796865127332239e-10
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 4.796865127332239e-10,
      "relative_gradient_delta": 6.07167481359261e-11,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 2.779998453661392e-11,
      "scalar_within_tolerance": true,
      "time_index": 4,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        172.79510848644207,
        -24.17772558607598
      ],
      "bayesfilter_gradient_max_abs": 172.79510848644207,
      "filterflow_gradient_diag": [
        172.7951085450445,
        -24.177725600452597
      ],
      "filterflow_gradient_max_abs": 172.7951085450445,
      "gradient_delta": [
        -5.860243845745572e-08,
        1.4376617230027477e-08
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 5.860243845745572e-08,
      "relative_gradient_delta": 3.3914408197601925e-10,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.581402089977928e-11,
      "scalar_within_tolerance": true,
      "time_index": 9,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        3224.3267645592096,
        -184.3032449332778
      ],
      "bayesfilter_gradient_max_abs": 3224.3267645592096,
      "filterflow_gradient_diag": [
        3224.3267886205685,
        -184.3032493825567
      ],
      "filterflow_gradient_max_abs": 3224.3267886205685,
      "gradient_delta": [
        -2.4061358999460936e-05,
        4.4492788902061875e-06
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 2.4061358999460936e-05,
      "relative_gradient_delta": 7.462444279649107e-09,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 5.035900585426134e-10,
      "scalar_within_tolerance": true,
      "time_index": 24,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        2732.589436113304,
        -125.18962097180408
      ],
      "bayesfilter_gradient_max_abs": 2732.589436113304,
      "filterflow_gradient_diag": [
        2732.5897170034305,
        -125.18963042931237
      ],
      "filterflow_gradient_max_abs": 2732.5897170034305,
      "gradient_delta": [
        -0.00028089012630516663,
        9.457508298282846e-06
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 0.00028089012630516663,
      "relative_gradient_delta": 1.0279264558354262e-07,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 2.842170943040401e-14,
      "scalar_within_tolerance": true,
      "time_index": 49,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        762.8643246802055,
        -97.82621248290687
      ],
      "bayesfilter_gradient_max_abs": 762.8643246802055,
      "filterflow_gradient_diag": [
        762.8642912801339,
        -97.82621259386863
      ],
      "filterflow_gradient_max_abs": 762.8642912801339,
      "gradient_delta": [
        3.340007162933034e-05,
        1.109617642214289e-07
      ],
      "gradient_within_tolerance": true,
      "max_abs_gradient_delta": 3.340007162933034e-05,
      "relative_gradient_delta": 4.3782455164185145e-08,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 9.252687505068025e-10,
      "scalar_within_tolerance": true,
      "time_index": 74,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ],
      "bayesfilter_gradient_max_abs": 9110.446610302024,
      "filterflow_gradient_diag": [
        9105.143875898348,
        57.123649814928335
      ],
      "filterflow_gradient_max_abs": 9105.143875898348,
      "gradient_delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.302734403676368,
      "relative_gradient_delta": 0.0005823888645749906,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.2123888255882775e-09,
      "scalar_within_tolerance": true,
      "time_index": 93,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        8383.773392155563,
        207.4167537924887
      ],
      "bayesfilter_gradient_max_abs": 8383.773392155563,
      "filterflow_gradient_diag": [
        8378.470661213249,
        207.55053001782872
      ],
      "filterflow_gradient_max_abs": 8378.470661213249,
      "gradient_delta": [
        5.302730942314156,
        -0.13377622534002853
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.302730942314156,
      "relative_gradient_delta": 0.0006328996253292711,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 6.9354371134977555e-09,
      "scalar_within_tolerance": true,
      "time_index": 94,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        3930.0078873197845,
        727.426714952718
      ],
      "bayesfilter_gradient_max_abs": 3930.0078873197845,
      "filterflow_gradient_diag": [
        3924.7051504549877,
        727.5604915151332
      ],
      "filterflow_gradient_max_abs": 3924.7051504549877,
      "gradient_delta": [
        5.3027368647967705,
        -0.13377656241516434
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.3027368647967705,
      "relative_gradient_delta": 0.001351117258880461,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 8.690761887919507e-09,
      "scalar_within_tolerance": true,
      "time_index": 98,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "bayesfilter_gradient_diag": [
        7025.174608954654,
        713.4652966764394
      ],
      "bayesfilter_gradient_max_abs": 7025.174608954654,
      "filterflow_gradient_diag": [
        7019.871884959112,
        713.5990729926672
      ],
      "filterflow_gradient_max_abs": 7019.871884959112,
      "gradient_delta": [
        5.302723995541783,
        -0.13377631622779518
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.302723995541783,
      "relative_gradient_delta": 0.0007553875743663474,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 7.408061719615944e-09,
      "scalar_within_tolerance": true,
      "time_index": 99,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    }
  ],
  "status": "compared"
}
```

## FilterFlow Scan

```json
{
  "backend": "executable_filterflow_subprocess",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "final_gradient_diag": [
    7019.871884959112,
    713.5990729926672
  ],
  "final_mean_log_likelihood": -154.67994172886134,
  "finite_values": true,
  "first_rows": [
    {
      "cumulative_mean_log_likelihood": -2.004090374815232,
      "ess_before_resampling": [
        49.99999999999999
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        0.008924445612040184,
        5.795395272864551e-20
      ],
      "gradient_matrix": [
        [
          0.008924445612040184,
          0.00016288542399612796
        ],
        [
          4.241522690094141e-19,
          5.795395272864551e-20
        ]
      ],
      "resampling_flag": [
        false
      ],
      "time_index": 0
    },
    {
      "cumulative_mean_log_likelihood": -17.2005020674398,
      "ess_before_resampling": [
        49.93670594480325
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -8.844738225016581,
        -0.010466566494080693
      ],
      "gradient_matrix": [
        [
          -8.844738225016581,
          -8.695718557812015
        ],
        [
          -0.011382827205209022,
          -0.010466566494080693
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 1
    },
    {
      "cumulative_mean_log_likelihood": -18.089399104816973,
      "ess_before_resampling": [
        5.942671242253685
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -6.3325021473024945,
        -0.9347283384311086
      ],
      "gradient_matrix": [
        [
          -6.3325021473024945,
          -2.420121832653158
        ],
        [
          -0.7283681282184683,
          -0.9347283384311086
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 2
    },
    {
      "cumulative_mean_log_likelihood": -20.756685012298828,
      "ess_before_resampling": [
        44.22504748606863
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -46.8548532635973,
        50.732841268587705
      ],
      "gradient_matrix": [
        [
          -46.8548532635973,
          -59.40002611648325
        ],
        [
          38.47277080156124,
          50.732841268587705
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 3
    },
    {
      "cumulative_mean_log_likelihood": -21.827449488050206,
      "ess_before_resampling": [
        22.4243293073044
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        7.268058776233275,
        -7.900398612576443
      ],
      "gradient_matrix": [
        [
          7.268058776233275,
          12.412104246274685
        ],
        [
          -9.347910409571414,
          -7.900398612576443
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 4
    }
  ],
  "last_row": {
    "cumulative_mean_log_likelihood": -154.67994172886134,
    "ess_before_resampling": [
      16.836798718761134
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      7019.871884959112,
      713.5990729926672
    ],
    "gradient_matrix": [
      [
        7019.871884959112,
        119.37856505492687
      ],
      [
        12089.784897206187,
        713.5990729926672
      ]
    ],
    "resampling_flag": [
      true
    ],
    "time_index": 99
  },
  "package_versions": {
    "numpy": "1.26.4",
    "python": "3.11.14",
    "tensorflow": "2.19.1"
  },
  "scan_contract": "single_persistent_tape_full_path_cumulative_gradients",
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
    "optimal_proposal": true,
    "resampling_correction": false,
    "resampling_neff": 0.9999,
    "scaling": 0.85,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ]
  },
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-03 21:05:33.210930: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780491933.224920     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780491933.229663     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780491933.241206     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780491933.241250     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780491933.241255     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780491933.241256     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-03 21:05:33.244677: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-03 21:05:35.721303: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n"
}
```

## BayesFilter Scan

```json
{
  "backend": "tensorflow_tensorflow_probability",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "final_gradient_diag": [
    7025.174608954654,
    713.4652966764394
  ],
  "final_mean_log_likelihood": -154.67994172145328,
  "finite_values": true,
  "first_rows": [
    {
      "cumulative_mean_log_likelihood": -2.004090374815232,
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        0.008924445612040184,
        0.0
      ],
      "gradient_max_abs": 0.008924445612040184,
      "log_likelihood_increment": [
        -2.004090374815232
      ],
      "log_neff_before_resampling": [
        3.912023005428146
      ],
      "max_column_residual": 0.0,
      "max_row_residual": 0.0,
      "resampling_flag": [
        false
      ],
      "time_index": 0,
      "transport_status": "not_triggered"
    },
    {
      "cumulative_mean_log_likelihood": -17.200502067421393,
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -8.844738225000961,
        -0.010466566493996424
      ],
      "gradient_max_abs": 8.844738225000961,
      "log_likelihood_increment": [
        -15.196411692606162
      ],
      "log_neff_before_resampling": [
        3.910756322419912
      ],
      "max_column_residual": 5.551115123125783e-16,
      "max_row_residual": 9.762526802292726e-06,
      "resampling_flag": [
        true
      ],
      "time_index": 1,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "cumulative_mean_log_likelihood": -18.089399104801462,
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -6.332502147276955,
        -0.9347283384324467
      ],
      "gradient_max_abs": 6.332502147276955,
      "log_likelihood_increment": [
        -0.8888970373800693
      ],
      "log_neff_before_resampling": [
        1.7821587363699605
      ],
      "max_column_residual": 3.552713678800501e-15,
      "max_row_residual": 4.948488572020793e-06,
      "resampling_flag": [
        true
      ],
      "time_index": 2,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "cumulative_mean_log_likelihood": -20.756685012276385,
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -46.85485326359639,
        50.73284126858788
      ],
      "gradient_max_abs": 50.73284126858788,
      "log_likelihood_increment": [
        -2.6672859074749233
      ],
      "log_neff_before_resampling": [
        3.789291313781822
      ],
      "max_column_residual": 8.881784197001252e-16,
      "max_row_residual": 1.0043286847949418e-05,
      "resampling_flag": [
        true
      ],
      "time_index": 3,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    },
    {
      "cumulative_mean_log_likelihood": -21.827449488022406,
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        7.268058775833268,
        -7.900398612096756
      ],
      "gradient_max_abs": 7.900398612096756,
      "log_likelihood_increment": [
        -1.0707644757460217
      ],
      "log_neff_before_resampling": [
        3.110146499237527
      ],
      "max_column_residual": 1.7763568394002505e-15,
      "max_row_residual": 8.557021202060255e-06,
      "resampling_flag": [
        true
      ],
      "time_index": 4,
      "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
    }
  ],
  "last_row": {
    "cumulative_mean_log_likelihood": -154.67994172145328,
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      7025.174608954654,
      713.4652966764394
    ],
    "gradient_max_abs": 7025.174608954654,
    "log_likelihood_increment": [
      -1.0760734770445781
    ],
    "log_neff_before_resampling": [
      2.8235668913994716
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 5.1938332349399374e-06,
    "resampling_flag": [
      true
    ],
    "time_index": 99,
    "transport_status": "computed_with_clipped_upstream_gradient_filterflow_all_rows"
  },
  "scan_contract": "single_persistent_tape_full_path_cumulative_gradients",
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
    "optimal_proposal": true,
    "resampling_correction": false,
    "resampling_neff": 0.9999,
    "scaling": 0.85,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ]
  },
  "status": "executed"
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
- Finite gradients alone are smoke evidence only.
