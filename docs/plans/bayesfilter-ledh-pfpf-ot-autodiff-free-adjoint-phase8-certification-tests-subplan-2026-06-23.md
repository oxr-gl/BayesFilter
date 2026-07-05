# Phase 8 Subplan: Certification Tests

status: REFRESHED_AFTER_P7_DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P8-CERTIFICATION-TESTS

## Phase Objective

Certify the exact opt-in LEDH-PFPF-OT P8p SIR manual route as no-autodiff
before any GPU ladder, finite-difference comparison, N10000 actual-gradient
run, default-route change, or scientific claim.

P8 is not allowed to inherit P7's broad `FAIL_CURRENT_ROUTE` audit as a pass.
It must either produce a passing no-autodiff audit for the exact selected route
or write a blocker result.

## Entry Conditions

- P7 implemented an opt-in `--ad-evaluation-mode manual-reverse` route.
- P7 focused tests passed under CPU-hidden local execution.
- P7 runtime sentinel smoke passed for the selected manual route.
- P7 audit artifact exists at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-current-route-audit-result-2026-06-23.json`.
- The P7 audit artifact records `failed_p1_ids: []` and no bad route flag
  vetoes, but still records broad production static findings and one unselected
  tape-backed custom-gradient boundary.
- P1-L013/P1-L015 remain closed for the selected manual streaming finite
  transport route.

## Required Artifacts

- P8 exact route manifest at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json`,
  including:
  - git commit;
  - production entrypoint;
  - selected route name;
  - exact command flags;
  - `ad_evaluation_mode: manual-reverse`;
  - `transport_plan_mode: streaming`;
  - `transport_ad_mode: stabilized`;
  - selected manual streaming transport gradient mode;
  - dtype/TF32 policy;
  - chunk sizes;
  - seed list and seed aggregation policy;
  - audit script path/hash or version;
  - whitelist path/hash;
  - runtime sentinel command;
  - audit result path.
- Refined audit result JSON with decision `PASS_NO_AUTODIFF_AUDIT`, or a
  blocker result explaining why certification cannot pass.
- Focused certification tests for route flags, static scan, custom-gradient
  grad-body scan, runtime sentinel, and route-manifest validation.
- P8 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-result-2026-06-23.md`.
- Refreshed P9 GPU-ladder subplan only if P8 passes.

## Required Checks/Tests/Reviews

- CPU-hidden compile checks for changed implementation/audit/test files.
- Focused pytest for:
  - P7 manual score route;
  - audit governance;
  - P8 route-manifest validation;
  - runtime sentinel coverage.
- Static no-autodiff audit command for the exact P8 route manifest.
- Runtime sentinel execution of the selected route with tiny CPU-hidden
  parameters.
- `git diff --check` for touched files.
- Bounded exact-path Claude review of the P8 result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the exact selected manual LEDH-PFPF-OT route pass static and runtime no-autodiff certification? |
| Baseline/comparator | P7 manual route and P2/P7 audit artifacts. |
| Primary criterion | The exact P8 route manifest passes `PASS_NO_AUTODIFF_AUDIT`, runtime sentinel runs the selected route without forbidden API calls, and focused tests pass. |
| Veto diagnostics | Any selected-route forbidden API; any selected custom-gradient `grad` body opens autodiff; broad whitelist or production whitelist; route flag selects `reverse-gradient`, `forward-jvp`, `filterflow_custom_op`, or `transport_ad_mode=full`; route manifest incomplete; runtime sentinel absent; diagnostic autodiff promoted as proof; audit pass reused for a different route. |
| Explanatory only | Tiny diagnostic autodiff parity, CPU-only timings, P7 broad failure count, old diagnostic helper locations. |
| Not concluded | GPU feasibility, N10000 feasibility, FD agreement, HMC readiness, posterior correctness, production default, or scientific validity. |

## Required Certification Repairs To Consider

P8 may use only reviewed local repairs that make the audit more precise or the
route cleaner.  Candidate repairs are:

- split or classify diagnostic autodiff helpers so the production route
  manifest no longer treats reverse/JVP diagnostics as selected production
  code;
- make the audit distinguish allowed manual `tf.custom_gradient` boundaries
  from forbidden custom-gradient bodies, with exact boundary records and clean
  grad-body scans;
- route-flag-veto unselected legacy `filterflow_custom_op` rather than
  treating it as selected production evidence;
- add route-manifest validation that binds the audit pass to
  `manual-reverse`, streaming transport, stabilized transport AD mode, and
  manual streaming transport gradients;
- expand runtime sentinel tests so the exact selected route executes under the
  sentinel.

Any repair that broadens a whitelist, hides a production forbidden API,
changes default policy, or weakens the no-autodiff definition is forbidden.

## Forbidden Claims/Actions

- Do not run GPU ladder or FD checks in P8.
- Do not claim P8 passed unless the exact audit decision is
  `PASS_NO_AUTODIFF_AUDIT`.
- Do not use Zhao-Cui as comparator or oracle.
- Do not use `transport_ad_mode=full`.
- Do not make `manual-reverse` the default route.
- Do not whitelist production files or directory prefixes.
- Do not treat tiny autodiff parity as certification.
- Do not change pass/fail criteria after seeing audit failures without a
  visible repair note and focused rerun.

## Exact Next-Phase Handoff Conditions

Advance to P9 only if:

- P8 result decision is `PASSED`;
- exact route manifest path and audit result path are recorded;
- audit result decision is `PASS_NO_AUTODIFF_AUDIT`;
- runtime sentinel route execution passed;
- focused local checks passed;
- Claude review returns `VERDICT: AGREE`;
- refreshed P9 subplan binds every GPU rung to the same route manifest and
  audit artifact.

## Stop Conditions

- Static audit cannot pass without weakening the no-autodiff contract.
- Runtime sentinel cannot execute the selected route without forbidden API use.
- The selected route requires `reverse-gradient`, `forward-jvp`,
  `filterflow_custom_op`, or `transport_ad_mode=full`.
- Audit changes would need broad whitelisting or production-path exceptions.
- Claude review returns `VERDICT: REVISE` for the same blocker five times.
- Continuing would require GPU, FD, N10000, default-policy, package,
  credential, network, model-file, or scientific-claim boundary crossing.
