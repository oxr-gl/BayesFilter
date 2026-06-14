# Filterflow R3 Transport Internals Audit

## Decision

`filterflow_r3_transport_internals_no_difference_on_selected_rows`

## Interpretation

No BayesFilter-versus-filterflow difference was detected in the selected-row recomputed transport internals. Nonzero deltas remain between the stored filterflow trace and a fresh recomputation on the same rows, with max trace transport-matrix delta 1.1920928955078125e-07 and max trace post-resample-particle delta 6.103515625e-05. The prior R3 replay discrepancy is therefore better described as float32 repeat-call/trace sensitivity around the transport output, not as a detected low-level BayesFilter formula mismatch.

## Comparison

```json
{
  "finite_values": true,
  "first_divergence": {
    "status": "no_divergence"
  },
  "implementation_agreement": true,
  "max_bayesfilter_trace_post_resample_particles_delta": 6.103515625e-05,
  "max_bayesfilter_trace_transport_matrix_delta": 1.1920928955078125e-07,
  "max_field_deltas": {
    "alpha": 0.0,
    "beta": 0.0,
    "centered_particles": 0.0,
    "cost_xx": 0.0,
    "cost_xy": 0.0,
    "cost_yx": 0.0,
    "cost_yy": 0.0,
    "diameter_value": 0.0,
    "epsilon_0": 0.0,
    "input_log_weights": 0.0,
    "input_particles": 0.0,
    "iterations": 0.0,
    "scale": 0.0,
    "scaled_particles": 0.0,
    "scaling_factor": 0.0,
    "sinkhorn_scale": 0.0,
    "transport_matrix": 0.0,
    "transported_particles": 0.0
  },
  "max_filterflow_trace_post_resample_particles_delta": 6.103515625e-05,
  "max_filterflow_trace_transport_matrix_delta": 1.1920928955078125e-07,
  "row_comparisons": [
    {
      "bayesfilter_trace_post_resample_particles_delta": 0.0,
      "bayesfilter_trace_transport_matrix_delta": 5.960464477539063e-08,
      "field_deltas": {
        "alpha": 0.0,
        "beta": 0.0,
        "centered_particles": 0.0,
        "cost_xx": 0.0,
        "cost_xy": 0.0,
        "cost_yx": 0.0,
        "cost_yy": 0.0,
        "diameter_value": 0.0,
        "epsilon_0": 0.0,
        "input_log_weights": 0.0,
        "input_particles": 0.0,
        "iterations": 0.0,
        "scale": 0.0,
        "scaled_particles": 0.0,
        "scaling_factor": 0.0,
        "sinkhorn_scale": 0.0,
        "transport_matrix": 0.0,
        "transported_particles": 0.0
      },
      "filterflow_trace_post_resample_particles_delta": 0.0,
      "filterflow_trace_transport_matrix_delta": 5.960464477539063e-08,
      "first_divergent_field": "none",
      "time_index": 7
    },
    {
      "bayesfilter_trace_post_resample_particles_delta": 7.62939453125e-06,
      "bayesfilter_trace_transport_matrix_delta": 2.9802322387695312e-08,
      "field_deltas": {
        "alpha": 0.0,
        "beta": 0.0,
        "centered_particles": 0.0,
        "cost_xx": 0.0,
        "cost_xy": 0.0,
        "cost_yx": 0.0,
        "cost_yy": 0.0,
        "diameter_value": 0.0,
        "epsilon_0": 0.0,
        "input_log_weights": 0.0,
        "input_particles": 0.0,
        "iterations": 0.0,
        "scale": 0.0,
        "scaled_particles": 0.0,
        "scaling_factor": 0.0,
        "sinkhorn_scale": 0.0,
        "transport_matrix": 0.0,
        "transported_particles": 0.0
      },
      "filterflow_trace_post_resample_particles_delta": 7.62939453125e-06,
      "filterflow_trace_transport_matrix_delta": 2.9802322387695312e-08,
      "first_divergent_field": "none",
      "time_index": 16
    },
    {
      "bayesfilter_trace_post_resample_particles_delta": 0.0,
      "bayesfilter_trace_transport_matrix_delta": 1.4901161193847656e-08,
      "field_deltas": {
        "alpha": 0.0,
        "beta": 0.0,
        "centered_particles": 0.0,
        "cost_xx": 0.0,
        "cost_xy": 0.0,
        "cost_yx": 0.0,
        "cost_yy": 0.0,
        "diameter_value": 0.0,
        "epsilon_0": 0.0,
        "input_log_weights": 0.0,
        "input_particles": 0.0,
        "iterations": 0.0,
        "scale": 0.0,
        "scaled_particles": 0.0,
        "scaling_factor": 0.0,
        "sinkhorn_scale": 0.0,
        "transport_matrix": 0.0,
        "transported_particles": 0.0
      },
      "filterflow_trace_post_resample_particles_delta": 0.0,
      "filterflow_trace_transport_matrix_delta": 1.4901161193847656e-08,
      "first_divergent_field": "none",
      "time_index": 43
    },
    {
      "bayesfilter_trace_post_resample_particles_delta": 6.103515625e-05,
      "bayesfilter_trace_transport_matrix_delta": 1.1920928955078125e-07,
      "field_deltas": {
        "alpha": 0.0,
        "beta": 0.0,
        "centered_particles": 0.0,
        "cost_xx": 0.0,
        "cost_xy": 0.0,
        "cost_yx": 0.0,
        "cost_yy": 0.0,
        "diameter_value": 0.0,
        "epsilon_0": 0.0,
        "input_log_weights": 0.0,
        "input_particles": 0.0,
        "iterations": 0.0,
        "scale": 0.0,
        "scaled_particles": 0.0,
        "scaling_factor": 0.0,
        "sinkhorn_scale": 0.0,
        "transport_matrix": 0.0,
        "transported_particles": 0.0
      },
      "filterflow_trace_post_resample_particles_delta": 6.103515625e-05,
      "filterflow_trace_transport_matrix_delta": 1.1920928955078125e-07,
      "first_divergent_field": "none",
      "time_index": 79
    }
  ],
  "status": "compared"
}
```

## Trace Validation

```json
{
  "official_trace_deltas": {
    "log_likelihoods": 3.0517578125e-05,
    "log_weights": 0.0,
    "particles": 0.0
  },
  "official_trace_match": true,
  "tolerance": 5e-05
}
```

## Compact Internals

### Filterflow

```json
{
  "backend": "executable_filterflow_subprocess",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "rows": [
    {
      "direct_transport_matrix_delta": 5.960464477539063e-08,
      "finite_values": true,
      "time_index": 7,
      "trace_post_resample_particles_delta": 0.0,
      "trace_transport_matrix_delta": 5.960464477539063e-08
    },
    {
      "direct_transport_matrix_delta": 2.9802322387695312e-08,
      "finite_values": true,
      "time_index": 16,
      "trace_post_resample_particles_delta": 7.62939453125e-06,
      "trace_transport_matrix_delta": 2.9802322387695312e-08
    },
    {
      "direct_transport_matrix_delta": 1.4901161193847656e-08,
      "finite_values": true,
      "time_index": 43,
      "trace_post_resample_particles_delta": 0.0,
      "trace_transport_matrix_delta": 1.4901161193847656e-08
    },
    {
      "direct_transport_matrix_delta": 1.1920928955078125e-07,
      "finite_values": true,
      "time_index": 79,
      "trace_post_resample_particles_delta": 6.103515625e-05,
      "trace_transport_matrix_delta": 1.1920928955078125e-07
    }
  ],
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-03 00:15:11.940562: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780416911.948817     350 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780416911.951412     350 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780416911.957830     350 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780416911.957863     350 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780416911.957867     350 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780416911.957869     350 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-03 00:15:11.960122: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-03 00:15:14.252462: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n"
}
```

### BayesFilter

```json
{
  "backend": "tensorflow_tensorflow_probability",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "rows": [
    {
      "direct_transport_matrix_delta": 0.0,
      "finite_values": true,
      "time_index": 7,
      "trace_post_resample_particles_delta": 0.0,
      "trace_transport_matrix_delta": 5.960464477539063e-08
    },
    {
      "direct_transport_matrix_delta": 0.0,
      "finite_values": true,
      "time_index": 16,
      "trace_post_resample_particles_delta": 7.62939453125e-06,
      "trace_transport_matrix_delta": 2.9802322387695312e-08
    },
    {
      "direct_transport_matrix_delta": 0.0,
      "finite_values": true,
      "time_index": 43,
      "trace_post_resample_particles_delta": 0.0,
      "trace_transport_matrix_delta": 1.4901161193847656e-08
    },
    {
      "direct_transport_matrix_delta": 0.0,
      "finite_values": true,
      "time_index": 79,
      "trace_post_resample_particles_delta": 6.103515625e-05,
      "trace_transport_matrix_delta": 1.1920928955078125e-07
    }
  ],
  "status": "executed",
  "stderr_excerpt": ""
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
- No smoothness-surface gradient correctness is concluded.
- No transport residual correctness claim is concluded.
