# Result: 1D-to-Smoothness Filterflow Agreement Ladder

## Decision

`one_d_to_smoothness_agreement_ladder_first_mismatch_detected`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `one_d_to_smoothness_agreement_ladder_first_mismatch_detected` | `passed agreement on 0 evidence-bearing rungs: []` | `implementation mismatch observed` | `why R1_1d_T100_filterflow_observation_path differs after the changed axis; likely scalar/ledger scale, dtype, or transport residual sensitivity` | `localize the first failing cell by per-time scalar increments, first bad ledger field, float32-vs-float64 stress, and shorter prefixes of the same observation path` | `correctness of either implementation, gradient correctness, full smoothness validation` |

## First Cells

| Field | Value |
| --- | --- |
| first failing cell | `{'rung_id': 'R1_1d_T100_filterflow_observation_path', 'cell_index': 0, 'cell_id': 'T100_filterflow_observation_path'}` |
| first blocked cell | `{'rung_id': 'R2_1d_initial_particle_generation', 'cell_index': 0, 'cell_id': 'blocked_after_R1'}` |

## Rung Ledger

| Rung | Status | Evidence-bearing | Direct failure | Blocker | Changed axis |
| --- | --- | --- | --- | --- | --- |
| `R1_1d_T100_filterflow_observation_path` | `mismatch` | `True` | `True` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `observations switched to local executable filterflow-generated T=100 path` |
| `R2_1d_initial_particle_generation` | `blocked` | `False` | `False` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `blocked_before_execution` |
| `R3_1d_transition_random_stream` | `blocked` | `False` | `False` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `blocked_before_execution` |
| `R4_resampling_policy_trigger_semantics` | `blocked` | `False` | `False` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `blocked_before_execution` |
| `R5_scalar_contract` | `blocked` | `False` | `False` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `blocked_before_execution` |
| `R6_theta_grid_surface` | `blocked` | `False` | `False` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `blocked_before_execution` |
| `R7_2d_constant_velocity_state` | `blocked` | `False` | `False` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `blocked_before_execution` |
| `R8_gradient_smoothness_surface` | `blocked` | `False` | `False` | `blocked_after_R1_1d_T100_filterflow_observation_path_mismatch` | `blocked_before_execution` |

## Evidence-Bearing Cells

### R1_1d_T100_filterflow_observation_path

| Metric | Value |
| --- | ---: |
| scalar delta | `2.205229699611664` |
| row residual delta | `0.0005531286149466075` |
| column residual delta | `4.768371573149466e-07` |
| BayesFilter row residual | `2.4885690175224795e-09` |
| filterflow row residual | `0.000553131103515625` |
| implementation agreement | `False` |

Shared quality diagnostic: `not_shared_residual_disagreement`.

## First Discrepancy Or Blocker

The first observed BayesFilter/filterflow mismatch is `{'rung_id': 'R1_1d_T100_filterflow_observation_path', 'cell_index': 0, 'cell_id': 'T100_filterflow_observation_path'}`. Later rungs are blocked by this first mismatch and are not evidence-bearing.

## Fixture

```json
{
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "data_seed": 123,
  "filter_seed": 1234,
  "fixture_contract": "filterflow_observations_and_initial_particles_replayed_as_explicit_tensors",
  "initial_particles_scalar": [
    0.007650548592209816,
    -0.00659151328727603,
    -0.0014401334337890148,
    -0.007043421268463135
  ],
  "observation_count": 100,
  "status": "executed",
  "transition_noises_source": "not_from_fixture; runner uses existing controlled generated_T100 ledger"
}
```

## Comparator

```json
{
  "branch_string_status": "descriptive_only",
  "diff_digest": "02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3",
  "head_commit": "5d8300ba247c4c17e1a301a22560c24fd0670bfe",
  "package_manifest_digest": "51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86",
  "python_version": "Python 3.11.14",
  "status": "current_local_patched_checkout",
  "status_short": "M scripts/base.py\n M scripts/simple_linear_common.py\n M scripts/simple_linear_smoothness.py",
  "symbolic_head": "bayesfilter-py311-compat"
}
```

## Claude Review

Plan review status: `ACCEPT_after_round_3_seed_correction`.
Result review status is recorded in the review-loop artifact.

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
- Shared residual magnitude is not a BayesFilter/filterflow discrepancy.
