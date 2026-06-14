# P16 Zhao-Cui Source-Support Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- DeepTransport `tensor-ssm-paper-demo` companion code snapshot.

what_is_not_concluded:
- No literature completeness claim beyond the checked local sources and prior
  P10-P15 ledgers.
- No source claim based on abstracts, venue rank, or citation count.
- No proof that BayesFilter has a production implementation.

## Sources

| Source | Local artifact | Publication/full-text status | Retraction/quarantine/version status | Inspected anchors | Allowed claims | Forbidden claims |
|---|---|---|---|---|---|---|
| Zhao and Cui JMLR 2024 | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | Published JMLR 2024; local full text available; PDF states CC-BY 4.0 | No local quarantine notice found; no external retraction check performed in this run; version treated as local JMLR PDF | Sections 1--3, 4.1, 5, selected Section 6 examples, Appendix references from local text | State-space recursion, TT approximation idea, squared-TT construction, marginalization formula, KR maps, particle/path correction, preconditioning framework, numerical examples as reported | Global differentiability of adaptive code; BayesFilter implementation readiness; HMC convergence; exact posterior accuracy of approximations |
| Cui and Dolgov FoCM 2022 | Referenced through P10-P15 ledgers; full local source not reinspected in P16 | Prior artifacts cite as supporting squared inverse Rosenblatt transports | Not freshly checked in P16 | Used only where Zhao--Cui themselves refer Lemma 1/Proposition 2 support | Background support for squared-TT/KR concepts | New theorem-level claims not derived in P16 |
| `tensor-ssm-paper-demo` code snapshot | `third_party/audit/zhao_cui_tensor_ssm_p10/source` | Local audit copy available; LGPL text present | Code snapshot has no local quarantine notice; no live upstream check in P16 | `models/full_sol.m`, `models/Y_sol.m`, `deep-tensor.dev/src/@TTSIRT/marginalise.m`, `TTSIRT.m`, `SIRT.m` | Implementation evidence that normalizers, marginalization, TTSIRT, inverse/conditional transports, and log-marginal update paths exist | Mathematical validity; production readiness; exact reproducibility of all paper figures |

## Source-Support Decision

`SOURCE_SUPPORT_PASS_FOR_LOCAL_ANNOTATED_RECONSTRUCTION_WITH_METADATA_BLOCKERS`

The main note is supported by checked local technical text and by project
derivations.  Live metadata, citation counts, and forward snowballing were not
queried in this execution and are explicitly not used as support.
