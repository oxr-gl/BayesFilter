# Visible Stop Handoff: Total-VJP GPU/XLA Validation

Date: 2026-07-01

Status: `COMPLETE`

## Current State

The governed execution program completed through Phase 5.

Final label:

`GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE_WITH_RAW_DIRECTION_GATE_PASS`

Final result:

`docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-result-2026-07-01.md`

## Key Results

- Phase 0 proved the full-route dispatch and trusted GPU visibility.
- Phase 1 passed the tiny GPU/XLA full-route smoke.
- Phase 2 was skipped because no harness repair was needed.
- Phase 3 passed the particle ladder through `N=1000,T=3`.
- Phase 4 passed the same-scalar raw-direction FD gate with a runtime caveat.
- Claude read-only reviews agreed at the material gates.

## Important Caveats

- The route remains experimental.
- Phase 4 same-scalar FD at `N=1000,T=3` took about 50.5 minutes even after the
  batched-theta repair.
- This does not prove posterior correctness, exact nonlinear likelihood
  correctness, or full HMC production readiness.
- The stopped partial derivative route must not be called a score.

## Recommended Next Step

Build a cheaper same-scalar FD sentinel or an XLA/batched value comparator for
routine regression testing of the corrected full-route score.
