# Result: Row 173 Time 93 Transport-Jacobian Probe

## Decision

`filterflow_float64_row_173_time_93_transport_jacobian_match`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_time_93_transport_jacobian_match | transport Jacobian rows match on recorded fields | none | single frozen row/time transport Jacobian probe | look outside transport Jacobian only if full-path residual remains | correctness of either implementation, analytic gradient correctness, posterior correctness, production readiness, public API readiness, HMC readiness, general nonlinear-SSM validity, DSGE/NAWM validation, monograph claim |

## Model Contract

```json
{
  "convergence_threshold": 1e-06,
  "dtype": "float64",
  "epsilon": 0.25,
  "max_iter": 500,
  "mesh_index": 173,
  "model": "filterflow_simple_linear_smoothness_constant_velocity_lgssm",
  "num_particles": 50,
  "scaling": 0.85,
  "target_time_index": 93,
  "theta": [
    0.9710526315789474,
    0.9842105263157894
  ]
}
```

## Comparison

```json
{
  "first_delta_over_tolerance": {
    "status": "no_delta",
    "tolerance": 0.0002
  },
  "interpretation": "transport_jacobian_matches_on_recorded_fields",
  "rows": {
    "alpha": {
      "finite": true,
      "left_max_abs": 0.3769078189121096,
      "max_abs_delta": 0.0,
      "right_max_abs": 0.3769078189121096,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "beta": {
      "finite": true,
      "left_max_abs": 0.3034856844641617,
      "max_abs_delta": 0.0,
      "right_max_abs": 0.3034856844641617,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "centered_particles": {
      "finite": true,
      "left_max_abs": 1.380629704942411,
      "max_abs_delta": 0.0,
      "right_max_abs": 1.380629704942411,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "cost_matrix": {
      "finite": true,
      "left_max_abs": 4.4108535244393385,
      "max_abs_delta": 0.0,
      "right_max_abs": 4.4108535244393385,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "grad_log_weights": {
      "finite": true,
      "left_max_abs": 1.1695816019011562,
      "max_abs_delta": 0.0,
      "right_max_abs": 1.1695816019011562,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "grad_particles": {
      "finite": true,
      "left_max_abs": 1.0756725353916639,
      "max_abs_delta": 3.3306690738754696e-16,
      "right_max_abs": 1.0756725353916639,
      "shape_match": true,
      "sum_delta": -8.928946991504372e-16
    },
    "iterations": {
      "finite": true,
      "left_max_abs": 79.0,
      "max_abs_delta": 0.0,
      "right_max_abs": 79.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "manual_grad_log_weights": {
      "finite": true,
      "left_max_abs": 1.1695816019011562,
      "max_abs_delta": 0.0,
      "right_max_abs": 1.1695816019011562,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "manual_grad_particles": {
      "finite": true,
      "left_max_abs": 1.0756725353916639,
      "max_abs_delta": 5.551115123125783e-16,
      "right_max_abs": 1.0756725353916639,
      "shape_match": true,
      "sum_delta": -4.886905767206851e-16
    },
    "manual_transport_matrix": {
      "finite": true,
      "left_max_abs": 0.3191070695509539,
      "max_abs_delta": 4.336808689942018e-19,
      "right_max_abs": 0.3191070695509539,
      "shape_match": true,
      "sum_delta": 4.575308021598207e-18
    },
    "scale": {
      "finite": true,
      "left_max_abs": 0.8171318665268777,
      "max_abs_delta": 0.0,
      "right_max_abs": 0.8171318665268777,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "scaled_particles": {
      "finite": true,
      "left_max_abs": 1.689604532020779,
      "max_abs_delta": 0.0,
      "right_max_abs": 1.689604532020779,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "transport_matrix": {
      "finite": true,
      "left_max_abs": 0.3191070695509539,
      "max_abs_delta": 0.0,
      "right_max_abs": 0.3191070695509539,
      "shape_match": true,
      "sum_delta": 0.0
    }
  },
  "status": "compared"
}
```

## Frozen Source

```json
{
  "log_weights_shape": [
    1,
    50
  ],
  "particles_shape": [
    1,
    50,
    2
  ],
  "source": "filterflow_row_173_time_93_vjp_subprocess",
  "target_time_index": 93,
  "theta": [
    0.9710526315789474,
    0.9842105263157894
  ],
  "transport_upstream_clip_fraction": 0.88,
  "upstream_shape": [
    1,
    50,
    50
  ]
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
  "gradient_summaries": {
    "custom_grad_log_weights": {
      "finite": true,
      "max_abs": 1.1695816019011562,
      "shape": [
        1,
        50
      ],
      "sum": 26.13115017061091
    },
    "custom_grad_particles": {
      "finite": true,
      "max_abs": 1.0756725353916639,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -7.598639330063592
    },
    "manual_grad_log_weights": {
      "finite": true,
      "max_abs": 1.1695816019011562,
      "shape": [
        1,
        50
      ],
      "sum": 26.13115017061091
    },
    "manual_grad_particles": {
      "finite": true,
      "max_abs": 1.0756725353916639,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -7.598639330063593
    }
  },
  "settings": {
    "convergence_threshold": 1e-06,
    "dtype": "float64",
    "epsilon": 0.25,
    "max_iter": 500,
    "num_particles": 50,
    "scaling": 0.85
  },
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-03 22:45:55.233684: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780497955.242683     269 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780497955.245460     269 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780497955.252230     269 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780497955.252275     269 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780497955.252279     269 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780497955.252281     269 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-03 22:45:55.254528: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-03 22:45:57.982542: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
  "summaries": {
    "alpha": {
      "finite": true,
      "max_abs": 0.3769078189121096,
      "shape": [
        1,
        50
      ],
      "sum": 5.974087413813816
    },
    "beta": {
      "finite": true,
      "max_abs": 0.3034856844641617,
      "shape": [
        1,
        50
      ],
      "sum": 5.812165742274698
    },
    "centered_particles": {
      "finite": true,
      "max_abs": 1.380629704942411,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.0089706847793423e-12
    },
    "cost_matrix": {
      "finite": true,
      "max_abs": 4.4108535244393385,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 1291.0628448285918
    },
    "custom_transport_matrix": {
      "finite": true,
      "max_abs": 0.3191070695509539,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 50.0
    },
    "diameter_value": {
      "finite": true,
      "max_abs": 0.5777994839447761,
      "shape": [
        1
      ],
      "sum": 0.5777994839447761
    },
    "iterations": {
      "finite": true,
      "max_abs": 79.0,
      "shape": [],
      "sum": 79.0
    },
    "manual_transport_matrix": {
      "finite": true,
      "max_abs": 0.3191070695509539,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 50.0
    },
    "scale": {
      "finite": true,
      "max_abs": 0.8171318665268777,
      "shape": [
        1,
        1,
        1
      ],
      "sum": 0.8171318665268777
    },
    "scaled_particles": {
      "finite": true,
      "max_abs": 1.689604532020779,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.2351049002989889e-12
    }
  }
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
  "gradient_summaries": {
    "manual_grad_log_weights": {
      "finite": true,
      "max_abs": 1.1695816019011562,
      "shape": [
        1,
        50
      ],
      "sum": 26.13115017061091
    },
    "manual_grad_particles": {
      "finite": true,
      "max_abs": 1.0756725353916639,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -7.598639330063592
    }
  },
  "settings": {
    "convergence_threshold": 1e-06,
    "dtype": "float64",
    "epsilon": 0.25,
    "max_iter": 500,
    "num_particles": 50,
    "scaling": 0.85
  },
  "status": "executed",
  "stderr_excerpt": "",
  "summaries": {
    "alpha": {
      "finite": true,
      "max_abs": 0.3769078189121096,
      "shape": [
        1,
        50
      ],
      "sum": 5.974087413813816
    },
    "beta": {
      "finite": true,
      "max_abs": 0.3034856844641617,
      "shape": [
        1,
        50
      ],
      "sum": 5.812165742274698
    },
    "centered_particles": {
      "finite": true,
      "max_abs": 1.380629704942411,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.0089706847793423e-12
    },
    "cost_matrix": {
      "finite": true,
      "max_abs": 4.4108535244393385,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 1291.0628448285918
    },
    "iterations": {
      "finite": true,
      "max_abs": 79.0,
      "shape": [],
      "sum": 79.0
    },
    "scale": {
      "finite": true,
      "max_abs": 0.8171318665268777,
      "shape": [
        1,
        1,
        1
      ],
      "sum": 0.8171318665268777
    },
    "scaled_particles": {
      "finite": true,
      "max_abs": 1.689604532020779,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -1.2351049002989889e-12
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 0.3191070695509539,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 50.0
    }
  }
}
```

## Verification

- CPU-only manifest recorded `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- This artifact is a difference audit only.