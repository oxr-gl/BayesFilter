# Paper-First Scholarship Primary-Source Ledger

Date: 2026-05-28

## Purpose

This ledger records source availability for the high-dimensional nonlinear
filtering paper-first rewrite. It is deliberately a source-control and blocker
ledger, not a literature survey. A paper may drive chapter derivations only
after its technical text has been locally inspected.

Downloaded PDFs and HTML snapshots are stored under
`.local_sources/highdim_nonlinear_filtering/`. That directory is a local
working cache and must not be committed.

## Local MCP Status

ResearchAssistant MCP is read-only and available. On 2026-05-28, Codex queried
the local workspace for the required tensor-train filtering, Zhao--Cui
conditional KR transport, Spantini--Baptista--Marzouk transport filtering,
sparse-grid filtering, transport-map MCMC, deep inverse Rosenblatt TT, and
tensor-substrate papers. The relevant queries returned no local summaries for
the required paper-first pillars. Related local review items visible through
ResearchAssistant were NeuTra, RMHMC, learned HMC, and normalizing flows, all
marked `needs_review`.

MathDevMCP `doctor` reported LaTeXML, Pandoc, Sage, SymPy, and LeanDojo
available; direct Lean version check timed out. MathDevMCP was not used to
audit derivations in P1 because P1 only establishes source readiness.

## Source-Support Classes

- `LOCAL_FULL_TEXT_INDEXED`: technical full text is locally available and
  relevant technical sections/equations/algorithms/theorems have been indexed
  enough to permit detailed reading in a rewrite phase.
- `LOCAL_FULL_TEXT_PENDING_DETAILED_READ`: local full text exists, but the
  technical content has not yet been indexed.
- `LOCAL_HTML_FULL_TEXT_INDEXED`: technical HTML full text is locally available
  and indexed; a PDF may still be unavailable.
- `LOCAL_SUMMARY_ONLY`: local summary exists, but not enough for theorem-level
  chapter support.
- `PAYWALL_OR_ACCESS_BLOCKED`: direct CLI access to full text failed, or only a
  publisher landing page/SPA shell was available.
- `MANUAL_PLACEMENT_NEEDED`: the user should place the PDF manually in the
  local source cache before the paper is used for theorem-level exposition.
- `RETRACTED_OR_QUARANTINED`: the item has been reported as retracted or
  otherwise unsuitable as scholarly support. Do not use it for claims except to
  explain why it is excluded.

`LOCAL_FULL_TEXT_INDEXED` is still not a claim that every proof in the paper has
been verified. It only means the paper is locally available and section/equation
anchors are ready for the paper-first rewrite.

## Required Paper Ledger

| Pillar | Paper | Local artifact or blocker | Current support | Technical anchors indexed for rewrite |
| --- | --- | --- | --- | --- |
| Direct TT nonlinear filtering | Li, Wang, Yau, Zhang, TT method for nonlinear filtering via FKE/DMZ-style PDEs, `https://arxiv.org/abs/1908.04010` | `.local_sources/highdim_nonlinear_filtering/li_wang_yau_zhang_tt_nonlinear_filtering_1908.04010.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Sections 2--6; model equations (1)--(2), DMZ equation (3), operator equation (4), robust transform (5)--(8), TT/QTT definitions (9)--(11), FKE scheme around (12); Propositions 4.1 and 4.3; Algorithms 1--2; convergence section with Lemmas 5.3, 5.5, 5.6 and Theorem 5.7; rank/time Tables 1--5. |
| Direct TT nonlinear filtering | Zhao and Cui, TT sequential state and parameter learning with conditional KR transports, `https://www.jmlr.org/papers/v25/23-0743.html` | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | `LOCAL_FULL_TEXT_INDEXED` | JMLR full text; SSM and posterior equations (1)--(9); Algorithm 1; square-root/conditional KR construction in Section 3; Proposition 2, Proposition 4, Algorithms 2--5; propagation-error Propositions 5--6, Theorems 7--8, Proposition 9, Proposition 11, Corollary 12; Appendix A Lemmas 13--15; Appendix B Kalman posterior densities. |
| Direct TT nonlinear filtering | Functional TT grid filtering for Bayes-optimal continuous-discrete filtering, `https://www.tandfonline.com/doi/full/10.1080/17415977.2020.1862109` | `.local_sources/highdim_nonlinear_filtering/functional_tt_grid_filtering_1862109_bath.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Bath accepted manuscript; continuous-discrete filtering setup; Fokker--Planck/continuity derivation around equations (1)--(7); finite-volume filter and Bayes update discussion; functional TT representation Section 4 with tensor-product grids, TT/MPO operations, discretized Fokker--Planck ODE, normalization/positivity comments, and discussion of QTT/DMZ links. |
| Direct TT nonlinear filtering | Meng, Yau, Zhang, TT nonlinear filtering with correlated noise, `https://arxiv.org/abs/2605.25677` | `.local_sources/highdim_nonlinear_filtering/meng_yau_zhang_tt_correlated_noise_2605.25677.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Sections 2--6 and Appendices; correlated-noise signal/observation model (1), DMZ/Zakai SPDE (2), TT format (3), stochastic integrals (4), Ito--Taylor representation (5), semi-discrete DMZ scheme (6), tensor grid (7)--(8), operators (9), TT approximation conditions (10)--(14), semi-implicit Milstein scheme (15); Algorithm 1; Table 1; Lemmas 4.1--4.4, Theorems 4.3--4.6, Lemmas 5.1--5.6, Theorem 5.7; numerical Table 2 and examples (35)--(36). |
| Tensor-network Kalman | Batselier, Chen, Wong TNKF for lifted Volterra systems, `https://arxiv.org/abs/1610.05434` | `.local_sources/highdim_nonlinear_filtering/batselier_chen_wong_tnkf_1610.05434.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Sections 2--6; tensor-network Kalman equations in Section 3; lifted Volterra/TN state and covariance representation; Lemmas 1--3; complexity table; recursive MIMO Volterra system identification and application sections. |
| Tensor-network Kalman | Tensor-network square-root Kalman filter, `https://arxiv.org/abs/2409.03276` | `.local_sources/highdim_nonlinear_filtering/tensor_network_square_root_kalman_2409.03276.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Sections 2--7; problem formulation and tensor-network background; tensor-networked SRKF Section 4; PSD-preserving square-root motivation and TNKF rounding failure warning; Algorithm 1 online GP regression as SRKF; Algorithm 2 SVD-based QR covariance update; Lemmas 5 and 7; complexity discussion. |
| Tensor-network Kalman | Low-rank tensor UKF tractography, `https://www.sciencedirect.com/science/article/pii/S1053811923001507` | User placed `.local_sources/highdim_nonlinear_filtering/Spatially regularized low-rank tensor approximation for accurate and fast tractography Gruen(23).pdf`; `pdfinfo` reports NeuroImage 271 (2023) 120004, DOI `10.1016/j.neuroimage.2023.120004`, 10 pages. | `LOCAL_FULL_TEXT_INDEXED` | P1R indexed Sections 1--5; low-rank tensor approximation equations (1)--(7), spatial weights (8)--(11), UKF state and update equations (12)--(20), HCP/ISMRM/tumor experiments, Table 1, and references. Supports a domain-specific observation-compression example only, not general high-dimensional filtering validity. |
| Transport-map filtering | Spantini, Baptista, Marzouk nonlinear ensemble filtering, `https://epubs.siam.org/doi/10.1137/20M1312204` | `.local_sources/highdim_nonlinear_filtering/spantini_baptista_marzouk_transport_filtering_1907.00389.pdf` | `LOCAL_FULL_TEXT_INDEXED` | arXiv/SIAM preprint; Sections 2--5; nonlinear filtering background; stochastic and deterministic map filters; Algorithm 1 triangular-map inversion; Algorithms 2--3 analysis steps; Appendix A monotone triangular map parameterization; Appendix B conditionally independent/localized deterministic map filter; Appendices C--F diagnostics and experiments. |
| Transport-map filtering | Ensemble transport smoothing, Part I, `https://www.sciencedirect.com/science/article/pii/S2590055223000124` | `.local_sources/highdim_nonlinear_filtering/ensemble_transport_smoothing_part_i_2210.17000.pdf` | `LOCAL_FULL_TEXT_INDEXED` | arXiv preprint; Sections 2--5; triangular transport, sparsity, and conditional sampling; ensemble transport smoother objectives; Proposition 1; Appendix A objective derivation; Appendix B Gaussian conditioning; Algorithms 1--4 in Appendix C; Appendix D proof of Proposition 1; Appendix E sparse filtering updates. |
| Transport-map filtering | Decomposable transports for Bayesian filtering/smoothing, `https://approximateinference.org/2016/accepted/SpantiniEtAl2016.pdf` | User reported this paper as retracted on 2026-05-28. Direct conference URL also timed out after 120 seconds with 0 bytes; alternate URL returned 404. | `RETRACTED_OR_QUARANTINED` | Do not request manual placement and do not use this paper as theorem-level support. Decomposable-transport discussion should instead rely on checked, non-quarantined sources such as Spantini--Baptista--Marzouk nonlinear ensemble filtering, Ensemble Transport Smoothing Part I, and primary transport-map theory where available. |
| Sparse/high-order | High-degree cubature Kalman filter, `https://www.sciencedirect.com/science/article/pii/S000510981200550X` | User placed `.local_sources/highdim_nonlinear_filtering/High-degree cubature Kalman filter Jia(13).pdf`; `pdfinfo` reports Automatica 49 (2013) 510--518, DOI `10.1016/j.automatica.2012.11.014`, 9 pages. | `LOCAL_FULL_TEXT_INDEXED` | P1R indexed Sections 1--5; Gaussian approximation filter equations (1)--(15), cubature definition (16), spherical--radial construction (17)--(21), Definition 3.1, Theorem 3.1, Proposition 3.1, third/fifth-degree rules including (40)--(46), Proposition 3.2, Tables 1--3, and references. Supports high-degree CKF rule/exactness and point-growth discussion within the paper's Gaussian-additive-noise setting. |
| Sparse/high-order | Sparse-grid quadrature nonlinear filtering, `https://www.sciencedirect.com/science/article/pii/S0005109811005541` | User placed `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf`; `pdfinfo` reports Automatica 48 (2012) 327--341, DOI `10.1016/j.automatica.2011.08.057`, 15 pages. | `LOCAL_FULL_TEXT_INDEXED` | P1R indexed Sections 1--5 and Appendix; Bayesian/Gaussian filtering equations (1)--(25), Smolyak sparse-grid rule (26)--(29), Theorem 3.1, Algorithm 1, Theorem 3.2 showing UKF as level-2 SGQF, Proposition 3.1 point-growth result, Proposition 3.2 nesting result, orbit-estimation examples, Appendix formulas (47)--(52), and references. Supports SGQF construction, UKF-subset claim, and polynomial point-growth claim within the paper's assumptions. |
| Sparse/high-order | Adaptive sparse-grid Gauss-Hermite filtering, `https://www.sciencedirect.com/science/article/pii/S0377042718301742` | `.local_sources/highdim_nonlinear_filtering/adaptive_sparse_grid_gauss_hermite_1803.09272.pdf` | `LOCAL_FULL_TEXT_INDEXED` | arXiv preprint; Sections 2--5; sparse-grid Gauss--Hermite filter, adaptive index sets, forward/backward/admissible indices, local and global error indicators, tolerance and error-weighting parameters, multivariate integral pseudo-algorithm in Section 3.2, examples and Tables 1--4. |
| HMC/transport substrate | Transport-map accelerated MCMC, `https://epubs.siam.org/doi/10.1137/17M1134640` | `.local_sources/highdim_nonlinear_filtering/transport_map_accelerated_mcmc_1412.5492.pdf` | `LOCAL_FULL_TEXT_INDEXED` | arXiv/SIAM preprint; Sections 2--7; map-induced proposal and transformed target; optimization objectives around equations (7)--(8); adaptive map construction; Algorithm 1; convergence analysis Section 5; numerical examples and appendices. |
| HMC/transport substrate | NeuTra HMC, `https://arxiv.org/abs/1903.03704` | `.local_sources/highdim_nonlinear_filtering/neutra_hmc_1903.03704.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Sections 1--4; Neural Transport MCMC Section 2; transformed target and Jacobian discussion; relationship to RMHMC; NeuTra HMC trajectory comparison; experiments Section 4. The source supports diagnostic/acceleration framing only, not BayesFilter HMC convergence. |
| HMC/transport substrate | Deep inverse Rosenblatt transports using tensor trains, `https://arxiv.org/abs/2007.06968` | `.local_sources/highdim_nonlinear_filtering/deep_inverse_rosenblatt_tt_2007.06968.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Sections 2--7 and appendices; Propositions 1--7, Lemmas 1--2, Theorems 1, 3, and 4; squared inverse Rosenblatt transport, DIRT construction, debiasing; Algorithms 1--2 for IRT-MCMC/IS and Algorithms 3--4 for MaxVol/TT-cross. |
| Tensor substrate | TT sampling of multivariate densities, `https://link.springer.com/article/10.1007/s11222-019-09910-z` | `.local_sources/highdim_nonlinear_filtering/tt_sampling_multivariate_densities_springer_09910z.pdf`; HTML snapshot also cached. | `LOCAL_FULL_TEXT_INDEXED` | Springer open PDF/HTML; TT-cross Algorithm 1; conditional-density sampler Algorithm 2; Lemmas 1--2 for rejection/asymptotic variance framing; Sections 4--5 on TT-CD, TT-MH, TT-qIW, control variates, examples, ranks, IACT, and Tables 1--4. |
| Tensor substrate | TT rank bounds for Gaussian densities, `https://arxiv.org/abs/2001.08187` | `.local_sources/highdim_nonlinear_filtering/tt_rank_bounds_gaussian_2001.08187.pdf` | `LOCAL_FULL_TEXT_INDEXED` | Sections 2--5; low-rank tensor preliminaries; Theorems 2.3, 2.4, 2.6, 2.7, 2.8; Gaussian rank-bound Theorem 3.1; Lemmas 3.3, 3.5, 3.6, 3.7; numerical rank-bound tests; Bayesian filtering application Section 5. |
| Tensor substrate | Fokker-Planck by TT cross approximation, `https://pmc.ncbi.nlm.nih.gov/articles/PMC8366026/` | `.local_sources/highdim_nonlinear_filtering/fokker_planck_tt_cross_frontiers.pdf`; PMC HTML also cached. Direct PMC PDF endpoint served a browser proof-of-work page, recorded as `.local_sources/highdim_nonlinear_filtering/fokker_planck_tt_cross_pmc8366026_pow_html.html`. | `LOCAL_FULL_TEXT_INDEXED` | Frontiers PDF and PMC HTML; multidimensional Fokker--Planck equation and SDE formulation; splitting into diffusion and convection; TT format and cross approximation; Algorithms 1--5; detailed algorithm Section 4; examples including OUP and dumbbell; effective TT-rank discussion and code repository note. |
| Tensor substrate | Fast high-dimensional integration using tensor networks, `https://arxiv.org/abs/2202.09780` | `.local_sources/highdim_nonlinear_filtering/tensor_network_highdim_integration_2202.09780.pdf` | `LOCAL_FULL_TEXT_INDEXED` | arXiv preprint; tensor-network integration equations (1)--(2); TT-X interpolation equations (3)--(9); node-selection and complexity discussion; Fourier-TT construction; convergence/time Tables 1--2. Supports quadrature-replacement intuition, not filtering-specific correctness. |

## Manual Placement Blockers

P1R resolved the three earlier manual-placement blockers.  The low-rank tensor
UKF tractography paper, the high-degree cubature Kalman filter paper, and the
sparse-grid quadrature nonlinear filtering paper are now locally present and
indexed.  No remaining non-quarantined seed paper in the paper-first master
program is blocked solely by missing local full text.

## Quarantined Sources

- Decomposable transports for Bayesian filtering/smoothing, Spantini et al.
  2016: user reported this paper as retracted on 2026-05-28. It is removed from
  the manual-placement request list and must not be used as scholarly support.
  Later checked transport-map filtering and smoothing papers may be used for
  decomposable-map exposition when their own text supports the claim.

## Execution Decision

`SOURCE_READY_FOR_PAPER_FIRST_REWRITE_WITH_SCHOLARLY_AUDIT_BLOCKERS`.

The P1R pass confirms that the three previously missing PDFs are now locally
available and technically indexed.  Chapter rewrite phases may proceed for
material grounded in non-quarantined papers marked `LOCAL_FULL_TEXT_INDEXED` or
`LOCAL_HTML_FULL_TEXT_INDEXED`, subject to the stricter P1R scholarly-audit
ledgers.  The decomposable-transport workshop paper remains quarantined and
cannot support any claim.

## Non-Implications

This ledger does not validate any tensor-train, tensor-network,
transport-map, sparse-grid, HMC, NeuTra, or BayesFilter/NAWM method. It only
records local source availability and technical anchors for subsequent
paper-first derivation work.
