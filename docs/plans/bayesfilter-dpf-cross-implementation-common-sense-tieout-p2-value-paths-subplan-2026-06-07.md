# P2 Deterministic Value Paths Subplan

metadata_date: 2026-06-07
parent_program: `bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`

## Phase Question

Do BayesFilter and executable float64 FilterFlow produce the same deterministic
fixed-noise bootstrap filter value path when resampling is disabled?

## Evidence Contract

Primary comparator:

- common model specs from P1;
- fixed initial particles;
- fixed transition innovations;
- fixed observations;
- uniform initial weights;
- bootstrap proposal;
- explicit no-resampling policy.

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

## Current Artifact

- Plan:
  `docs/plans/bayesfilter-dpf-common-filter-path-noresampling-plan-2026-06-06.md`
- Result:
  `docs/plans/bayesfilter-dpf-common-filter-path-noresampling-result-2026-06-06.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_noresampling_tf.py`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json`

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf --validate-only
```

## Exit Gate

P2 exits when the common LGSSM, SV, and range-bearing no-resampling value paths
are matched or each non-matched path is classified.
