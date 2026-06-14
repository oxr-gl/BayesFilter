# P7 Gaussian/Transport/Tensor Self-Contained Derivation And Gradient Plan

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R/P3/P4/P5/P6 high-dimensional nonlinear
filtering artifacts, P6 reader-first result, `ch34`, `ch35`, `ch18`, `ch36`,
`docs/references.bib`, `docs/source_map.yml`, `docs/main.tex`, `docs/main.log`,
`docs/main.pdf`, local source cache, and the scholarly literature audit policy.

what_is_not_concluded: This plan does not conclude production readiness, NAWM
readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, GPU/XLA readiness, default readiness, exhaustive
literature coverage, or machine-certified proof validity.

## Objective

Repair the remaining panel blocker identified after P6: `ch34` and `ch35` are
still too compressed for a mixed numerical panel, and the Gaussian/high-order/
tensor approximate filters do not yet derive the exact analytical gradient of
the approximate likelihood scalar that would be required before HMC use.

This pass is not another broad readability pass.  It is a focused
professor-facing derivation pass for:

1. self-contained method exposition in `ch34` and `ch35`;
2. exact gradient contracts for implemented approximate likelihoods;
3. clear HMC admissibility labels for each approximation family.

## Skeptical Plan Audit

The failure mode after P6 is not missing orientation; earlier chapters already
introduce state-space filtering.  The remaining failure is method-local:
sections that name EKF, UKF, CKF, high-degree CKF, tensor-product
Gauss--Hermite quadrature, sparse-grid Gauss--Hermite filtering, particle
methods, transport maps, tensor trains, TT/KR transports, and tensor-network
Kalman filters without teaching the mechanism deeply enough for a chemistry,
physics, numerical-analysis, or applied-mathematics professor.

The wrong remedy would be to add more short survey paragraphs or more summary
tables.  The right remedy is to teach each method in a repeatable pattern:
object, construction, scalar likelihood, gradient, failure mode, diagnostic,
and industrial role.

The second failure is sharper: HMC needs the gradient of the scalar actually
reported to the sampler.  Therefore a Gaussian/high-order/tensor approximate
filter must derive
\[
  \nabla_\theta \widehat\ell_T(\theta),
\]
not merely state that an approximate likelihood exists.  Chapter `ch18` already
contains the local template for SVD sigma-point point, moment, innovation, and
Gaussian innovation likelihood derivatives; P7 should reuse the pattern while
respecting the different chapter scope.

This plan passes the skeptical audit if it:

- treats the P6 state as the baseline;
- targets `ch34` and `ch35`, with only narrow coordination edits elsewhere;
- does not convert source metadata, citation count, venue rank, abstracts, or
  blocked originals into theorem support;
- quotes or cites literature only where a checked technical result is actually
  used;
- states when a formula is a project derivation rather than a source theorem;
- assigns `HMC_ADMISSIBLE_APPROXIMATE_TARGET`, `HMC_BRANCH_LOCAL_ONLY`,
  `HMC_NOT_ADMISSIBLE_UNTIL_SMOOTHED`, or `DIAGNOSTIC_ONLY` labels for each
  approximation family;
- removes or demotes human-unfriendly summary material that appears before the
  method has been taught.

## Evidence Contract

Question: Can `ch34` and `ch35` be expanded into self-contained professor-facing
chapters, and can Gaussian/high-order/tensor approximate filters be given
analytical gradient contracts sufficient to decide whether they may feed HMC as
approximate targets?

Baseline: P6 `ch34` and `ch35`, plus the existing gradient treatment in `ch18`
and HMC same-scalar contract in `ch36`.

Primary pass criteria:

- a chemistry/physics/numerical-analysis professor can reconstruct the method
  object and approximation without prior filtering jargon;
- `ch34` explains EKF/IEKF, second-order EKF, sigma points, UKF, CKF,
  high-degree CKF, tensor-product GHQ, and sparse-grid GHQ before using them in
  tables or synthesis;
- `ch35` explains empirical measures, importance weights, resampling, ESS,
  guided proposals, transport correction, triangular maps, TT density/PDE
  filters, TT/KR transports, and TN covariance filters as standalone objects;
- every literature citation is attached to a specific checked theorem,
  algorithm, equation, derivation, or construction;
- every approximate likelihood family that could feed HMC has a scalar and
  gradient contract or is explicitly marked not HMC-admissible;
- MathDevMCP attempts are recorded for narrow algebra only;
- Claude hostile review accepts or leaves only minor editorial/layout issues.

Veto diagnostics:

- a method remains a named acronym without construction;
- a table asserts complexity/failure/diagnostic claims before the method is
  explained;
- any HMC-adjacent approximate filter lacks a scalar-gradient contract;
- adaptive rank, sparse-grid, resampling, clipping, floor, or branch changes
  are silently treated as smooth gradients;
- a source-gap or quarantined paper is used as support;
- citations appear as prestige/context where the text actually needs a
  theorem, algorithm, or equation;
- PDF build fails or new undefined citation/reference blockers appear.

Explanatory diagnostics:

- layout warnings in dense derivation tables;
- MathDevMCP status for small algebra;
- Claude minor style suggestions.

## Allowed Writes

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex` only if a
  cross-reference to the new P7 gradient contract is required
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex` only if export
  imports must be updated after `ch34`/`ch35` changes
- `docs/main.pdf`
- `docs/references.bib` only for newly used checked sources
- `docs/source_map.yml` only for provenance changes
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-*`

Forbidden writes:

- DPF implementation lane files;
- student-baseline or controlled-DPF files;
- production `bayesfilter/` code;
- public APIs;
- broad orientation chapters;
- unrelated dirty files;
- `.local_sources/` commits.

## Stop Conditions

Stop as `BLOCKED` if:

- a required method cannot be explained without an unavailable source and no
  checked successor/alternative source supports the claim;
- any derivative formula would require a smoothness/branch assumption that
  cannot be stated honestly;
- a method's approximate likelihood cannot be named as a scalar;
- Claude finds a major readability, source-support, overclaim, or gradient
  defect unresolved after five iterations;
- LaTeX build fails or new undefined references/citations cannot be repaired in
  scope.

Stop as `PARTIAL_READY_WITH_BLOCKERS` if:

- exposition improves but some method family remains diagnostic-only due to
  unresolved gradient or source blockers;
- layout remains rough but nonblocking;
- MathDevMCP cannot certify broad derivations.

## Required P7 Artifacts

Create:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-self-contained-gradient-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-gradient-obligation-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-source-anchor-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-mathdevmcp-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-claude-review-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-result-2026-05-29.md`

Each P7 ledger must include `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## Chapter 34 Rewrite Scope

### 1. Replace short method paragraphs with teachable sections

For each method family, use this section rhythm:

1. object being approximated;
2. construction in equations;
3. running quadratic-observation cell interpretation;
4. scalar approximate likelihood contribution if applicable;
5. analytical gradient contract;
6. failure mode;
7. diagnostic and industrial role;
8. exact technical citation anchor where a source result is used.

Required method families:

- EKF and iterated EKF;
- second-order EKF;
- generic deterministic Gaussian quadrature;
- UKF;
- CKF;
- high-degree CKF;
- tensor-product Gauss--Hermite quadrature;
- sparse-grid Gauss--Hermite / SGQF;
- adaptive sparse-grid filtering.

### 2. Explain before using acronyms

Do not use these terms in tables or conclusions before explaining them:

- high-degree CKF;
- tensor-product GHQ;
- sparse-grid GHQ;
- SGQF;
- CUT/SVD-CUT if referenced;
- sigma-point likelihood;
- square-root factor update.

### 3. Derive approximate Gaussian-filter likelihood gradients

For a generic deterministic Gaussian quadrature rule,
\[
  \chi_t^{(r)}(\theta)=m_t^-(\theta)+C_t^-(\theta)\xi^{(r)},\qquad
  z_t^{(r)}(\theta)=h_\theta(\chi_t^{(r)}(\theta)),
\]
derive:
\[
  \bar z_t=\sum_r w_r^{(m)}z_t^{(r)},\qquad
  S_t=R_\theta+\sum_r w_r^{(c)}(z_t^{(r)}-\bar z_t)
  (z_t^{(r)}-\bar z_t)^\top,
\]
\[
  v_t=y_t-\bar z_t,\qquad
  \widehat\ell_t
  =
  -\frac12\{\log\det S_t+v_t^\top S_t^{-1}v_t+n_y\log(2\pi)\}.
\]
Then derive first derivatives:
\[
  \dot\chi_t^{(r,i)}=\dot m_t^{-(i)}+\dot C_t^{-(i)}\xi^{(r)}
  \quad\text{for fixed offsets,}
\]
\[
  \dot z_t^{(r,i)}
  =
  D_xh_\theta(\chi_t^{(r)})\dot\chi_t^{(r,i)}
  +\partial_i h_\theta(\chi_t^{(r)}),
\]
\[
  \dot{\bar z}_t^{(i)}=\sum_r w_r^{(m)}\dot z_t^{(r,i)},
\]
\[
  \dot S_t^{(i)}
  =
  \dot R_\theta^{(i)}
  +
  \sum_r w_r^{(c)}
  \{\dot\Delta_t^{(r,i)}\Delta_t^{(r)\top}
  +\Delta_t^{(r)}\dot\Delta_t^{(r,i)\top}\},
\]
where \(\Delta_t^{(r)}=z_t^{(r)}-\bar z_t\), and
\[
  \dot v_t^{(i)}=\dot y_t^{(i)}-\dot{\bar z}_t^{(i)}.
\]
If recorded observations do not depend on \(\theta\), state
\(\dot y_t^{(i)}=0\).

With \(S_tw_t=v_t\), derive the score:
\[
  \partial_i\widehat\ell_t
  =
  -\frac12
  \left[
    \tr(S_t^{-1}\dot S_t^{(i)})
    +2\dot v_t^{(i)\top}w_t
    -w_t^\top\dot S_t^{(i)}w_t
  \right].
\]
Explain that this is the derivative of the approximate Gaussian innovation
likelihood, not the exact nonlinear filtering likelihood.

### 4. Branch and adaptivity labels

For each quadrature family, assign:

- `HMC_ADMISSIBLE_APPROXIMATE_TARGET`: fixed rule, differentiable maps,
  differentiable covariance factor policy, finite \(S_t\), same scalar and
  gradient.
- `HMC_BRANCH_LOCAL_ONLY`: hard floors, fixed active SVD/eigen support, fixed
  sparse-grid index set, or frozen TT rank branch.
- `HMC_NOT_ADMISSIBLE_UNTIL_SMOOTHED`: resampling, discontinuous adaptive
  sparse-grid point changes, rank changes, clipping, failed factorization, or
  nondifferentiable gates in the scalar path.
- `DIAGNOSTIC_ONLY`: method used only for local curvature or comparison, not as
  an HMC target.

### 5. Replace or relocate tables

Move complexity/failure tables after the method sections.  Remove redundant
tables that read like internal audit artifacts.  Any remaining table must help
a human reader learn the method.

## Chapter 35 Rewrite Scope

### 1. Expand each method into self-contained exposition

For each family, use:

1. object;
2. construction;
3. running-cell interpretation;
4. exact or approximate scalar if any;
5. gradient/HMC status if relevant;
6. failure mode;
7. diagnostic;
8. source anchor.

Required expansions:

- empirical particle measures and importance sampling;
- SIR/bootstrap filter and resampling;
- log-weight variance and ESS collapse;
- guided proposals and density-ratio correction;
- transport maps as change-of-variable objects;
- triangular/Rosenblatt/KR maps;
- ensemble transport filters and deterministic analysis maps;
- TT density/PDE filters;
- TT-cross/maxvol/rank diagnostics only where source support is checked;
- TT sequential learning and conditional KR transport bridge;
- tensor-network Kalman and square-root covariance filters.

### 2. Particle filter gradient/HMC boundary

Do not imply standard resampling particle filters give smooth HMC gradients.
State:

- fixed random numbers/no resampling/fixed ancestry can define a branch-local
  algorithmic scalar derivative;
- resampling and ancestor changes make the scalar nondifferentiable or
  piecewise constant/discontinuous in ordinary implementations;
- unbiased likelihood estimators support pseudo-marginal logic only under the
  relevant source assumptions, not ordinary HMC gradients;
- differentiable resampling belongs to the DPF lane and must not be imported as
  evidence here.

### 3. Transport gradient/HMC contract

For an invertible map \(x=T_\phi(z,\theta)\), derive:
\[
  q_\theta(x)=r(z)\left|\det D_zT_\phi(z,\theta)\right|^{-1},
  \qquad z=T_\phi^{-1}(x,\theta),
\]
and the log correction:
\[
  \log w(x,\theta)=\log\gamma_\theta(x)-\log q_\theta(x).
\]
For transformed HMC, derive:
\[
  U_z(z;\theta)
  =
  -\log\pi_q(T_\phi(z,\theta))
  -\log|\det D_zT_\phi(z,\theta)|.
\]
Then state the gradient contract and the support/Jacobian vetoes.

### 4. TT / tensor gradient contract

Separate three objects:

- TT density approximation \(\widehat p_\theta(x)\);
- TT/PDE operator propagation;
- TT/TN covariance or factor approximation.

For HMC use, require a scalar:
\[
  \widehat\ell_T(\theta)=\sum_t \log \widehat Z_t(\theta)
\]
with a declared differentiable branch.  Record:

- derivatives are branch-local if TT ranks, cross pivots, maxvol selections,
  truncation ranks, or active grids are frozen;
- rank adaptation, pivot changes, clipping, and hard truncation are
  nondifferentiable gates unless smoothed or declared outside HMC;
- TT compression residuals do not by themselves control likelihood-gradient
  error.

### 5. Chemistry/physics readability test

After rewriting each major section, ask:

> Could a computational chemistry or physics professor reconstruct the object,
> approximation, and failure mode without knowing nonlinear filtering jargon?

If no, expand with a toy scalar/block example before moving on.

## Source-Citation Protocol

Citation placement rule:

- Cite a paper exactly where a checked construction/result is used.
- Do not place a bibliography list at section end as substitute for technical
  support.
- For project derivations, cite only the source ingredients and label the
  derivation as a project derivation.
- Do not use abstracts, introductions, conclusions, metadata, citation counts,
  venue rank, or quarantined/retracted papers as theorem support.

Minimum source anchors to verify from existing ledgers before execution:

- Julier--Uhlmann UT/UKF;
- Arasaratnam--Haykin CKF and square-root CKF;
- Jia high-degree CKF;
- Jia SGQF;
- Singh adaptive sparse-grid Gauss--Hermite filter;
- Gordon bootstrap filter;
- Arulampalam tutorial for SIR mechanics only;
- Bengtsson and Snyder particle-collapse sources;
- Rosenblatt triangular transform;
- Reich ensemble transform;
- Spantini transport-map filtering/smoothing source that is not quarantined;
- Oseledets TT-SVD and TT-cross;
- Zhao--Cui TT sequential learning/KR;
- Batselier TN Kalman and Menzen TN square-root caution.

If any source anchor is not locally checked, downgrade the claim or add a
source-blocker note instead of using the citation.

## MathDevMCP Protocol

Use MathDevMCP only for narrow proof obligations:

- Gaussian innovation score identity;
- derivative of \(\log\det S\);
- derivative of \(v^\top S^{-1}v\);
- fixed-point quadrature moment derivative algebra;
- change-of-variable/Jacobian sign identities;
- small PSD/covariance counterexamples if new ones are introduced.

Record statuses:

- `MCP_VERIFIED`;
- `MCP_UNVERIFIED`;
- `MCP_INCONCLUSIVE`;
- `MCP_TOOL_LIMIT`;
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`.

Do not claim MathDevMCP certifies the broad chapter or HMC validity.

## Claude Review Loop

Claude Code is a bounded hostile reviewer only.  Codex remains supervisor and
final authority.  Use the scholarly literature audit review template plus the
task-specific criteria below.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p7-gaussian-transport-tensor-plan-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p7-gaussian-transport-tensor-exec-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded hostile academic/industrial review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.

Review criteria:

- Can a chemistry/physics/numerical-analysis professor understand `ch34` and
  `ch35` without already knowing nonlinear filtering jargon?
- Are high-degree CKF, tensor-product GHQ, sparse-grid GHQ/SGQF, particles,
  transports, TT density filters, TT/KR maps, and TN covariance filters taught
  before they are used in conclusions?
- Are citations attached to specific checked results rather than bibliography
  gestures?
- Are approximate likelihood scalar and gradient contracts explicit?
- Are branch/adaptivity/nondifferentiability limits honest?
- Are HMC-admissibility labels defensible?
- Are source blockers and quarantines respected?
- Are overclaims absent?
- Does the PDF build and render the expanded material?

Loop up to five iterations.  On iteration 5, accept only if remaining issues
are minor editorial/layout issues.  Stop for major source-support, derivation,
readability, unsupported-claim, or PDF blockers.

## PDF And Validation

Build:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
```

Validate:

```bash
git diff --check -- docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-*
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references|Rerun to get outlines" docs/main.log
pdftotext docs/main.pdf - | rg -n "Gaussian innovation likelihood|tensor-product Gauss|high-degree CKF|sparse-grid Gauss|approximate likelihood gradient|HMC_ADMISSIBLE|HMC_BRANCH_LOCAL|HMC_NOT_ADMISSIBLE|DIAGNOSTIC_ONLY|TT density approximation|transport gradient contract"
git status --short -- docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex docs/main.pdf docs/references.bib docs/source_map.yml docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p7-gaussian-transport-tensor-* .local_sources
```

Record layout warnings separately from scholarly blockers.

## Final Result Must Include

- what Codex inspected;
- whether the scholarly-literature-audit policy was used;
- Claude ACCEPT/REJECT history;
- MathDevMCP audit status;
- files changed;
- `ch34` self-contained expansion summary;
- `ch35` self-contained expansion summary;
- approximate-likelihood gradient derivation summary;
- HMC-admissibility labels by method family;
- source anchors newly used or downgraded;
- PDF build status;
- final skeptical mixed-panel probability estimate;
- residual scholarly/readability/gradient gaps and what is not concluded.
