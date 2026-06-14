# P18 Zhao--Cui Source-Support Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- DeepTransport `tensor-ssm-paper-demo` companion code snapshot, as audited in P10.

what_is_not_concluded:
- No claim that adaptive Zhao--Cui code is globally differentiable.
- No claim that BayesFilter has production TT filtering code.
- No claim that P18 validates posterior accuracy on BayesFilter target models.
- No default-method recommendation.

## Source Status

| Source | Local artifact | Status checked | Technical anchors inspected for P18 | Allowed claims | Forbidden claims |
|---|---|---|---|---|---|
| Zhao and Cui JMLR 2024 | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | Local full text present; PDF metadata reports 51 pages and JMLR 2024. Web check requested on 2026-06-01 for JMLR page/retraction signals; no adverse local quarantine notice found. | Sections 1--3 and 5; Eqs. (1)--(26), (30)--(35); Algorithms 1--5; Lemma 1; Propositions 2 and 4; notation block; Section 5 preconditioning text. | State-space recursion, four marginal learning tasks, TT approximation, squared-TT nonnegativity, marginalization/mass matrix formula, KR maps, particle correction, path smoothing, preconditioning framework. | Production readiness, global differentiability of adaptive branch choices, exact posterior accuracy, BayesFilter target-model validation. |
| Cui and Dolgov FoCM 2022 | Not freshly loaded in P18; referenced through Zhao--Cui Lemma 1/Proposition 2 citations and prior ledgers. | Used only where Zhao--Cui explicitly delegates square-root/KR results. | Zhao--Cui Lemma 1 and Proposition 2 references. | Background support for squared-TT/KR identities as cited by Zhao--Cui. | New theorem-level claims beyond P18 project derivations. |
| `tensor-ssm-paper-demo` snapshot | `third_party/audit/zhao_cui_tensor_ssm_p10/source` | Local code snapshot audited in P10. | P10 code audit/crosswalk, filtering scalar, reproducibility ledgers. | Implementation evidence that the companion code has TT/SIRT objects, marginalization paths, and log-normalizer-like updates. | Mathematical proof, Octave portability for every script, production quality. |

## Quarantine And Version Notes

- No local quarantine or retraction note is present in `.local_sources/` or the
  P10--P17 ledgers.
- Citation counts and venue rankings are not used as correctness evidence.
- If live metadata lookup is unavailable or incomplete, P18 records the blocker
  rather than inventing metadata.

Decision: `SOURCE_SUPPORT_PASS_FOR_P18_LOCAL_TRUE_ANNOTATION`.
