# P37-M1 Result: Exact-Reference Linear Gaussian Model Tests

metadata_date: 2026-06-05
phase: P37-M1 exact-reference LGSSM tests

## Skeptical Plan Audit

Status: `PASS_TO_EXECUTION`.

M1 is an exact-reference value-path phase.  The main audit risks were:

- wrong baseline: using the BayesFilter value path as its own oracle;
- proxy promotion: treating runtime, rank, or ESS as accuracy evidence;
- overclaim: implying full Zhao--Cui `T=50`, `m=n=3`, rank/basis ladder
  reproduction from a small clean-room exact-reference grid;
- clean-room risk: copying MATLAB implementation structure rather than
  restating the P30 model in BayesFilter notation.

Resolution: M1 added a clean-room P30-shaped LGSSM fixture, an independent
covariance-form Kalman oracle inside the test file, and a small `(a,d)` grid
posterior comparison.  It did not implement the full Zhao--Cui grid, TT
approximation accuracy, derivative checks, or paper figure reproduction.

## Evidence Contract

Question: does the BayesFilter value path agree with exact Kalman evidence and
posterior summaries on a P30-shaped linear Gaussian benchmark?

Baseline/comparator:
- independent covariance-form Kalman recursion in
  `tests/highdim/test_p30_lgssm_exact_reference.py`;
- existing BayesFilter exact Kalman tests as regression guardrails.

Primary pass criteria:
- BayesFilter log evidence equals independent Kalman log evidence within
  `2e-12` on the clean-room P30-shaped fixture;
- retained filtering mean/covariance equal independent Kalman mean/covariance;
- small `(a,d)` parameter-grid posterior has zero Hellinger and relative `L1`
  discrepancy within tolerance;
- public API guardrail remains green.

Veto diagnostics:
- nonfinite posterior grid;
- exact-reference mismatch;
- missing oracle;
- lower-phase regression;
- any derivative/HMC/full-grid claim.

Explanatory-only diagnostics:
- runtime;
- rank/basis metadata in fixture manifest;
- test pass counts.

What will not be concluded:
- no full Zhao--Cui `T=50` reproduction grid;
- no paper figure reproduction;
- no TT approximation accuracy claim for the `(a,d)` posterior;
- no fixed-branch derivative claim;
- no HMC, DSGE, GPU-production, or stable public API claim.

## Source-Governance Status

- P30 anchors identified: `eq:p27-lg1`--`eq:p27-lg15`.
- Zhao--Cui paper anchors identified: linear Gaussian benchmark section and
  parameter posterior comparison.
- MATLAB behavioral anchors identified: `eg1_kalman/main_script.m`,
  `models/kalman/setup.m`, `models/kalman/theta_pdf.m`,
  `models/kalman/transition.m`, `models/kalman/like.m`.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/models.py`, `bayesfilter/highdim/filtering.py`,
  `tests/highdim/test_filtering_kalman_exact.py`,
  `tests/highdim/test_p30_lgssm_exact_reference.py`.
- Deviations listed: yes, M1 uses a deterministic clean-room observation
  matrix and short deterministic observation path rather than reproducing the
  full MATLAB-generated data path.
- Clean-room boundary respected: yes; MATLAB files were inspected only for
  high-level benchmark settings and behavioral anchors.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Files Changed

```text
tests/highdim/test_p30_lgssm_exact_reference.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-result-2026-06-05.md
```

M1 did not change production filtering code.

## Implemented Tests

New tests:

- `test_p30_lgssm_clean_room_fixture_matches_independent_kalman_reference`
- `test_p30_lgssm_parameter_grid_posterior_matches_kalman_oracle`
- `test_p30_lgssm_fixture_manifest_records_partial_grid_nonclaim`

The clean-room fixture uses:

```text
state dimension m = 3
observation dimension n = 3
horizon T = 3 or 4 in tests
parameter grid a in {0.50, 0.65, 0.80}
parameter grid d in {0.45, 0.60, 0.75}
transition scale b = sqrt(1-a^2)
initial state X_0 ~ N(0, I_3)
observation covariance d^2 I_3
```

The fixture manifest explicitly records:

```text
not the full Zhao--Cui T=50 reproduction grid
no fixed-branch derivative claim
no TT approximation accuracy claim
```

## Run Manifest

Focused new test:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_lgssm_exact_reference.py
```

result:

```text
3 passed, 2 warnings in 5.94s
```

M1 phase command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/test_v1_public_api.py
```

result:

```text
17 passed, 2 warnings in 3.71s
```

Broader CPU guardrail:

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
  tests/highdim/test_p30_lgssm_exact_reference.py
```

result:

```text
121 passed, 2 warnings in 7.25s
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status: deliberate CPU-only test; `CUDA_VISIBLE_DEVICES=-1` set
before TensorFlow import.

dtype: `tf.float64`.

random seeds: deterministic fixture strings and deterministic observation
path; no random data generation in M1 tests.

## Decision

Primary pass criterion status: `PASS`.

Veto diagnostics status:
- exact-reference log evidence passed;
- filtering moments passed;
- posterior-grid Hellinger and relative `L1` checks passed;
- public API guardrail passed;
- no derivative/HMC/full-grid claim was added.

Failure exit status:
- exact-reference mismatch would fail the test;
- fixture manifest records non-claims.

Decision: `PASS_TO_CLAUDE_REVIEW`.

