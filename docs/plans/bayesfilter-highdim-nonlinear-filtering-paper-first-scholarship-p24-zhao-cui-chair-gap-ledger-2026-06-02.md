# P24 Zhao--Cui Chair Gap Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.

what_is_not_concluded:
- No theorem that moderate TT ranks hold for arbitrary nonlinear posteriors.
- No claim that the fixed-branch gradient differentiates the adaptive
  Zhao--Cui algorithm.
- No claim that the note is a production implementation.

## Chair Gaps

| Gap | Control added in P24 | Status |
|---|---|---|
| Why moderate TT rank is plausible beyond storage counts. | Added split-rank, SVD analogy, local-dependence equations, global-failure example, preconditioning residual ratio, and diagnostics in "Why Moderate Tensor-Train Rank Is A Plausible Hypothesis." | `DONE` |
| How physical \(r\), reference \(z\), preconditioned \(u\), and retained \(z_t\) coordinates relate. | Added coordinate transformation section with density/Jacobian equations and table of symbols, spaces, density identities, and stored objects. | `DONE` |
| Why fixed-branch gradient is useful but narrower than adaptive differentiation. | Added adaptive branch \(B(\beta)\), fixed branch \(B_0\), scalar definitions, and finite-difference identity. | `DONE` |

