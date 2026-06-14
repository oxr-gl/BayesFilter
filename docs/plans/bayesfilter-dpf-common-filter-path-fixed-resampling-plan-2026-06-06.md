# DPF Common Filter-Path Fixed-Resampling Plan

metadata_date: 2026-06-06

## Question

Can BayesFilter and executable float64 FilterFlow run the same bootstrap
particle-filter value path on the common model suite when a resampling branch is
forced by a shared deterministic ancestor map?

## Evidence Contract

Primary engineering question:

- after fixed-noise no-resampling agreement, do the two implementations still
  agree when the carried posterior state is resampled before a later proposal,
  with particles gathered by the same deterministic ancestor indices and
  weights reset to uniform?

Primary comparator:

- no implementation is an oracle.  The comparator is the declared common model
  spec, fixed initial particles, fixed transition innovations, fixed
  observations, uniform initial weights, a bootstrap proposal, and an explicit
  fixed resampling schedule plus ancestor map.

Primary pass criterion:

- every executable model cell must match within declared tolerances for
  pre-resampling particles/weights, resampling flags, ancestor indices,
  post-resampling particles/weights, predicted particles, observation
  log-density, unnormalized log weights, normalized log weights, incremental
  predictive log normalizers, cumulative scalar, ESS, filtered means, and
  filtered variances.

Veto diagnostics:

- nonfinite values in any executed cell;
- unclassified mismatch;
- different fixed particles, innovations, observations, ancestor maps,
  resampling schedule, scalar objective, or dtype between the two sides;
- resampling count other than the declared count;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow runs importing before `CUDA_VISIBLE_DEVICES=-1` or
  exposing GPUs.

Explanatory diagnostics:

- per-model and per-field maximum absolute deltas, model checksums, ancestor
  index ledgers, FilterFlow backend notes, and environment manifests.

What will not be concluded:

- no random-number-generator equality claim;
- no stochastic/systematic/multinomial resampler distributional correctness;
- no differentiable-resampling or gradient correctness claim;
- no implementation is promoted as scientifically correct;
- no student-repository tie-out claim;
- no TT-filter correctness claim;
- no paper-scale, GPU, HMC, DSGE, or production-readiness claim.

Planned artifacts:

- runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_fixed_resampling_tf.py`;
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json`;
- report/result:
  `docs/plans/bayesfilter-dpf-common-filter-path-fixed-resampling-result-2026-06-06.md`;
- report mirror:
  `experiments/dpf_implementation/reports/dpf-common-filter-path-fixed-resampling-2026-06-06.md`.

## Skeptical Plan Audit

Audit status: `PASS_WITH_SCOPE_LIMIT`.

Wrong-baseline risk:

- the plan does not treat BayesFilter or FilterFlow as truth.  Both execute the
  same replayed resampling contract.

Proxy-metric risk:

- exact value-path agreement under fixed ancestor replay is a consistency
  result only.  It is not a resampler correctness proof and is not scientific
  validation of the filter.

Fair-comparison risk:

- using a replayed ancestor map bypasses each implementation's random
  resampling draw.  That is acceptable for this rung because the question is
  branch semantics after resampling, not RNG or distributional equivalence.

Hidden-assumption risk:

- resampling occurs before proposal at the selected step, matching FilterFlow's
  SMC update ordering.  The result must state this explicitly.

Gradient-risk:

- gradients are out of scope.  The fixed ancestor map introduces a discrete
  branch and does not test differentiable resampling.

Stop condition:

- stop after the three common models either match on the fixed-resampling value
  path or produce classified blockers/mismatches with preserved ledgers.

## Fixed Resampling Contract

- Horizon: `3`
- Number of particles: inherited from each common model, currently `3`
- Schedule: no resampling before step `0`; resampling before step `1`;
  no resampling before step `2`
- Ancestor map at the resampling step: `[0, 0, 2]`
- Weight reset at the resampling step: uniform normalized log weights
- Scalar: sum of per-step predictive log normalizers after the proposal and
  observation update

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf --validate-only
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_fixed_resampling_tf.py
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json
git diff --check
```
