# DPF Common Model Suite V2 P1 Declarative Spec Subplan

metadata_date: 2026-06-07
phase: P1
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Can `common_model_suite_tf.py` become the single declarative v2 production
fixture surface, while v1 APIs remain available for already-closed artifacts?

## Inputs

- P0 governance result.
- `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
- Transitional fixture semantics:
  - `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
  - `experiments/dpf_implementation/tf_tfp/fixtures/stochastic_volatility_tf.py`
  - `experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py`
  - `experiments/dpf_implementation/tf_tfp/fixtures/structural_ar1_quadratic_tf.py`
- BayesFilter highdim surfaces:
  - `bayesfilter.highdim.SpatialSIRSSM`
  - `bayesfilter.highdim.PredatorPreySSM`

## Evidence Contract

Primary criterion:

- `common_model_suite_tf.py` exposes v2 specs for all six production rows:
  `lgssm_2d_h25_rich`, `sv_1d_h18_rich`,
  `range_bearing_4d_h20_rich`, `structural_ar1_quadratic_h16`,
  `spatial_sir_j3_rk4`, and `predator_prey_rk4`.
- The v2 manifest gate fails unless exactly these six model ids are present.

Veto diagnostics:

- v1 functions or old runners break;
- v2 specs remain runner-hard-coded rather than carrying their own path and
  gradient contracts;
- standalone fixture semantics are copied incompletely;
- SIR or predator-prey parameter/domain policies are changed silently;
- checksums omit observations, particles, innovations, ancestors, gradient
  knobs, scalar definitions, or tolerances.
- any v2 runner or manifest generator uses the old three-row
  `common_model_specs()` API as the v2 source;
- any change alters v1 row payloads or checksums under validation-only reads.

Non-claims:

- P1 claims only spec construction and manifest integrity, not BF/FF agreement.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_manifest_2026-06-07.json`
- P1 result ledger under `docs/plans/`.

## Required Spec Fields

Each v2 row must declare:

- model id and family;
- source surface and retirement successor relationship;
- model parameters and `theta`;
- simulated or frozen observations;
- density probes: `x0`, `x_prev`, `x_next`, `x_obs`, `observation`;
- path contract: horizon, initial particles, transition innovations,
  observations, scalar definition;
- fixed ancestor replay contract;
- gradient contract: physical knob names, initial values, finite-difference
  step, parameterization, inclusion/exclusion reason;
- tolerances and dtype.

For `spatial_sir_j3_rk4`, the spec must additionally declare state-coordinate
convention, infectious-only observation route, `domain_policy`, RK4 `delta`,
internal step, substep count, neighbor sets, graph semantics, covariances, and
gradient inclusion/exclusion reason.

For `predator_prey_rk4`, the spec must additionally declare state-coordinate
convention, direct noisy-state observation route, `domain_policy`, RK4 `delta`,
internal step, substep count, parameter box, chosen physical parameterization,
covariances, and gradient inclusion/exclusion reason for each candidate knob.

## Tasks

1. Add v2 dataclasses or extend existing dataclasses without breaking v1.
2. Add builders for all six v2 rows.
3. Add manifest serialization and checksum helpers.
4. Add tests or validation commands for exact six-row model-id membership,
   import, shape, finite-value, checksum,
   and v1-backward-compatibility checks.
5. Add the frozen pre-run row classification table required by P2.
6. Do not delete the old standalone fixture modules in P1.

## Exit Criteria

- v2 manifest validates.
- v2 manifest contains exactly the six declared production rows.
- v1 validation-only commands still read closed artifacts.
- v1 payloads/checksums are unchanged by shared-helper refactors.
- P2 pre-run row classification table is written with one row per v2 model.
- No BF/FF comparison is attempted in P1.

## Stop Conditions

- The v2 spec cannot represent SIR or predator-prey without changing their
  scientific model contract.
- Absorbing old standalone fixture semantics would require changing closed v1
  artifacts.
- Preserving v1 validation would require changing closed artifact semantics.
