# P2 Deterministic Value Paths Result

metadata_date: 2026-06-07
phase: P2 deterministic value paths
decision: PASS_P2_NORESAMPLING_VALUE_PATHS_MATCHED

## Question

Do BayesFilter and executable float64 FilterFlow produce the same deterministic
fixed-noise bootstrap filter value path when resampling is disabled?

## Comparator

- Common model specs from P1.
- Fixed initial particles, fixed transition innovations, fixed observations,
  uniform initial weights, bootstrap proposal, and explicit no-resampling
  policy.
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_noresampling_tf.py`

## Evidence Contract

Primary pass criterion:

- each executable model cell matches within tolerance for predicted particles,
  transition log densities, observation log densities, unnormalized and
  normalized log weights, predictive log-normalizer increments, cumulative
  scalar, ESS, filtered means, and filtered variances.

Veto diagnostics:

- any resampling event;
- nonfinite ledger field;
- unclassified mismatch;
- different fixed particles, innovations, observations, scalar objective, or
  dtype;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow import without `CUDA_VISIBLE_DEVICES=-1`.

Explanatory diagnostics:

- per-step ledger deltas, scalar deltas, backend notes, and checksums.

Non-claims:

- no resampling correctness claim;
- no gradient correctness claim;
- no random-number generator equivalence;
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
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf --validate-only
python -c "import json; d=json.load(open('experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json')); print(d.get('decision')); print(d.get('summary')); print([(c['model'], c['family'], c['status'], c['metrics'].get('scalar_abs_delta'), c['metrics'].get('max_abs_delta'), c['filterflow'].get('backend')) for c in d['cells']])"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_noresampling_tf.py experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p2-value-paths-subplan-2026-06-07.md
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

- `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json`

## Result Summary

Decision from runner:

- `common_filter_path_noresampling_all_matched`

Summary from refreshed JSON artifact:

- cells: `3`
- status counts: `{'MATCHED': 3}`
- max absolute filter-path delta: `1.7763568394002505e-15`
- scalar absolute deltas:
  `{'lgssm_2d_linear': 0.0, 'range_bearing_2d_cv': 0.0, 'sv_1d_synthetic': 2.220446049250313e-16}`

Cell table:

| model | family | status | scalar delta | max path delta | backend note |
|---|---|---:|---:|---:|---|
| `lgssm_2d_linear` | `linear_gaussian` | `MATCHED` | `0.0` | `0.0` | `filterflow_builtin_linear_gaussian_noresampling` |
| `sv_1d_synthetic` | `stochastic_volatility` | `MATCHED` | `2.220446049250313e-16` | `1.3322676295501878e-15` | `filterflow_builtin_sv_noresampling` |
| `range_bearing_2d_cv` | `range_bearing` | `MATCHED` | `0.0` | `1.7763568394002505e-15` | `filterflow_local_range_bearing_noresampling` |

Explained mismatches:

- none.

Interface blockers:

- none in the P2 common no-resampling suite.

Out of scope:

- resampling correctness;
- pathwise gradients;
- random-number generator equivalence;
- student implementation comparisons.

Unclassified mismatches:

- none.

## Repair History

No P2 repair was required.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_P2_NORESAMPLING_VALUE_PATHS_MATCHED | all three deterministic no-resampling path cells matched within tolerance | no P2 veto open | no-resampling agreement does not test ancestor replay or gradients | run P3 fixed resampling branches | no resampling, gradient, RNG, student, or correctness claim |

## Post-Run Red Team

Strongest alternative explanation:

- no-resampling paths can match while fixed-ancestor branch ordering or
  gradient routing still differs.

Result that would overturn the decision:

- a refreshed artifact with a resampling event, nonfinite ledger field,
  unclassified mismatch, scalar/path delta outside tolerance, or manifest
  mismatch.

Weakest evidence link:

- the phase is deterministic and deliberately small.  It answers the common
  value-path contract question but not stochastic resampler behavior.
