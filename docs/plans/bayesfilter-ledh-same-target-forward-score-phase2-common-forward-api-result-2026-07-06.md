# Phase 2 Result: Common Forward Likelihood API

metadata_date: 2026-07-06
status: PASSED_WITH_BOUNDED_FALLBACK_REVIEW
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 2

## Phase Objective

Build a shared metadata/API contract that separates target likelihood
densities from LEDH proposal/flow quantities and labels the finite-`N`
leaderboard scalar as the observed-data log-likelihood estimator.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong baseline | Used the Phase 1 target/theta contract and existing LGSSM/SIR LEDH runners. |
| Proxy metric promoted | The new contract is metadata-only and cannot admit rows or scores. |
| Proposal scalar promoted | Validation rejects proposal scalar names and requires the target scalar `observed_data_log_likelihood_estimator`. |
| Scoped SIR promotion | Validation rejects the scoped parameterized SIR diagnostic when marked as a full leaderboard row. |
| Fixed SIR theta regression | Validation rejects fixed SIR `no_free_theta` and requires `sir_log_scale_theta`, dimension 3, and exact parameter order. |
| Backend drift | No new numerical backend was introduced. New code is metadata validation and runner metadata wiring only. |

Audit status: passed for Phase 2 execution.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the shared API make it impossible to confuse proposal flow quantities with the target likelihood scalar? |
| Baseline/comparator | Existing LGSSM/SIR LEDH runners and Phase 1 row contracts. |
| Primary criterion | Passed locally: contract labels `observed_data_log_likelihood_estimator`, requires target transition/observation densities, and keeps `pre_flow_log_density`/`forward_log_det` as correction fields. |
| Veto diagnostics | No proposal scalar was exposed as target; no missing target densities; fixed SIR remains 3D `sir_log_scale_theta`; scoped SIR remains diagnostic-only; no NumPy/JAX/PyTorch algorithmic path added. |
| Explanatory diagnostics | Contract manifests are embedded in new LGSSM and scoped-SIR artifacts and synthesized for older inclusive-leaderboard artifacts. |
| Not concluded | No new model row is admitted. No score route is admitted. No HMC readiness or posterior correctness is claimed. |

## Code Artifacts

- `bayesfilter/highdim/ledh_forward_contract.py`
- `bayesfilter/highdim/__init__.py`
- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
- `tests/highdim/test_ledh_forward_contract_phase2.py`

## What The Contract Enforces

- `target_scalar = observed_data_log_likelihood_estimator`
- `output_tensor_field = log_likelihood`
- target density fields:
  - `transition_log_density`
  - `observation_log_density`
- proposal/flow correction fields:
  - `pre_flow_log_density`
  - `forward_log_det`
  - `proposal_observation_surface`
- correction formula:
  `transition_log_density + observation_log_density - pre_flow_log_density + forward_log_det`

For fixed SIR, the contract requires:

- row id `zhao_cui_spatial_sir_austria_j9_T20`;
- row scope `main_observed_data_filtering_row`;
- theta coordinate `sir_log_scale_theta`;
- theta dimension `3`;
- parameter order `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`;
- truth theta `[0,0,0]`.

For scoped parameterized SIR, the contract requires:

- row id `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`;
- scope `legacy_scoped_parameterized_sir_diagnostic`;
- `full_leaderboard_row = false`.

## Local Checks

CPU-only checks intentionally hid GPU devices with `CUDA_VISIBLE_DEVICES=-1`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  bayesfilter/highdim/ledh_forward_contract.py \
  bayesfilter/highdim/__init__.py \
  docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_score_remains_blocked \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful -q
```

Result: `18 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_lgssm_manual_score_phase4.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

Result: `13 passed, 2 warnings`.

```text
git diff --check -- \
  bayesfilter/highdim/ledh_forward_contract.py \
  bayesfilter/highdim/__init__.py \
  docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py \
  tests/highdim/test_ledh_forward_contract_phase2.py
```

Result: passed.

## Boundary Safety

- No row was admitted from metadata alone.
- No leaderboard was rebuilt.
- No score implementation was added.
- No `GradientTape`, `ForwardAccumulator`, or autodiff route was introduced.
- No scoped SIR diagnostic was promoted to full fixed-SIR evidence.
- No HMC readiness or posterior correctness claim is made.

## Read-Only Review

Claude review gate command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/BayesFilter \
  --review-name ledh-same-target-forward-score-phase2 \
  --bundle /home/chakwong/BayesFilter/docs/reviews/ledh-same-target-forward-score-phase2-review-bundle-2026-07-06.md \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Review result:

- `REVIEW_STATUS=bounded_fallback_agree`
- `VERDICT=AGREE`
- run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260706-171156-ledh-same-target-forward-score-phase2`
- summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260706-171156-ledh-same-target-forward-score-phase2/status.json`

Interpretation: this is weaker than a full primary material review. It is
recorded as a bounded no-obvious-blocker signal after the primary review path
did not produce a direct full-review verdict.

## Phase 3 Handoff

Phase 3 may begin after read-only review if the reviewer finds no material
blocker. Phase 3 must admit value scalars model by model. The first task is to
use the Phase 2 contract to verify each candidate row computes the same
observed-data log-likelihood estimator, not a proposal objective.
