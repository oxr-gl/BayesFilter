# P1T Citation/Venue Metadata Ledger

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: five user-supplied blocker PDFs in `.local_sources/highdim_nonlinear_filtering/`.

what_is_not_concluded: see section "What Is Not Concluded".

## Purpose

Record metadata status for the five P1T local-PDF closures.  Citation counts and
venue information are coverage signals only.  They never support theorem-level,
algorithm-level, convergence, implementation, or production-readiness claims.

No live metadata refresh was run in P1T.  Cached P1S metadata is used only where
an exact cached record was already available.  Missing metadata is recorded as
not available in this local-only pass, not as zero.

## Metadata Rows

| source | citation_count | citation_source | citation_access_date | venue | venue_metric | venue_metric_source | venue_metric_access_date | retraction_metadata | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Arasaratnam--Haykin, "Cubature Kalman Filters" | `not available in P1T local-pass scope` | P1S cached OpenAlex search was noisy/no exact row used | `QUERY_NOT_RUN_P1T` | IEEE Transactions on Automatic Control | `not queried` | `QUERY_NOT_RUN_P1T` | `QUERY_NOT_RUN_P1T` | local/P1S cached check found no signal, but no exact live metadata refresh in P1T | Source support comes from local IEEE PDF, not citation/venue metadata. |
| Girolami--Calderhead, "Riemann manifold Langevin and Hamiltonian Monte Carlo methods" | `not available in P1T local-pass scope` | P1S cached OpenAlex search was noisy/no exact row used | `QUERY_NOT_RUN_P1T` | Journal of the Royal Statistical Society: Series B | `not queried` | `QUERY_NOT_RUN_P1T` | `QUERY_NOT_RUN_P1T` | local/P1S cached check found no signal, but no exact live metadata refresh in P1T | Source support comes from local JRSS B PDF, not citation/venue metadata. |
| Snyder et al., "Obstacles to High-Dimensional Particle Filtering" | 700 | cached OpenAlex exact row `openalex_snyder_obstacles_pf.json` | 2026-05-28 P1S cache, reused without live refresh in P1T | Monthly Weather Review | `not queried` | `QUERY_NOT_RUN_P1T` | `QUERY_NOT_RUN_P1T` | cached exact row had `is_retracted=false` | Count raises coverage priority only; source support comes from local technical text. |
| Bengtsson--Bickel--Li, "Curse-of-Dimensionality Revisited: Collapse of the Particle Filter in Very Large Scale Systems" | `not available in P1T local-pass scope` | `QUERY_NOT_RUN_P1T` | `QUERY_NOT_RUN_P1T` | IMS Collections / Probability and Statistics: Essays in Honor of David A. Freedman | `not queried` | `QUERY_NOT_RUN_P1T` | `QUERY_NOT_RUN_P1T` | local check found no signal; no live metadata refresh in P1T | Source support comes from local IMS PDF, not metadata. |
| Gordon--Salmond--Smith, "Novel Approach to Nonlinear/Non-Gaussian Bayesian State Estimation" | `not available in P1T local-pass scope` | `QUERY_NOT_RUN_P1T` | `QUERY_NOT_RUN_P1T` | IEE Proceedings F: Radar and Signal Processing | `not queried` | `QUERY_NOT_RUN_P1T` | `QUERY_NOT_RUN_P1T` | local check found no signal; no live metadata refresh in P1T | Source support comes from local scan/OCR plus later visual check for exact formulas. |

## What Is Not Concluded

This ledger does not rank sources by truth, quality, or correctness.  It does
not provide venue rankings.  It does not close forward-snowball coverage.  It
only records the limited metadata status of the five P1T sources.
