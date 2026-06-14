# Result: FilterFlow Float64 Row 173 VJP Decomposition

## Decision

`filterflow_float64_row_173_vjp_total_gradient_match`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_vjp_total_gradient_match | time-1 scalar and total gradient match; intermediate VJP deltas are explanatory graph-structure diagnostics | none | single row and single time index; no correctness claim | run a same-contract full-path cumulative gradient scan to find the first true residual time | correctness of either implementation, analytic gradient correctness, production readiness |

## Model Contract

| Key | Value |
| --- | --- |
| `model` | `filterflow_simple_linear_smoothness_constant_velocity_lgssm` |
| `mesh_index` | `173` |
| `theta` | `[0.9710526315789474, 0.9842105263157894]` |
| `target_time_index` | `1` |
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
  "first_gradient_delta_over_tolerance": {
    "field": "pre_particles",
    "row": {
      "bayesfilter_max_abs": 3.6201043637939385,
      "filterflow_max_abs": 1.129670326767506,
      "finite": true,
      "max_abs_delta": 3.6159617690863133,
      "shape_match": true,
      "sum_delta": 4.733570722400016
    },
    "status": "delta",
    "tolerance": 0.0002
  },
  "first_value_delta_over_tolerance": {
    "status": "no_delta",
    "tolerance": 5e-08
  },
  "gradient_deltas": {
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
    "normalized": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "observation_ll": {
      "bayesfilter_max_abs": 0.3156947073865741,
      "filterflow_max_abs": 0.31569470738635247,
      "finite": true,
      "max_abs_delta": 2.216560268664125e-13,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "post_log_weights": {
      "bayesfilter_max_abs": 0.3156947073865741,
      "filterflow_max_abs": 0.31569470738635247,
      "finite": true,
      "max_abs_delta": 2.216560268664125e-13,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "post_particles": {
      "bayesfilter_max_abs": 2.6452767160877118,
      "filterflow_max_abs": 2.645276716087951,
      "finite": true,
      "max_abs_delta": 5.030420524576584e-13,
      "shape_match": true,
      "sum_delta": 1.3223200312495464e-11
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
    "pre_log_weights": {
      "bayesfilter_max_abs": 0.44756953732379734,
      "filterflow_max_abs": 0.4475695373244526,
      "finite": true,
      "max_abs_delta": 6.552536291337674e-13,
      "shape_match": true,
      "sum_delta": 1.901412360894028e-11
    },
    "pre_particles": {
      "bayesfilter_max_abs": 3.6201043637939385,
      "filterflow_max_abs": 1.129670326767506,
      "finite": true,
      "max_abs_delta": 3.6159617690863133,
      "shape_match": true,
      "sum_delta": 4.733570722400016
    },
    "proposal_ll": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 0.31569470738635247,
      "finite": true,
      "max_abs_delta": 0.31569470738635247,
      "shape_match": true,
      "sum_delta": 1.0
    },
    "proposal_mean": {
      "bayesfilter_max_abs": 2.2278338047405373,
      "filterflow_max_abs": 0.0,
      "finite": true,
      "max_abs_delta": 2.2278338047405373,
      "shape_match": true,
      "sum_delta": 6.0755864124953645
    },
    "proposed_particles": {
      "bayesfilter_max_abs": 2.2278338047405373,
      "filterflow_max_abs": 3.885780586188048e-15,
      "finite": true,
      "max_abs_delta": 2.2278338047405413,
      "shape_match": true,
      "sum_delta": 6.075586412495374
    },
    "transition_ll": {
      "bayesfilter_max_abs": 0.3156947073865741,
      "filterflow_max_abs": 0.31569470738635247,
      "finite": true,
      "max_abs_delta": 2.216560268664125e-13,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "transport_matrix": {
      "bayesfilter_max_abs": 0.0,
      "filterflow_max_abs": 9.881276925667308,
      "finite": true,
      "max_abs_delta": 9.881276925667308,
      "shape_match": true,
      "sum_delta": 1137.9047077611326
    },
    "unnormalized": {
      "bayesfilter_max_abs": 0.3156947073865741,
      "filterflow_max_abs": 0.31569470738635247,
      "finite": true,
      "max_abs_delta": 2.216560268664125e-13,
      "shape_match": true,
      "sum_delta": 0.0
    }
  },
  "interpretation": "first_vjp_difference_field_pre_particles",
  "max_abs_total_gradient_delta": 1.5619505688846402e-11,
  "resampling_flags_match": true,
  "scalar_delta": 1.8406609569865395e-11,
  "status": "compared",
  "total_gradient_delta": [
    1.5619505688846402e-11,
    8.426939701600134e-14
  ],
  "transport_upstream_clip_fraction_delta": 0.12,
  "value_deltas": {
    "increment": {
      "bayesfilter_max_abs": 15.196411692606162,
      "filterflow_max_abs": 15.196411692624567,
      "finite": true,
      "max_abs_delta": 1.8404833213025995e-11,
      "shape_match": true,
      "sum_delta": 1.8404833213025995e-11
    },
    "log_ess": {
      "bayesfilter_max_abs": 3.910756322419912,
      "filterflow_max_abs": 3.9107563224199113,
      "finite": true,
      "max_abs_delta": 4.440892098500626e-16,
      "shape_match": true,
      "sum_delta": 4.440892098500626e-16
    },
    "normalized": {
      "bayesfilter_max_abs": 17.358632204072613,
      "filterflow_max_abs": 17.358632204009652,
      "finite": true,
      "max_abs_delta": 6.296119181570248e-11,
      "shape_match": true,
      "sum_delta": 1.0130634109373204e-09
    },
    "observation_ll": {
      "bayesfilter_max_abs": 2.7527274464026354,
      "filterflow_max_abs": 2.7527274463997276,
      "finite": true,
      "max_abs_delta": 2.90789614609821e-12,
      "shape_match": true,
      "sum_delta": 2.1458390619955026e-12
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
      "bayesfilter_max_abs": 2.3362666995840704,
      "filterflow_max_abs": 2.33626669958171,
      "finite": true,
      "max_abs_delta": 2.360334150353083e-12,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "post_update_log_likelihoods": {
      "bayesfilter_max_abs": 17.200502067421393,
      "filterflow_max_abs": 17.2005020674398,
      "finite": true,
      "max_abs_delta": 1.8406609569865395e-11,
      "shape_match": true,
      "sum_delta": 1.8406609569865395e-11
    },
    "post_update_log_weights": {
      "bayesfilter_max_abs": 17.358632204072613,
      "filterflow_max_abs": 17.358632204009652,
      "finite": true,
      "max_abs_delta": 6.296119181570248e-11,
      "shape_match": true,
      "sum_delta": 1.0130634109373204e-09
    },
    "pre_log_weights": {
      "bayesfilter_max_abs": 3.9833688267575242,
      "filterflow_max_abs": 3.9833688267575242,
      "finite": true,
      "max_abs_delta": 3.552713678800501e-15,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "pre_particles": {
      "bayesfilter_max_abs": 2.5933950054045614,
      "filterflow_max_abs": 2.5933950054045614,
      "finite": true,
      "max_abs_delta": 0.0,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "proposal_ll": {
      "bayesfilter_max_abs": 5.896490813727095,
      "filterflow_max_abs": 5.896490813727095,
      "finite": true,
      "max_abs_delta": 2.6645352591003757e-15,
      "shape_match": true,
      "sum_delta": 3.9968028886505635e-15
    },
    "proposal_mean": {
      "bayesfilter_max_abs": 4.12649214562547,
      "filterflow_max_abs": 4.126492145622718,
      "finite": true,
      "max_abs_delta": 2.751576744230988e-12,
      "shape_match": true,
      "sum_delta": 2.842170943040401e-14
    },
    "proposed_particles": {
      "bayesfilter_max_abs": 5.002437644950284,
      "filterflow_max_abs": 5.002437644951584,
      "finite": true,
      "max_abs_delta": 2.751576744230988e-12,
      "shape_match": true,
      "sum_delta": 2.842170943040401e-14
    },
    "transition_ll": {
      "bayesfilter_max_abs": 32.49679430969144,
      "filterflow_max_abs": 32.49679430965263,
      "finite": true,
      "max_abs_delta": 4.3375081304475316e-11,
      "shape_match": true,
      "sum_delta": 9.072209650184959e-11
    },
    "transport_matrix": {
      "bayesfilter_max_abs": 0.2579538057358776,
      "filterflow_max_abs": 0.25795380573572435,
      "finite": true,
      "max_abs_delta": 1.5326628854950286e-13,
      "shape_match": true,
      "sum_delta": 0.0
    },
    "unnormalized": {
      "bayesfilter_max_abs": 32.555043896678775,
      "filterflow_max_abs": 32.55504389663422,
      "finite": true,
      "max_abs_delta": 4.455813495951588e-11,
      "shape_match": true,
      "sum_delta": 9.276845958083868e-11
    }
  }
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
  "gradient_summaries": {
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
      "max_abs": 0.31569470738635247,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 0.31569470738635247,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_particles": {
      "finite": true,
      "max_abs": 2.645276716087951,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 17.158380309962997
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
    "pre_log_weights": {
      "finite": true,
      "max_abs": 0.4475695373244526,
      "shape": [
        1,
        50
      ],
      "sum": -8.400112486435889
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 1.129670326767506,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 12.161952699789518
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 0.31569470738635247,
      "shape": [
        1,
        50
      ],
      "sum": -1.0
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
      "max_abs": 3.885780586188048e-15,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 9.603560421681565e-15
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 0.31569470738635247,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 9.881276925667308,
      "shape": [
        1,
        50,
        50
      ],
      "sum": -1137.9047077611326
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 0.31569470738635247,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    }
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
    "target_time_index": 1,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ],
    "transport_backward": "FilterFlow custom gradient clips d_transport to [-1,1]"
  },
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-03 20:41:33.568517: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780490493.579882     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780490493.584174     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780490493.595038     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780490493.595104     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780490493.595109     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780490493.595110     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-03 20:41:33.598458: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-03 20:41:36.044559: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
  "target_scalar": -17.2005020674398,
  "total_gradient_diag": [
    -8.844738225016581,
    -0.010466566494080693
  ],
  "transport_upstream_clip_fraction": 0.12,
  "value_summaries": {
    "increment": {
      "finite": true,
      "max_abs": 15.196411692624567,
      "shape": [
        1
      ],
      "sum": -15.196411692624567
    },
    "log_ess": {
      "finite": true,
      "max_abs": 3.9107563224199113,
      "shape": [
        1
      ],
      "sum": 3.9107563224199113
    },
    "normalized": {
      "finite": true,
      "max_abs": 17.358632204009652,
      "shape": [
        1,
        50
      ],
      "sum": -420.722152124421
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 2.7527274463997276,
      "shape": [
        1,
        50
      ],
      "sum": 28.22468017399411
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
      "max_abs": 2.33626669958171,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -132.12083840320508
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 17.2005020674398,
      "shape": [
        1
      ],
      "sum": -17.2005020674398
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 17.358632204009652,
      "shape": [
        1,
        50
      ],
      "sum": -420.722152124421
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 3.9833688267575242,
      "shape": [
        1,
        50
      ],
      "sum": -195.63256651599147
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 2.5933950054045614,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -132.2181669047356
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 5.896490813727095,
      "shape": [
        1,
        50
      ],
      "sum": -3.2793767008897037
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 4.126492145622718,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 229.80558036397272
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 5.002437644951584,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 222.54040960851978
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 32.49679430965263,
      "shape": [
        1,
        50
      ],
      "sum": -1016.4456433591258
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 0.25795380573572435,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 50.0
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 32.55504389663422,
      "shape": [
        1,
        50
      ],
      "sum": -1180.5427367556492
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
  "gradient_summaries": {
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
      "max_abs": 0.3156947073865741,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_log_weights": {
      "finite": true,
      "max_abs": 0.3156947073865741,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "post_particles": {
      "finite": true,
      "max_abs": 2.6452767160877118,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 17.158380309949774
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
    "pre_log_weights": {
      "finite": true,
      "max_abs": 0.44756953732379734,
      "shape": [
        1,
        50
      ],
      "sum": -8.400112486416875
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 3.6201043637939385,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 16.895523422189534
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
    "proposal_mean": {
      "finite": true,
      "max_abs": 2.2278338047405373,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -6.0755864124953645
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 2.2278338047405373,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -6.0755864124953645
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 0.3156947073865741,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 0.0,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 0.0
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 0.3156947073865741,
      "shape": [
        1,
        50
      ],
      "sum": 1.0
    }
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
    "target_time_index": 1,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ],
    "transport_backward": "FilterFlow custom gradient clips d_transport to [-1,1]"
  },
  "status": "executed",
  "stderr_excerpt": "",
  "target_scalar": -17.200502067421393,
  "total_gradient_diag": [
    -8.844738225000961,
    -0.010466566493996424
  ],
  "transport_upstream_clip_fraction": 0.0,
  "value_summaries": {
    "increment": {
      "finite": true,
      "max_abs": 15.196411692606162,
      "shape": [
        1
      ],
      "sum": -15.196411692606162
    },
    "log_ess": {
      "finite": true,
      "max_abs": 3.910756322419912,
      "shape": [
        1
      ],
      "sum": 3.910756322419912
    },
    "normalized": {
      "finite": true,
      "max_abs": 17.358632204072613,
      "shape": [
        1,
        50
      ],
      "sum": -420.72215212543404
    },
    "observation_ll": {
      "finite": true,
      "max_abs": 2.7527274464026354,
      "shape": [
        1,
        50
      ],
      "sum": 28.224680173991963
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
      "max_abs": 2.3362666995840704,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -132.12083840320508
    },
    "post_update_log_likelihoods": {
      "finite": true,
      "max_abs": 17.200502067421393,
      "shape": [
        1
      ],
      "sum": -17.200502067421393
    },
    "post_update_log_weights": {
      "finite": true,
      "max_abs": 17.358632204072613,
      "shape": [
        1,
        50
      ],
      "sum": -420.72215212543404
    },
    "pre_log_weights": {
      "finite": true,
      "max_abs": 3.9833688267575242,
      "shape": [
        1,
        50
      ],
      "sum": -195.63256651599147
    },
    "pre_particles": {
      "finite": true,
      "max_abs": 2.5933950054045614,
      "shape": [
        1,
        50,
        2
      ],
      "sum": -132.2181669047356
    },
    "proposal_ll": {
      "finite": true,
      "max_abs": 5.896490813727095,
      "shape": [
        1,
        50
      ],
      "sum": -3.2793767008896997
    },
    "proposal_mean": {
      "finite": true,
      "max_abs": 4.12649214562547,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 229.8055803639727
    },
    "proposed_particles": {
      "finite": true,
      "max_abs": 5.002437644950284,
      "shape": [
        1,
        50,
        2
      ],
      "sum": 222.54040960851975
    },
    "transition_ll": {
      "finite": true,
      "max_abs": 32.49679430969144,
      "shape": [
        1,
        50
      ],
      "sum": -1016.4456433592165
    },
    "transport_matrix": {
      "finite": true,
      "max_abs": 0.2579538057358776,
      "shape": [
        1,
        50,
        50
      ],
      "sum": 50.0
    },
    "unnormalized": {
      "finite": true,
      "max_abs": 32.555043896678775,
      "shape": [
        1,
        50
      ],
      "sum": -1180.542736755742
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
