# P12 Zhao-Cui TT Source Anchor Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- Zhao-Cui companion code audit snapshot.

what_is_not_concluded:
- Source anchors do not prove posterior accuracy.
- Source anchors do not certify the adaptive code gradient.
- Code anchors support implementation behavior only.

## Paper Anchors

| Source | Technical anchor | Used for | Support class |
|---|---|---|---|
| Zhao-Cui 2024 | Equations (1)--(3) | State-space model transition, observation, and parameter notation | `PRIMARY_TECHNICAL_SUPPORT` |
| Zhao-Cui 2024 | Equations (9)--(12), Algorithm 1 | Sequential nonseparable density over \((x_t,\theta,x_{t-1})\) and TT approximation/integration architecture | `PRIMARY_TECHNICAL_SUPPORT` |
| Zhao-Cui 2024 | Equation (13), Lemma 1 vicinity | Squared-TT defensive density \(\widehat\pi=\phi^2+\tau\lambda\) and normalizer | `PRIMARY_TECHNICAL_SUPPORT` |
| Zhao-Cui 2024 | Algorithm 2 | Sequential estimation using squared-TT approximations | `PRIMARY_TECHNICAL_SUPPORT` |
| Zhao-Cui 2024 | Section 4.1 | Exact joint normalizer as evidence and motivation for approximating \(q_t\) | `PRIMARY_TECHNICAL_SUPPORT` |
| Zhao-Cui 2024 | Proposition 2, Proposition 4 vicinity | Marginalization and conditional KR maps from squared-TT densities | `PRIMARY_TECHNICAL_SUPPORT_FOR_CONTEXT` |
| Cui-Dolgov 2022 | Sections 2--3 | TT inverse Rosenblatt and squared inverse Rosenblatt transport substrate | `PRIMARY_TECHNICAL_SUPPORT_FOR_CONTEXT` |

## Code Anchors

| Code path | Inspected line or behavior | Used for | Support class |
|---|---|---|---|
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m` | `sol.logmarginal_likelihood = sol.logmarginal_likelihood + log(sirt.z) - const` | Companion-code scalar behavior | `IMPLEMENTATION_EVIDENCE` |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m` | `potential_to_density` maps potential values to square-root density values with reference/Jacobian factors | Square-root density construction in code | `IMPLEMENTATION_EVIDENCE` |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m` | `approx = TTFun(...)` | TT approximation object creation | `IMPLEMENTATION_EVIDENCE` |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m` | QR/mass marginalization and `obj.z = obj.fun_z + obj.tau` | Normalizer behavior | `IMPLEMENTATION_EVIDENCE` |

Decision:
`SOURCE_ANCHORS_RECORDED_FOR_P12`
