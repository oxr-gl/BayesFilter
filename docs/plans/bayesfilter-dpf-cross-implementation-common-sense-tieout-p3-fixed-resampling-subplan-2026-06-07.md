# P3 Fixed Resampling Branches Subplan

metadata_date: 2026-06-07
parent_program: `bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`

## Phase Question

Do BayesFilter and executable float64 FilterFlow produce the same bootstrap
filter value path when a resampling branch is forced by a shared deterministic
ancestor map?

## Evidence Contract

Primary comparator:

- P2 fixed-noise value-path contract;
- fixed resampling schedule;
- fixed ancestor map `[0, 0, 2]`;
- weight reset to uniform at the resampling branch;
- resampling before proposal, matching FilterFlow update ordering.

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

## Current Artifact

- Plan:
  `docs/plans/bayesfilter-dpf-common-filter-path-fixed-resampling-plan-2026-06-06.md`
- Result:
  `docs/plans/bayesfilter-dpf-common-filter-path-fixed-resampling-result-2026-06-06.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_fixed_resampling_tf.py`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json`

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf --validate-only
```

## Exit Gate

P3 exits when the common LGSSM, SV, and range-bearing fixed-ancestor value paths
are matched or each non-matched path is classified.
