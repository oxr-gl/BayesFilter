# P37-M2 Result: Stochastic-Volatility Reference And Contract Tests

metadata_date: 2026-06-05
phase: P37-M2 stochastic-volatility tests

## Skeptical Plan Audit

Status: `PASS_TO_NARROWED_EXECUTION`.

The original M2 subplan includes long-horizon stochastic-volatility validation.
Before execution, the plan was narrowed because the current
`FixedBranchSquaredTTFilter` value path accepts `LinearGaussianSSM` only.  A
long SV run would therefore have used the wrong baseline or turned a reference
oracle into a false implementation claim.

Main audit risks:

- wrong baseline: treating a dense reference oracle as BayesFilter TT filtering;
- proxy promotion: treating finite likelihoods or short runtime as posterior
  accuracy;
- hidden convention: failing to record whether `x_0` is included;
- transformed-coordinate ambiguity: failing to distinguish `eq:p27-sv5a` from
  `eq:p27-sv5b`;
- stale context: registry saying `REFERENCE_ONLY` after model equations and
  tests exist;
- unsupported claim: implying Zhao--Cui `T=1000` reproduction, SMC agreement,
  or nonlinear fixed-branch filtering.

Resolution: M2 implemented the clean-room synthetic SV model equations,
declared the fixed-`sigma` transformed coordinates
`theta'=(Phi^{-1}(gamma), log beta)`, used the convention `x_0:x_T`, added
tiny dense references, added a bounded finite reference smoke row, and marked
the registry as `BLOCKED_UNVALIDATED` until a nonlinear fixed-branch value path
exists.

## Evidence Contract

Question: do the P30 synthetic stochastic-volatility equations, transformed
coordinates, and tiny reference oracles behave consistently enough to support a
future nonlinear fixed-branch filter implementation?

Baseline/comparator:

- direct P30 equations in `StochasticVolatilitySSM`;
- independent tiny joint dense quadrature over `x_0:x_T`;
- independent sequential dense-grid reference over the latent state.

Primary pass criteria:

- transformed parameters recover `(gamma,beta,sigma)=(0.6,0.4,1.0)`;
- model log densities match the scalar normal equations for initial,
  transition, and observation factors;
- tiny joint dense log evidence agrees with the sequential dense-grid
  reference within tolerance;
- bounded synthetic reference row has finite log evidence, finite filtering
  mean path, and positive variance path;
- manifest and registry record source anchors, dimension convention, and
  non-claims.

Veto diagnostics:

- invalid gamma or beta domain;
- missing `x_0:x_T` convention;
- nonfinite `exp(x/2)` likelihood values;
- treating dense reference or SMC as exact BayesFilter TT evidence;
- nonlinear SV filter run accepted without a real nonlinear value path.

Explanatory-only diagnostics:

- wall time of the bounded reference smoke row;
- reference grid order;
- finite path diagnostics.

What will not be concluded:

- no BayesFilter nonlinear fixed-branch filtering evidence for SV;
- no TT posterior approximation accuracy;
- no Zhao--Cui `T=1000` reproduction;
- no SMC/SMC2 reference evidence;
- no real-data S&P 500 claim;
- no high-dimensional scalability claim.

## Source-Governance Status

- P30 anchors identified: `eq:p27-sv1`--`eq:p27-sv10`.
- Synthetic transformed-coordinate anchor: `eq:p27-sv5a`.
- Zhao--Cui paper anchors identified: stochastic-volatility benchmark section.
- MATLAB behavioral anchors identified: `eg2_sv/mainscript.m`,
  `eg2_sv/mainscriptSP500.m`, `eg2_sv/SP500.txt`.
- BayesFilter SV model/test anchors identified:
  `bayesfilter/highdim/models.py`,
  `tests/highdim/test_p30_stochastic_volatility.py`.
- BayesFilter governance/registry anchors updated:
  `bayesfilter/highdim/validation.py`,
  `tests/highdim/test_p30_model_suite_contracts.py`.
- Deviations listed: yes.  M2 uses clean-room deterministic observations and
  dense references; it does not copy MATLAB code or reproduce the paper run.
- Clean-room boundary respected: yes.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Files Changed

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/__init__.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_model_suite_contracts.py
tests/highdim/test_p30_stochastic_volatility.py
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-result-2026-06-05.md
```

## Implemented Tests

New tests:

- `test_p30_sv_transform_and_log_densities_match_equations`
- `test_p30_sv_tiny_dense_joint_reference_matches_sequential_grid`
- `test_p30_sv_bounded_reference_smoke_records_finite_diagnostics`
- `test_p30_sv_fixture_manifest_states_transform_and_dimension_convention`
- `test_p30_sv_registry_marks_model_fixtures_as_blocked_until_filter_support`
- `test_p30_sv_filter_attempt_is_explicitly_blocked_until_nonlinear_value_path_exists`

The clean-room fixture uses:

```text
sigma = 1
gamma_true = 0.6
beta_true = 0.4
theta' = (Phi^{-1}(gamma), log beta)
X'_t = X_t
synthetic state convention = x_0:x_T
joint dimension convention = 2+(T+1)
tiny joint dense reference horizon = T=1
bounded sequential reference horizon = T=10
```

The first focused run found an oracle-accounting bug: the sequential dense
reference returned the final log-evidence increment rather than the cumulative
log evidence.  The reference was patched to return `sum_t log Z_t`, then the
focused and broad guardrails passed.  This is classified as a reference-oracle
implementation fix, not evidence against the SV equations.

## Run Manifest

Focused M2 command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py
```

first result:

```text
1 failed, 16 passed, 2 warnings in 9.99s
```

failure:

```text
test_p30_sv_tiny_dense_joint_reference_matches_sequential_grid
joint log evidence = 0.26513151737068763
sequential log evidence = 0.24320530050707312
```

root cause:

```text
sequential oracle returned the final normalizer increment instead of cumulative
log evidence.
```

focused M2 rerun:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py
```

result:

```text
17 passed, 2 warnings in 7.17s
```

Broader highdim guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/highdim/test_p30_stochastic_volatility.py
```

result:

```text
128 passed, 2 warnings in 11.03s
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status: deliberate CPU-only test; `CUDA_VISIBLE_DEVICES=-1` set before
TensorFlow import.

dtype: `tf.float64`.

random seeds: deterministic SV simulator seed `3702` in the bounded reference
smoke row.

## Decision Table

| Field | Status |
|---|---|
| Primary criterion | `PASS_REFERENCE_CONTRACTS` |
| Veto diagnostics | `PASS`, with nonlinear filter support intentionally blocked |
| Main uncertainty | dense references are tiny/bounded; no TT nonlinear filtering path exists yet |
| Next justified action | implement nonlinear fixed-branch adjacent target/value path for `TFHighDimStateSpaceModel` |
| What is not concluded | no SV TT posterior accuracy, no paper-scale reproduction, no high-dimensional scalability |

## Decision

Decision: `PASS_TO_CLAUDE_REVIEW_AS_REFERENCE_PHASE`.

M2 can support the next implementation phase by supplying source-matched SV
equations, transformed coordinates, and reference checks.  It cannot be used as
evidence that BayesFilter can already run the Zhao--Cui stochastic-volatility
TT filter.
