# P59-9c Subplan: Preconditioned Route Integration

metadata_date: 2026-06-11
status: PLAN_DRAFT_FOR_CLAUDE_REVIEW

## Question

Does the author-SIR Phase 9 row use the full source route or the
preconditioned Algorithm-5 route, and if preconditioned route is required, is
the P57-M8 surface wired into the actual M9 step-spec assembly?

## Source Contract

- Full route source: `models/full_sol.m`.
- Preconditioned route source: `models/pre_sol.m`.
- Linear preconditioner source: `models/tensordot/precond.m`.

## Tasks

1. Declare row-level route choice for M9:
   - `full_route_selected`;
   - `preconditioned_route_required`;
   - or `preconditioned_route_deferred_with_source_reason`.
2. For the author Austria SIR row, check `eg3_sir/mainscript.m`; because it
   constructs `full_sol`, the expected P59-9c decision is
   `full_route_selected` unless a source-cited contrary requirement is found.
3. If preconditioned route is required, consume P57-M8's preconditioned map and
   proposal-correction surface in the author-SIR step-spec path.
4. If not required for the first bounded d=18 launch, record why `full_sol`
   source route is the launch route.
5. Preserve P58 readiness status:
   - `preconditioned_route_required = false` for full route; or
   - `preconditioned_route_required = true` plus
     `PASS_P57_M8_PRECONDITIONED_ALGORITHM5`.
6. Emit the route-decision artifact before P59-9b starts.  P59-9b and P59-9d
   must block if this artifact is absent.

## Pass Criteria

`PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION` requires an explicit source-based
route choice and, when needed, executable wiring into the M9 manifest path.

## Vetoes

- treating P57-M8 algebraic tests as actual M9 integration when no step specs
  use the route;
- silently switching routes for performance;
- using UKF as a route substitute.
- allowing P59-9b or P59-9d to pass before this route decision exists.

## Initial Token

`PLAN_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION`
