# DPF Common Fixed-Branch Gradient Plan

metadata_date: 2026-06-06

## Question

Can BayesFilter and executable float64 FilterFlow produce matching gradients
for the same fixed-noise, fixed-ancestor bootstrap particle-filter scalar on the
common model suite?

## Evidence Contract

Primary engineering question:

- after density, no-resampling value-path, and fixed-ancestor value-path
  agreement, do the two implementations agree on gradients of the same replayed
  scalar under explicit physical parameter knobs?

Primary comparator:

- no implementation is an oracle.  The comparator is the declared common model
  contract, fixed initial particles, fixed transition innovations, fixed
  observations, fixed resampling schedule, fixed ancestor map, and explicit
  physical gradient knobs.

Primary pass criterion:

- every executable gradient cell must match within declared tolerances for the
  scalar and gradient vector, and each implementation's autodiff gradient must
  agree with its own central finite-difference gradient within the finite-
  difference tolerance.

Gradient knobs:

- `lgssm_2d_linear`: scalar multiplier on the transition matrix `A`;
- `sv_1d_synthetic`: physical parameters `(gamma, beta)`;
- `range_bearing_2d_cv`: range observation noise scale `sigma_range`.

Veto diagnostics:

- nonfinite scalar or gradient;
- unclassified scalar or gradient mismatch;
- each side differentiating a different scalar, branch, ancestor map, or
  physical knob;
- central finite-difference self-check failure;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow runs importing before `CUDA_VISIBLE_DEVICES=-1` or
  exposing GPUs.

Explanatory diagnostics:

- scalar deltas, gradient deltas, finite-difference deltas, parameter values,
  model checksums, fixed-branch ledgers, and environment manifests.

What will not be concluded:

- no random-number-generator equality claim;
- no stochastic-resampler or differentiable-resampler correctness;
- no gradient through random/discrete ancestor selection;
- no implementation is promoted as scientifically correct;
- no student-repository tie-out claim;
- no TT-filter correctness claim;
- no paper-scale, GPU, HMC, DSGE, or production-readiness claim.

Planned artifacts:

- runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_fixed_branch_gradient_tf.py`;
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json`;
- report/result:
  `docs/plans/bayesfilter-dpf-common-fixed-branch-gradient-result-2026-06-06.md`;
- report mirror:
  `experiments/dpf_implementation/reports/dpf-common-fixed-branch-gradient-2026-06-06.md`.

## Skeptical Plan Audit

Audit status: `PASS_WITH_SCOPE_LIMIT`.

Wrong-baseline risk:

- the plan does not compare against either implementation as truth.  It
  compares both against a shared replayed scalar contract and includes finite-
  difference self-checks.

Proxy-metric risk:

- matching gradients are only consistency evidence for this fixed branch.  They
  are not filter correctness, resampling correctness, or scientific validation.

Fair-comparison risk:

- LGSSM and range-bearing common adapters have no native `theta`; explicit
  physical knobs are therefore introduced in the runner.  The result must state
  exactly which knobs were differentiated.

Hidden-assumption risk:

- ancestor indices are fixed and nondifferentiated.  This is a branch-gradient
  replay test, not a gradient through random resampling.

Stop condition:

- stop after the three common models either match on scalar and gradients with
  finite-difference self-checks or produce classified blockers/mismatches with
  preserved artifacts.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf --validate-only
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_common_fixed_branch_gradient_tf.py
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json
git diff --check
```
