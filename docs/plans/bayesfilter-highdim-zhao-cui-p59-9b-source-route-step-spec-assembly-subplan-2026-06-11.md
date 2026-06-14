# P59-9b Subplan: Source-Route Step-Spec Assembly

metadata_date: 2026-06-11
status: PLAN_DRAFT_FOR_CLAUDE_REVIEW

## Question

Can the fitted 36D author-SIR transport artifacts be assembled into
`SourceRouteSequentialStepSpec` objects that preserve the author current and
previous state ordering?

## Prerequisite Route Gate

P59-9b must not run until P59-9c has emitted a route decision.  For the author
Austria SIR row, `eg3_sir/mainscript.m` launches `full_sol`, so 9b may assemble
the full source route only after 9c records `full_route_selected`.

If 9c records `preconditioned_route_required`, 9b must block until its tasks are
rewritten to consume P57-M8 preconditioned maps and `pre_sol` anchors.

## Source Contract

`full_sol.solve` and `full_sol.reapprox` require a consecutive sequence of
per-time SIRT objects, affine frames, retained samples, proposal-correction
weights, and previous retained marginal evidence for `t > 1`.

## Tasks

1. Consume only P59-9a fit artifacts with source-route provenance and the
   P59-9c `full_route_selected` decision for the author SIR row.
2. Build `SourceRouteSequentialDensityComponents` for author SIR with:
   - `parameter_dim = 0`;
   - `state_dim = 18`;
   - transition and likelihood callbacks bound to the author model and
     observations.
3. Build consecutive `SourceRouteSequentialStepSpec` rows with:
   - `SourceRouteTarget`;
   - `SourceRouteTransportProtocol` wrapping fixed-TT/SIRT transports;
   - frozen reference samples;
   - measure convention;
   - previous marginal keep/input axes for `t > 1`.
4. Confirm that `previous_marginal_keep_axes` preserves the
   `[theta, x_{t-1}]` prefix and that `previous_marginal_input_axes` points to
   the previous-state coordinates inside `[theta, x_t, x_{t-1}]`.
5. Write an assembly manifest that P58's readiness guard can consume.

## Pass Criteria

`PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` requires at least a bounded
two-step author-SIR source-route step-spec sequence with no contract doubles and
with previous-marginal axes checked.

## Vetoes

- step specs built from old local/operator/all-grid routes;
- time-2 spec without previous marginal evidence;
- any 18D transition-only spec labeled as source-route reapproximation.
- missing P59-9c route decision.

## Initial Token

`PLAN_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY`
