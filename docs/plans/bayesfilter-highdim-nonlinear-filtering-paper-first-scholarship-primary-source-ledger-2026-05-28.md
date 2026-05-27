# Paper-First Scholarship Primary-Source Ledger

Date: 2026-05-28

## Purpose

This ledger records source availability for the high-dimensional nonlinear
filtering paper-first rewrite.  It is deliberately a blocker ledger, not a
literature survey.  A paper may drive chapter derivations only after its
technical text has been locally inspected.

## Local MCP Status

ResearchAssistant MCP is read-only and available.  On 2026-05-28, Codex queried
the local workspace for the required tensor-train filtering, Zhao--Cui
conditional KR transport, Spantini--Baptista--Marzouk transport filtering,
sparse-grid filtering, transport-map MCMC, deep inverse Rosenblatt TT, and
tensor-substrate papers.  The relevant queries returned no local summaries for
the required paper-first pillars.  The only related local review items visible
were NeuTra, RMHMC, learned HMC, and normalizing flows, all marked
`needs_review`.

Therefore chapter execution is blocked until source intake is approved and the
technical sections are inspected.

## Source-Support Classes

- `LOCAL_FULL_TEXT_CHECKED`: technical full text is locally available and
  relevant equations/algorithms have been inspected.
- `LOCAL_SUMMARY_ONLY`: local summary exists, but not enough for theorem-level
  chapter support.
- `METADATA_ONLY`: title/URL known, no technical support.
- `NEEDS_NETWORK_INTAKE`: fetch or inspect the exact public source URL before
  using.
- `PAYWALL_OR_ACCESS_BLOCKED`: source may need institutional/manual access.

## Required Paper Ledger

| Pillar | Paper | URL | Current support | Required inspection before rewrite |
| --- | --- | --- | --- | --- |
| Direct TT nonlinear filtering | Li, Wang, Yau, Zhang, TT method for nonlinear filtering via FKE/DMZ-style PDEs | `https://arxiv.org/abs/1908.04010` | `NEEDS_NETWORK_INTAKE` | Model assumptions, FKE/DMZ equation, TT discretization, offline/online algorithm, convergence/error and examples. |
| Direct TT nonlinear filtering | Zhao and Cui, TT sequential state and parameter learning with conditional KR transports | `https://www.jmlr.org/papers/v25/23-0743.html` | `NEEDS_NETWORK_INTAKE` | Posterior recursion, TT approximation, conditional KR transport construction, state/parameter learning algorithm, complexity. |
| Direct TT nonlinear filtering | Functional TT grid filtering for Bayes-optimal continuous-discrete filtering | `https://www.tandfonline.com/doi/full/10.1080/17415977.2020.1862109` | `NEEDS_NETWORK_INTAKE` | Continuous-discrete filtering formulation, functional TT grid approximation, update/prediction algorithm, error/failure modes. |
| Direct TT nonlinear filtering | Meng, Yau, Zhang, TT nonlinear filtering with correlated noise | `https://arxiv.org/abs/2605.25677` | `NEEDS_NETWORK_INTAKE` | Correlated-noise filtering equation, DMZ/SPDE handling, TT approximation, assumptions, algorithm. |
| Tensor-network Kalman | Batselier, Chen, Wong TNKF for lifted Volterra systems | `https://arxiv.org/abs/1610.05434` | `NEEDS_NETWORK_INTAKE` | Lifted system, tensor-network state/covariance representation, Kalman update, rank/truncation diagnostics. |
| Tensor-network Kalman | Tensor-network square-root Kalman filter | `https://arxiv.org/abs/2409.03276` | `NEEDS_NETWORK_INTAKE` | Square-root factor update, PSD preservation rationale, tensor rounding failure modes, algorithm. |
| Tensor-network Kalman | Low-rank tensor UKF tractography | `https://www.sciencedirect.com/science/article/pii/S1053811923001507` | `NEEDS_NETWORK_INTAKE` | Observation compression setting, tensor UKF construction, domain limits, relevance to nonlinear observation geometry. |
| Transport-map filtering | Spantini, Baptista, Marzouk nonlinear ensemble filtering | `https://epubs.siam.org/doi/10.1137/20M1312204` | `NEEDS_NETWORK_INTAKE` | Coupling formulation, map update, ensemble approximation, localization/decomposition, complexity. |
| Transport-map filtering | Ensemble transport smoothing, Part I | `https://www.sciencedirect.com/science/article/pii/S2590055223000124` | `NEEDS_NETWORK_INTAKE` | Smoothing factorization, transport construction, triangular/decomposable structure, algorithm. |
| Transport-map filtering | Decomposable transports for Bayesian filtering/smoothing | `https://approximateinference.org/2016/accepted/SpantiniEtAl2016.pdf` | `NEEDS_NETWORK_INTAKE` | Decomposable map assumptions, filtering/smoothing factorization, algorithmic implications. |
| Sparse/high-order | High-degree cubature Kalman filter | `https://www.sciencedirect.com/science/article/pii/S000510981200550X` | `NEEDS_NETWORK_INTAKE` | Cubature rule, exactness degree, point count, Kalman update use, limitations. |
| Sparse/high-order | Sparse-grid quadrature nonlinear filtering | `https://www.sciencedirect.com/science/article/pii/S0005109811005541` | `NEEDS_NETWORK_INTAKE` | Smolyak/sparse-grid construction, nonlinear filtering recursion, complexity, examples. |
| Sparse/high-order | Adaptive sparse-grid Gauss-Hermite filtering | `https://www.sciencedirect.com/science/article/pii/S0377042718301742` | `NEEDS_NETWORK_INTAKE` | Adaptive rule construction, Gauss-Hermite weighting, refinement criteria, failure modes. |
| HMC/transport substrate | Transport-map accelerated MCMC | `https://epubs.siam.org/doi/10.1137/17M1134640` | `NEEDS_NETWORK_INTAKE` | Pushforward target, map approximation, MCMC acceleration theory, diagnostics. |
| HMC/transport substrate | NeuTra HMC | `https://arxiv.org/abs/1903.03704` | `LOCAL_SUMMARY_ONLY` | Full paper still needs technical inspection: learned transport, transformed target, HMC diagnostics, experiments. |
| HMC/transport substrate | Deep inverse Rosenblatt transports using tensor trains | `https://arxiv.org/abs/2007.06968` | `NEEDS_NETWORK_INTAKE` | Inverse Rosenblatt construction, TT representation, sampling/proposal relevance, complexity. |
| Tensor substrate | TT sampling of multivariate densities | `https://link.springer.com/article/10.1007/s11222-019-09910-z` | `NEEDS_NETWORK_INTAKE` | Sampling algorithm, density representation, complexity, failure modes. |
| Tensor substrate | TT rank bounds for Gaussian densities | `https://arxiv.org/abs/2001.08187` | `NEEDS_NETWORK_INTAKE` | Rank theorem assumptions, Gaussian covariance structure, implications and limits. |
| Tensor substrate | Fokker-Planck by TT cross approximation | `https://pmc.ncbi.nlm.nih.gov/articles/PMC8366026/` | `NEEDS_NETWORK_INTAKE` | PDE discretization, TT-cross method, complexity, error/failure diagnostics. |
| Tensor substrate | Fast high-dimensional integration using tensor networks | `https://arxiv.org/abs/2202.09780` | `NEEDS_NETWORK_INTAKE` | Integration formulation, tensor-network contraction, complexity, relation to quadrature replacement. |

## Execution Decision

`BLOCK_CHAPTER_REWRITE_PENDING_SOURCE_INTAKE`.

The planning files can be reviewed and committed if accepted.  The chapter
rewrite cannot begin honestly until the exact public sources above are fetched
or otherwise made locally available and their technical sections are inspected.

## Requested Source-Intake Approval

If the planning review is accepted, Codex should ask the user for approval to
fetch the exact public URLs listed in this ledger for local scholarly review.
Paywalled URLs may produce metadata or access blockers; those blockers must be
recorded rather than bypassed.
