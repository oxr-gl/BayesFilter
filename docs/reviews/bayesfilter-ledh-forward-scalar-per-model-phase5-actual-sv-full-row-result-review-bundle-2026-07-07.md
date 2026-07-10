# Read-Only Review Bundle: Phase 5 Actual-SV Result And Phase 6 Handoff

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Codex is
supervisor and executor. Claude is read-only reviewer only.

## Objective

Review the Phase 5 actual-SV full-row forward scalar result and the Phase 6
generalized-SV subplan for consistency, correctness, feasibility, artifact
coverage, and boundary safety.

## Files To Inspect

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase6-generalized-sv-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py`
- `tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_artifact.py`
- `tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py`
- `docs/plans/ledh-phase5-actual-sv-forward-scalar-artifact-2026-07-07.md`

Do not inspect the whole repo. If extra context is required, inspect only:

- `bayesfilter/highdim/ledh_forward_contract.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`

## Phase 5 Target Contract

Target scalar:

```text
observed_data_log_likelihood_estimator
```

Reported tensor:

```text
log_likelihood
```

Exact transformed actual-SV target:

```text
z_t = log(y_t^2)
z_t - 2 log(beta) - x_t ~ log(chi_square_1)
```

Full-row admission requires:

```text
row_id = zhao_cui_sv_actual_nongaussian_T1000
T = 1000
N = 10000
seeds = [81120,81121,81122,81123,81124]
theta = [0.2533471031357997,-0.916290731874155]
admission_status = n10000_same_target_value_admitted
```

## Phase 5 Evidence Summary

Full-row artifact:

- `docs/plans/ledh-phase5-actual-sv-forward-scalar-artifact-2026-07-07.json`
- `admission_status = n10000_same_target_value_admitted`
- `log_likelihood_by_seed =
  [-2290.10205078125, -2289.888916015625, -2289.83154296875,
  -2289.517333984375, -2290.427490234375]`
- output tensor device `/job:localhost/replica:0/task:0/device:GPU:0`
- exact transform offset `0.0`
- target density `exact_log_chi_square_log_density`
- no raw Gaussian, KSC, or augmented-noise target substitution

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_artifact.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_artifact.py -q
```

Result: `35 passed, 2 warnings in 2.69s`.

## Phase 6 Handoff Contract

Generalized-SV row:

```text
zhao_cui_generalized_sv_synthetic_from_estimated_values
```

Frozen target:

```text
target_observation_policy = source_route_prior_mean_generalized_sv
theta_coordinate = source_route_active_transformed_prior_mean
theta = [1.0824113944610982,-2.076793740349318,0.0]
T = 1008
N = 10000
seeds = [81120,81121,81122,81123,81124]
target density = raw_zero_mean_generalized_sv_prior_mean_normal_log_density
```

The log-square Gaussianized observation may be used only as an LEDH proposal
surface, not as the target likelihood.

## Review Questions

Return `VERDICT: REVISE` if any are true:

- Phase 5 result admits actual-SV without exact full-row settings or
  `require_admitted=True` replay;
- Phase 5 result still treats the tiny artifact as admitted;
- Phase 5 actual-SV target correction uses raw Gaussian observation likelihood,
  KSC finite mixture, augmented-noise Gaussian closure, or positive transform
  offset;
- Phase 5 result makes score, HMC, posterior, scientific-superiority, runtime
  ranking, generalized-SV, KSC, or leaderboard claims;
- Phase 6 subplan allows actual-SV or KSC evidence to admit generalized-SV;
- Phase 6 subplan allows native generalized-SV dense fixture substitution,
  SP500 returns as benchmark observations, or author defaults as truth;
- Phase 6 subplan treats log-square Gaussianized observation as target
  likelihood instead of proposal-only;
- Phase 6 subplan omits tiny-smoke-before-full-row discipline, full-row
  guards, replay tests, evidence contract, forbidden claims, handoff
  conditions, or stop conditions.

Return `VERDICT: AGREE` if the Phase 5 result is locally consistent and the
Phase 6 subplan is feasible, artifact-complete, and boundary-safe for
generalized-SV value admission or blocker production only.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
