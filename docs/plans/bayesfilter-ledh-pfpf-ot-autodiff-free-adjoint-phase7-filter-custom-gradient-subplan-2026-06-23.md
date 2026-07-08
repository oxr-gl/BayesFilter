# Phase 7 Subplan: Filter-Level Custom Gradient

status: REFRESHED_AFTER_P6_DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P7-FILTER-CUSTOM-GRADIENT

## Phase Objective

Implement the production filter-level manual route with a manual reverse-time
scan and no production autodiff, replacing the remaining outer objective tape
leaks P1-L001/P1-L003.

## Entry Conditions

- P6 transport no-autodiff gate passed for the selected manual streaming
  finite transport route.
- P5 primitive adjoints passed and P7 must inherit those boundaries.
- P2 audit tool is active.
- P7 begins with the current route still failed only for P1-L001/P1-L003 in
  the reviewed manifest.
- P1-L013/P1-L015 are closed for the selected transport route and must not be
  reopened.
- GPU, FD, actual-gradient validation, and certification tests remain
  forbidden in P7.

## Required Artifacts

- Implementation diffs.
- New opt-in route metadata.
- Focused unit/integration tests.
- P7 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-result-2026-06-23.md`.
- Refreshed P8 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-subplan-2026-06-23.md`.
- Route-manifest draft with exact production entrypoint, route flags,
  transport mode, dtype/TF32 policy, chunk sizes, seed aggregation, and audit
  path.

## Required Checks/Tests/Reviews

- CPU-hidden route-selection tests.
- Runtime sentinel proving no forbidden autodiff APIs execute.
- Static audit on changed files.
- Focused tests for manual seed-weighted objective aggregation and reverse
  scan on tiny fixed-branch cases.
- P2 audit must show P1-L001/P1-L003 are closed for the new exact route or
  remain explicit blockers.
- Bounded Claude implementation/result review.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the LEDH-PFPF-OT value expose an opt-in manual production score route that does not need the outer objective tape? |
| Baseline/comparator | Prior S7R route with outer `GradientTape`; P5/P6 manual primitive boundaries. |
| Primary criterion | New opt-in route computes finite tiny manual scores and route-bound audit closes P1-L001/P1-L003 without reopening P1-L013/P1-L015. |
| Veto diagnostics | Outer tape remains required; hidden fallback; route default changed; audit bypassed; transport route regresses; P5/P6 boundaries modified without their own reviewed remediation; `transport_ad_mode=full`; GPU/FD/actual-gradient run. |
| Explanatory only | Tiny diagnostic parity, CPU-only timing, local runtime sentinel traces. |
| Not concluded | N10000 feasibility, FD agreement, HMC readiness, posterior correctness, production default, or scientific validity. |

## Forbidden Claims/Actions

- Do not make the new route default.
- Do not run GPU ladder before P8 certification.
- Do not use diagnostic autodiff in production.
- Do not repair P5 primitive helpers or P6 transport helpers in P7; write an
  external blocker if those inherited boundaries prove insufficient.
- Do not use `transport_ad_mode=full`, Zhao-Cui as comparator, FD, or tiny
  autodiff parity as production proof.

## Exact Next-Phase Handoff Conditions

Advance to P8 only if the route is opt-in, finite on tiny checks, route-bound
audit closes P1-L001/P1-L003, P1-L013/P1-L015 remain closed, and the P8
subplan has an exact certification manifest/check contract.

## Stop Conditions

- Manual reverse scan cannot be implemented without broad redesign.
- Audit detects production autodiff and fix is not local.
- P7 would need GPU, FD, actual-gradient, default-route change, P5 repair, or
  P6 transport repair to pass.
