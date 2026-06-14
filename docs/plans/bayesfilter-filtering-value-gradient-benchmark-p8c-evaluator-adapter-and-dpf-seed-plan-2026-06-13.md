# P8c Plan: Evaluator Adapter Closure, LGSSM Differentiated-Kalman Score Wiring, and DPF 5-Seed Aggregation

Date: 2026-06-13

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 8 move from partial numeric P8b output to a standardized benchmark matrix where every target-compatible algorithm/model cell has an evaluator path, value result, score result when applicable, provenance, and DPF Monte Carlo uncertainty? |
| Baseline | Current P8b runner `scripts/filtering_value_gradient_benchmark_run_p8_numeric.py`, current P8b artifact `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json`, and adapter matrix `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-adapter-status-matrix-2026-06-11.csv`. |
| Primary criterion | Every row listed in this plan either emits a standardized numeric cell with value/score/provenance or an explicit machine-readable structured status; DPF cells report mean values over 5 seeds plus standard errors before any comparison table treats them as numeric stochastic results. |
| Comparators | LGSSM exact differentiated-Kalman score for affine-equivalent sigma-point filters; declared KSC mixture route for the KSC surrogate row; algorithm-specific evaluator outputs for UKF/SVD/CUT4/Zhao-Cui/DPF on the nonlinear rows. |
| Veto diagnostics | LGSSM sigma-point score still wired to `tf_autodiff_kalman` fallback or a native sigma-point eigensystem derivative when repeated spectra block that path; any `protocol_ready_numeric_evaluator_pending` cell left silent; any DPF cell with one seed only; any DPF mean reported without seed list and MC standard error; any spatial SIR gradient emitted despite no free theta; any old LEDH-PFPF-OT result used as current evidence. |
| Explanatory diagnostics | Sigma-point branch blocker labels, value gaps to LGSSM Kalman, score coordinate systems, DPF per-seed spread, ESS/resampling summaries when available, runtime per evaluator. |
| Not concluded | Filter ranking, Bayesian-estimation readiness, HMC readiness, exact nonlinear likelihood correctness, or general DPF gradient validity. |
| Artifacts | Updated P8 numeric JSON/CSV/Markdown artifacts, focused tests, and a P8c result note under `docs/plans`. |

## Skeptical Plan Audit

Status: `REVIEWED_AND_PATCHED_BEFORE_EXECUTION`.

The current problem is not that the rows are mathematically invalid. The problem is that the runner has not yet materialized a common evaluator protocol for many target-compatible cells. The plan therefore treats `protocol_ready_numeric_evaluator_pending` as an implementation gap, not as a scientific blocker.

Risk checks:

- Wrong baseline: LGSSM sigma-point gradients must use affine equivalence to a non-eigensystem differentiated Kalman backend, not native sigma-point eigensystem differentiation when repeated eigenvalues block that path.
- Proxy metric risk: finite gradient norm is not correctness. Each score cell needs coordinate-system and derivative-provenance metadata.
- Missing stop condition: P8c cannot pass while any listed target-compatible evaluator cell remains `not_run_adapter_pending`.
- Unfair comparison risk: DPF stochastic filters must be aggregated over the same seed count and report MC standard error before comparison against deterministic filters.
- Hidden assumption risk: spatial SIR rows have no free theta in this benchmark contract; value execution is required, gradient is not applicable.
- Artifact-answer risk: regenerated tables must answer the user-facing question directly: algorithms as rows, models as columns, with values/scores and no silent holes.

Claude read-only plan review on 2026-06-13 found material pre-execution blockers. The plan was patched before code execution: the runner command now uses explicit output paths instead of a nonexistent `--metadata-date` flag; P8c tests are separate from stale P8b expectations; the adapter protocol is split into per-run evaluation and aggregation; LGSSM pass criteria require value and score tieouts, not provenance strings alone; and DPF stop rules require five successful seeds with sample standard deviation and MC standard error.

Execution-time amendment: a bounded smoke probe showed that the public QR full-Hessian path can exceed the supervised smoke budget on the P8c T=50, p=5 LGSSM cell. The already-ported graph-native covariance-form differentiated Kalman reference path with Cholesky solves executes quickly, returns value/score/Hessian for the same affine LGSSM, and avoids the sigma-point eigensystem repeated-eigenvalue problem. P8c therefore uses that non-eigensystem differentiated-Kalman reference route for promoted LGSSM value/score/Hessian cells, with provenance explicitly labeled `tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta`. This is a wiring fix, not a claim that the QR full-Hessian path is invalid.

## Scope

### Models

P8c keeps the existing Phase 8 source-scope rows:

- `benchmark_lgssm_exact_oracle_m3_T50`;
- `zhao_cui_sv_actual_nongaussian_T1000`;
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`;
- `zhao_cui_spatial_sir_austria_j9_T20`;
- `zhao_cui_predator_prey_T20`;
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

Spatial SIR has value-only evaluator status because there is no free theta in the current benchmark contract.

### Algorithms

P8c covers:

- `kalman_exact_or_mixture_enumeration` where structurally applicable;
- `ukf`;
- `svd_sigma_point`;
- `cut4`;
- `zhao_cui_scalar_or_multistate`;
- `bootstrap_dpf_current`;
- `ledh_pfpf_alg1_ukf_current`.

Historical LEDH-PFPF-OT rows remain discarded as current evidence.

## Phase P8c-1: LGSSM Non-Eigensystem Analytic Score Wiring

Goal: replace the current LGSSM sigma-point score fallback with the non-eigensystem analytic path.

Current issue:

- `scripts/filtering_value_gradient_benchmark_run_p8_numeric.py` first tries `tf_svd_ukf_score`, `tf_svd_cubature_score`, or `tf_svd_cut4_score`.
- On repeated spectra it falls back to `tf_autodiff_kalman_physical_theta_after_sigma_value_tieout`.
- The correct amended path is the affine LGSSM conversion plus a differentiated Kalman recursion that does not differentiate the sigma-point eigensystem. The supervised P8c execution uses `affine_structural_to_linear_gaussian_tf` plus the ported covariance-form differentiated Kalman reference score/Hessian route.

Implementation tasks:

1. Import `affine_structural_to_linear_gaussian_tf`, `TFLinearGaussianStateSpaceDerivatives`, and the covariance-form differentiated Kalman score/Hessian route.
2. Add `_lgssm_linear_derivatives(theta)` for physical theta `[phi1, phi2, phi3, q_scale, r_scale]`.
3. Include first and second derivatives for:
   - diagonal transition matrix in `phi`;
   - transition covariance `Q = q_scale^2 I`;
   - stationary initial covariance `diag(q_scale^2 / (1 - phi_i^2))`;
   - observation covariance `R = r_scale^2 I`.
4. In UKF/SVD/CUT4 LGSSM cells:
   - compute sigma-point value;
   - verify value tieout to exact Kalman within tolerance;
   - compute score and Hessian using the non-eigensystem differentiated Kalman route;
   - emit provenance `<algorithm>_lgssm_affine_equivalence_to_tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta`.
5. Keep the native SVD/eigen sigma-point derivative attempt as a diagnostic only, with blocker preserved if it hits `blocked_weak_spectral_gap`.
6. Do not label the differentiated-Kalman path as a native sigma-point placement derivative.

Pass criteria:

- LGSSM UKF/SVD/CUT4 score cells use non-eigensystem differentiated-Kalman provenance, not `tf_autodiff_kalman`.
- LGSSM value gap to Kalman remains below tolerance.
- LGSSM score gap to exact differentiated-Kalman reference is below tolerance.
- Hessian/curvature fields are emitted for these affine-equivalence cells when the differentiated-Kalman route returns a Hessian.
- Tests fail if a promoted provenance string is emitted without both value-gap and score-gap tieout diagnostics.

## Phase P8c-2: Standard Evaluator Adapter Protocol

Goal: make the missing evaluator adapter concrete and shared across deterministic, Zhao-Cui, and DPF lanes.

Add a runner-local or module-level protocol with two layers.

Layer 1 is a per-run evaluator:

```text
evaluate_once(
  algorithm_id,
  model_row_id,
  theta,
  observations,
  seed=None,
  particle_count=None,
) -> SingleRunEvaluation
```

Layer 2 is an aggregator/formatter:

```text
aggregate_cell(
  algorithm_id,
  model_row_id,
  evaluations: list[SingleRunEvaluation],
  adapter_status,
) -> StandardizedBenchmarkCell
```

Deterministic filters normally pass one `SingleRunEvaluation` to `aggregate_cell`. DPF filters must pass exactly five successful `SingleRunEvaluation` records for value summaries.

Required output fields:

- `algorithm_id`;
- `model_row_id`;
- `dataset_status`;
- `target_contract_status`;
- `value_adapter_status`;
- `score_adapter_status`;
- `hessian_adapter_status`;
- `numeric_execution_status`;
- `log_likelihood`;
- `average_log_likelihood`;
- `score`;
- `score_l2_norm`;
- `score_max_component`;
- `score_min_component`;
- `score_coordinate_system`;
- `score_derivative_provenance`;
- `curvature_status`;
- `hessian_min_eigenvalue_negative_log_likelihood`;
- `particle_count`;
- `seed_count`;
- `seed_list`;
- `per_seed_results`;
- `mc_standard_error`;
- `data_standard_error`;
- `reason_codes`;
- `nonclaims`;
- `runtime_seconds`;
- `evaluator_backend`.

Rules:

- Value cells must not depend on score availability.
- Score cells require explicit coordinate and provenance.
- Spatial SIR must be excluded from score dispatch and must emit value fields plus `score_adapter_status=not_applicable_no_free_theta`.
- A failing evaluator must return a structured blocker cell, not disappear from the matrix.
- All cells must survive JSON and CSV emission.

## Phase P8c-3: Deterministic UKF/SVD/CUT4 Adapters

Goal: fill UKF/SVD/CUT4 on:

- actual SV;
- KSC SV surrogate;
- predator-prey;
- generalized SV;
- spatial SIR value-only.

Implementation tasks:

1. Add model-row constructors that return observations, theta, structural model, derivative provider when applicable, and horizon metadata.
2. Route UKF to the unscented sigma-point value path and score path when derivatives exist.
3. Route SVD to the cubature sigma-point value path and score path when derivatives exist.
4. Route CUT4 to the CUT4 value path and score path when derivatives exist.
5. For KSC SV surrogate, label the target as the declared Gaussian-mixture surrogate, not actual SV truth.
6. For actual SV and generalized SV, use the row-specific transformed/additive non-Gaussian observation contract already established in P8 source-scope artifacts.
7. For predator-prey, emit a native row-specific structural evaluator with derivative status tied to the implemented derivative adapter.
8. For spatial SIR, emit value only and no score.

Pass criteria:

- No UKF/SVD/CUT4 cell on the listed rows remains `protocol_ready_numeric_evaluator_pending`.
- If a score branch blocks, the cell still has value output and an explicit score blocker.
- Score coordinate systems are row-specific and documented.

## Phase P8c-4: Zhao-Cui Scalar/Multistate Adapters

Goal: fill `zhao_cui_scalar_or_multistate` on:

- LGSSM;
- actual SV;
- KSC SV surrogate;
- predator-prey;
- generalized SV;
- spatial SIR value-only.

Implementation tasks:

1. Add an evaluator dispatch that chooses scalar or multistate Zhao-Cui based on the model row and state dimension.
2. Use exact paper/source parameter values or already approved source-scope synthetic truth values.
3. Preserve the distinction between:
   - source-faithful Zhao-Cui approximation;
   - declared KSC surrogate;
   - actual non-Gaussian SV target;
   - execution-only spatial SIR route.
4. Expose scores only where the implemented Zhao-Cui derivative path is actually available and provenance can be named.
5. Emit structured value-only status otherwise.

Pass criteria:

- No Zhao-Cui target-compatible value cell remains `protocol_ready_numeric_evaluator_pending`.
- Score cells are either numeric with provenance or explicit derivative-pending/blocker cells.
- Spatial SIR emits value-only output without pretending a free-theta gradient exists.

## Phase P8c-5: DPF 5-Seed Aggregation

Goal: convert DPF rows from blocked seed-ladder status to stochastic numeric summaries over 5 seeds.

Algorithms:

- `bootstrap_dpf_current`;
- `ledh_pfpf_alg1_ukf_current`.

Rows:

- all six Phase 8 model rows, with spatial SIR value-only and no gradient.

Seed protocol:

- Use exactly five benchmark seeds for this phase: `[81120, 81121, 81122, 81123, 81124]`.
- Use the same five seeds for both DPF algorithms and all model rows unless a row-specific deterministic seed mapping is required and documented.
- Preserve per-seed log likelihoods and score diagnostics in `per_seed_results`.
- Report:
  - mean log likelihood;
  - mean average log likelihood;
  - sample standard deviation;
  - MC standard error `sample_sd / sqrt(5)`;
  - seed count `5`;
  - seed list;
  - particle count;
  - ESS/resampling diagnostics when available.

Gradient policy:

- Main DPF score cells remain invalid unless the row has a reviewed fixed-branch or differentiable stochastic-gradient contract.
- If a fixed-branch diagnostic gradient is emitted, label it diagnostic-only and do not use it as the primary gradient benchmark.
- If no reviewed DPF gradient contract exists, value and MC uncertainty still execute and score fields remain structured status-only.

Pass criteria:

- No DPF value cell remains `blocked_pending_dpf_seed_ladder_and_mc_se`.
- Every DPF numeric value cell has `seed_count=5`, the exact shared seed list `[81120, 81121, 81122, 81123, 81124]`, five successful per-seed records, sample standard deviation, and finite `mc_standard_error`.
- Per-seed failures cannot be hidden inside an otherwise numeric aggregate cell; any failure makes the aggregate cell structured-blocked with the failing seed recorded.
- No DPF cell is ranked by gradient unless a separate reviewed gradient contract is present.
- No DPF cell emits a primary numeric score unless a separate reviewed gradient contract is cited in the cell provenance.

## Phase P8c-6: Artifact Emission and Tables

Goal: regenerate user-readable and machine-readable results.

Artifacts:

- JSON: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json`;
- value CSV/table;
- score CSV/table;
- curvature CSV/table;
- stochastic uncertainty CSV/table;
- status CSV/table;
- Markdown summary with algorithms as rows and models as columns.

Table rules:

- Value table cells show average log likelihood when numeric, otherwise structured status.
- Score table cells show score norm when numeric, otherwise structured score status.
- DPF table cells include mean +/- MC SE in a separate uncertainty table.
- Spatial SIR score cells show `not_applicable_no_free_theta`.

## Phase P8c-7: Tests and Gates

Focused tests:

1. LGSSM differentiated-Kalman route:
   - provenance contains `tf_covariance_differentiated_kalman_cholesky_solve`;
   - no LGSSM sigma-point cell uses `tf_autodiff_kalman` fallback;
   - value and score tie out.
2. Evaluator adapter coverage:
   - every listed target-compatible deterministic/Zhao-Cui value cell executes or emits a structured blocker;
   - no `protocol_ready_numeric_evaluator_pending` remains in P8c output.
3. Spatial SIR:
   - value cell executes;
   - score is `not_applicable_no_free_theta`.
4. DPF:
   - every DPF value cell has exactly 5 seeds;
   - MC SE is finite;
   - gradient status is not silently promoted.
5. Artifact integrity:
   - JSON validates with `python -m json.tool`;
   - every CSV has the full algorithm/model grid;
   - Markdown summary contains no silent `N/A`.

Suggested commands:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8_numeric.py --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json --value-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-value-table-2026-06-13.csv --score-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-score-table-2026-06-13.csv --curvature-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-curvature-table-2026-06-13.csv --status-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-status-table-2026-06-13.csv --uncertainty-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-stochastic-uncertainty-table-2026-06-13.csv --markdown docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-summary-2026-06-13.md
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8c_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8c_numeric.py
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim docs/plans
```

The P8c run must use explicit output-path flags unless the runner is later extended with a reviewed `--metadata-date` option. P8b tests must not be edited to pretend P8c and P8b are the same artifact; add a P8c-specific test file or update tests only if the P8b artifact itself is intentionally superseded.

## Claude Review Loop

Claude is read-only reviewer only; Codex remains supervisor and executor.

Review prompt scope:

- Check whether LGSSM differentiated-Kalman analytic wiring is correctly distinguished from native sigma-point eigensystem derivatives.
- Check whether every listed adapter gap has an execution or structured-blocker path.
- Check whether DPF 5-seed aggregation is enough for this phase's stochastic value summaries and whether gradient claims remain properly limited.
- Check whether spatial SIR value-only/no-free-theta semantics are preserved.

Convergence:

- Loop until Claude reports no material blockers or max 5 iterations.
- If Claude does not respond, run a tiny probe through the trusted Claude worker wrapper. If the probe responds, rewrite the review prompt into smaller chunks rather than declaring Claude unavailable.

## Stop Conditions

Stop and patch the plan/result before claiming P8c success if:

- any listed target-compatible value cell is still `not_run_adapter_pending`;
- any DPF value cell lacks exactly five successful per-seed evaluations, the shared seed list, sample standard deviation, or MC SE;
- any DPF primary score is numeric without a reviewed gradient contract;
- any LGSSM sigma-point score provenance says `tf_autodiff_kalman`;
- any LGSSM affine-equivalence value or score tieout exceeds tolerance;
- any spatial SIR score is numeric;
- old LEDH-PFPF-OT appears as current evidence;
- generated tables hide a structured blocker or status behind blank/`N/A`.

## Result Note To Write After Execution

Write `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-evaluator-adapter-and-dpf-seed-result-2026-06-13.md` with:

- command manifest;
- git commit and dirty-state summary;
- CPU/GPU status;
- seeds and particle counts;
- complete value table;
- complete score/status table;
- DPF uncertainty table;
- decision table;
- post-run red-team note;
- Claude review ledger links if review is run.
