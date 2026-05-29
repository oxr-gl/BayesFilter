# P1 Primary-Source Intake Result

Date: 2026-05-28

## Scope

Lane: high-dimensional nonlinear filtering paper-first scholarship.

This result records the approved source-intake pass for the paper-first rewrite.
It does not execute chapter rewrites, does not validate mathematical claims,
and does not commit downloaded papers.

## User Approval

The user explicitly approved automatic download and inspection of all paper URLs
listed for the high-dimensional nonlinear filtering paper-first rewrite. Codex
was instructed to use public/direct URLs where available, store PDFs or HTML
snapshots under `.local_sources/highdim_nonlinear_filtering/`, avoid paywall
bypass, and report manual-placement blockers where CLI institutional access was
unavailable.

## Codex Inspection

Codex inspected:

- the paper-first master program and P1 source-intake subplan;
- the existing primary-source ledger;
- local source cache contents under `.local_sources/highdim_nonlinear_filtering/`;
- `docs/references.bib`, `docs/source_map.yml`, and active high-dimensional
  chapter targets for lane context;
- local git status to avoid touching unrelated DPF/student/controlled-baseline
  dirty files.

## ResearchAssistant MCP Use

ResearchAssistant MCP was queried in read-only mode. It returned no local paper
summaries for the direct tensor-train filtering, Zhao--Cui conditional KR
transport, Spantini--Baptista--Marzouk transport filtering, sparse-grid
filtering, transport-map MCMC, or tensor-substrate pillars. This confirms that
chapter mathematics must be sourced from the downloaded primary texts rather
than local summaries.

## MathDevMCP Use

MathDevMCP `doctor` was run. It reported LaTeXML, Pandoc, Sage, SymPy, and
LeanDojo available, with direct Lean version check timing out. No derivation
audit was run in P1 because this phase only records source availability and
technical anchors.

## Downloads And Cache

Successful usable local artifacts include:

- `li_wang_yau_zhang_tt_nonlinear_filtering_1908.04010.pdf`
- `zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`
- `functional_tt_grid_filtering_1862109_bath.pdf`
- `meng_yau_zhang_tt_correlated_noise_2605.25677.pdf`
- `batselier_chen_wong_tnkf_1610.05434.pdf`
- `tensor_network_square_root_kalman_2409.03276.pdf`
- `spantini_baptista_marzouk_transport_filtering_1907.00389.pdf`
- `ensemble_transport_smoothing_part_i_2210.17000.pdf`
- `adaptive_sparse_grid_gauss_hermite_1803.09272.pdf`
- `transport_map_accelerated_mcmc_1412.5492.pdf`
- `neutra_hmc_1903.03704.pdf`
- `deep_inverse_rosenblatt_tt_2007.06968.pdf`
- `tt_sampling_multivariate_densities_springer_09910z.pdf`
- `tt_rank_bounds_gaussian_2001.08187.pdf`
- `fokker_planck_tt_cross_frontiers.pdf`
- `tensor_network_highdim_integration_2202.09780.pdf`

HTML snapshots were also cached for the Springer TT-sampling article and the
PMC Fokker--Planck article. The direct PMC PDF endpoint served a browser
proof-of-work page, but the Frontiers PDF succeeded.

## Access Blockers

The following table records the original P1 access blockers.  P1R later
resolved three of them by indexing user-placed PDFs; see the correction below.

| Paper | Attempted route | Result | Required action |
| --- | --- | --- | --- |
| Low-rank tensor UKF tractography, ScienceDirect `S1053811923001507` | ScienceDirect direct PDF endpoint; University of Bonn public URL | ScienceDirect returned 403; Bonn URL returned only a JavaScript SPA shell | Place the PDF manually in `.local_sources/highdim_nonlinear_filtering/` and rerun P1 indexing. |
| Decomposable transports for Bayesian filtering/smoothing, Spantini et al. 2016 | approximateinference workshop PDF URL and alternate URL | primary URL timed out after 120 seconds with 0 bytes; alternate URL returned 404; user reported the paper as retracted on 2026-05-28 | Quarantine. Do not request manual placement and do not use as scholarly support. |
| High-degree cubature Kalman filter, ScienceDirect `S000510981200550X` | ScienceDirect direct PDF endpoint | 403 | Place the PDF manually before deriving the rule or exactness claims. |
| Sparse-grid quadrature nonlinear filtering, ScienceDirect `S0005109811005541` | ScienceDirect direct PDF endpoint | 403 | Place the PDF manually before deriving the Smolyak filtering method. |

No paywall bypass was attempted.

## P1R Source-Status Correction

On 2026-05-28, the user placed three previously blocked PDFs in
`.local_sources/highdim_nonlinear_filtering/`.  P1R verified them with
`pdfinfo` and `pdftotext` and indexed their technical anchors:

- `High-degree cubature Kalman filter Jia(13).pdf`: Automatica 49 (2013)
  510--518, DOI `10.1016/j.automatica.2012.11.014`, 9 pages.
- `Sparse-grid quadrature nonlinear filtering Jia(11).pdf`: Automatica 48
  (2012) 327--341, DOI `10.1016/j.automatica.2011.08.057`, 15 pages.
- `Spatially regularized low-rank tensor approximation for accurate and fast tractography Gruen(23).pdf`:
  NeuroImage 271 (2023) 120004, DOI `10.1016/j.neuroimage.2023.120004`,
  10 pages.

These three papers are no longer `MANUAL_PLACEMENT_NEEDED`; they are
`LOCAL_FULL_TEXT_INDEXED` for P1R.  The decomposable-transport workshop paper
remains `RETRACTED_OR_QUARANTINED` and cannot support claims.

## Post-Approval Retry Validation

After the user explicitly approved public URL intake, Codex performed one
additional bounded retry pass on the four blocked public routes. The retry used
`curl -L --fail --show-error --max-time 60 -A "Mozilla/5.0"` and wrote only
under `.local_sources/highdim_nonlinear_filtering/`.

Retry results:

- Low-rank tensor UKF tractography, ScienceDirect `S1053811923001507`: 403.
- Spantini et al. 2016 decomposable transports workshop PDF: timed out after
  60 seconds with 0 bytes received; then user reported the paper as retracted,
  so it is quarantined rather than treated as a manual-placement blocker.
- High-degree cubature Kalman filter, ScienceDirect `S000510981200550X`: 403.
- Sparse-grid quadrature nonlinear filtering, ScienceDirect
  `S0005109811005541`: 403.

This retry changed the access decision for the decomposable-transports workshop
item after the user's retraction notice: it is now `RETRACTED_OR_QUARANTINED`.
The remaining three inaccessible publisher papers remain
`MANUAL_PLACEMENT_NEEDED`, and no theorem-level chapter claims should cite them
as read until a usable full text is placed locally and indexed.

## Technical Indexing

Codex used `pdftotext`, `rg`, `file`, and `pdfinfo`-style checks to confirm
usable PDFs and identify technical anchors. The updated primary-source ledger
records section, equation, algorithm, proposition, theorem, lemma, appendix, and
table anchors where visible.

This technical indexing is a readiness step for detailed scholarly reading. It
is not a substitute for the later paper-by-paper derivations and proof sketches.

## Execution Decision

`SOURCE_READY_FOR_PAPER_FIRST_REWRITE_WITH_SCHOLARLY_AUDIT_BLOCKERS`.

P2--P8 may proceed only for material grounded in papers marked
`LOCAL_FULL_TEXT_INDEXED` in the ledger and in the P1R source-support ledger.
Any section that would have depended on the retracted decomposable-transports
workshop paper must replace it with checked, non-quarantined transport-map
sources.  Citation/venue metadata and snowballing blockers remain separate
P1R scholarly-audit limitations.

## Validation

Planned validation for this P1 update:

- `git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- verify `.local_sources/` is untracked and unstaged;
- verify only allowed high-dimensional paper-first planning/result notes were
  modified.

## Non-Implications

This result does not validate tensor-train filtering, tensor-network Kalman
filtering, transport-map filtering/smoothing, sparse-grid filtering, NeuTra,
HMC convergence, tensor-method robustness, NAWM readiness, or BayesFilter
production readiness.
