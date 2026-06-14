# P12 Zhao-Cui TT Claim Support Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- Zhao-Cui companion code audit snapshot.

what_is_not_concluded:
- No claim of exact posterior accuracy.
- No claim of HMC readiness.
- No claim that adaptive branches are globally differentiable.

## Claim Map

| Claim in P12 note | Support | Status |
|---|---|---|
| Exact state-space filtering recursion follows from prediction plus Bayes update | Project derivation in P12 Section 2 | `PROJECT_DERIVATION` |
| Zhao-Cui approximate the nonseparable density over \((x_t,\theta,x_{t-1})\) | Zhao-Cui Algorithm 1 and equations (9)--(12) | `PRIMARY_TECHNICAL_SUPPORT` |
| Squared-TT defensive density has form \(\phi^2+\tau\lambda\) | Zhao-Cui equation (13) and squared-TT section | `PRIMARY_TECHNICAL_SUPPORT` |
| Squared-TT sequential estimation is applied recursively | Zhao-Cui Algorithm 2 | `PRIMARY_TECHNICAL_SUPPORT` |
| Exact joint normalizer is evidence in Zhao-Cui discussion | Zhao-Cui Section 4.1 | `PRIMARY_TECHNICAL_SUPPORT` |
| Conditional KR maps can be obtained from squared-TT marginals/conditionals | Zhao-Cui Proposition 4 vicinity and Cui-Dolgov Sections 2--3 | `PRIMARY_TECHNICAL_SUPPORT_FOR_CONTEXT` |
| Companion code reports `log(sirt.z)-const` | `models/full_sol.m` | `IMPLEMENTATION_EVIDENCE` |
| Companion code sets `obj.z = obj.fun_z + obj.tau` | `@TTSIRT/marginalise.m` | `IMPLEMENTATION_EVIDENCE` |
| Proposition 1: fixed-branch recursion gives nonnegative normalized approximate filters | P12 proof using nonnegativity, positive finite normalizer, Tonelli, induction | `PROJECT_DERIVATION` |
| Proposition 2: fixed-branch score differentiates declared scalar | P12 proof using chain rule, differentiated squared normalizer, TT product rule, fixed core equations | `PROJECT_DERIVATION` plus narrow `MCP_VERIFIED` identities |
| Adaptive Zhao-Cui code is not globally differentiated by the fixed-branch proof | P10 gradient-feasibility ledger and P12 corollary | `PROJECT_DERIVATION` and `IMPLEMENTATION_EVIDENCE` |

## Source Gaps

- No claim relies on citation counts, venue rank, abstracts, introductions, or
  conclusions.
- The P12 note does not reprove Zhao-Cui's approximation-error theorems.
- The P12 note does not derive the full derivative of adaptive TT-cross,
  rank-changing, or sample-changing operations.

Decision:
`CLAIMS_MAPPED_TO_SOURCE_OR_PROJECT_DERIVATION`
