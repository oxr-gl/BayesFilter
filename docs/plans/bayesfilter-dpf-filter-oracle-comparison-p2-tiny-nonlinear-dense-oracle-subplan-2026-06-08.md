# P2 Subplan: Tiny Nonlinear Dense-Oracle Rows

metadata_date: 2026-06-08
phase: P2
status: REVIEWED_READY_AFTER_P1_PASS

## Question

For tiny nonlinear targets where dense/refined quadrature is feasible, how do
DPF, UKF, SVD/sigma-point, and CUT4 compare in value and gradient against a
refined same-target reference?

## Evidence Contract

Baseline/comparator:

- dense/refined quadrature for the declared target;
- reference gradient from autodiff through fixed dense computation or
  P42 Tier-1 regression directional finite differences with step-stability
  checks.  Finite differences alone are not sufficient unless the P42 Tier-1
  reference-route stability and near-stationary safeguards are satisfied and
  recorded.

Primary criteria:

- at least one tiny nonlinear target has a reference refinement pass;
- DPF, UKF, SVD/sigma-point, and CUT4 are run only when P0 classifies them as
  same-target or approximation routes;
- value and gradient errors are reported separately;
- gradient reports include directional derivative checks and near-stationary
  guardrails from P42.

Primary gradient object:

- exact comparator: `reference_score` from dense/refined same-target reference;
- DPF candidate: `fixed_branch_score` unless a reviewed stochastic-score
  amendment is accepted before execution;
- scalar differentiated: the declared target log likelihood or negative log
  likelihood with sign convention recorded per row.

Candidate target families:

- scalar cubic observation additive-Gaussian closure;
- scalar or 2D quadratic observation closure;
- tiny nonlinear transition closure;
- short-horizon structural AR1 quadratic row if dense reference is feasible.

Veto diagnostics:

- dense reference lacks refinement evidence;
- quadrature dimension/horizon exceeds reviewed resource caps;
- CUT4 or UKF is called ground truth;
- finite differences are single-step only;
- gradient compared in a different parameterization.

Explanatory-only diagnostics:

- quadrature order, refinement residual, runtime, point count, conditioning, and
  route finite status.

What will not be concluded:

- no high-dimensional nonlinear correctness;
- no paper-scale reproduction;
- no default DPF promotion.

## Tasks

1. Select P0 eligible tiny nonlinear rows.
2. Define dense reference refinement ladder and resource caps.
3. Freeze parameterization and observations.
4. Run deterministic comparator routes and DPF routes.
5. Report value, gradient, and directional derivative errors.
6. Write result artifacts and run Claude review.

## Planned Commands And Artifacts

Runner status:
planned module; P2 `PRECHECK` must implement this runner, select an existing
runner by reviewed amendment, or write a blocker before any execution claim.

Planned command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf --validate-only
```

If dense-reference work is blocked before a runner is implemented, P2 must
write a blocker result and send that blocker to Claude review.

Required artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-claude-review-ledger-2026-06-08.md`

Claude result or blocker review follows the master max-five read-only loop.

## Exit Criteria

P2 exits with `PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_READY_FOR_P3` after at least
one promoted dense-oracle row or a reviewed blocker ledger explaining why no
row is feasible.

## Stop Conditions

- no same-target dense reference can pass refinement;
- DPF stochastic variance overwhelms the planned tolerance and no particle
  ladder amendment is reviewed;
- route target mismatch appears after execution.
