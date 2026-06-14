# P17 Zhao-Cui Source Support Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit and paper-code crosswalk ledgers.

what_is_not_concluded:
- No fresh forward-citation metadata was collected.
- No retraction database query was performed in this run.
- No theorem-level claim is supported by code alone.

## Source Support

| Source | Local path / status | Inspected anchors | Allowed claims | Forbidden claims |
|---|---|---|---|---|
| Zhao--Cui JMLR 2024 | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`; local PDF states JMLR 2024 and CC-BY 4.0 | Sections 1--3 and 5; selected Section 4/6 context; Algorithms 1--5; Eqs. (1)--(35) within scope | SSM recursion, TT approximation, squared-TT density, marginalization, KR maps, particle/path correction, preconditioning formulas | Global differentiability of adaptive code; posterior accuracy on BayesFilter target; production readiness |
| Cui--Dolgov FoCM 2022 | Not freshly reinspected in P17; used through Zhao--Cui citations and prior ledgers | Zhao--Cui Lemma 1 and Proposition 2 references | Background support for squared-TT/KR concepts as cited by Zhao--Cui | New theorem-level claims not derived in P17 |
| Companion code snapshot | `third_party/audit/zhao_cui_tensor_ssm_p10/source`; LGPL notices present | P10 code audit and paper-code crosswalk | Implementation evidence for code paths and scalar behavior | Mathematical validity or BayesFilter production readiness |

Decision: `SOURCE_SUPPORT_SUFFICIENT_FOR_P17_RECONSTRUCTION_WITH_EXTERNAL_PROOF_LIMITS`

