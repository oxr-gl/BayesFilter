# P3 Subplan: Conditional-Gaussian and Mixture-Oracle Rows

metadata_date: 2026-06-08
phase: P3
status: REVIEWED_READY_AFTER_P2_PASS

## Question

For transformed or finite-mixture targets that admit Kalman or Kalman-mixture
references, can DPF value and gradients be compared against exact references
for that declared approximation target?

## Evidence Contract

Baseline/comparator:

- exact transformed reference where available;
- finite-mixture Kalman reference for a declared KSC-style or similar mixture
  target;
- dense reference only when transformation or mixture exactness is not enough.

Primary criteria:

- target identity separates native SV, transformed SV, and mixture
  approximation rows;
- transformation Jacobian terms are recorded;
- exactness is claimed only for the transformed or mixture target, not for the
  native target unless proved;
- DPF comparisons report value and gradient errors plus stochastic evaluator
  variance.

Primary gradient object:

- exact comparator: `reference_score` for the declared transformed or mixture
  target;
- DPF candidate: `fixed_branch_score` unless a reviewed stochastic-score
  amendment is accepted before execution;
- scalar differentiated: the declared transformed or mixture log likelihood,
  with Jacobian/sign convention recorded per row.

Veto diagnostics:

- native and transformed likelihoods mixed in one metric;
- mixture approximation called native exact truth;
- Jacobian terms missing;
- state-dependent residual transform treated as observation-only without proof;
- gradient parameterization mismatch.

Explanatory-only diagnostics:

- mixture component count, approximation labels, finite status, and route
  runtime.

What will not be concluded:

- no native SV correctness from mixture-target agreement;
- no generalized-SV native equality unless separately proved;
- no HMC readiness.

## Tasks

1. Select simple transformed or mixture rows from P0.
2. Freeze target identity and Jacobian convention.
3. Build/reference Kalman or Kalman-mixture route.
4. Run DPF and deterministic approximation comparators.
5. Report exact-target and approximation-target claims separately.
6. Write artifacts and run Claude review.

## Planned Commands And Artifacts

Runner status:
planned module; P3 `PRECHECK` must implement this runner, select an existing
runner by reviewed amendment, or write a blocker before any execution claim.

Planned command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf --validate-only
```

If target separation blocks execution before a runner is implemented, P3 must
write a blocker result and send that blocker to Claude review.

Required artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p3_conditional_gaussian_mixture_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-claude-review-ledger-2026-06-08.md`

Claude result or blocker review follows the master max-five read-only loop.

## Exit Criteria

P3 exits with `PASS_P3_CONDITIONAL_GAUSSIAN_READY_FOR_P4` after at least one
reviewed exact transformed/mixture row or a blocker note that preserves target
separation.

## Stop Conditions

- reference route cannot be shown exact for the declared target;
- transformed and native targets cannot be separated in code artifacts;
- P42 gradient rules cannot be satisfied.
