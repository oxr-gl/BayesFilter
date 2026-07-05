# Phase 4 Subplan: HMC-Direction Diagnostic Gate

Date: 2026-07-01

Status: `READY_FOR_CLAUDE_REVIEW`

## Phase Objective

Evaluate whether the corrected full-route SIR gradient direction is accurate
enough for HMC-adjacent use under the agreed relaxed rule.

## Entry Conditions Inherited From Previous Phase

- Phase 3 passed through `N=1000`, `T=3`, five seeds under GPU/XLA full route.
- The route remained finite and metadata proved `transport_ad_mode="full"`.
- Phase 3 showed decreasing MCSE from `N=64` to `N=256` to `N=1000` for all
  three parameters.

## Required Artifacts

- Phase 4 JSON result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-2026-07-01.json`.
- Phase 4 memory samples:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-memory-2026-07-01.json`.
- Phase 4 progress artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-progress-2026-07-01.json`.
- Phase 4 markdown result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-result-2026-07-01.md`.
- Updated final-decision subplan.

## Required Checks, Tests, Reviews

Run a reviewed SIR direction diagnostic using the same corrected full route and
the same finite scalar.  Use the existing regression-FD runner with
`--fd-mode enabled`, raw parameter directions only, and
`transport_ad_mode="full"`.

Command:

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode enabled \
  --basis-set raw \
  --direction-filter log_kappa_scale,log_nu_scale,log_obs_noise_scale \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 3 \
  --base-step-mode ad-signal \
  --target-objective-delta 0.15 \
  --adaptive-step-factors 1.0,0.5,0.25 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --time-steps 3 \
  --num-particles 1000 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 128 \
  --col-chunk-size 128 \
  --particle-chunk-size 128 \
  --progress-output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-progress-2026-07-01.json \
  --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-memory-2026-07-01.json \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-2026-07-01.json
```

The result parser must compare each raw direction's AD directional derivative
against its regression FD plateau summary.  The parser must record absolute
error, MCSE, MCSE multiples when available, relative error, and which of the
three pass rules was met.

Runtime note:

- The first corrected Phase 4 attempt used the serial FD value path and was
  interrupted after it stayed in the first FD window for roughly 25 minutes.
  That was a diagnostic execution-shape problem, not evidence about the
  derivative.  The refreshed command uses the runner's batched-theta FD mode
  with theta-offset chunks of 3 to preserve the same scalar while bounding the
  number of value replays.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the corrected full-route gradient direction good enough for the intended HMC direction use? |
| Baseline/comparator | Finite-difference or regression finite-difference estimate for the same finite scalar and same route. |
| Primary criterion | For every checked parameter/direction, pass if one holds: within `2 MCSE`; or within `4 MCSE` and MCSE decreases as `N` increases; or relative error below `1%`. |
| Veto diagnostics | FD/regression artifacts not same scalar; nonfinite estimates; MCSE unavailable; route metadata not full; CPU fallback. |
| Explanatory diagnostics | Per-parameter error, MCSE, relative error, N trend, seed variance. |
| Not concluded | No posterior correctness or full HMC production readiness. |
| Artifact preserving result | Phase 4 result markdown/JSON. |

## Forbidden Claims And Actions

- Do not use the stopped route as the gradient being evaluated.
- Do not pass based on proxy metrics alone.
- Do not change the MCSE/relative-error rule after seeing results.
- Do not use Phase 3 MCSE decrease alone to pass Phase 4.  Phase 4 must inspect
  same-scalar regression FD direction results.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 if:

- Phase 4 result is written;
- criteria are applied exactly;
- Claude review returns `VERDICT: AGREE`.

## Stop Conditions

- No same-scalar FD/regression harness for full route.
- Nonfinite or unusable MCSE.
- GPU/XLA route fails during direction diagnostic.
