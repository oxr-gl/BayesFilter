# Filterflow Float64 Branch Reference Plan

## Goal

Create a dedicated local filterflow branch, `bayesfilter-py311-float64-reference`,
that uses float64 data and TensorFlow arithmetic for the BayesFilter/filterflow
DPF comparison lane.  Future BayesFilter-owned comparison runners should compare
against this branch, not the native float32 executable path, unless the task is
explicitly a paper/upstream float32 reproduction audit.

## Evidence Contract

- Question: can the local filterflow float64 branch run the Section-5.1-style
  LGSSM reference table natively and preserve the already-approved float64
  table-scale behavior?
- Comparator: the approved float64 probe artifact
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_reference_probe_2026-06-03.json`.
- Primary criterion: branch-native Kalman, PF, and RegularisedTransform rows
  execute with finite values, and per-time deltas versus the approved float64
  probe are within `1e-7`.  This is a branch-native regression check; the
  earlier float64 probe remains the table-scale approval against canonical
  float32 filterflow.
- Veto diagnostics: wrong branch checked out, missing branch marker file,
  non-finite likelihoods, dtype-mixing error, source mutation outside
  `.localsource/filterflow`, or protected BayesFilter paths changed.
- Explanatory diagnostics: filterflow branch, commit, diff summary, table rows,
  dtype ledger, and prior float64 probe decision.
- Not concluded: paper correctness, pristine upstream status, production
  readiness, posterior correctness, or gradient correctness.
- Artifacts: result note under `docs/plans/` and branch-native JSON under
  `experiments/dpf_implementation/reports/outputs/`.

## Allowed Write Set

- `.localsource/filterflow` on branch `bayesfilter-py311-float64-reference`.
- `docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-plan-2026-06-03.md`.
- `docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-result-2026-06-03.md`.
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_branch_reference_tf.py`.
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_branch_reference_2026-06-03.json`.
- Narrow updates to experimental filterflow comparison runners/docs so future
  comparisons target the float64 reference branch.

## Forbidden Write Set

- Production `bayesfilter/`.
- `tests/`.
- Monograph chapters under `docs/chapters/`.
- High-dimensional nonlinear filtering lane.
- Vendored student code.

## Skeptical Pre-Execution Audit

| Risk | Control |
| --- | --- |
| Treating float64 as pristine upstream | Branch marker and result note state it is local reference code only. |
| Losing canonical evidence | Prior float32/float64 probe remains the evidence that float64 preserves table scale. |
| Comparing against wrong branch | Branch verifier checks `bayesfilter-py311-float64-reference`. |
| Hidden production drift | Verification checks protected BayesFilter paths. |
| Float32 branch accidentally used again | Future comparison policy and runner constants are updated to require the float64 branch. |
| Overclaiming correctness | Result records only implementation-difference reference status. |

The plan passes the skeptical audit because it separates (1) policy, (2)
branch-native execution, and (3) prior table-scale evidence.

## Verification Commands

- `python -m py_compile` for touched BayesFilter runner and touched filterflow
  files.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_branch_reference_tf`.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_branch_reference_tf --validate-only`.
- JSON parse/schema check.
- Import-boundary check.
- NumPy import gate for touched BayesFilter TF/TFP runner, allowing only
  external filterflow subprocess/reporting fixture usage.
- Trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git -C .localsource/filterflow status --short --branch`.
- `git status --short --branch`.
