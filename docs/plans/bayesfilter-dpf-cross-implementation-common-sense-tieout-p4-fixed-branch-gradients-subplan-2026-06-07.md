# P4 Fixed-Branch Gradients Subplan

metadata_date: 2026-06-07
parent_program: `bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`

## Phase Question

Do BayesFilter and executable float64 FilterFlow produce matching gradients for
the same fixed-noise, fixed-ancestor bootstrap scalar under explicit physical
parameter knobs?

## Evidence Contract

Primary comparator:

- P3 fixed-ancestor replay contract;
- explicit physical gradient knobs:
  `transition_matrix_scale` for LGSSM, `(gamma,beta)` for SV, and
  `sigma_range` for range-bearing.

Primary pass criterion:

- every executable gradient cell matches within tolerance for scalar and
  gradient vector, and each implementation's autodiff gradient agrees with its
  own central finite-difference gradient within the finite-difference
  tolerance.

Veto diagnostics:

- nonfinite scalar or gradient;
- unclassified scalar or gradient mismatch;
- different scalar, branch, ancestor map, or physical knob;
- central finite-difference self-check failure;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow import without `CUDA_VISIBLE_DEVICES=-1`.

Explanatory diagnostics:

- scalar deltas, gradient deltas, finite-difference deltas, physical parameter
  values, and checksums.

Non-claims:

- no gradient through random or discrete ancestor selection;
- no stochastic-resampler or differentiable-resampler correctness;
- no student-repository tie-out claim.

## Current Artifact

- Plan:
  `docs/plans/bayesfilter-dpf-common-fixed-branch-gradient-plan-2026-06-06.md`
- Result:
  `docs/plans/bayesfilter-dpf-common-fixed-branch-gradient-result-2026-06-06.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_fixed_branch_gradient_tf.py`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json`

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf --validate-only
```

## Exit Gate

P4 exits when the common LGSSM, SV, and range-bearing fixed-branch gradients
match and pass finite-difference self-checks, or each non-matched gradient is
classified.
