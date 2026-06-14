# DPF Common Filter-Path No-Resampling Plan

metadata_date: 2026-06-06

## Question

Can BayesFilter and executable float64 FilterFlow run the same deterministic
bootstrap particle-filter value path on the common LGSSM, stochastic-volatility,
and range-bearing model contracts when proposal randomness is fixed and
resampling is disabled?

## Evidence Contract

Primary engineering question:

- do the two implementations agree on the fixed-noise, no-resampling filtering
  recursion for the common model suite, after density-component agreement has
  already been established?

Primary comparator:

- no implementation is treated as an oracle.  The comparator is the declared
  common model spec plus fixed initial particles, fixed transition innovations,
  fixed observations, uniform initial weights, a bootstrap proposal, and an
  explicit no-resampling policy.

Primary pass criterion:

- every executable model cell must match within declared tolerances for
  predicted particles, transition log densities, observation log densities,
  unnormalized log weights, normalized log weights, incremental predictive log
  normalizers, cumulative scalar, ESS, filtered means, and filtered variances.

Veto diagnostics:

- nonfinite values in any executed cell;
- unclassified mismatch;
- any resampling event or nonzero resampling count;
- different fixed particles, innovations, observations, scalar objective, or
  dtype between the two sides;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow runs importing before `CUDA_VISIBLE_DEVICES=-1` or
  exposing GPUs.

Explanatory diagnostics:

- per-model and per-field maximum absolute deltas, model checksums, FilterFlow
  backend notes, step ledgers, and environment manifests.

What will not be concluded:

- no resampling correctness claim;
- no differentiable-resampling or gradient correctness claim;
- no implementation is promoted as scientifically correct;
- no student-repository tie-out claim;
- no TT-filter correctness claim;
- no paper-scale, GPU, HMC, DSGE, or production-readiness claim.

Planned artifacts:

- runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_noresampling_tf.py`;
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json`;
- report/result:
  `docs/plans/bayesfilter-dpf-common-filter-path-noresampling-result-2026-06-06.md`;
- report mirror:
  `experiments/dpf_implementation/reports/dpf-common-filter-path-noresampling-2026-06-06.md`.

## Skeptical Plan Audit

Audit status: `PASS_WITH_SCOPE_LIMIT`.

Wrong-baseline risk:

- the result will compare both implementations against a shared deterministic
  filtering contract, not against either implementation as truth.

Proxy-metric risk:

- agreement is a consistency check only.  It will not be used as evidence of
  algorithmic correctness, resampling correctness, gradient correctness, or
  scientific validity.

Fair-comparison risk:

- the range-bearing FilterFlow side remains a local subprocess adapter because
  upstream FilterFlow does not expose a built-in range-bearing observation
  model.  The result must label this as local adapter coverage.

Hidden-assumption risk:

- transition innovations are fixed arrays, not sampled random variables.  The
  test therefore checks replayed bootstrap-recursion semantics, not random
  number generator equivalence.

Gradient-risk:

- gradients are intentionally out of scope.  A later plan must fix the
  differentiable scalar, parameterization, and resampling branch semantics
  before comparing gradients.

Stop condition:

- stop after the three common models either match as fixed-noise no-resampling
  value paths or produce classified blockers/mismatches with preserved ledgers.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf --validate-only
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_common_filter_path_noresampling_tf.py
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json
git diff --check
```
