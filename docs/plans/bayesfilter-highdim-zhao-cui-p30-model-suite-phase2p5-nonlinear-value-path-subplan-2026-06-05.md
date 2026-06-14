# P37-M2.5 Subplan: Scalar Nonlinear Fixed-Branch Value Path

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

upstream_phase:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-result-2026-06-05.md`

## Purpose

Unblock the stochastic-volatility validation lane by adding the smallest honest
nonlinear value path: scalar state, fixed parameter, dense deterministic
quadrature, retained scalar grid filter, branch manifests, and comparison
against the M2 dense SV reference.

This is a value-only bridge from governed nonlinear model contracts to future
TT fitting.  It is not a full Zhao--Cui adaptive TT/KR implementation and it is
not a derivative phase.

## Skeptical Plan Audit

Status: `PASS_TO_NARROWED_EXECUTION`.

Risks checked:

- wrong baseline: comparing the new value path against itself instead of the
  independent M2 dense reference;
- proxy promotion: treating finite diagnostics as SV posterior accuracy;
- hidden approximation: using a finite integration window without recording it;
- stale context: leaving M2 marked blocked after adding a value path, or
  promoting it too far;
- environment mismatch: using GPU or long runs for a CPU reference phase;
- missing stop condition: letting dense grids become unbounded runtime;
- artifact mismatch: result docs that do not state the exact command and
  boundary.

Resolution:

- implement only scalar `TFHighDimStateSpaceModel` filtering;
- require `fit_config is None` and `product_basis is None` for this dense path;
- use declared `fit_quadrature_order` and the scalar coordinate map to define
  the integration grid/window;
- compare SV rows against the independent M2 sequential dense-grid reference;
- keep the traceability status `BLOCKED_UNVALIDATED` or a clearly partial
  status until TT approximation rows exist;
- stop before derivative, TT posterior accuracy, SMC, `T=1000`, or real-data
  claims.

## Evidence Contract

Question: can BayesFilter evaluate a scalar nonlinear fixed-branch filtering
value path for the P30 synthetic SV model and match an independent dense-grid
reference on tiny/bounded horizons?

Baseline/comparator:

- independent sequential dense-grid SV reference from M2 tests;
- M2 model-equation tests as guardrails;
- existing exact LGSSM and highdim guardrails.

Primary pass criteria:

- one-step and multi-step SV log evidence agree with the independent dense
  reference within declared tolerance;
- retained scalar mean and variance agree with the dense reference;
- branch replay is deterministic for identical config/model/theta/data;
- invalid non-scalar model use remains blocked;
- no public API or derivative claim is added.

Veto diagnostics:

- nonfinite log target, normalizer, retained mean, or retained variance;
- integration window or quadrature order not recorded;
- missing branch manifest;
- accepting multidimensional nonlinear models under this scalar path;
- claiming TT, KR, adaptive cross, HMC, DSGE, GPU, SMC, real-data, or
  paper-scale `T=1000` validation.

Explanatory only:

- wall time;
- quadrature order;
- integration radius/window;
- branch hash;
- finite diagnostic flags.

What will not be concluded:

- no TT posterior approximation accuracy;
- no Zhao--Cui `T=1000` reproduction;
- no high-dimensional state scalability;
- no derivative/HMC/DSGE readiness;
- no SMC/real-data evidence.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/filtering.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_stochastic_volatility.py
tests/highdim/test_p30_model_suite_contracts.py
docs/plans/*phase2p5*result*.md
docs/plans/*phase2p5*claude-review-ledger*.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

No top-level `bayesfilter` public API exports.

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py

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

python -m compileall -q bayesfilter/highdim tests/highdim/test_p30_stochastic_volatility.py
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/validation.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Exit Criteria

- scalar nonlinear SV value path passes tiny/bounded dense-reference tests;
- branch replay is deterministic;
- lower-phase and public API guardrails remain green;
- Claude code/governance review returns pass after at most five iterations;
- result ledger states exact scope and non-claims.
