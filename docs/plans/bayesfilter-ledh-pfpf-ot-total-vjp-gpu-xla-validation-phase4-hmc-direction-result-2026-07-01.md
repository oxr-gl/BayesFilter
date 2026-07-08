# Phase 4 Result: HMC-Direction Diagnostic Gate

Date: 2026-07-01

Status: `PASS_WITH_RUNTIME_CAVEAT`

## Decision

Phase 4 passed the predeclared raw-direction rule for the corrected
`transport_ad_mode="full"` route at `N=1000`, `T=3`, five seeds.  For all three
raw parameter directions, the manual total derivative was within `4 MCSE` of
the same-scalar regression finite-difference estimate, and the Phase 3 MCSE
trend decreased as particle count increased.  `log_kappa_scale` also passed the
relative-error rule with error below `1%`.

This is evidence that the full-route gradient direction is good enough for the
intended HMC-adjacent direction use in this diagnostic.  It is not posterior
correctness evidence, exact nonlinear likelihood evidence, or production HMC
readiness.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Is the corrected full-route gradient direction good enough for the intended HMC direction use? |
| Primary criterion | Passed for all three raw directions. |
| Veto diagnostics | No veto triggered in the completed batched-theta run. |
| Runtime caveat | Serial FD was interrupted as too slow; batched-theta FD completed but took `3030.1685376500245` seconds. |
| Not concluded | No posterior correctness, no exact nonlinear likelihood correctness, no full HMC production readiness. |

## Route And Artifact Gate

Completed JSON:

`docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-2026-07-01.json`

Gate facts:

- `status`: `pass`
- `primary_pass`: `true`
- output tensors on `/device:GPU:0`
- `compiler.mode`: `xla`
- `compiler.jit_compile`: `true`
- `transport.transport_ad_mode`: `full`
- `regression_fd.fd_mode`: `enabled`
- FD evaluation mode: `batched-theta`
- elapsed seconds: `3030.1685376500245`
- peak TensorFlow allocator bytes: `6726029824`

Memory artifact:

`docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-memory-2026-07-01.json`

Progress artifact:

`docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-progress-2026-07-01.json`

## Direction Rule Evaluation

Representative FD slope uses the smallest available base-step window for each
raw direction.  This is the conservative local-window comparison in the
artifact.

| Direction | AD directional derivative | FD representative | Absolute error | MCSE | Error / MCSE | Relative error | Pass rule | Plateau |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `log_kappa_scale` | `-260.80517578125` | `-263.24005126953125` | `2.43487548828125` | `0.6466002464294434` | `3.76566` | `0.924964%` | `4_MCSE_AND_DECREASING_MCSE`, `REL_LT_1_PERCENT` | unchecked: minimum-step clamp left only one base step |
| `log_nu_scale` | `104.21639251708984` | `105.2790298461914` | `1.0626373291015625` | `0.2674814760684967` | `3.97275` | `1.009353%` | `4_MCSE_AND_DECREASING_MCSE` | checked, slope range `0.233245849609375` |
| `log_obs_noise_scale` | `46.0502815246582` | `46.76666259765625` | `0.7163810729980469` | `0.23570899665355682` | `3.03926` | `1.531820%` | `4_MCSE_AND_DECREASING_MCSE` | checked, slope range `0.06605148315429688` |

The `4 MCSE` rule is applicable because Phase 3 showed decreasing MCSE from
`N=64` to `N=256` to `N=1000` for all three parameters:

- `log_kappa_scale`: `3.0782182216644287 -> 1.1120595932006836 -> 0.6466002464294434`
- `log_nu_scale`: `1.2480616569519043 -> 0.4503864347934723 -> 0.2674814760684967`
- `log_obs_noise_scale`: `0.9125424027442932 -> 0.3991796672344208 -> 0.23570899665355682`

## Runtime And Harness Notes

The first Phase 4 command used serial FD and was interrupted after it stayed in
the first FD window for roughly 25 minutes.  That was a diagnostic execution
problem, not derivative evidence.  The reviewed repair used
`--fd-evaluation-mode batched-theta --theta-offset-batch-size 3`, which
preserves the same theta rows and finite scalar while reducing serial value
replays.

Even with batched-theta, this diagnostic is expensive at `N=1000`: about
50.5 minutes wall time for one raw-basis run.  Future routine use should either
cache/reuse compiled value paths, run a smaller same-scalar FD sentinel, or add
a purpose-built batched/XLA value comparator.

## Plain Scientific Classification

- Target computed: finite fixed-Sinkhorn active-transport scalar used by the
  P8p regression-FD diagnostic.
- Derivative classification: corrected manual total derivative route.
- Comparator: same-scalar regression finite difference on raw parameter
  directions.
- What passed: direction agreement under the predeclared relaxed HMC-adjacent
  rule.
- What remains unsupported: posterior correctness, exact nonlinear likelihood
  correctness, production HMC readiness, and any claim that the stopped partial
  derivative route is a score.

## Next-Phase Handoff

Refresh Phase 5 final decision subplan and send this result plus the final
decision draft to Claude read-only review.  The direct final label supported by
the artifacts is:

`GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE_WITH_RAW_DIRECTION_GATE_PASS`
