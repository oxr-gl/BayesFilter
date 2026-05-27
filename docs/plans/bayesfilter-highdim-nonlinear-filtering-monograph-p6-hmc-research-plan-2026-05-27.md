# P6 HMC for Nonlinear SSMs Research Chapter Plan

## Question

What HMC policy is reviewer-defensible for nonlinear SSMs when plain
mass-matrix HMC can diverge and TFP NUTS is diagnostic-only?

## Evidence Contract

Baseline:

- Existing HMC target chapter.
- Model B/C HMC ladder result.
- ResearchAssistant summaries for NeuTra, learned/HNN HMC, RMHMC, and flows
  when available.

Primary criterion:

- The chapter treats HMC as a per-model research problem and derives target,
  gradient, Metropolis, transformed-target, and diagnostic contracts.

Veto diagnostics:

- Finite short chains are called convergence.
- TFP NUTS is proposed as a production backend.
- HNN/NeuTra speed is claimed without target-preserving correction and
  downstream diagnostics.
- Divergences, nonfinite values, failed value/score parity, failed energy
  diagnostics, or R-hat/ESS failures are narrated as tuning nuisances rather
  than blocker or repair evidence.

Explanatory diagnostics:

- Divergence, acceptance, energy error, E-BFMI, R-hat, ESS, value/score parity,
  XLA/GPU compile state.

Non-implications:

- Passing P6 does not validate HMC for NAWM or any nonlinear model.

Artifact:

- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`

## HMC Stop/Reroute Rules

Any HMC diagnostic with one or more divergences, nonfinite samples, nonfinite
initial gradients, failed eager/compiled value or gradient parity, unavailable
R-hat/ESS on a multi-chain run, R-hat outside the declared tolerance, or low
E-BFMI must be labeled `hmc_blocker_or_repair`, not `accepted`.  Such a run may
support a geometry diagnosis or a next-step tuning/transport plan only.

## Stop Rules

Stop P6 with a blocker if the chapter cannot separate target correctness,
integrator correctness, sampler diagnostics, and posterior scientific validity.

## Exit Label

`P6_HMC_ACCEPTED` if the HMC chapter is conservative and per-model.
