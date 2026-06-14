# DPF Common Model Suite Implementation Plan

metadata_date: 2026-06-06

## Question

Can we implement a common set of small state-space model contracts that both
BayesFilter and executable float64 FilterFlow can run, so later value and
gradient matching is not limited to ad hoc one-off fixtures?

## Evidence Contract

Primary engineering question:

- do BayesFilter and FilterFlow evaluate the same declared density components
  for a shared LGSSM, stochastic-volatility, and nonlinear range-bearing
  model suite?

Primary comparator:

- no implementation is an oracle.  The comparator is the common declarative
  model spec plus two adapters: a BayesFilter highdim-protocol adapter and a
  FilterFlow subprocess adapter.

Primary pass criterion:

- all executable common-suite density cells match within declared tolerance for
  initial, transition, and observation components where both sides expose the
  component.

Veto diagnostics:

- nonfinite values in an executed density cell;
- unclassified mismatch;
- comparing different model equations or parameterizations;
- mutating `.localsource/filterflow`;
- treating density agreement as particle-filter correctness;
- CPU-only TensorFlow runs importing before `CUDA_VISIBLE_DEVICES=-1`.

Explanatory diagnostics:

- per-component deltas, model checksums, adapter status, FilterFlow branch
  fingerprint, and existing student/model-suite interface notes.

What will not be concluded:

- no filtering-algorithm correctness;
- no end-to-end DPF value or gradient equality for every model;
- no TT correctness;
- no paper-scale reproduction;
- no HMC, DSGE, GPU, or production-readiness claim.

Planned artifacts:

- common model module:
  `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`;
- common-suite runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_tieout_tf.py`;
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json`;
- report/result:
  `docs/plans/bayesfilter-dpf-common-model-suite-implementation-result-2026-06-06.md`.

## Skeptical Plan Audit

Audit status: `PASS_WITH_SCOPE_LIMIT`.

Wrong-baseline risk:

- the plan does not compare against BayesFilter or FilterFlow as truth.  The
  shared spec is a contract, and both adapters are audited against that
  contract.

Proxy-metric risk:

- the first implementation compares density components only.  It does not
  promote RMSE, ESS, table cells, TT evidence, or student outputs into a
  correctness criterion.

Fair-comparison risk:

- range-bearing is supported by a custom FilterFlow adapter in the subprocess,
  because upstream FilterFlow has no built-in range-bearing model.  This is
  acceptable for common-model execution, but the result must label it as a
  local adapter rather than upstream FilterFlow model coverage.

Gradient-risk:

- this implementation stops at density values.  Gradients and full filter path
  equality require a separate plan that fixes proposal, resampling, random
  numbers, and scalar objective per model.

Stop condition:

- stop after LGSSM, SV, and range-bearing density tie-outs are implemented and
  validated.  Any unclassified executed mismatch vetoes the result.

## Initial Common Models

| Model | Shared contract | FilterFlow adapter | BayesFilter adapter |
|---|---|---|---|
| `lgssm_2d_linear` | affine-free linear Gaussian transition and observation | built-in random-walk transition plus linear observation | highdim `LinearGaussianSSM` |
| `sv_1d_synthetic` | `x_t = gamma x_{t-1} + sigma eta_t`, `y_t ~ Normal(0,beta exp(x_t/2))` | built-in SV transition/observation | highdim `StochasticVolatilitySSM` |
| `range_bearing_2d_cv` | constant-velocity linear Gaussian transition and range-bearing observation | local FilterFlow transition/observation adapter in subprocess | common highdim-protocol adapter |

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf --validate-only
python -m py_compile experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_tieout_tf.py
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json
git diff --check
```
