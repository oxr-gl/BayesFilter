# Phase 4 Result: Manual No-Tape Score Implementation

metadata_date: 2026-07-06
status: PASSED_WITH_FALLBACK_CODEX_READ_ONLY_REVIEW
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 4

## Phase Objective

Implement or confirm analytical/manual total-derivative scores only for rows
whose same-target forward likelihood scalar was admitted in Phase 3.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong scalar | Fixed-SIR score adapter exposes `observed_data_log_likelihood_estimator` from the Phase 2/3 forward contract. |
| Scoped row promoted | The old parameterized SIR row remains `historical_diagnostic_only`; fixed SIR has a separate adapter and fixed row id. |
| Hidden autodiff | Admitted helpers and runtime tests use no `GradientTape` or `ForwardAccumulator`. |
| Stop-gradient repair | Fixed-SIR admitted score rejects `transport_ad_mode="stabilized"` and requires full transport derivative. |
| Missing total-VJP terms | Fixed-SIR component test covers all five required component channels. |
| Score before scalar | Only Phase 3 admitted rows were implemented or confirmed. |

Audit status: passed locally.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are the implemented scores derivatives of the exact Phase 3 admitted finite-`N` LEDH likelihood scalars? |
| Baseline/comparator | Phase 3 value scalars, LGSSM compact score tests, fixed-SIR same-scalar finite difference, and no-autodiff sentinels. |
| Primary criterion | Passed locally for tiny LGSSM and fixed SIR checks. |
| Veto diagnostics | No admitted score helper opened TensorFlow autodiff; fixed-SIR stopped-scale transport is rejected; scoped SIR diagnostic is not promoted. |
| Explanatory diagnostics | Finite-difference errors, component reconstruction, and historical-route parity checks. |
| Not concluded | `N=10000` memory correctness, full leaderboard readiness, HMC readiness, posterior correctness, or scientific superiority. |

## Admitted Tiny Score Rows

| Row | Score route | Status |
| --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot` | tiny same-scalar score local pass |
| `zhao_cui_spatial_sir_austria_j9_T20` | `manual_total_vjp_no_autodiff_same_scalar_fixed_sir_logscale_ledh_pfpf_ot` | tiny same-scalar score local pass |

## Blocked Rows

Rows that remain score-blocked because Phase 3 did not admit their same-target
forward scalar:

- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

The scoped `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` row
remains historical/diagnostic and is not a full observed-data score row.

## Code And Test Artifacts

- `docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py`
- `tests/test_ledh_fixed_sir_manual_score_phase4.py`
- `tests/test_ledh_lgssm_manual_score_phase4.py`
- `tests/test_ledh_score_memory_n10000.py`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase5-per-model-score-tests-subplan-2026-07-06.md`

## Local Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_fixed_sir_manual_score_phase4.py -q
```

Result: `5 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_lgssm_manual_score_phase4.py \
  tests/test_ledh_fixed_sir_manual_score_phase4.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_has_phase4_tiny_score_but_n10000_pending \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful -q
```

Result: `13 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/test_ledh_lgssm_manual_score_phase4.py \
  tests/test_ledh_fixed_sir_manual_score_phase4.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_has_phase4_tiny_score_but_n10000_pending \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful -q
```

Result: `25 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py \
  tests/test_ledh_fixed_sir_manual_score_phase4.py \
  tests/test_ledh_score_memory_n10000.py
```

Result: passed.

```text
git diff --check -- <Phase 4 files>
```

Result: passed.

## Phase 5 Handoff

Phase 5 must run trusted GPU `N=10000` correctness and memory tests for:

- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_spatial_sir_austria_j9_T20`

Phase 5 must not count the scoped parameterized SIR diagnostic as the fixed-SIR
full-row memory test.

## Nonclaims

- No `N=10000` score-memory pass is claimed in Phase 4.
- No full leaderboard rebuild is claimed.
- No exact nonlinear likelihood correctness claim for fixed SIR.
- No HMC readiness, posterior correctness, scientific superiority, or fair
  runtime ranking.

## Read-Only Review

Claude review gate was attempted twice with the bounded Phase 4 review bundle,
but the sandbox escalation approval review timed out before command execution
both times. This was treated as reviewer transport/approval unavailability, not
as a Phase 4 code blocker.

Fallback fresh Codex read-only review was run against:

- `docs/reviews/ledh-same-target-forward-score-phase4-review-bundle-2026-07-06.md`

Fallback result:

- `VERDICT=AGREE`
- Review summary: no material blockers; Phase 4 admission limited to LGSSM and
  fixed SIR; scoped parameterized SIR remains diagnostic; fixed SIR uses
  `zhao_cui_spatial_sir_austria_j9_T20`,
  `main_observed_data_filtering_row`, the Phase 2/3 target scalar, full manual
  transport derivative, and the required five component labels.

Review interpretation: this is a fallback Codex read-only review, not a Claude
primary gate. It supports advancing to Phase 5 because the local evidence and
bounded review found no material blocker. It does not authorize `N=10000`,
leaderboard, HMC, posterior, or scientific-superiority claims.
