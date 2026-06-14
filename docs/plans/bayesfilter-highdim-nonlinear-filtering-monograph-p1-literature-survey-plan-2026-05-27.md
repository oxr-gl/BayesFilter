# P1 Literature Survey and Taxonomy Plan

## Question

Which nonlinear filtering and inference method families are serious candidates
for high-dimensional nonlinear SSMs, and what claims can each family support?

## Evidence Contract

Baseline:

- ResearchAssistant MCP local paper summaries first, with review-status and
  parser limitations recorded.
- Primary source pages, DOI/arXiv pages, or source URLs for every paper/method
  not locally indexed.
- Existing BayesFilter DPF and nonlinear chapters as context only.

Primary criterion:

- A survey matrix records method family, problem class, assumptions, update
  object, complexity/scaling, degeneracy mode, implementation availability,
  BayesFilter relevance, source-support class, and non-claims.
- For scholarly readiness, every theorem, approximation-order, complexity,
  degeneracy, empirical-performance, or implementation-availability claim must
  map to a primary technical source section/equation, a reviewed local
  ResearchAssistant summary, or a blocker.  Metadata-only rows may remain only
  as search scaffolding.

Veto diagnostics:

- Survey omits direct tensor-train filtering, transport filtering, classical
  high-order Gaussian filters, particle/flow filters, or HMC acceleration.
- Survey treats a source's reported experiment as BayesFilter validation.
- Survey uses source titles or abstracts as proof of mathematical claims.
- Any row lacks a source URL or explicit "local source unavailable" blocker.
- A mathematical theorem, complexity claim, or empirical performance claim lacks
  a source-support class.
- A row with `primary_metadata_only`, `local_ra_summary_only`,
  `secondary_context_only`, or `blocked_source_needed` is used to support a
  final chapter claim rather than a motivation or blocker.

Explanatory diagnostics:

- Citation counts, code availability, and source maturity.

Non-implications:

- Passing P1 does not approve implementation, defaults, or scientific validity.

Artifact:

- Literature chapter sections and survey matrix in the chapter draft.

## Source-Support Classes

Each matrix row must use one of:

- `primary_technical_checked`: relevant technical section/equation inspected;
- `primary_metadata_only`: source page/abstract/metadata checked only, so
  technical claims remain provisional;
- `local_ra_summary_only`: ResearchAssistant summary exists but source text is
  unavailable or unreviewed;
- `secondary_context_only`: used only to motivate search, not to support claims;
- `blocked_source_needed`: row cannot support chapter claims until inspected.

Chapter prose may rely on `primary_metadata_only`, `local_ra_summary_only`, or
`secondary_context_only` only for scoped motivation, not for theorem,
complexity, algorithmic, implementation-availability, or performance claims.
Final scholarly-readiness requires that each method family have at least one
technically checked primary source or a recorded source-gap blocker.

## Stop Rules

Stop P1 with a structured blocker if direct tensor/transport/HMC sources cannot
be assigned at least metadata-level support, if the survey matrix cannot
distinguish primary technical support from abstract-level support, or if any
method family needed by later chapters lacks a technically checked source and no
source-gap blocker is recorded.

## Required Families

- EKF, IEKF, second-order EKF, UKF, CKF, Gauss-Hermite, CUT4, higher-degree
  cubature.
- Sparse-grid and Smolyak filters.
- Projection filters and assumed-density filters.
- EnKF, ensemble transform, ensemble transport.
- Particle, auxiliary, guided, flow, transport, and differentiable particle
  filters.
- Tensor-train nonlinear filtering and tensor-network Kalman filtering.
- Low-rank tensor UKF examples.
- Transport-map filtering and smoothing.
- NeuTra, transport-preconditioned HMC, HNN/learned HMC, DA-HMC.

## Exit Label

`P1_SURVEY_ACCEPTED` if the matrix is broad enough and all claims are bounded.

`P1_SCHOLARLY_SOURCE_ACCEPTED` only if source gaps have been closed for claims
that appear in final chapter prose, or those claims are explicitly removed or
blocked.
