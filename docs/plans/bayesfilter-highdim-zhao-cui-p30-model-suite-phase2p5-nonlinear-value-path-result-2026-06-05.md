# P37-M2.5 Result: Scalar Nonlinear Value Path

metadata_date: 2026-06-05
phase: P37-M2.5 scalar nonlinear fixed-branch value path

## Skeptical Plan Audit

Status: `PASS_TO_NARROWED_EXECUTION`.

M2 showed that the P30 synthetic stochastic-volatility equations and dense
references were available, but the BayesFilter value path still accepted only
`LinearGaussianSSM`.  The risk in M2.5 was jumping directly to a general
nonlinear TT/SIRT filter and producing a hard-to-audit implementation.

M2.5 therefore implemented only a scalar dense quadrature value path for
`TFHighDimStateSpaceModel` instances with `state_dim == 1`.  It requires
`fit_config is None` and `product_basis is None`, records the quadrature grid
and branch identity, and compares the SV result against the independent dense
reference from M2.

This avoids:

- treating finite dense-grid output as TT posterior accuracy;
- promoting a scalar bridge as high-dimensional scalability;
- silently using a finite integration window without a manifest;
- adding derivative, HMC, DSGE, GPU, SMC, or real-data claims.

## Evidence Contract

Question: can BayesFilter evaluate a scalar nonlinear fixed-branch filtering
value path for the P30 synthetic SV model and match an independent dense-grid
reference on tiny/bounded horizons?

Baseline/comparator:

- independent M2 sequential dense-grid SV reference;
- M2 tiny joint dense quadrature check;
- existing LGSSM and highdim guardrails.

Primary pass criteria:

- scalar SV log evidence agrees with the independent dense-grid reference;
- retained scalar mean and variance agree with the dense reference;
- branch replay is deterministic;
- TT-artifact requests are blocked under this dense value-only lane;
- public API guardrails remain green.

Veto diagnostics:

- nonfinite target, normalizer, mean, or variance;
- missing integration grid/window diagnostics;
- accepting TT/SIRT fitting requests as if supported;
- unsupported claim beyond scalar dense value path.

Explanatory-only diagnostics:

- wall time;
- quadrature order;
- integration window;
- branch hashes.

What will not be concluded:

- no TT posterior approximation accuracy;
- no Zhao--Cui `T=1000` reproduction;
- no high-dimensional state scalability;
- no derivative/HMC/DSGE readiness;
- no SMC/real-data evidence.

## Source-Governance Status

- P30 anchors identified: `eq:p27-sv1`--`eq:p27-sv10`.
- Synthetic transformed-coordinate anchor: `eq:p27-sv5a`.
- BayesFilter SV model/value-path anchors:
  `bayesfilter/highdim/models.py`, `bayesfilter/highdim/filtering.py`.
- BayesFilter tests:
  `tests/highdim/test_p30_stochastic_volatility.py`,
  `tests/highdim/test_p30_model_suite_contracts.py`.
- Traceability ledger updated: yes, SV synthetic row is now
  `BAYESFILTER_EXTENSION` for scalar dense value-path evidence only.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Files Changed

```text
bayesfilter/highdim/filtering.py
bayesfilter/highdim/__init__.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_model_suite_contracts.py
tests/highdim/test_p30_stochastic_volatility.py
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-subplan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-result-2026-06-05.md
```

## Implemented Behavior

New scalar dense value path:

```text
FixedBranchSquaredTTFilter.log_likelihood(model, theta, observations)
```

now dispatches non-LGSSM scalar `TFHighDimStateSpaceModel` instances to a
dense quadrature lane when:

```text
model.state_dim() == 1
fit_config is None
product_basis is None
```

The lane:

- uses `fit_quadrature_order` for Gauss-Legendre nodes on the reference line;
- maps reference nodes to physical nodes through the scalar coordinate map;
- evaluates initial, transition, and observation log densities from the model
  protocol;
- stores retained scalar grid density, mean, variance, and branch identity;
- records integration grid size and integration window;
- blocks TT-artifact fitting under this dense value-only path.

New/updated tests:

- `test_p30_sv_scalar_nonlinear_value_path_matches_dense_reference`
- `test_p30_sv_scalar_nonlinear_value_path_replay_is_deterministic`
- `test_p30_sv_scalar_nonlinear_value_path_blocks_tt_artifact_request`
- registry tests now mark synthetic SV as a scalar dense BayesFilter extension
  with TT/SIRT/paper-scale non-claims.
- after Claude code review, the dense-reference comparison checks every step's
  log normalizer, retained mean, and retained variance, not only the final
  retained marginal.

## Run Manifest

Initial focused run after implementation:

```text
2 collection errors
```

root cause:

```text
IndentationError in `_coordinate_map_for_dimension`.
```

fix:

```text
corrected indentation and reran compile before tests.
```

Second focused run:

```text
1 failed, 18 passed
```

root cause:

```text
SV registry test still expected the pre-M2.5 `BLOCKED_UNVALIDATED` status.
```

fix:

```text
updated test expectation to `BAYESFILTER_EXTENSION` with scalar dense value-path
non-claims.
```

Final focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py
```

result:

```text
19 passed, 2 warnings in 6.41s
```

Compile:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim/test_p30_stochastic_volatility.py
```

result:

```text
passed
```

Whitespace:

```bash
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py \
  bayesfilter/highdim/validation.py tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-subplan-2026-06-05.md
```

result:

```text
passed
```

Broad highdim guardrail:

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
130 passed, 2 warnings in 10.52s
```

Claude code review iteration 1 found two blockers:

```text
1. The SV dense-reference comparison checked total log evidence and final
   retained moments only, not every filtering step.
2. `_as_matrix` treated rank-1 scalar vectors as one row with many columns
   instead of a column grid.
```

Fixes:

```text
- added per-step log-normalizer, mean, and variance checks against the
  independent dense reference;
- changed `_as_matrix` so width-1 rank-1 tensors become `[-1,1]` column grids.
```

Post-fix focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py
```

post-fix result:

```text
19 passed, 2 warnings in 6.64s
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status: deliberate CPU-only test; `CUDA_VISIBLE_DEVICES=-1` set before
TensorFlow import.

dtype: `tf.float64`.

## Decision Table

| Field | Status |
|---|---|
| Primary criterion | `PASS_SCALAR_DENSE_VALUE_PATH` |
| Veto diagnostics | `PASS`; TT-artifact requests are blocked |
| Main uncertainty | scalar dense value path is not the Zhao--Cui TT/SIRT implementation |
| Next justified action | use this scalar nonlinear lane as a bridge for M3 references, then implement real TT/SIRT fitting separately |
| What is not concluded | no TT accuracy, `T=1000`, SMC, real-data, derivative, DSGE, HMC, GPU, or high-dimensional scalability claim |

## Decision

Decision: `PASS_TO_CLAUDE_REVIEW`.

M2.5 upgrades the SV lane from reference-only to a scalar dense BayesFilter
extension.  The paper-scale Zhao--Cui SV TT/SIRT benchmark remains future work.
