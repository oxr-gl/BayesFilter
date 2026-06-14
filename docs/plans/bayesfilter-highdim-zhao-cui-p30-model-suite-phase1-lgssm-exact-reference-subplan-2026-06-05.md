# P37-M1 Subplan: Exact-Reference Linear Gaussian Model Tests

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Turn the P30 linear Gaussian benchmark into executable exact-reference tests.
This is the central accuracy gate because Kalman filtering supplies a
non-Monte-Carlo comparator.

## Mathematical Model

P30 defines

```text
X_t - mu 1 = b (X_{t-1} - mu 1) + a eps_t^x,    eps_t^x ~ N(0, I_m)
Y_t        = C X_t + d eps_t^y,                  eps_t^y ~ N(0, I_n)
X_0 | mu   ~ N(mu 1, I_m)
theta      = (mu, a, b, d)
```

The Zhao--Cui numerical instance uses `m=n=3`, `T=50`, `mu=0`,
`a^2+b^2=1`, and effective estimated parameter
`theta_est=(a,d) in [0.4,1]^2`.

## Source-Governance Status

- P30 anchors: `eq:p27-lg1`--`eq:p27-lg15`.
- Paper anchor: linear Gaussian benchmark section, Kalman reference and
  parameter posterior comparison.
- MATLAB anchors: `eg1_kalman/main_script.m`, `eg1_kalman/computeHL2.m`,
  `eg1_kalman/computeL1.m`.
- BayesFilter current anchors:
  `bayesfilter/highdim/models.py`, `bayesfilter/highdim/filtering.py`,
  `tests/highdim/test_filtering_kalman_exact.py`,
  `tests/highdim/test_scaling_smoke.py`.

## Evidence Contract

Question: does the BayesFilter fixed-branch squared-TT value path agree with
exact Kalman evidence and posterior summaries on the P30 LGSSM ladder?

Decision table:

| Field | Contract |
|---|---|
| Baseline / comparator | exact Kalman log evidence, filtering means/covariances, and parameter-grid posterior for `(a,d)` |
| Primary criterion | declared rows meet log-evidence, moment, Hellinger, and relative `L1` tolerances |
| Veto diagnostics | convention mismatch, nonfinite posterior grid, exact Kalman mismatch, missing oracle, lower-phase regression |
| Explanatory only | runtime, memory, TT rank, basis size, fit residuals, ESS |

Primary pass criteria:

- exact Kalman log evidence agreement within declared tolerance;
- filtering mean/covariance agreement for small dense cases;
- parameter-posterior grid comparison for `(a,d)` reports Hellinger,
  relative `L1`, and evidence error;
- rank/basis ladder records failure classification when it cannot meet the
  tolerance;
- lower-level algebra and public API tests remain green.

Vetoes:

- wrong likelihood/evidence convention;
- mismatch between physical coordinates and reference coordinates;
- nonfinite evidence or posterior grid values;
- missing exact Kalman reference for a promoted row;
- using ESS, runtime, or residual alone as accuracy promotion evidence.

## Implementation Tasks

1. Extend exact LGSSM fixtures from tiny cases to the P30 parameter convention.
2. Implement an independent Kalman reference path for `log Z_{1:T}`,
   `m_t(theta)`, and `P_t(theta)`; reuse existing BayesFilter Kalman code only
   if the result ledger identifies it as the comparator and adds a second
   small hand-check fixture.
3. Add a parameter-grid posterior test for `(a,d)` on a small grid before the
   full Zhao--Cui grid.
4. Add optional larger rows approaching `m=n=3`, `T=50`, `ell in
   {17,25,33,41,49}`, `R in {10,15,20,25,30}`.
5. Record `D_H`, relative `L1`, evidence error, ESS if sampling is used,
   memory, wall time, and rank/basis settings.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/filtering.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_lgssm_exact_reference.py
docs/plans/*p37*phase1*result*.md
```

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_p30_lgssm_exact_reference.py

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py

git diff --check
```

## Exit Criteria

- exact-reference LGSSM tests pass at small and declared reproduction rows;
- result ledger states which Zhao--Cui grid rows are reproduced and which are
  pending;
- traceability ledger updates LGSSM row without overclaiming full model-suite
  reproduction;
- no derivative or HMC claim is made from this value-only phase.
