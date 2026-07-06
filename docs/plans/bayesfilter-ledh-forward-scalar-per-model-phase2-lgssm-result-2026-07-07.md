# Phase 2 Result: LGSSM Forward Scalar Reconfirmation

metadata_date: 2026-07-07
status: `PASSED_LGSSM_FORWARD_SCALAR_LOCAL_PENDING_REVIEW`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 2

## Phase Objective

Reconfirm the exact linear-Gaussian LEDH row under the shared executable
forward-scalar artifact schema.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions

- Phase 1 schema guard passed after repair.
- `validate_ledh_forward_scalar_artifact(...)` requires executable
  `log_likelihood_by_seed`, `average_log_likelihood_by_seed`, target-density
  correction, row/target identity, and theta equality with forward-contract
  `truth_theta`.
- Phase 2 LGSSM subplan was drafted and reviewed through the Phase 1 repair
  gate.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong baseline | Used only the existing LGSSM N=10000 value artifact and its exact Kalman target identity. |
| Proxy metric promoted | Runtime and finite output were not sufficient; the canonical artifact had to pass `require_admitted=True`. |
| Missing stop conditions | Theta mismatch, missing likelihood vectors, wrong comparator, wrong target, failed validation, and score creep were stop conditions. |
| Hidden assumptions | Old `total_log_likelihood_by_seed` was explicitly normalized to canonical `log_likelihood_by_seed`. |
| Artifact mismatch | Produced a canonical schema artifact and replay test, not a leaderboard rebuild. |

Audit status: passed.

## Source Artifact

Existing LGSSM N=10000 artifact:

```text
docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.json
```

The source artifact had:

- row id `benchmark_lgssm_exact_oracle_m3_T50`;
- `primary_pass_same_target_value_execution == true`;
- finite `total_log_likelihood_by_seed`;
- `shape.num_particles == 10000`;
- `shape.time_steps == 50`;
- batch seeds `[81120, 81121, 81122, 81123, 81124]`;
- exact comparator `tf_kalman_log_likelihood on same observations/model`;
- truth theta `(0.72, 0.55, 0.35, 0.35, 0.45)`.

## Canonical Artifact

Wrote canonical Phase 1 schema artifacts:

- `docs/plans/ledh-phase2-lgssm-forward-scalar-artifact-2026-07-07.json`
- `docs/plans/ledh-phase2-lgssm-forward-scalar-artifact-2026-07-07.md`

The canonical artifact maps:

- `log_likelihood_by_seed = total_log_likelihood_by_seed`;
- `average_log_likelihood_by_seed = total_log_likelihood_by_seed / 50`;
- `flow_observation_policy = identity_lgssm_observation_flow`;
- `target_observation_policy = lgssm_gaussian_observation_density`;
- `target_density_used_for_correction = true`;
- `admission_status = n10000_same_target_value_admitted`.

Validation:

```text
validate_ledh_forward_scalar_artifact(
    artifact,
    expected_row_id="benchmark_lgssm_exact_oracle_m3_T50",
    require_admitted=True,
)
```

passed during artifact generation and during the replay test.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the LGSSM row produce or preserve an executable same-target observed-data log likelihood artifact under the shared schema? |
| Baseline/comparator | Existing LGSSM N=10000 value artifact and exact Kalman log likelihood on the same observations/model. |
| Primary criterion | Passed locally: canonical LGSSM artifact validates with `require_admitted=True`, finite `log_likelihood_by_seed`, full-row scale, and exact Kalman target identity. |
| Veto diagnostics | No missing likelihood vector; no target scalar mismatch; no theta mismatch; no score evidence used for value admission; no runtime-only admission. |
| Explanatory diagnostics | Exact Kalman delta, runtime, compile time, and ESS remain explanatory only. |
| Not concluded | No nonlinear-row evidence, score admission, score correctness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |

## Local Checks

Phase 2 replay check:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py -q
```

Result:

```text
2 passed, 2 warnings in 2.55s
```

Combined required check set:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py -q
```

Result:

```text
26 passed, 2 warnings in 2.77s
```

The artifact-generation command was a CPU-hidden normalization/validation
command, not a new model execution. TensorFlow emitted CUDA initialization noise
on import despite `CUDA_VISIBLE_DEVICES=-1`; this is not GPU evidence and is
not a GPU failure diagnosis.

## Phase 3 Handoff

Phase 3 may begin only after read-only review agrees with this result and the
Phase 3 fixed SIR subplan.

Phase 3 must normalize or refresh the fixed SIR row into the same canonical
schema, with:

- row id `zhao_cui_spatial_sir_austria_j9_T20`;
- theta coordinate `sir_log_scale_theta`;
- theta `(0, 0, 0)`;
- finite `log_likelihood_by_seed`;
- full-row scale;
- target-density correction;
- no score admission.

## Nonclaims

- This is `not nonlinear-row evidence`.
- No nonlinear row is value-admitted by this phase.
- No score route is implemented or admitted.
- No leaderboard is rebuilt.
- No new GPU/XLA model evidence is produced.
- No HMC readiness, posterior correctness, scientific superiority, or runtime
  ranking is claimed.
