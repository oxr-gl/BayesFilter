# P4 Result: PF-PF Correction And Log-Det

Date: 2026-05-29

## Decision

`P4_PFPF_CORRECTION_LOGDET_ACCEPTED`

## Result

The integrated filter forms the PF-PF corrected log weight as:

`previous_log_weight + log p(x1 | ancestor) + log p(y | x1) - log q0(x0 | ancestor) + log |det D Phi(x0)|`.

For this first rung, `D Phi` is the frozen local-affine LEDH transport matrix
`L_post L_prior^{-1}` after evaluating the local observation Jacobian at the
pre-flow proposal particle.  The result records this as
`frozen_local_affine_log_abs_det` with scope
`local_observation_jacobian_held_fixed_per_particle`.

## Resolved Implementation Issue

An initial attempt computed per-particle autodiff Jacobians of the full
state-dependent local-linearization map.  That made the smoke harness too slow
and muddied the PF-PF convention.  The implementation was revised to the
auditable frozen local-affine LEDH determinant convention required by P1/P4.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| density contract | pass | `q0`, transition target, observation target, and forward log-det are recorded. |
| sign convention | pass | Forward log-det is added in corrected weights. |
| proxy overclaim | pass | Nonlinear correctness is not claimed. |
| missing stop conditions | pass | Non-finite corrected weights/log-det or singular map veto. |
| drift/contamination | pass | No production, monograph, vendored, or high-dimensional lane edits. |

## What Is Not Concluded

No exact nonlinear filtering, HMC readiness, posterior correctness, production
readiness, NAWM-scale readiness, or monograph claim.
