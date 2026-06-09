# P5 Subplan: DPF Statistical Closeness for Value and Gradients

metadata_date: 2026-06-08
phase: P5
status: REVIEWED_READY_AFTER_P4_PASS

## Question

On rows with approved exact or approximation references, are DPF bootstrap-OT
and LEDH-PFPF-OT statistically close in value and gradients under paired
multi-seed particle ladders?

## Evidence Contract

Baseline/comparator:

- P1-P4 approved reference route per target;
- exact references and approximation references must be reported in separate
  tables.

Primary criteria:

- import row-level `promotion_tolerance` and `certification_band` from the P0
  registry before any DPF run;
- run DPF methods with paired seeds and common observations;
- use at least five paired seeds and at least two particle counts;
- add a third particle count under the master stochastic evidence trigger;
- report same-dataset evaluator variance;
- report value bias, RMSE, standard error, max error, and per-observation error;
- report gradient vector error, relative score error, coordinate/block errors,
  directional derivative residuals, cosine similarity, and evaluator variance;
- classify each row as exact-target closeness, approximation-target closeness,
  diagnostic-only, or blocked.

Promotion rule:

- promote exact-target closeness only if the 95% CI for mean value error and
  mean gradient-error summaries lie within the row's predeclared
  `promotion_tolerance`, max absolute errors are below the row
  `certification_band`, and veto diagnostics are clear;
- promote approximation-target closeness only if the comparison is explicitly
  against the approximation reference named in P0, the 95% CI for mean value
  error and mean gradient-error summaries lie within the row's predeclared
  approximation `promotion_tolerance`, max absolute errors are below the row
  approximation `certification_band`, and the result table labels the row as
  approximation-target evidence rather than exact-target evidence;
- for approximation-target gradient rows, the binding statistic is the
  predeclared row-level gradient criterion in this order: vector relative score
  error if available, otherwise blockwise absolute score error, otherwise
  directional derivative residuals; the chosen statistic must be declared in
  P0 before execution;
- downgrade to diagnostic-only if estimates are finite but CI or max-error
  criteria fail without implementation evidence;
- block if reference, scalar, gradient estimand, or evaluator variance is
  missing or unclassified;
- never change tolerance or certification bands after seeing P5 results without
  reviewed amendment and rerun.

Primary gradient object:

- default DPF promoted gradient: `fixed_branch_score`;
- stochastic-score evidence requires a separate reviewed amendment before
  execution;
- the differentiated scalar must be named per row and must match the value
  scalar up to a recorded sign convention.

Veto diagnostics:

- missing P0 row tolerance or certification band;
- seed variability not reported;
- stochastic and fixed-branch gradients mixed;
- branch decisions not recorded for fixed-branch gradients;
- same-target and approximation-target rows merged;
- particle ladder shows nonconvergence but row is promoted;
- value closeness used to promote gradient closeness.

Explanatory-only diagnostics:

- ESS, resampling count, Sinkhorn residual, runtime, finite AD/FD checks, and
  particle degeneracy summaries.

What will not be concluded:

- no DPF correctness beyond tested rows;
- no stochastic-resampling distribution correctness unless separately tested;
- no HMC readiness.

## Tasks

1. Import P1-P4 eligible rows.
2. Freeze observations, parameterization, seeds, and particle counts.
3. Run bootstrap-OT and LEDH-PFPF-OT separately.
4. Compute value and gradient error summaries.
5. Record row-level decisions and blocked rows.
6. Run Claude result review.

## Planned Commands And Artifacts

Runner status:
planned module; P5 `PRECHECK` must implement this runner, select an existing
runner by reviewed amendment, or write a blocker before any execution claim.

Planned command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf --validate-only
```

P5 must not execute until P1-P4 artifacts define the eligible row list and
reference route for every included target.

Required artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-claude-review-ledger-2026-06-08.md`

Claude result or blocker review follows the master max-five read-only loop.

## Exit Criteria

P5 exits with `PASS_P5_DPF_STATISTICAL_CLOSENESS_READY_FOR_P6` if every
eligible row is promoted, downgraded, or blocked with reviewed evidence.

## Stop Conditions

- DPF gradient target cannot be tied to the same scalar;
- evaluator variance is too large for the planned particle ladder and no
  amended ladder is reviewed;
- numerical failures are nonfinite or unclassified.
