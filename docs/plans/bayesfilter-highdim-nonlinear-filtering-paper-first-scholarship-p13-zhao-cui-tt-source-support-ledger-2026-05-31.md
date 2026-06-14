# P13 Zhao-Cui TT Source-Support Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- Zhao-Cui companion code audit snapshot under `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

what_is_not_concluded:
- P13 is not a field-complete literature survey.
- No citation count or venue metadata is used as theorem support.
- No posterior accuracy claim is made from the papers or code.
- Code anchors support implementation behavior only.

## Source-Support Scope

P13 is a human-readable rewrite of the already-audited Zhao-Cui fixed-branch
derivation.  It inherits P10/P12 source-support and coverage ledgers.  This
ledger records the claim support used directly in the P13 note.

## Claim Support

| P13 claim or construction | Support class | Source or derivation |
|---|---|---|
| Filtering object \(q_t=\widehat p_{t-1}fg\), evidence increment, and marginal filter | `PROJECT_DERIVATION` | Derived directly in P13 from Bayes' rule. |
| Scalar nonlinear example and \(\widehat q_t=\phi_t^2+\tau\lambda\) normalization | `PROJECT_DERIVATION` | Derived directly in P13. |
| Functional TT core representation and mass contraction | `PROJECT_DERIVATION_WITH_SOURCE_CONTEXT` | Derived in P13; source context from Zhao-Cui and Cui-Dolgov. |
| Zhao-Cui sequential squared-TT algorithm uses nonseparable filtering density, squared TT, normalizer, marginalization, and conditional transport | `PRIMARY_TECHNICAL_SUPPORT` | Zhao-Cui equations (1)--(3), (9)--(13), Algorithm 1, Algorithm 2, Propositions 2 and 4, Section 4.1. |
| Squared inverse Rosenblatt / conditional KR substrate | `PRIMARY_TECHNICAL_SUPPORT_FOR_CONTEXT` | Cui-Dolgov Sections 2--3. |
| Companion code scalar path `log(sirt.z)-const` and `obj.z = obj.fun_z + obj.tau` | `IMPLEMENTATION_EVIDENCE` | P10 code audit snapshot paths listed in P13 appendix. |
| Proposition 1 normalized approximate filtering | `PROJECT_DERIVATION` | Proved in P13, preserving P12 proof. |
| Proposition 2 same-scalar fixed-branch gradient | `PROJECT_DERIVATION` | Proved in P13, preserving P12 proof. |

## Citation Discipline

- The main exposition derives filtering and gradient objects before citing
  Zhao-Cui or Cui-Dolgov.
- Code paths are confined to appendix/ledger context.
- Abstracts, metadata, introductions, conclusions, citation counts, and venue
  prestige are not used as theorem support.
- Retraction/version/quarantine status is inherited from P12 source-support
  ledgers; no new source is introduced in P13.

Decision:
`P13_SOURCE_SUPPORT_SCOPED_AND_HONEST`
