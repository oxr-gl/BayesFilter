# P19 Zhao--Cui Gradient Teaching Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P10 filtering-scalar and gradient-feasibility ledgers.
- P15 fixed-branch implementation specification.
- P18 annotated companion.

what_is_not_concluded:
- No claim that P19 proves exact posterior accuracy.
- No claim that adaptive Zhao--Cui code is globally differentiable.
- No claim that HMC convergence follows from the gradient derivation.

## Teaching Controls

| Topic | Required chair-readable control | Status |
|---|---|---|
| Scalar | Explain \(\widehat\ell_T=\sum_t\log\widehat Z_t\) before TT notation. | `IMPLEMENTED`; note Sec. 1, Eqs. (1)--(5). |
| Fixed branch | Explain what is frozen and why adaptive decisions are not differentiated. | `IMPLEMENTED`; note Sec. 1 and Sec. 6.  Clarifies that structural choices are frozen, while fitted core values remain parameter-dependent. |
| Log normalizer | Derive \(\partial\log Z=\dot Z/Z\) step by step. | `IMPLEMENTED`; note Sec. 2, Eqs. (7)--(13). |
| Squared approximation | Derive \(2\phi\dot\phi\) and identify frozen \(c,\tau,\lambda\). | `IMPLEMENTED`; note Sec. 3, Eqs. (14)--(20). |
| Rank-one TT | Derive two-coordinate rank-one square integral. | `IMPLEMENTED`; note Sec. 4, Eqs. (21)--(28). |
| Rank-\(R\) TT | Show mass matrices before full TT recursion. | `IMPLEMENTED`; note Sec. 5, Eqs. (29)--(36). |
| Linear solve | Derive \(N\dot g=\dot d-\dot N g\). | `IMPLEMENTED`; note Sec. 6, Eqs. (37)--(43). |
| Design-row bridge | Teach why a TT core update is linear in \(\vec(C_k)\), before Kronecker notation. | `IMPLEMENTED_AFTER_REVIEW`; note Sec. 8, Eqs. (53b)--(53h). |
| Full mass bridge | Tie rank-\(R\) warmup to the indexed full TT mass recursion. | `IMPLEMENTED_AFTER_REVIEW`; note Sec. 8 before Eq. (66). |
| Carried filter | Derive quotient derivative and next-step target role. | `IMPLEMENTED`; note Sec. 8, Eqs. (73)--(76). |
| Carried marginal contraction | Give explicit \(a_t\) and \(\dot a_t\) contraction recipe from core derivatives. | `IMPLEMENTED_AFTER_REVIEW`; note Sec. 8, Eqs. (74a)--(74d). |
| Finite difference | Specify same-branch parity test. | `IMPLEMENTED`; note Sec. 12, Eqs. (94)--(101). |
| Positivity floor | Explain that a floor changes the declared scalar and must be differentiated as such. | `IMPLEMENTED_AFTER_REVIEW`; note Sec. 8, Eq. (53a). |

## Current Teaching Judgment Before Claude Execution Review

Decision: `READY_FOR_HOSTILE_EXECUTION_REVIEW`.

The note now teaches the derivative in the order requested by the user:
normalizer, squared approximation, rank-one mass integral, rank-\(R\) mass
matrix, linear solve, full forward objects, full derivative objects, and then
the two propositions.  The remaining question is not whether the skeleton is
present, but whether the former-chemistry chair and numerical-computation
personas find the explanations teachable.  That is delegated to the P19 Claude
execution review loop, with Codex retaining final audit authority.
