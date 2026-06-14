# DPF1 Reference Test Contract

## Status

DPF1 execution artifact.  This contract defines the first-rung correctness and
diagnostic tests required for a BayesFilter-owned classical PF baseline.

## Test Ladder

| Tier | Test | Baseline/reference | Primary criterion | Veto diagnostics | What remains explanatory |
| --- | --- | --- | --- | --- | --- |
| DPF1-T0 | Import-boundary check | No student imports from `bayesfilter` or `tests` | `rg` finds no student-baseline imports | Any production/test import from student baseline | N/A |
| DPF1-T1 | LGSSM one-step Kalman recovery | Analytic Kalman predictive/posterior/log-likelihood reference | Residuals within declared tolerance and finite uncertainty fields | Non-finite weights, missing seed/dtype/device, likelihood/log-likelihood confusion | Particle-count trends across few seeds |
| DPF1-T2 | Resampling semantics smoke | Closed artifact fields for resampling method, trigger, ESS, seed | Structured row records conditional-unbiasedness claim or caveat | Missing trigger or resampling status | ESS and resampling-count comparisons |
| DPF1-T3 | Nonlinear range-bearing smoke | Shared controlled range-bearing fixture | Finite rows with explicit proxy labels | Treating proxy RMSE as correctness | RMSE, ESS, runtime, same-regime student comparison |
| DPF1-T4 | Failure-row smoke | Artificial non-finite or impossible likelihood case | Structured failure with no silent normalization | Silent NaN/inf suppression or untracked zero mass | Failure localization text |

## LGSSM Reference Contract

The first implementation should reproduce the IE3 style of reference evidence:

- analytic predictive mean/variance;
- analytic posterior mean/variance;
- analytic one-step log likelihood;
- replicated PF summaries with uncertainty fields;
- explicit statement that fewer-error-at-larger-N is descriptive unless a
  multi-seed statistical criterion is planned.

## Likelihood Semantics Contract

| Object | Required label |
| --- | --- |
| `p_theta(y_1:T)` | True marginal likelihood under the model. |
| `hat_p_theta^N(y_1:T)` | Randomized PF likelihood estimator under classical assumptions. |
| `log hat_p_theta^N(y_1:T)` | Log of the estimator, not an unbiased log-likelihood estimator. |
| `grad` of a relaxed or learned scalar | DPF4 object only; not part of DPF1 acceptance. |

## Stop Rules

Stop DPF1 implementation movement if:

- the baseline cannot state which likelihood object it returns;
- the reference fixture lacks an independent analytic comparator;
- finite checks or seed/dtype/device fields are absent;
- a student row is used as correctness evidence;
- production API changes are required before DPF6.

## Non-Implications

This contract does not validate differentiable resampling, PF-PF, HMC, learned
OT, production API readiness, or model-risk use.
