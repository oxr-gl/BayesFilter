# Read-Only Review Bundle: Phase 6 Generalized-SV Result And Phase 7 Handoff

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Codex is
supervisor and executor. Claude is read-only reviewer only.

## Objective

Review the Phase 6 generalized-SV full-row forward scalar result and the Phase
7 KSC-SV subplan for consistency, correctness, feasibility, artifact coverage,
and boundary safety.

## Files To Inspect

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase6-generalized-sv-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase7-ksc-sv-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_generalized_sv_value.py`
- `tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_artifact.py`
- `tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_tiny_artifact.py`
- `docs/plans/ledh-phase6-generalized-sv-forward-scalar-artifact-2026-07-07.md`

Do not inspect the whole repo. If extra context is required, inspect only:

- `bayesfilter/highdim/ledh_forward_contract.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`
- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`

## Phase 6 Target Contract

Target scalar:

```text
observed_data_log_likelihood_estimator
```

Reported tensor:

```text
log_likelihood
```

Generalized-SV target:

```text
y_t | x_t ~ Normal(0, exp(tau * x_t))
```

Full-row admission requires:

```text
row_id = zhao_cui_generalized_sv_synthetic_from_estimated_values
T = 1008
N = 10000
seeds = [81120,81121,81122,81123,81124]
theta = [1.0824113944610982,-2.076793740349318,0.0]
target_observation_policy = source_route_prior_mean_generalized_sv
admission_status = n10000_same_target_value_admitted
```

The log-square Gaussianized observation may be used only as an LEDH proposal
surface, not as the target likelihood.

## Phase 6 Evidence Summary

Full-row artifact:

- `docs/plans/ledh-phase6-generalized-sv-forward-scalar-artifact-2026-07-07.json`
- `admission_status = n10000_same_target_value_admitted`
- `log_likelihood_by_seed =
  [-1438.90966796875, -1438.8360595703125, -1438.908935546875,
  -1439.0206298828125, -1438.9456787109375]`
- output tensor device `/job:localhost/replica:0/task:0/device:GPU:0`
- target density `raw_zero_mean_generalized_sv_prior_mean_normal_log_density`
- flow observation transform `log(y_t^2 + 1e-6)` is proposal-only
- no actual-SV, KSC, native dense, SP500, or author-default substitution

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_generalized_sv_value.py \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_artifact.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_artifact.py -q
```

Result: `5 passed, 2 warnings in 5.02s`.

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
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_artifact.py -q
```

Result: `40 passed, 2 warnings in 2.64s`.

## Phase 7 Handoff Contract

KSC-SV row:

```text
zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000
```

Frozen target:

```text
target_observation_policy = ksc_log_chi_square_gaussian_mixture_surrogate
theta_coordinate = synthetic_unconstrained
theta = [0.2533471031357997,-0.916290731874155]
T = 1000
N = 10000
seeds = [81120,81121,81122,81123,81124]
target density = finite_ksc_log_chi_square_gaussian_mixture_log_density
transform = log(y_t^2 + 1e-8)
```

The KSC finite Gaussian mixture is the declared target likelihood for this row.
It is not exact native actual-SV likelihood and must not inherit actual-SV or
generalized-SV target evidence.

## Review Questions

Return `VERDICT: REVISE` if any are true:

- Phase 6 result admits generalized-SV without exact full-row settings or
  `require_admitted=True` replay;
- Phase 6 result still treats the tiny artifact as admitted;
- Phase 6 result uses actual-SV, KSC, native dense generalized-SV, SP500, or
  author-default evidence as target evidence;
- Phase 6 result treats log-square Gaussianized observation as target
  likelihood instead of proposal-only;
- Phase 6 result makes score, HMC, posterior, scientific-superiority, runtime
  ranking, KSC, actual-SV, or leaderboard claims;
- Phase 7 subplan allows actual-SV or generalized-SV evidence to admit KSC-SV;
- Phase 7 subplan treats KSC finite mixture as exact native actual-SV
  likelihood;
- Phase 7 subplan allows raw Gaussian SV callback likelihood as the KSC target;
- Phase 7 subplan omits transform offset `1e-8`, tiny-smoke-before-full-row
  discipline, full-row guards, replay tests, evidence contract, forbidden
  claims, handoff conditions, or stop conditions.

Return `VERDICT: AGREE` if the Phase 6 result is locally consistent and the
Phase 7 subplan is feasible, artifact-complete, and boundary-safe for KSC-SV
value admission or blocker production only.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
