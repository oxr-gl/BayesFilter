# SIR Gradient Reparameterization Diagnostic Plan

Date: 2026-07-01

Status: `R2_READY_FOR_LOCAL_CHECKS`

## Objective

Test whether the apparent `log_kappa_scale` difficulty is partly a raw
parametrization problem.  First evaluate a hand-designed SIR physics
reparameterization.  Only after that result is interpreted, evaluate a more
generic local whitening idea if still justified.

## Background

The completed budget-10 SIR artifact showed:

- `log_kappa_scale`: `inconclusive_precision_veto`
- `log_nu_scale`: `within_4_combined_se_requires_ladder_certificate`
- `log_obs_noise_scale`: `within_2_combined_se`

The raw `log_kappa_scale` direction is noisy because it globally scales the
infection-rate vector:

```text
kappa = base_kappa * exp(log_kappa_scale)
infection = kappa * susceptible * infectious
```

The existing reparameterization harness already defines:

- `physics_rho_tau_omega`, with directions
  `rho_log_kappa_minus_log_nu`, `tau_common_rate`, and `omega_obs_noise`;
- `local_seed_gradient_whitened`, based on seed-gradient covariance.

## Phase R1: Hand-Designed Physics Basis

Question:

- Does the SIR-motivated `rho/tau/omega` basis produce better behaved
  manual-vs-FD direction diagnostics than the raw `log_kappa_scale` and
  `log_nu_scale` axes at budget 10?

Command:

```bash
bash scripts/run_sir_gradient_reparam_physics_budget10.sh
```

Artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-physics-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-physics-budget10-progress-2026-07-01.json`

Evidence contract:

| Field | Contract |
| --- | --- |
| Baseline | Phase 5 budget-10 raw-basis artifact, same route and fixed seeds. |
| Primary criterion | Route is GPU/XLA/TF32 and each physics-basis direction reports manual directional derivative, FD slope, slope SE, seed MCSE context, and pass/failure diagnostics. |
| Veto diagnostics | CPU route, non-XLA, TF32 disabled, nonfinite objective/gradient, missing FD outputs, exit 137, or changed budget/seed/theta route without documentation. |
| Explanatory diagnostics | Direction signs, magnitudes, slope SE, regression R2, seed-gradient geometry, and whether `rho/tau` isolates the noisy infection-vs-recovery direction. |
| Not concluded | No global reparameterization proof, no HMC readiness, no budget-100 conclusion, no posterior correctness. |

## Phase R2: Generic Whitening

Run only after R1 is interpreted.

Question:

- Does local seed-gradient whitening suggest a better numerical basis, despite
  the caveat that the score covariance is itself noisy?

Guardrail:

- Whitening is explanatory and exploratory.  It must not be promoted as a
  stable default parametrization from this small five-seed artifact.
- The whitening matrix is built from the local seed-gradient covariance and
  uses an eigendecomposition only to choose diagnostic directions after the
  score has been computed.  It is not a differentiable algorithm route and is
  not evidence that an eigenbasis should enter the LEDH computation.

Command:

```bash
bash scripts/run_sir_gradient_reparam_whitened_budget10.sh
```

Artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-progress-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-memory-2026-07-01.json`

Evidence contract:

| Field | Contract |
| --- | --- |
| Baseline | Phase R1 physics-basis artifact and Phase 5 raw-basis budget-10 artifact, same route and fixed seeds. |
| Primary criterion | Route is GPU/XLA/TF32 and each whitened direction reports manual directional derivative, FD slope, slope SE, regression R2, and the covariance eigenvalues used to build the basis. |
| Veto diagnostics | CPU route, non-XLA, TF32 disabled, nonfinite objective/gradient, missing FD outputs, exit 137, changed seeds/budget/theta/offset ladder, or missing whitening eigenvalue metadata. |
| Explanatory diagnostics | Eigenvalue spread, direction signs/magnitudes, slope SE, regression R2, whether whitened coordinates concentrate the mismatch in one direction, and whether any direction becomes stable enough to motivate a structured reparameterization. |
| Not concluded | No default whitening proposal, no HMC readiness, no SIR gradient correctness, no production basis selection, no budget-100 conclusion. |

Skeptical audit:

- The run answers only whether the observed five-seed score covariance geometry
  suggests a better local basis.  It cannot validate the covariance estimate
  itself; if the score is wrong, the whitening basis can be wrong too.
- The run keeps the same budget-10 route because changing the transport budget,
  seeds, or FD ladder at the same time would confound the parametrization test.
- The whitening eigendecomposition is acceptable here because the matrix is not
  part of the gradient-bearing LEDH route under test.
- The successful Phase R1 physics-basis run took about 30 minutes because XLA
  compiled the manual-reverse seed microbatches separately.  Therefore, absence
  of progress JSON before the AD stage completes is not by itself a blocker;
  memory sampling is required before classifying the monolithic whitening run
  as stalled.

## Forbidden Claims And Actions

- Do not use whitening before interpreting the physics basis.
- Do not claim `log_kappa_scale` is mathematically wrong from one budget-10
  artifact.
- Do not use CPU fallback as material evidence.
- Do not change the Phase 1 gate or raw-basis historical artifact.
- Do not run budget 100 in this diagnostic; that remains blocked by memory.

## Required Local Checks

```bash
bash -n scripts/run_sir_gradient_reparam_physics_budget10.sh
bash -n scripts/run_sir_gradient_reparam_whitened_budget10.sh
python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

## Stop Conditions

- R1 exits 137 or fails to produce JSON.
- Route metadata shows non-GPU, non-XLA, or TF32 disabled.
- R1 is already decisive enough to design a smaller next diagnostic without
  whitening.
