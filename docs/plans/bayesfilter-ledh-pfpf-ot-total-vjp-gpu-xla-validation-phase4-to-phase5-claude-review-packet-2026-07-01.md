# Claude Review Packet: Phase 4 Result To Phase 5 Final Label

Status: `READY_FOR_REVIEW`

## Role Contract

Codex is supervisor and executor.  Claude is read-only reviewer only.  Claude
must not edit files, run experiments, launch agents, or change state.

## Question

Check whether the Phase 4 result correctly applies the predeclared direction
rule and whether the proposed final label is supported without overclaiming.

## Scope

Review only:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-subplan-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-execution-ledger-2026-07-01.md`

## Evidence

Phase 4 route gate:

- GPU output tensors;
- XLA JIT manual-reverse unit;
- `transport.transport_ad_mode == "full"`;
- `regression_fd.fd_mode == "enabled"`;
- FD mode `batched-theta`;
- finite objective, gradient, MCSE;
- elapsed seconds `3030.1685376500245`;
- peak TensorFlow allocator bytes `6726029824`.

Direction rule table:

| Direction | Error / MCSE | Relative error | Pass rule |
| --- | ---: | ---: | --- |
| `log_kappa_scale` | `3.76566` | `0.924964%` | `4_MCSE_AND_DECREASING_MCSE`, `REL_LT_1_PERCENT` |
| `log_nu_scale` | `3.97275` | `1.009353%` | `4_MCSE_AND_DECREASING_MCSE` |
| `log_obs_noise_scale` | `3.03926` | `1.531820%` | `4_MCSE_AND_DECREASING_MCSE` |

The Phase 3 MCSE trend decreases from `N=64` to `N=256` to `N=1000` for all
three parameters.

Proposed final label:

`GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE_WITH_RAW_DIRECTION_GATE_PASS`

## Pass/Block Criteria

Pass if:

- Phase 4 applied the predeclared rule exactly;
- the final label is supported by Phase 0--4 artifacts;
- the result does not claim posterior correctness, exact nonlinear likelihood
  correctness, production HMC readiness, or that the stopped partial derivative
  route is a score;
- runtime caveats and the serial-FD interruption are plainly recorded.

Block if:

- any direction fails the stated rule;
- the final label overclaims beyond the artifacts;
- the result hides the expensive FD diagnostic or the kappa one-window caveat;
- the result uses soft language to avoid saying what passed and what did not.

## Requested Verdict

Findings first if any.  End with exactly:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
