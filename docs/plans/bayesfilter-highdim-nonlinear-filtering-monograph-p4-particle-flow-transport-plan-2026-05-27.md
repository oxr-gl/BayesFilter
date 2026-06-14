# P4 Particle, Flow, and Transport Filtering Chapter Plan

## Question

What particle, flow, and transport filtering ideas are plausible for
high-dimensional nonlinear SSMs under degeneracy pressure?

## Evidence Contract

Baseline:

- Existing DPF chapters and evidence notes.
- Primary literature on ensemble transport filtering and transport maps.

Primary criterion:

- The chapter separates bootstrap particle degeneracy, guided proposals,
  flow-proposal correction, differentiable resampling, ensemble transport
  filtering, and smoothing claims.
- For scholarly readiness, each particle/flow/transport method must include a
  precise target/proposal/correction contract, implementation-grade pseudocode
  or exclusion rationale, complexity and memory scaling, degeneracy diagnostics,
  and source support for exactness or approximation claims.

Veto diagnostics:

- Flow proposals are treated as exact posterior samples without correction.
- Finite-particle evidence is treated as unbiased log-likelihood or score
  evidence.
- Ensemble transport is described as exact nonlinear filtering.
- Transport-map claims lack a clear distinction between proposal construction,
  approximation, and exact target correction.
- Particle degeneracy, ESS, smoothing, resampling bias, flow Jacobian, or
  transport-map claims are made without primary-source support or derivation.
- The chapter recommends high-dimensional use without an industrial failure
  analysis and BayesFilter evidence blocker.

Explanatory diagnostics:

- ESS, resampling, map residual, and localization discussion.

Non-implications:

- Passing P4 does not validate DPF-HMC or high-dimensional particle filtering.

Artifact:

- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`

## Stop Rules

Stop P4 with a blocker if the chapter cannot keep proposal, correction,
resampling, smoothing, and exactness claims separate.

Stop P4 scholarly refinement with a blocker if any method family lacks
target/proposal/correction pseudocode, source-supported assumptions, scaling,
degeneracy diagnostics, and NAWM-scale failure/rescue discussion.

## Exit Label

`P4_TRANSPORT_ACCEPTED` if degeneracy and correction boundaries are explicit.

`P4_SCHOLARLY_TRANSPORT_ACCEPTED` only if the chapter is technically grounded
enough that flow and transport claims cannot be mistaken for exact filtering or
posterior validation.
