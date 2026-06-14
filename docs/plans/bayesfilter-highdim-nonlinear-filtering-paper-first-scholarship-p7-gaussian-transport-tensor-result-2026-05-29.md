# P7 Gaussian/Transport/Tensor Self-Contained Gradient Result

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P7 plan, P6 result, P1R/P1S/P1T/P1U/P2R/P3/P4/P5/P6 ledgers,
`ch18_svd_sigma_point.tex`, `ch34`, `ch35`, `ch36`, `ch37`,
`docs/references.bib`, `docs/source_map.yml`, `docs/main.tex`,
`docs/main.log`, `docs/main.pdf`, Claude review outputs, MathDevMCP
diagnostics, and the scholarly literature audit policy.

what_is_not_concluded: This result does not conclude production readiness,
NAWM readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, GPU/XLA readiness, default readiness, exhaustive
literature coverage, or machine-certified proof validity.

## Decision

`READY_FOR_MIXED_PANEL_REVIEW_WITH_LAYOUT_WARNINGS_AND_SCOPE_LIMITS`.

## Codex Inspection

Codex inspected:

- the P7 plan;
- the scholarly literature audit policy and skill;
- the P6 result and prior high-dimensional nonlinear filtering artifacts;
- current `ch34`, `ch35`, and coordination points in `ch36`/`ch37`;
- `ch18_svd_sigma_point.tex` as the local gradient-derivation template;
- `docs/references.bib`, `docs/source_map.yml`, `docs/main.log`, and the dirty
  worktree.

## Execution Summary

P7 expanded `ch34` and `ch35` from compact survey chapters into method-local,
reader-first derivation chapters.

`ch34` now teaches:

- Gaussian projection as affine moment projection;
- EKF, IEKF, and second-order EKF as derivative filters;
- deterministic Gaussian quadrature as the common object behind UKF, CKF,
  high-degree CKF, tensor-product GHQ, and sparse-grid GHQ/SGQF;
- high-degree CKF before synthesis use;
- tensor-product GHQ before sparse-grid use;
- sparse-grid GHQ/SGQF and adaptive sparse-grid filters as source-local
  constructions rather than ungrounded acronym references;
- the approximate Gaussian innovation likelihood and score needed before HMC.

After Claude execution review iteration 1, P7 also repaired:

- sparse-grid HMC label consistency by separating nonadaptive fixed rules,
  frozen adaptive branches, and active adaptive point changes;
- high-degree CKF exposition by adding how the standardized point family
  changes relative to CKF;
- TT/PDE HMC language by demoting it to diagnostic-only until a concrete scalar
  and differentiable branch are instantiated.

`ch35` now teaches:

- empirical particle measures and SIR/bootstrap mechanics;
- log-weight variance and collapse;
- guided proposal correction;
- transport maps as change-of-variables objects;
- triangular and ensemble transport filters;
- TT density/PDE filters;
- TT sequential learning and conditional KR transport bridge;
- tensor-network Kalman and square-root covariance caution;
- HMC boundary labels for resampling, transport Jacobians, TT ranks/pivots, and
  TN covariance branches.

After Claude execution review iteration 1, broad transport/TT citations in
`ch35` were tightened to named P1R/P1U checked anchors, such as Parno--Marzouk
Sections 2--3 and Algorithm 1, Ramgraber Sections 2--3 and Proposition 1,
Li et al. Propositions/Algorithms/Lemmas/Theorem anchors, Fox equations
(1)--(7), Meng equations/Algorithm/Theorems, Zhao--Cui equations/Algorithms/
Propositions/Theorems/Corollary, and Cui--Dolgov propositions/theorems/
algorithms.  Papamakarios remains context-only.

Narrow coordination edits:

- `ch36` references the concrete P7 Gaussian/quadrature likelihood score and
  records why adaptive branches are not smooth HMC gradients.
- `ch37` imports approximate-score parity and HMC-admissibility labels into the
  synthesis table.

## Approximate-Likelihood Gradient Summary

For a fixed deterministic Gaussian rule,
\[
  \chi_t^{(r)}=m_t^-+C_t^-\xi^{(r)},\qquad
  z_t^{(r)}=h_\theta(\chi_t^{(r)}),
\]
P7 defines
\[
  \widehat\ell_t
  =
  -\frac12\{\log\det S_t+v_t^\top S_t^{-1}v_t+n_y\log(2\pi)\}.
\]
It derives \(\dot\chi\), \(\dot z\), \(\dot{\bar z}\), \(\dot S\), and
\(\dot v\), then proves the solve-form score
\[
  \partial_i\widehat\ell_t
  =
  -\frac12
  \left[
    \tr(S_t^{-1}\dot S_t^{(i)})
    +2\dot v_t^{(i)\top}w_t
    -w_t^\top\dot S_t^{(i)}w_t
  \right],
  \qquad S_tw_t=v_t.
\]
This supports HMC only for the declared approximate target and only under the
fixed smooth branch assumptions stated in `ch34`.

## Source Anchors

P7 uses citation anchors at the point of technical use:

- Julier--Uhlmann for UT/UKF construction;
- Arasaratnam--Haykin for CKF/square-root CKF construction;
- Jia 2012 for SGQF;
- Jia 2013 for high-degree CKF;
- Singh et al. 2018 for adaptive sparse-grid GHQ filtering;
- Gordon et al. and Arulampalam et al. for particle/SIR mechanics;
- Bengtsson et al. and Snyder et al. for particle collapse;
- Parno--Marzouk and Papamakarios et al. for transport/flow correction context;
- Rosenblatt and Spantini--Baptista--Marzouk 2022 for triangular/ensemble
  transport filtering;
- Oseledets 2011 and Oseledets--Tyrtyshnikov 2010 for TT and TT-cross;
- Li et al., Fox et al., Zhao--Cui, Cui--Dolgov, Batselier et al., and
  Menzen et al. for TT/TN filtering and transport/covariance contexts.

Quarantined Spantini 2016 is not used as support.

## Review And Validation Status

Claude plan review: `ACCEPT` on iteration 1.

Claude execution review iteration 1: `REJECT`.  Codex agreed with the major
repairable findings and patched sparse-grid labels, TT/PDE HMC demotion,
citation-specificity, high-degree CKF construction, and review/result ledger
state.

Claude execution review iteration 2: `ACCEPT`.  Claude accepted the repaired
execution artifact, with residual limit that PDF validation was still pending.

MathDevMCP: narrow algebra checks performed; broad chapter certification not
claimed.

PDF validation: `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error
docs/main.tex` succeeded and produced `docs/main.pdf` with 275 pages.  The log
scan found no undefined citation, undefined reference, or rerun blockers.
`pdftotext` confirmed the P7 section markers for high-degree CKF,
tensor-product Gauss--Hermite, sparse-grid Gauss--Hermite, approximate
Gaussian innovation likelihood, transport maps, TT sequential learning, and
tensor-network Kalman/square-root caution.

Layout status: `docs/main.log` still contains many underfull/overfull box
warnings, including dense-table warnings in the P7 block and earlier chapters.
These are recorded as editorial/layout warnings, not citation/reference,
source-support, or PDF-build blockers.

## Residual Risks

- The chapters are more self-contained but still not textbook-length lecture
  notes.
- Source support remains bounded by prior P1--P6 ledgers and P7 checked anchors;
  P7 did not perform a new network snowball pass.
- HMC labels are admissibility gates for approximate scalars, not convergence
  guarantees.
- Tensor and sparse-grid branch smoothness remains a method-specific
  implementation obligation.
- Dense tables still need a later layout pass if the printed PDF is the panel
  artifact.

## Final Probability Estimate

Codex estimate after P7: `0.63--0.72` for a skeptical mixed numerical
former-academic panel accepting the high-dimensional nonlinear filtering block
as a serious scholarly/industrial monograph artifact, subject to the residual
layout and scope limits above.  This estimate is higher than P6 because `ch34`
and `ch35` now teach the previously compressed method families and provide an
explicit approximate-likelihood gradient contract.  It is not higher because
the block remains dense, broad derivations are still human-reviewed rather than
machine-certified, and TT/transport/HMC remain conditional research-program
components rather than validated industrial defaults.
