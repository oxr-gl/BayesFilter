# P49 Clean-Room Zhao--Cui Source-Route Contract

metadata_date: 2026-06-09
program: P49-source-faithful-repair
phase: P49-M1
status: SOURCE_ROUTE_CONTRACT

## Route Label

This contract defines the `source_faithful_filtering` route for future
BayesFilter work.  It is a clean-room TensorFlow / TensorFlow Probability
design contract derived from source behavior, not copied MATLAB code.

The existing deterministic fixed branch remains a
`gradient_bearing_adaptation` unless a later phase proves otherwise.

## Source-To-Clean-Room Operation Table

| Step | Source anchor | Clean-room operation | Required BayesFilter object or function | Differentiability label | Status |
| --- | --- | --- | --- | --- | --- |
| 1. Initialize augmented samples | `full_sol.solve` lines 20--22; `pre_sol.solve` lines 14--15 | Draw samples for the model parameter/state block with shape `[d+m, N]`; allocate augmented time object with shape `[d+2m, N]`. | `SourceRouteSampleBatch` with `augmented_dim=d+2m`, `sample_count=N`, route metadata. | stochastic/non-differentiable source route | mapped |
| 2. Push samples through dynamics | `full_sol.solve` lines 22--25; `pre_sol.solve` lines 17--20 | Propagate previous samples through the transition/proposal and carry the previous latent block to form `[theta, x_t, x_{t-1}]`. | `source_route_push_samples(model, previous_batch, t)` returning propagated samples and proposal weights. | stochastic/non-differentiable source route | mapped |
| 3. ESS gate and enhanced sampling | `full_sol.reapprox` lines 48--63; `pre_sol.reapprox` lines 33--103 | Compute ESS, double/enhance samples while ESS is below threshold, and record enhancement attempts. | `effective_sample_size(weights)` plus `SourceRouteESSDiagnostics`. | stochastic branch | mapped |
| 4. Weighted recentering | `full_sol.reapprox` lines 65--71; `pre_sol.reapprox` lines 106--114 | Compute weighted location and affine scale matrix from proposed samples; multiply by expansion factor `epd`; store `mu_t,L_t`. | `SourceRouteCoordinateFrame(mu, L, log_abs_det, expansion_factor)`. | deterministic given samples | mapped |
| 5. Prior or previous retained object | `full_sol.reapprox` lines 73--83; `pre_sol.reapprox` lines 117--134 | At `t=1`, use model prior.  At `t>1`, marginalize the previous retained TT/SIRT object and map through previous affine coordinates. | `SourceRouteRetainedObject` with marginalization interface and coordinate frame. | mixed; source route only | mapped |
| 6. Shifted target construction | `full_sol.reapprox` lines 86--96; `pre_sol.reapprox` lines 218--227 and 249--258 | Build a negative-log target in local coordinates; estimate a stability shift constant from random reference samples; subtract the shift inside the target. | `SourceRouteTarget` with `shift_constant`, `log_abs_det`, and target-family label. | stochastic branch | mapped |
| 7. Fit TT/SIRT density/transport object | `full_sol.reapprox` lines 102--121; `pre_sol.reapprox` lines 231--244 and 263--270; `TTFun.cross` lines 8--169 | Fit or update a TT/SIRT object using adaptive/random enrichment or a reviewed clean-room equivalent. | `SourceRouteTransportObject` with fit diagnostics, adaptive-sampling diagnostics, and no copied source code. | non-differentiable source route | test_required |
| 8. Normalizer accounting | `full_sol.reapprox` line 124; `TTSIRT.marginalise` lines 85--86 | Accumulate `log(z) - shift_constant`; include affine determinant in target density consistently. | `SourceRouteNormalizerContribution(log_z, shift_constant, log_abs_det_policy)`. | deterministic given fit | mapped |
| 9. Generate retained samples | `full_sol.solve` lines 31--38; `pre_sol.reapprox` lines 272--286 | Sample reference points, evaluate inverse transport, map by affine frame, and store samples for the next step. | `SourceRouteRetainedObject.samples` and `SourceRouteRetainedObject.transport`. | stochastic branch | mapped |
| 10. Proposal correction and final ESS | `full_sol.solve` lines 35--38; `pre_sol.reapprox` lines 288--294 | Compare approximate proposal density with true target density; compute correction weights and ESS. | `source_route_proposal_log_weights(log_proposal, log_target)` and ESS diagnostics. | stochastic branch | mapped |
| 11. Preconditioned route | `pre_sol.reapprox` lines 136--213 | Optionally split target into preconditioner and residual variants: `pifg`, `fg`, `fgeta`, `g`, `geta`; compose maps `Tu2x`, `Tx2u`. | `SourceRoutePreconditionerContract` with variant, coefficient, reference density, forward/inverse maps. | non-differentiable source route | test_required |
| 12. Smoothing boundary | `full_sol.smooth` lines 133--205; `pre_sol.smooth` lines 303--394 | Backward conditional maps and smoothing weights are separate from filtering likelihood. | Deferred to P49-M6. | stochastic branch | out_of_M1_scope |

## Data Structure Contract

### `SourceRouteSampleBatch`

Required fields:

- `samples`: `tf.float64` tensor with shape `[D, N]`;
- `log_weights` or normalized weights with shape `[N]`;
- `time_index`;
- `route_label = source_faithful_filtering`;
- `sample_origin`: prior, propagated, enhanced, retained, or preconditioned.

Invariants:

- `D = d + 2m` for augmented filtering targets after propagation;
- weights are finite and normalizable;
- ESS is computed from normalized weights, not from unnormalized diagnostic
  residuals.

### `SourceRouteCoordinateFrame`

Required fields:

- `mu`: `tf.float64` tensor with shape `[D]`;
- `L`: invertible `tf.float64` tensor with shape `[D,D]`;
- `log_abs_det_L`;
- `expansion_factor`;
- source of samples and weights used to compute the frame.

Invariants:

- `L` must be nonsingular;
- target construction must include the affine determinant policy;
- the stability shift constant must not change the final likelihood except
  through the explicit `-shift_constant` normalizer contribution.

### `SourceRouteRetainedObject`

Required fields:

- retained density/transport object, not an all-axes tensor-product retained
  grid for source-faithful high-dimensional phases;
- coordinate frame `mu,L`;
- samples and proposal/correction weights;
- ESS diagnostics;
- normalizer contribution;
- branch/replay identity;
- route label and non-claims.

Invariants:

- a retained object for `source_faithful_filtering` must not expose pairwise
  all-grid propagation as its only transition interface;
- previous retained objects must support the marginalization required by the
  next-step prior;
- production code must not copy source MATLAB implementation text.

### `SourceRouteTarget`

Required fields:

- local-coordinate negative-log target;
- source terms: prior or previous retained density, transition density,
  observation likelihood, affine determinant, and shift constant;
- target-family label: full, preconditioner, residual, or smoothing.

Invariants:

- determinant and proposal-correction terms are first-class fields, not hidden
  comments;
- nonfinite target values must be classified and guarded before fitting;
- target equality must be tested on low-dimensional analytic/dense fixtures
  before production-scale claims.

## Function Boundary Contract

| Function boundary | Inputs | Outputs | Required tests |
| --- | --- | --- | --- |
| `build_initial_source_samples` | model, parameters, `N`, seed | source sample batch | shape, finite, prior density tieout |
| `push_source_samples` | model, previous samples, normalized weights, time index | augmented samples, proposal weights | one-step transition density tieout |
| `source_route_recenter` | samples, weights, expansion factor | coordinate frame | weighted mean/covariance and determinant tests |
| `build_source_route_target` | previous retained object, model densities, frame, time index | target object | affine Gaussian and nonlinear one-step target equality |
| `fit_source_transport` | target object, samples/debug samples, fit options | retained transport/density object | adaptive fit smoke, no all-grid fallback, clean-room boundary |
| `source_route_log_normalizer_update` | transport normalizer, shift constant, determinant policy | scalar log contribution | shift-invariance and determinant tests |
| `sample_source_retained_object` | retained object, random reference samples | samples plus proposal log density | proposal-density and ESS tests |
| `source_route_proposal_correction` | true target log density, proposal log density | correction log weights and ESS | dense one-step likelihood recovery |

## Reference Test Ladder For Later Phases

| Test class | Baseline | Promotion role |
| --- | --- | --- |
| Affine Gaussian one-step | exact Kalman/dense Gaussian integral | determinant, shift, normalizer accounting |
| Scalar SV transformed ladder | Kalman/mixture/CUT4 references where contract permits | low-dimensional value and gradient calibration only |
| Low-dimensional nonlinear dense quadrature | dense grid or high-order quadrature | target equality and proposal correction |
| Spatial SIR `J=1` closure | exact or dense short-horizon reference | source-route smoke only |
| Predator-prey short horizon | dense/high-order controlled reference | route/tuning separation before production rows |

## Non-Claims

This contract does not claim:

- numerical accuracy;
- paper-scale SIR or predator-prey readiness;
- HMC readiness;
- differentiability of the source route;
- adaptive TT-cross reproduction by the existing fixed branch;
- smoothing support;
- permission to copy MATLAB source code into BayesFilter.

## Open Items For Later Gates

| Item | Assigned phase | Status |
| --- | --- | --- |
| Minimal retained object skeleton and no-all-grid invariant | P49-M2 | pending |
| ESS and proposal correction tests | P49-M3 | pending |
| Recentring/Jacobian/shift tests | P49-M4 | pending |
| Preconditioned predator-prey variant ladder | P49-M5 | pending |
| Smoothing boundary and backward conditionals | P49-M6 | pending |
| Gradient-lane evidence contract | P49-M7 | pending |
