# Result: 1D-to-Smoothness LGSSM Continuation Ladder

## Decision

`one_d_to_smoothness_ladder_protocol_blocked_inspection_only`

Technical observation: `one_d_to_smoothness_ladder_R2_veto`

Protocol status: `blocked_inspection_only_nonaccepted_plan`

Downstream use: blocked until the plan is accepted in a reviewed loop or the human explicitly authorizes this inspection-only artifact as sufficient

Plan review status: `REJECT_patched_for_user_inspection_after_round_5`

| Field | Value |
| --- | --- |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `R3_1d_particle_count_ladder` |
| selected inherited setting | `{'convergence_threshold': 1e-06, 'max_iterations': 500, 'max_absolute_row_residual': 1.4204764579250906e-05, 'max_absolute_column_residual': 1.1920928955078125e-07}` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `one_d_to_smoothness_ladder_protocol_blocked_inspection_only` | `protocol blocked; technical R1/R2 prefix executed` | `R2 T=32 residual veto; plan review non-acceptance veto` | `whether R2 failure is fixture-specific, horizon-specific, or transport convergence/annealing-specific` | `reopen plan review or obtain explicit human authorization, then isolate R2 T=32 residual with horizon/cost/iteration diagnostics` | `full smoothness alignment, production readiness, gradient correctness` |

## Rung Ledger

| Rung | Status | Evidence-bearing | Direct failure | Veto/block reason | Inherited blocker |
| --- | --- | --- | --- | --- | --- |
| `R1_T4_residual_ladder` | `pass` | `True` | `False` | `None` | `None` |
| `R2_1d_horizon_ladder` | `veto` | `True` | `True` | `blocked_by_R2_horizon_32_veto` | `None` |
| `R3_1d_particle_count_ladder` | `blocked` | `False` | `False` | `blocked_by_R2_horizon_32_veto` | `blocked_by_R2_horizon_32_veto` |
| `R4_1d_random_stream_alignment` | `blocked` | `False` | `False` | `blocked_by_R2_horizon_32_veto` | `blocked_by_R2_horizon_32_veto` |
| `R5_1d_resampling_policy_match` | `blocked` | `False` | `False` | `blocked_by_R2_horizon_32_veto` | `blocked_by_R2_horizon_32_veto` |
| `R6_1d_parameter_grid_surface` | `blocked` | `False` | `False` | `blocked_by_R2_horizon_32_veto` | `blocked_by_R2_horizon_32_veto` |
| `R7_1d_smoothness_scalar_contract` | `blocked` | `False` | `False` | `blocked_by_R2_horizon_32_veto` | `blocked_by_R2_horizon_32_veto` |
| `R8_2d_constant_velocity_bridge` | `blocked` | `False` | `False` | `blocked_by_R2_horizon_32_veto` | `blocked_by_R2_horizon_32_veto` |

## Canonical Per-Rung Ledger

### R1_T4_residual_ladder

| Field | Value |
| --- | --- |
| status | `pass` |
| evidence bearing | `True` |
| failure observed directly | `False` |
| blocker reason | `None` |
| inherited blocker | `None` |
| first failing rung | `None` |
| first blocked rung | `None` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{
  "epsilon": 0.25,
  "horizon": 4,
  "num_particles": 4,
  "observations": [
    0.05,
    -0.1,
    0.08,
    -0.04
  ],
  "scaling": 0.9,
  "scenario_id": "T4_extension",
  "theta": 0.7,
  "transition_noises": [
    [
      0.0,
      0.1,
      -0.2,
      0.3
    ],
    [
      0.2,
      -0.1,
      0.0,
      -0.3
    ],
    [
      -0.1,
      0.0,
      0.25,
      -0.15
    ],
    [
      0.15,
      -0.25,
      0.05,
      0.1
    ]
  ]
}
```

Varied variables:

```json
{
  "convergence_threshold": [
    1e-06,
    1e-07,
    1e-08
  ],
  "max_iterations": [
    200,
    500,
    1000
  ]
}
```

Primary metrics:

```json
{
  "cell_summaries": [
    {
      "cell_status": "veto",
      "convergence_threshold": 1e-06,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9368130259955763,
        "bayesfilter_gradient_tape": -2.4471359617699653,
        "filterflow_finite_difference_gradient": -1.9371509552001953,
        "filterflow_gradient_tape": -2.2461719512939453,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 200,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": false,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 0.0005233019270021178,
        "bayesfilter_scalar": 1.2977620902498526,
        "filterflow_max_column_residual": 2.384185791015625e-07,
        "filterflow_max_row_residual": 0.0005233287811279297,
        "filterflow_scalar": 1.2977619171142578,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 2.384185791015625e-07,
        "max_absolute_row_residual": 0.0005233287811279297,
        "scalar_delta": 1.731355947498514e-07,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": false,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "veto",
      "convergence_threshold": 1e-07,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9368126776897476,
        "bayesfilter_gradient_tape": -2.447141084060507,
        "filterflow_finite_difference_gradient": -1.9371509552001953,
        "filterflow_gradient_tape": -2.246178388595581,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 200,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": false,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 0.0005232588315606801,
        "bayesfilter_scalar": 1.2977622043731758,
        "filterflow_max_column_residual": 1.1920928955078125e-07,
        "filterflow_max_row_residual": 0.0005230903625488281,
        "filterflow_scalar": 1.2977620363235474,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 1.1920928955078125e-07,
        "max_absolute_row_residual": 0.0005232588315606801,
        "scalar_delta": 1.680496284350852e-07,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": false,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "veto",
      "convergence_threshold": 1e-08,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.936812633187568,
        "bayesfilter_gradient_tape": -2.4471417042966066,
        "filterflow_finite_difference_gradient": -1.9377470016479492,
        "filterflow_gradient_tape": -2.2461791038513184,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 200,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": false,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 0.0005232536132360188,
        "bayesfilter_scalar": 1.2977622181924673,
        "filterflow_max_column_residual": 2.384185791015625e-07,
        "filterflow_max_row_residual": 0.0005233287811279297,
        "filterflow_scalar": 1.297762155532837,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 2.384185791015625e-07,
        "max_absolute_row_residual": 0.0005233287811279297,
        "scalar_delta": 6.265963037321853e-08,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": false,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-06,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9375573807578483,
        "bayesfilter_gradient_tape": -2.4471730796246223,
        "filterflow_finite_difference_gradient": -1.9383430480957031,
        "filterflow_gradient_tape": -2.246048927307129,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 500,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 1.4204764579250906e-05,
        "bayesfilter_scalar": 1.297769129483926,
        "filterflow_max_column_residual": 1.1920928955078125e-07,
        "filterflow_max_row_residual": 1.4185905456542969e-05,
        "filterflow_scalar": 1.2977690696716309,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 1.1920928955078125e-07,
        "max_absolute_row_residual": 1.4204764579250906e-05,
        "scalar_delta": 5.981229511675679e-08,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-07,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9374275711370181,
        "bayesfilter_gradient_tape": -2.447183043875783,
        "filterflow_finite_difference_gradient": -1.9377470016479492,
        "filterflow_gradient_tape": -2.246058702468872,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 500,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 1.4281668403448577e-06,
        "bayesfilter_scalar": 1.297769840024542,
        "filterflow_max_column_residual": 1.1920928955078125e-07,
        "filterflow_max_row_residual": 1.430511474609375e-06,
        "filterflow_scalar": 1.2977699041366577,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 1.1920928955078125e-07,
        "max_absolute_row_residual": 1.430511474609375e-06,
        "scalar_delta": 6.411211561641039e-08,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-08,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9374297627416937,
        "bayesfilter_gradient_tape": -2.447184137457463,
        "filterflow_finite_difference_gradient": -1.9383430480957031,
        "filterflow_gradient_tape": -2.2460591793060303,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 500,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 1.4361799216544568e-07,
        "bayesfilter_scalar": 1.297769912357856,
        "filterflow_max_column_residual": 2.384185791015625e-07,
        "filterflow_max_row_residual": 4.76837158203125e-07,
        "filterflow_scalar": 1.2977699041366577,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 2.384185791015625e-07,
        "max_absolute_row_residual": 4.76837158203125e-07,
        "scalar_delta": 8.221198388724815e-09,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-06,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9375573807578483,
        "bayesfilter_gradient_tape": -2.4471730796246223,
        "filterflow_finite_difference_gradient": -1.9383430480957031,
        "filterflow_gradient_tape": -2.246048927307129,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 1000,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 1.4204764579250906e-05,
        "bayesfilter_scalar": 1.297769129483926,
        "filterflow_max_column_residual": 1.1920928955078125e-07,
        "filterflow_max_row_residual": 1.4185905456542969e-05,
        "filterflow_scalar": 1.2977690696716309,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 1.1920928955078125e-07,
        "max_absolute_row_residual": 1.4204764579250906e-05,
        "scalar_delta": 5.981229511675679e-08,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-07,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9374275711370181,
        "bayesfilter_gradient_tape": -2.447183043875783,
        "filterflow_finite_difference_gradient": -1.9377470016479492,
        "filterflow_gradient_tape": -2.246058702468872,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 1000,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 1.4281668403448577e-06,
        "bayesfilter_scalar": 1.297769840024542,
        "filterflow_max_column_residual": 1.1920928955078125e-07,
        "filterflow_max_row_residual": 1.430511474609375e-06,
        "filterflow_scalar": 1.2977699041366577,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 1.1920928955078125e-07,
        "max_absolute_row_residual": 1.430511474609375e-06,
        "scalar_delta": 6.411211561641039e-08,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-08,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.9374300298435898,
        "bayesfilter_gradient_tape": -2.4471841377292245,
        "filterflow_finite_difference_gradient": -1.9383430480957031,
        "filterflow_gradient_tape": -2.2460591793060303,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 1000,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 1.3974400236982376e-07,
        "bayesfilter_scalar": 1.297769912410482,
        "filterflow_max_column_residual": 2.384185791015625e-07,
        "filterflow_max_row_residual": 4.76837158203125e-07,
        "filterflow_scalar": 1.2977699041366577,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 2.384185791015625e-07,
        "max_absolute_row_residual": 4.76837158203125e-07,
        "scalar_delta": 8.273824292359677e-09,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "T4_extension"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    }
  ],
  "evaluated_cell_count": 9,
  "max_absolute_column_residual": 2.384185791015625e-07,
  "max_absolute_row_residual": 0.0005233287811279297,
  "passing_cell_count": 6,
  "selected_r1_cell": {
    "convergence_threshold": 1e-06,
    "max_absolute_column_residual": 1.1920928955078125e-07,
    "max_absolute_row_residual": 1.4204764579250906e-05,
    "max_iterations": 500
  }
}
```

Veto diagnostics:

```json
{
  "r2_unblocked": true,
  "residual_tolerance": 0.0001
}
```

Explanatory diagnostics:

```json
{
  "known_prior_T4_row_residual": 0.0005233019270021178,
  "sweep_contract": "threshold in {1e-6,1e-7,1e-8}; max_iterations in {200,500,1000}"
}
```

### R2_1d_horizon_ladder

| Field | Value |
| --- | --- |
| status | `veto` |
| evidence bearing | `True` |
| failure observed directly | `True` |
| blocker reason | `blocked_by_R2_horizon_32_veto` |
| inherited blocker | `None` |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `None` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{
  "epsilon": 0.25,
  "num_particles": 4,
  "scaling": 0.9,
  "selected_r1_cell": {
    "convergence_threshold": 1e-06,
    "max_absolute_column_residual": 1.1920928955078125e-07,
    "max_absolute_row_residual": 1.4204764579250906e-05,
    "max_iterations": 500
  },
  "theta": 0.7
}
```

Varied variables:

```json
{
  "horizon": [
    4,
    8,
    16,
    32,
    100
  ]
}
```

Primary metrics:

```json
{
  "cell_summaries": [
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-06,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -1.177687120070825,
        "bayesfilter_gradient_tape": 0.994957901676633,
        "filterflow_finite_difference_gradient": -1.1786818504333496,
        "filterflow_gradient_tape": -0.09377634525299072,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 500,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 3.858330841066682e-05,
        "bayesfilter_scalar": -0.678767820621069,
        "filterflow_max_column_residual": 2.384185791015625e-07,
        "filterflow_max_row_residual": 3.8623809814453125e-05,
        "filterflow_scalar": -0.6787679195404053,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 2.384185791015625e-07,
        "max_absolute_row_residual": 3.8623809814453125e-05,
        "scalar_delta": 9.8919336277703e-08,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 4,
        "scenario_id": "generated_T4"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-06,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -0.6567680774449691,
        "bayesfilter_gradient_tape": -1.0560253712155616,
        "filterflow_finite_difference_gradient": -0.6568431854248047,
        "filterflow_gradient_tape": -1.1461809873580933,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 500,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 3.974393986760916e-05,
        "bayesfilter_scalar": 2.6711910666528245,
        "filterflow_max_column_residual": 1.1920928955078125e-07,
        "filterflow_max_row_residual": 3.9696693420410156e-05,
        "filterflow_scalar": 2.6711909770965576,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 1.1920928955078125e-07,
        "max_absolute_row_residual": 3.974393986760916e-05,
        "scalar_delta": 8.955626684681306e-08,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 8,
        "scenario_id": "generated_T8"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "pass",
      "convergence_threshold": 1e-06,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -4.70432256243658,
        "bayesfilter_gradient_tape": -8.912183740715058,
        "filterflow_finite_difference_gradient": -4.700422286987305,
        "filterflow_gradient_tape": -16.11032485961914,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 500,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": true,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 1.3420703364963593e-05,
        "bayesfilter_scalar": 1.700923192237744,
        "filterflow_max_column_residual": 2.384185791015625e-07,
        "filterflow_max_row_residual": 1.341104507446289e-05,
        "filterflow_scalar": 1.7009224891662598,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 2.384185791015625e-07,
        "max_absolute_row_residual": 1.3420703364963593e-05,
        "scalar_delta": 7.030714841427255e-07,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 16,
        "scenario_id": "generated_T16"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": true,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    },
    {
      "cell_status": "veto",
      "convergence_threshold": 1e-06,
      "explanatory_diagnostics": {
        "bayesfilter_finite_difference_gradient": -8.920029687256026,
        "bayesfilter_gradient_tape": -5.9341656593135585,
        "filterflow_finite_difference_gradient": -8.919239044189453,
        "filterflow_gradient_tape": 0.9346641302108765,
        "gradient_promotion": "not_concluded"
      },
      "filterflow_command": "CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>",
      "max_iterations": 500,
      "primary_metrics": {
        "absolute_residuals_within_tolerance": false,
        "bayesfilter_max_column_residual": 4.440892098500626e-16,
        "bayesfilter_max_row_residual": 0.0009653550196917493,
        "bayesfilter_scalar": 6.9935334497502195,
        "filterflow_max_column_residual": 2.384185791015625e-07,
        "filterflow_max_row_residual": 0.000965416431427002,
        "filterflow_scalar": 6.993533134460449,
        "ledger_within_tolerance": true,
        "max_absolute_column_residual": 2.384185791015625e-07,
        "max_absolute_row_residual": 0.000965416431427002,
        "scalar_delta": 3.152897702918267e-07,
        "scalar_within_tolerance": true,
        "trigger_match": true
      },
      "scenario": {
        "horizon": 32,
        "scenario_id": "generated_T32"
      },
      "veto_diagnostics": {
        "absolute_residuals_within_tolerance": false,
        "filterflow_blocker": null,
        "finite_bayesfilter_scalar": true,
        "finite_filterflow_scalar": true,
        "ledger_within_tolerance": true,
        "scalar_within_tolerance": true,
        "trigger_match": true
      }
    }
  ],
  "evaluated_horizons": [
    4,
    8,
    16,
    32
  ],
  "max_absolute_column_residual": 2.384185791015625e-07,
  "max_absolute_row_residual": 0.000965416431427002
}
```

Veto diagnostics:

```json
{
  "residual_tolerance": 0.0001
}
```

Explanatory diagnostics:

```json
{
  "generated_fixture": "tf_stateless_normal_fixed_seed",
  "note": "R2 is reached only if R1 selects a passing residual setting."
}
```

### R3_1d_particle_count_ladder

| Field | Value |
| --- | --- |
| status | `blocked` |
| evidence bearing | `False` |
| failure observed directly | `False` |
| blocker reason | `blocked_by_R2_horizon_32_veto` |
| inherited blocker | `blocked_by_R2_horizon_32_veto` |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `R3_1d_particle_count_ladder` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{}
```

Varied variables:

```json
{}
```

Primary metrics:

```json
{}
```

Veto diagnostics:

```json
{
  "blocked_before_execution": true
}
```

Explanatory diagnostics:

```json
{
  "blocked_rung_interpretation": "This rung was not evidence-bearing; the first failing rung is reported separately."
}
```

### R4_1d_random_stream_alignment

| Field | Value |
| --- | --- |
| status | `blocked` |
| evidence bearing | `False` |
| failure observed directly | `False` |
| blocker reason | `blocked_by_R2_horizon_32_veto` |
| inherited blocker | `blocked_by_R2_horizon_32_veto` |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `R3_1d_particle_count_ladder` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{}
```

Varied variables:

```json
{}
```

Primary metrics:

```json
{}
```

Veto diagnostics:

```json
{
  "blocked_before_execution": true
}
```

Explanatory diagnostics:

```json
{
  "blocked_rung_interpretation": "This rung was not evidence-bearing; the first failing rung is reported separately."
}
```

### R5_1d_resampling_policy_match

| Field | Value |
| --- | --- |
| status | `blocked` |
| evidence bearing | `False` |
| failure observed directly | `False` |
| blocker reason | `blocked_by_R2_horizon_32_veto` |
| inherited blocker | `blocked_by_R2_horizon_32_veto` |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `R3_1d_particle_count_ladder` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{}
```

Varied variables:

```json
{}
```

Primary metrics:

```json
{}
```

Veto diagnostics:

```json
{
  "blocked_before_execution": true
}
```

Explanatory diagnostics:

```json
{
  "blocked_rung_interpretation": "This rung was not evidence-bearing; the first failing rung is reported separately."
}
```

### R6_1d_parameter_grid_surface

| Field | Value |
| --- | --- |
| status | `blocked` |
| evidence bearing | `False` |
| failure observed directly | `False` |
| blocker reason | `blocked_by_R2_horizon_32_veto` |
| inherited blocker | `blocked_by_R2_horizon_32_veto` |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `R3_1d_particle_count_ladder` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{}
```

Varied variables:

```json
{}
```

Primary metrics:

```json
{}
```

Veto diagnostics:

```json
{
  "blocked_before_execution": true
}
```

Explanatory diagnostics:

```json
{
  "blocked_rung_interpretation": "This rung was not evidence-bearing; the first failing rung is reported separately."
}
```

### R7_1d_smoothness_scalar_contract

| Field | Value |
| --- | --- |
| status | `blocked` |
| evidence bearing | `False` |
| failure observed directly | `False` |
| blocker reason | `blocked_by_R2_horizon_32_veto` |
| inherited blocker | `blocked_by_R2_horizon_32_veto` |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `R3_1d_particle_count_ladder` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{}
```

Varied variables:

```json
{}
```

Primary metrics:

```json
{}
```

Veto diagnostics:

```json
{
  "blocked_before_execution": true
}
```

Explanatory diagnostics:

```json
{
  "blocked_rung_interpretation": "This rung was not evidence-bearing; the first failing rung is reported separately."
}
```

### R8_2d_constant_velocity_bridge

| Field | Value |
| --- | --- |
| status | `blocked` |
| evidence bearing | `False` |
| failure observed directly | `False` |
| blocker reason | `blocked_by_R2_horizon_32_veto` |
| inherited blocker | `blocked_by_R2_horizon_32_veto` |
| first failing rung | `R2_1d_horizon_ladder` |
| first blocked rung | `R3_1d_particle_count_ladder` |

Comparator fingerprint before:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Comparator fingerprint after:

```json
{
  "branch_ref_exists": true,
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

Fixed variables:

```json
{}
```

Varied variables:

```json
{}
```

Primary metrics:

```json
{}
```

Veto diagnostics:

```json
{
  "blocked_before_execution": true
}
```

Explanatory diagnostics:

```json
{
  "blocked_rung_interpretation": "This rung was not evidence-bearing; the first failing rung is reported separately."
}
```


## R1 Cell Summary

| threshold | max iterations | status | scalar delta | max row residual | max column residual |
| ---: | ---: | --- | ---: | ---: | ---: |
| `1e-06` | `200` | `veto` | `1.731355947498514e-07` | `0.0005233287811279297` | `2.384185791015625e-07` |
| `1e-07` | `200` | `veto` | `1.680496284350852e-07` | `0.0005232588315606801` | `1.1920928955078125e-07` |
| `1e-08` | `200` | `veto` | `6.265963037321853e-08` | `0.0005233287811279297` | `2.384185791015625e-07` |
| `1e-06` | `500` | `pass` | `5.981229511675679e-08` | `1.4204764579250906e-05` | `1.1920928955078125e-07` |
| `1e-07` | `500` | `pass` | `6.411211561641039e-08` | `1.430511474609375e-06` | `1.1920928955078125e-07` |
| `1e-08` | `500` | `pass` | `8.221198388724815e-09` | `4.76837158203125e-07` | `2.384185791015625e-07` |
| `1e-06` | `1000` | `pass` | `5.981229511675679e-08` | `1.4204764579250906e-05` | `1.1920928955078125e-07` |
| `1e-07` | `1000` | `pass` | `6.411211561641039e-08` | `1.430511474609375e-06` | `1.1920928955078125e-07` |
| `1e-08` | `1000` | `pass` | `8.273824292359677e-09` | `4.76837158203125e-07` | `2.384185791015625e-07` |

## R2 Horizon Summary

| horizon | status | scalar delta | max row residual | max column residual | residual pass |
| ---: | --- | ---: | ---: | ---: | --- |
| `4` | `pass` | `9.8919336277703e-08` | `3.8623809814453125e-05` | `2.384185791015625e-07` | `True` |
| `8` | `pass` | `8.955626684681306e-08` | `3.974393986760916e-05` | `1.1920928955078125e-07` | `True` |
| `16` | `pass` | `7.030714841427255e-07` | `1.3420703364963593e-05` | `2.384185791015625e-07` | `True` |
| `32` | `veto` | `3.152897702918267e-07` | `0.000965416431427002` | `2.384185791015625e-07` | `False` |

## Interpretation

Within the executed scalar-state prefix, R1 found a viable residual setting, but the R2 horizon extension produced the first direct evidence-bearing failure at T=32. This is not a claim that the full smoothness-alignment ladder has been exercised.

## Scope Caveat

This run localizes the first evidence-bearing failure within the executed R1/R2 scalar-state prefix. It does not answer the full smoothness-alignment question because R3-R8 are blocked after the R2 veto.

## Governance Blocker

Plan review reached round 5 without Claude `ACCEPT`. The final
plan-review finding was patched, and the run is preserved as an
inspection-only diagnostic. This is not a protocol-clean reviewed
result and must not be promoted as downstream evidence unless the
human explicitly authorizes that use or plan review is reopened and
accepted.

## Comparator

| Field | Value |
| --- | --- |
| path | `/home/chakwong/BayesFilter/.localsource/filterflow` |
| head commit | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| symbolic head | `bayesfilter-py311-compat` |
| branch string status | `descriptive_only` |
| branch ref exists | `True` |
| Python version | `Python 3.11.14` |
| diff digest | `02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3` |
| package manifest digest | `51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86` |
| exact filterflow command | `CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <1D continuation cell script>` |

Local diff/status:

```text
M scripts/base.py
 M scripts/simple_linear_common.py
 M scripts/simple_linear_smoothness.py
```

## Verification Notes

The runner validates parent and filterflow-subprocess CPU-only manifests,
rung ledger shape, first-failure/first-blocked consistency, and JSON
schema invariants during normal and `--validate-only` execution.

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
