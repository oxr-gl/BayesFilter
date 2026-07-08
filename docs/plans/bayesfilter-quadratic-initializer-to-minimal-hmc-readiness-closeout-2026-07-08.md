# Quadratic Initializer To Minimal HMC Readiness Closeout

Date: 2026-07-08

## Status

`COMPLETED_THROUGH_PHASE_3_MECHANICS_SMOKE`

## Summary

The runbook established a repaired path from reusable quadratic initializer to
minimal fixed-kernel HMC mechanics smoke:

1. Phase 0 found and documented a real coordinate mismatch risk.
2. The initializer was repaired so returned mass precision/covariance are in
   original theta coordinates when quadratic fitting uses whitened `z`.
3. Phase 1 produced a finite SPD theta-coordinate mass artifact.
4. Phase 2 consumed that artifact with `initialize_hmc_kernel_geometry`.
5. Phase 3 ran a tiny fixed-kernel mechanics smoke with finite telemetry.

## Decisions

| Phase | Decision | Key evidence |
| --- | --- | --- |
| 0 | `COMPLETED_WITH_REPAIR` | HMC expects theta-coordinate precision; old initializer exposed whitened precision if `scale` was supplied. |
| 1 | `PASSED_WITH_LOCAL_NEIGHBORHOOD_REPAIR` | Initializer accepted; precision condition number `55.004100411471235`; mass coordinates `theta`. |
| 2 | `PASSED_GEOMETRY_ONLY` | `selected_hint=negative_hessian`; step `0.22590050090246147`; L `7`; `L * step_size=1.5813035063172303`; no HMC runtime. |
| 3 | `PASSED_MECHANICS_SMOKE_ONLY` | 4 finite samples; acceptance `1.0`; finite log-accept and target-log-prob traces; no tuning. |

## Remaining Gaps

- Native boolean divergence telemetry is not exposed in the Phase 3 TFP HMC
  path. This is not zero divergences.
- Phase 3 has only 4 retained samples and 1 burn-in step, so acceptance and
  finite diagnostics are mechanics checks only.
- No R-hat, ESS, posterior/reference agreement, multi-seed uncertainty,
  calibration, or long-run stability evidence exists in this runbook.
- No GPU/XLA production evidence was run.
- No source-faithful Zhao-Cui claim was attempted or established.

## Next Justified Plan

If continuing, draft a separate short-chain validation plan. It should state a
native-divergence policy up front, run more than one seed or explain why not,
and keep readiness/posterior claims gated behind predeclared diagnostics.

## Final Nonclaims

- No HMC readiness claim.
- No posterior correctness claim.
- No sampler convergence claim.
- No sampler superiority claim.
- No default-readiness or production-readiness claim.
- No source-faithful Zhao-Cui parity claim.

