# P50 Deterministic Filter Loop Contract

metadata_date: 2026-06-09
program: P50-hmc-deterministic-filtering
phase: P50-M1
status: ACTIVE_CONTRACT
route_label: hmc_compatible_deterministic_filtering

## Purpose

This contract defines the deterministic differentiable filtering loop that P50
will build and test.  It is source-inspired where useful, but its target is HMC
compatibility, not adaptive TT/SIRT source-faithful reproduction.

## Non-Goals

This contract does not require:

- adaptive TT/SIRT filtering;
- stochastic enhancement or random resampling inside the HMC gradient path;
- S&P 500 reproduction;
- smoothing/backward conditionals;
- production HMC readiness.

## Required Inputs

| Input | Contract |
| --- | --- |
| `model` | A TensorFlow/TFP-compatible state-space model with deterministic log-density evaluation for transition and observation factors. |
| `theta` | `tf.float64` parameter vector or structured parameter payload accepted by the model adapter. |
| `observations` | `tf.float64` observation tensor with time dimension first. |
| `config` | Deterministic filter configuration including quadrature/grid/TT design, coordinate-map policy, normalizer floor, dtype, and reference-measure convention. |
| `initial_state` | Optional deterministic retained filter state.  If omitted, the loop builds a deterministic initial target from the model prior and first observation. |

## Required State Object

The loop state must carry enough information to replay and differentiate the
value path:

| Field | Meaning |
| --- | --- |
| `time_index` | Current filtering time. |
| `retained_filter` | Deterministic retained approximation, currently compatible with `FixedBranchFilterStepResult.retained_filter`. |
| `coordinate_map` | Deterministic reference-to-physical coordinate map. |
| `log_normalizer_increment` | Scalar log contribution for the current step. |
| `log_likelihood_so_far` | Scalar accumulated log likelihood. |
| `accounting_terms` | Named scalar terms for target shift, coordinate-map Jacobian, proposal correction if used, and approximation normalizer. |
| `branch_identity` | Stable manifest/hash describing deterministic choices that affect value and gradient. |
| `diagnostics` | Explanatory diagnostics such as ESS-like summaries, approximation status, and reference checks. |

Existing compatible objects:

- `FixedBranchFilterResult`;
- `FixedBranchFilterStepResult`;
- `RetainedFilter`;
- `AffineCoordinateMap`;
- P49 accounting helpers in `bayesfilter.highdim.source_route`.

## Per-Step Operation Order

For time `t`, the deterministic loop must use this order:

1. Build the physical target density for the current filtering step from:
   - prior or previous retained approximation;
   - deterministic transition factor;
   - observation likelihood factor.
2. Apply the deterministic coordinate map from reference coordinates to
   physical coordinates.
3. Add the coordinate-map log absolute determinant exactly once when expressing
   a physical density in reference coordinates.
4. Apply a predeclared target shift only for numerical stabilization.
5. Fit or evaluate the deterministic retained approximation under the declared
   fixed branch/design.
6. Compute the approximation log normalizer in the reference convention.
7. Undo the target shift in log-normalizer accounting.
8. Add any deterministic proposal-correction term only if the proposal density
   and target-density convention are explicit.
9. Accumulate the scalar log-likelihood increment.
10. Store a step result with branch identity, retained filter, accounting terms,
    and diagnostics.

## Accounting Sign Convention

| Term | Required convention |
| --- | --- |
| `log_physical_density` | Log density in physical coordinates. |
| `log_reference_density` | `log_physical_density + log_abs_det(d physical / d reference)`. |
| `negative_log_target` | `-log_density` only; conversion to log-density must be explicit. |
| `shift_constant` | If `shifted_negative_log = negative_log_target - shift_constant`, then `log_increment = log_transport_normalizer - shift_constant`. |
| `log_abs_det` | Included exactly once, either inside the target or as a named separate term; the policy must be recorded. |
| `proposal_correction` | `log_target_density - log_proposal_density`, never a negative-log value unless converted by a named helper. |
| `log_likelihood` | Sum of scalar per-step log-normalizer increments. |

For each step, the composed increment must be recorded in one of these explicit
forms:

```text
log_increment =
  log_reference_normalizer
  - shift_constant
```

when the reference target already includes the coordinate-map Jacobian and no
separate proposal correction is used, or:

```text
log_increment =
  log_reference_normalizer
  - shift_constant
  + log_abs_det_term_if_separate
  + deterministic_proposal_correction_term_if_used
```

when either the Jacobian or deterministic proposal correction is kept outside
the fitted reference target.  The chosen policy must be present in
`accounting_terms`.

## Differentiability Boundary

Allowed in the HMC gradient path:

- TensorFlow/TFP tensor operations;
- deterministic fixed design choices recorded in branch identity;
- deterministic coordinate maps;
- deterministic clipping/floors only when predeclared and tested as part of the
  value path.

Forbidden without a separate reviewed contract:

- random resampling;
- adaptive sample enhancement;
- data-dependent branch changes not recorded in replay identity;
- NumPy algorithmic implementation in BayesFilter-owned differentiable paths;
- finite-difference gradients as implementation gradients.

## Reference Ladder

| Rung | Purpose | Promotion status |
| --- | --- | --- |
| Exact/dense tiny reference | Primary for one-step and low-dimensional deterministic value tieouts. | Can pass value-path gates under declared tolerances. |
| Kalman reference | Primary for linear-Gaussian and mixture-linearized SV cases where assumptions match. | Can pass model-specific value gates; approximation status must be stated. |
| CUT4 reference | Comparator for deterministic quadrature/moment behavior. | Cannot by itself prove gradient correctness. |
| Autodiff score | Primary implementation gradient source. | Must be calibrated by M4 diagnostics. |
| Directional finite-difference regression | Diagnostic for gradients. | Veto/explanatory only unless M4 declares a primary criterion. |
| Short HMC smoke | HMC-tier diagnostic. | Cannot promote full HMC readiness unless M7 tiers pass. |

## Required Tests For Implementation Phases

M2 one-step tests must cover:

- shape and dtype;
- log-density versus negative-log conversion;
- coordinate-map Jacobian counted once;
- target shift normalizer identity;
- deterministic branch identity/replay metadata;
- exact/dense one-step value agreement.

M3 sequential tests must cover:

- per-step increment sum equals total log likelihood;
- stable branch identity across replay;
- no hidden randomness;
- low-dimensional sequential reference agreement.

M4 and later phases must cover:

- value error;
- gradient norm error;
- directional cosine/error;
- likelihood variability normalization;
- HMC-tier veto diagnostics.

## Pass Boundary

Passing M1 only authorizes implementation against this contract.  It does not
claim the implementation exists, values are correct, gradients are correct, or
HMC is ready.
