# P3 Industrial Defect Synthesis Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R source-local literature base,
`docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`,
`docs/references.bib`, and `.local_sources/highdim_nonlinear_filtering/`.

what_is_not_concluded: This ledger does not conclude NAWM readiness,
production readiness, posterior accuracy, HMC convergence, tensor-method
validation, transport-method validation, GPU/XLA readiness, machine-certified
proof validity, or exhaustive literature completeness.

## Evidence Contract

Question: Does the rewritten synthesis chapter address the eight industrial
defect and synthesis gaps with source-grounded mathematical claims rather than
handwaving?

Comparator: The P2R chapter block, which passed academic review but still
contained compact proof sketches, diagnostic-only MathDevMCP status, layout
warnings, and insufficient industrial defect synthesis.

Primary pass criterion: Each of the eight requested blocks is represented by a
chapter section, equation/proposition/algorithm/table, source family, explicit
mitigation logic, and residual non-claim.

Veto diagnostics:

- unsupported theorem-level claim from abstracts, metadata, citation counts, or
  venue rank;
- hidden use of the quarantined Spantini et al. 2016 decomposable-transport
  workshop paper;
- production/NAWM/HMC-convergence/tensor-validation/GPU-readiness overclaim;
- missing same-scalar target boundary for HMC;
- performance comparison before mathematical validity gates;
- PDF build/reference failure for the rewritten chapter.

Explanatory diagnostics: Claude reviewer comments, MathDevMCP diagnostic
status, LaTeX overfull/underfull warnings, and source-risk items that are
explicitly labelled rather than used as support.

## Eight-Block Coverage Ledger

| Block | Chapter anchor | Derivation/proposition object | Source support | Status |
|---|---|---|---|---|
| 1. Full derivation gap | Secs. `sec:bf-hd-defect-particles`--`sec:bf-hd-defect-hmc` | `prop:bf-hd-particle-collapse-calculus`, `prop:bf-hd-local-cubature-diagnostic`, `prop:bf-hd-tensor-viability`, `prop:bf-hd-transport-auditability`, `prop:bf-hd-hmc-downstream` | Source-local particle, cubature, TT/TN, transport, and HMC families | Improved but still not paper-length; marked as derivation/proof sketches where scope is heuristic or compositional. |
| 2. MathDevMCP certification gap | P3 result note plus this ledger | New label audits requested for P3 propositions | MathDevMCP diagnostics only | Must be recorded as human-reviewed unless tool certifies. |
| 3. Exposition depth gap | Entire rewritten `ch37` | Defect-first exposition and worked equations | P1R--P2R ledgers and local source cache | Expanded relative to P2R; still compact relative to a standalone professor-proof monograph volume. |
| 4. PDF/layout gap | PDF validation section of result | LaTeX build, log scan, `pdftotext` check | Repo LaTeX build artifacts | Layout warnings may remain; citation/reference blockers must not. |
| 5. Industrial synthesis propositions | Sec. `sec:bf-hd-industrial-propositions` | `prop:bf-hd-block-scaffold-first`, `prop:bf-hd-useful-not-novel`, `alg:bf-hd-defect-synthesis` | Gaussian filtering, sparse-grid/cubature, TT/TN, transport, HMC source families | Main synthesis is explicit and non-novel by design. |
| 6. Defect derivations | Secs. `sec:bf-hd-defect-particles`, `sec:bf-hd-defect-gaussian`, `sec:bf-hd-defect-tensor`, `sec:bf-hd-defect-transport`, `sec:bf-hd-defect-hmc` | Eq. `eq:bf-hd-synth-ess`, `eq:bf-hd-synth-logweight`, `eq:bf-hd-synth-quadrature-remainder`, `eq:bf-hd-synth-tt-defects`, `eq:bf-hd-synth-tn-indefinite`, `eq:bf-hd-synth-transport-density`, `eq:bf-hd-synth-hmc-target` | Bengtsson/Snyder; Julier/Arasaratnam/Jia/Singh; Oseledets/Li/Fox/Zhao/Meng/Batselier/Menzen; Rosenblatt/Reich/Spantini/Ramgraber/Parno/Hoffman/Cui; Neal/Hoffman/Gelman/Betancourt/Girolami | Covered as monograph derivations and counterexample-style defect equations. |
| 7. Mitigation derivations | Each defect section and numerical table | Structural mitigations tied to diagnostic variables | Same as above plus pseudo-marginal/PMCMC sources for likelihood-estimator boundary | Covered as conditional contracts, not validation. |
| 8. Performance model gap | Sec. `sec:bf-hd-performance-models` | Cost table with killing variables | Filter method papers plus standard algebraic cost reasoning | Covered as scaling heuristics; not benchmark evidence. |

## Claim-Support Ledger

| Claim | Support class | Checked anchors | Allowed conclusion | Forbidden conclusion |
|---|---|---|---|---|
| Particle filters collapse exponentially when log-weight variance grows with effective dimension. | Source-local plus project derivation | `eq:bf-hd-synth-ess`, `eq:bf-hd-synth-logweight`, `prop:bf-hd-particle-collapse-calculus`; Bengtsson 2008 and Snyder 2008 | Dimension enters through log-likelihood dispersion; ESS/runtime must be vetoed before speed claims. | Exact constant, universal asymptotic theorem, or posterior accuracy claim. |
| Sparse-grid/high-degree cubature is first a local diagnostic, not a global default. | Source-local plus projection identity | `eq:bf-hd-synth-quadrature-remainder`, `prop:bf-hd-local-cubature-diagnostic`; Julier 1997, Arasaratnam 2009, Jia 2012/2013, Singh 2018 | Higher-order rules reduce quadrature error on controlled blocks but do not remove Gaussian projection error. | Global filter validity or superiority. |
| TT methods are viable only under stable ranks and semantic probability/covariance checks. | Source-local plus algebraic storage argument | `eq:bf-hd-synth-tt-defects`, `eq:bf-hd-synth-tn-indefinite`, `prop:bf-hd-tensor-viability`; Oseledets 2011, Li 2019, Fox 2021, Zhao 2024, Meng 2025/2026, Batselier 2016, Menzen 2024 | TT/TN components require rank, mass, positivity, PSD, and likelihood/score diagnostics. | General nonlinear tensor-filter validation. |
| Transport maps are industrially useful only when geometry improves without destroying target auditability. | Source-local plus change-of-variables identity | `eq:bf-hd-synth-transport-density`, `prop:bf-hd-transport-auditability`; Rosenblatt 1952, Reich 2013, Spantini 2022, Ramgraber 2023, Parno 2018, Hoffman 2019, Cui 2021 | Maps must export support/Jacobian/correction diagnostics. | Transport loss alone proves posterior correctness. |
| HMC belongs downstream of a same-scalar likelihood contract. | Source-local plus Hamiltonian target identity | `eq:bf-hd-synth-hmc-target`, `prop:bf-hd-hmc-downstream`; Neal 2011, Hoffman--Gelman 2014, Betancourt 2017, Girolami--Calderhead 2011, Andrieu--Roberts 2009, Andrieu--Doucet--Holenstein 2010 | HMC variants compare only after scalar/gradient/acceptance target parity. | HMC fixes an approximate or inconsistent filter target. |
| A non-novel composition can be industrially superior if each component reduces a named defect and exports a veto diagnostic. | Project synthesis with source families | `prop:bf-hd-block-scaffold-first`, `prop:bf-hd-useful-not-novel`, `alg:bf-hd-defect-synthesis` | Engineering value can come from disciplined composition and handoff diagnostics. | Academic novelty, production readiness, or validation. |

## Numerical Defect Ledger

| Numerical problem | Mathematical symptom | Mitigation | Residual risk |
|---|---|---|---|
| Underflow and weight collapse | log weights require log-sum-exp; ESS can still collapse | log-sum-exp plus ESS/max-weight/ancestor veto | arithmetic stability can hide statistical collapse. |
| Ill-conditioned innovations | large `kappa(S)` or failed factorization | factor solves, declared regularization | regularization changes likelihood if not encoded in target. |
| PSD loss | negative eigenvalue or failed Cholesky | Joseph/square-root/factor update | rounding can still damage downstream likelihood. |
| TT density drift | mass error or negative cells | mass/positivity/rank diagnostics | nonnegative representation may be expensive or source-limited. |
| Transport support mismatch | infinite density ratio or failed inverse/Jacobian | support coverage and explicit correction | learned maps can pass training loss and fail target checks. |
| HMC scalar mismatch | gradient does not match reported scalar | finite-difference and autodiff parity | approximate target remains approximate even if internally consistent. |

## Performance Ledger

| Component | Killing variable | Mitigation interpretation |
|---|---|---|
| Dense Gaussian filter | full state dimension and dense factorization | expose block/factor structure before nonlinear upgrades. |
| Sigma-point/cubature | state dimension and observation cost | apply only to local blocks unless point count is affordable. |
| Sparse grids | effective block dimension, level, and smoothness | diagnostic role first; adaptive/local promotion only after residual checks. |
| Particle methods | effective observation dimension through log-weight variance | guided/local/transport proposals reduce dispersion only if correction is retained. |
| TT/TN methods | rank, grid mode, boundary and semantic errors | rank stability and mass/PSD checks are promotion gates. |
| Transport maps | map dimension, logdet/Jacobian cost, ensemble size | local/triangular maps and residual checks before HMC acceleration. |
| HMC through filters | gradient-through-filter cost and invalid regions | fixed baseline and same-scalar diagnostics before acceleration claims. |

## Snowball And Omission-Risk Register

P3 does not rerun the full P1R/P1S snowball process.  It imports the existing
reviewed snowball and omission ledgers as the active reviewer-risk register and
records the P3 action for each risk that touches the industrial-defect
synthesis.

| risk_or_seed | prior ledger anchor | P3 action | reviewer answer | residual risk |
|---|---|---|---|---|
| Smolyak/Genz/Stroud sparse-grid and cubature foundations | P1S snowball closure row `Smolyak/Genz/Stroud`; P1S omission row `Smolyak 1963 sparse-grid formula`; P1U alternative-source row `Stroud book` | Keep sparse-grid performance discussion source-local to Jia 2012/2013 and Singh 2018; do not claim independent Smolyak/Stroud/Genz theorem support. | The synthesis uses sparse grids as block diagnostics under checked filtering papers, not as broad numerical-analysis theory. | Medium for any future full sparse-grid theory section. |
| TT-cross/maxvol foundations | P1S omission row `TT-cross/maxvol foundations`; P1U source-closure Savostyanov row where available | Do not use maxvol quasioptimality as a P3 theorem; rank and semantic checks rely on Oseledets TT storage and filtering-source diagnostics. | Tensor viability is a conditional industrial gate, not a TT-cross convergence theorem. | Medium-high for future TT-cross algorithm derivation. |
| Robust/pathwise DMZ transformations | P1S snowball and omission rows `Robust/pathwise DMZ`; P1U source closures for Davis/Yau/Meng where available | P3 does not derive PR-DMZ; it only treats TT/PDE routes as source-local pilots and keeps recent preprints provisional. | No hidden robust-DMZ support is used for industrial claims. | High if a future chapter expands pathwise robust filtering theory. |
| Arasaratnam--Haykin CKF primary support | P1S omission row `Arasaratnam--Haykin CKF`; local source cache later contains CKF PDF | P3 relies mainly on Ch34/P2R checked cubature exposition and does not rest a theorem on CKF priority. | CKF appears as a known Gaussian/cubature family and diagnostic comparator. | Low-medium if the local CKF PDF is not fully reflected in earlier ledgers. |
| Bengtsson/Snyder high-dimensional PF collapse | P1S omission row `Bengtsson--Bickel--Li and Snyder`; local source cache later contains both PDFs | P3 uses the collapse papers as source-local family anchors and gives a lognormal project derivation, while forbidding exact universal constants. | The chapter explains the collapse mechanism and does not claim a complete asymptotic theorem. | Low for industrial warning; medium for formal asymptotic statement. |
| Girolami--Calderhead RMHMC | P1S omission row `Girolami--Calderhead RMHMC`; local source cache later contains PDF | P3 uses RMHMC only as geometry-aware HMC context behind the same-scalar contract. | RMHMC does not change the target-validity boundary. | Low for P3; medium for future detailed RMHMC derivation. |
| Transport forward-snowball candidates | P1S snowball rows for Spantini 2022, Reich 2013, Parno--Marzouk 2018 | Do not claim comprehensive transport survey.  Use checked Spantini 2022, Reich 2013, Ramgraber 2023, Parno 2018, Hoffman 2019, Cui 2021. | A skeptical panel can see that forward coverage is a coverage signal, not theorem support. | Medium for final survey completeness. |
| Quarantined Spantini et al. 2016 decomposable transport workshop | P1S quarantined snowball entry and omission row | Exclude as support. | The retracted/quarantined workshop paper is not cited in P3 support. | Closed for P3 support; monitor if user supplies formal retraction details. |
| Broad finite-precision PSD analysis | P3 source-risk note | Keep as source risk; use only elementary PSD counterexample and square-root/factor logic. | The chapter does not pretend to contain a full Higham-style numerical linear algebra treatment. | Medium for future numerical-analysis appendix. |

## Source Risks And Quarantine

- The Spantini et al. 2016 decomposable-transport workshop paper remains
  quarantined/retracted and is not used as support.
- Savostyanov-specific maxvol quasioptimality, some local-particle-filter
  literature, and broader finite-precision numerical-analysis sources remain
  useful future additions but are not used as checked theorem support in P3.
- Stroud, Smolyak, Genz, and Knothe originals remain alternative-source or
  replacement-scoped where not fully source-local checked.
- Recent arXiv sources, especially Meng 2025/2026, are treated provisionally.
- Citation counts and venue rankings remain coverage signals only.
- The LaTeX preamble `docs/preamble.tex` loads `algorithm` and
  `algpseudocode`, so the P3 algorithm environment is integrated at source
  level; rendered PDF validation remains a separate gate.

## Review Gates

The Claude block review must answer, for each block A--H:

- `ACCEPT` only if the block is source-grounded, mathematically explicit, and
  free of overclaims;
- `REJECT` if it relies on prose where an equation, counterexample, proof
  sketch, diagnostic variable, or source-local anchor is required;
- on iteration 5, accept only minor editorial issues; stop for major source,
  derivation, numerical, unsupported-claim, or PDF-integration blockers.
