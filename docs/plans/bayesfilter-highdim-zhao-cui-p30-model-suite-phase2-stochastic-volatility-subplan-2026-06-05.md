# P37-M2 Subplan: Long-Horizon Stochastic-Volatility Tests

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Implement the P30 stochastic-volatility benchmark as a staged nonlinear
long-horizon validation lane.  This phase tests time-horizon stability, not
high-dimensional state scalability.

## Mathematical Model

Synthetic benchmark:

```text
X_t = gamma X_{t-1} + sigma eps_t^x,       eps_t^x ~ N(0,1)
Y_t = beta exp(X_t/2) eps_t^y,             eps_t^y ~ N(0,1)
X_0 | gamma,sigma ~ N(0, sigma^2/(1-gamma^2))
```

Zhao--Cui synthetic setting:

```text
sigma = 1
theta = (gamma, beta)
T = 1000
truth = (gamma, beta) = (0.6, 0.4)
transformed coordinates = (Phi^{-1}(gamma), log beta), X_t' = X_t
rank ladder R in {5,10,20}, ell = 33, ALS sweeps = 5
```

The result must state whether the latent dimension convention is
`2+(T+1)` including `x_0`, or `2+T` with `x_0` absorbed into the initial
density.

## Source-Governance Status

- P30 anchors: `eq:p27-sv1`--`eq:p27-sv10`.
- Paper anchor: stochastic-volatility benchmark and S&P 500 example.
- MATLAB anchors: `eg2_sv/mainscript.m`, `eg2_sv/mainscriptSP500.m`,
  `eg2_sv/SP500.txt`.
- BayesFilter current anchors: none for highdim Zhao--Cui SV; this starts as
  `REFERENCE_ONLY`.

## Evidence Contract

Question: can the fixed-branch highdim filter run a nonlinear long-horizon SV
benchmark with stable diagnostics and meaningful accuracy checks against small
references, synthetic truth, or independent SMC?

Decision table:

| Field | Contract |
|---|---|
| Baseline / comparator | tiny dense quadrature where feasible; synthetic truth; optional independent SMC with MC uncertainty |
| Primary criterion | tiny reference rows pass, then bounded long-horizon rows report finite path, parameter, ESS, and resource diagnostics |
| Veto diagnostics | invalid transform/domain, overflow, SMC treated as exact, missing MCSE, nonfinite likelihood, rank or conditioning failure |
| Explanatory only | posterior plots, raw SMC agreement without uncertainty, wall time, rank trends, ESS trends |

Primary pass criteria:

- tiny-horizon SV rows agree with dense quadrature or a separately validated
  reference;
- synthetic rows record posterior concentration around the truth, path RMSE,
  coverage, ESS quantiles, memory, and time;
- long-horizon rows are promoted only after tiny references and finite
  diagnostics pass;
- real-data rows, if any, are labeled stability/reasonableness only.

Vetoes:

- missing transformed-coordinate convention;
- unstable `gamma` domain handling or invalid stationary variance;
- treating SMC as exact without Monte Carlo uncertainty;
- nonfinite likelihood from `exp(X_t/2)` overflow;
- rank saturation or conditioning failure without classification;
- claiming high-dimensional scalability from this one-dimensional latent
  process.

## Fairness And Evidence Boundary

Fair comparison controls:

- all methods in a comparison use the same generated observations, latent
  truth, priors, parameter transform, horizon, dtype, and seed ledger;
- SMC comparisons record particle count, resampling rule, proposal family,
  random seeds, wall-time accounting policy, and MCSE or replicate
  uncertainty;
- if wall-clock budgets differ, the row is labeled an explanatory comparison,
  not a promotion comparison.

BayesFilter-native evidence required for promotion:

- tiny dense-reference row, or independently audited reference with
  uncertainty;
- synthetic-truth row with parameter concentration, path RMSE, coverage, and
  finite diagnostics;
- resource manifest with memory/time and failure classification.

MATLAB agreement can confirm benchmark setup and qualitative behavior.  It
cannot by itself prove BayesFilter correctness or posterior accuracy.

## Stop Conditions And Pre-Mortem

Stop before long `T` if tiny dense rows fail, transformed coordinates are
ambiguous, likelihoods overflow, or conditioning/rank vetoes fire.

Misleading-pass risks:

- high ESS despite biased fitted target;
- synthetic truth near prior center hiding approximation error;
- SMC comparator too noisy to detect discrepancy;
- long-horizon run promoted because it is finite rather than accurate.

Failure interpretation must separate implementation bug, tuning/resource
failure, reference uncertainty, and evidence against the method.

## Implementation Tasks

1. Implement SV data simulator with fixed seed and manifest.
2. Implement tiny dense reference rows for `T in {1,2,3}` and small parameter
   grids.
3. Add long-horizon smoke rows for `T in {10,50,100}` before attempting
   `T=1000`.
4. Add optional independent SMC comparator only under a separate evidence
   contract that records particle count, seeds, MCSE, and failure modes.
5. Add paper-scale synthetic row with `R in {5,10,20}`, `ell=33`, and
   `S_ALS=5` only after smaller rows pass.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_stochastic_volatility.py
docs/plans/*p37*phase2*result*.md
```

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_stochastic_volatility.py

git diff --check
```

Long `T=1000` or GPU rows require a separate experiment plan and trusted GPU
commands if GPU is used.

## Exit Criteria

- tiny reference rows pass;
- at least one bounded long-horizon synthetic row passes with finite metrics;
- result ledger states whether the paper-scale `T=1000` row was run or remains
  pending;
- no high-dimensional scalability or exact nonlinear posterior claim is made.
