# Phase 5 Result: Final Decision And Next Implementation

Date: 2026-07-01

Status: `PASS_FINAL`

## Final Label

`GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE_WITH_RAW_DIRECTION_GATE_PASS`

## Decision

The corrected LEDH-PFPF-OT finite-Sinkhorn total-derivative route is viable in
the repository default trusted GPU/XLA/TF32 lane for the checked SIR diagnostic.
It ran through `N=1000`, `T=3`, five seeds with finite objective, finite
gradient components, finite seed-gradient MCSE, GPU output tensors, XLA JIT,
and `transport_ad_mode="full"`.

The same route also passed the raw-direction same-scalar regression-FD gate at
`N=1000`, `T=3`.  All three raw parameter directions passed the predeclared
rule: within `2 MCSE`, or within `4 MCSE` with MCSE decreasing as `N`
increases, or relative error below `1%`.

This route remains experimental.  The Phase 4 FD diagnostic is expensive, the
raw-basis gate is not full HMC production validation, and this does not prove
posterior correctness or exact nonlinear likelihood correctness.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Keep and use the corrected full-route implementation for next SIR/HMC-adjacent diagnostics, labeled experimental. |
| Primary criterion | Passed: GPU/XLA/TF32 viability through `N=1000,T=3` and raw-direction same-scalar FD gate passed. |
| Veto diagnostics | No final veto triggered.  CPU fallback, missing XLA, route metadata mismatch, nonfinite output, and missing MCSE did not occur in the completed gates. |
| Main uncertainty | Phase 4 FD is expensive; only raw directions and the checked SIR diagnostic are covered. |
| Next justified action | Add a cheaper same-scalar FD sentinel or XLA/batched value comparator for routine regression testing. |
| Not concluded | No posterior correctness, exact nonlinear likelihood correctness, full HMC production readiness, or validation of all models/bases/time horizons. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Environment | Python `3.11.14`, TensorFlow `2.19.1` |
| CPU/GPU | Trusted GPU execution on NVIDIA GeForce RTX 4080 SUPER; TF32 enabled |
| Seeds | Phase 1: `81120,81121`; Phase 3/4 material rungs: `81120,81121,81122,81123,81124` |
| Main Phase 4 command | `python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py ... --fd-mode enabled --basis-set raw --fd-evaluation-mode batched-theta --theta-offset-batch-size 3 --transport-ad-mode full --num-particles 1000 --time-steps 3` |
| Phase 4 wall time | `3030.1685376500245` seconds |
| Phase 4 output | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-2026-07-01.json` |
| Plan | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-master-program-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-result-2026-07-01.md` |
| Ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-execution-ledger-2026-07-01.md` |

## Artifact Chain

| Phase | Result | Status |
| --- | --- | --- |
| 0 | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-result-2026-07-01.md` | `PASS` |
| 1 | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-result-2026-07-01.md` | `PASS` |
| 2 | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-result-2026-07-01.md` | `SKIPPED_NOT_NEEDED` |
| 3 | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-result-2026-07-01.md` | `PASS` |
| 4 | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-result-2026-07-01.md` | `PASS_WITH_RUNTIME_CAVEAT` |

## Evidence Summary

Phase 0:

- Static dispatch proof shows the legacy selector
  `manual_streaming_finite_sinkhorn_stopped_scale_keys`, when paired with
  `transport_ad_mode="full"`, reaches
  `_filterflow_manual_streaming_finite_transport_total_vjp`.
- Focused local checks passed.
- Trusted GPU probe saw the RTX 4080 SUPER and TensorFlow GPU.

Phase 1:

- Tiny trusted GPU/XLA full-route smoke passed at `N=16,T=1`.
- Output tensors were on GPU.
- Manual-reverse unit used XLA JIT.
- Objective, gradient, and MCSE were finite.

Phase 3:

- Particle ladder passed through `N=1000,T=3`.
- `T=3` MCSE decreased from `N=64` to `N=256` to `N=1000` for all three
  parameters.
- `N=1000,T=3` peak TensorFlow allocator memory was `6726029824` bytes.

Phase 4:

- Same-scalar raw-direction regression FD gate passed at `N=1000,T=3`.
- `log_kappa_scale`: `3.76566 MCSE`, `0.924964%` relative error.
- `log_nu_scale`: `3.97275 MCSE`.
- `log_obs_noise_scale`: `3.03926 MCSE`.
- Serial FD was too slow and interrupted; reviewed batched-theta FD completed in
  `3030.1685376500245` seconds.

## What Is Supported

- The stopped partial derivative route is wrong for any claim that it is the
  score of the executed active-transport scalar.
- The corrected `transport_ad_mode="full"` route computes the intended finite
  fixed-Sinkhorn total-derivative target for this diagnostic path.
- The corrected route is operational under trusted GPU/XLA/TF32 through the
  checked SIR ladder.
- The raw-direction same-scalar FD evidence is good enough for the intended
  HMC-adjacent direction use in this diagnostic.

## What Is Not Supported

- No claim of posterior correctness.
- No claim of exact nonlinear likelihood correctness.
- No claim of full HMC production readiness.
- No production/default promotion beyond the existing owner directive.
- No claim that the legacy stopped partial derivative route is a score.
- No claim that all parameterizations, bases, models, or long time horizons are
  validated.

## Runtime Caveat

The most important engineering caveat is Phase 4 runtime.  The full
same-scalar FD diagnostic at `N=1000,T=3` is expensive even with batched theta
evaluation.  For routine testing, add a smaller same-scalar sentinel or a
purpose-built batched/XLA value comparator.  Do not silently replace the
same-scalar FD gate with a proxy metric.

## Claude Final Review

Claude reviewed the Phase 4 result and proposed final label as read-only
reviewer and returned `VERDICT: AGREE`.

Claude agreed that:

- Phase 4 applied the predeclared rule correctly.
- The `log_kappa_scale` one-window caveat is plainly recorded.
- The serial-FD interruption and runtime cost are plainly recorded.
- The final label is supported without overclaiming.

## Next Action

Use the corrected full-route implementation for the next SIR/HMC-adjacent
diagnostic work, but keep it labeled experimental.  The next engineering
improvement should target a cheaper same-scalar FD sentinel or an XLA/batched
value comparator for routine regression testing.
