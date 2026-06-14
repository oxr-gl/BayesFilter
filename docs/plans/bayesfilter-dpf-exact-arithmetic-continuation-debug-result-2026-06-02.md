# Exact-Arithmetic Continuation Debug

## Decision

`exact_arithmetic_continuation_blocked_after_partial_agreement`

## First Cells

| Field | Value |
| --- | --- |
| first failing cell | `{'rung_id': 'none_observed', 'cell_index': -1, 'cell_id': 'none_observed'}` |
| first blocked cell | `{'rung_id': 'R3_filterflow_transition_stream', 'cell_index': 0, 'cell_id': 'proposal_stream_not_replayed'}` |

## Rung Ledger

| Rung | Status | Evidence-bearing | Direct failure | Blocker | Changed axis |
| --- | --- | --- | --- | --- | --- |
| `R1_filterflow_observation_path_exact_arithmetic` | `pass` | `True` | `False` | `None` | `observations switched to executable filterflow smoothness fixture` |
| `R2_filterflow_initial_particles_exact_arithmetic` | `pass` | `True` | `False` | `None` | `initial particles switched to executable filterflow fixture draw` |
| `R3_filterflow_transition_stream` | `blocked` | `False` | `False` | `blocked_by_uninstrumented_filterflow_transition_proposal_stream: the executable filterflow smoothness path samples proposal noises inside its SMC loop and the public script fixture does not serialize per-time proposal draws. Continuing the one-axis ladder requires a reviewed non-mutating trace wrapper or explicit authorization to instrument the local filterflow reference.` | `transition proposal stream switched toward executable filterflow smoothness path` |
| `R4_resampling_policy_trigger_semantics` | `blocked` | `False` | `False` | `blocked_by_uninstrumented_filterflow_transition_proposal_stream: the executable filterflow smoothness path samples proposal noises inside its SMC loop and the public script fixture does not serialize per-time proposal draws. Continuing the one-axis ladder requires a reviewed non-mutating trace wrapper or explicit authorization to instrument the local filterflow reference.` | `blocked_before_execution` |
| `R5_scalar_contract` | `blocked` | `False` | `False` | `blocked_by_uninstrumented_filterflow_transition_proposal_stream: the executable filterflow smoothness path samples proposal noises inside its SMC loop and the public script fixture does not serialize per-time proposal draws. Continuing the one-axis ladder requires a reviewed non-mutating trace wrapper or explicit authorization to instrument the local filterflow reference.` | `blocked_before_execution` |
| `R6_theta_grid_surface` | `blocked` | `False` | `False` | `blocked_by_uninstrumented_filterflow_transition_proposal_stream: the executable filterflow smoothness path samples proposal noises inside its SMC loop and the public script fixture does not serialize per-time proposal draws. Continuing the one-axis ladder requires a reviewed non-mutating trace wrapper or explicit authorization to instrument the local filterflow reference.` | `blocked_before_execution` |
| `R7_2d_constant_velocity_state` | `blocked` | `False` | `False` | `blocked_by_uninstrumented_filterflow_transition_proposal_stream: the executable filterflow smoothness path samples proposal noises inside its SMC loop and the public script fixture does not serialize per-time proposal draws. Continuing the one-axis ladder requires a reviewed non-mutating trace wrapper or explicit authorization to instrument the local filterflow reference.` | `blocked_before_execution` |
| `R8_gradient_smoothness_surface` | `blocked` | `False` | `False` | `blocked_by_uninstrumented_filterflow_transition_proposal_stream: the executable filterflow smoothness path samples proposal noises inside its SMC loop and the public script fixture does not serialize per-time proposal draws. Continuing the one-axis ladder requires a reviewed non-mutating trace wrapper or explicit authorization to instrument the local filterflow reference.` | `blocked_before_execution` |

## Evidence Cells

### R1_filterflow_observation_path_exact_arithmetic

| Metric | Value |
| --- | ---: |
| implementation agreement | `True` |
| scalar delta | `0.0` |
| max field delta | `4.656612873077393e-10` |
| row residual delta | `0.0` |
| column residual delta | `0.0` |
| first failure | `{'status': 'no_field_failure', 'time_index': None, 'field_set': [], 'triggered': False}` |

### R2_filterflow_initial_particles_exact_arithmetic

| Metric | Value |
| --- | ---: |
| implementation agreement | `True` |
| scalar delta | `0.0` |
| max field delta | `3.2014213502407074e-10` |
| row residual delta | `0.0` |
| column residual delta | `0.0` |
| first failure | `{'status': 'no_field_failure', 'time_index': None, 'field_set': [], 'triggered': False}` |

## Interpretation

No direct mismatch was found before the first blocker. The next debugging step is to obtain an exact replay or trace of the filterflow transition proposal random stream.

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
- No production dtype default is concluded.
