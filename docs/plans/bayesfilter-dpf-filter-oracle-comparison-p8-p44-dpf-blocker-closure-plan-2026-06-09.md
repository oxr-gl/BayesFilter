# P8 Plan: P44 DPF Blocker Closure And N/A Metric Fill

metadata_date: 2026-06-09
phase: P8
status: PLAN_REVIEW_AGREED_READY_FOR_VISIBLE_EXECUTION

## Question

Can the two DPF routes, `dpf_bootstrap_ot` and `dpf_ledh_pfpf_ot`, be run on
the P44 exact-target panels with reviewed same-target adapters so the P6
`N/A` cells for value and fixed-branch gradient metrics become measured rows
rather than blocked rows?

## Scope

Targets:

- `p44_m2_cubic_additive_gaussian_panel`
- `p44_m3_quadratic_observation_panel`
- `p44_m4_nonlinear_transition_h2_panel`

Routes:

- `dpf_bootstrap_ot`
- `dpf_ledh_pfpf_ot`

Primary output:

- A new P8 JSON/report/result artifact with measured P44 DPF value and
  fixed-branch score metrics, row decisions, branch records, directional
  residuals, and explicit nonclaims.
- A P6-amended display table that fills the previous P44 DPF `N/A` cells from
  P8 evidence without overwriting the historical P6 result.

Execution sequence:

- P8 is gated. It must first pass a P44-M2 dim-1 adapter probe for both DPF
  routes. P44-M3/M4 and higher dimensions must not run until that probe exits
  `PASS_P8_M2_DIM1_ADAPTER_GATE`.

## Six Blockers And Planned Fixes

| Blocker | Planned fix |
| --- | --- |
| Placeholder DPF bands | Predeclare numeric P8 reporting and promotion bands before execution. |
| Missing same-target DPF adapter | Implement P44 M2/M3/M4 DPF adapters using the same observation paths, parameterizations, state transitions, and dense-reference scalar sign convention as the P44 oracle panels. |
| Missing paired-seed variance | Run paired seeds for both DPF routes and report mean, RMSE, SE, CI95, max errors, and evaluator variance summaries. |
| Fixed-branch gradient not tied to dense scalar | Differentiate the DPF log-likelihood estimator with respect to the same P44 theta vector and compare against the dense log-likelihood score. |
| Missing directional derivative residuals | Run central finite-difference directional checks for each method/target/dim at one audited seed/count and record residuals and branch-signature stability. |
| Missing branch records | Store per-seed, per-particle-count, per-time ESS, resampling decision, resampling method, transport diagnostics, and LEDH diagnostics. |

## Evidence Contract

Scientific/engineering question:

- Are P44 DPF value and fixed-branch gradient estimates now measured against
  the correct same-target dense references, and if so, are they close enough
  under predeclared bands to be promoted, diagnostic, or failed?

Baseline/comparator:

- Exact-target dense refined quadrature reference for the corresponding P44
  target and dimension.
- P44-M2 references may use the existing P2 structured dense-reference JSON.
- P44-M3/M4 references must be exported as structured P8 reference rows before
  DPF calibration. Markdown-only P44 source notes are not sufficient for
  promotion.

Primary criterion:

- Every P44 target/method row must exit with one of:
  `PROMOTED_EXACT_TARGET_CLOSENESS`, `DIAGNOSTIC_ONLY_MEASURED`,
  `FAILED_NUMERIC_BANDS`, or `BLOCKED_WITH_REVIEWED_REASON`.
- The previous P6 `N/A` cells are considered filled only for rows with finite
  DPF value and gradient metrics, paired-seed variance, directional residual
  records, and branch records.

Predeclared numeric bands:

- Particle counts: `[128, 256]`; a third count `512` is triggered if the
  256-particle row has value CI excluding zero, mean relative score error above
  the diagnostic band, nonfinite rows, unstable branch signatures in directional
  checks, or less than 25 percent RMSE reduction from 128.
- Paired seeds: `[101, 202, 303, 404, 505]`.
- Reporting band: finite value RMSE, score RMSE, mean relative score error,
  CI95, max absolute value error, max relative score error, directional residual
  maximum, and branch records must be emitted.
- Diagnostic band: mean absolute per-observation value error <= `0.50` and
  mean relative score error <= `1.00`.
- Promotion band: CI95 for mean per-observation value error lies within
  `[-0.10, 0.10]`, value RMSE per observation <= `0.25`, mean relative score
  error <= `0.35`, score RMSE <= `max(1.0, 0.50 * reference_score_norm)`,
  max relative score error <= `0.75`, and directional residual max <= `0.25 *
  max(1.0, reference_score_norm)`.
- Failure band: finite measured rows that exceed diagnostic bands are
  `FAILED_NUMERIC_BANDS`, not blocked.

Fixed-branch score contract:

- The differentiated scalar is the DPF log-likelihood estimator for the same
  P44 observations and theta vector used by the dense reference.
- During differentiation, stateless initial draws, transition/proposal draws,
  realized ESS-triggered branch decisions, and realized transport application
  choices are fixed for the row.
- Gradients through random draws, through the discrete ESS/resampling decision,
  or through the probability law of branch selection are not claimed.
- The branch signature is the ordered per-time tuple of ESS, resampling boolean,
  resampling method, transport active-mask status, Sinkhorn/annealed-transport
  iteration status, and LEDH local-linearization convention where applicable.
- The score sign convention is `score = d log_likelihood / d theta`, matching
  the dense reference scalar exactly.

Relative-score metric:

- Let `g_dpf` be the fixed-branch DPF score vector and `g_ref` the dense
  reference score vector for the same target and dimension.
- `reference_score_norm = ||g_ref||_2`.
- `score_error_norm = ||g_dpf - g_ref||_2`.
- `relative_score_error = score_error_norm / max(1.0, reference_score_norm)`.
- Row summaries report seed means, RMSE over seed score-error norms, standard
  error, CI95 for scalar value errors, max relative score error, and the final
  particle-count value used for classification.

Directional residual contract:

- Directional checks are required at the final reported particle count for
  every measured row. If a third particle count is triggered, directional
  checks must run at that third count.
- Directional checks use the same fixed branch signature as the AD score. If
  the central finite-difference plus/minus evaluations change the branch
  signature, the row cannot be promoted and must be diagnostic or blocked with
  the branch instability recorded.
- Directional residual is
  `max_i |v_i^T g_ad - (L(theta + eps v_i) - L(theta - eps v_i)) / (2 eps)|`
  for canonical coordinate directions plus at least two mixed unit directions.

LEDH target convention contract:

- Before any LEDH row runs, the adapter must emit a structured convention
  record for each P44 target containing the transition prior mean, transition
  covariance, observation function, observation Jacobian, residual convention,
  local linearization point, and PF-PF corrected-weight formula.
- If any LEDH convention field is absent, LEDH rows for that target are blocked
  before execution.

Veto diagnostics:

- Dense reference row missing or not machine-readable.
- DPF adapter does not use the same observations, parameterization, or scalar
  sign convention as the dense reference.
- TensorFlow imports before CPU-only device hiding.
- Any nonfinite DPF value or gradient.
- Seed/evaluator variance omitted.
- Directional residuals omitted.
- Branch records omitted.
- LEDH route used on a target without a declared observation Jacobian or local
  transition/prior-mean convention.
- A row is promoted while branch signatures change in the directional residual
  check.
- Historical P6 `N/A` cells are overwritten rather than filled in a P8/P6
  amendment artifact.

P44-M2 dim-1 adapter gate:

- Run both DPF routes on `p44_m2_cubic_additive_gaussian_panel`, dim `1`, at
  `128` particles and seeds `[101, 202, 303, 404, 505]`.
- Also run directional residual checks at `128` particles for one representative
  seed per route.
- Stop before M3/M4 or dim 2/3 if any of the following occurs: nonfinite value
  or score, adapter scalar sign mismatch against dense reference, missing
  branch records, missing evaluator variance, missing LEDH convention record,
  branch-signature instability in directional checks, or directional residual
  above the diagnostic band.
- Passing this gate does not promote DPF. It only authorizes the full P44 P8
  measurement run.

Explanatory-only diagnostics:

- ESS summaries, resampling counts, Sinkhorn residuals, LEDH Jacobian singular
  values, runtime, value RMSE ladder trend, score RMSE ladder trend, and
  branch-signature mismatch details for non-promoted rows.

What will not be concluded:

- No universal DPF superiority.
- No stochastic-score correctness; gradients are fixed-branch scores only.
- No production, HMC, GPU, public API, or default-policy readiness.
- No claim that a diagnostic or failed row is scientifically invalid; it may
  require tuning, larger particle counts, or a better proposal.

Artifact preserving the result:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p8_p44_dpf_blocker_closure_2026-06-09.json`
- Report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-2026-06-09.md`
- Result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-result-2026-06-09.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-claude-review-ledger-2026-06-09.md`
- Amended P6 display:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-amended-with-p8-dpf-metrics-2026-06-09.md`

Serious-run manifest requirement:

- The result artifact must include a run manifest with git commit, exact
  command, environment or conda env, CPU/GPU status, data/source version when
  applicable, random seeds, wall time, output artifact paths, plan file, and
  result file. `N/A` is allowed only for fields that genuinely do not apply.

Decision-table requirement:

- The result artifact must include a decision table with decision, primary
  criterion status, veto diagnostic status, main uncertainty, next justified
  action, and what is not being concluded.

Post-run or post-blocker red-team requirement:

- If P8 executes numerical DPF rows, the result artifact must include a
  post-run red-team note with strongest alternative explanation, what result
  would overturn the conclusion, and weakest part of the evidence.
- If P8 stops before full execution, the result artifact must include a
  post-blocker red-team note and the structured blocker-manifest path explaining
  which gate stopped the run and what smallest artifact would unblock it.

## Skeptical Plan Audit

Status: `PASS_CLAUDE_REVIEW_AGREED_ITERATION_5`.

Wrong-baseline risk:

- Controlled by comparing DPF only to same-target dense P44 references. The
  deterministic CUT4/Zhao-Cui rows remain context, not DPF promotion baselines.

Proxy-promotion risk:

- Controlled by separating measured diagnostic rows from promoted rows. Filling
  an `N/A` cell is not a promotion unless all numeric and veto criteria pass.

Missing stop-condition risk:

- Controlled by row-level exit labels and veto diagnostics. Nonfinite rows,
  missing references, missing branch records, or missing directional residuals
  stop promotion.

Unfair-comparison risk:

- Controlled by paired seeds, common observations, fixed particle-count ladder,
  and the same dense reference scalar/score per target/dim.

Hidden-assumption risk:

- Controlled by recording CPU-only TensorFlow mode, parameterization, scalar
  sign convention, fixed-branch gradient definition, and LEDH local
  linearization convention.

Stale-context risk:

- Controlled by validating the current P44 dense-reference helpers, DPF runner
  APIs, and output paths immediately before implementation and recording the
  git commit in the run manifest. Older P6/P7 tables are historical context
  only unless regenerated or explicitly amended by P8.

Environment-mismatch risk:

- Controlled by running TensorFlow in deliberate CPU-only mode with
  `CUDA_VISIBLE_DEVICES=-1` set before import, recording the environment in the
  manifest, and treating GPU, conda, or sandbox differences as outside the P8
  claim.

Artifact adequacy risk:

- Controlled by writing structured JSON for all reference, DPF, branch,
  directional residual, and row-decision records before generating the amended
  display table.

## Pre-Mortem

How the run could pass while misleading us:

- The DPF adapter could match scalar signs and shapes while silently using a
  different observation path, parameter transform, or dense-reference target.
- Fixed-branch gradients could agree with finite differences only on stable
  branch signatures while remaining poor estimators of stochastic score
  behavior.
- Paired-seed summary intervals could look acceptable at small dimensions while
  hiding particle-count sensitivity, target-specific instability, or untested
  higher-dimensional failure.
- LEDH could appear competitive because the local linearization convention is
  favorable for one target but not a generally valid proposal convention.

How the run could fail for implementation or tuning reasons rather than the
scientific idea:

- Particle counts `[128, 256, 512]` may be too small for a nonlinear P44 target.
- ESS thresholds, transport settings, LEDH local covariance regularization, or
  finite-difference epsilons may be poorly tuned.
- Branch signatures may change under directional perturbations because of
  threshold ties rather than because the DPF value path is unusable.
- Dense-reference export or validation may expose a target-contract bug before
  any meaningful DPF evidence is collected.

Cheapest discriminating diagnostics:

- Start with the P44-M2 dim-1 gate and inspect same-target scalar tieout,
  branch records, finite gradients, and directional residuals before running
  M3/M4.
- If a row fails numeric bands but has finite stable branches, rerun only that
  target/method at the triggered 512-particle count and compare RMSE reduction.
- If a row fails directional residuals, repeat one seed with a larger
  branch-stability margin or a smaller finite-difference epsilon before
  interpreting the failure as a method limitation.
- If LEDH fails while bootstrap DPF is finite, inspect the emitted LEDH
  convention record and local Jacobian diagnostics before treating the failure
  as evidence against DPF generally.

## Execution Tasks

1. Plan review: run Claude read-only review, revise until `VERDICT: AGREE` or
   five iterations. If unresolved material findings remain at iteration 5, stop
   with `BLOCKED_FOR_HUMAN_REVIEW` rather than executing.
2. Implement P44 same-target DPF adapter and runner.
3. Implement structured dense-reference export for P44-M3/M4 and a validator.
4. Validate CPU-only import discipline and syntax.
5. Run the P44-M2 dim-1 adapter gate for both DPF routes.
6. If and only if the M2 dim-1 gate passes, run full P44 M2/M3/M4,
   dims 1/2/3, both DPF routes, paired seeds, and
   particle ladder.
7. Write P8 JSON/report/result and P6-amended display table, including the
   required serious-run manifest and result-note decision table.
8. Run validators.
9. Run Claude result review, revise until `VERDICT: AGREE` or five iterations.
   If unresolved material result-review findings remain at iteration 5, record
   `BLOCKED_FOR_HUMAN_REVIEW` with the unresolved finding list.

## Planned Commands

Plan review command pattern:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-p8-p44-plan-review-iterN \
  "Review docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-plan-2026-06-09.md ..."
```

Claude execution control:

- Plan-review and result-review Claude calls must run through the approved
  read-only wrapper with trusted/elevated permissions. Non-trusted Claude
  hangs, missing output, auth failures, or network failures are sandbox
  evidence only until the same bounded wrapper prompt is rerun in the trusted
  context.
- Claude remains read-only: review prompts may use read/list/search tools but
  must not grant edit/write/bash mutation tools.

Execution command pattern:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-p8-mpl \
  python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p8_p44_dpf_blocker_closure_tf

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-p8-mpl \
  python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p8_p44_dpf_blocker_closure_tf --validate-only
```

## Exit Criteria

P8 exits with `PASS_P8_P44_DPF_BLOCKER_CLOSURE_READY_FOR_REVIEW` if every P44
DPF row has finite measured metrics or a reviewed residual blocker, and the
amended display fills every previous P44 DPF `N/A` cell with either numeric
metrics or a new reviewed failure/blocker label.

P8 exits with `BLOCKED_P8_P44_DPF_ADAPTER_GATE` if the P44-M2 dim-1 gate fails
before full execution. In that case, M3/M4 remain unrun and the amended display
must state that the original P6 `N/A` cells remain blocked by the failed adapter
gate rather than by missing implementation.
