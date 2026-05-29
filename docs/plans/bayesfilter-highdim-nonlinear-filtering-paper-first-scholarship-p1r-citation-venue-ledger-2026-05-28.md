# P1R Citation And Venue Metadata Ledger

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: high-dimensional nonlinear filtering paper-first seed set.

what_is_not_concluded: see section "What Is Not Concluded".

Field mapping: the table uses the exact metadata fields `citation_count`,
`citation_metadata_source`, `citation_metadata_access_date`, `venue_metric`,
`venue_metric_source`, and `venue_metric_access_date` required by the P1R plan.

## Metadata Policy

Citation counts and venue rankings are coverage and prioritization signals only.
They are never truth evidence and never theorem-level support.  P1R did not run
live citation/ranking queries because no exact metadata source/query scope was
approved for this redo.  Therefore citation-count and venue-rank fields are
blocked rather than guessed.

Local venue and DOI fields below come from local PDF metadata, article headers,
or `docs/references.bib` where available.  Missing citation counts are recorded
as `METADATA_BLOCKED_NO_APPROVED_QUERY`, not as zero.

Blocked access dates use the explicit sentinel `QUERY_DATE_N/A`.

## Metadata Rows

| Paper | Seed? | Venue/status from local source | citation_count | citation_metadata_source | citation_metadata_access_date | venue_metric | venue_metric_source | venue_metric_access_date | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Li--Wang--Yau--Zhang 2019 TT nonlinear filtering | yes | arXiv:1908.04010 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked arXiv technical source; do not use venue/citation prestige. |
| Zhao--Cui 2024 TT sequential learning | yes | JMLR 25 (2024), local PDF header, CC-BY | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked peer-reviewed primary source. |
| Fox--Dolgov--Morrison--Molteno 2021 functional TT grid filtering | yes | Inverse Problems in Science and Engineering 29(8), DOI `10.1080/17415977.2020.1862109`, accepted manuscript | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked accepted manuscript; venue metrics unavailable. |
| Meng--Yau--Zhang 2026 TT correlated-noise filtering | yes | arXiv:2605.25677 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Treat as recent arXiv; cite only with source-status caveat. |
| Batselier--Chen--Wong 2016 TNKF | yes | arXiv:1610.05434 local PDF; preprint submitted to Automatica per text | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked preprint for TNKF mechanics. |
| Menzen--Kok--Batselier 2024 tensor-network square-root Kalman filter | yes | arXiv:2409.03276 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as recent arXiv for PSD/square-root warning with caveat. |
| Gruen--Groeschel--Schultz 2023 low-rank tensor tractography | yes | NeuroImage 271 (2023) 120004, DOI `10.1016/j.neuroimage.2023.120004`, local PDF metadata | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite only as domain-specific empirical example. |
| Spantini--Baptista--Marzouk transport filtering | yes | arXiv/SIAM preprint local PDF; DOI listed in master as `10.1137/20M1312204` | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked transport-map filtering source. |
| Ramgraber--Baptista--McLaughlin--Marzouk ensemble transport smoothing | yes | arXiv:2210.17000v2 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite for smoothing framework; note arXiv/source status. |
| Spantini et al. 2016 decomposable transport workshop | yes, quarantined | User-reported retracted; no support status | `QUARANTINED` | `QUARANTINED` | `QUERY_DATE_N/A` | `QUARANTINED` | `QUARANTINED` | `QUERY_DATE_N/A` | `RETRACTED_OR_QUARANTINED`; do not cite as support. |
| Jia--Xin--Cheng 2012 sparse-grid quadrature nonlinear filtering | yes | Automatica 48 (2012) 327--341, DOI `10.1016/j.automatica.2011.08.057`, local PDF metadata | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked primary source for SGQF mechanics. |
| Jia--Xin--Cheng 2013 high-degree cubature Kalman filter | yes | Automatica 49 (2013) 510--518, DOI `10.1016/j.automatica.2012.11.014`, local PDF metadata | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked primary source for high-degree CKF. |
| Singh--Radhakrishnan--Bhaumik--Date adaptive sparse-grid GH filter | yes | arXiv:1803.09272 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked arXiv competitor with caveat. |
| Parno--Marzouk transport-map accelerated MCMC | yes | SIAM/ASA JUQ 2018 per `docs/references.bib`; local PDF arXiv/SIAM preprint | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked primary source for transport-map MCMC. |
| Hoffman et al. NeuTra HMC | yes | ICML 2019/JMLR 2021 metadata from local PDF and `docs/references.bib` | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite for geometry-preconditioned HMC only, not convergence. |
| Cui--Dolgov deep inverse Rosenblatt TT | yes | arXiv:2007.06968v3 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked TT/transport bridge. |
| Dolgov et al. TT sampling of multivariate densities | yes | Statistics and Computing 30 (2020), DOI `10.1007/s11222-019-09910-z`, local PDF metadata | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked TT sampling substrate. |
| TT rank bounds for Gaussian densities | yes | arXiv:2001.08187 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked rank-plausibility source. |
| Fokker--Planck by TT cross approximation | yes | Frontiers PDF/PMC HTML local; DOI not extracted in P1R | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked PDE/tensor substrate source after bib identity cleanup. |
| Cassel fast high-dimensional integration using tensor networks | yes | arXiv:2202.09780 local PDF | `METADATA_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY` | `QUERY_SOURCE_BLOCKED` | `QUERY_DATE_N/A` | Cite as checked tensor-integration context only. |

## Metadata Blockers

- No approved live source for citation counts such as Semantic Scholar, Google
  Scholar, OpenAlex, Crossref citation-by metadata, Scopus, Web of Science, or
  publisher citation widgets was queried in P1R.
- No approved live source for venue ranking such as JCR, Scimago, CORE, ABDC, or
  conference ranking tables was queried in P1R.
- Future metadata intake must record exact query source, query scope, access
  date, and affected papers before numbers enter this ledger.

## What Is Not Concluded

This ledger does not rank papers by correctness, quality, or truth.  It does
not prove that a highly cited or highly ranked venue paper is correct, nor that
a low-citation or arXiv paper is irrelevant.  It only records local publication
identity and live-metadata blockers.
