# Phase R11 Diagnostic: Superseded CPU Finite-N Bias Check

Date: 2026-06-30

Status: `SUPERSEDED_BY_GPU_XLA_TF32_ROUTE`

## Supersession Note

This draft proposed a CPU-hidden FP64 material-route diagnostic.  That is the
wrong evidence route for LEDH after the owner clarification on 2026-06-30:
LEDH testing must use the GPU XLA TF32 batched branch unless explicitly marked
as reference-only.  This file is retained only to preserve the correction.

The active replacement plan is:

`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-score-diagnostic-2026-06-30.md`

## Retired Question

Does the R10 D=2 `log_observation_variance` score discrepancy shrink on a
CPU-hidden material replay route when particle count increases from `N=64` to
`N=1000` at fixed `T=10`?

## Evidence Contract

- Baseline: R10 Stage B D=2, `N=64`, `seed_count=10`, `T=10`, minimal-ridge
  replay policy.
- Comparator: exact FP64 Kalman value/score for the same LGSSM observation
  sequence and parameter convention `R(theta)=exp(theta_R) I_D`.
- Primary diagnostic: D=2 score deltas, especially `log_observation_variance`,
  relative to MCSE of the seed average.
- Veto diagnostics: nonfinite values/scores, ridge failure, covariance residual
  above `5e-4`, or a route mismatch from the R10 minimal-ridge replay scalar.
- Explanatory diagnostics: value delta, realized ridge range, score MCSE, and
  whether the N1000 delta is materially smaller than R10 N64.
- Nonclaims: this CPU-hidden FP64 diagnostic is not GPU/XLA/TF32 readiness, not
  SIR/SV correctness, not production readiness, and not HMC readiness.
- Stop condition: do not execute this retired plan for LEDH evidence.

## Planned Command

Run an import-level diagnostic using the existing R10 material functions with:

- `state_dim=2`;
- `num_particles=1000`;
- `seed_count=10`;
- `time_steps=10`;
- `settings=0.55:2`;
- `chol_ridge_abs=1e-10`;
- `chol_ridge_rel=1e-8`;
- `chol_ridge_max_attempts=12`;
- `CUDA_VISIBLE_DEVICES=-1`.

This command is retired and must not be used as LEDH evidence.  Any future
CPU-only run must be explicitly scoped as a reference/debug artifact.
