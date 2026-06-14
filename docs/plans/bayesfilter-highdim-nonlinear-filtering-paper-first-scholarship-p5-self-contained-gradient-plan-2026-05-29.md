# P5 Self-Contained Exposition And Analytical-Gradient Plan

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R/P3/P4 high-dimensional nonlinear filtering
artifacts, `ch33`--`ch37`, `docs/references.bib`, `docs/main.tex`,
`docs/main.log`, `docs/main.pdf`, the scholarly literature audit policy, and
the P4 MathDevMCP and derivation ledgers.

what_is_not_concluded: This plan does not conclude production readiness, NAWM
readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, GPU/XLA readiness, machine-certified proof
validity, or exhaustive literature coverage.

## Skeptical Plan Audit

The material flaw in the P4 state is not primarily citation coverage.  It is
reader contract and gradient completeness.  A mixed numerical panel can object
that the chapters assume nonlinear filtering vocabulary, and that the HMC
chapter states a same-scalar gradient contract before deriving the analytical
state-space likelihood gradient it needs.

This P5 pass is therefore narrow.  It should not reopen the literature survey
or rewrite the block again as a compliance artifact.  It should add enough
definitions, object roles, and gradient derivations that a numerical analyst,
computational chemist, physicist, or applied mathematician can audit the
mathematical handoff from filtering normalizers to HMC gradients.

P5 inherits the P1R/P1S/P1T/P1U/P2R/P3/P4 source-support, snowball,
omission-risk, and quarantine ledgers.  It may not weaken those ledgers.  Any
new theorem-level or algorithm-level literature claim introduced during P5 must
either be supported by those existing checked ledgers or the relevant ledger
must be extended inside the allowed write set.  If that cannot be done, the
claim must be omitted or marked as a source gap.

The plan passes the skeptical audit if:

- the exact baseline is the current P4 chapter block;
- the primary promotion criterion is clearer self-contained exposition plus
  explicit analytical likelihood and HMC-gradient derivations;
- MathDevMCP is used only on split algebraic obligations and cannot be treated
  as broad certification;
- Claude review is hostile and bounded;
- PDF and citation/reference validation are required;
- no chapter claims are promoted to production evidence.
- the existing source-support/quarantine state is inherited and no new
  substantive claim bypasses checked primary technical support.

## Evidence Contract

Question: Can the current high-dimensional nonlinear filtering block be made
more self-contained for a mixed numerical review panel and give an analytical
gradient derivation sufficient to support the HMC same-scalar target contract?

Baseline: the P4 `ch33`--`ch37` chapters and P4 result/derivation ledgers.

Primary pass criterion:

- `ch33` defines the filtering law, normalizers, likelihood, and parameter
  sensitivity recursions in project notation.
- `ch36` derives the HMC potential gradient from the analytical likelihood
  gradient and transformation/Jacobian terms.
- `ch33`--`ch37` contain compact self-contained object/role exposition for
  non-filtering numerical readers.
- Each analytical-gradient obligation is recorded in a P5 ledger.

Veto diagnostics:

- missing or inconsistent likelihood-gradient recursion;
- HMC gradient not tied to the same scalar potential;
- approximate-filter gradients confused with exact likelihood gradients;
- unsupported theorem-level claims;
- use of abstracts, metadata, venue rank, citation counts, blocked originals,
  or quarantined papers as theorem support;
- a needed primary technical source is unavailable and the text would otherwise
  fall back to abstract, introduction, conclusion, venue, or metadata support;
- undefined citations/references or failed PDF build;
- Claude `REJECT` with major unresolved derivation or self-containedness
  finding.

Explanatory diagnostics:

- MathDevMCP verification of small algebraic identities;
- PDF layout warnings;
- Claude minor editorial suggestions.

Artifact preserving the result:

- this plan;
- P5 self-contained exposition, analytical-gradient, MathDevMCP, and Claude
  ledgers;
- rebuilt `docs/main.pdf`;
- P5 result note.

Source-support artifact rule:

- P5 does not create a new full literature survey.
- P5 must record when it relies on existing literature ledgers.
- P5 must extend a ledger only for new nontrivial claims not already covered.

## Allowed Writes

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.pdf`
- `docs/references.bib` only if a needed checked source is missing
- `docs/source_map.yml` only if provenance changes
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p5-*`

Forbidden writes: DPF implementation lane files, student-baseline files,
controlled-DPF files, production `bayesfilter/` code, public APIs,
`.local_sources/` commits, and unrelated dirty files.

Per-file intent:

- `ch33`: primary location for exact filtering objects, likelihood
  normalizers, and sensitivity recursions.
- `ch36`: primary location for analytical HMC-gradient, transformation, scalar
  parity, and approximate-gradient contract text.
- `ch34`, `ch35`: compact reader-contract clarifications only.
- `ch37`: compact synthesis-map and anti-overclaim clarifications only.
- `references.bib`: only for already-inspected primary sources required by a
  new nontrivial claim.
- `source_map.yml`: only if provenance changes.

## Stop Conditions

Stop and report `BLOCKED` if:

- the likelihood-gradient derivation cannot be made internally consistent
  under stated assumptions;
- the HMC-gradient expression cannot be tied to the exact or declared
  approximate scalar;
- a new substantive source-dependent claim requires unavailable technical text
  and would otherwise rely on abstract, metadata, introduction, conclusion, or
  venue support;
- Claude finds a major derivation or overclaim blocker that remains unresolved
  after five iterations;
- LaTeX cannot build the PDF;
- new undefined citations/references appear and cannot be fixed inside the
  allowed write set.

Stop and report `PARTIAL_READY_WITH_BLOCKERS` if:

- the math is human-reviewed but key obligations remain tool-inconclusive;
- self-containedness improves but panel-facing exposition remains visibly too
  compact;
- only layout warnings remain after successful build.

## Self-Contained Exposition Checklist

Each chapter should add or strengthen a compact reader contract:

- define the mathematical object before describing methods;
- state input object, output object, exact target, approximation, failure mode,
  diagnostic, and industrial relevance for each method family;
- use simple examples where they clarify a defect;
- keep implementation evidence compact and outside the main mathematical flow;
- preserve source blockers, quarantines, and nonclaims.

Chapter targets:

- `ch33`: conditional law, normalizer, likelihood, exact versus approximate
  target, density/PDE vocabulary bridge, sensitivity object.
- `ch34`: Gaussian projection as moment closure, quadrature as expectation
  approximation, polynomial exactness versus posterior accuracy.
- `ch35`: particles as empirical measures, transports as change-of-variable or
  coupling objects, TT/TN as compressed representations with semantic checks.
- `ch36`: HMC as a sampler for a scalar potential, not a filter; target,
  transform, Jacobian, analytical gradient, and diagnostics.
- `ch37`: synthesis map from defects in `ch33`--`ch36` to industrial decision
  gates.

## Analytical-Gradient Derivation Checklist

In `ch33`, derive the exact discrete-time state-space likelihood gradient:

- define \(p_t^-(x_t)=p_\theta(x_t\mid y_{1:t-1})\),
  \(p_t(x_t)=p_\theta(x_t\mid y_{1:t})\), and
  \(Z_t(\theta)=\int g_\theta(y_t\mid x_t)p_t^-(x_t)\,dx_t\);
- derive
  \(\ell_T(\theta)=\sum_t\log Z_t(\theta)\) and
  \(\nabla_\theta \ell_T=\sum_t \nabla_\theta Z_t/Z_t\);
- define prediction and update sensitivities
  \(s_t^-=\nabla_\theta p_t^-\) and \(s_t=\nabla_\theta p_t\);
- derive the sensitivity prediction recursion, normalizer gradient, and
  normalized update sensitivity;
- state assumptions: dominated differentiation, finite positive normalizers,
  differentiable transition and observation densities, nonpathological support,
  and separate treatment for continuous-time/PDE adjoints.
- label support status in the chapter-side ledger: the discrete-time
  sensitivity recursion is `PROJECT_DERIVATION`; continuous-time/PDE
  score/adjoint analogues are `SOURCE_GAP_BLOCKER` or `SURVEY_CONTEXT_ONLY`
  unless derived from inspected technical sources in this pass.

In `ch36`, derive the analytical HMC potential gradient:

- \(U(q)=-\ell_T(\tau(q))-\log\pi(\tau(q))-\log|\det D\tau(q)|\);
- \(\nabla_q U(q)=
  -D\tau(q)^\top[\nabla_\theta\ell_T(\theta)+
  \nabla_\theta\log\pi(\theta)]_{\theta=\tau(q)}
  -\nabla_q\log|\det D\tau(q)|\);
- connect \(\nabla_\theta\ell_T\) to `ch33` sensitivity recursions;
- include a scalar Gaussian example whose gradient is computed by hand;
- distinguish analytical gradients, autodiff of the same scalar, finite
  differences as diagnostics, and approximate-filter gradients.
- state that approximate-filter gradients do not establish exact posterior
  gradients, exact likelihood gradients, or correctness of HMC for the exact
  model unless an exact correction proof is supplied.

## Approximate-Filter Gradient Contract

If an approximate filter defines \(\widehat Z_t\), \(\widehat p_t^-\), and
\(\widehat p_t\), downstream HMC targets
\(\widehat\pi(\theta\mid y_{1:T})\propto
\exp\{\sum_t\log\widehat Z_t(\theta)\}\pi(\theta)\) unless an exact correction
is present.  The reported gradient must be the derivative of that reported
scalar.  Truncation, resampling, rounding, clipping, adaptive stopping, and
nondifferentiable gates must declare the scalar being differentiated.

Mandatory anti-overclaim text for `ch36` and `ch37`: approximate-filter
gradients support only the declared approximate scalar.  They cannot be
described as exact posterior gradients or exact state-space likelihood
gradients absent an exact correction proof.

## MathDevMCP Obligation-Splitting Protocol

Do not ask MathDevMCP to certify broad propositions.  Split obligations into:

- derivative of \(\log Z\): \(\nabla\log Z=\nabla Z/Z\);
- normalization sensitivity formula for \(p=a/Z\);
- scalar Gaussian likelihood-gradient example;
- chain-rule expression for a one-dimensional transform when feasible;
- any reused covariance or PSD toy equalities.

If MathDevMCP returns `MCP_UNVERIFIED`, `MCP_INCONCLUSIVE`, or
`MCP_TOOL_LIMIT`, the derivation may remain in the main text only with an
explicit human-reviewed derivation note and appropriate support status.  If the
human derivation cannot be written clearly, the claim must be weakened,
downgraded to a heuristic, or omitted.

Record statuses as:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

## Claude Review Loop

Use Claude as a read-only hostile reviewer.  Codex remains final authority.
For plan review and execution review, Claude must output `ACCEPT` or `REJECT`
first.  Loop up to five iterations.  Accept iteration five only if remaining
issues are minor editorial or layout issues.  Stop for major derivation,
source-support, unsupported-claim, or PDF blockers.

Review criteria:

- self-containedness for mixed numerical professors;
- correctness and assumption clarity of the likelihood-gradient derivation;
- correctness and assumption clarity of the HMC-gradient derivation;
- exact versus approximate gradient separation;
- honest MathDevMCP status;
- no source/quarantine violations;
- no unsupported production or posterior-accuracy claims.

Operational self-containedness acceptance test:

- before first use, each chapter defines its central scalar or object;
- each chapter includes at least one sentence distinguishing exact target,
  approximation, diagnostic role, and industrial relevance;
- a reader can identify the input and output object of each method family
  without relying on prior nonlinear-filtering jargon.

## PDF Validation

Run:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references|Rerun to get outlines" docs/main.log
pdftotext docs/main.pdf - | rg -n "Analytical Likelihood-Gradient|Filtering Sensitivity|Analytical HMC Gradient|Approximate-Filter Gradient|P5"
git diff --check
```

Record layout warnings separately from scholarly blockers.
