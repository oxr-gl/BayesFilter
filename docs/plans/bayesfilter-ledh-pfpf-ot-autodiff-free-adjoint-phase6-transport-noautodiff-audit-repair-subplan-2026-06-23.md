# Phase 6 Subplan: Transport No-Autodiff Audit And Repair

status: REFRESHED_AFTER_P5_DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P6-TRANSPORT-NOAUTODIFF-AUDIT-REPAIR

## Phase Objective

Audit and repair the transport custom-gradient route so its forward and
manual `grad` body do not use autodiff and can compose into the filter-level
manual adjoint.  P6 owns closure of P1-L013/P1-L015.

## Entry Conditions

- P5 primitive adjoints passed.
- P2 audit tool is active.
- P6 inherits the P3 transport/Sinkhorn/blockwise adjoint contract and P5
  cotangent shapes.
- P5 provides non-transport primitive boundaries for Gaussian log-density VJP,
  named transition/observation log-density VJPs, log-normalization with
  likelihood-increment cotangent, fixed floor-mask VJP, log-weight correction
  signs, observation residual conventions, and linearized LEDH flow VJP.
- P6 begins with the current route still failed by P2 for P1-L013/P1-L015.
- GPU ladder, FD, N10000 actual-gradient validation, and filter-level
  certification remain forbidden in P6.

## Required Artifacts

- Transport audit result.
- Implementation diffs if leaks or excessive state are found.
- Focused transport tests.
- P6 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-result-2026-06-23.md`.
- Refreshed P7 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-subplan-2026-06-23.md`.
- Route-manifest draft section identifying the exact transport gradient mode,
  `transport_ad_mode`, chunk sizes, stopped scale/key policy, and audit result
  path to be consumed by P7/P8.
- Exact transport helper/body classification for the old replay route and the
  candidate blockwise manual VJP route.

## Required Checks/Tests/Reviews

- Static custom-gradient body scan.
- Runtime sentinel around transport route.
- Existing transport primitive tests.
- Focused tests for softmin VJP, transport-from-potentials VJP, finite
  Sinkhorn reverse scan, padding/mask behavior, and no dense retained state.
- Focused source scan proving the selected transport `grad` body does not open
  `tf.GradientTape`, `ForwardAccumulator`, `.gradient`, or `.jacobian`.
- P2 audit must either pass the repaired/candidate transport route or continue
  to fail with exact remaining leak IDs.
- Bounded Claude review.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is transport manual VJP genuinely no-autodiff and suitable for filter-level composition? |
| Baseline/comparator | P3 transport contract, current failed manual streaming finite route, candidate blockwise VJP route, and S7R N2500 OOM trace. |
| Primary criterion | Transport route passes no-autodiff grad-body audit and focused tests without using `transport_ad_mode=full`; P1-L013/P1-L015 are closed or remain explicit blockers. |
| Veto diagnostics | Custom grad body opens tape; dense transport materialized; hidden raw autodiff fallback; candidate route selected by name without grad-body audit; route switches scalar semantics. |
| Explanatory only | CPU-only local timing or allocation notes from focused tests.  No GPU execution is allowed in P6. |
| Not concluded | Full filter route works. |
| Preserved artifact | P6 result artifact path listed above. |

## Forbidden Claims/Actions

- Do not solve N2500 by switching to `transport_ad_mode=full`.
- Do not run GPU ladder.
- Do not change route semantics without derivation update.
- Do not treat `tf.custom_gradient` or the name
  `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys` as a
  pass without inspecting the `grad` body.
- Do not use Zhao-Cui, FD, or tiny autodiff parity as a production oracle.
- Do not claim P6 certifies the full filter-level no-autodiff route; P7/P8 own
  that composition and audit.
- Do not modify P5 non-transport primitive helpers in P6.  If a P5 primitive
  boundary defect is discovered, write an external blocker or P5 remediation
  note instead of absorbing that repair into P6.

## Exact Next-Phase Handoff Conditions

Advance to P7 only if transport can be called by a filter-level manual adjoint
without production autodiff, the exact transport route fields are pinned for a
P7 route manifest, and P2/P6 audit output records whether P1-L013/P1-L015 are
closed or still blocking.

## Stop Conditions

- Transport grad body still needs autodiff.
- Dense transport storage reappears.
- Claude review fails to converge.
- The only feasible repair path is `transport_ad_mode=full`.
- The candidate route changes the scalar, branch, stopped-key/scale policy, or
  route manifest without a derivation update.
- P6 would require GPU, FD, actual-gradient, or full filter certification to
  pass.
