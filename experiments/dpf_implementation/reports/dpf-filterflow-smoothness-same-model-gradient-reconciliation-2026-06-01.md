# Filterflow Smoothness Same-Model Gradient Reconciliation

## Decision

`same_model_gradient_wrong_model_gap_closed_gradient_agreement_not_concluded`

## Governance

This runner closes the prior wrong-model gradient-harness gap only. It does not
claim Claude review closure by itself and does not promote production readiness.

## Same-Model Diagnostic

| Key | Value |
| --- | --- |
| `row_count` | `16` |
| `finite_rows` | `16` |
| `bayesfilter_likelihood_rmse_vs_filterflow` | `184345.80209129627` |
| `bayesfilter_likelihood_rmse_vs_kalman` | `490562.36155074654` |
| `filterflow_likelihood_rmse_vs_kalman` | `323943.654172315` |
| `bayesfilter_gradient_rmse_vs_filterflow` | `2.537001953821507e+145` |
| `bayesfilter_gradient_rmse_vs_kalman` | `2.537001953821507e+145` |
| `filterflow_gradient_rmse_vs_kalman` | `144487904.88971964` |
| `bayesfilter_gradient_cosine_vs_filterflow` | `-0.014110786351377623` |
| `bayesfilter_gradient_cosine_vs_kalman` | `-0.06569613949112281` |
| `filterflow_gradient_cosine_vs_kalman` | `0.8895568190836276` |
| `bayesfilter_gradient_sign_agreement_vs_filterflow` | `0.34375` |
| `bayesfilter_gradient_sign_agreement_vs_kalman` | `0.28125` |
| `filterflow_gradient_sign_agreement_vs_kalman` | `0.9375` |
| `bayesfilter_gradient_norm` | `1.4351450283445662e+146` |
| `filterflow_gradient_norm` | `817352317.6343408` |
| `kalman_gradient_norm` | `5956.745084331147` |
| `same_model_gap_closed` | `True` |
| `scalar_comparability_status` | `open_blocking_for_gradient_agreement` |
| `gradient_agreement_concluded` | `False` |
| `gradient_claim_status` | `same_model_finite_diagnostics_not_gradient_agreement` |

## Scientific Validity Limits

| ID | Status | Detail |
| --- | --- | --- |
| `same_model_wrong_comparator_gap` | `closed` | BayesFilter gradient harness now uses filterflow smoothness constant-velocity LGSSM. |
| `bit_identical_randomness` | `open_controlled` | Observations and initial particles are extracted, but BayesFilter transition noises use stateless common random numbers rather than filterflow internal split_seed draws. |
| `scalar_comparability` | `open_blocking_for_gradient_agreement` | Same-model scalar definitions are recorded, but likelihood scales remain far apart, including filterflow versus Kalman. |
| `gradient_agreement` | `same_model_finite_diagnostics_not_gradient_agreement` | Finite same-model diagnostics are recorded; gradient agreement is not concluded. |
| `scientific_validity` | `bounded_diagnostic_only` | No production, posterior, HMC, or general nonlinear-SSM validity follows. |

## Model Contract

| Key | Value |
| --- | --- |
| `model` | `filterflow_simple_linear_smoothness_constant_velocity_lgssm` |
| `transition_matrix` | `A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]` |
| `transition_covariance` | `[[0.3333333333333333, 0.5], [0.5, 1.0]]` |
| `observation_matrix` | `[[1.0, 0.0]]` |
| `observation_covariance` | `[[0.01]]` |
| `horizon` | `100` |
| `mesh_size` | `4` |
| `num_particles` | `25` |
| `batch_size` | `1` |
| `resampling_threshold` | `ESS <= 0.9999 N` |
| `epsilon` | `0.25` |
| `scaling` | `0.85` |
| `convergence_threshold` | `1e-06` |
| `max_iter` | `200` |

## Seed Contract

| Key | Value |
| --- | --- |
| `status` | `recorded` |
| `data_seed` | `123` |
| `filter_seed` | `1234` |
| `observation_checksum` | `24302.800384521484` |
| `initial_particles_checksum` | `-0.020055056884302758` |
| `initial_particles_shape` | `[1, 25, 2]` |
| `observations_shape` | `[100, 1]` |

## Scalar Contract

| Key | Value |
| --- | --- |
| `status` | `same_model_scalar_definitions_recorded` |
| `filterflow_scalar` | `tf.reduce_mean(final_state.log_likelihoods), batch_size=1` |
| `bayesfilter_scalar` | `tf.reduce_mean(log_likelihoods), batch_size=1` |
| `kalman_scalar` | `total Kalman log likelihood from get_surface_kf` |
| `normalization_note` | `batch_size=1 makes mean and total equal; per-time values are explanatory only` |
| `filterflow_first_scalar` | `-1258564.375` |
| `kalman_first_scalar` | `-221.1320427033769` |

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| close wrong-model gradient-harness gap | same filterflow smoothness LGSSM used | pass | bit-identical filterflow transition-noise stream not reconstructed | derive or export exact filterflow random stream if gradient equality is required | gradient correctness or scientific validity |

## Non-Implications

- No gradient agreement is concluded.
- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No monograph claim is concluded.
