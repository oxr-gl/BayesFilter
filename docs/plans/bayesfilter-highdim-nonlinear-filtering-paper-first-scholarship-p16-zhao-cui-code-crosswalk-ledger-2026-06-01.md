# P16 Zhao-Cui Code-Crosswalk Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.
- DeepTransport `tensor-ssm-paper-demo` companion code snapshot.

what_is_not_concluded:
- No claim that all code examples were rerun in P16.
- No production BayesFilter implementation claim.

## Checked Code Anchors

| Mathematical object | Code path | P16 use |
|---|---|---|
| Sequential target and log-marginal update | `models/full_sol.m` | Confirms research code updates `logmarginal_likelihood` through `log(sirt.z)-const`. |
| Prior/current target potential | `models/full_sol.m::fun_into_sirt` | Confirms target combines previous approximation, transition, likelihood, and shift. |
| TTSIRT normalizer | `deep-tensor.dev/src/@TTSIRT/marginalise.m` | Confirms `obj.z = obj.fun_z + obj.tau`. |
| Marginalization direction | `@TTSIRT/marginalise.m` | Confirms left/right marginalization logic. |
| Inverse/conditional Rosenblatt operations | `@TTSIRT/TTSIRT.m`, `eval_irt_reference.m`, `eval_cirt_reference.m` | Confirms code has inverse and conditional transport evaluators. |
| Defensive density machinery | `SIRT.m`, `TTSIRT.m` | Confirms tau and potential-to-density pathway. |

## Decision

`CODE_CROSSWALK_PASS_AS_IMPLEMENTATION_EVIDENCE_NOT_MATHEMATICAL_PROOF`
