# Phase 3 Result: Fixed SIR Forward Scalar Reconfirmation

metadata_date: 2026-07-07
status: `PASSED_FIXED_SIR_FORWARD_SCALAR_LOCAL_PENDING_REVIEW`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 3

## Phase Objective

Reconfirm the fixed spatial SIR row as an executable same-target observed-data
forward scalar under the shared schema and the amended free-parameter
`sir_log_scale_theta` contract.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions

- Phase 1 schema guard passed after theta-equality repair.
- Phase 2 LGSSM canonical artifact validated locally.
- Phase 2/3 handoff review passed after the Phase 3 mandatory replay-test
  repair.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong baseline | Used only the fixed SIR N=10000 value artifact and amended SIR theta contract. |
| Proxy metric promoted | Runtime and finite output were not sufficient; the canonical artifact had to pass `require_admitted=True`. |
| Missing stop conditions | `no_free_theta`, wrong theta, missing target-density correction, missing likelihood vector, failed validation, and score creep were stop conditions. |
| Hidden assumptions | Old top-level `log_likelihood` was explicitly normalized to canonical `log_likelihood_by_seed`. |
| Artifact mismatch | Produced a canonical schema artifact and mandatory replay test, not a leaderboard rebuild. |

Audit status: passed.

## Source Artifact

Existing fixed SIR N=10000 artifact:

```text
docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json
```

The source artifact had:

- finite `log_likelihood`;
- `primary_pass_5x_runtime_gate == true`;
- `shape.num_particles == 10000`;
- `shape.time_steps == 20`;
- batch seeds `[81120, 81121, 81122, 81123, 81124]`;
- `sir_semantics.row_id == zhao_cui_spatial_sir_austria_j9_T20`;
- `sir_semantics.target_density_used_for_correction == true`.

## Canonical Artifact

Wrote canonical Phase 1 schema artifacts:

- `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.json`
- `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.md`

The canonical artifact maps:

- `log_likelihood_by_seed = log_likelihood`;
- `average_log_likelihood_by_seed = log_likelihood / 20`;
- `theta_coordinate_system = sir_log_scale_theta`;
- `theta_values = [0.0, 0.0, 0.0]`;
- `flow_observation_policy = sir_infectious_components_gaussian_flow_observation`;
- `target_observation_policy = fixed_sir_infectious_components_gaussian_observation_density`;
- `target_density_used_for_correction = true`;
- `admission_status = n10000_same_target_value_admitted`.

Validation:

```text
validate_ledh_forward_scalar_artifact(
    artifact,
    expected_row_id="zhao_cui_spatial_sir_austria_j9_T20",
    require_admitted=True,
)
```

passed during artifact generation and during the mandatory replay test.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the fixed SIR row produce or preserve an executable same-target observed-data log likelihood artifact under the shared schema and amended free-parameter target? |
| Baseline/comparator | Existing fixed SIR N=10000 value artifact and accepted `sir_log_scale_theta` row contract. |
| Primary criterion | Passed locally: canonical fixed SIR artifact validates with `require_admitted=True`, finite `log_likelihood_by_seed`, full-row scale, `sir_log_scale_theta`, theta `[0,0,0]`, and target-density correction. |
| Veto diagnostics | No `no_free_theta` admission; no missing likelihood vector; no theta mismatch; no missing target-density correction; no score evidence used for value admission; no runtime-only admission. |
| Explanatory diagnostics | Runtime, compile time, ESS, old artifact shape, and source semantics remain explanatory only. |
| Not concluded | No score admission, score correctness, exact nonlinear likelihood correctness, Zhao-Cui TT/SIRT source-faithfulness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |

## Local Checks

Mandatory Phase 3 replay check:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py -q
```

Result:

```text
2 passed, 2 warnings in 2.50s
```

Combined required check set:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py -q
```

Result:

```text
28 passed, 2 warnings in 2.57s
```

The artifact-generation command was a CPU-hidden normalization/validation
command, not a new model execution. TensorFlow emitted CUDA initialization noise
on import despite `CUDA_VISIBLE_DEVICES=-1`; this is not GPU evidence and is
not a GPU failure diagnosis.

## Phase 4 Handoff

Phase 4 may begin only after read-only review agrees with this result and the
Phase 4 predator-prey subplan.

Phase 4 is the first previously blocked model in this per-model runbook. It
must build or locate an executable predator-prey forward scalar artifact rather
than normalize a previously admitted row.

## Nonclaims

- This is `not old no_free_theta admission`.
- This is not predator-prey, SV, or generalized-SV evidence.
- No score route is implemented or admitted.
- No leaderboard is rebuilt.
- No new GPU/XLA model execution evidence is produced.
- No exact nonlinear likelihood correctness, Zhao-Cui TT/SIRT
  source-faithfulness, HMC readiness, posterior correctness, scientific
  superiority, or runtime ranking is claimed.
