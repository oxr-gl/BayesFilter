# P3 Fixed Resampling Branches Result

metadata_date: 2026-06-07
phase: P3 fixed resampling branches
decision: PASS_P3_FIXED_ANCESTOR_VALUE_PATHS_MATCHED

## Question

Do BayesFilter and executable float64 FilterFlow produce the same bootstrap
filter value path when a resampling branch is forced by a shared deterministic
ancestor map?

## Comparator

- P2 fixed-noise value-path contract.
- Fixed resampling schedule.
- Fixed ancestor map `[0, 0, 2]`.
- Weight reset to uniform at the resampling branch.
- Resampling before proposal, matching FilterFlow update ordering.
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_fixed_resampling_tf.py`

## Evidence Contract

Primary pass criterion:

- each executable model cell matches within tolerance for pre-resampling
  particles/weights, resampling flags, ancestor indices, post-resampling
  particles/weights, predicted particles, observation log densities,
  unnormalized and normalized log weights, predictive log-normalizer
  increments, cumulative scalar, ESS, filtered means, and filtered variances.

Veto diagnostics:

- resampling count other than the declared count;
- different ancestor map or branch timing;
- nonfinite ledger field;
- unclassified mismatch;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow import without `CUDA_VISIBLE_DEVICES=-1`.

Explanatory diagnostics:

- per-step deltas, resampling-count ledgers, backend notes, and checksums.

Non-claims:

- no random resampler distribution correctness;
- no random-number generator equality;
- no differentiable-resampling or gradient correctness;
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
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf --validate-only
python -c "import json; d=json.load(open('experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json')); print(d.get('decision')); print(d.get('summary')); print([(c['model'], c['family'], c['status'], c['metrics'].get('scalar_abs_delta'), c['metrics'].get('max_abs_delta'), c['metrics'].get('resampling_counts'), c['filterflow'].get('backend')) for c in d['cells']])"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_fixed_resampling_tf.py experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p3-fixed-resampling-subplan-2026-06-07.md
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

- `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json`

## Result Summary

Decision from runner:

- `common_filter_path_fixed_resampling_all_matched`

Summary from refreshed JSON artifact:

- cells: `3`
- status counts: `{'MATCHED': 3}`
- max absolute fixed-resampling path delta: `1.7763568394002505e-15`
- scalar absolute deltas:
  `{'lgssm_2d_linear': 0.0, 'range_bearing_2d_cv': 0.0, 'sv_1d_synthetic': 0.0}`
- resampling counts:
  `{'lgssm_2d_linear': {'bayesfilter': 1, 'filterflow': 1}, 'range_bearing_2d_cv': {'bayesfilter': 1, 'filterflow': 1}, 'sv_1d_synthetic': {'bayesfilter': 1, 'filterflow': 1}}`

Cell table:

| model | family | status | scalar delta | max path delta | resampling counts | backend note |
|---|---|---:|---:|---:|---|---|
| `lgssm_2d_linear` | `linear_gaussian` | `MATCHED` | `0.0` | `0.0` | `{'bayesfilter': 1, 'filterflow': 1}` | `filterflow_builtin_linear_gaussian_fixed_ancestor` |
| `sv_1d_synthetic` | `stochastic_volatility` | `MATCHED` | `0.0` | `8.881784197001252e-16` | `{'bayesfilter': 1, 'filterflow': 1}` | `filterflow_builtin_sv_fixed_ancestor` |
| `range_bearing_2d_cv` | `range_bearing` | `MATCHED` | `0.0` | `1.7763568394002505e-15` | `{'bayesfilter': 1, 'filterflow': 1}` | `filterflow_local_range_bearing_fixed_ancestor` |

Explained mismatches:

- none.

Interface blockers:

- none in the P3 common fixed-ancestor suite.

Out of scope:

- random resampler distribution correctness;
- random-number generator equality;
- differentiable resampling;
- gradients;
- student implementation comparisons.

Unclassified mismatches:

- none.

## Repair History

No P3 repair was required.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_P3_FIXED_ANCESTOR_VALUE_PATHS_MATCHED | all three fixed-ancestor path cells matched within tolerance and resampled once on both sides | no P3 veto open | fixed replay does not test random resampling distribution or gradients | run P4 fixed-branch gradients | no random resampler, differentiable resampling, gradient, student, or correctness claim |

## Post-Run Red Team

Strongest alternative explanation:

- fixed-ancestor replay can match while gradients through the fixed branch or
  parameter knobs still differ.

Result that would overturn the decision:

- a refreshed artifact with resampling count other than one per side, a
  different ancestor map or branch timing, nonfinite ledger field, unclassified
  mismatch, or delta outside tolerance.

Weakest evidence link:

- this is branch replay, not a stochastic resampler distribution test.
