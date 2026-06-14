# Result: Row 173 Transport-Upstream Source Probe

## Decision

`filterflow_float64_row_173_transport_upstream_source_h2_downstream_adjoint_topology`

## Hypothesis Classification

`h2_downstream_adjoint_topology_mismatch`

forward boundary values match but downstream adjoints differ

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_transport_upstream_source_h2_downstream_adjoint_topology | h2_downstream_adjoint_topology_mismatch | {'all_vetoes_clear': True, 'comparator_drift': False, 'path_boundary_clean': True, 'scalar_value_gate_pass': True, 'all_resampling_flags_match': True, 'all_forward_finite': True, 'all_adjoints_finite': True, 'cpu_only_parent': True} | single row, target time, and two probe times; no global claim | trace adjoint topology around post-transport state carryover | correctness, posterior correctness, production readiness, global gradient agreement |

## Source Comparison

```json
{
  "all_adjoints_finite": true,
  "all_forward_finite": true,
  "all_resampling_flags_match": true,
  "interpretation": "downstream_adjoint_topology_mismatch",
  "max_abs_total_gradient_delta": 5.302734403676368,
  "rows": [
    {
      "bayesfilter_resampling_flag": [
        true
      ],
      "bayesfilter_transport_residuals": {
        "column": 8.881784197001252e-16,
        "row": 9.749829811056543e-06
      },
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_transport_upstream_delta": {
        "finite": true,
        "max_abs_delta": 0.0,
        "sum_delta": 0.0
      },
      "filterflow_resampling_flag": [
        true
      ],
      "filterflow_transport_residuals": {
        "column": 1.1102230246251565e-15,
        "row": 9.749830994998376e-06
      },
      "first_adjoint_delta_node": {
        "adjoint_max_abs_delta": 5.500608568351231,
        "node": "pre_particles"
      },
      "first_forward_delta_node": null,
      "max_adjoint_delta": 14.4878444484294,
      "max_adjoint_delta_node": {
        "adjoint_finite": true,
        "adjoint_max_abs_delta": 14.4878444484294,
        "adjoint_sum_delta": 21.262310437624233,
        "forward_finite": true,
        "forward_max_abs_delta": 3.1445779313798994e-10,
        "forward_sum_delta": -2.176051339120022e-09,
        "node": "proposal_mean"
      },
      "max_forward_delta": 1.1801262189692352e-09,
      "max_forward_delta_node": {
        "adjoint_finite": true,
        "adjoint_max_abs_delta": 1.948882166757926e-10,
        "adjoint_sum_delta": 2.6577559597562583e-12,
        "forward_finite": true,
        "forward_max_abs_delta": 1.1801262189692352e-09,
        "forward_sum_delta": 2.8624902448370904e-09,
        "node": "pre_log_weights"
      },
      "node_rows": [
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 5.500608568351231,
          "adjoint_sum_delta": -24.423658477866233,
          "forward_finite": true,
          "forward_max_abs_delta": 3.06442871078616e-10,
          "forward_sum_delta": 1.8381172139925184e-09,
          "node": "pre_particles"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.948882166757926e-10,
          "adjoint_sum_delta": 2.6577559597562583e-12,
          "forward_finite": true,
          "forward_max_abs_delta": 1.1801262189692352e-09,
          "forward_sum_delta": 2.8624902448370904e-09,
          "node": "pre_log_weights"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 4.524380869952438e-12,
          "forward_sum_delta": 4.524380869952438e-12,
          "node": "log_ess"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0010672900132249197,
          "adjoint_sum_delta": -0.2512387528610418,
          "forward_finite": true,
          "forward_max_abs_delta": 9.559442126771955e-11,
          "forward_sum_delta": -1.9627978177769046e-14,
          "node": "transport_matrix"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 4.840391921834275e-06,
          "adjoint_sum_delta": -2.9051907020918866e-05,
          "forward_finite": true,
          "forward_max_abs_delta": 3.6079761400742427e-10,
          "forward_sum_delta": 5.125311730580506e-09,
          "node": "post_particles"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.5821476504473964e-06,
          "adjoint_sum_delta": 2.6306268361558915e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 0.0,
          "forward_sum_delta": 0.0,
          "node": "post_log_weights"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 14.4878444484294,
          "adjoint_sum_delta": 21.262310437624233,
          "forward_finite": true,
          "forward_max_abs_delta": 3.1445779313798994e-10,
          "forward_sum_delta": -2.176051339120022e-09,
          "node": "proposal_mean"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 14.4878444484294,
          "adjoint_sum_delta": 21.262310437624233,
          "forward_finite": true,
          "forward_max_abs_delta": 3.1445779313798994e-10,
          "forward_sum_delta": -2.176051339120022e-09,
          "node": "proposed_particles"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.5821476504473964e-06,
          "adjoint_sum_delta": 2.6306268361558915e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 1.362403523330613e-10,
          "forward_sum_delta": 5.972933259101865e-10,
          "node": "observation_ll"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.5821476504473964e-06,
          "adjoint_sum_delta": 2.6306268361558915e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 7.612754870933713e-10,
          "forward_sum_delta": -1.3622907246713112e-09,
          "node": "transition_ll"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.9890538775005911,
          "adjoint_sum_delta": 0.9999999999999978,
          "forward_finite": true,
          "forward_max_abs_delta": 3.028688411177427e-13,
          "forward_sum_delta": 3.4305891460917337e-13,
          "node": "proposal_ll"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.5821476504473964e-06,
          "adjoint_sum_delta": 2.6306268361558915e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 7.489386888437366e-10,
          "forward_sum_delta": -7.653406797203388e-10,
          "node": "unnormalized"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 6.547651310029323e-12,
          "forward_sum_delta": 6.547651310029323e-12,
          "node": "increment"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 2.4334127574077158e-06,
          "adjoint_sum_delta": -7.54537618547998e-05,
          "forward_finite": true,
          "forward_max_abs_delta": 7.554863401537659e-10,
          "forward_sum_delta": -1.092723245221805e-09,
          "node": "normalized_log_weights"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 1.4379963886312908e-10,
          "forward_sum_delta": -1.4379963886312908e-10,
          "node": "post_log_likelihoods"
        }
      ],
      "raw_transport_upstream_delta": {
        "finite": true,
        "max_abs_delta": 0.0010672900132249197,
        "sum_delta": -0.2512387528610418
      },
      "resampling_flags_match": true,
      "time_index": 43
    },
    {
      "bayesfilter_resampling_flag": [
        true
      ],
      "bayesfilter_transport_residuals": {
        "column": 3.552713678800501e-15,
        "row": 8.397815569827216e-06
      },
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_transport_upstream_delta": {
        "finite": true,
        "max_abs_delta": 0.038257926126621045,
        "sum_delta": -1.9092531867589029
      },
      "filterflow_resampling_flag": [
        true
      ],
      "filterflow_transport_residuals": {
        "column": 3.552713678800501e-15,
        "row": 8.39781654016214e-06
      },
      "first_adjoint_delta_node": {
        "adjoint_max_abs_delta": 5.757224499990219,
        "node": "pre_particles"
      },
      "first_forward_delta_node": null,
      "max_adjoint_delta": 5.757224499990219,
      "max_adjoint_delta_node": {
        "adjoint_finite": true,
        "adjoint_max_abs_delta": 5.757224499990219,
        "adjoint_sum_delta": -3.8070319560212296,
        "forward_finite": true,
        "forward_max_abs_delta": 4.839648681809194e-10,
        "forward_sum_delta": 3.327102149341954e-09,
        "node": "pre_particles"
      },
      "max_forward_delta": 4.996177693783466e-09,
      "max_forward_delta_node": {
        "adjoint_finite": true,
        "adjoint_max_abs_delta": 0.0069749582753122485,
        "adjoint_sum_delta": -0.038194859182577964,
        "forward_finite": true,
        "forward_max_abs_delta": 4.996177693783466e-09,
        "forward_sum_delta": 9.282950408362467e-09,
        "node": "pre_log_weights"
      },
      "node_rows": [
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 5.757224499990219,
          "adjoint_sum_delta": -3.8070319560212296,
          "forward_finite": true,
          "forward_max_abs_delta": 4.839648681809194e-10,
          "forward_sum_delta": 3.327102149341954e-09,
          "node": "pre_particles"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0069749582753122485,
          "adjoint_sum_delta": -0.038194859182577964,
          "forward_finite": true,
          "forward_max_abs_delta": 4.996177693783466e-09,
          "forward_sum_delta": 9.282950408362467e-09,
          "node": "pre_log_weights"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 1.411590844213606e-10,
          "forward_sum_delta": -1.411590844213606e-10,
          "node": "log_ess"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.06167895758798991,
          "adjoint_sum_delta": -32.150265266150306,
          "forward_finite": true,
          "forward_max_abs_delta": 2.482101746359433e-10,
          "forward_sum_delta": -1.8973256027662425e-14,
          "node": "transport_matrix"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0002572478904350334,
          "adjoint_sum_delta": -0.0033939337955600293,
          "forward_finite": true,
          "forward_max_abs_delta": 4.3946357664026436e-10,
          "forward_sum_delta": 1.2092018941700644e-08,
          "node": "post_particles"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.0212514167662334e-10,
          "adjoint_sum_delta": -1.9099305470504646e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 0.0,
          "forward_sum_delta": 0.0,
          "node": "post_log_weights"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 4.655565035713791,
          "adjoint_sum_delta": 14.065477963916738,
          "forward_finite": true,
          "forward_max_abs_delta": 2.4846258384059183e-10,
          "forward_sum_delta": -5.34583932676469e-09,
          "node": "proposal_mean"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 4.655565035713791,
          "adjoint_sum_delta": 14.065477963916738,
          "forward_finite": true,
          "forward_max_abs_delta": 2.4846258384059183e-10,
          "forward_sum_delta": -5.34583932676469e-09,
          "node": "proposed_particles"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.0212514167662334e-10,
          "adjoint_sum_delta": -1.9099305470504646e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 1.935811511089014e-10,
          "forward_sum_delta": -7.198179829970286e-10,
          "node": "observation_ll"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.0212514167662334e-10,
          "adjoint_sum_delta": -1.9099305470504646e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 6.03701089119113e-10,
          "forward_sum_delta": -8.217529767762244e-09,
          "node": "transition_ll"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.3613479504667966,
          "adjoint_sum_delta": 1.0000000000000013,
          "forward_finite": true,
          "forward_max_abs_delta": 2.4158453015843406e-13,
          "forward_sum_delta": 2.0095036745715333e-13,
          "node": "proposal_ll"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.0212514167662334e-10,
          "adjoint_sum_delta": -1.9099305470504646e-15,
          "forward_finite": true,
          "forward_max_abs_delta": 7.149374425807764e-10,
          "forward_sum_delta": -8.937552031795803e-09,
          "node": "unnormalized"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 1.6294787741344408e-10,
          "forward_sum_delta": -1.6294787741344408e-10,
          "node": "increment"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 1.2786646741425045e-10,
          "adjoint_sum_delta": 1.3483103522560214e-12,
          "forward_finite": true,
          "forward_max_abs_delta": 5.519895651673323e-10,
          "forward_sum_delta": -7.901581611235997e-10,
          "node": "normalized_log_weights"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 1.427679308108054e-09,
          "forward_sum_delta": -1.427679308108054e-09,
          "node": "post_log_likelihoods"
        }
      ],
      "raw_transport_upstream_delta": {
        "finite": true,
        "max_abs_delta": 0.06167895758798991,
        "sum_delta": -32.150265266150306
      },
      "resampling_flags_match": true,
      "time_index": 52
    }
  ],
  "status": "compared",
  "target_scalar_delta": 6.2123888255882775e-09,
  "total_gradient_delta": [
    5.302734403676368,
    -0.1337765252068337
  ]
}
```

## Veto Status

```json
{
  "all_adjoints_finite": true,
  "all_forward_finite": true,
  "all_resampling_flags_match": true,
  "all_vetoes_clear": true,
  "comparator_drift": false,
  "cpu_only_parent": true,
  "path_boundary_clean": true,
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
  "probe_times": [
    43,
    52
  ],
  "settings": {
    "T": 100,
    "dtype": "float64",
    "mesh_index": 173,
    "n_particles": 50,
    "probe_times": [
      43,
      52
    ],
    "target_time_index": 93,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ]
  },
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-04 23:59:13.094358: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780588753.107924     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780588753.112242     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780588753.123525     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780588753.123584     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780588753.123588     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780588753.123590     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-04 23:59:13.126749: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-04 23:59:15.649623: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
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
  "probe_times": [
    43,
    52
  ],
  "settings": {
    "T": 100,
    "dtype": "float64",
    "mesh_index": 173,
    "n_particles": 50,
    "probe_times": [
      43,
      52
    ],
    "target_time_index": 93,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ]
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
- No analytic gradient correctness is concluded.
- No posterior correctness is concluded.
- No global gradient agreement is concluded.
- No full mesh or surface agreement is concluded.
- No production readiness or public API readiness is concluded.
