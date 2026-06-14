# P1 Common Model Contracts Result

metadata_date: 2026-06-07
phase: P1 common model contracts
decision: PASS_P1_DENSITY_CONTRACTS_MATCHED

## Question

Do BayesFilter and executable float64 FilterFlow evaluate the same declared
density components for the common model suite?

## Comparator

- Shared model specs:
  `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
- BayesFilter highdim/common model adapters.
- Executable float64 FilterFlow subprocess adapters.
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_tieout_tf.py`

## Evidence Contract

Primary pass criterion:

- each common model density cell is `MATCHED` within tolerance for initial,
  transition, observation, and scalar density components where both surfaces
  expose those components.

Veto diagnostics:

- nonfinite density component;
- unclassified mismatch;
- spec checksum mismatch;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow import without `CUDA_VISIBLE_DEVICES=-1`;
- range-bearing local adapter mislabeled as upstream FilterFlow coverage.

Explanatory diagnostics:

- per-component deltas, model checksums, backend notes, and manifest fields.

Non-claims:

- density agreement is not full filter-path agreement;
- density agreement is not filtering correctness;
- no student-repository tie-out claim;
- range-bearing FilterFlow coverage uses a local subprocess adapter, not an
  upstream built-in model.

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
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf --validate-only
python -c "import json; d=json.load(open('experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json')); print(d.get('summary')); print([(c['model'], c['family'], c['status'], c['metrics']['max_abs_delta'], c['filterflow']['backend']) for c in d['cells']])"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_tieout_tf.py experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p1-common-model-contracts-subplan-2026-06-07.md
```

Environment:

- CPU/GPU status: CPU-only intent, `CUDA_VISIBLE_DEVICES=-1` set before
  TensorFlow runner import.
- TensorFlow emitted CUDA plugin registration and `cuInit` warnings despite
  hidden devices; the commands completed successfully and no GPU execution was
  requested.
- Random seeds: fixed by common model suite fixture where applicable.
- Dtype: float64.

Output artifact:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json`

## Result Summary

Decision from runner:

- `common_model_suite_density_all_matched`

Summary from refreshed JSON artifact:

- cells: `3`
- status counts: `{'MATCHED': 3}`
- max absolute density delta: `1.7763568394002505e-15`

Cell table:

| model | family | status | max abs delta | backend note |
|---|---|---:|---:|---|
| `lgssm_2d_linear` | `linear_gaussian` | `MATCHED` | `0.0` | `filterflow_builtin_linear_gaussian` |
| `sv_1d_synthetic` | `stochastic_volatility` | `MATCHED` | `1.1102230246251565e-16` | `filterflow_builtin_sv_plus_stationary_initial` |
| `range_bearing_2d_cv` | `range_bearing` | `MATCHED` | `1.7763568394002505e-15` | `filterflow_local_range_bearing_adapter` |

Explained mismatches:

- none.

Interface blockers:

- none in the P1 common density suite.

Out of scope:

- full filter paths;
- resampling behavior;
- gradients;
- student implementation comparisons.

Unclassified mismatches:

- none.

## Repair History

No P1 repair was required.

One explanatory tooling issue occurred:

- `jq` was unavailable in the shell, so Python standard-library JSON parsing
  was used to summarize the artifact.  This did not affect the runner or
  validation commands.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_P1_DENSITY_CONTRACTS_MATCHED | all three common density cells matched within tolerance | no P1 veto open | density agreement does not imply path or gradient agreement | run P2 deterministic value paths | no filter correctness, path, resampling, gradient, or student claim |

## Post-Run Red Team

Strongest alternative explanation:

- density components can match while proposal ordering, scalar accumulation,
  resampling, or gradient paths still differ.

Result that would overturn the decision:

- a refreshed artifact with any nonfinite component, checksum mismatch,
  unclassified density mismatch, or mislabeled range-bearing backend.

Weakest evidence link:

- P1 relies on a small common fixture suite.  It is enough for the stated
  density-contract question but not for broader algorithmic validation.
