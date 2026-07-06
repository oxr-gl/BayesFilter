# Phase 1 Result: Shared Forward Scalar Runner Schema

metadata_date: 2026-07-07
status: `PASSED_LOCAL_SCHEMA_GUARD_PENDING_REVIEW`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 1

## Phase Objective

Standardize the executable forward-scalar artifact schema and validator used by
all model-specific phases.

This phase is forward-scalar-only. It did not implement model-specific
adapters, admit a model row, implement scores, admit scores, or rebuild the
leaderboard.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions

- Phase 0 recorded exactly two value-admitted rows:
  - `benchmark_lgssm_exact_oracle_m3_T50`;
  - `zhao_cui_spatial_sir_austria_j9_T20`.
- Phase 0 recorded exactly four value-blocked rows:
  - `zhao_cui_predator_prey_T20`;
  - `zhao_cui_sv_actual_nongaussian_T1000`;
  - `zhao_cui_generalized_sv_synthetic_from_estimated_values`;
  - `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`.
- Phase 0 local checks passed.
- Bounded read-only review agreed that Phase 1 could begin.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong baseline | Inherited the Phase 0 admitted/blocked baseline; no row was reclassified. |
| Proxy metric promoted | Runtime, memory, finite output, and callback existence are not sufficient for admission. |
| Missing stop conditions | Tests now cover metadata-only, callback-only, wrong scalar, no target-density correction, and actual-SV/KSC cross-use. |
| Hidden assumptions | Canonical artifacts must carry row, theta, target, flow, seed, horizon, particle-count, and likelihood vectors explicitly. |
| Artifact mismatch | Phase 1 produces a schema validator only; LGSSM/SIR legacy artifact normalization is deferred to their model phases. |

Audit status: passed.

## Implementation

Added the executable artifact schema version:

```text
bayesfilter.highdim.ledh_forward_scalar_artifact.v1
```

Added canonical admission statuses:

- `metadata_only_blocked`;
- `tiny_executed_not_full_row`;
- `n10000_same_target_value_admitted`;
- `blocked_missing_current_runner`;
- `blocked_wrong_target`;
- `blocked_nonfinite`.

Added validator:

- `validate_ledh_forward_scalar_artifact(...)` in
  `bayesfilter/highdim/ledh_forward_contract.py`.

The validator requires:

- `schema_version`;
- `row_id`;
- `forward_contract`;
- `target_scalar`;
- `target_output_tensor_field`;
- `target_density_fields`;
- `proposal_flow_fields`;
- `correction_formula`;
- `theta_values`;
- `theta_coordinate_system`;
- `flow_observation_policy`;
- `target_observation_policy`;
- `target_density_used_for_correction`;
- `batch_seeds`;
- `num_particles`;
- `time_steps`;
- `log_likelihood_by_seed`;
- `average_log_likelihood_by_seed`;
- `finite_output`;
- `admission_status`;
- `nonclaims`.

For `require_admitted=True`, the validator also requires:

- `admission_status == n10000_same_target_value_admitted`;
- a full leaderboard row forward contract;
- at least `10000` particles.

## Guard Coverage

Added focused tests in:

- `tests/highdim/test_ledh_forward_scalar_admission_guard.py`

The tests assert:

- a canonical executable artifact validates;
- a metadata-only contract cannot be value admission;
- callback-only evidence without `log_likelihood_by_seed` fails;
- missing `average_log_likelihood_by_seed` fails;
- a proposal scalar cannot replace the target scalar;
- `target_density_used_for_correction != true` fails;
- ambiguous flow/target observation policy fails;
- tiny executed artifacts validate as diagnostics but cannot satisfy
  `require_admitted=True`;
- admitted status requires full-row scale;
- actual-SV and KSC-SV target policies cannot be cross-used.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Is there a shared executable artifact schema/validator that prevents metadata-only, callback-only, wrong-target, and actual-SV/KSC cross-use admission? |
| Baseline/comparator | Phase 0 baseline and existing forward contract metadata. |
| Primary criterion | Passed locally: validator/tests reject artifacts without executable `log_likelihood` evidence and reject target/flow ambiguity before row admission. |
| Veto diagnostics | No metadata-only contract can pass executable artifact validation; callback-only evidence without likelihood vector fails; actual-SV/KSC cross-use fails; proposal scalar fails; score fields are not required for value admission. |
| Explanatory diagnostics | Existing tiny artifacts, old N=10000 artifacts, and legacy callback inventories remain context only. |
| Not concluded | No model row admission, score admission, score correctness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |

## Local Checks

Focused new guard check:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py -q
```

Result:

```text
11 passed, 2 warnings in 2.91s
```

Required Phase 1 check set:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py -q
```

Result:

```text
23 passed, 2 warnings in 2.72s
```

This was a deliberate CPU-hidden schema/contract check. It is not GPU evidence
and is not model execution evidence.

## Phase 2 Handoff

Phase 2 may begin only after read-only review agrees with this result and the
Phase 2 LGSSM subplan.

Phase 2 must use this shared executable artifact schema. It may normalize the
existing LGSSM N=10000 value artifact into the canonical schema only if the
normalization preserves the row target, exact Kalman comparator identity,
theta, seed list, horizon, particle count, target density fields, proposal
correction fields, and finite `log_likelihood_by_seed`.

## Nonclaims

- No new row is value-admitted.
- No score route is implemented or admitted.
- No leaderboard is rebuilt.
- No GPU/XLA model evidence is produced.
- No HMC readiness, posterior correctness, scientific superiority, or runtime
  ranking is claimed.
