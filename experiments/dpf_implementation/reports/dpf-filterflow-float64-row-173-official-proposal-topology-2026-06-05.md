# Result: Row 173 Official Proposal-Likelihood Topology Probe

## Decision

`filterflow_float64_row_173_official_proposal_topology_h2_state_object_topology_required`

## Hypothesis Classification

`h2_state_object_topology_required`

BayesFilter reproduces the official VJP only under the detached/internal state-object topology variant

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_official_proposal_topology_h2_state_object_topology_required | h2_state_object_topology_required | {'all_vetoes_clear': True, 'comparator_drift': False, 'path_boundary_clean': True, 'scalar_value_gate_pass': True, 'proposal_ll_value_gate_pass': True, 'all_resampling_flags_match': True, 'all_forward_finite': True, 'all_adjoints_finite': True, 'all_local_gradients_finite': True, 'all_variant_gradients_finite': True, 'helper_boundary_not_material_explanatory': False, 'cpu_only_parent': True} | single row, target time, and one probe time; no global claim | mirror the executable state-object proposal-likelihood topology in the next value-preserving BayesFilter probe | correctness, posterior correctness, production readiness, global gradient agreement |

## Source Comparison

```json
{
  "all_adjoints_finite": true,
  "all_forward_finite": true,
  "all_local_gradients_finite": true,
  "all_proposal_ll_value_gates_pass": true,
  "all_resampling_flags_match": true,
  "all_scalar_value_gates_pass": true,
  "all_variant_gradients_finite": true,
  "any_primary_vjp_match": true,
  "best_primary_match_max_abs_total_gradient_delta": 544.9274396565979,
  "best_primary_match_variant": "likelihood_particles_detached_sampling_mean_at_time_43",
  "best_variant_by_gradient_delta": "direct_sampled_distribution",
  "best_variant_max_abs_total_gradient_delta": 5.302734403676368,
  "direct_local_vjp_delta": 28.749898405961705,
  "direct_max_abs_total_gradient_delta": 5.302734403676368,
  "direct_proposal_mean_vjp_delta": 0.0,
  "filterflow_target_scalar": -141.71711568701727,
  "filterflow_total_gradient_diag": [
    9105.143875898348,
    57.123649814928335
  ],
  "global_gap_remaining": true,
  "helper_boundary": {
    "classification": "helper_boundary_material_or_unresolved",
    "fresh_all_variant": "fresh_recomputed_distribution_all_times",
    "helper_all_variant": "helper_function_recomputed_distribution_all_times",
    "max_abs_total_gradient_delta_between_variants": 0.0,
    "max_local_gradient_tensor_delta_between_variants": 28.749898405961705,
    "max_proposal_ll_forward_delta_between_variants": 0.0,
    "not_material": false,
    "row_deltas": [
      {
        "local_gradient_tensor_delta_rows": [
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "target_to_proposal_mean",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 14.48784430419384,
            "name": "target_to_internal_likelihood_mean",
            "sum_delta": -21.262306586037056
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "target_to_proposed_particles",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "proposal_ll_to_proposal_mean",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_internal_likelihood_mean",
            "sum_delta": -17.20700588220021
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "proposal_ll_to_proposed_particles",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "proposal_dist_log_prob_to_proposal_mean",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "proposal_dist_log_prob_to_proposed_particles",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "fresh_dist_log_prob_to_fresh_proposal_mean",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "fresh_dist_log_prob_to_proposed_particles",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "transition_ll_to_proposed_particles",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "observation_ll_to_proposed_particles",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "sample_to_proposal_mean_target_upstream",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "sample_sum_to_proposal_mean",
            "sum_delta": 0.0
          },
          {
            "finite": true,
            "max_abs_delta": 0.0,
            "name": "sample_noise_sum_to_proposal_mean",
            "sum_delta": 0.0
          }
        ],
        "proposal_ll_forward_delta_between_variants": 0.0,
        "proposal_ll_to_proposed_particles_delta_between_variants": 0.0,
        "time_index": 43
      }
    ],
    "scalar_delta_between_variants": 0.0,
    "total_gradient_delta_between_variants": [
      0.0,
      0.0
    ]
  },
  "interpretation": "state_object_topology_required",
  "material_global_reduction": false,
  "primary_matching_variants": [
    "likelihood_particles_detached_sampling_mean_at_time_43",
    "likelihood_particles_detached_sampling_mean_all_times"
  ],
  "status": "compared",
  "variant_comparisons": {
    "detached_sampling_mean_internal_at_time_43": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 4995.545471522408,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 0.0,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 28.749898405961705
      },
      "primary_vjp_matches_filterflow": false,
      "proposal_ll_to_proposed_particles_delta": 0.0,
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
            "max_abs_delta": 2.0,
            "sum_delta": 1000.0
          },
          "filterflow_resampling_flag": [
            true
          ],
          "filterflow_transport_residuals": {
            "column": 1.1102230246251565e-15,
            "row": 9.749830994998376e-06
          },
          "first_adjoint_delta_node": {
            "adjoint_max_abs_delta": 6.570578591668732,
            "node": "pre_particles"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 2.3905124287677584,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": {
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 2.3905124287677584,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.3905124287677584,
              "name": "target_to_proposal_mean",
              "sum_delta": -47.3732090291125
            },
            {
              "bayesfilter_max_abs": 14.487844299484102,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 1.243715781562571e-05,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -2.3195424740104576e-06
            },
            {
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 3.3423958535339082e-06,
              "name": "target_to_proposed_particles",
              "sum_delta": 3.850724550846091e-06
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 28.749898405961705,
              "name": "proposal_ll_to_proposal_mean",
              "sum_delta": -17.20700588220021
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": 0.0
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.3905124287677584,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": -47.3732090291125
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
          "max_adjoint_delta": 1733.9336427308667,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 1733.9336427308667,
            "adjoint_sum_delta": 403359.39428408956,
            "forward_finite": true,
            "forward_max_abs_delta": 9.559442126771955e-11,
            "forward_sum_delta": -1.9627978177769046e-14,
            "node": "transport_matrix"
          },
          "max_forward_delta": 1.1801262189692352e-09,
          "max_forward_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 0.7628675168159019,
            "adjoint_sum_delta": 19.9999913040334,
            "forward_finite": true,
            "forward_max_abs_delta": 1.1801262189692352e-09,
            "forward_sum_delta": 2.8624902448370904e-09,
            "node": "pre_log_weights"
          },
          "max_local_gradient_delta": {
            "bayesfilter_max_abs": 28.749898405961705,
            "filterflow_max_abs": 0.0,
            "finite": true,
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "sum_delta": -17.20700588220021
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 6.570578591668732,
              "adjoint_sum_delta": 19.687765784136495,
              "forward_finite": true,
              "forward_max_abs_delta": 3.06442871078616e-10,
              "forward_sum_delta": 1.8381172139925184e-09,
              "node": "pre_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.7628675168159019,
              "adjoint_sum_delta": 19.9999913040334,
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
              "adjoint_max_abs_delta": 1733.9336427308667,
              "adjoint_sum_delta": 403359.39428408956,
              "forward_finite": true,
              "forward_max_abs_delta": 9.559442126771955e-11,
              "forward_sum_delta": -1.9627978177769046e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 7.863264329351046,
              "adjoint_sum_delta": 49.052342162477814,
              "forward_finite": true,
              "forward_max_abs_delta": 3.6079761400742427e-10,
              "forward_sum_delta": 5.125311730580506e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.3423958535339082e-06,
              "adjoint_sum_delta": 3.850724550846091e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.3905124287677584,
              "adjoint_sum_delta": -47.3732090291125,
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
              "adjoint_max_abs_delta": 1.243715781562571e-05,
              "adjoint_sum_delta": -2.3195424740104576e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.3423958535339082e-06,
              "adjoint_sum_delta": 3.850724550846091e-06,
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
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.362403523330613e-10,
              "forward_sum_delta": 5.972933259101865e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.612754870933713e-10,
              "forward_sum_delta": -1.3622907246713112e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": -1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.49002637689955e-10,
              "forward_sum_delta": -7.649942901366558e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.5565330942263245e-12,
              "forward_sum_delta": 6.5565330942263245e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.433810319446561e-06,
              "adjoint_sum_delta": -7.546608911633427e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 7.555591707841813e-10,
              "forward_sum_delta": -1.092820944847972e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4378542800841387e-10,
              "forward_sum_delta": -1.4378542800841387e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 1733.9336427308667,
            "sum_delta": 403359.39428408956
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.71711568080545,
      "target_scalar_delta": 6.2118203913996695e-09,
      "total_gradient_delta": [
        4995.545471522408,
        -30.226352032160584
      ],
      "total_gradient_diag": [
        14100.689347420755,
        26.89729778276775
      ],
      "wiring_variant": "detached_sampling_mean_internal_at_time_43"
    },
    "direct_sampled_distribution": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 5.302734403676368,
      "max_proposal_ll_forward_delta": 3.028688411177427e-13,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 28.749898405961705,
        "proposal_ll_to_proposed_particles": 28.749898405961705,
        "proposal_ll_to_sampling_proposal_mean": 0.0
      },
      "primary_vjp_matches_filterflow": false,
      "proposal_ll_to_proposed_particles_delta": 28.749898405961705,
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
            "name": "proposal_ll_to_internal_likelihood_mean",
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
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 2.3904999934235462,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -47.373211348865105
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
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": -17.20700588220021
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
            "name": "proposal_ll_to_internal_likelihood_mean",
            "sum_delta": -17.20700588220021
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
              "adjoint_max_abs_delta": 2.3904999934235462,
              "adjoint_sum_delta": -47.373211348865105,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "internal_likelihood_mean"
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
      "target_scalar": -141.71711568080488,
      "target_scalar_delta": 6.2123888255882775e-09,
      "total_gradient_delta": [
        5.302734403676368,
        -0.1337765252068337
      ],
      "total_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ],
      "wiring_variant": "direct_sampled_distribution"
    },
    "fresh_recomputed_distribution_all_times": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 5.306099442515915,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 0.0,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 28.749898405961705
      },
      "primary_vjp_matches_filterflow": false,
      "proposal_ll_to_proposed_particles_delta": 0.0,
      "rows": [
        {
          "bayesfilter_resampling_flag": [
            true
          ],
          "bayesfilter_transport_residuals": {
            "column": 8.881784197001252e-16,
            "row": 9.749829810612454e-06
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
            "adjoint_max_abs_delta": 0.0010679658144567838,
            "node": "transport_matrix"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 2.390512429387744,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": {
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 2.390512429387744,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.390512429387744,
              "name": "target_to_proposal_mean",
              "sum_delta": -47.37320902729254
            },
            {
              "bayesfilter_max_abs": 14.48784430419384,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 1.2443002424866734e-05,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -2.3206152360026513e-06
            },
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 3.343965721325226e-06,
              "name": "target_to_proposed_particles",
              "sum_delta": 3.852544501997679e-06
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 28.749898405961705,
              "name": "proposal_ll_to_proposal_mean",
              "sum_delta": -17.20700588220021
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": 0.0
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 12.33074664276991,
              "filterflow_max_abs": 12.33074664236036,
              "finite": true,
              "max_abs_delta": 1.1585079562337341e-09,
              "name": "transition_ll_to_proposed_particles",
              "sum_delta": 1.4963437114379197e-08
            },
            {
              "bayesfilter_max_abs": 23.75646302678831,
              "filterflow_max_abs": 23.75646302703842,
              "finite": true,
              "max_abs_delta": 1.156763573817443e-09,
              "name": "observation_ll_to_proposed_particles",
              "sum_delta": -1.496118784416467e-08
            },
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.390512429387744,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": -47.37320902729254
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
          "max_adjoint_delta": 14.48784430419384,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 14.48784430419384,
            "adjoint_sum_delta": 21.262306586037056,
            "forward_finite": true,
            "forward_max_abs_delta": 3.1440094971912913e-10,
            "forward_sum_delta": -2.1808546080137603e-09,
            "node": "fresh_proposal_mean"
          },
          "max_forward_delta": 1.1799690113889483e-09,
          "max_forward_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 1.949674310885996e-10,
            "adjoint_sum_delta": 2.6578877987404326e-12,
            "forward_finite": true,
            "forward_max_abs_delta": 1.1799690113889483e-09,
            "forward_sum_delta": 2.855670366841423e-09,
            "node": "pre_log_weights"
          },
          "max_local_gradient_delta": {
            "bayesfilter_max_abs": 28.749898405961705,
            "filterflow_max_abs": 0.0,
            "finite": true,
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "sum_delta": -17.20700588220021
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.2984257686809997e-06,
              "adjoint_sum_delta": -2.907241130267399e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.0684077501064166e-10,
              "forward_sum_delta": 1.84738269126683e-09,
              "node": "pre_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.949674310885996e-10,
              "adjoint_sum_delta": 2.6578877987404326e-12,
              "forward_finite": true,
              "forward_max_abs_delta": 1.1799690113889483e-09,
              "forward_sum_delta": 2.855670366841423e-09,
              "node": "pre_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 4.419131727217973e-12,
              "forward_sum_delta": 4.419131727217973e-12,
              "node": "log_ess"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0010679658144567838,
              "adjoint_sum_delta": -0.25139783299841234,
              "forward_finite": true,
              "forward_max_abs_delta": 9.544676160544441e-11,
              "forward_sum_delta": -2.104638433780053e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 4.843456829051185e-06,
              "adjoint_sum_delta": -2.9070303095304895e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.611564380889831e-10,
              "forward_sum_delta": 5.134577207854818e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.343965721325226e-06,
              "adjoint_sum_delta": 3.852544501997679e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.390512429387744,
              "adjoint_sum_delta": -47.37320902729254,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.48784430419384,
              "adjoint_sum_delta": 21.262306586037056,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "fresh_proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.2443002424866734e-05,
              "adjoint_sum_delta": -2.3206152360026513e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.343965721325226e-06,
              "adjoint_sum_delta": 3.852544501997679e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
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
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.368301028037422e-10,
              "forward_sum_delta": 5.997011776059935e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.594191941961981e-10,
              "forward_sum_delta": -1.355233036903769e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": -3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 0.9890545604054324,
              "adjoint_sum_delta": -1.000000000000001,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "fresh_dist_log_prob"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.470610796644905e-10,
              "forward_sum_delta": -7.555325254315903e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.6560090772327385e-12,
              "forward_sum_delta": 6.6560090772327385e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.434953797481043e-06,
              "adjoint_sum_delta": -7.550154501719908e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 7.537170887417233e-10,
              "forward_sum_delta": -1.0883329792932273e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4418333194043953e-10,
              "forward_sum_delta": -1.4418333194043953e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 0.0010679658144567838,
            "sum_delta": -0.25139783299841234
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.7171156808077,
      "target_scalar_delta": 6.2095750763546675e-09,
      "total_gradient_delta": [
        5.306099442515915,
        -0.13386141801179008
      ],
      "total_gradient_diag": [
        9110.449975340864,
        56.989788396916545
      ],
      "wiring_variant": "fresh_recomputed_distribution_all_times"
    },
    "fresh_recomputed_distribution_at_time_43": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 5.303606461880918,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 0.0,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 28.749898405961705
      },
      "primary_vjp_matches_filterflow": false,
      "proposal_ll_to_proposed_particles_delta": 0.0,
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
            "adjoint_max_abs_delta": 5.500608568276989,
            "node": "pre_particles"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 2.3905124287677584,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": {
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 2.3905124287677584,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.3905124287677584,
              "name": "target_to_proposal_mean",
              "sum_delta": -47.3732090291125
            },
            {
              "bayesfilter_max_abs": 14.487844299484102,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 1.243715781562571e-05,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -2.3195424740104576e-06
            },
            {
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 3.3423958535339082e-06,
              "name": "target_to_proposed_particles",
              "sum_delta": 3.850724550846091e-06
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 28.749898405961705,
              "name": "proposal_ll_to_proposal_mean",
              "sum_delta": -17.20700588220021
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": 0.0
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.3905124287677584,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": -47.3732090291125
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
          "max_adjoint_delta": 14.487844299484102,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 14.487844299484102,
            "adjoint_sum_delta": 21.26230658710982,
            "forward_finite": true,
            "forward_max_abs_delta": 3.1445779313798994e-10,
            "forward_sum_delta": -2.176051339120022e-09,
            "node": "fresh_proposal_mean"
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
            "bayesfilter_max_abs": 28.749898405961705,
            "filterflow_max_abs": 0.0,
            "finite": true,
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "sum_delta": -17.20700588220021
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 5.500608568276989,
              "adjoint_sum_delta": -24.423658482599496,
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
              "adjoint_max_abs_delta": 0.0010674644310313397,
              "adjoint_sum_delta": -0.25127968651199417,
              "forward_finite": true,
              "forward_max_abs_delta": 9.559442126771955e-11,
              "forward_sum_delta": -1.9627978177769046e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 4.841182943138289e-06,
              "adjoint_sum_delta": -2.905664029659305e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.6079761400742427e-10,
              "forward_sum_delta": 5.125311730580506e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.3423958535339082e-06,
              "adjoint_sum_delta": 3.850724550846091e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.3905124287677584,
              "adjoint_sum_delta": -47.3732090291125,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.487844299484102,
              "adjoint_sum_delta": 21.26230658710982,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "fresh_proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.243715781562571e-05,
              "adjoint_sum_delta": -2.3195424740104576e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.3423958535339082e-06,
              "adjoint_sum_delta": 3.850724550846091e-06,
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
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.362403523330613e-10,
              "forward_sum_delta": 5.972933259101865e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.612754870933713e-10,
              "forward_sum_delta": -1.3622907246713112e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": -1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 0.9890545600839085,
              "adjoint_sum_delta": -1.0000000000000002,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "fresh_dist_log_prob"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.49002637689955e-10,
              "forward_sum_delta": -7.649942901366558e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.5565330942263245e-12,
              "forward_sum_delta": 6.5565330942263245e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.433810319446561e-06,
              "adjoint_sum_delta": -7.546608911633427e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 7.555591707841813e-10,
              "forward_sum_delta": -1.092820944847972e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4378542800841387e-10,
              "forward_sum_delta": -1.4378542800841387e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 0.0010674644310313397,
            "sum_delta": -0.25127968651199417
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.71711568080545,
      "target_scalar_delta": 6.2118203913996695e-09,
      "total_gradient_delta": [
        5.303606461880918,
        -0.13379852573832096
      ],
      "total_gradient_diag": [
        9110.447482360229,
        56.989851289190014
      ],
      "wiring_variant": "fresh_recomputed_distribution_at_time_43"
    },
    "helper_function_recomputed_distribution_all_times": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 5.306099442515915,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 28.749898405961705,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 28.749898405961705
      },
      "primary_vjp_matches_filterflow": false,
      "proposal_ll_to_proposed_particles_delta": 0.0,
      "rows": [
        {
          "bayesfilter_resampling_flag": [
            true
          ],
          "bayesfilter_transport_residuals": {
            "column": 8.881784197001252e-16,
            "row": 9.749829810612454e-06
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
            "adjoint_max_abs_delta": 0.0010679658144567838,
            "node": "transport_matrix"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 2.390512429387744,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": {
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 2.390512429387744,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.390512429387744,
              "name": "target_to_proposal_mean",
              "sum_delta": -47.37320902729254
            },
            {
              "bayesfilter_max_abs": 0.0,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 14.4878343008842,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -21.2623089066523
            },
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 3.343965721325226e-06,
              "name": "target_to_proposed_particles",
              "sum_delta": 3.852544501997679e-06
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 28.749898405961705,
              "name": "proposal_ll_to_proposal_mean",
              "sum_delta": -17.20700588220021
            },
            {
              "bayesfilter_max_abs": 0.0,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 28.749898405961705,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": -17.20700588220021
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 12.33074664276991,
              "filterflow_max_abs": 12.33074664236036,
              "finite": true,
              "max_abs_delta": 1.1585079562337341e-09,
              "name": "transition_ll_to_proposed_particles",
              "sum_delta": 1.4963437114379197e-08
            },
            {
              "bayesfilter_max_abs": 23.75646302678831,
              "filterflow_max_abs": 23.75646302703842,
              "finite": true,
              "max_abs_delta": 1.156763573817443e-09,
              "name": "observation_ll_to_proposed_particles",
              "sum_delta": -1.496118784416467e-08
            },
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.390512429387744,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": -47.37320902729254
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
          "max_adjoint_delta": 14.4878343008842,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 14.4878343008842,
            "adjoint_sum_delta": -21.2623089066523,
            "forward_finite": true,
            "forward_max_abs_delta": 3.1440094971912913e-10,
            "forward_sum_delta": -2.1808546080137603e-09,
            "node": "internal_likelihood_mean"
          },
          "max_forward_delta": 1.1799690113889483e-09,
          "max_forward_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 1.949674310885996e-10,
            "adjoint_sum_delta": 2.6578877987404326e-12,
            "forward_finite": true,
            "forward_max_abs_delta": 1.1799690113889483e-09,
            "forward_sum_delta": 2.855670366841423e-09,
            "node": "pre_log_weights"
          },
          "max_local_gradient_delta": {
            "bayesfilter_max_abs": 28.749898405961705,
            "filterflow_max_abs": 0.0,
            "finite": true,
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "sum_delta": -17.20700588220021
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.2984257686809997e-06,
              "adjoint_sum_delta": -2.907241130267399e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.0684077501064166e-10,
              "forward_sum_delta": 1.84738269126683e-09,
              "node": "pre_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.949674310885996e-10,
              "adjoint_sum_delta": 2.6578877987404326e-12,
              "forward_finite": true,
              "forward_max_abs_delta": 1.1799690113889483e-09,
              "forward_sum_delta": 2.855670366841423e-09,
              "node": "pre_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 4.419131727217973e-12,
              "forward_sum_delta": 4.419131727217973e-12,
              "node": "log_ess"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0010679658144567838,
              "adjoint_sum_delta": -0.25139783299841234,
              "forward_finite": true,
              "forward_max_abs_delta": 9.544676160544441e-11,
              "forward_sum_delta": -2.104638433780053e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 4.843456829051185e-06,
              "adjoint_sum_delta": -2.9070303095304895e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.611564380889831e-10,
              "forward_sum_delta": 5.134577207854818e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.343965721325226e-06,
              "adjoint_sum_delta": 3.852544501997679e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.390512429387744,
              "adjoint_sum_delta": -47.37320902729254,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "fresh_proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.4878343008842,
              "adjoint_sum_delta": -21.2623089066523,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.343965721325226e-06,
              "adjoint_sum_delta": 3.852544501997679e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
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
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.368301028037422e-10,
              "forward_sum_delta": 5.997011776059935e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.594191941961981e-10,
              "forward_sum_delta": -1.355233036903769e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": -3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.470610796644905e-10,
              "forward_sum_delta": -7.555325254315903e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.6560090772327385e-12,
              "forward_sum_delta": 6.6560090772327385e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.434953797481043e-06,
              "adjoint_sum_delta": -7.550154501719908e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 7.537170887417233e-10,
              "forward_sum_delta": -1.0883329792932273e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4418333194043953e-10,
              "forward_sum_delta": -1.4418333194043953e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 0.0010679658144567838,
            "sum_delta": -0.25139783299841234
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.7171156808077,
      "target_scalar_delta": 6.2095750763546675e-09,
      "total_gradient_delta": [
        5.306099442515915,
        -0.13386141801179008
      ],
      "total_gradient_diag": [
        9110.449975340864,
        56.989788396916545
      ],
      "wiring_variant": "helper_function_recomputed_distribution_all_times"
    },
    "likelihood_particles_detached_sampling_mean_all_times": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 3729.0941878293434,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 0.0,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 0.0
      },
      "primary_vjp_matches_filterflow": true,
      "proposal_ll_to_proposed_particles_delta": 0.0,
      "rows": [
        {
          "bayesfilter_resampling_flag": [
            true
          ],
          "bayesfilter_transport_residuals": {
            "column": 8.881784197001252e-16,
            "row": 9.749829810612454e-06
          },
          "clip_count_delta": 0.0,
          "clip_mask_mismatch_count": 0,
          "clipped_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 2.0,
            "sum_delta": -1200.0
          },
          "filterflow_resampling_flag": [
            true
          ],
          "filterflow_transport_residuals": {
            "column": 1.1102230246251565e-15,
            "row": 9.749830994998376e-06
          },
          "first_adjoint_delta_node": {
            "adjoint_max_abs_delta": 3.3707864237479734,
            "node": "pre_particles"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 8.622280601377469,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": null,
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 8.622280601377469,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 8.622280601377469,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 8.622280601377469,
              "name": "target_to_proposal_mean",
              "sum_delta": -4.570862885269387
            },
            {
              "bayesfilter_max_abs": 8.420767937860203,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 22.670693029428435,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -34.90776690602296
            },
            {
              "bayesfilter_max_abs": 0.9910506356918151,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 2.592023773498907,
              "name": "target_to_proposed_particles",
              "sum_delta": 56.44780799393832
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
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": 0.0
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 12.33074664276991,
              "filterflow_max_abs": 12.33074664236036,
              "finite": true,
              "max_abs_delta": 1.1585079562337341e-09,
              "name": "transition_ll_to_proposed_particles",
              "sum_delta": 1.4963437114379197e-08
            },
            {
              "bayesfilter_max_abs": 23.75646302678831,
              "filterflow_max_abs": 23.75646302703842,
              "finite": true,
              "max_abs_delta": 1.156763573817443e-09,
              "name": "observation_ll_to_proposed_particles",
              "sum_delta": -1.496118784416467e-08
            },
            {
              "bayesfilter_max_abs": 0.9910506356918151,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 0.9910506356918151,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": 9.074595114101273
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
          "max_adjoint_delta": 1947.641319766725,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 1947.641319766725,
            "adjoint_sum_delta": -64205.40943599083,
            "forward_finite": true,
            "forward_max_abs_delta": 9.544676160544441e-11,
            "forward_sum_delta": -2.104638433780053e-14,
            "node": "transport_matrix"
          },
          "max_forward_delta": 1.1799690113889483e-09,
          "max_forward_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 1.411612433482981,
            "adjoint_sum_delta": -23.999952840404127,
            "forward_finite": true,
            "forward_max_abs_delta": 1.1799690113889483e-09,
            "forward_sum_delta": 2.855670366841423e-09,
            "node": "pre_log_weights"
          },
          "max_local_gradient_delta": {
            "bayesfilter_max_abs": 8.420767937860203,
            "filterflow_max_abs": 14.4878343008842,
            "finite": true,
            "max_abs_delta": 22.670693029428435,
            "name": "target_to_internal_likelihood_mean",
            "sum_delta": -34.90776690602296
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.3707864237479734,
              "adjoint_sum_delta": 0.08928143579468695,
              "forward_finite": true,
              "forward_max_abs_delta": 3.0684077501064166e-10,
              "forward_sum_delta": 1.84738269126683e-09,
              "node": "pre_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.411612433482981,
              "adjoint_sum_delta": -23.999952840404127,
              "forward_finite": true,
              "forward_max_abs_delta": 1.1799690113889483e-09,
              "forward_sum_delta": 2.855670366841423e-09,
              "node": "pre_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 4.419131727217973e-12,
              "forward_sum_delta": 4.419131727217973e-12,
              "node": "log_ess"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1947.641319766725,
              "adjoint_sum_delta": -64205.40943599083,
              "forward_finite": true,
              "forward_max_abs_delta": 9.544676160544441e-11,
              "forward_sum_delta": -2.104638433780053e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 8.785421111275701,
              "adjoint_sum_delta": 0.25672828202257936,
              "forward_finite": true,
              "forward_max_abs_delta": 3.611564380889831e-10,
              "forward_sum_delta": 5.134577207854818e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.9762063279406918,
              "adjoint_sum_delta": 3.552713678800501e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 11.01279171135911,
              "adjoint_sum_delta": 42.80234999456765,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 8.622280601377469,
              "adjoint_sum_delta": -4.570862885269387,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 8.420767937860203,
              "adjoint_sum_delta": -13.645457999370665,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "fresh_proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 22.670693029428435,
              "adjoint_sum_delta": -34.90776690602296,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.592023773498907,
              "adjoint_sum_delta": 56.44780799393832,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
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
              "adjoint_max_abs_delta": 1.9762063279406918,
              "adjoint_sum_delta": 3.552713678800501e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.368301028037422e-10,
              "forward_sum_delta": 5.997011776059935e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.9762063279406918,
              "adjoint_sum_delta": 3.552713678800501e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.594191941961981e-10,
              "forward_sum_delta": -1.355233036903769e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.9762063279406918,
              "adjoint_sum_delta": -3.552713678800501e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 1.9762063279406918,
              "adjoint_sum_delta": 3.552713678800501e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.470610796644905e-10,
              "forward_sum_delta": -7.555325254315903e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.6560090772327385e-12,
              "forward_sum_delta": 6.6560090772327385e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.810013679473901,
              "adjoint_sum_delta": -6.534151165302896,
              "forward_finite": true,
              "forward_max_abs_delta": 7.537170887417233e-10,
              "forward_sum_delta": -1.0883329792932273e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4418333194043953e-10,
              "forward_sum_delta": -1.4418333194043953e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 1947.641319766725,
            "sum_delta": -64205.40943599083
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.7171156808077,
      "target_scalar_delta": 6.2095750763546675e-09,
      "total_gradient_delta": [
        3729.0941878293434,
        276.07691011775063
      ],
      "total_gradient_diag": [
        12834.238063727691,
        333.20055993267897
      ],
      "wiring_variant": "likelihood_particles_detached_sampling_mean_all_times"
    },
    "likelihood_particles_detached_sampling_mean_at_time_43": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 544.9274396565979,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 0.0,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 0.0
      },
      "primary_vjp_matches_filterflow": true,
      "proposal_ll_to_proposed_particles_delta": 0.0,
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
            "max_abs_delta": 2.0,
            "sum_delta": -400.0
          },
          "filterflow_resampling_flag": [
            true
          ],
          "filterflow_transport_residuals": {
            "column": 1.1102230246251565e-15,
            "row": 9.749830994998376e-06
          },
          "first_adjoint_delta_node": {
            "adjoint_max_abs_delta": 4.515390564097784,
            "node": "pre_particles"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 14.888157522566043,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": null,
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 14.888157522566043,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 14.888157522566043,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 14.888157522566043,
              "name": "target_to_proposal_mean",
              "sum_delta": -26.110902442002676
            },
            {
              "bayesfilter_max_abs": 14.487844299484102,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 1.243715781562571e-05,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -2.3195424740104576e-06
            },
            {
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 3.342395853422886e-06,
              "name": "target_to_proposed_particles",
              "sum_delta": 3.850724551526102e-06
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
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": 0.0
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.3905124287677584,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": -47.3732090291125
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
          "max_adjoint_delta": 1733.932837488822,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 1733.932837488822,
            "adjoint_sum_delta": -403359.89684346266,
            "forward_finite": true,
            "forward_max_abs_delta": 9.559442126771955e-11,
            "forward_sum_delta": -1.9627978177769046e-14,
            "node": "transport_matrix"
          },
          "max_forward_delta": 1.1801262189692352e-09,
          "max_forward_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 0.2714740936688117,
            "adjoint_sum_delta": -7.999998597877518,
            "forward_finite": true,
            "forward_max_abs_delta": 1.1801262189692352e-09,
            "forward_sum_delta": 2.8624902448370904e-09,
            "node": "pre_log_weights"
          },
          "max_local_gradient_delta": {
            "bayesfilter_max_abs": 14.888157522566043,
            "filterflow_max_abs": 0.0,
            "finite": true,
            "max_abs_delta": 14.888157522566043,
            "name": "target_to_proposal_mean",
            "sum_delta": -26.110902442002676
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 4.515390564097784,
              "adjoint_sum_delta": -76.4577596771987,
              "forward_finite": true,
              "forward_max_abs_delta": 3.06442871078616e-10,
              "forward_sum_delta": 1.8381172139925184e-09,
              "node": "pre_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.2714740936688117,
              "adjoint_sum_delta": -7.999998597877518,
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
              "adjoint_max_abs_delta": 1733.932837488822,
              "adjoint_sum_delta": -403359.89684346266,
              "forward_finite": true,
              "forward_max_abs_delta": 9.559442126771955e-11,
              "forward_sum_delta": -1.9627978177769046e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 7.863260742789592,
              "adjoint_sum_delta": -49.05240027575841,
              "forward_finite": true,
              "forward_max_abs_delta": 3.6079761400742427e-10,
              "forward_sum_delta": 5.125311730580506e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.487844450085998,
              "adjoint_sum_delta": 21.262310437834373,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.888157522566043,
              "adjoint_sum_delta": -26.110902442002676,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.487844299484102,
              "adjoint_sum_delta": 21.26230658710982,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "fresh_proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.243715781562571e-05,
              "adjoint_sum_delta": -2.3195424740104576e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.342395853422886e-06,
              "adjoint_sum_delta": 3.850724551526102e-06,
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
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.362403523330613e-10,
              "forward_sum_delta": 5.972933259101865e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.612754870933713e-10,
              "forward_sum_delta": -1.3622907246713112e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": -1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.49002637689955e-10,
              "forward_sum_delta": -7.649942901366558e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.5565330942263245e-12,
              "forward_sum_delta": 6.5565330942263245e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.433810319446561e-06,
              "adjoint_sum_delta": -7.546608911633427e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 7.555591707841813e-10,
              "forward_sum_delta": -1.092820944847972e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4378542800841387e-10,
              "forward_sum_delta": -1.4378542800841387e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 1733.932837488822,
            "sum_delta": -403359.89684346266
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.71711568080545,
      "target_scalar_delta": 6.2118203913996695e-09,
      "total_gradient_delta": [
        -544.9274396565979,
        217.2238286974801
      ],
      "total_gradient_diag": [
        8560.21643624175,
        274.34747851240843
      ],
      "wiring_variant": "likelihood_particles_detached_sampling_mean_at_time_43"
    },
    "official_internal_mean_all_times": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 5.306099442515915,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 0.0,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 28.749898405961705
      },
      "primary_vjp_matches_filterflow": false,
      "proposal_ll_to_proposed_particles_delta": 0.0,
      "rows": [
        {
          "bayesfilter_resampling_flag": [
            true
          ],
          "bayesfilter_transport_residuals": {
            "column": 8.881784197001252e-16,
            "row": 9.749829810612454e-06
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
            "adjoint_max_abs_delta": 0.0010679658144567838,
            "node": "transport_matrix"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 2.390512429387744,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": {
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 2.390512429387744,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.390512429387744,
              "name": "target_to_proposal_mean",
              "sum_delta": -47.37320902729254
            },
            {
              "bayesfilter_max_abs": 14.48784430419384,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 1.2443002424866734e-05,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -2.3206152360026513e-06
            },
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 3.343965721325226e-06,
              "name": "target_to_proposed_particles",
              "sum_delta": 3.852544501997679e-06
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 28.749898405961705,
              "name": "proposal_ll_to_proposal_mean",
              "sum_delta": -17.20700588220021
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": 0.0
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 12.33074664276991,
              "filterflow_max_abs": 12.33074664236036,
              "finite": true,
              "max_abs_delta": 1.1585079562337341e-09,
              "name": "transition_ll_to_proposed_particles",
              "sum_delta": 1.4963437114379197e-08
            },
            {
              "bayesfilter_max_abs": 23.75646302678831,
              "filterflow_max_abs": 23.75646302703842,
              "finite": true,
              "max_abs_delta": 1.156763573817443e-09,
              "name": "observation_ll_to_proposed_particles",
              "sum_delta": -1.496118784416467e-08
            },
            {
              "bayesfilter_max_abs": 2.390512429387744,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.390512429387744,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": -47.37320902729254
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
          "max_adjoint_delta": 14.48784430419384,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 14.48784430419384,
            "adjoint_sum_delta": 21.262306586037056,
            "forward_finite": true,
            "forward_max_abs_delta": 3.1440094971912913e-10,
            "forward_sum_delta": -2.1808546080137603e-09,
            "node": "fresh_proposal_mean"
          },
          "max_forward_delta": 1.1799690113889483e-09,
          "max_forward_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 1.949674310885996e-10,
            "adjoint_sum_delta": 2.6578877987404326e-12,
            "forward_finite": true,
            "forward_max_abs_delta": 1.1799690113889483e-09,
            "forward_sum_delta": 2.855670366841423e-09,
            "node": "pre_log_weights"
          },
          "max_local_gradient_delta": {
            "bayesfilter_max_abs": 28.749898405961705,
            "filterflow_max_abs": 0.0,
            "finite": true,
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "sum_delta": -17.20700588220021
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.2984257686809997e-06,
              "adjoint_sum_delta": -2.907241130267399e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.0684077501064166e-10,
              "forward_sum_delta": 1.84738269126683e-09,
              "node": "pre_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.949674310885996e-10,
              "adjoint_sum_delta": 2.6578877987404326e-12,
              "forward_finite": true,
              "forward_max_abs_delta": 1.1799690113889483e-09,
              "forward_sum_delta": 2.855670366841423e-09,
              "node": "pre_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 4.419131727217973e-12,
              "forward_sum_delta": 4.419131727217973e-12,
              "node": "log_ess"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0010679658144567838,
              "adjoint_sum_delta": -0.25139783299841234,
              "forward_finite": true,
              "forward_max_abs_delta": 9.544676160544441e-11,
              "forward_sum_delta": -2.104638433780053e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 4.843456829051185e-06,
              "adjoint_sum_delta": -2.9070303095304895e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.611564380889831e-10,
              "forward_sum_delta": 5.134577207854818e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.343965721325226e-06,
              "adjoint_sum_delta": 3.852544501997679e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.390512429387744,
              "adjoint_sum_delta": -47.37320902729254,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.48784430419384,
              "adjoint_sum_delta": 21.262306586037056,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "fresh_proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.2443002424866734e-05,
              "adjoint_sum_delta": -2.3206152360026513e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.343965721325226e-06,
              "adjoint_sum_delta": 3.852544501997679e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1440094971912913e-10,
              "forward_sum_delta": -2.1808546080137603e-09,
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
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.368301028037422e-10,
              "forward_sum_delta": 5.997011776059935e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.594191941961981e-10,
              "forward_sum_delta": -1.355233036903769e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": -3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 0.9890545604054324,
              "adjoint_sum_delta": -1.000000000000001,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "fresh_dist_log_prob"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5831496854579186e-06,
              "adjoint_sum_delta": 3.3080363535248347e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.470610796644905e-10,
              "forward_sum_delta": -7.555325254315903e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.6560090772327385e-12,
              "forward_sum_delta": 6.6560090772327385e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.434953797481043e-06,
              "adjoint_sum_delta": -7.550154501719908e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 7.537170887417233e-10,
              "forward_sum_delta": -1.0883329792932273e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4418333194043953e-10,
              "forward_sum_delta": -1.4418333194043953e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 0.0010679658144567838,
            "sum_delta": -0.25139783299841234
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.7171156808077,
      "target_scalar_delta": 6.2095750763546675e-09,
      "total_gradient_delta": [
        5.306099442515915,
        -0.13386141801179008
      ],
      "total_gradient_diag": [
        9110.449975340864,
        56.989788396916545
      ],
      "wiring_variant": "official_internal_mean_all_times"
    },
    "official_internal_mean_at_time_43": {
      "all_adjoints_finite": true,
      "all_forward_finite": true,
      "all_local_gradients_finite": true,
      "all_resampling_flags_match": true,
      "finite_gradient": true,
      "finite_scalar": true,
      "max_abs_total_gradient_delta": 5.303606461880918,
      "max_proposal_ll_forward_delta": 0.0,
      "primary_vjp_deltas": {
        "proposal_ll_to_internal_likelihood_mean": 0.0,
        "proposal_ll_to_proposed_particles": 0.0,
        "proposal_ll_to_sampling_proposal_mean": 28.749898405961705
      },
      "primary_vjp_matches_filterflow": false,
      "proposal_ll_to_proposed_particles_delta": 0.0,
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
            "adjoint_max_abs_delta": 5.500608568276989,
            "node": "pre_particles"
          },
          "first_forward_delta_node": null,
          "first_local_gradient_delta": {
            "max_abs_delta": 2.3905124287677584,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_log_prob_gradient_delta": {
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "tolerance": 0.0002
          },
          "first_sample_gradient_delta": null,
          "first_target_adjoint_gradient_delta": {
            "max_abs_delta": 2.3905124287677584,
            "name": "target_to_proposal_mean",
            "tolerance": 0.0002
          },
          "local_gradient_rows": [
            {
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.3905124287677584,
              "name": "target_to_proposal_mean",
              "sum_delta": -47.3732090291125
            },
            {
              "bayesfilter_max_abs": 14.487844299484102,
              "filterflow_max_abs": 14.4878343008842,
              "finite": true,
              "max_abs_delta": 1.243715781562571e-05,
              "name": "target_to_internal_likelihood_mean",
              "sum_delta": -2.3195424740104576e-06
            },
            {
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 2.3905111099816416,
              "finite": true,
              "max_abs_delta": 3.3423958535339082e-06,
              "name": "target_to_proposed_particles",
              "sum_delta": 3.850724550846091e-06
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 28.749898405961705,
              "name": "proposal_ll_to_proposal_mean",
              "sum_delta": -17.20700588220021
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_internal_likelihood_mean",
              "sum_delta": 0.0
            },
            {
              "bayesfilter_max_abs": 28.749898405961705,
              "filterflow_max_abs": 28.749898405961705,
              "finite": true,
              "max_abs_delta": 0.0,
              "name": "proposal_ll_to_proposed_particles",
              "sum_delta": 0.0
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
              "bayesfilter_max_abs": 2.3905124287677584,
              "filterflow_max_abs": 0.0,
              "finite": true,
              "max_abs_delta": 2.3905124287677584,
              "name": "sample_to_proposal_mean_target_upstream",
              "sum_delta": -47.3732090291125
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
          "max_adjoint_delta": 14.487844299484102,
          "max_adjoint_delta_node": {
            "adjoint_finite": true,
            "adjoint_max_abs_delta": 14.487844299484102,
            "adjoint_sum_delta": 21.26230658710982,
            "forward_finite": true,
            "forward_max_abs_delta": 3.1445779313798994e-10,
            "forward_sum_delta": -2.176051339120022e-09,
            "node": "fresh_proposal_mean"
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
            "bayesfilter_max_abs": 28.749898405961705,
            "filterflow_max_abs": 0.0,
            "finite": true,
            "max_abs_delta": 28.749898405961705,
            "name": "proposal_ll_to_proposal_mean",
            "sum_delta": -17.20700588220021
          },
          "node_rows": [
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 5.500608568276989,
              "adjoint_sum_delta": -24.423658482599496,
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
              "adjoint_max_abs_delta": 0.0010674644310313397,
              "adjoint_sum_delta": -0.25127968651199417,
              "forward_finite": true,
              "forward_max_abs_delta": 9.559442126771955e-11,
              "forward_sum_delta": -1.9627978177769046e-14,
              "node": "transport_matrix"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 4.841182943138289e-06,
              "adjoint_sum_delta": -2.905664029659305e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 3.6079761400742427e-10,
              "forward_sum_delta": 5.125311730580506e-09,
              "node": "post_particles"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "post_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.3423958535339082e-06,
              "adjoint_sum_delta": 3.850724550846091e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "proposal_loc"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.3905124287677584,
              "adjoint_sum_delta": -47.3732090291125,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 14.487844299484102,
              "adjoint_sum_delta": 21.26230658710982,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "fresh_proposal_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.243715781562571e-05,
              "adjoint_sum_delta": -2.3195424740104576e-06,
              "forward_finite": true,
              "forward_max_abs_delta": 3.1445779313798994e-10,
              "forward_sum_delta": -2.176051339120022e-09,
              "node": "internal_likelihood_mean"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 3.3423958535339082e-06,
              "adjoint_sum_delta": 3.850724550846091e-06,
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
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 1.362403523330613e-10,
              "forward_sum_delta": 5.972933259101865e-10,
              "node": "observation_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.612754870933713e-10,
              "forward_sum_delta": -1.3622907246713112e-09,
              "node": "transition_ll"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": -1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
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
              "adjoint_max_abs_delta": 0.9890545600839085,
              "adjoint_sum_delta": -1.0000000000000002,
              "forward_finite": true,
              "forward_max_abs_delta": 0.0,
              "forward_sum_delta": 0.0,
              "node": "fresh_dist_log_prob"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 1.5824060634050952e-06,
              "adjoint_sum_delta": 1.7383284482003214e-15,
              "forward_finite": true,
              "forward_max_abs_delta": 7.49002637689955e-10,
              "forward_sum_delta": -7.649942901366558e-10,
              "node": "unnormalized"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 6.5565330942263245e-12,
              "forward_sum_delta": 6.5565330942263245e-12,
              "node": "increment"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 2.433810319446561e-06,
              "adjoint_sum_delta": -7.546608911633427e-05,
              "forward_finite": true,
              "forward_max_abs_delta": 7.555591707841813e-10,
              "forward_sum_delta": -1.092820944847972e-09,
              "node": "normalized_log_weights"
            },
            {
              "adjoint_finite": true,
              "adjoint_max_abs_delta": 0.0,
              "adjoint_sum_delta": 0.0,
              "forward_finite": true,
              "forward_max_abs_delta": 1.4378542800841387e-10,
              "forward_sum_delta": -1.4378542800841387e-10,
              "node": "post_log_likelihoods"
            }
          ],
          "raw_transport_upstream_delta": {
            "finite": true,
            "max_abs_delta": 0.0010674644310313397,
            "sum_delta": -0.25127968651199417
          },
          "resampling_flags_match": true,
          "time_index": 43
        }
      ],
      "status": "compared",
      "target_scalar": -141.71711568080545,
      "target_scalar_delta": 6.2118203913996695e-09,
      "total_gradient_delta": [
        5.303606461880918,
        -0.13379852573832096
      ],
      "total_gradient_diag": [
        9110.447482360229,
        56.989851289190014
      ],
      "wiring_variant": "official_internal_mean_at_time_43"
    }
  },
  "variant_order": [
    "direct_sampled_distribution",
    "official_internal_mean_at_time_43",
    "official_internal_mean_all_times",
    "detached_sampling_mean_internal_at_time_43",
    "likelihood_particles_detached_sampling_mean_at_time_43",
    "likelihood_particles_detached_sampling_mean_all_times",
    "fresh_recomputed_distribution_at_time_43",
    "fresh_recomputed_distribution_all_times",
    "helper_function_recomputed_distribution_all_times"
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
  "all_variant_gradients_finite": true,
  "all_vetoes_clear": true,
  "comparator_drift": false,
  "cpu_only_parent": true,
  "helper_boundary_not_material_explanatory": false,
  "path_boundary_clean": true,
  "proposal_ll_value_gate_pass": true,
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
        "proposal_ll_to_internal_likelihood_mean": {
          "finite": true,
          "max_abs": 28.749898405961705,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 17.20700588220021
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
        "target_to_internal_likelihood_mean": {
          "finite": true,
          "max_abs": 14.4878343008842,
          "shape": [
            1,
            50,
            2
          ],
          "sum": 21.2623089066523
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
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-05 05:05:50.613084: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780607150.624301     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780607150.627515     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780607150.637814     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780607150.637867     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780607150.637872     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780607150.637873     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-05 05:05:50.640998: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-05 05:05:52.797367: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
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
  "variant_summaries": {
    "detached_sampling_mean_internal_at_time_43": {
      "finite_gradient": true,
      "finite_scalar": true,
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
            "proposal_ll_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 17.20700588220021
            },
            "proposal_ll_to_proposal_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -17.20700588220021
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
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
            },
            "target_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 14.487844299484102,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 21.26230658710982
            },
            "target_to_proposal_mean": {
              "finite": true,
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
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
      "target_scalar": -141.71711568080545,
      "total_gradient_diag": [
        14100.689347420755,
        26.89729778276775
      ]
    },
    "direct_sampled_distribution": {
      "finite_gradient": true,
      "finite_scalar": true,
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
            "proposal_ll_to_internal_likelihood_mean": {
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
            "target_to_internal_likelihood_mean": {
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
      "target_scalar": -141.71711568080488,
      "total_gradient_diag": [
        9110.446610302024,
        56.9898732897215
      ]
    },
    "fresh_recomputed_distribution_all_times": {
      "finite_gradient": true,
      "finite_scalar": true,
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
              "sum": 26.403815288753663
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
            "proposal_ll_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 17.20700588220021
            },
            "proposal_ll_to_proposal_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -17.20700588220021
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
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "target_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 14.48784430419384,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 21.262306586037056
            },
            "target_to_proposal_mean": {
              "finite": true,
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "transition_ll_to_proposed_particles": {
              "finite": true,
              "max_abs": 12.33074664276991,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -43.610821170903336
            }
          },
          "time_index": 43
        }
      ],
      "probe_times": [
        43
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        9110.449975340864,
        56.989788396916545
      ]
    },
    "fresh_recomputed_distribution_at_time_43": {
      "finite_gradient": true,
      "finite_scalar": true,
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
            "proposal_ll_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 17.20700588220021
            },
            "proposal_ll_to_proposal_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -17.20700588220021
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
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
            },
            "target_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 14.487844299484102,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 21.26230658710982
            },
            "target_to_proposal_mean": {
              "finite": true,
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
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
      "target_scalar": -141.71711568080545,
      "total_gradient_diag": [
        9110.447482360229,
        56.989851289190014
      ]
    },
    "helper_function_recomputed_distribution_all_times": {
      "finite_gradient": true,
      "finite_scalar": true,
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
              "sum": 26.403815288753663
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
            "proposal_ll_to_internal_likelihood_mean": {
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
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -17.20700588220021
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
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "target_to_internal_likelihood_mean": {
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
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "transition_ll_to_proposed_particles": {
              "finite": true,
              "max_abs": 12.33074664276991,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -43.610821170903336
            }
          },
          "time_index": 43
        }
      ],
      "probe_times": [
        43
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        9110.449975340864,
        56.989788396916545
      ]
    },
    "likelihood_particles_detached_sampling_mean_all_times": {
      "finite_gradient": true,
      "finite_scalar": true,
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
              "sum": 26.403815288753663
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
            "proposal_ll_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 17.20700588220021
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
              "max_abs": 0.9910506356918151,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 9.074595114101273
            },
            "target_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 8.420767937860203,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -13.645457999370665
            },
            "target_to_proposal_mean": {
              "finite": true,
              "max_abs": 8.622280601377469,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -4.570862885269387
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 0.9910506356918151,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 9.074595114101273
            },
            "transition_ll_to_proposed_particles": {
              "finite": true,
              "max_abs": 12.33074664276991,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -43.610821170903336
            }
          },
          "time_index": 43
        }
      ],
      "probe_times": [
        43
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        12834.238063727691,
        333.20055993267897
      ]
    },
    "likelihood_particles_detached_sampling_mean_at_time_43": {
      "finite_gradient": true,
      "finite_scalar": true,
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
            "proposal_ll_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 17.20700588220021
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
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
            },
            "target_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 14.487844299484102,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 21.26230658710982
            },
            "target_to_proposal_mean": {
              "finite": true,
              "max_abs": 14.888157522566043,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -26.110902442002676
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
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
      "target_scalar": -141.71711568080545,
      "total_gradient_diag": [
        8560.21643624175,
        274.34747851240843
      ]
    },
    "official_internal_mean_all_times": {
      "finite_gradient": true,
      "finite_scalar": true,
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
              "sum": 26.403815288753663
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
            "proposal_ll_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 17.20700588220021
            },
            "proposal_ll_to_proposal_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -17.20700588220021
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
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "target_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 14.48784430419384,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 21.262306586037056
            },
            "target_to_proposal_mean": {
              "finite": true,
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 2.390512429387744,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.37320902729254
            },
            "transition_ll_to_proposed_particles": {
              "finite": true,
              "max_abs": 12.33074664276991,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -43.610821170903336
            }
          },
          "time_index": 43
        }
      ],
      "probe_times": [
        43
      ],
      "target_scalar": -141.7171156808077,
      "total_gradient_diag": [
        9110.449975340864,
        56.989788396916545
      ]
    },
    "official_internal_mean_at_time_43": {
      "finite_gradient": true,
      "finite_scalar": true,
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
            "proposal_ll_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 17.20700588220021
            },
            "proposal_ll_to_proposal_mean": {
              "finite": true,
              "max_abs": 28.749898405961705,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -17.20700588220021
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
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
            },
            "target_to_internal_likelihood_mean": {
              "finite": true,
              "max_abs": 14.487844299484102,
              "shape": [
                1,
                50,
                2
              ],
              "sum": 21.26230658710982
            },
            "target_to_proposal_mean": {
              "finite": true,
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
            },
            "target_to_proposed_particles": {
              "finite": true,
              "max_abs": 2.3905124287677584,
              "shape": [
                1,
                50,
                2
              ],
              "sum": -47.3732090291125
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
      "target_scalar": -141.71711568080545,
      "total_gradient_diag": [
        9110.447482360229,
        56.989851289190014
      ]
    }
  }
}
```

## Non-Implications

- No correctness claim is made for either implementation.
- No analytic gradient correctness is concluded.
- No posterior correctness is concluded.
- No global gradient agreement is concluded.
- No full mesh or surface agreement is concluded.
- No production readiness or public API readiness is concluded.
- No preferred BayesFilter algorithm is concluded from this diagnostic.
