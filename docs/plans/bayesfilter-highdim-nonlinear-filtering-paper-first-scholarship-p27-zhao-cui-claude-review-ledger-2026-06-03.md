# P27 Zhao--Cui Large-Scale Validation Claude Review Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- Chopin and Papaspiliopoulos, "An Introduction to Sequential Monte Carlo,"
  2020.
- Gordon, Salmond, and Smith, "Novel Approach to Nonlinear/Non-Gaussian
  Bayesian State Estimation," 1993.

what_is_not_concluded:
- Claude review does not certify empirical validity.
- No benchmark was run.
- No claim is made that the adaptive Zhao--Cui algorithm is globally
  differentiable.

## Review Attempts

| Iteration | Scope | Outcome |
|---|---|---|
| 1 | Full P27 files | Stalled/no useful output within the working interval; replaced by bounded excerpt review. |
| 1b | Validation section excerpt, P27 lines 8244--9266 | Returned 10 findings. |

## Codex Classification Of Claude Findings

| # | Claude finding summary | Codex classification | Patch/control added |
|---|---|---|---|
| 1 | Fixed-branch derivative validation not operational enough. | ACCEPT | Added \(\widehat\ell_T\) definition, branch transcript \(B\), finite-difference ladder \(\mathcal H_{\rm FD}\), branch-stable decreasing-window definition, and failure consequence in `The Exact-Reference Linear Gaussian Benchmark`. |
| 2 | Opening overclaims large-scale validation relative to Zhao--Cui reproduced models. | ACCEPT | Added explicit protocol-not-outcomes sentence; reframed Zhao--Cui models as diverse benchmark suite; stated BayesFilter large-scale claim requires added stress ladders. |
| 3 | Veto thresholds are undefined. | ACCEPT | Added default tolerance table after veto equations with \(\varepsilon_{\rm norm}\), \(\kappa_{\rm max}^{\rm allowed}\), \(\varepsilon_{\rm fit}\), and \(\varepsilon_{\rm KR}\). |
| 4 | Stochastic-volatility transformed coordinates mix fixed- and free-\(\sigma\) cases. | ACCEPT | Split into synthetic fixed-\(\sigma\) transform and real-data free-\(\sigma\) transform. |
| 5 | SIR and predator-prey reproduction settings omit key Zhao--Cui choices. | ACCEPT | Added SIR \(\Delta\), RK4 step, process/observation noise, initial conditions, and prior; added predator-prey truth, \(\Delta\), RK4 step, noise, prior box, and \(X_0\) prior. |
| 6 | Benchmark table mixes incomparable accuracy metrics. | ACCEPT | Replaced \(E_{\rm acc}\) with model-specific diagnostic class and \(\mathcal E_{\rm model}\); table now marks measured fields. |
| 7 | Benchmark implications too clean without seed/uncertainty policy. | ACCEPT | Qualified each implication by declared seeds, tolerances, run contract, cost model, or uncertainty policy; added one-seed diagnostic caveat. |
| 8 | Some language sounds like internal governance. | PARTIAL | Softened the main offending phrases: "eligible" became "should be interpreted only"; "dots not acceptable" became measured-values prose. Retained "must/should" where it states mathematical test requirements. |
| 9 | LG derivative \(\beta\) and \(\widehat\ell_T\) not locally defined. | ACCEPT | Added local definition before derivative equation. |
| 10 | No unsupported result claims, but title/opening could be misread. | ACCEPT | Added explicit "does not report BayesFilter benchmark outcomes" sentence. |

## Remaining Review Limitation

Claude did not complete a full-file review.  The successful review covered the
new validation section only, which is the requested P27 change.  Codex accepts
this limitation because P27 preserves P26 and the user's request was to add the
test section.

