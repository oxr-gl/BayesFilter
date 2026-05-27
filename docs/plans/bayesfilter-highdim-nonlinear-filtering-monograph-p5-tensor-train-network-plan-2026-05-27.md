# P5 Tensor-Train and Tensor-Network Filtering Chapter Plan

## Question

How can tensor trains, tensor networks, and low-rank tensor structure reduce
effective complexity without overclaiming dimension reduction?

## Evidence Contract

Baseline:

- Direct TT nonlinear filtering papers.
- Tensor-train sequential Bayesian learning.
- Tensor-network Kalman and square-root tensor-network Kalman papers.
- Low-rank tensor UKF tractography example.

Primary criterion:

- The chapter records TT density/filtering, tensorized PDE filtering,
  tensor-network Kalman covariance safeguards, low-rank observation compression,
  rank-growth diagnostics, and BayesFilter pilot architecture.

Veto diagnostics:

- Tensor methods are described as automatically solving high dimension.
- Rank truncation ignores positivity, normalization, or covariance
  positive-definiteness.
- A tensor surrogate is proposed for HMC without value/score parity and
  posterior distortion checks.
- Tensor-network Kalman covariance compression is discussed without square-root
  or positive-definiteness safeguards.

Explanatory diagnostics:

- TT rank, residual, normalization error, positivity, gradient parity, and
  downstream filtering/HMC diagnostics.

Non-implications:

- Passing P5 does not create a tensor backend or validate tensor filtering.

Artifact:

- tensor sections in `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`

## Stop Rules

Stop P5 with a blocker if the chapter cannot state rank-growth, truncation,
normalization, positivity, and covariance-validity diagnostics for tensor
methods.

## Exit Label

`P5_TENSOR_ACCEPTED` if the chapter provides a research pilot and rank/error
contract with no default claim.
