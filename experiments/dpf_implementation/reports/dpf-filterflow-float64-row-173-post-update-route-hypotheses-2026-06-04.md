# Result: Row 173 Post-Update Route Hypothesis Probe

## Decision

`filterflow_float64_row_173_post_update_h3_route_residual`

## Hypothesis Classification

`h3_post_update_route_residual`

post_update_delta reconstructs the observed residual but the component-sum reconstruction fails tolerance

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_post_update_h3_route_residual | h3_post_update_route_residual | none | single row/time post-update route probe; no correctness claim | instrument the post_update tape route to explain why its parameter-path adjoint is not equal to the component-sum route | correctness of either implementation, global smoothness-gradient agreement, production readiness |

## Veto Status

```json
{
  "all_vetoes_clear": true,
  "comparator_drift": false,
  "gradient_rows_finite": true,
  "path_boundary_clean": true,
  "resampling_flags_match": true,
  "scalar_delta": 6.2123888255882775e-09,
  "scalar_gate_pass": true,
  "value_additivity_pass": true
}
```

## Post-Update Route

```json
{
  "component_sum_delta": [
    3.473033814316295e-05,
    -5.653939183503098e-07
  ],
  "component_sum_pass": false,
  "component_sum_reconstruction_residual": [
    -5.302699673338225,
    0.13377595981291535
  ],
  "fields": [
    "post_update_log_likelihoods",
    "pre_current_log_likelihoods",
    "increment"
  ],
  "gradient_rows": {
    "increment": {
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
      "finite": true
    },
    "post_update_log_likelihoods": {
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
      "finite": true
    },
    "pre_current_log_likelihoods": {
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
      "finite": true
    }
  },
  "increment_delta": [
    -5.524705193238333e-05,
    -7.156052106438437e-07
  ],
  "max_abs_component_sum_reconstruction_residual": 5.302699673338225,
  "max_abs_post_update_reconstruction_residual": 0.0,
  "observed_residual": [
    5.302734403676368,
    -0.1337765252068337
  ],
  "post_update_delta": [
    5.302734403676368,
    -0.1337765252068337
  ],
  "post_update_pass": true,
  "post_update_reconstruction_residual": [
    0.0,
    0.0
  ],
  "pre_current_delta": [
    8.997739007554628e-05,
    1.5021129229353392e-07
  ],
  "status": "compared",
  "value_additivity_pass": true,
  "values": {
    "increment": {
      "bayesfilter": [
        -0.7603288018870904
      ],
      "filterflow": [
        -0.7603288017481669
      ],
      "max_abs_value_delta": 1.389235393389754e-10
    },
    "post_update_log_likelihoods": {
      "bayesfilter": [
        -141.71711568080488
      ],
      "filterflow": [
        -141.71711568701727
      ],
      "max_abs_value_delta": 6.2123888255882775e-09
    },
    "pre_current_log_likelihoods": {
      "bayesfilter": [
        -140.9567868789178
      ],
      "filterflow": [
        -140.9567868852691
      ],
      "max_abs_value_delta": 6.351314141284092e-09
    }
  },
  "within_side_additivity_gaps": {
    "bayesfilter": {
      "gap": [
        6.217248937900877e-15
      ],
      "max_abs_gap": 6.217248937900877e-15
    },
    "cross_impl_gap_delta": [
      -1.7763568394002505e-15
    ],
    "cross_impl_gap_delta_max_abs": 1.7763568394002505e-15,
    "filterflow": {
      "gap": [
        7.993605777301127e-15
      ],
      "max_abs_gap": 7.993605777301127e-15
    }
  }
}
```

## Scalar And Resampling Gates

```json
{
  "bayesfilter_resampling_flag": [
    true
  ],
  "bayesfilter_target_scalar": -141.71711568080488,
  "filterflow_resampling_flag": [
    true
  ],
  "filterflow_target_scalar": -141.71711568701727,
  "resampling_flags_match": true,
  "scalar_delta": 6.2123888255882775e-09,
  "scalar_gate_pass": true
}
```

## Input Manifest

```json
{
  "adjacent_boundary_baseline": {
    "comparator_fingerprint": null,
    "decision": "filterflow_float64_row_173_adjacent_boundary_reconstructed",
    "digest": "5c022fdd8026befd9eae9f1a11326cbcab6a08cd85801fe9f79d9c9722c76b1c",
    "field": "post_update_log_likelihoods",
    "filterflow_fingerprint_final": {
      "branch_ref_exists": true,
      "branch_string_status": "descriptive_only",
      "diff_digest": "12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126",
      "head_commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
      "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
      "path": "/home/chakwong/BayesFilter/.localsource/filterflow",
      "provenance_note": "Comparator identity is HEAD commit plus local-diff/status fingerprint; branch string is descriptive only.",
      "python_version": "Python 3.11.14",
      "status": "current_local_patched_checkout",
      "status_branch": "## bayesfilter-py311-float64-reference",
      "status_short": "",
      "symbolic_head": "bayesfilter-py311-float64-reference"
    },
    "filterflow_fingerprint_initial": {
      "branch_ref_exists": true,
      "branch_string_status": "descriptive_only",
      "diff_digest": "12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126",
      "head_commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
      "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
      "path": "/home/chakwong/BayesFilter/.localsource/filterflow",
      "provenance_note": "Comparator identity is HEAD commit plus local-diff/status fingerprint; branch string is descriptive only.",
      "python_version": "Python 3.11.14",
      "status": "current_local_patched_checkout",
      "status_branch": "## bayesfilter-py311-float64-reference",
      "status_short": "",
      "symbolic_head": "bayesfilter-py311-float64-reference"
    },
    "filterflow_status": {
      "branch": "bayesfilter-py311-float64-reference",
      "commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
      "dtype": "float64",
      "expected_commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
      "marker_path": "/home/chakwong/BayesFilter/.localsource/filterflow/BAYESFILTER_FLOAT64_REFERENCE.md",
      "path": "/home/chakwong/BayesFilter/.localsource/filterflow",
      "status_branch": "## bayesfilter-py311-float64-reference",
      "status_short": ""
    },
    "interpretation": "adjacent_boundary_residual_reconstructed_by_post_update_log_likelihoods",
    "observed_residual": [
      5.302734403676368,
      -0.1337765252068337
    ],
    "path": "experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_adjacent_boundary_2026-06-04.json",
    "post_update_delta": [
      5.302734403676368,
      -0.1337765252068337
    ],
    "status": "loaded"
  },
  "comparator_checkout": "/home/chakwong/BayesFilter/.localsource/filterflow",
  "comparator_fingerprint": {
    "branch_ref_exists": true,
    "branch_string_status": "descriptive_only",
    "diff_digest": "12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126",
    "head_commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
    "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
    "path": "/home/chakwong/BayesFilter/.localsource/filterflow",
    "provenance_note": "Comparator identity is HEAD commit plus local-diff/status fingerprint; branch string is descriptive only.",
    "python_version": "Python 3.11.14",
    "status": "current_local_patched_checkout",
    "status_branch": "## bayesfilter-py311-float64-reference",
    "status_short": "",
    "symbolic_head": "bayesfilter-py311-float64-reference"
  },
  "covariance_convention": {
    "observation_covariance": [
      [
        0.01
      ]
    ],
    "source": "executable FilterFlow constant-velocity smoothness helper",
    "transition_covariance": [
      [
        0.3333333333333333,
        0.5
      ],
      [
        0.5,
        1.0
      ]
    ]
  },
  "data_seed": 123,
  "dtype": "float64",
  "filter_seed": 1234,
  "initial_particles_checksum": -0.13359209100740663,
  "initial_particles_digest": "427cc02332c09254099f655d334bf54c38facef4a569e443f5a718e4b604b6aa",
  "observations_checksum": 24302.800267778097,
  "observations_digest": "b98dde488fdc17353e7fe90707bf0534b4215c19404c977225aa2dcdf01a8a87",
  "resampling_flag": [
    true
  ],
  "row_index": 173,
  "target_time_index": 93,
  "theta": [
    0.9710526315789474,
    0.9842105263157894
  ],
  "theta_digest": "3cca30e290aaf41d50268ed3745f384871fd5a8b6897081ed03982c316e42a78",
  "transport_matrix_digest": "9d854fe64efda760f3ca4cd440e91d42ab62deb7a6441602bae7153def985caf",
  "transport_matrix_shape": [
    1,
    50,
    50
  ]
}
```

## Comparator Fingerprint

```json
{
  "checkout_path": "/home/chakwong/BayesFilter/.localsource/filterflow",
  "entrypoint_hashes": {
    ".localsource/filterflow/filterflow/models/simple_linear_gaussian.py": {
      "mtime_ns": 1780422093570885005,
      "sha256": "9311335db9e1cad5e4e3ae98f2e8cc214d1b75fe604cf92fa803f116fb11d55a",
      "status": "present"
    },
    ".localsource/filterflow/filterflow/resampling/differentiable/biased.py": {
      "mtime_ns": 1780422178126866506,
      "sha256": "b44362f62d452cfc643693fdad8ca4fe05aef5ebba1549c2b83b95b2a4542752",
      "status": "present"
    },
    ".localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py": {
      "mtime_ns": 1780421981934905453,
      "sha256": "ddc9a2c1c64ccc2906fcf4be7d442b222c757076ead03b05e07b15a5de04b1e5",
      "status": "present"
    },
    ".localsource/filterflow/scripts/simple_linear_smoothness.py": {
      "mtime_ns": 1780422136894885694,
      "sha256": "cd182a4831fd1416153eedd264069dc6e49982317fc50f39c59452b4d2965a30",
      "status": "present"
    }
  },
  "fingerprint": {
    "branch_ref_exists": true,
    "branch_string_status": "descriptive_only",
    "diff_digest": "12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126",
    "head_commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
    "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
    "path": "/home/chakwong/BayesFilter/.localsource/filterflow",
    "provenance_note": "Comparator identity is HEAD commit plus local-diff/status fingerprint; branch string is descriptive only.",
    "python_version": "Python 3.11.14",
    "status": "current_local_patched_checkout",
    "status_branch": "## bayesfilter-py311-float64-reference",
    "status_short": "",
    "symbolic_head": "bayesfilter-py311-float64-reference"
  },
  "reference_status": {
    "branch": "bayesfilter-py311-float64-reference",
    "commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
    "dtype": "float64",
    "expected_commit": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
    "marker_path": "/home/chakwong/BayesFilter/.localsource/filterflow/BAYESFILTER_FLOAT64_REFERENCE.md",
    "path": "/home/chakwong/BayesFilter/.localsource/filterflow",
    "status_branch": "## bayesfilter-py311-float64-reference",
    "status_short": ""
  }
}
```

## Baseline Comparator Comparison

```json
{
  "baseline_artifact": "experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_adjacent_boundary_2026-06-04.json",
  "baseline_artifact_digest": "5c022fdd8026befd9eae9f1a11326cbcab6a08cd85801fe9f79d9c9722c76b1c",
  "entrypoint_hash_or_mtime_comparison": {
    "baseline_entrypoint_hashes": null,
    "current_entrypoint_hashes": {
      ".localsource/filterflow/filterflow/models/simple_linear_gaussian.py": {
        "mtime_ns": 1780422093570885005,
        "sha256": "9311335db9e1cad5e4e3ae98f2e8cc214d1b75fe604cf92fa803f116fb11d55a",
        "status": "present"
      },
      ".localsource/filterflow/filterflow/resampling/differentiable/biased.py": {
        "mtime_ns": 1780422178126866506,
        "sha256": "b44362f62d452cfc643693fdad8ca4fe05aef5ebba1549c2b83b95b2a4542752",
        "status": "present"
      },
      ".localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py": {
        "mtime_ns": 1780421981934905453,
        "sha256": "ddc9a2c1c64ccc2906fcf4be7d442b222c757076ead03b05e07b15a5de04b1e5",
        "status": "present"
      },
      ".localsource/filterflow/scripts/simple_linear_smoothness.py": {
        "mtime_ns": 1780422136894885694,
        "sha256": "cd182a4831fd1416153eedd264069dc6e49982317fc50f39c59452b4d2965a30",
        "status": "present"
      }
    },
    "equivalence_basis": "Prior adjacent-boundary artifact predates per-entrypoint hashes. Matching commit SHA, clean dirty-status summary, and diff digest are used as the recorded baseline-vs-current entrypoint identity control for tracked comparator files.",
    "pass": true,
    "status": "baseline_hashes_not_recorded"
  },
  "pass": true,
  "rows": {
    "checkout_path": {
      "baseline": "/home/chakwong/BayesFilter/.localsource/filterflow",
      "current": "/home/chakwong/BayesFilter/.localsource/filterflow",
      "pass": true
    },
    "commit_sha": {
      "baseline": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
      "current": "1e5fbc288c1c11fc18ba01bb4842832e2088b800",
      "pass": true
    },
    "diff_digest": {
      "baseline": "12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126",
      "current": "12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126",
      "pass": true
    },
    "dirty_status_summary": {
      "baseline": "",
      "current": "",
      "pass": true
    },
    "package_manifest_digest": {
      "baseline": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
      "current": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
      "pass": true
    },
    "python_version": {
      "baseline": "Python 3.11.14",
      "current": "Python 3.11.14",
      "pass": true
    },
    "status_branch": {
      "baseline": "## bayesfilter-py311-float64-reference",
      "current": "## bayesfilter-py311-float64-reference",
      "pass": true
    },
    "symbolic_head_or_branch_marker": {
      "baseline": "bayesfilter-py311-float64-reference",
      "current": "bayesfilter-py311-float64-reference",
      "pass": true
    }
  },
  "status": "compared"
}
```

## Boundary Mode Summary

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
        9110.449975340864,
        56.989788396916545
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta": [
        5.306099442515915,
        -0.13386141801179008
      ],
      "gradient_within_tolerance": false,
      "max_abs_gradient_delta": 5.306099442515915,
      "mode": "fresh_proposal_log_prob_filterflow_contract",
      "mode_description": "Evaluate proposal log probability with a freshly recomputed proposal distribution, matching executable FilterFlow OptimalProposalModel.loglikelihood.",
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

## Same-Tape State-Adjoint Summary

```json
{
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
}
```

## Run Manifest

```json
{
  "branch": "main",
  "command": "CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_post_update_route_probe_tf",
  "commit": "7ccb9c39883471c2d5ec2891cbf33b9ed436bada",
  "conda_env": "tf-gpu",
  "cpu_only": true,
  "cuda_visible_devices": "-1",
  "data_seed": 123,
  "dirty_state_summary": "M docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md\n M docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md\n M docs/references.bib\n M experiments/controlled_dpf_baseline/README.md\n?? .cache/\n?? .claude/\n?? .local_sources/\n?? .localenv/\n?? .localsource/\n?? AGENTS.md\n?? CLAUDE.md\n?? bayesfilter/highdim/\n?? docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-review-loop-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-review-loop-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-exact-arithmetic-continuation-debug-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-exact-arithmetic-continuation-debug-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-surface-window-coverage-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-debug-summary-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-result-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-boundary-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-92-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-94-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-gradient-discrepancy-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-0-19-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-100-119-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-120-139-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-140-159-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-160-179-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-180-199-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-20-39-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-200-219-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-220-239-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-240-259-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-260-279-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-280-299-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-300-319-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-320-339-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-340-359-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-360-379-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-380-399-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-40-59-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-60-79-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-80-99-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-py311-compat-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-py311-compat-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-citation-coverage-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-extraction-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-doc-patch-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-baseline-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-reference-test-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-student-comparison-context-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-bias-proxy-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-deferred-neural-path-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-differentiable-resampling-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-resampling-test-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-excluded-flow-risk-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-kernel-pff-exclusion-check-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-particle-flow-pfpf-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-differentiable-objective-gradient-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-downstream-evidence-requirements-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-objective-classification-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-benchmark-ladder-matrix-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-cpu-gpu-runtime-policy-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-seed-uncertainty-policy-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-benchmark-ladder-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-api-review-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-decision-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf7-final-audit-implementation-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-final-audit-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-handoff-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-sv-test-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-master-program-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-ladder-master-program-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ot-backend-governance-correction-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-backend-governance-correction-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p0-scope-and-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p0-scope-and-contract-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-structural-ar1-linear-mle-test-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ar1-linear-mle-test-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ssm-interface-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ssm-interface-result-2026-05-29.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase-subplans-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-addenda-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-claude-review-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-promotion-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-filtering-scalar-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-gradient-feasibility-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-mathdevmcp-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-octave-compatibility-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-octave-compatibility-result-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-reproducibility-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-result-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-claude-review-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-derivation-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-mathdevmcp-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claim-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-coverage-and-omission-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-proposition-proof-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-anchor-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-proposition-humanization-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-reader-comprehension-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-gradient-teaching-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-reader-panel-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-algorithm-choices-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-backward-snowball-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-citation-venue-metadata-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-claim-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-forward-snowball-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-gradient-derivation-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-omitted-paper-risk-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-reference-example-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-backward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-bayesfilter-translation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claim-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-code-crosswalk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-equation-by-equation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-fixed-branch-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-forward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-gradient-derivation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-fixed-branch-derivative-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-inventory-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section1-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section2-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section3-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section5-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-backward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-claim-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-eight-issue-control-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-equation-count-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-fixed-branch-gradient-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-forward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section1-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section2-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section3-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section5-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-inventory-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-finite-difference-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-fixed-branch-scalar-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-gradient-equation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-gradient-teaching-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-equation-and-size-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-merge-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-teachability-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-equation-to-specification-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-finite-difference-protocol-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-fixed-branch-implementation-ready-spec-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-full-algorithm-gap-register-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-implementation-readiness-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-implementation-specification-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integration-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-readable-orientation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-eleven-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-p22-preservation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-backward-snowball-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-chair-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-citation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-citation-venue-metadata-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-claim-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-forward-snowball-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-cleanup-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-implementation-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-omitted-paper-risk-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-source-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-claim-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-five-gap-closure-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-source-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-chemist-gap-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-human-facing-cleanup-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-implementation-gap-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-validation-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-chair-reader-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-equation-audit-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-implementation-readiness-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-notation-dimension-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-numerical-sanity-test-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-source-fidelity-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-submission-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-submission-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-algorithm-provenance-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-critical-equation-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-critical-equation-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-kr-preconditioning-jacobian-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-mass-normalizer-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-notation-shape-contract-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-proposition2-derivative-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-expansion-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-gradient-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-gradient-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-source-support-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-validation-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-standard-upgrade-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-scholarly-grounding-and-engineering-exposition-remediation-plan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-conclusion-and-panel-positioning-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-gradient-path-implementation-completeness-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-neighboring-method-comparison-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-opening-and-conceptual-spine-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-value-path-implementation-completeness-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-worked-example-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-audit-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-result-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-review-2026-05-27.md\n?? experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md\n?? experiments/dpf_implementation/\n?? tests/highdim/\n?? third_party/",
  "filter_seed": 1234,
  "gpu_devices_visible": [],
  "gpu_visibility_note": "CPU-only was intentionally forced before TensorFlow import; visible GPU list is informational only, not machine setup evidence.",
  "json_path": "experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_post_update_route_hypotheses_2026-06-04.json",
  "package_versions": {
    "tensorflow": "2.19.1",
    "tensorflow_probability": "0.25.0"
  },
  "plan_path": "docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-plan-2026-06-04.md",
  "pre_import_cuda_visible_devices": "-1",
  "python_version": "3.11.14",
  "report_path": "experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-post-update-route-hypotheses-2026-06-04.md",
  "result_path": "docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-result-2026-06-04.md",
  "wall_time_seconds": 240.06487579690292
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
- This post-update route probe is a row-173/time-93 difference audit only.
- No correctness claim is made for either implementation.
- No global smoothness-gradient correctness is concluded.
- No claim is made about other rows, times, horizons, parameter settings, or models.

## JSON Output

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_post_update_route_hypotheses_2026-06-04.json`
