# Manual Adjoint Phase 1 Result: Derivation And Chapter Contract

status: COMPLETE_REVIEWED
date: 2026-06-22
phase: M1-DERIVATION

## Question

What exact finite LEDH-PFPF-OT transport scalar and primitive adjoints should
the manual/custom-gradient route implement and test?

## Short Answer

M1 defines a narrow first target:

```text
manual_dense_finite_sinkhorn_stopped_scale_keys
```

This is a dense, tiny/small, finite Sinkhorn primitive route for M2 tests.  It
is not the exact regularized OT optimizer, not a streaming route, not a public
API, and not a governed `N=10000` actual-gradient route.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Question | Answered for M2 primitive planning. |
| Baseline/comparator | Existing finite dense Sinkhorn/barycentric code path plus tiny TensorFlow autodiff/FD references for M2. |
| Primary criterion | Passed: derivation contract states scalar, variables, primitive adjoints, stopped/frozen quantities, unsupported modes, and M2 parity tests. |
| Veto status | No veto.  The contract explicitly avoids exact-OT conflation, raw full-AD N10000, streaming claims, and public/default integration. |
| Explanatory diagnostics | Code anchors, shape table, primitive equations, and tolerance handoff. |
| Not concluded | No manual-adjoint correctness, code implementation, streaming memory improvement, P82 validation, HMC/default/posterior readiness. |

## Skeptical Plan Audit

The M1 plan passes because it answers a derivation-boundary question only.  It
does not run GPU work, does not launch a numerical experiment, does not promote
proxy metrics, and does not claim correctness from equations alone.

The main risks were:

- deriving the exact regularized OT optimizer instead of the finite code path;
- leaving the scalar ambiguous;
- allowing the known-bad `transport_ad_mode=full` N10000 route back in;
- claiming streaming memory before a measured streaming route exists.

The derivation contract mitigates these risks by anchoring to current code paths
and by making dense tiny finite primitives the only M2 target.

## Artifacts

- Derivation contract:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md`
- Refreshed M2 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-subplan-2026-06-22.md`

## M2 Handoff

M2 may proceed to primitive dense tests only if local checks pass.  M2 must test:

- barycentric projection VJP;
- dense log-domain softmin VJP;
- dense transport-from-potentials VJP;
- finite Sinkhorn loop VJP/JVP on tiny dense fixed-iteration fixtures;
- scalar directional finite-difference spot checks;
- unsupported-route rejection.

M2 must use the M1 route name and tolerances unless it patches the subplan
before execution.

## Claude R1 Review And Patch

Claude read-only review returned `VERDICT: REVISE`.

Material findings were:

- name the tiny full-graph AD/JVP/VJP oracle baseline explicitly;
- sharpen the nonclaim that M1/M2 do not establish a memory-disciplined route;
- add M2 advancement and stop rules;
- separate primitive adjoint derivability from memory discipline;
- state that M2 validates frozen-control finite loops, not adaptive stopping;
- label M2 as CPU/float64 oracle-style validation, not GPU/TF32 evidence;
- name the M2 result artifact;
- cite prior runtime blocker artifacts for the raw full-AD N10000 exclusion.

Patches applied:

- updated the derivation contract with prior evidence anchors, M2 oracle
  baseline, environment boundary, frozen-control boundary, memory-discipline
  boundary, M2 advancement rule, and M2 evidence destination;
- updated the M2 subplan with the oracle baseline, CPU/float64 boundary,
  advancement rule, and P82 nonclaim.

R2 review returned `VERDICT: AGREE`.  A non-blocking suggestion to add explicit
stop language was applied to the derivation contract and M2 subplan.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept M1 derivation contract | Passed after R1 patch and R2 review | No veto | Whether primitive implementation will match tiny autodiff/JVP/VJP | Start M2 primitive VJP phase under its subplan | No implementation correctness |
| Keep P82 blocked | Passed | Raw full-AD N10000 remains forbidden | Whether manual route can scale | Continue M2-M7 gates | No P82 FD agreement |

## Nonclaims

This result does not conclude manual-adjoint correctness, implementation
readiness, streaming memory improvement, SIR d18 readiness, P82 FD agreement,
HMC/NUTS readiness, posterior correctness, exact likelihood correctness,
default-gradient readiness, or production readiness.
