# DPF Common Filter-Path No-Resampling Claude Review Ledger

metadata_date: 2026-06-06

## Scope

Artifacts submitted for external review:

- `docs/plans/bayesfilter-dpf-common-filter-path-noresampling-plan-2026-06-06.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_noresampling_tf.py`
- `docs/plans/bayesfilter-dpf-common-filter-path-noresampling-result-2026-06-06.md`
- `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json`

Review question:

- Does the runner honestly test fixed initial particles, fixed transition
  innovations, fixed observations, no resampling, the same bootstrap predictive
  log-normalizer scalar, and the same ledger fields between BayesFilter and
  FilterFlow?

## External Review Attempts

| attempt | command route | outcome | usable review? |
|---|---|---|---|
| 1 | `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name common-filter-path-review ...` | No output after several minutes; process no longer visible in `ps` afterward. | No |
| 2 | `timeout 180s bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name common-filter-path-review-brief ...` | Timed out with exit code `124` and no output. | No |
| 3 | `timeout 120s claude -p ...` | Exited with code `0` but returned only `(none)`. | No |

## Review Status

`CLAUDE_REVIEW_BLOCKED_NO_USABLE_OUTPUT`

The external Claude review did not converge to usable findings in this run.
This ledger should not be interpreted as Claude approval.  The no-resampling
tie-out result remains supported by local execution and validation only.

## Local Checks Already Completed

- Main runner:
  `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf`
- Validation:
  `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf --validate-only`
- Compile check:
  `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_noresampling_tf.py`
- JSON parse:
  `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json`
- Whitespace check:
  `git diff --check`

All local checks exited successfully.  TensorFlow printed CUDA factory/cuInit
messages during CPU-only imports, but the run manifest records
`pre_import_cuda_visible_devices=-1` and `gpu_devices_visible=[]`.

## Local Evidence Summary

- Decision: `common_filter_path_noresampling_all_matched`
- Matched cells: `3/3`
- Models:
  `lgssm_2d_linear`, `sv_1d_synthetic`, `range_bearing_2d_cv`
- Maximum absolute filter-path delta:
  `1.7763568394002505e-15`
- Scalar absolute deltas:
  `lgssm_2d_linear=0.0`,
  `sv_1d_synthetic=2.220446049250313e-16`,
  `range_bearing_2d_cv=0.0`

## Residual Review Need

Before promoting this beyond a local consistency result, rerun a usable
external review.  The key residual review questions are:

- whether transition-density ledger fields could mislead readers, since the
  bootstrap scalar intentionally uses observation likelihoods and previous
  weights but does not add transition log densities;
- whether fixed transition innovations should move from the runner into the
  shared common-model fixture before student-repository tie-outs;
- whether the range-bearing local FilterFlow adapter should be split out into a
  reusable adapter module before resampling and gradient tests.
