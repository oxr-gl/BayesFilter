# Phase 3 Result: Material Particle Ladder

Date: 2026-07-01

Status: `PASS`

## Decision

Phase 3 passed through the conditional `N=1000`, `T=3`, five-seed rung under
trusted GPU/XLA/TF32.  The corrected manual total-derivative finite-Sinkhorn
route remained operational and finite at every checked particle count.

This is viability and scaling evidence for the corrected route.  It is not HMC
direction evidence and it is not posterior correctness evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | At what particle count does the corrected full route remain finite and operational under GPU/XLA? |
| Primary criterion | Passed for `N=16,T=1`, `N=64,T=3`, `N=256,T=3`, and `N=1000,T=3`. |
| Veto diagnostics | No veto triggered.  No CPU fallback, no missing XLA, no route-metadata failure, no nonfinite value/gradient/MCSE, no OOM. |
| Not concluded | No HMC direction validity, no posterior correctness, no exact nonlinear likelihood correctness, no production promotion. |

## Rung Summary

| Rung | Status | Elapsed seconds | Peak TF allocator bytes | Objective | Gradient values | MCSE |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `N=16,T=1,seeds=2` | `pass` | `138.15769824199378` | `50466816` | `-36.1256103515625` | `[-9.37370777130127, 3.432502508163452, 4.548910617828369]` | `{log_kappa_scale: 0.3407630920410156, log_nu_scale: 0.1250770092010498, log_obs_noise_scale: 0.3113260269165039}` |
| `N=64,T=3,seeds=5` | `pass` | `715.8411605180008` | `87696128` | `-124.877685546875` | `[-259.3408203125, 103.57362365722656, 44.914710998535156]` | `{log_kappa_scale: 3.0782182216644287, log_nu_scale: 1.2480616569519043, log_obs_noise_scale: 0.9125424027442932}` |
| `N=256,T=3,seeds=5` | `pass` | `688.3836792290676` | `468697856` | `-125.1681137084961` | `[-259.8353576660156, 103.83641052246094, 45.78861618041992]` | `{log_kappa_scale: 1.1120595932006836, log_nu_scale: 0.4503864347934723, log_obs_noise_scale: 0.3991796672344208}` |
| `N=1000,T=3,seeds=5` | `pass` | `505.82778843608685` | `6726029824` | `-125.3008041381836` | `[-260.80517578125, 104.21639251708984, 46.0502815246582]` | `{log_kappa_scale: 0.6466002464294434, log_nu_scale: 0.2674814760684967, log_obs_noise_scale: 0.23570899665355682}` |

The `T=3` MCSE decreased from `N=64` to `N=256` to `N=1000` for all three
parameters.  This supports the interpretation that the batch mean gradient
stabilizes as particle count increases.  It does not by itself prove agreement
with finite differences.

## Rung Artifacts

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n16-t1-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n64-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n64-t3-memory-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n256-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n256-t3-memory-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n1000-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n1000-t3-memory-2026-07-01.json`

## Gate Checks

Each rung passed the JSON gate:

- `status == "pass"`;
- `primary_pass is true`;
- output tensors on GPU;
- `compiler.mode == "xla"` and `compiler.jit_compile is true`;
- `transport.transport_ad_mode == "full"`;
- finite objective;
- finite gradient components;
- finite seed-gradient MCSE;
- `gradients_connected is true`;
- memory sample artifact present for rungs above `N=16`.

## Plain Scientific Classification

- Target computed: finite fixed-Sinkhorn active-transport scalar used by the
  P8p regression-FD diagnostic.
- Derivative classification: corrected manual total derivative route.
- What passed: GPU/XLA/TF32 viability through `N=1000,T=3`, five seeds.
- What remains untested: same-scalar finite-difference direction agreement and
  HMC direction adequacy.

## Next-Phase Handoff

Phase 4 may start after Claude reviews this result and the refreshed Phase 4
subplan.  The next question must be finite-difference direction agreement for
the same finite scalar and the same `transport_ad_mode="full"` route, not more
viability smoke.
