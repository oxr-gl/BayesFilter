# High-Dimensional Nonlinear Filtering Paper-First Scholarship Master Program

Date: 2026-05-28

## Purpose

This program replaces the current high-dimensional nonlinear filtering scaffold
with a paper-first scholarly monograph block.  The prior block was useful as a
claim-control audit, but it was not adequate as an academic artifact: it
foregrounded BayesFilter evidence boxes, source-gap ledgers, and no-overclaim
language while leaving too much primary-source mathematics undeveloped.

The new acceptance target is a critical academic review panel of former
professors turned industrial practitioners.  The chapters must explain the
papers, not merely cite them.  Each major paper or method family must be
presented in BayesFilter notation with assumptions, equations, derivations or
proof sketches, algorithms, complexity, failure modes, and industrial relevance.

## Active Chapter Targets

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

`docs/main.tex`, `docs/main.pdf`, `docs/references.bib`, and
`docs/source_map.yml` may be updated only after the source-intake and chapter
rewrite phases allow it.

## Required Literature Pillars

The program must use primary technical sources, not abstracts, for the following
pillars.

### Direct Tensor-Train Nonlinear Filtering

- Li, Wang, Yau, Zhang, tensor-train nonlinear filtering via
  Fokker-Planck/Kushner-Stratonovich/DMZ-style PDE machinery,
  `https://arxiv.org/abs/1908.04010`.
- Zhao and Cui, JMLR 2024, tensor-train sequential state and parameter learning
  with conditional Knothe-Rosenblatt transports,
  `https://www.jmlr.org/papers/v25/23-0743.html`.
- Functional tensor-train grid filtering for Bayes-optimal
  continuous-discrete filtering,
  `https://www.tandfonline.com/doi/full/10.1080/17415977.2020.1862109`.
- Meng, Yau, Zhang 2026, tensor-train nonlinear filtering with correlated
  noise, `https://arxiv.org/abs/2605.25677`.

### Tensor-Network Kalman Family

- Batselier, Chen, Wong tensor-network Kalman filtering for lifted Volterra
  systems, `https://arxiv.org/abs/1610.05434`.
- Tensor-network square-root Kalman filter,
  `https://arxiv.org/abs/2409.03276`.
- Low-rank tensor UKF tractography paper,
  `https://www.sciencedirect.com/science/article/pii/S1053811923001507`.

### Transport-Map Nonlinear Filtering

- Spantini, Baptista, Marzouk, nonlinear ensemble filtering via couplings and
  transport maps, `https://epubs.siam.org/doi/10.1137/20M1312204`.
- Ensemble transport smoothing, Part I,
  `https://www.sciencedirect.com/science/article/pii/S2590055223000124`.
- Decomposable transports for Bayesian filtering and smoothing,
  `https://approximateinference.org/2016/accepted/SpantiniEtAl2016.pdf`.

### Sparse-Grid And Higher-Order Competitors

- High-degree cubature Kalman filter,
  `https://www.sciencedirect.com/science/article/pii/S000510981200550X`.
- Sparse-grid quadrature nonlinear filtering,
  `https://www.sciencedirect.com/science/article/pii/S0005109811005541`.
- Adaptive sparse-grid Gauss-Hermite filtering,
  `https://www.sciencedirect.com/science/article/pii/S0377042718301742`.

### HMC And Transport Acceleration Substrate

- Transport-map accelerated MCMC,
  `https://epubs.siam.org/doi/10.1137/17M1134640`.
- NeuTra HMC, `https://arxiv.org/abs/1903.03704`.
- Deep inverse Rosenblatt transports using tensor trains,
  `https://arxiv.org/abs/2007.06968`.

### Numerical Tensor Substrate

- Tensor-train sampling of multivariate densities,
  `https://link.springer.com/article/10.1007/s11222-019-09910-z`.
- Tensor-train rank bounds for Gaussian densities,
  `https://arxiv.org/abs/2001.08187`.
- Fokker-Planck by tensor-train cross approximation,
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC8366026/`.
- Fast high-dimensional integration using tensor networks,
  `https://arxiv.org/abs/2202.09780`.

## Non-Negotiable Scholarly Gates

1. **Primary-source fidelity gate.**  Every literature claim in the final
   scholarly exposition must trace to a checked primary-source
   section/equation/theorem or to a blocker.  Local ResearchAssistant summaries
   may support triage, planning, and source discovery only; they may not support
   chapter mathematics, theorem claims, or paper-specific derivations unless
   the corresponding technical full text is inspected.  Abstract-only support is
   forbidden.
2. **Derivation gate.**  Each main method receives assumptions, state variables,
   central equations, a derivation or proof sketch, and a statement of what is
   exact versus projected, discretized, truncated, localized, or learned.
3. **Algorithm gate.**  Each method family receives implementation-grade
   pseudocode or a precise exclusion rationale.
4. **Complexity gate.**  Each method family records state dimension, grid or
   rank dimension, particle/ensemble size, map dimension, memory scaling, and
   leading numerical bottlenecks.
5. **Failure-mode gate.**  Each method lists degeneracy, rank growth,
   positivity, normalization, covariance, localization, Jacobian, sampler, or
   approximation-fidelity failures.
6. **Industrial gate.**  Each chapter answers what fails at NAWM-like DSGE
   scale, what structure could rescue it, and what evidence would be needed
   before promotion.
7. **Academic prose gate.**  The main chapter text must read like a monograph,
   not an internal audit memo.  BayesFilter evidence appears only in compact
   implementation-boundary notes or appendices.
8. **No-overclaim gate.**  The rewrite still forbids claims of NAWM readiness,
   HMC convergence, tensor-method validation, posterior accuracy, broad GPU/XLA
   readiness, production defaults, or client switch-over readiness unless
   directly supported.

## Phase Order

1. P0: failure diagnosis and acceptance criteria reset.
2. P1: primary-source intake and citation ledger.
3. P2: foundations rewrite.
4. P3: tensor-train nonlinear filtering rewrite.
5. P4: tensor-network Kalman and square-root tensor filtering rewrite.
6. P5: transport-map filtering and smoothing rewrite.
7. P6: sparse-grid and high-degree cubature competitors rewrite.
8. P7: transport-preconditioned HMC, NeuTra, and TT-KR bridge rewrite.
9. P8: synthesis chapter with propositions and proof sketches.
10. P9: PDF integration and academic-style editorial pass.
11. P10: final critical academic review, audit, and commit.

## Required Review Loop

For planning and for each execution phase:

1. Codex inspects relevant local files, source status, and previous artifacts.
2. Codex performs a skeptical plan audit before editing or running commands.
3. Claude Code is launched as a read-only hostile reviewer:
   `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-paperfirst-<phase>-review-iter<N> --model sonnet --effort high "<bounded read-only review prompt>"`
4. Claude must output `ACCEPT` or `REJECT` first.
5. Codex audits Claude's review.  Claude is not final authority.
6. If Claude rejects and Codex agrees, Codex patches and resubmits.
7. Planning loops stop after 5 iterations.  Execution section/chapter loops
   stop after 10 iterations.
8. On the final allowed iteration, accept only minor editorial issues; stop if
   any source-fidelity, derivation, citation, or synthesis blocker remains.

## Source-Intake Stop Rule

ResearchAssistant MCP currently has no local summaries for most required papers.
If P1 confirms that the primary source text is not locally available, execution
must stop after the reviewed plan/subplans and source-intake ledger are created.
Codex must ask the user for approval to fetch the exact public URLs listed in
this plan.  No chapter rewrite may claim to have read or derived from a paper
that has not been locally inspected.

The mechanical execution predicate for P2--P8 is:

`PHASE_SOURCE_READY = all papers required by the phase have support class
LOCAL_FULL_TEXT_CHECKED in the P1 ledger, with local artifact path, inspected
technical section numbers, inspected equation/theorem/algorithm identifiers
where available, intended chapter consumers, and unresolved blockers recorded.`

If `PHASE_SOURCE_READY` is false, the phase result must be
`BLOCKED_PENDING_SOURCE_INTAKE`; no chapter editing is allowed.

## Allowed Write Set

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- the five active chapter files listed above
- `docs/main.tex`
- `docs/main.pdf`
- `docs/references.bib`
- `docs/source_map.yml`

## Forbidden

- Do not touch DPF implementation lane files.
- Do not touch student-baseline or controlled-DPF files.
- Do not edit production `bayesfilter/` code.
- Do not change public APIs.
- Do not use abstracts as theorem support.
- Do not treat local smoke tests as scientific validation.
- Do not stage unrelated dirty files.
- Do not run GPU/CUDA/NVIDIA commands.
- Do not run network/API source intake without an accepted source-intake plan
  and explicit user approval for the exact URLs.

## Final Audit

The final audit must verify:

- every phase P0-P10 has a result or structured blocker;
- every required paper has source-support status and citation ledger entry;
- every major chapter claim maps to a P1 ledger row with inspected technical
  sections/equations or to an explicit blocker;
- every chapter section has hostile review acceptance or a blocker;
- every major equation has assumptions and derivation/proof sketch;
- MathDevMCP audit attempts or limitations are recorded for important labels;
- PDF builds and contains the rewritten chapters;
- no undefined citations or references in the new block;
- no unsupported tensor, transport, HMC, NAWM, GPU/XLA, posterior, or production
  claims remain;
- `docs/source_map.yml` parses;
- `git diff --check` passes;
- staged files are path-scoped and allowed only.

## Commit Policy

If and only if final academic audit passes, create one path-scoped commit:

`Rewrite high-dimensional nonlinear filtering chapters from primary literature`
