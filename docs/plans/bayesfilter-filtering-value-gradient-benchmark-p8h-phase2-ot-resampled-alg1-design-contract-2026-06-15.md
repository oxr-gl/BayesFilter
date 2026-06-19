# P8h Phase 2 Design Contract: OT-Resampled Algorithm 1 LEDH

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Purpose

Specify the implementation contract for the P8h serious candidate before any
code changes:

`Li-Coates Algorithm 1 UKF LEDH + PF-PF correction + Corenflos-style OT/Sinkhorn or annealed-transport resampling`.

This contract is design-only. It does not validate implementation correctness,
value adequacy, gradient correctness, GPU scaling, HMC readiness, stochastic PF
marginal-gradient correctness, exact nonlinear likelihood correctness, or filter
ranking.

## Existing Entry Points

| Role | Current entry point | Anchor | Current status |
|---|---|---|---|
| Algorithm 1 result state | `LedhPFPFAlg1UKFTFResult` | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:68` | Carries route IDs, log likelihood, filtered summaries, covariance histories, corrected weights, ESS, resampling diagnostics, and finite flag. |
| Algorithm 1 time-step state | `LedhAlg1TimeStepResult` | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:50` | Carries `updated_covariances`, `predicted_covariances`, flow matrices, offsets, log det, and diagnostics. |
| Algorithm 1 runner | `run_ledh_pfpf_alg1_ukf_tf` | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:731` | Currently accepts only `resampling_route in {"none", "classical_resampling"}` and rejects OT routes. |
| Current PF-PF correction | corrected log-weight formula | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:819` | `log_weights + target_transition + target_observation - step.pre_flow_log_density + step.forward_log_det`. |
| Classical covariance gather precedent | `apply_classical_resampling_state_tf` | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:1634` | Gathers particles and covariance state by the same ancestor indices for classical resampling. |
| Finite Sinkhorn resampler | `sinkhorn_resample_tf` and `SinkhornTFResult` | `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py:15`, `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py:30` | Returns particles, coupling, source/target weights, and residual diagnostics. |
| Annealed transport resampler | `annealed_transport_resample_tf` and `AnnealedTransportTFResult` | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:15`, `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:22` | Returns particles, uniformized log weights for triggered rows, transport matrix, and diagnostics. |
| Historical OT wrapper | `_resample_particles` in `ledh_pfpf_ot_tf.py` | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py:162` | Dispatches `annealed_transport` and `fixed_target_sinkhorn`, but lacks Algorithm 1 covariance lifecycle. |
| P8 benchmark no-resampling adapter | `_dpf_run_result` call to Algorithm 1 runner | `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:1863` | Currently hard-codes `resampling_route="none"` for the current Algorithm 1 route. |
| P8g fixed-randomness gradient scope | `_p8g_fixed_randomness_gradient_check` | `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:2238` | Diagnostic no-resampling gradient harness only. |
| P8g value/tuning scope | `_p8g_g4_tuning_payload` | `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:2816` | No-resampling scalar-SV tuning blocker; superseded by P8h. |

## Route Identifiers

Phase 3 implementation must add a new route identifier family rather than
reusing P8g names:

- `resampling_route`: one of
  - `ot_annealed_transport_covariance_carry`;
  - `ot_sinkhorn_barycentric_covariance_carry`.
- `route_variant`: initial scalar-SV graph route should use a P8h-specific name,
  such as `p8h_sv_scalar_graph_ot_resampled_alg1`.
- `transport_method`: one of `annealed_transport` or `fixed_target_sinkhorn`.
- `covariance_carry_route`: `same_transport_barycentric_covariance_carry`.
- `pfpf_correction_route`: `algorithm1_pfpf_corrected_log_weight_pre_resampling`.

The old route names `p8g_sv_scalar_graph`, `none`, and
`fixed-randomness/no-resampling` may appear only as historical comparators or
diagnostics.

## OT Trigger Policy

Initial implementation must use an ESS trigger analogous to the existing
runner:

- compute corrected weights from the PF-PF correction before resampling;
- trigger OT resampling when `ESS < ess_threshold_ratio * num_particles`;
- record `ess`, `ess_ratio`, threshold, and boolean `resampled`;
- reset weights to uniform after OT resampling only for triggered rows;
- keep untriggered rows on the weighted path with explicit `resampling_method:
  "none"` diagnostics.

The trigger is a design/implementation policy, not a claim that the chosen
threshold is tuned.

## Canonical Transport Convention

Phase 3 must not consume raw OT helper matrices directly in the Algorithm 1
state update. It must first expose one canonical barycentric transport object:

`A[target_index, source_index]`.

Required convention:

- `A` has shape `[N, N]`;
- each target row sums to one within the declared numerical tolerance;
- transported particles are `X'_j = sum_i A[j, i] X_i`;
- carried covariance state is `P'_j = sum_i A[j, i] P_i`;
- implementation diagnostics must report the raw helper matrix convention and
  the canonical matrix convention.

For `fixed_target_sinkhorn`, the raw `SinkhornTFResult.coupling` is source by
target. The canonical matrix must be computed from the coupling by transposing
and column-normalizing:

`A[j, i] = coupling[i, j] / max(sum_i coupling[i, j], floor)`.

For `annealed_transport`, the raw `AnnealedTransportTFResult.transport_matrix`
is already applied as `transported = transport_matrix @ particles`. The
canonical matrix must therefore be the raw transport matrix after validating
row-stochastic target-by-source orientation, unless implementation inspection
proves a different convention and documents the conversion before use.

If either helper cannot provide a finite canonical `A[target, source]` matrix
with compatible shape and row sums, that OT method is blocked for P8h.

## Covariance Auxiliary-State Carry

The Algorithm 1 covariance state belongs to Li--Coates Algorithm 1. The
BayesFilter integration contract is to carry this auxiliary state through the
same canonical relaxed transport used for particle locations.

For canonical `A[target, source]`, the covariance carry rule is:

`P'_j = sum_i A[j, i] P_i`

where `P_i` is `step.updated_covariances[i]` at the same time step. The
implementation must then symmetrize and apply the declared covariance floor
through the existing covariance stabilization policy before the next time step.

This is not a new filter claim. It is an auxiliary-state bookkeeping rule for
combining Algorithm 1 covariance state with a relaxed OT resampling map.

Required covariance diagnostics:

- `covariance_carry_route`;
- `finite_carried_covariances`;
- `min_carried_covariance_eigenvalue`;
- `covariance_carry_psd_projection_residual`;
- `transport_column_mass_min`;
- `transport_column_mass_max`;
- `canonical_transport_row_sum_min`;
- `canonical_transport_row_sum_max`;
- `transport_mass_total_residual`;
- `covariance_transport_shape`;
- `state_transport_shape`.

## Transport Data Contract

Phase 3 must expose a helper that returns transported particles and the
canonical `A[target, source]` matrix needed for covariance carry. Acceptable raw
sources:

- `AnnealedTransportTFResult.transport_matrix`;
- `SinkhornTFResult.coupling` with column-normalized barycentric weights.

If a resampler cannot provide a finite matrix with compatible `[N, N]` shape
under the canonical convention above, it is blocked for P8h.

Required transport diagnostics:

- `resampling_method`;
- `transport_method`;
- `epsilon`;
- `sinkhorn_iterations` or `max_iterations`;
- `transport_gradient_mode` when annealed transport is used;
- row/column residuals or equivalent transport residuals;
- `raw_transport_matrix_convention`;
- `canonical_transport_matrix_convention: "target_by_source_row_stochastic"`;
- `finite_transport`;
- `finite_particles`;
- `relaxed_resampling_not_categorical: true`.

## PF-PF Correction Attachment

The PF-PF correction must remain attached before resampling:

1. compute `corrected_log_weights` using the existing Algorithm 1 formula;
2. normalize corrected weights and update the incremental log likelihood;
3. compute weighted filtered summaries before resampling, as the current runner
   does;
4. use corrected normalized weights as the OT source marginal;
5. after triggered OT resampling, carry particle state and covariance state and
   set next-step weights to uniform.

The design does not add a new likelihood correction for OT bias. Phase 5/6 must
interpret the value/gradient as the declared relaxed target unless a later
reviewed correction is introduced.

## Gradient Semantics

P8h gradient checks may differentiate only the declared relaxed computational
graph:

- finite unrolled Sinkhorn or annealed-transport computation;
- declared covariance carry;
- fixed/common random draws when required for reproducibility.

Forbidden gradient claims:

- gradient of categorical resampling;
- stochastic PF marginal-likelihood gradient correctness;
- exact nonlinear likelihood correctness;
- HMC readiness from gradient finiteness alone.

## Implementation Boundary For Phase 3

Phase 3 may modify implementation only after this contract passes review. The
implementation must start with scalar-SV, TensorFlow/TFP, no NumPy algorithmic
backend, and focused tests for:

- route identifiers;
- transport shape/residual diagnostics;
- covariance carry shape/finite/PSD diagnostics;
- PF-PF correction preserved before OT resampling;
- no use of the old `ledh_pfpf_ot_tf` route as Algorithm 1 evidence.

P8g quarantine and stale no-resampling boundaries:

- `_p8g_fixed_randomness_gradient_check` remains historical no-resampling
  gradient-plumbing evidence only;
- `_p8g_g4_tuning_payload` remains historical no-resampling tuning/blocker
  evidence only;
- P8h must not reuse P8g route metadata, schema names, or `resampling_route:
  "none"` artifacts as evidence for the OT-resampled route;
- any P8h benchmark or gradient harness must introduce a P8h-specific artifact
  schema and route identifiers in a reviewed later phase.

## Stop Conditions

Stop before Phase 3 implementation if:

- the covariance carry rule above is judged a new scientific claim rather than
  bookkeeping;
- no current OT helper can expose a differentiable transport matrix with
  compatible shape;
- PF-PF correction placement would have to change without human approval;
- the design would require claiming categorical-resampling gradients or HMC
  readiness;
- implementation would require a non-TensorFlow backend.
