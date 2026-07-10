# Phase 7 Result / Phase 8 Subplan Read-Only Review Bundle

metadata_date: 2026-07-07
review_scope: `bounded_phase7_result_phase8_handoff`

## Role Contract

Claude is read-only reviewer only.

Do not edit files, run experiments, launch agents, approve policy boundaries,
or change state.

Codex remains supervisor and executor.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Objective

Review whether Phase 7 locally closes KSC-SV same-target forward-scalar value
admission and whether the Phase 8 value-only integration subplan is safe to
execute.

Target scalar: `observed_data_log_likelihood_estimator`.

Reported tensor field: `log_likelihood`.

Scores are out of scope.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase7-ksc-sv-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase8-integration-subplan-2026-07-07.md`
- `docs/plans/ledh-phase7-ksc-sv-forward-scalar-artifact-2026-07-07.json`
- `tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_artifact.py`
- `bayesfilter/highdim/ledh_forward_contract.py`

Do not review the whole repo.

## Phase 7 Summary

Phase 7 created and locally admitted:

```text
zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000
```

Canonical full artifact:

```text
docs/plans/ledh-phase7-ksc-sv-forward-scalar-artifact-2026-07-07.json
```

Key fields:

- `admission_status = n10000_same_target_value_admitted`;
- `run_scope = full-row-admission`;
- `T = 1000`;
- `N = 10000`;
- `batch_seeds = [81120,81121,81122,81123,81124]`;
- `theta_values = [0.2533471031357997,-0.916290731874155]`;
- `target_observation_policy = ksc_log_chi_square_gaussian_mixture_surrogate`;
- `target_observation_density =
  finite_ksc_log_chi_square_gaussian_mixture_log_density`;
- `target_transform = log_y_square_plus_offset`;
- `transform_offset = 1e-8`;
- `ksc_mixture_is_target_likelihood = true`;
- `actual_sv_exact_log_chi_square_target_used = false`;
- `generalized_sv_target_used = false`;
- `legacy_raw_gaussian_callback_used = false`;
- `dense_transport_matrix_materialized = false`;
- `log_likelihood_by_seed =
  [-2288.165771484375, -2287.877685546875, -2287.852294921875,
  -2287.529296875, -2288.34375]`;
- output tensor device `/job:localhost/replica:0/task:0/device:GPU:0`.

## Local Checks Already Passed

Compile:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_ksc_sv_value.py \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_artifact.py
```

Focused replay:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_artifact.py -q
```

Result: `5 passed, 2 warnings`.

Through-Phase-7 replay:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_artifact.py -q
```

Result: `45 passed, 2 warnings`.

## Review Questions

1. Does the Phase 7 result correctly distinguish the KSC finite-mixture
   surrogate target from exact native actual-SV likelihood?
2. Does Phase 7 avoid using actual-SV, generalized-SV, raw Gaussian callback,
   score, runtime, memory, or finite-output-only evidence as KSC admission?
3. Does the Phase 8 subplan consume only admitted forward-scalar artifacts?
4. Does the Phase 8 subplan block score integration, runtime cross-ranking,
   old score-inclusive builders, and promotion of the parameterized SIR
   diagnostic row?
5. Are the Phase 8 artifacts/checks sufficient to catch stale paths, wrong row
   ids, score creep, KSC target overclaim, and diagnostic-row promotion?

## Pass Criteria

Return `VERDICT: AGREE` only if:

- Phase 7 local admission is internally consistent with the cited artifact and
  replay test;
- KSC nonclaims are boundary-safe;
- Phase 8 is feasible and does not cross score/all-algorithm/runtime-ranking
  boundaries; and
- no fixable blocker is found.

Return `VERDICT: REVISE` if any material issue remains.
