# P10 Plan: Zhao-Cui TT Code Audit, Derivation, And Promotion

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition."
- Existing BayesFilter P8/P9 Ch34 fixed-SGQF artifacts.

what_is_not_concluded:
- No production readiness.
- No NAWM readiness.
- No posterior accuracy.
- No HMC convergence.
- No tensor-method validation on a BayesFilter client model.
- No default method recommendation.
- No GPU/XLA readiness.
- No permission to copy LGPL/GPL code into production `bayesfilter/`.

## Purpose

This pass decides whether the Zhao-Cui tensor-train sequential filtering route is
source-grounded, code-backed, and gradient-contract-feasible enough to become
one of the two main high-dimensional nonlinear filtering candidates beside the
fixed sparse-grid Gaussian projection filter from Chapter 34.

The intended outcome is not "TT wins."  The intended outcome is a defensible
promotion, demotion, or conditional-promotion decision based on inspected paper
anchors, companion code, a reproducibility attempt, a filtering-normalizer
extraction, and an honest fixed-branch gradient analysis.

## Skeptical Plan Audit

The plan targets the actual blocker: Chapter 35 currently treats Zhao-Cui too
briefly and still contains panel-facing audit language.  A mixed numerical
panel would ask whether the TT method has real code, what the recursive density
object is, where the normalizer enters, and whether the approximation can
support the same scalar needed downstream by HMC.

Risks checked before execution:
- Wrong baseline: fixed SGQF is a quadrature candidate, while Zhao-Cui is a
  density/transport candidate.  The comparison must be by represented object,
  not by a single runtime number.
- Proxy metric risk: an included demo or ESS output cannot establish posterior
  accuracy or suitability for BayesFilter models.
- Missing stop condition: promotion stops if no filtering scalar or normalizer
  can be identified, if paper/code mismatch on the core recursion, or if the
  gradient path is too opaque to state honestly.
- Environment mismatch: the companion code is MATLAB 2021a/2023a oriented.
  This machine currently has neither `matlab` nor `octave` on PATH, so a code
  run may be environment-blocked.  That blocker must be recorded separately
  from an algorithmic failure.
- License mismatch: the companion code is LGPL-3.0-or-later.  It may support
  code audit and replication evidence, but it must not be copied into
  production `bayesfilter/` without a separate license decision.
- Hidden assumptions: TT ranks, cross-interpolation choices, random enrichment,
  SVD truncation, defensive terms, basis/domain choices, and preconditioning
  all affect the scalar and derivative path.

The plan is executable because the source paper is locally cached, the code has
been cloned to `/tmp/bayesfilter-p10-zhao-cui-tensor-ssm-paper-demo`, and the
write scope is limited to Chapter 35, Chapter 37, PDF output, and P10 ledgers.

## Evidence Contract

Question:
Is Zhao-Cui TT sequential filtering sufficiently source-grounded, code-backed,
and gradient-contract-feasible to become one of the two main high-dimensional
nonlinear filtering candidates?

Baselines and comparators:
- fixed SGQF from Chapter 34 as the quadrature/compressed-grid candidate;
- existing BayesFilter SVD-CUT4/SVD sigma-point spine as a same-scalar
  value/score reference pattern, not as a high-dimensional solution;
- Zhao-Cui paper Algorithms 1--5 and companion MATLAB code.

Promotion criteria:
- companion code is inspectable and either runnable or blocked only by a clear
  environment limitation;
- at least one included example run path can be audited without hidden missing
  code;
- paper and code expose recursive posterior approximations and normalizer or
  evidence increments clearly enough to define an approximate scalar
  \(\widehat\ell_T\);
- approximation and adaptation branches are identifiable;
- a fixed-branch analytical gradient contract can be stated honestly;
- rank, mass, positivity, normalization, support, map, and branch diagnostics
  are identifiable.

Veto diagnostics:
- code missing core TT/SIRT implementation;
- license forbids intended use without unacceptable obligations;
- examples cannot be run or understood;
- no identifiable filtering scalar/normalizer;
- TT approximation branches too opaque to state a same-scalar gradient;
- paper/code mismatch on core algorithm;
- unsupported claims or overclaims would be required for promotion.

Diagnostics that are explanatory only:
- demo ESS;
- plotted L1 curves;
- wall time in an included script;
- repository size or polish;
- citation count or venue prestige.

Artifact preserving the result:
- P10 ledgers and promotion result under `docs/plans/`.
- Chapter edits, if and only if the promotion criteria pass at conditional or
  full promotion scope.

## Allowed Writes

- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.pdf`
- `docs/references.bib` only if a new checked source is actually used
- `docs/source_map.yml` only if provenance changes
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-*`

Forbidden writes:
- DPF implementation lane files;
- student-baseline files;
- controlled-DPF files;
- production `bayesfilter/` code;
- public APIs;
- unrelated dirty files.

## Stop Conditions

Stop without promotion if any major blocker remains:
- no filtering scalar/normalizer;
- companion code lacks the core algorithm;
- paper/code crosswalk fails for Algorithms 1--2;
- license makes audit evidence unusable for the intended presentation;
- Chapter 35 would need claims not supported by the inspected source;
- Claude or Codex identifies a major unsupported derivation or overclaim.

Conditional promotion is allowed if the method has source and code support for
filtering/smoothing and a clear approximate scalar, but the complete analytical
gradient remains a future implementation obligation.

## Code Audit Checklist

- license and copying constraints;
- language/runtime and dependencies;
- examples and reproducibility commands;
- core classes/functions for SSM, TT density, squared TT, KR maps, marginal
  densities, normalizers, filtering, smoothing, parameter learning;
- rank, truncation, basis, domain, random-enrichment, and preconditioning
  controls;
- storage of evidence increments or `logmarginal_likelihood`;
- diagnostic outputs: ESS, rank, timing, L1 comparisons, weights.

## Reproducibility Checklist

- Try smallest Kalman demo if MATLAB/Octave exists.
- Record exact command and environment.
- If not runnable here, record `ENVIRONMENT_BLOCKED_NO_MATLAB_OR_OCTAVE`.
- Audit the run path by reading `eg1_kalman/main_script.m`, model setup, and
  `full_sol`/`Y_sol` recursion.
- Do not treat an environment-blocked run as an algorithmic failure.

## Paper-To-Code Crosswalk Checklist

Map paper objects to code paths:
- SSM equations (1)--(3) and recursion (9)--(12);
- Algorithm 1 nonseparable/separable/integration steps;
- squared-TT density (13), marginal Proposition 2, conditional maps (17)--(20);
- Algorithm 2 squared-TT sequential estimation;
- Proposition 4 conditional KR backward sampler;
- Algorithms 3--5 if used in Chapter 35;
- code paths `ssmodel`, `Y_sol`, `full_sol`, `red_sol`, `pre_sol`,
  `TTSIRT`, `TTIRT`, `TTFun`, `marginalise`, `eval_irt`, `eval_cirt`,
  `eval_pdf`, and `logmarginal_likelihood`.

## Filtering Scalar / Normalizer Extraction Checklist

Identify whether the method defines
\[
  \widehat\ell_T(\theta)=\sum_{t=1}^T \log \widehat Z_t(\theta).
\]

The paper candidates are:
- Algorithm 1 normalizing constant \(c_t\) for the TT approximation;
- squared-TT normalizer \(\widehat z_t\) in (13);
- conditional evidence \(p(y_t\mid y_{1:t-1})\) in (9)--(10);
- implementation field `sol.logmarginal_likelihood += log(sirt.z) - const`.

The audit must state whether this scalar is an approximate evidence, a
posterior-normalization artifact, or only a diagnostic implementation quantity.

## Analytical-Gradient Feasibility Checklist

Classify operations on \(\theta\mapsto\widehat\ell_T(\theta)\):
- smooth: transition/likelihood densities, fixed tensor contractions, fixed
  basis evaluations, fixed affine maps, fixed normalizer contractions;
- piecewise smooth with fixed branch: Cholesky/preconditioning, QR/SVD with
  simple spectra, fixed TT ranks and interpolation sets;
- adaptive/discrete: TT-cross pivots, random enrichment, rank truncation,
  max-rank clipping, resampling/data-splitting choices, minimum-constant shift,
  adaptive preconditioning;
- nonsmooth or branch-local: hard clipping, `max(...,0)`, finite ESS-triggered
  resampling/reapproximation;
- unsupported: any derivative of learned TT cores with respect to parameters
  not derived or implemented.

Allowed gradient conclusion:
- Complete analytical HMC gradient only if derivative of TT coefficients,
  normalizers, branch choices, and parameter-dependent maps are fully derived.
- Otherwise state a fixed-branch gradient contract and list the missing
  derivatives required before HMC.

## MathDevMCP Obligation Splitting

Use MathDevMCP only for narrow identities:
- \(\partial_i\log Z=(\partial_i Z)/Z\);
- derivative of normalized density \(p_\theta=q_\theta/Z_\theta\);
- simple squared-density normalizer identity
  \(Z=\int \phi_\theta(x)^2\,dx+\tau\);
- change-of-variable identity for a differentiable triangular map;
- finite-dimensional TT contraction derivative when the cores are fixed.

Record:
- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

No broad certification claim is allowed.

## Chapter Rewrite Scope

If the promotion gate passes at least conditionally:
- rewrite the Zhao-Cui section in Chapter 35 as source reconstruction rather
  than survey prose;
- define the filtering object, TT density, squared TT, normalizer, KR maps, and
  recursive algorithm in BayesFilter notation;
- add pseudocode enough for Codex to implement a minimal prototype;
- explain diagnostics in human language;
- replace internal status labels with mathematical statements about scalar
  availability, fixed/adaptive branches, and HMC consequences;
- update Chapter 37 to compare fixed SGQF and Zhao-Cui TT as two conditional
  candidates.

If promotion fails:
- keep Zhao-Cui as promising but not promoted;
- write blockers and next actions instead of expanding claims.

## Claude Review Loop

Plan review command:
`bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p10-zhao-cui-tt-plan-review-iter<N> --model sonnet --effort high "<bounded hostile plan review prompt>"`

Execution review command:
`bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p10-zhao-cui-tt-exec-review-iter<N> --model sonnet --effort high "<bounded hostile academic/industrial code-and-math review prompt>"`

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude and loops
up to five iterations.  Iteration 5 may be accepted only for minor editorial or
layout issues.

## PDF Validation Requirements

Run:
- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex`
- `git diff --check`
- targeted `docs/main.log` scan for undefined citations/references/rerun
  blockers;
- `pdftotext docs/main.pdf -` scan for new Zhao-Cui TT sections.

Check `.local_sources/` remains untracked and unstaged, and only allowed files
changed intentionally.
