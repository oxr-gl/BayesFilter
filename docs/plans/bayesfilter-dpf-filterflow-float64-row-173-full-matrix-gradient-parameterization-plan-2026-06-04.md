# Plan: Row 173 Full-Matrix Gradient Parameterization Probe

## Scope

This is a BayesFilter-owned experimental DPF difference audit. It tests whether
the row `173`, time `93` float64 FilterFlow/BayesFilter gradient mismatch is
caused by BayesFilter differentiating through a two-parameter diagonal vector
instead of FilterFlow's watched full transition-matrix variable.

Allowed write set:

- `experiments/dpf_implementation/tf_tfp/`
- `experiments/dpf_implementation/reports/`
- `docs/plans/`

Forbidden write set:

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow/`
- vendored/student code
- high-dimensional nonlinear filtering lane artifacts
- DSGE/NAWM-specific implementations or tests

## Evidence Contract

Question: Does a BayesFilter replay that watches the full `2x2` transition
matrix and compares `diag_part(d target / d A)` to FilterFlow eliminate the
row-173/time-93 gradient residual?

Comparator: the local executable float64 FilterFlow reference checkout, used
read-only through the existing row-173 VJP subprocess helper.

Primary criterion: compare the max absolute diagonal gradient delta between
FilterFlow and two BayesFilter replays:

1. current BayesFilter theta-vector parameterization;
2. BayesFilter full transition-matrix parameterization.

Promotion decision rule:

| Decision | Required condition |
| --- | --- |
| `blocked` | FilterFlow subprocess, BayesFilter replay, comparator fingerprint, JSON, or CPU-only execution fails. |
| `scalar_or_resampling_veto` | Scalars or resampling flags differ before gradient interpretation. |
| `full_matrix_parameterization_explains_delta` | Full-matrix BayesFilter diagonal gradient matches FilterFlow within `2e-4`, while theta-vector BayesFilter does not. |
| `parameterization_not_source` | Full-matrix BayesFilter still fails the `2e-4` diagonal-gradient gate and does not materially reduce the delta enough to identify parameterization as the source. |
| `partial_parameterization_effect_only` | Full-matrix materially reduces the delta but still fails the `2e-4` gate. |
| `both_parameterizations_match` | Both BayesFilter parameterizations match FilterFlow within `2e-4`. |

Diagnostics that can veto:

- non-finite scalar or gradient;
- scalar delta greater than `5e-8`;
- resampling flag mismatch;
- comparator fingerprint drift during the run;
- JSON validation failure;
- lane-boundary violation.

Diagnostics that are explanatory only:

- full `2x2` gradient matrix entries;
- off-diagonal full-matrix gradient entries;
- theta-vector versus full-matrix BayesFilter internal delta;
- value tensors for `post_update_log_likelihoods`,
  `pre_current_log_likelihoods`, and `increment`.

## Inputs

- Row index: `173`.
- Target time: `93`.
- Theta: `[0.9710526315789474, 0.9842105263157894]`.
- `T=100`, `N=50`, `batch_size=1`.
- Seeds: `DATA_SEED=123`, `FILTER_SEED=1234`.
- Annealed transport settings: `epsilon=0.25`, `scaling=0.85`,
  `convergence_threshold=1e-6`, `max_iter=500`,
  `resampling_neff=0.9999`.
- Dtype: `float64`.
- CPU-only: `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.

## Outputs

- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_full_matrix_gradient_parameterization_tf.py`
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-matrix-gradient-parameterization-result-2026-06-04.md`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-full-matrix-gradient-parameterization-2026-06-04.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_full_matrix_gradient_parameterization_2026-06-04.json`

## Skeptical Pre-Execution Audit

The plan answers only the parameterization question. It does not test global
smoothness-gradient agreement, mathematical correctness of either implementation,
or production readiness. It uses the same scalar, observations, particles,
seeds, dtype, transport settings, and local executable FilterFlow reference as
the row-173 probes. If values or resampling flags fail, gradient interpretation
must stop. If full-matrix BayesFilter still disagrees, the result should push
debugging back to post-update/resampling tape topology rather than claiming a
parameterization fix.

Audit status: passed. The planned artifacts are lane-scoped and directly answer
whether the FilterFlow full-matrix watched-variable method changes the
BayesFilter gradient comparison.

## Verification

- `python -m py_compile` for the touched runner.
- CPU-only runner execution.
- `--validate-only`.
- JSON parse check.
- NumPy import gate over the touched BayesFilter TF/TFP runner.
- Import-boundary search for student/highdim/DSGE/NAWM imports.
- Lane-scoped trailing-whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters .localsource/filterflow third_party`.

## Non-Conclusions

- No correctness claim is made for either implementation.
- No global smoothness-gradient agreement is concluded.
- No production readiness, public API readiness, posterior correctness, HMC
  readiness, DSGE/NAWM validation, banking/model-risk claim, or monograph claim
  is concluded.
- No permanent BayesFilter parameterization policy change is concluded.
