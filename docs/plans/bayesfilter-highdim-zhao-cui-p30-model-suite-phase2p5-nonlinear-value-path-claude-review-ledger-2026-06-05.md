# P37-M2.5 Claude Review Ledger

metadata_date: 2026-06-05
phase: P37-M2.5 scalar nonlinear value path

review_scope:
- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/validation.py`
- `tests/highdim/test_p30_model_suite_contracts.py`
- `tests/highdim/test_p30_stochastic_volatility.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-subplan-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-result-2026-06-05.md`

## Iterations

### Code Gate Iteration 1

worker: `highdim-p37-m2p5-code-review-iter1`

status: `BLOCKED_M2P5_CODE`

raw_response:

```text
BLOCKED_M2P5_CODE
1. The SV “dense-reference comparison” test does not actually verify the full scalar nonlinear value path it claims to cover. `tests/highdim/test_p30_stochastic_volatility.py:336` checks total log evidence plus only the final retained mean/variance, so a bug in intermediate filtering steps could still pass while `result.diagnostics["value_path"]` claims the dense quadrature path. Minimal fix: compare each `result.steps[t].log_normalizer` against the sequential reference increments and each step’s retained mean/variance against `reference["mean_path"][t]` / `reference["variance_path"][t]`.

2. The scalar dense path shape helper is brittle for natural 1D inputs. `bayesfilter/highdim/filtering.py:1139` converts rank-1 tensors to shape `[1, n]`, not `[n, 1]`, so scalar point vectors are misinterpreted as one row with `n` columns. Current tests avoid this by always passing explicit column matrices, but the path is supposed to be scalar/dense and this helper sits on that boundary. Minimal fix: in `_as_matrix`, when `width == 1` and rank is 1, reshape to `[-1, 1]` instead of `[1, :]`, or add a scalar-specific helper and use it for the 1D dense-grid path.
```

fixes:
- Added per-step log-normalizer, retained mean, and retained variance checks
  against the independent sequential dense-grid reference.
- Changed `_as_matrix` so width-1 rank-1 tensors are interpreted as scalar
  column grids.

### Code Gate Iteration 2

worker: `highdim-p37-m2p5-code-review-iter2`

status: `PASS_M2P5_CODE`

raw_response:

```text
PASS_M2P5_CODE
```

### Governance Gate Iteration 1

worker: `highdim-p37-m2p5-governance-review-iter1`

status: `PASS_M2P5_GOVERNANCE`

raw_response:

```text
PASS_M2P5_GOVERNANCE
```

## Final Status

`PASS_M2P5`

open_findings:
- none for M2.5 as a scalar dense value-path phase.

remaining_boundaries:
- no TT/SIRT posterior approximation claim;
- no Zhao--Cui `T=1000` reproduction;
- no high-dimensional scalability claim;
- no derivative, HMC, DSGE, GPU, SMC, or real-data claim.
