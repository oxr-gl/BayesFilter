# P16 Zhao-Cui Omitted-Paper Risk Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.
- Cui and Dolgov FoCM 2022.

what_is_not_concluded:
- No exhaustive survey of TT filtering, transport filters, or particle methods.
- No claim that all direct competitors have been compared.

## Omission Risks

| Risk | Why a reviewer may ask | Current P16 handling | Next action |
|---|---|---|---|
| Tensor-train filtering papers outside Zhao--Cui | P16 promotes Zhao--Cui as a candidate | P16 is an annotated reconstruction, not a survey | Later chapter update should survey direct TT/TN filtering competitors. |
| Transport-map filtering literature | KR maps are central | Zhao--Cui related-work context recorded; P16 derives needed maps | Later survey should inspect Spantini/Reich transport-filter details if used for comparison. |
| Particle MCMC/SMC2 baselines | Zhao--Cui compares against them | Context only; no claim of superiority in P16 | Empirical comparison chapter should handle baselines. |
| Fixed sparse-grid candidate | Other high-dimensional candidate in BayesFilter | Mentioned as comparator in plan, not compared in note | Synthesis chapter should compare mathematically and empirically. |

## Decision

`OMISSION_RISK_ACCEPTABLE_FOR_ANNOTATED_RECONSTRUCTION_NOT_FOR_FINAL_SURVEY`
