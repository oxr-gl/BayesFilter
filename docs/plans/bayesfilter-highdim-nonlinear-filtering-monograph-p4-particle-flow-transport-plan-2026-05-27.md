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

Veto diagnostics:

- Flow proposals are treated as exact posterior samples without correction.
- Finite-particle evidence is treated as unbiased log-likelihood or score
  evidence.
- Ensemble transport is described as exact nonlinear filtering.
- Transport-map claims lack a clear distinction between proposal construction,
  approximation, and exact target correction.

Explanatory diagnostics:

- ESS, resampling, map residual, and localization discussion.

Non-implications:

- Passing P4 does not validate DPF-HMC or high-dimensional particle filtering.

Artifact:

- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`

## Stop Rules

Stop P4 with a blocker if the chapter cannot keep proposal, correction,
resampling, smoothing, and exactness claims separate.

## Exit Label

`P4_TRANSPORT_ACCEPTED` if degeneracy and correction boundaries are explicit.
