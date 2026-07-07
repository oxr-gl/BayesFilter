# Phase 9 Subplan: GPU NeuTra Training Preflight

Date: 2026-07-07

## Phase Objective

Design the first GPU-only NeuTra training preflight for the LGSSM-first
BayesFilter program using the admitted non-DSGE targets and filters.

This phase may prepare and smoke the training harness.  It must not make a
posterior convergence, HMC readiness, production-readiness, route-ranking, or
scientific-validity claim.

## Entry Conditions Inherited From Previous Phase

- Phase 7 admitted the simple nonlinear Model B generic target adapter with the
  deterministic `tf_svd_ukf` route.
- Phase 8 admitted the deterministic `tf_svd_cubature` route through the same
  generic adapter boundary.
- Phase 8 deferred `tf_svd_cut4` and `tf_principal_sqrt_ukf` for explicit
  later gates.
- Phase 8 local checks passed:
  - `tests/test_simple_nonlinear_generic_target_adapter_tf.py`: `23 passed`;
  - py_compile passed.
- No NeuTra training, HMC sampling, GPU work, posterior correctness,
  production-readiness, or scientific-validity claim has been made for the
  simple nonlinear target.
- Owner policy: serious NeuTra training must be GPU; external sample
  generation must be multicore CPU and must be recorded separately.

## Required Artifacts

- Phase 9 result or blocker:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-result-2026-07-07.md`
- GPU training policy manifest naming:
  - target id;
  - admitted filter route;
  - GPU execution requirement;
  - forbidden CPU training fallback;
  - random seeds;
  - output artifact paths;
  - nonclaims.
- Focused smoke test or script for training-harness shape/value plumbing.
- Refreshed next-phase subplan for either:
  - actual GPU training run; or
  - blocker repair if preflight fails.

## Required Checks/Tests/Reviews

- Re-run Phase 8 target-adapter tests.
- Run an escalated GPU probe before any command that detects or uses GPU:
  `nvidia-smi` and a TensorFlow GPU visibility probe.
- If any training smoke is run, it must use trusted/escalated permissions and
  record GPU device evidence.
- CPU-only commands must set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import
  and must be labeled CPU-only.
- Run `git diff --check` on Phase 9 artifacts.
- Bounded read-only review of the Phase 9 result/blocker and next subplan
  before any full training run.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter prepare a GPU-only NeuTra training preflight for admitted non-DSGE SSM targets without crossing into posterior or HMC claims? |
| Baseline/comparator | Phase 6 LGSSM training harness and Phase 8 admitted simple nonlinear target/filter routes. |
| Primary criterion | Training harness can bind an admitted target route, enforce GPU-only training policy, emit finite initial objective diagnostics, and write a manifest without running unauthorized full training or HMC. |
| Veto diagnostics | CPU training fallback, untrusted GPU evidence, hidden HMC, hidden sample generation, nonfinite objective/gradient, missing manifest, missing seeds, or use of deferred filter routes. |
| Explanatory diagnostics | GPU device visibility, initial objective/gradient norm, parameter dimension, batch shape, route signatures, and runtime. |
| Not concluded | NeuTra quality, HMC readiness, posterior correctness, sampler convergence, route superiority, production readiness, or scientific validity. |
| Artifact | Phase 9 result/blocker, GPU policy manifest, focused tests/scripts, next subplan. |

## Forbidden Claims/Actions

- Do not run CPU NeuTra training.
- Do not hide CPU explicitly for training as a substitute for GPU policy.
- Do not run full training without a reviewed execution command and artifact
  path.
- Do not run HMC sampling or sampler tuning.
- Do not use DSGE/c603.
- Do not use deferred filter routes.
- Do not mix external sample generation into GPU training; sample generation
  belongs to a multicore CPU phase with separate artifacts.
- Do not claim posterior correctness, convergence, production readiness,
  default-policy change, route ranking, or scientific validity.

## Exact Next-Phase Handoff Conditions

The next phase may begin only if:

- Phase 9 records whether GPU-only training preflight passed or blocked;
- any GPU evidence was collected under trusted/escalated execution;
- no CPU training fallback was used;
- admitted target/filter route signatures are recorded;
- a full training command is either drafted and reviewed or explicitly blocked;
- read-only review agrees with the next subplan boundary.

## Stop Conditions

Stop if:

- GPU visibility cannot be established in trusted context;
- training harness attempts CPU training;
- any required objective or gradient diagnostic is nonfinite;
- a deferred filter route is needed;
- HMC or sample generation is required to proceed;
- review does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 9 result or blocker;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, GPU/CPU boundary safety, and claim discipline.
