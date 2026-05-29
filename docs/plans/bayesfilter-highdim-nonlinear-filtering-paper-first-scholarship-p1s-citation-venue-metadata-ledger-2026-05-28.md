# P1S Citation And Venue Metadata Ledger

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: P1R seed set plus P1S foundational blockers where public metadata
was queried.

what_is_not_concluded: see section "What Is Not Concluded".

## Metadata Policy

Citation counts and venue facts are coverage/prioritization signals only.  They
do not support theorem, algorithm, convergence, accuracy, implementation, or
production claims.  Local bibliographic facts are separated from live metadata
queries.  Search-result metadata can be noisy; only exact title/DOI matches are
used as paper-level citation-count rows.

## Metadata Rows

| paper_or_topic | seed_or_blocker | local_bibliographic_fact_source | live_metadata_source_status | citation_count | citation_metadata_source | citation_metadata_query | citation_metadata_access_date | venue | venue_metric | venue_metric_source | venue_metric_query | venue_metric_access_date | metadata_caveat | coverage_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Oseledets 2011, "Tensor-Train Decomposition" | blocker | local PDF metadata and `docs/references.bib` context | `OPENALEX_EXACT_DOI_RECORD` | 2617 | OpenAlex snapshot `.local_sources/highdim_nonlinear_filtering/openalex_oseledets_tt_2011.json` | DOI `10.1137/090752286` | 2026-05-28 | SIAM Journal on Scientific Computing | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Citation count is live OpenAlex metadata; venue rank not queried. | High coverage priority; closed by source anchors, not by count. |
| Jia--Xin--Cheng 2012 SGQF | seed | local PDF metadata | `OPENALEX_EXACT_DOI_RECORD` | 259 | OpenAlex snapshot `openalex_jia_sgqf_2012.json` | DOI `10.1016/j.automatica.2011.08.057` | 2026-05-28 | Automatica | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Publication year in OpenAlex appears as 2011 while local PDF issue is 2012; DOI/title match. | Keep as central Ch34 source. |
| Jia--Xin--Cheng 2013 high-degree CKF | seed | local PDF metadata | `OPENALEX_EXACT_DOI_RECORD` | 460 | OpenAlex snapshot `openalex_jia_hdcf_2013.json` | DOI `10.1016/j.automatica.2012.11.014` | 2026-05-28 | Automatica | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Publication year in OpenAlex appears as 2012 while local PDF issue is 2013; DOI/title match. | Keep as central Ch34 source. |
| Spantini--Baptista--Marzouk 2022 transport filtering | seed | local PDF and bibliography DOI | `OPENALEX_EXACT_DOI_RECORD` | 64 | OpenAlex snapshot `openalex_spantini_transport_filtering.json` | DOI `10.1137/20M1312204` | 2026-05-28 | SIAM Review | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Citation count is coverage signal only. | Keep as central transport filtering source. |
| Parno--Marzouk 2018 transport-map accelerated MCMC | seed | local PDF and `docs/references.bib` | `OPENALEX_EXACT_DOI_RECORD` | 81 | OpenAlex snapshot `openalex_parno_transport_mcmc.json` | DOI `10.1137/17M1134640` | 2026-05-28 | SIAM/ASA Journal on Uncertainty Quantification | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Citation count is not HMC/transport validation. | Keep as transport-preconditioned MCMC source. |
| Reich 2013 ensemble transform | blocker | local PDF and `docs/references.bib` | `OPENALEX_EXACT_DOI_RECORD` | 184 | OpenAlex snapshot `openalex_reich_ensemble_transform.json` | DOI `10.1137/130907367` | 2026-05-28 | SIAM Journal on Scientific Computing | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Citation count is coverage signal only. | Closed as transport competitor/foundation. |
| Hoffman--Gelman 2014 NUTS | blocker | local JMLR PDF and `docs/references.bib` | `OPENALEX_EXACT_RECORD_BY_DOI_STYLE_ID` | 169 | OpenAlex snapshot `openalex_hoffman_gelman_nuts.json` | DOI-style id `10.5555/2627435.2638586` | 2026-05-28 | Journal of Machine Learning Research | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | OpenAlex uses ACM-style identifier; local JMLR PDF is primary support. | Closed as NUTS reference. |
| Li--Wang--Yau--Zhang 2019 TT filtering | seed | local arXiv PDF | `OPENALEX_SEARCH_EXACT_TOP_RESULT` | 3 | OpenAlex snapshot `openalex_li_wang_yau_zhang_tt_filtering.json` | title search | 2026-05-28 | arXiv | `VENUE_RANK_NOT_APPLICABLE_ARXIV` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Search results include unrelated high-cited papers after exact top result; use only exact top row. | Keep as direct method, with low-citation/recent-preprint caveat. |
| Zhao--Cui 2024 TT sequential learning | seed | local JMLR PDF | `OPENALEX_SEARCH_EXACT_TOP_RESULT_ARXIV_ONLY` | 1 | OpenAlex snapshot `openalex_zhao_cui_jmlr_2024.json` | title search | 2026-05-28 | JMLR local PDF; OpenAlex top row is arXiv preprint | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | OpenAlex search found arXiv DOI, not the JMLR version; local JMLR PDF governs bibliographic status. | Keep as peer-reviewed direct method; metadata incomplete. |
| Arasaratnam--Haykin CKF | blocker | P1R/Jia references; no local full text | `OPENALEX_SEARCH_NO_EXACT_TOP_RESULT` | `METADATA_UNRELIABLE_SEARCH_NO_EXACT_RECORD` | OpenAlex snapshot `openalex_arasaratnam_haykin_ckf.json` | title search | 2026-05-28 | unknown | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | OpenAlex search top rows were not the CKF primary paper; do not record count. | Remains source/metadata blocked for primary CKF derivation. |
| Betancourt 2017 HMC conceptual introduction | blocker | local arXiv PDF | `OPENALEX_SEARCH_NOISY_NO_EXACT_RECORD_USED` | `METADATA_UNRELIABLE_SEARCH_NO_EXACT_RECORD` | OpenAlex snapshot `openalex_betancourt_hmc.json` | title search | 2026-05-28 | arXiv | `VENUE_RANK_NOT_APPLICABLE_ARXIV` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Search returned citing/related works, not a reliable exact record. | Use local PDF as technical source; no citation-count claim. |
| Girolami--Calderhead RMHMC | blocker | `docs/references.bib`; no local full text | `OPENALEX_SEARCH_NOISY_NO_EXACT_RECORD_USED` | `METADATA_UNRELIABLE_SEARCH_NO_EXACT_RECORD` | OpenAlex snapshot `openalex_girolami_calderhead_rmhmc.json` | title search | 2026-05-28 | JRSS B per bibliography | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Search was noisy; no local technical text. | Remains source-blocked. |
| Snyder et al. 2008 obstacles to high-dimensional PF | blocker | `docs/references.bib`; public PDF attempt failed | `OPENALEX_SEARCH_EXACT_TOP_RESULT` | 700 | OpenAlex snapshot `openalex_snyder_obstacles_pf.json` | title search | 2026-05-28 | Monthly Weather Review | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Exact metadata found, but no technical full text; count raises omission risk only. | Remains source-blocked for theorem-level collapse claims. |
| Arulampalam et al. 2002 PF tutorial | blocker | local PDF and `docs/references.bib` | `OPENALEX_SEARCH_EXACT_TOP_RESULT` | 11461 | OpenAlex snapshot `openalex_arulampalam_pf_tutorial.json` | title search | 2026-05-28 | IEEE Transactions on Signal Processing | `VENUE_RANK_NOT_QUERIED` | `QUERY_NOT_RUN` | `QUERY_NOT_RUN` | `QUERY_DATE_N/A` | Very high count is a coverage signal, not proof of correctness. | Closed for standard PF tutorial baseline. |

## Metadata Blockers

- Venue rankings were not queried from JCR, Scimago, CORE, ABDC, or similar
  ranking services.
- Several OpenAlex search queries were noisy.  No citation count was recorded
  unless the title/DOI match was exact enough for this planning phase.
- Google Scholar, Scopus, and Web of Science were not queried.

## What Is Not Concluded

This ledger does not rank papers by truth or quality.  It does not validate
methods and does not close source-support blockers without checked technical
anchors.
