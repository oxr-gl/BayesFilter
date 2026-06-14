# Result: Row 173 Proposal/Update Adjoint-Topology Probe

## Decision

`filterflow_float64_row_173_proposal_adjoint_topology_h4_downstream_update_topology`

## Hypothesis Classification

`h4_downstream_update_topology`

forward tensors and direct distribution log-prob gradients match, but the official proposal-likelihood wiring into proposed particles differs

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_proposal_adjoint_topology_h4_downstream_update_topology | h4_downstream_update_topology | {'all_vetoes_clear': True, 'comparator_drift': False, 'path_boundary_clean': True, 'scalar_value_gate_pass': True, 'all_resampling_flags_match': True, 'all_forward_finite': True, 'all_adjoints_finite': True, 'all_local_gradients_finite': True, 'stop_gradient_ablation_executed': True, 'cpu_only_parent': True} | single row, target time, and one probe time; no global claim | trace the official proposal-likelihood wiring path and reconcile BayesFilter proposal_ll construction with executable FilterFlow | correctness, posterior correctness, production readiness, global gradient agreement |

## Source Comparison

```json
{
  "all_adjoints_finite": true,
  "all_forward_finite": true,
  "all_local_gradients_finite": true,
  "all_resampling_flags_match": true,
  "interpretation": "proposal_likelihood_wiring_topology",
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
      "first_local_gradient_delta": {
        "max_abs_delta": 14.888157520909445,
        "name": "target_to_proposal_mean",
        "tolerance": 0.0002
      },
      "first_log_prob_gradient_delta": {
        "max_abs_delta": 28.749898405961705,
        "name": "proposal_ll_to_proposed_particles",
        "tolerance": 0.0002
      },
      "first_sample_gradient_delta": null,
      "first_target_adjoint_gradient_delta": {
        "max_abs_delta": 14.888157520909445,
        "name": "target_to_proposal_mean",
        "tolerance": 0.0002
      },
      "local_gradient_rows": [
        {
          "bayesfilter_max_abs": 14.888157520909445,
          "filterflow_max_abs": 0.0,
          "finite": true,
          "max_abs_delta": 14.888157520909445,
          "name": "target_to_proposal_mean",
          "sum_delta": -26.11090244221281
        },
        {
          "bayesfilter_max_abs": 14.888157520909445,
          "filterflow_max_abs": 2.3905111099816416,
          "finite": true,
          "max_abs_delta": 14.4878444484294,
          "name": "target_to_proposed_particles",
          "sum_delta": 21.262310437624233
        },
        {
          "bayesfilter_max_abs": 0.0,
          "filterflow_max_abs": 0.0,
          "finite": true,
          "max_abs_delta": 0.0,
          "name": "proposal_ll_to_proposal_mean",
          "sum_delta": 0.0
        },
        {
          "bayesfilter_max_abs": 0.0,
          "filterflow_max_abs": 28.749898405961705,
          "finite": true,
          "max_abs_delta": 28.749898405961705,
          "name": "proposal_ll_to_proposed_particles",
          "sum_delta": 17.20700588220021
        },
        {
          "bayesfilter_max_abs": 0.0,
          "filterflow_max_abs": 0.0,
          "finite": true,
          "max_abs_delta": 0.0,
          "name": "proposal_dist_log_prob_to_proposal_mean",
          "sum_delta": 0.0
        },
        {
          "bayesfilter_max_abs": 0.0,
          "filterflow_max_abs": 0.0,
          "finite": true,
          "max_abs_delta": 0.0,
          "name": "proposal_dist_log_prob_to_proposed_particles",
          "sum_delta": 0.0
        },
        {
          "bayesfilter_max_abs": 28.749898405961705,
          "filterflow_max_abs": 28.749898405961705,
          "finite": true,
          "max_abs_delta": 0.0,
          "name": "fresh_dist_log_prob_to_fresh_proposal_mean",
          "sum_delta": 0.0
        },
        {
          "bayesfilter_max_abs": 28.749898405961705,
          "filterflow_max_abs": 28.749898405961705,
          "finite": true,
          "max_abs_delta": 0.0,
          "name": "fresh_dist_log_prob_to_proposed_particles",
          "sum_delta": 0.0
        },
        {
          "bayesfilter_max_abs": 12.330746642771128,
          "filterflow_max_abs": 12.33074664236036,
          "finite": true,
          "max_abs_delta": 1.1572183211683296e-09,
          "name": "transition_ll_to_proposed_particles",
          "sum_delta": 1.4936211878424643e-08
        },
        {
          "bayesfilter_max_abs": 23.75646302678831,
          "filterflow_max_abs": 23.75646302703842,
          "finite": true,
          "max_abs_delta": 1.156763573817443e-09,
          "name": "observation_ll_to_proposed_particles",
          "sum_delta": -1.4952661331335548e-08
        },
        {
          "bayesfilter_max_abs": 14.888157520909445,
          "filterflow_max_abs": 0.0,
          "finite": true,
          "max_abs_delta": 14.888157520909445,
          "name": "sample_to_proposal_mean_target_upstream",
          "sum_delta": -26.11090244221281
        },
        {
          "bayesfilter_max_abs": 0.0,
          "filterflow_max_abs": 0.0,
          "finite": true,
          "max_abs_delta": 0.0,
          "name": "sample_sum_to_proposal_mean",
          "sum_delta": 0.0
        },
        {
          "bayesfilter_max_abs": 0.0,
          "filterflow_max_abs": 0.0,
          "finite": true,
          "max_abs_delta": 0.0,
          "name": "sample_noise_sum_to_proposal_mean",
          "sum_delta": 0.0
        }
      ],
      "max_adjoint_delta": 14.888157520909445,
      "max_adjoint_delta_node": {
        "adjoint_finite": true,
        "adjoint_max_abs_delta": 14.888157520909445,
        "adjoint_sum_delta": -26.11090244221281,
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
      "max_local_gradient_delta": {
        "bayesfilter_max_abs": 0.0,
        "filterflow_max_abs": 28.749898405961705,
        "finite": true,
        "max_abs_delta": 28.749898405961705,
        "name": "proposal_ll_to_proposed_particles",
        "sum_delta": 17.20700588220021
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
          "node": "proposal_loc"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 14.888157520909445,
          "adjoint_sum_delta": -26.11090244221281,
          "forward_finite": true,
          "forward_max_abs_delta": 3.1445779313798994e-10,
          "forward_sum_delta": -2.176051339120022e-09,
          "node": "proposal_mean"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 3.1445779313798994e-10,
          "forward_sum_delta": -2.176051339120022e-09,
          "node": "fresh_proposal_mean"
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
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 0.0,
          "forward_sum_delta": 0.0,
          "node": "sample_noise"
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
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 0.0,
          "forward_sum_delta": 0.0,
          "node": "proposal_dist_log_prob"
        },
        {
          "adjoint_finite": true,
          "adjoint_max_abs_delta": 0.0,
          "adjoint_sum_delta": 0.0,
          "forward_finite": true,
          "forward_max_abs_delta": 0.0,
          "forward_sum_delta": 0.0,
          "node": "fresh_dist_log_prob"
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
  "all_local_gradients_finite": true,
  "all_resampling_flags_match": true,
  "all_vetoes_clear": true,
  "comparator_drift": false,
  "cpu_only_parent": true,
  "path_boundary_clean": true,
  "scalar_value_gate_pass": true,
  "stop_gradient_ablation_executed": true
}
```

## Stop-Gradient Ablation Comparison

```json
{
  "best_value_valid_mode": {
    "description": "No added local stop-gradient at time 43.",
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_delta_to_filterflow": [
      5.302734403676368,
      -0.1337765252068337
    ],
    "max_abs_gradient_delta_to_filterflow": 5.302734403676368,
    "mode": "raw",
    "scalar_delta_to_filterflow": 6.2123888255882775e-09,
    "scalar_within_tolerance": true,
    "target_scalar": -141.71711568080488,
    "total_gradient_diag": [
      9110.446610302024,
      56.9898732897215
    ]
  },
  "filterflow_gradient_diag": [
    9105.143875898348,
    57.123649814928335
  ],
  "filterflow_target_scalar": -141.71711568701727,
  "interpretation": "tested_modes_do_not_reduce_filterflow_gradient_delta",
  "matching_modes": [],
  "raw_max_abs_gradient_delta": 5.302734403676368,
  "status": "compared"
}
```

## Stop-Gradient Ablation

```json
{
  "contract": "BayesFilter-only local time-43 stop-gradient ablations. Forward values should remain scalar-aligned before gradient deltas are interpreted.",
  "rows": [
    {
      "description": "No added local stop-gradient at time 43.",
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta_to_filterflow": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "max_abs_gradient_delta_to_filterflow": 5.302734403676368,
      "mode": "raw",
      "scalar_delta_to_filterflow": 6.2123888255882775e-09,
      "scalar_within_tolerance": true,
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    {
      "description": "Stop gradient through proposed particles at time 43.",
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta_to_filterflow": [
        -6009.101621290683,
        170.28463144408303
      ],
      "max_abs_gradient_delta_to_filterflow": 6009.101621290683,
      "mode": "stop_proposed_particles",
      "scalar_delta_to_filterflow": 6.2118203913996695e-09,
      "scalar_within_tolerance": true,
      "target_scalar": -141.71711568080545,
      "total_gradient_diag": [
        3096.042254607664,
        227.40828125901137
      ]
    },
    {
      "description": "Stop gradient through proposal mean at time 43.",
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta_to_filterflow": [
        2398.5868528354986,
        8.654066853741888
      ],
      "max_abs_gradient_delta_to_filterflow": 2398.5868528354986,
      "mode": "stop_proposal_mean",
      "scalar_delta_to_filterflow": 6.2123888255882775e-09,
      "scalar_within_tolerance": true,
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        11503.730728733846,
        65.77771666867022
      ]
    },
    {
      "description": "Stop gradient through proposal log probability at time 43.",
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta_to_filterflow": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "max_abs_gradient_delta_to_filterflow": 5.302734403676368,
      "mode": "stop_proposal_ll",
      "scalar_delta_to_filterflow": 6.2123888255882775e-09,
      "scalar_within_tolerance": true,
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    {
      "description": "Stop gradient through transition log probability at time 43.",
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta_to_filterflow": [
        -512.2817835393616,
        18.882576235224583
      ],
      "max_abs_gradient_delta_to_filterflow": 512.2817835393616,
      "mode": "stop_transition_ll",
      "scalar_delta_to_filterflow": 6.2123888255882775e-09,
      "scalar_within_tolerance": true,
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        8592.862092358986,
        76.00622605015292
      ]
    },
    {
      "description": "Stop gradient through observation log probability at time 43.",
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta_to_filterflow": [
        -209.8087762632731,
        -1.158815986038789
      ],
      "max_abs_gradient_delta_to_filterflow": 209.8087762632731,
      "mode": "stop_observation_ll",
      "scalar_delta_to_filterflow": 6.2123888255882775e-09,
      "scalar_within_tolerance": true,
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        8895.335099635075,
        55.964833828889546
      ]
    },
    {
      "description": "Keep proposed-particle values but stop the sample-noise residual from feeding back through proposal mean at time 43.",
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_delta_to_filterflow": [
        5.303606461880918,
        -0.1337985257380936
      ],
      "max_abs_gradient_delta_to_filterflow": 5.303606461880918,
      "mode": "stop_proposal_sample_noise",
      "scalar_delta_to_filterflow": 6.2118203913996695e-09,
      "scalar_within_tolerance": true,
      "target_scalar": -141.71711568080545,
      "total_gradient_diag": [
        9110.447482360229,
        56.98985128919024
      ]
    }
  ],
  "status": "executed"
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
  "local_gradient_summary": [
    {
      "local_gradients": {
        "fresh_dist_log_prob_to_fresh_proposal_mean": {
          "finite": true,
          "max_abs": 28.749898405961705,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 17.20700588220021
        },
        "fresh_dist_log_prob_to_proposed_particles": {
          "finite": true,
          "max_abs": 28.749898405961705,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -17.20700588220021
        },
        "observation_ll_to_proposed_particles": {
          "finite": true,
          "max_abs": 23.75646302703842,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 26.40381530371485
        },
        "proposal_dist_log_prob_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "proposal_dist_log_prob_to_proposed_particles": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "proposal_ll_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "proposal_ll_to_proposed_particles": {
          "finite": true,
          "max_abs": 28.749898405961705,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -17.20700588220021
        },
        "sample_noise_sum_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "sample_sum_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "sample_to_proposal_mean_target_upstream": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
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
        },
        "target_to_proposed_particles": {
          "finite": true,
          "max_abs": 2.3905111099816416,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -47.373212879837055
        },
        "transition_ll_to_proposed_particles": {
          "finite": true,
          "max_abs": 12.33074664236036,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -43.610821185866776
        }
      },
      "time_index": 43
    }
  ],
  "probe_times": [
    43
  ],
  "settings": {
    "T": 100,
    "dtype": "float64",
    "mesh_index": 173,
    "n_particles": 50,
    "probe_times": [
      43
    ],
    "target_time_index": 93,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ]
  },
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-05 02:18:08.042000: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780597088.057168     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780597088.062347     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780597088.073590     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780597088.073650     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780597088.073655     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780597088.073656     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-05 02:18:08.076898: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-05 02:18:10.729273: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
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
  "local_gradient_summary": [
    {
      "local_gradients": {
        "fresh_dist_log_prob_to_fresh_proposal_mean": {
          "finite": true,
          "max_abs": 28.749898405961705,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 17.20700588220021
        },
        "fresh_dist_log_prob_to_proposed_particles": {
          "finite": true,
          "max_abs": 28.749898405961705,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -17.20700588220021
        },
        "observation_ll_to_proposed_particles": {
          "finite": true,
          "max_abs": 23.75646302678831,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 26.40381528876219
        },
        "proposal_dist_log_prob_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "proposal_dist_log_prob_to_proposed_particles": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "proposal_ll_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "proposal_ll_to_proposed_particles": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "sample_noise_sum_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "sample_sum_to_proposal_mean": {
          "finite": true,
          "max_abs": 0.0,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 0.0
        },
        "sample_to_proposal_mean_target_upstream": {
          "finite": true,
          "max_abs": 14.888157520909445,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -26.11090244221281
        },
        "target_to_proposal_mean": {
          "finite": true,
          "max_abs": 14.888157520909445,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -26.11090244221281
        },
        "target_to_proposed_particles": {
          "finite": true,
          "max_abs": 14.888157520909445,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -26.11090244221281
        },
        "transition_ll_to_proposed_particles": {
          "finite": true,
          "max_abs": 12.330746642771128,
          "shape": [
            1,
            50,
            2
          ],
          "sum": -43.610821170930556
        }
      },
      "time_index": 43
    }
  ],
  "probe_times": [
    43
  ],
  "settings": {
    "T": 100,
    "dtype": "float64",
    "mesh_index": 173,
    "n_particles": 50,
    "probe_times": [
      43
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
- BayesFilter stop-gradient ablations are explanatory only and do not define a preferred algorithm.
