# P6 Subplan: Cross-Filter Error Calibration

metadata_date: 2026-06-08
phase: P6
status: REVIEWED_READY_AFTER_P5_PASS

## Question

How large are DPF, UKF, SVD/sigma-point, CUT4, and Zhao-Cui value and gradient
errors relative to reference error scales and data-law variability, without
turning approximation rows into exactness claims?

## Evidence Contract

Baseline/comparator:

- P1-P5 row-level value and gradient errors;
- reference-route refinement uncertainty;
- DPF evaluator variance;
- optional data-law variability only where P0/P5 declare a simulation design.

Primary criteria:

- produce separate ledgers for exact-target rows and approximation-target rows;
- compute normalized value and score errors;
- include reference uncertainty and evaluator variance in interpretation;
- classify filters by evidence class, not by a single ranking number.

Suggested summaries:

- total and per-observation value error;
- score vector relative error;
- directional derivative residuals;
- reference refinement residual;
- DPF within-dataset standard deviation;
- optional `rmse / sd_L` for simulation rows with declared data law.

Veto diagnostics:

- data-law variability used to excuse same-target numerical mismatch;
- approximation route ranked as if exact;
- reference uncertainty omitted;
- DPF evaluator variance omitted;
- row with failed gradient veto included in speed/ranking table as valid.

Explanatory-only diagnostics:

- runtime, memory, particle count, quadrature order, point count, and route
  availability.

What will not be concluded:

- no global filter ranking across incompatible targets;
- no default-policy change;
- no HMC readiness.

## Tasks

1. Load P1-P5 result artifacts.
2. Validate claim class per row.
3. Build exact-target and approximation-target calibration tables.
4. Separate blocked and diagnostic-only rows.
5. Write final calibration artifact and run Claude review.

## Planned Commands And Artifacts

Runner status:
planned module; P6 `PRECHECK` must implement this runner, select an existing
runner by reviewed amendment, or write a blocker before any execution claim.

Planned command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf --validate-only
```

If no promoted rows exist, P6 must write an empty-calibration blocker result
instead of fabricating metrics.

Required artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-claude-review-ledger-2026-06-08.md`

Claude result or blocker review follows the master max-five read-only loop.

## Exit Criteria

P6 exits with `PASS_P6_CROSS_FILTER_CALIBRATION_READY_FOR_P7` only if
calibration tables preserve claim classes and all veto diagnostics are clear.

## Stop Conditions

- no promoted rows exist and calibration would fabricate metrics;
- incompatible target rows cannot be separated;
- Claude or Codex identifies a ranking overclaim that cannot be repaired.
