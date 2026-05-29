# P1T Claim-Support Closure Ledger

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: five user-supplied blocker PDFs in `.local_sources/highdim_nonlinear_filtering/`.

what_is_not_concluded: see section "What Is Not Concluded".

## Purpose

This ledger translates P1T source closure into instructions for the later
paper-first chapter rewrite.  These rows are not chapter prose and not
derivation audits; they identify which future claims now have primary-source
technical anchors.

## Claim Rows

| future_claim | intended_chapter | support_class | checked_anchor_or_blocker | allowed_scope | forbidden_scope | rewrite_instruction |
| --- | --- | --- | --- | --- | --- | --- |
| CKF is a Gaussian-assumed nonlinear filter that approximates the Bayesian moment integrals using a third-degree spherical-radial cubature rule with `2n` equally weighted points. | Ch34 | `PRIMARY_TECHNICAL_SUPPORT` | Arasaratnam--Haykin Sections II--V; spherical rule (28)--(30); radial rule (31)--(33); Propositions 4.1--4.2; Appendix A CKF algorithm. | Explain CKF as a deterministic Gaussian moment filter and local competitor to UKF, QKF, SGQF, and high-degree CKF. | Do not state CKF solves general nonlinear/non-Gaussian filtering or is adequate at NAWM scale. | Add a proposition/proof sketch deriving the cubature point set and the moment update under Gaussian assumptions; cite the exact paper anchors. |
| Square-root CKF propagates covariance factors to improve numerical stability and preserve positive-definite covariance structure in finite precision. | Ch34 | `PRIMARY_TECHNICAL_SUPPORT` | Arasaratnam--Haykin Section VI and Appendix B equations (52)--(63). | Use as the classical square-root motivation next to tensor-network square-root covariance discussion. | Do not infer tensor-network square-root validity from CKF alone. | Present as a finite-dimensional dense-filter stability lesson. |
| RMHMC replaces the constant HMC mass matrix with a position-specific metric and therefore produces a nonseparable Hamiltonian requiring a generalized leapfrog integrator. | Ch36 | `PRIMARY_TECHNICAL_SUPPORT` | Girolami--Calderhead Sections 4--6; Hamiltonian (13); Hamilton equations (14)--(15); generalized leapfrog (16)--(18). | Explain RMHMC as a geometry-aware MCMC substrate and comparator for transport-preconditioned HMC/NeuTra. | Do not claim RMHMC is practical or convergent for BayesFilter nonlinear SSM posterior paths. | Add derivation of the RMHMC Hamiltonian marginalization and state why the metric derivatives are costly. |
| Metric-aware MCMC can be powerful but may be computationally prohibitive when metric tensors and derivatives are dense or state-dependent in high-dimensional latent models. | Ch36/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Girolami--Calderhead Sections 7--10 and discussion, especially stochastic-volatility and log-Gaussian Cox process cost caveats. | Supports industrial-practitioner warning about dense metric tensors and generalized leapfrog fixed-point solves. | Do not generalize to all structured/sparse metrics without separate evidence. | Use as a bridge to transport/TT structure as possible rescue mechanisms. |
| Prior-proposal particle filters can collapse in high dimensions because the normalized importance weights concentrate, and the effective dimension is tied to the variance of the observation log likelihood. | Ch33/Ch35/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Snyder et al. equations (7a)--(11), heuristic formula (19), Gaussian--Gaussian Section 5, conclusion; Bengtsson--Bickel--Li Lemma 3.1 and Propositions 3.2--3.4. | State assumptions: prior proposal, likelihood-weight update, large observation/effective dimension, iid/Gaussian or stated asymptotic regularity. | Do not state that all particle filters fail or that transport/local proposal/localization methods cannot rescue PF. | Write theorem/proposition style exposition with assumptions, then separate Snyder's heuristic `tau^2` discussion from Bengtsson--Bickel--Li formal asymptotics. |
| Resampling alone does not improve a poor posterior approximation produced by collapsed weights. | Ch35/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Snyder et al. introduction and conclusion; Gordon Section 3.3/5 sample-impoverishment caveats. | Use as motivation for better proposals, localization, transport, or structural decomposition. | Do not use this as a theorem about every resampling method in every SMC design. | State as a source-local caution for bootstrap/prior-proposal PF. |
| The original bootstrap particle filter represents the filtering posterior by samples, propagates samples through the transition model, weights by likelihood, and resamples from the resulting discrete distribution. | Ch33/Ch35 | `PRIMARY_TECHNICAL_SUPPORT` | Gordon--Salmond--Smith Sections 2--3; recursive equations (1)--(7); prediction/update/resampling algorithm; Section 3.2 weighted-bootstrap justification. | Supports historical baseline and original bootstrap/SIR algorithm description, with OCR caveat. | Do not use OCR text for exact quotation or theorem-level formula without visual check; do not claim high-dimensional adequacy. | Cite Gordon for historical origin and Arulampalam/Chopin for cleaner modern notation; visually verify exact formulas before final LaTeX. |
| The high-dimensional PF-collapse papers are strong survey context for treating bootstrap/prior-proposal particle filtering as a diagnostic or competitor rather than an unqualified default high-dimensional solution. | Ch37 | `SURVEY_CONTEXT_ONLY` | Snyder conclusion; Bengtsson--Bickel--Li discussion; Gordon/Arulampalam baseline mechanics. | Supports a cautious synthesis recommendation to be justified later by chapter-level argument and project judgment. | Does not prove a theorem, exclude all PF-family methods, or validate any proposed BayesFilter alternative. | In synthesis, write this as a Codex/project inference from multiple checked sources, then separately derive diagnostic gates: ESS/weight concentration, log-likelihood variance, local observation blocks, proposal mismatch, and resampling impoverishment. |

## What Is Not Concluded

These rows do not prove future chapter propositions in BayesFilter notation.
They do not audit algebra, implementation, or numerical evidence.  A later
rewrite must still write assumptions, derivations, and proof sketches, then use
MathDevMCP where feasible.
