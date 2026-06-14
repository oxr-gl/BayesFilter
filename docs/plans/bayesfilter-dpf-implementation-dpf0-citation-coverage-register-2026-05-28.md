# DPF0 Citation Coverage Register

## Status

DPF0 execution artifact.  This register answers DPF0A-PATCH-001 by checking the
implementation-relevant DPF citation surface before implementation obligations
are extracted.  It does not edit `docs/references.bib`, `docs/source_map.yml`,
monograph chapters, production code, or vendored student files.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| Stale context | pass | DPF0-A result says `DPF0 may start: yes`; master and DPF0 plan were re-read on 2026-05-28. |
| Wrong baseline | pass | The authority baseline is the DPF monograph plus bibliography/source-map support, not student reports. |
| Proxy overclaim | pass | Student and controlled metrics remain explanatory only. |
| Missing stop conditions | pass | Missing reviewed paper summaries or missing references become review/defer items, not implementation authority. |
| Hidden production/monograph drift | pass | This phase writes plan artifacts only. |
| Vendored-code contamination | pass | Vendored student files are not edited, executed, or copied. |
| High-dimensional-lane contamination | pass | The separate high-dimensional nonlinear filtering lane is not used. |
| Artifact fitness | pass | The register records include/defer/exclude decisions that feed the DPF0 claim ledger. |

## Coverage Decisions

| Topic | Current BayesFilter support | Student/comparison pressure | DPF0 decision | Consequence |
| --- | --- | --- | --- | --- |
| Classical SMC/bootstrap PF | `docs/chapters/ch19_particle_filters.tex`; `gordon1993novel`, `doucet2001sequential`, `andrieu2010particle`; IE3 LGSSM evidence. | Student reports use PF/BPF as comparison rows. | include | DPF1 must implement classical bootstrap/SIR semantics before relaxed components. |
| Pseudo-marginal value-side use | `andrieu2009pseudo`, `andrieu2010particle`; `ch19_particle_filters.tex`; `ch19e`. | Student docs mention PMMH/PHMC surfaces. | include as boundary only | DPF4 may cite value-side distinction but no smooth HMC target claim follows. |
| EDH/LEDH particle flow | `daumhuang2008`; `ch19b`; `ch19c`; IE4 affine-flow evidence. | Student EDH/PFPF panels are comparison-only. | include with affine/nonlinear separation | DPF3 must specify proposal correction and affine parity before nonlinear claims. |
| Invertible PF-PF proposal correction | `li2017particle`; `ch19c`; IE4 PF-PF algebra parity. | Student EDH/PFPF rows nominate implementation surfaces. | include | DPF3 must preserve target/proposal density and Jacobian obligations. |
| Differentiable soft resampling | `zhumurphyjonschkowski2020`; `ch32_diff_resampling_neural_ot`; IE5 soft-resampling evidence. | Student README wording around "unbiasedness" is too broad. | include with wording guard | DPF2 must label affine/mean-preserving versus nonlinear-biased behavior. |
| Entropic OT/Sinkhorn resampling | `corenflos2021differentiable`, `villani2003topics`, `cuturi2013sinkhorn`, `peyre2019computational`, `schmitzer2019stabilized`; `ch32`; IE5 Sinkhorn evidence. | Student amortized-OT docs compare against Sinkhorn teachers. | include as relaxed component | DPF2 must record epsilon, budget, residuals, stabilization, and gradient path. |
| Learned/amortized OT | `zaheer2017deep`, `lee2019set`; `ch19d`; IE6 deferred no approved teacher/student artifact. | Student docs report speedups and heldout MSE. | defer | Needs provenance-bearing teacher/student component spec; no posterior or HMC claim. |
| Particle filter networks / differentiable learned PF | `jonschkowski2018differentiable`, `karkus2018particle` are present in `docs/references.bib`. | Student docs cite neural resampling and learned components. | include as literature watch, not obligation | DPF2/DPF4 should not implement neural PF/resampling until component objective and evidence are specified. |
| Stochastic flow / high-dimensional PFF | `hu2021particle` and student usability gates identify caution surfaces. | Student reports mark stochastic flow/PFF paths as needing clean-room specs or debug gates. | defer/exclude by default | DPF3 should keep stochastic flow out unless a clean-room spec is approved; kernel PFF remains excluded pending debug. |
| DPF-HMC target suitability | `neal2011mcmc`, `betancourt2017conceptual`, `andrieu2009pseudo`, `andrieu2010particle`; `ch19e`; IE7 fixed-scalar evidence. | Student notebook language says "validated DPF-HMC pipeline." | include as boundary only | DPF4 must classify objectives and ban HMC/posterior claims without target and sampler evidence. |

## Source-Support Ceiling

The local evidence program records a `bibliography_spine_only` source-support
ceiling unless a row explicitly has stronger reviewed-source support.  DPF0
therefore extracts implementation obligations from monograph equations,
BayesFilter derivations, and clean-room evidence reports, while treating broader
student-cited method families as include/defer/exclude decisions.

## Open Citation Items

| Item | Status | Required future action |
| --- | --- | --- |
| Learned/amortized OT implementation papers beyond the current set-operator spine | deferred | DPF2 or a future DPF2-A must review the exact teacher/student paper sections before any learned-OT component is implemented. |
| Neural resampling / particle-network objectives | deferred | DPF2/DPF4 must specify objective semantics and teacher/source support before code. |
| Stochastic flow and kernel PFF literature | deferred/excluded | DPF3 must require clean-room target/proposal/Jacobian specs and a bounded debug gate. |
| HMC with relaxed or learned DPF likelihoods | boundary only | DPF4/DPF5 must require named scalar, same-scalar gradient, posterior/reference, and sampler diagnostics before any HMC claim. |

## DPF0 Consequence

No citation gap blocks DPF0 claim extraction.  The gaps are not mathematical
errors in the monograph; they are implementation-scope controls for later
phases.
