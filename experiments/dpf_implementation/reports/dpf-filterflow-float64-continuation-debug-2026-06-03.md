# Filterflow Float64 Continuation Debug

## Decision

`filterflow_float64_continuation_no_mismatch_observed`

## First Cells

| Field | Value |
| --- | --- |
| first failing cell | `{'rung_id': 'none_observed', 'cell_index': -1, 'cell_id': 'none_observed'}` |
| first blocked cell | `{'rung_id': 'none_observed', 'cell_index': -1, 'cell_id': 'none_observed'}` |

## Reference

| Key | Value |
| --- | --- |
| `future_comparator` | `filterflow_float64_reference_branch` |
| `branch` | `bayesfilter-py311-float64-reference` |
| `commit` | `1e5fbc288c1c11fc18ba01bb4842832e2088b800` |
| `upstream_base` | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| `dtype` | `float64` |
| `local_reference_status` | `BayesFilter audit reference code, not pristine upstream` |
| `transition_covariance` | `I_2 executable reproduction setting` |
| `fixed_target_sinkhorn` | `local BayesFilter diagnostic/comparator only` |

## Rung Ledger

| Rung | Status | Evidence-bearing | Direct failure | Scalar delta | Max field delta | Blocker |
| --- | --- | --- | --- | ---: | ---: | --- |
| `R0_controlled_1d_T2` | `pass` | `True` | `False` | `0.0` | `1.1102230246251565e-16` | `None` |
| `R1_controlled_1d_T4` | `pass` | `True` | `False` | `0.0` | `4.440892098500626e-16` | `None` |
| `R2_filterflow_observation_path_T100` | `pass` | `True` | `False` | `0.0` | `2.9103830456733704e-11` | `None` |
| `R3_filterflow_initial_particles_T100` | `pass` | `True` | `False` | `0.0` | `1.1102230246251565e-14` | `None` |
| `R4_filterflow_2d_trace_replay` | `pass` | `True` | `False` | `N/A` | `N/A` | `None` |

## Evidence Details

### R0_controlled_1d_T2

Changed axis: baseline controlled scalar-state T=2

```json
{
  "explanatory_diagnostics": {
    "bayesfilter_finite_difference_gradient": -1.6753548204218038,
    "bayesfilter_gradient_tape": -1.7820385507243621,
    "filterflow_finite_difference_gradient": -1.6753548204218038,
    "filterflow_gradient_tape": -1.7820385507243621,
    "first_failure": {
      "field_set": [],
      "status": "no_field_failure",
      "time_index": null,
      "triggered": false
    },
    "gradient_promotion": "not_concluded"
  },
  "primary_metrics": {
    "bayesfilter_max_column_residual": 4.440892098500626e-16,
    "bayesfilter_max_row_residual": 3.77402173978858e-06,
    "bayesfilter_scalar": 0.06241077425770425,
    "column_residual_delta": 0.0,
    "filterflow_max_column_residual": 4.440892098500626e-16,
    "filterflow_max_row_residual": 3.77402173978858e-06,
    "filterflow_scalar": 0.06241077425770425,
    "implementation_agreement": true,
    "ledger_within_tolerance": true,
    "max_field_delta": 1.1102230246251565e-16,
    "row_residual_delta": 0.0,
    "scalar_delta": 0.0,
    "scalar_within_tolerance": true,
    "trigger_match": true
  }
}
```

### R1_controlled_1d_T4

Changed axis: controlled scalar-state horizon extended to T=4

```json
{
  "explanatory_diagnostics": {
    "bayesfilter_finite_difference_gradient": -1.9368130259955763,
    "bayesfilter_gradient_tape": -2.246140845103192,
    "filterflow_finite_difference_gradient": -1.9368130259955763,
    "filterflow_gradient_tape": -2.246171981702727,
    "first_failure": {
      "field_set": [],
      "status": "no_field_failure",
      "time_index": null,
      "triggered": false
    },
    "gradient_promotion": "not_concluded"
  },
  "primary_metrics": {
    "bayesfilter_max_column_residual": 4.440892098500626e-16,
    "bayesfilter_max_row_residual": 0.0005233019270021178,
    "bayesfilter_scalar": 1.297762090249853,
    "column_residual_delta": 0.0,
    "filterflow_max_column_residual": 4.440892098500626e-16,
    "filterflow_max_row_residual": 0.0005233019270021178,
    "filterflow_scalar": 1.297762090249853,
    "implementation_agreement": true,
    "ledger_within_tolerance": true,
    "max_field_delta": 4.440892098500626e-16,
    "row_residual_delta": 0.0,
    "scalar_delta": 0.0,
    "scalar_within_tolerance": true,
    "trigger_match": true
  }
}
```

### R2_filterflow_observation_path_T100

Changed axis: observations switched to executable float64 filterflow fixture path

```json
{
  "explanatory_diagnostics": {
    "bayesfilter_finite_difference_gradient": 1466200.2070248127,
    "bayesfilter_gradient_tape": -5.281543288090485e+90,
    "filterflow_finite_difference_gradient": 1466200.2070248127,
    "filterflow_gradient_tape": 1467598.9420375386,
    "first_failure": {
      "field_set": [],
      "status": "no_field_failure",
      "time_index": null,
      "triggered": false
    },
    "gradient_promotion": "not_concluded"
  },
  "primary_metrics": {
    "bayesfilter_max_column_residual": 8.881784197001252e-16,
    "bayesfilter_max_row_residual": 2.488568462410967e-09,
    "bayesfilter_scalar": -103553524.57435603,
    "column_residual_delta": 0.0,
    "filterflow_max_column_residual": 8.881784197001252e-16,
    "filterflow_max_row_residual": 2.488569572633992e-09,
    "filterflow_scalar": -103553524.57435603,
    "implementation_agreement": true,
    "ledger_within_tolerance": true,
    "max_field_delta": 2.9103830456733704e-11,
    "row_residual_delta": 1.1102230246251565e-15,
    "scalar_delta": 0.0,
    "scalar_within_tolerance": true,
    "trigger_match": true
  }
}
```

### R3_filterflow_initial_particles_T100

Changed axis: initial particles switched to executable float64 filterflow fixture draw

```json
{
  "explanatory_diagnostics": {
    "bayesfilter_finite_difference_gradient": 1473588.8357460499,
    "bayesfilter_gradient_tape": -1.923353652277926e+91,
    "filterflow_finite_difference_gradient": 1473588.8357460499,
    "filterflow_gradient_tape": 1475117.7701472612,
    "first_failure": {
      "field_set": [],
      "status": "no_field_failure",
      "time_index": null,
      "triggered": false
    },
    "gradient_promotion": "not_concluded"
  },
  "primary_metrics": {
    "bayesfilter_max_column_residual": 8.881784197001252e-16,
    "bayesfilter_max_row_residual": 8.726600611241864e-06,
    "bayesfilter_scalar": -103552831.4836906,
    "column_residual_delta": 0.0,
    "filterflow_max_column_residual": 8.881784197001252e-16,
    "filterflow_max_row_residual": 8.726600611241864e-06,
    "filterflow_scalar": -103552831.4836906,
    "implementation_agreement": true,
    "ledger_within_tolerance": true,
    "max_field_delta": 1.1102230246251565e-14,
    "row_residual_delta": 0.0,
    "scalar_delta": 0.0,
    "scalar_within_tolerance": true,
    "trigger_match": true
  }
}
```

### R4_filterflow_2d_trace_replay

Changed axis: 2D filterflow transition proposal trace replay

```json
{
  "explanatory_diagnostics": {
    "float64_trace_replay_status": "The continuation runner consumes the no-runtime-shim float64 R3 trace/replay helper as the evidence-bearing R4 rung.",
    "source_audit": {
      "float32_token_count": 0,
      "float64_ready": true,
      "interpretation": "Float64 R3 helper has no obvious float32 tokens.",
      "source_digest": "b8851ff9365fde059e90640e9145160c65db4c9885677996ac8ce1a43ffe8c1f"
    },
    "traced_transport_matrix_comparison": {
      "finite_bayesfilter_replay": true,
      "first_failure": {
        "status": "no_failure"
      },
      "implementation_agreement": true,
      "per_time_deltas": [
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 0
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 1
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 2
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 3
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 4
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 5
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 6
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 7
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 8
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 9
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 10
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 11
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 12
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 13
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 14
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 15
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 16
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 17
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 18
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 19
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 20
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 21
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 22
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 23
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 24
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 25
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 26
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 27
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 28
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 29
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 30
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 31
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 32
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 33
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 34
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 35
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 36
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 37
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 38
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 39
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 40
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 41
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 42
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 43
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 44
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 45
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 46
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 47
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 48
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 49
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 50
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 51
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 52
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 53
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 54
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 55
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 56
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 57
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 58
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 59
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 60
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 61
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 62
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 63
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 64
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 65
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 66
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 67
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 68
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 69
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 70
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 71
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 72
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 73
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 74
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 75
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 76
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 77
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 78
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 79
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 80
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 81
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 82
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 83
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 84
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 85
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 86
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 87
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 88
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 89
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 90
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 91
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 92
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 93
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 94
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 95
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 96
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 97
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 98
        },
        {
          "deltas": {
            "log_likelihood_increment": 0.0,
            "observation_log_likelihoods": 0.0,
            "post_resample_log_weights": 0.0,
            "post_resample_particles": 0.0,
            "post_update_log_likelihoods": 0.0,
            "post_update_log_weights": 0.0,
            "proposal_log_likelihoods": 0.0,
            "transition_log_likelihoods": 0.0
          },
          "failing_fields": [],
          "time_index": 99
        }
      ],
      "resampling_flags_match": true,
      "series_deltas": {
        "log_likelihoods": 0.0,
        "log_weights": 0.0,
        "particles": 0.0
      },
      "status": "compared"
    }
  },
  "primary_metrics": {
    "decision": "filterflow_r3_float64_trace_replay_pass",
    "first_failure": {
      "status": "no_failure"
    },
    "implementation_agreement": true,
    "runtime_shims": [],
    "series_deltas": {
      "log_likelihoods": 1.5979679801603197e-09,
      "log_weights": 2.572270396683507e-09,
      "particles": 0.0
    },
    "trace_contract": "external_eager_loop_reproduces_official_filterflow_before_replay_without_runtime_shims"
  }
}
```

## Interpretation

No direct difference or blocker was observed in the bounded ladder.

## Non-Implications

- No mathematical correctness claim for either implementation.
- No production readiness claim.
- No public API readiness claim.
- No posterior correctness claim.
- No gradient correctness claim.
- No general nonlinear-SSM validation claim.
- No DSGE/NAWM validation claim.
- No monograph claim.
- Fixed-target Sinkhorn remains a local BayesFilter diagnostic only.
