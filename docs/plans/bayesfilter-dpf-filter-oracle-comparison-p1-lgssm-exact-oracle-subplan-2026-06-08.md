# P1 Subplan: LGSSM Exact-Oracle Value and Gradient Comparison

metadata_date: 2026-06-08
phase: P1
status: REVIEWED_READY_AFTER_P0_PASS

## Question

For LGSSM targets, are BayesFilter DPF value and gradient estimates
statistically close to exact Kalman value and analytic Kalman gradient, and do
deterministic filters recover the exact route where they should?

## Evidence Contract

Baseline/comparator:

- exact Kalman log likelihood;
- analytic Kalman gradient in the declared parameterization;
- optional deterministic sanity routes: UKF, SVD/sigma-point, CUT4, and
  Zhao-Cui/fixed-design TT only if P0 classifies them as same-target for LGSSM.

Primary criteria:

- Kalman reference value and gradient pass existing reference tests or a new
  focused reference validation;
- deterministic same-target routes match Kalman within tight numerical
  tolerance or are classified as approximation/blocked;
- DPF bootstrap-OT and LEDH-PFPF-OT report paired multi-seed value and gradient
  errors against Kalman;
- DPF reports evaluator variance across seeds and particle ladder levels.

Default DPF stochastic contract:

- seeds: at least five paired seeds;
- particle counts: at least two counts, with the third-count trigger inherited
  from the master stochastic evidence minimums;
- confidence intervals: 95% CI for mean value and gradient errors;
- promotion is blocked if larger particle counts fail to reduce both value RMSE
  and score RMSE or if evaluator variance is not reported.

Primary gradient object:

- exact comparator: `reference_score` from analytic Kalman recursion;
- DPF candidate: `fixed_branch_score` unless a reviewed stochastic-score
  amendment is accepted before execution;
- scalar differentiated: the declared DPF log-likelihood or negative
  log-likelihood scalar matching the Kalman value convention, with all sign
  conventions recorded.

Suggested metrics:

- value error `L_method - L_kalman`;
- per-observation value error;
- gradient vector error `g_method - g_kalman`;
- relative score error `||e_g|| / max(1, ||g_kalman||)`;
- coordinate/block absolute errors;
- gradient cosine similarity;
- DPF mean, bias, standard error, RMSE, and max error by particle count.

Veto diagnostics:

- analytic gradient missing or parameterization mismatch;
- value target mismatch;
- DPF gradient is a fixed-branch proxy but is reported as full stochastic
  score;
- evaluator variance is not separated from bias;
- value pass used to excuse gradient failure.

Explanatory-only diagnostics:

- ESS, resampling counts, Sinkhorn residuals, wall time, and AD-vs-FD checks.

What will not be concluded:

- no nonlinear model correctness;
- no stochastic-resampling distribution correctness;
- no HMC readiness.

## Tasks

1. Select LGSSM fixtures from P0 eligible rows.
2. Freeze parameter vector and transform.
3. Implement or select exact Kalman value/gradient reference.
4. Run deterministic filter sanity routes classified by P0.
5. Run DPF particle ladder with paired seeds.
6. Write JSON and markdown result artifacts.
7. Run Claude read-only result review.

## Planned Commands And Artifacts

Runner status:
planned module; P1 `PRECHECK` must implement this runner, select an existing
runner by reviewed amendment, or write a blocker before any execution claim.

Planned command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf --validate-only
```

If a different existing runner is selected instead, the phase must write a
reviewed amendment before execution and preserve the same artifact contract.

Required artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p1_lgssm_exact_oracle_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-claude-review-ledger-2026-06-08.md`

Claude result review follows the master max-five read-only loop.  Unresolved
material findings at the cap force `BLOCKED_FOR_HUMAN_REVIEW`.

## Exit Criteria

P1 exits with `PASS_P1_LGSSM_EXACT_ORACLE_READY_FOR_P2` only after reviewed
Kalman reference, value evidence, gradient evidence, DPF Monte Carlo
uncertainty, and nonclaims are recorded.

## Stop Conditions

- exact Kalman gradient cannot be computed in the target parameterization;
- DPF value or gradient path cannot be tied to the same scalar;
- same-target deterministic route fails and cannot be classified without a
  repair amendment.
