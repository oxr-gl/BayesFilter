# Result: Row 173 Direct-Theta Hypothesis Test

## Decision

`filterflow_float64_row_173_direct_theta_not_source`

## Interpretation

`h4_current_step_direct_derivatives_match_under_frozen_sample`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_direct_theta_not_source | h4_current_step_direct_derivatives_match_under_frozen_sample | none | single row/time direct-gradient probe; no correctness claim | move the cut-set one boundary upstream or downstream because current direct term is not the source | correctness of either implementation, production readiness, analytic gradient correctness |

## Best Rows

```json
{
  "best_core_row": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "row": "theta_vector:frozen_sample",
    "term": "unnormalized_core"
  },
  "best_increment_row": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "row": "theta_vector:frozen_sample",
    "term": "increment"
  },
  "observed_total_gradient_delta": [
    5.302734403676368,
    -0.1337765252068337
  ]
}
```

## Term Delta Rows

```json
{
  "full_matrix:active_sample:increment": {
    "gradient_delta": [
      2.887645678129047e-11,
      2.0747847884194925e-12
    ],
    "max_abs_gradient_delta": 2.887645678129047e-11,
    "max_abs_residual_after_subtracting_from_observed": 5.3027344036474915,
    "residual_after_subtracting_from_observed": [
      5.3027344036474915,
      -0.13377652520890848
    ]
  },
  "full_matrix:active_sample:observation_ll": {
    "gradient_delta": [
      21.153855858142315,
      4.245308512970539e-18
    ],
    "max_abs_gradient_delta": 21.153855858142315,
    "max_abs_residual_after_subtracting_from_observed": 15.851121454465947,
    "residual_after_subtracting_from_observed": [
      -15.851121454465947,
      -0.1337765252068337
    ]
  },
  "full_matrix:active_sample:proposal_ll": {
    "gradient_delta": [
      597.7316769373439,
      -19.680133739960443
    ],
    "max_abs_gradient_delta": 597.7316769373439,
    "max_abs_residual_after_subtracting_from_observed": 592.4289425336675,
    "residual_after_subtracting_from_observed": [
      -592.4289425336675,
      19.54635721475361
    ]
  },
  "full_matrix:active_sample:proposal_mean": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "full_matrix:active_sample:transition_ll": {
    "gradient_delta": [
      -618.8855327954575,
      19.68013373996252
    ],
    "max_abs_gradient_delta": 618.8855327954575,
    "max_abs_residual_after_subtracting_from_observed": 624.1882671991339,
    "residual_after_subtracting_from_observed": [
      624.1882671991339,
      -19.813910265169355
    ]
  },
  "full_matrix:active_sample:unnormalized": {
    "gradient_delta": [
      2.887645678129047e-11,
      2.0747847884194925e-12
    ],
    "max_abs_gradient_delta": 2.887645678129047e-11,
    "max_abs_residual_after_subtracting_from_observed": 5.3027344036474915,
    "residual_after_subtracting_from_observed": [
      5.3027344036474915,
      -0.13377652520890848
    ]
  },
  "full_matrix:active_sample:unnormalized_core": {
    "gradient_delta": [
      2.887645678129047e-11,
      2.0747847884194925e-12
    ],
    "max_abs_gradient_delta": 2.887645678129047e-11,
    "max_abs_residual_after_subtracting_from_observed": 5.3027344036474915,
    "residual_after_subtracting_from_observed": [
      5.3027344036474915,
      -0.13377652520890848
    ]
  },
  "full_matrix:frozen_sample:increment": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "full_matrix:frozen_sample:observation_ll": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "full_matrix:frozen_sample:proposal_ll": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "full_matrix:frozen_sample:proposal_mean": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "full_matrix:frozen_sample:transition_ll": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "full_matrix:frozen_sample:unnormalized": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "full_matrix:frozen_sample:unnormalized_core": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:active_sample:increment": {
    "gradient_delta": [
      2.887645678129047e-11,
      2.0747847884194925e-12
    ],
    "max_abs_gradient_delta": 2.887645678129047e-11,
    "max_abs_residual_after_subtracting_from_observed": 5.3027344036474915,
    "residual_after_subtracting_from_observed": [
      5.3027344036474915,
      -0.13377652520890848
    ]
  },
  "theta_vector:active_sample:observation_ll": {
    "gradient_delta": [
      21.153855858142315,
      4.245308512970539e-18
    ],
    "max_abs_gradient_delta": 21.153855858142315,
    "max_abs_residual_after_subtracting_from_observed": 15.851121454465947,
    "residual_after_subtracting_from_observed": [
      -15.851121454465947,
      -0.1337765252068337
    ]
  },
  "theta_vector:active_sample:proposal_ll": {
    "gradient_delta": [
      597.7316769373439,
      -19.680133739960443
    ],
    "max_abs_gradient_delta": 597.7316769373439,
    "max_abs_residual_after_subtracting_from_observed": 592.4289425336675,
    "residual_after_subtracting_from_observed": [
      -592.4289425336675,
      19.54635721475361
    ]
  },
  "theta_vector:active_sample:proposal_mean": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:active_sample:transition_ll": {
    "gradient_delta": [
      -618.8855327954575,
      19.68013373996252
    ],
    "max_abs_gradient_delta": 618.8855327954575,
    "max_abs_residual_after_subtracting_from_observed": 624.1882671991339,
    "residual_after_subtracting_from_observed": [
      624.1882671991339,
      -19.813910265169355
    ]
  },
  "theta_vector:active_sample:unnormalized": {
    "gradient_delta": [
      2.887645678129047e-11,
      2.0747847884194925e-12
    ],
    "max_abs_gradient_delta": 2.887645678129047e-11,
    "max_abs_residual_after_subtracting_from_observed": 5.3027344036474915,
    "residual_after_subtracting_from_observed": [
      5.3027344036474915,
      -0.13377652520890848
    ]
  },
  "theta_vector:active_sample:unnormalized_core": {
    "gradient_delta": [
      2.887645678129047e-11,
      2.0747847884194925e-12
    ],
    "max_abs_gradient_delta": 2.887645678129047e-11,
    "max_abs_residual_after_subtracting_from_observed": 5.3027344036474915,
    "residual_after_subtracting_from_observed": [
      5.3027344036474915,
      -0.13377652520890848
    ]
  },
  "theta_vector:frozen_sample:increment": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:frozen_sample:observation_ll": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:frozen_sample:proposal_ll": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:frozen_sample:proposal_mean": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:frozen_sample:transition_ll": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:frozen_sample:unnormalized": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  },
  "theta_vector:frozen_sample:unnormalized_core": {
    "gradient_delta": [
      0.0,
      0.0
    ],
    "max_abs_gradient_delta": 0.0,
    "max_abs_residual_after_subtracting_from_observed": 5.302734403676368,
    "residual_after_subtracting_from_observed": [
      5.302734403676368,
      -0.1337765252068337
    ]
  }
}
```

## Direct Row Comparison

```json
{
  "filterflow_full_matrix:active_sample": {
    "all_gradient_finite": true,
    "filterflow_term_gradients": {
      "increment": [
        286.3674760142072,
        -3.552713678800501e-15
      ],
      "observation_ll": [
        21.153855858142315,
        4.245308512970539e-18
      ],
      "proposal_ll": [
        0.0,
        0.0
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        265.21362015606474,
        0.0
      ],
      "unnormalized": [
        286.3674760142072,
        -3.552713678800501e-15
      ],
      "unnormalized_core": [
        286.3674760142072,
        -3.552713678800501e-15
      ]
    },
    "gradient_deltas": {
      "increment": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ],
      "observation_ll": [
        21.153855858142315,
        4.245308512970539e-18
      ],
      "proposal_ll": [
        597.7316769373439,
        -19.680133739960443
      ],
      "proposal_mean": [
        0.0,
        0.0
      ],
      "transition_ll": [
        -618.8855327954575,
        19.68013373996252
      ],
      "unnormalized": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ],
      "unnormalized_core": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ]
    },
    "max_gradient_delta": 618.8855327954575,
    "max_value_delta": 0.0,
    "parameterization": "full_matrix",
    "sample_mode": "unknown",
    "status": "filterflow_internal_control",
    "value_deltas": {
      "increment": 0.0,
      "observation_ll": 0.0,
      "proposal_ll": 0.0,
      "proposal_mean": 0.0,
      "proposed_particles": 0.0,
      "transition_ll": 0.0,
      "unnormalized": 0.0,
      "unnormalized_core": 0.0
    }
  },
  "filterflow_full_matrix:frozen_sample": {
    "all_gradient_finite": true,
    "filterflow_term_gradients": {
      "increment": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        -597.7316769373439,
        19.680133739960443
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        884.0991529515222,
        -19.68013373996252
      ],
      "unnormalized": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "unnormalized_core": [
        286.36747601417835,
        -2.078337502098293e-12
      ]
    },
    "gradient_deltas": {
      "increment": [
        0.0,
        0.0
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        0.0,
        0.0
      ],
      "proposal_mean": [
        0.0,
        0.0
      ],
      "transition_ll": [
        0.0,
        0.0
      ],
      "unnormalized": [
        0.0,
        0.0
      ],
      "unnormalized_core": [
        0.0,
        0.0
      ]
    },
    "max_gradient_delta": 0.0,
    "max_value_delta": 0.0,
    "parameterization": "full_matrix",
    "sample_mode": "unknown",
    "status": "filterflow_internal_control",
    "value_deltas": {
      "increment": 0.0,
      "observation_ll": 0.0,
      "proposal_ll": 0.0,
      "proposal_mean": 0.0,
      "proposed_particles": 0.0,
      "transition_ll": 0.0,
      "unnormalized": 0.0,
      "unnormalized_core": 0.0
    }
  },
  "full_matrix:active_sample": {
    "all_gradient_finite": true,
    "bayesfilter_term_gradients": {
      "increment": [
        286.3674760142072,
        -3.552713678800501e-15
      ],
      "observation_ll": [
        21.153855858142315,
        4.245308512970539e-18
      ],
      "proposal_ll": [
        0.0,
        0.0
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        265.21362015606474,
        0.0
      ],
      "unnormalized": [
        286.3674760142072,
        -3.552713678800501e-15
      ],
      "unnormalized_core": [
        286.3674760142072,
        -3.552713678800501e-15
      ]
    },
    "filterflow_term_gradients": {
      "increment": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        -597.7316769373439,
        19.680133739960443
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        884.0991529515222,
        -19.68013373996252
      ],
      "unnormalized": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "unnormalized_core": [
        286.36747601417835,
        -2.078337502098293e-12
      ]
    },
    "gradient_deltas": {
      "increment": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ],
      "observation_ll": [
        21.153855858142315,
        4.245308512970539e-18
      ],
      "proposal_ll": [
        597.7316769373439,
        -19.680133739960443
      ],
      "proposal_mean": [
        0.0,
        0.0
      ],
      "transition_ll": [
        -618.8855327954575,
        19.68013373996252
      ],
      "unnormalized": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ],
      "unnormalized_core": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ]
    },
    "max_gradient_delta": 618.8855327954575,
    "max_value_delta": 0.0,
    "parameterization": "full_matrix",
    "sample_mode": "active_sample",
    "status": "compared",
    "value_deltas": {
      "increment": 0.0,
      "observation_ll": 0.0,
      "proposal_ll": 0.0,
      "proposal_mean": 0.0,
      "proposed_particles": 0.0,
      "transition_ll": 0.0,
      "unnormalized": 0.0,
      "unnormalized_core": 0.0
    }
  },
  "full_matrix:frozen_sample": {
    "all_gradient_finite": true,
    "bayesfilter_term_gradients": {
      "increment": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        -597.7316769373439,
        19.680133739960443
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        884.0991529515222,
        -19.68013373996252
      ],
      "unnormalized": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "unnormalized_core": [
        286.36747601417835,
        -2.078337502098293e-12
      ]
    },
    "filterflow_term_gradients": {
      "increment": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        -597.7316769373439,
        19.680133739960443
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        884.0991529515222,
        -19.68013373996252
      ],
      "unnormalized": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "unnormalized_core": [
        286.36747601417835,
        -2.078337502098293e-12
      ]
    },
    "gradient_deltas": {
      "increment": [
        0.0,
        0.0
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        0.0,
        0.0
      ],
      "proposal_mean": [
        0.0,
        0.0
      ],
      "transition_ll": [
        0.0,
        0.0
      ],
      "unnormalized": [
        0.0,
        0.0
      ],
      "unnormalized_core": [
        0.0,
        0.0
      ]
    },
    "max_gradient_delta": 0.0,
    "max_value_delta": 0.0,
    "parameterization": "full_matrix",
    "sample_mode": "frozen_sample",
    "status": "compared",
    "value_deltas": {
      "increment": 0.0,
      "observation_ll": 0.0,
      "proposal_ll": 0.0,
      "proposal_mean": 0.0,
      "proposed_particles": 0.0,
      "transition_ll": 0.0,
      "unnormalized": 0.0,
      "unnormalized_core": 0.0
    }
  },
  "theta_vector:active_sample": {
    "all_gradient_finite": true,
    "bayesfilter_term_gradients": {
      "increment": [
        286.3674760142072,
        -3.552713678800501e-15
      ],
      "observation_ll": [
        21.153855858142315,
        4.245308512970539e-18
      ],
      "proposal_ll": [
        0.0,
        0.0
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        265.21362015606474,
        0.0
      ],
      "unnormalized": [
        286.3674760142072,
        -3.552713678800501e-15
      ],
      "unnormalized_core": [
        286.3674760142072,
        -3.552713678800501e-15
      ]
    },
    "filterflow_term_gradients": {
      "increment": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        -597.7316769373439,
        19.680133739960443
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        884.0991529515222,
        -19.68013373996252
      ],
      "unnormalized": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "unnormalized_core": [
        286.36747601417835,
        -2.078337502098293e-12
      ]
    },
    "gradient_deltas": {
      "increment": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ],
      "observation_ll": [
        21.153855858142315,
        4.245308512970539e-18
      ],
      "proposal_ll": [
        597.7316769373439,
        -19.680133739960443
      ],
      "proposal_mean": [
        0.0,
        0.0
      ],
      "transition_ll": [
        -618.8855327954575,
        19.68013373996252
      ],
      "unnormalized": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ],
      "unnormalized_core": [
        2.887645678129047e-11,
        2.0747847884194925e-12
      ]
    },
    "max_gradient_delta": 618.8855327954575,
    "max_value_delta": 0.0,
    "parameterization": "theta_vector",
    "sample_mode": "active_sample",
    "status": "compared",
    "value_deltas": {
      "increment": 0.0,
      "observation_ll": 0.0,
      "proposal_ll": 0.0,
      "proposal_mean": 0.0,
      "proposed_particles": 0.0,
      "transition_ll": 0.0,
      "unnormalized": 0.0,
      "unnormalized_core": 0.0
    }
  },
  "theta_vector:frozen_sample": {
    "all_gradient_finite": true,
    "bayesfilter_term_gradients": {
      "increment": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        -597.7316769373439,
        19.680133739960443
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        884.0991529515222,
        -19.68013373996252
      ],
      "unnormalized": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "unnormalized_core": [
        286.36747601417835,
        -2.078337502098293e-12
      ]
    },
    "filterflow_term_gradients": {
      "increment": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        -597.7316769373439,
        19.680133739960443
      ],
      "proposal_mean": [
        2.8914798179045254e-11,
        2.076122093761108e-12
      ],
      "transition_ll": [
        884.0991529515222,
        -19.68013373996252
      ],
      "unnormalized": [
        286.36747601417835,
        -2.078337502098293e-12
      ],
      "unnormalized_core": [
        286.36747601417835,
        -2.078337502098293e-12
      ]
    },
    "gradient_deltas": {
      "increment": [
        0.0,
        0.0
      ],
      "observation_ll": [
        0.0,
        0.0
      ],
      "proposal_ll": [
        0.0,
        0.0
      ],
      "proposal_mean": [
        0.0,
        0.0
      ],
      "transition_ll": [
        0.0,
        0.0
      ],
      "unnormalized": [
        0.0,
        0.0
      ],
      "unnormalized_core": [
        0.0,
        0.0
      ]
    },
    "max_gradient_delta": 0.0,
    "max_value_delta": 0.0,
    "parameterization": "theta_vector",
    "sample_mode": "frozen_sample",
    "status": "compared",
    "value_deltas": {
      "increment": 0.0,
      "observation_ll": 0.0,
      "proposal_ll": 0.0,
      "proposal_mean": 0.0,
      "proposed_particles": 0.0,
      "transition_ll": 0.0,
      "unnormalized": 0.0,
      "unnormalized_core": 0.0
    }
  }
}
```

## Run Manifest

```json
{
  "branch": "main",
  "command": "CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_direct_theta_hypothesis_tf",
  "commit": "7ccb9c39883471c2d5ec2891cbf33b9ed436bada",
  "cpu_only": true,
  "cuda_visible_devices": "-1",
  "dirty_state_summary": "M docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md\n M docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md\n M docs/references.bib\n M experiments/controlled_dpf_baseline/README.md\n?? .cache/\n?? .claude/\n?? .local_sources/\n?? .localenv/\n?? .localsource/\n?? AGENTS.md\n?? CLAUDE.md\n?? bayesfilter/highdim/\n?? docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-review-loop-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-plan-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-result-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-review-loop-2026-06-01.md\n?? docs/plans/bayesfilter-dpf-exact-arithmetic-continuation-debug-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-exact-arithmetic-continuation-debug-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-full-surface-window-coverage-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-plan-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-review-loop-2026-06-04.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-debug-summary-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-boundary-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-92-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-94-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-row-gradient-discrepancy-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-0-19-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-100-119-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-120-139-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-140-159-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-160-179-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-180-199-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-20-39-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-200-219-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-220-239-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-240-259-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-260-279-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-280-299-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-300-319-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-320-339-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-340-359-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-360-379-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-380-399-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-40-59-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-60-79-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-80-99-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-result-2026-05-31.md\n?? docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-py311-compat-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-py311-compat-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-citation-coverage-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-extraction-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-doc-patch-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-baseline-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-reference-test-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf1-student-comparison-context-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-bias-proxy-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-deferred-neural-path-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-differentiable-resampling-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-resampling-test-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf2-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-excluded-flow-risk-register-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-kernel-pff-exclusion-check-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-particle-flow-pfpf-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf3-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-differentiable-objective-gradient-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-downstream-evidence-requirements-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-objective-classification-ledger-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf4-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-benchmark-ladder-matrix-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-cpu-gpu-runtime-policy-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-seed-uncertainty-policy-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-benchmark-ladder-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-spec-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-api-review-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-decision-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf6-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-dpf7-final-audit-implementation-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-final-audit-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-handoff-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-implementation-sv-test-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-master-program-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-ladder-master-program-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-ot-backend-governance-correction-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-backend-governance-correction-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p0-scope-and-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p0-scope-and-contract-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-plan-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-result-2026-05-30.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-master-program-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-result-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md\n?? docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-review-loop-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-plan-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-result-2026-06-02.md\n?? docs/plans/bayesfilter-dpf-structural-ar1-linear-mle-test-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ar1-linear-mle-test-result-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ssm-interface-plan-2026-05-29.md\n?? docs/plans/bayesfilter-dpf-structural-ssm-interface-result-2026-05-29.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase-subplans-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-result-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-subplan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-addenda-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-claude-review-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-promotion-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-filtering-scalar-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-gradient-feasibility-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-mathdevmcp-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-octave-compatibility-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-octave-compatibility-result-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-reproducibility-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-plan-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-result-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-claude-review-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-derivation-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-mathdevmcp-ledger-2026-05-30.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claim-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-coverage-and-omission-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-proposition-proof-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-anchor-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-proposition-humanization-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-reader-comprehension-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-gradient-teaching-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-reader-panel-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-algorithm-choices-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-backward-snowball-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-citation-venue-metadata-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-claim-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-claude-review-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-discrepancy-report-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-forward-snowball-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-gradient-derivation-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-plan-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-result-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-omitted-paper-risk-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-reference-example-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-source-support-ledger-2026-05-31.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-backward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-bayesfilter-translation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claim-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-code-crosswalk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-equation-by-equation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-fixed-branch-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-forward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-gradient-derivation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-fixed-branch-derivative-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-inventory-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section1-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section2-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section3-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-section5-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-backward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-claim-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-eight-issue-control-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-equation-count-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-fixed-branch-gradient-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-forward-snowball-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section1-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section2-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section3-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-section5-source-unit-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-source-support-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-inventory-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-finite-difference-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-fixed-branch-scalar-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-gradient-equation-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-gradient-teaching-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-mathdevmcp-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-claude-review-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-discrepancy-report-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-equation-and-size-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-plan-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-result-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-merge-ledger-2026-06-01.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-teachability-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-equation-to-specification-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-finite-difference-protocol-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-fixed-branch-implementation-ready-spec-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-full-algorithm-gap-register-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-implementation-readiness-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-implementation-specification-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integration-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-readable-orientation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-eleven-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-p22-preservation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-backward-snowball-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-chair-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-citation-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-citation-venue-metadata-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-claim-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-forward-snowball-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-cleanup-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-implementation-gap-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-omitted-paper-risk-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-source-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-plan-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-result-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-claim-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-claude-review-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-discrepancy-report-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-five-gap-closure-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-source-support-ledger-2026-06-02.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-chemist-gap-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-human-facing-cleanup-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-implementation-gap-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-validation-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-chair-reader-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-equation-audit-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-implementation-readiness-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-notation-dimension-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-numerical-sanity-test-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-source-fidelity-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-submission-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p28-submission-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-algorithm-provenance-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-critical-equation-audit-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-critical-equation-audit-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-kr-preconditioning-jacobian-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-mass-normalizer-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-notation-shape-contract-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p29-proposition2-derivative-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-expansion-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-gradient-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-discrepancy-report-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.pdf\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-gradient-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-source-support-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-validation-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-standard-upgrade-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-scholarly-grounding-and-engineering-exposition-remediation-plan-2026-06-04.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-conclusion-and-panel-positioning-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-gradient-path-implementation-completeness-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-neighboring-method-comparison-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-opening-and-conceptual-spine-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-value-path-implementation-completeness-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-worked-example-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-claude-review-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-mathdevmcp-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-plan-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-result-2026-06-03.md\n?? docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-source-ledger-2026-06-03.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-audit-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-result-2026-05-27.md\n?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-review-2026-05-27.md\n?? experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md\n?? experiments/dpf_implementation/\n?? tests/highdim/\n?? third_party/",
  "gpu_devices_visible": [],
  "package_versions": {
    "tensorflow": "2.19.1",
    "tensorflow_probability": "0.25.0"
  },
  "pre_import_cuda_visible_devices": "-1",
  "python_version": "3.11.14",
  "wall_time_seconds": 21.05202948092483
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
- This is a difference audit only; no claim is made that either side is correct.
- A direct-term match or mismatch does not establish global smoothness-gradient correctness.
- The local float64 FilterFlow checkout is the executable comparator for this lane, not pristine upstream.

## JSON Output

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_direct_theta_hypothesis_2026-06-04.json`
