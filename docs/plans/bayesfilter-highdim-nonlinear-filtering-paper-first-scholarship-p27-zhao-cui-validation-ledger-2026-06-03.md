# P27 Zhao--Cui Large-Scale Validation Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Chopin and Papaspiliopoulos, "An Introduction to Sequential Monte Carlo,"
  2020.
- Gordon, Salmond, and Smith, "Novel Approach to Nonlinear/Non-Gaussian
  Bayesian State Estimation," 1993.
- Oseledets, "Tensor-Train Decomposition," 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.

what_is_not_concluded:
- No benchmark was run.
- No empirical success is claimed.
- No exact nonlinear posterior accuracy, adaptive global differentiability, or
  production readiness is claimed.

## Source Anchors Checked

| Source | Anchor | Use In P27 |
|---|---|---|
| Zhao--Cui JMLR 2024 | Section 6 opening | Defines the four numerical examples and comparison to SMC2 where applicable. |
| Zhao--Cui JMLR 2024 | Section 6.1, Eq. (36), Appendix B reference | Linear Gaussian/Kalman benchmark with exact parameter posterior evaluation. |
| Zhao--Cui JMLR 2024 | Section 6.2 and Example 1 | Stochastic-volatility synthetic and S&P500 validation examples. |
| Zhao--Cui JMLR 2024 | Section 6.3, Eq. (37) | Spatial SIR model with Austrian-state adjacency and 18-dimensional latent state. |
| Zhao--Cui JMLR 2024 | Section 6.4, Eq. (38) | Predator-prey model and linear/nonlinear preconditioning comparison. |
| Zhao--Cui JMLR 2024 | Figures 3--18 text | Metrics: relative \(L^1\), Hellinger distance, ESS, trajectory summaries, rank/basis ladders. |

## Validation Additions

| Need | P27 Section | Control Added |
|---|---|---|
| Large-scale test section | `Large-Scale Validation Models And Test Protocol` | Added validation ladder \(\mathcal V_0,\ldots,\mathcal V_5\). |
| Mathematical models | Linear Gaussian, stochastic volatility, SIR, predator-prey subsections | Added explicit state, observation, prior, dimension, and benchmark parameter equations. |
| Memory and performance | `What The Tests Must Measure` | Added target evaluation, core storage, derivative storage, solve size, mass/KR count, memory, and runtime decompositions. |
| Accuracy metrics | `Accuracy Metrics With Exact Or Reference Targets` | Added Hellinger, relative \(L^1\), moment error, RMSE, coverage, ESS quantile equations. |
| Robustness/failure | `Robustness Tests And Veto Conditions` | Added finite, normalization, condition, rank, KR, and derivative veto equations. |
| Fixed-branch derivative validation | Linear Gaussian subsection and benchmark table | Added fixed-branch finite-difference equations and derivative table template. |
| Benchmark limits | `What Each Benchmark Can And Cannot Establish` | Added explicit conditional conclusions for each model. |

## Reviewer-Risk Items

- The validation section is a specification, not a result.  A panel may still
  require actual benchmark numbers before endorsing the algorithm empirically.
- SMC2 comparison is source-supported by Zhao--Cui, but P27 does not specify a
  full independent SMC2 implementation contract.
- The BayesFilter stress ladder is a project-derived extension, not directly
  copied from Zhao--Cui.

