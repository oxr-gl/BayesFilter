# P12 Zhao-Cui TT Source Support Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- Zhao-Cui companion code audit snapshot.

what_is_not_concluded:
- No complete literature survey.
- No citation-count or venue-rank truth evidence.
- No claim that public pages prove mathematical correctness.
- No claim that absence of a visible warning proves absence of all errata.

## Source Status

| Source | Local artifact | Public status check | Retraction/quarantine/version status | Allowed claims | Forbidden claims |
|---|---|---|---|---|---|
| Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models" | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | JMLR page checked on 2026-05-31: `https://jmlr.org/papers/v25/23-0743.html`; page reports 25(244):1--51, 2024, PDF and code links | No visible retraction, withdrawal, expression of concern, or erratum marker on checked JMLR page; local PDF title/authors/pages match public PDF metadata inspected by `pdftotext` | State-space setup, sequential TT architecture, squared-TT approximation, evidence normalizer, marginalization/KR map context | Posterior accuracy in BayesFilter target model, HMC readiness, production readiness, complete analytical gradient of adaptive code |
| Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports" | `.local_sources/highdim_nonlinear_filtering/deep_inverse_rosenblatt_tt_2007.06968.pdf` | Springer page checked on 2026-05-31: `https://link.springer.com/article/10.1007/s10208-021-09537-5`; page reports version of record and DOI | No visible retraction, withdrawal, expression of concern, or erratum marker on checked Springer page; local PDF is arXiv v3, not the publisher PDF, so version-of-record mismatch risk is recorded | Squared inverse Rosenblatt transport and TT transport substrate as context | Claims requiring exact publisher-version wording unless checked against the Springer page or version of record |
| Zhao-Cui companion code snapshot | `third_party/audit/zhao_cui_tensor_ssm_p10/source` | Snapshot created from public companion repository during P10 audit; in-repo audit snapshot retained for traceability | Research-code snapshot, not production BayesFilter code; license and reuse boundaries remain third-party-audit only | Implementation behavior: scalar accumulator, normalizer path, classes/functions present | Mathematical validity, production correctness, license permission to copy into production modules |

## Metadata Discipline

Citation counts and venue ranks are not used to support any theorem-level or
algorithm-level claim in P12.  The public pages are used only for source status
and version/provenance checks.

Decision:
`SCOPED_SOURCE_SUPPORT_RECORDED_VERSION_RISK_NOTED_FOR_CUI_DOLGOV_LOCAL_PDF`
