# BayesFilter NeuTra GPU Training / CPU Sample Generation Policy Reset

Date: 2026-07-07

## Owner Directive

Future BayesFilter NeuTra training should be GPU work.  Generation of external
samples, replay datasets, target/evaluation samples, proposal clouds, or
training datasets should use multicore CPU parallelism.

## Policy Change

- Added `AGENTS.md` policy section `NeuTra Execution Target Policy`.
- Serious BayesFilter-owned NeuTra training, including affine, dense-IAF,
  normalizing-flow, and future learned transport families, must plan for trusted
  GPU execution by default.
- CPU-only NeuTra training is now allowed only as an explicitly labeled tiny
  smoke, reference, or sandbox-diagnostic exception under a reviewed plan.
- CPU-only NeuTra training exceptions must not support learned transport
  quality, HMC readiness, posterior correctness, production readiness, or
  scientific-validity claims.
- External sample generation should be planned as multicore CPU work, recording
  worker count, seeds, target signature, and artifact hashes.

## Phase 6 Interpretation

The LGSSM-first Phase 6 CPU-only affine NeuTra-style run remains a historical
bounded smoke/integration fixture.  It is not the future serious NeuTra
training route and must not be cited as evidence that CPU-only NeuTra training
is the BayesFilter default.

## Boundary

This policy reset does not certify HMC convergence, posterior correctness,
dense IAF quality, sampler superiority, production readiness, or scientific
validity.  Those claims still require reviewed evidence gates.
