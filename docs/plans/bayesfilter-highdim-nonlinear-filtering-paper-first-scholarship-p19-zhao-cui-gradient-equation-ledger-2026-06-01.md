# P19 Zhao--Cui Gradient Equation Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P15 fixed-branch implementation specification.
- P18 annotated companion.

what_is_not_concluded:
- Equation coverage is not proof of correctness.
- Equation count is not a substitute for chair teach-back.

## Equation Blocks In The P19 Note

| Block | Mathematical purpose | Status |
|---|---|---|
| Scalar likelihood | Define \(\widehat\ell_T\) and \(\widehat Z_t\). | `IMPLEMENTED`; Eqs. (1)--(5). |
| Log normalizer | Derive \(\partial\log Z\). | `IMPLEMENTED`; Eqs. (7)--(13). |
| Differentiation under integral | State sufficient conditions and formula. | `IMPLEMENTED`; Eqs. (10)--(11). |
| Squared density | Derive derivative of \(e^{-c}\phi^2+\tau\lambda\). | `IMPLEMENTED`; Eqs. (14)--(20). |
| Rank-one TT | Derive \(\partial\int h_1^2h_2^2\). | `IMPLEMENTED`; Eqs. (21)--(28). |
| Rank-\(R\) TT | Derive mass matrices. | `IMPLEMENTED`; Eqs. (29)--(36). |
| Linear solve | Derive fixed solve derivative. | `IMPLEMENTED`; Eqs. (37)--(43). |
| Full TT environments | Derive environment and design-row derivative. | `IMPLEMENTED`; Eqs. (53b)--(65), with note that Eq. (45a) clarifies parameter-dependent core values. |
| Design-row Kronecker bridge | Show entrywise why the local row is \(L\,b\,R\) and why the Kronecker shorthand is valid. | `IMPLEMENTED_AFTER_REVIEW`; Eqs. (53b)--(53h). |
| Positivity floor | State how a target floor changes the declared scalar and derivative. | `IMPLEMENTED_AFTER_REVIEW`; Eq. (53a). |
| Mass contraction | Derive full contraction derivative. | `IMPLEMENTED`; Eqs. (66)--(72), with added bridge to rank-\(R\) warmup. |
| Carried filter | Derive quotient derivative. | `IMPLEMENTED`; Eqs. (73)--(76). |
| Carried marginal contraction | Derive \(a_t(z_D)\) and \(\dot a_t(z_D)\) from left environments and retained-coordinate core entries. | `IMPLEMENTED_AFTER_REVIEW`; Eqs. (74a)--(74d). |
| Same-scalar proposition | Prove fixed-branch derivative result. | `IMPLEMENTED`; Proposition 2 and Eqs. (85)--(89). |
| Same-branch finite difference | Define branch identity and centered difference. | `IMPLEMENTED`; Eqs. (94)--(101), with Eq. (95a) clarifying that core values are recomputed by the fixed fitting rule. |

## Equation Count

The note contains 124 numbered or locally tagged displayed equations, including
lettered clarifications (45a), (53a)--(53h), (74a)--(74d), and (95a).  This
count is explanatory only; it is
not a substitute for mathematical correctness or reader teach-back.

Decision: `EQUATION_BLOCKS_IMPLEMENTED_READY_FOR_REVIEW`.
