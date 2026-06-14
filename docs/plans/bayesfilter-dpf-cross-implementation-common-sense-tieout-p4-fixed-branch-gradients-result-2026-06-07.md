# P4 Fixed-Branch Gradients Result

metadata_date: 2026-06-07
phase: P4 fixed-branch gradients
decision: PASS_P4_FIXED_BRANCH_GRADIENTS_MATCHED

## Question

Do BayesFilter and executable float64 FilterFlow produce matching gradients for
the same fixed-noise, fixed-ancestor bootstrap scalar under explicit physical
parameter knobs?

## Comparator

- P3 fixed-ancestor replay contract.
- Explicit physical gradient knobs:
  `transition_matrix_scale` for LGSSM, `(gamma,beta)` for stochastic
  volatility, and `sigma_range` for range-bearing.
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_fixed_branch_gradient_tf.py`

## Evidence Contract

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

## Command Manifest

Git commit:

```text
7ccb9c39883471c2d5ec2891cbf33b9ed436bada
```

Dirty-worktree status:

- dirty worktree with many existing modified and untracked DPF/highdim
  artifacts; unrelated changes were preserved.

Commands:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf --validate-only
python -c "import json; d=json.load(open('experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json')); print(d.get('decision')); print(d.get('summary'))"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_common_fixed_branch_gradient_tf.py experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p4-fixed-branch-gradients-subplan-2026-06-07.md
```

Environment:

- CPU/GPU status: CPU-only intent, `CUDA_VISIBLE_DEVICES=-1` set before
  TensorFlow runner import.
- JSON run manifest records `cpu_only: True`,
  `pre_import_cuda_visible_devices: -1`, and `gpu_devices_visible: []`.
- TensorFlow emitted CUDA plugin registration and `cuInit` warnings despite
  hidden devices; the commands completed successfully and no GPU execution was
  requested.
- Dtype: float64.

Output artifact:

- `experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json`

## Result Summary

Decision from runner:

- `common_fixed_branch_gradient_all_matched`

Summary from refreshed JSON artifact:

- cells: `3`
- status counts: `{'MATCHED': 3}`
- max scalar delta: `0.0`
- max gradient delta: `0.0`
- max BayesFilter AD-vs-FD delta: `1.0343861767125873e-07`
- max FilterFlow AD-vs-FD delta: `1.0343861767125873e-07`

Cell table:

| model | status | knobs | scalar delta | max gradient delta | BF FD delta | FF FD delta |
|---|---:|---|---:|---:|---:|---:|
| `lgssm_2d_linear` | `MATCHED` | `transition_matrix_scale` | `0.0` | `0.0` | `8.091749492677991e-12` | `8.091749492677991e-12` |
| `sv_1d_synthetic` | `MATCHED` | `gamma,beta` | `0.0` | `0.0` | `1.9265300466031476e-10` | `1.7599965929093742e-10` |
| `range_bearing_2d_cv` | `MATCHED` | `sigma_range` | `0.0` | `0.0` | `1.0343861767125873e-07` | `1.0343861767125873e-07` |

Explained mismatches:

- none.

Interface blockers:

- none in the P4 common fixed-branch gradient suite.

Out of scope:

- gradients through random or discrete ancestor selection;
- stochastic-resampler or differentiable-resampler correctness;
- student implementation comparisons.

Unclassified mismatches:

- none.

## Repair History

No P4 repair was required.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_P4_FIXED_BRANCH_GRADIENTS_MATCHED | all fixed-branch scalar and gradient cells matched and each side passed finite-difference self-check | no P4 veto open | fixed-branch gradients do not cover gradients through random/discrete ancestor selection | run P5 remaining BayesFilter/FilterFlow coverage classification | no stochastic-resampler, differentiable-resampler, student, or correctness claim |

## Post-Run Red Team

Strongest alternative explanation:

- fixed-branch gradient agreement can hold while models or filter surfaces
  outside the common suite remain uncovered or interface-blocked.

Result that would overturn the decision:

- a refreshed artifact with nonfinite scalar/gradient, scalar or gradient delta
  outside tolerance, finite-difference self-check failure, or mismatched branch
  or physical knob.

Weakest evidence link:

- this phase checks fixed-branch gradients only.  It deliberately avoids
  gradients through random or discrete resampling decisions.
