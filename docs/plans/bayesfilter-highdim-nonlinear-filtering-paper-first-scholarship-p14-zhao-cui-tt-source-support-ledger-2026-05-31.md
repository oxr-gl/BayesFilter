# P14 Zhao-Cui TT Source-Support Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10/P11/P12/P13 BayesFilter artifacts.

what_is_not_concluded:
- No field-complete literature survey.
- No citation count or venue metadata is used as truth evidence.
- No posterior accuracy.
- Code anchors support inspected implementation structure only.

## Claim Labels

| Claim/construction | Label | Anchor |
|---|---|---|
| Filtering object \(q_t\), evidence increment, and marginal filter | `DERIVED_IN_NOTE` | P14 equations for \(q_t\), \(Z_t\), and filter marginal. |
| Scalar quadratic-observation example | `DERIVED_IN_NOTE` | P14 scalar example equations. |
| Two-coordinate rank factorization and three-coordinate TT coefficient form | `DERIVED_IN_NOTE` | P14 Section 3. |
| Functional TT representation and storage comparison | `DERIVED_IN_NOTE` with source context | P14 Section 3; source context Zhao-Cui/Cui-Dolgov TT substrate. |
| Squared approximation \(\phi^2+\tau\lambda\) | `PAPER_EXPLICIT` and `DERIVED_IN_NOTE` | Zhao-Cui equation (13) vicinity; P14 Section 4 derivation. |
| Sequential density over \((x_t,\theta,x_{t-1})\) | `PAPER_EXPLICIT` and `DERIVED_IN_NOTE` | Zhao-Cui equations (9)--(12), Algorithm 1; P14 derivation. |
| Marginal and conditional/KR constructions | `PAPER_EXPLICIT` | Zhao-Cui Propositions 2 and 4; Cui-Dolgov Sections 2--3. |
| Fixed-branch recursion and normalized-filter Proposition 1 | `DERIVED_IN_NOTE` | P14 Proposition 1, inherited from P12/P13 project derivation. |
| Fixed-branch same-scalar gradient Proposition 2 | `DERIVED_IN_NOTE` | P14 Proposition 2, inherited from P11/P12/P13 project derivation. |
| Companion MATLAB scalar path | `IMPLEMENTATION_INTERPRETATION` | P10 code audit paths; P14 appendix wording. |

## Source Discipline

- Main exposition derives before citing.
- Appendix records paper and code anchors.
- No abstract, citation count, venue prestige, introduction, or conclusion is
  used as theorem support.

Decision:
`P14_MAJOR_TEACHING_CLAIMS_LABELED`
