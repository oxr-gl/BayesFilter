# P24 Zhao--Cui Source-Support Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," arXiv:2007.06968 / prior-ledger FoCM status not freshly rechecked in P24.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," The Annals of Mathematical Statistics, 1952.
- DeepTransport `tensor-ssm-paper-demo` companion code snapshot, as audited in P10.

what_is_not_concluded:
- No claim that adaptive Zhao--Cui code is globally differentiable.
- No claim that BayesFilter has production TT filtering code.
- No claim that P24 validates posterior accuracy on BayesFilter target models.
- No default-method recommendation.

## Source Status

| Source | Local artifact | Status checked | Technical anchors inspected for P24 | Allowed claims | Forbidden claims |
|---|---|---|---|---|---|
| Zhao and Cui JMLR 2024 | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | Local full text present; PDF metadata reports 51 pages and JMLR 2024. Local source cache and prior P10--P23 ledgers contain no quarantine, withdrawal, retraction, erratum, or version-conflict notice. Live authoritative retraction/erratum lookup is not used as proof support in P24; absence of a live adverse notice is not concluded from this ledger. | Sections 1--3 and 5; Eqs. (1)--(26), (30)--(35); Algorithms 1--5; Lemma 1; Propositions 2 and 4; notation block; Section 5 preconditioning text. | State-space recursion, four marginal learning tasks, TT approximation, squared-TT nonnegativity, marginalization/mass matrix formula, KR maps, particle correction, path smoothing, preconditioning framework. | Production readiness, global differentiability of adaptive branch choices, exact posterior accuracy, BayesFilter target-model validation. |
| Cui and Dolgov arXiv / prior-ledger FoCM status | `.local_sources/highdim_nonlinear_filtering/deep_inverse_rosenblatt_tt_2007.06968.pdf` | Local full text present. P24 bibliography key `cui2021deep` records an arXiv-preprint entry; prior ledgers refer to a later FoCM publication status, but P24 did not freshly reconcile the arXiv and venue versions. Local source cache contains no quarantine notice. | Used only where Zhao--Cui explicitly delegates square-root/KR results, especially Lemma 1 and Proposition 2 references. | Background support for squared-TT/KR identities as cited by Zhao--Cui and for terminology connecting squared inverse Rosenblatt transports to the P24 reconstruction. | New theorem-level claims beyond Zhao--Cui's delegated statements or P24 project derivations; claims depending on the exact published-version wording without fresh version reconciliation. |
| Oseledets SIAM SISC 2011 | `.local_sources/highdim_nonlinear_filtering/oseledets_tt_decomposition_2011.pdf` | Local full text present; bibliography records SIAM Journal on Scientific Computing 2011 with DOI `10.1137/090752286`. Local source cache contains no quarantine, withdrawal, retraction, erratum, or version-conflict notice. | Tensor-train decomposition background; P24 uses it only to identify the standard TT factorization idea before deriving the local functional-TT algebra needed in the note. | Background support that TT decompositions are a standard rank-linked tensor representation. | Claims about Zhao--Cui filtering correctness, squared-TT nonnegativity, KR maps, fixed-branch derivatives, or BayesFilter implementation readiness. |
| Rosenblatt Annals of Mathematical Statistics 1952 | `.local_sources/highdim_nonlinear_filtering/Remarks on a Multivariate Transformation Rosenblatt(52).pdf` | Local full text present; bibliography records The Annals of Mathematical Statistics 1952. Local source cache contains no quarantine, withdrawal, retraction, erratum, or version-conflict notice. | Triangular transformation background; P24 derives the local conditional-CDF identities it needs rather than relying on a broad theorem-level import. | Background support for the historical triangular transformation terminology. | Claims about tensor trains, Zhao--Cui approximation error, adaptive-branch differentiability, or BayesFilter implementation readiness. |
| `tensor-ssm-paper-demo` snapshot | `third_party/audit/zhao_cui_tensor_ssm_p10/source` | Local code snapshot audited in P10. | P10 code audit/crosswalk, filtering scalar, reproducibility ledgers. | Implementation evidence that the companion code has TT/SIRT objects, marginalization paths, and log-normalizer-like updates. | Mathematical proof, Octave portability for every script, production quality. |

## Quarantine And Version Notes

- No local quarantine, withdrawal, retraction, erratum, or version-conflict note
  is present in `.local_sources/` or the P10--P23 ledgers for the sources used
  in P24.
- P24 records local provenance and version blockers.  It does not claim that a
  live bibliographic database, publisher correction page, or retraction index
  has been exhaustively queried for every cited source during this execution.
- Citation counts and venue rankings are not used as correctness evidence.
- If live metadata lookup is unavailable or incomplete, P24 records the blocker
  rather than inventing metadata.

Decision: `SOURCE_SUPPORT_PASS_FOR_P24_HUMAN_FACING_COMPANION`.
