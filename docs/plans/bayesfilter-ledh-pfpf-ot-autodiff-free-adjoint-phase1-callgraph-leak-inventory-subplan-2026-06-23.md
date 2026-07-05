# Phase 1 Subplan: Callgraph Leak Inventory

status: DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P1-CALLGRAPH-LEAK-INVENTORY

## Phase Objective

Build an exact production callgraph from the SIR actual-gradient harness to
LEDH-PFPF-OT transport and classify every autodiff usage as production leak,
custom-gradient boundary, or diagnostic/test-only.

## Entry Conditions

- P0 contract passed.
- Inherited state remains `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED`.
- No GPU/FD run is authorized.
- Production-vs-diagnostic boundary is fixed.
- No production LEDH-PFPF-OT gradient artifact may count unless the selected
  route passes an explicit no-autodiff audit bound to the exact same route
  manifest.

## Required Artifacts

- Route binding section in the result, anchored to:
  - P0 contract:
    `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-contract-2026-06-23.md`;
  - inherited state: `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED`;
  - exact SIR actual-gradient harness symbol/path and concrete command path
    used for this inventory;
  - exact current route bound by path, symbol, and call chain.
  If a Phase 8 route manifest does not exist yet, P1 must record
  `ROUTE_MANIFEST_NOT_YET_CREATED_P1`, but this marker is valid only after the
  current route is pinned by exact harness symbol/path, concrete command path,
  and path/line-anchored call chain.  If P1 cannot identify those route
  bindings, P1 is blocked.
- Path/line-anchored production callgraph section in the leak ledger, covering
  entrypoint to intermediate wrappers/callbacks to LEDH-PFPF-OT transport.
- Leak ledger: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-autodiff-leak-ledger-2026-06-23.md`
- Result: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-result-2026-06-23.md`
- Refreshed Phase 2 subplan if inventory changes audit needs.

## Required Checks/Tests/Reviews

- `rg` source scan for the forbidden API/pattern set below in production,
  benchmark, test, script, and callback/helper files that are reachable from or
  adjacent to the selected SIR actual-gradient route.
- Exact path/line anchors for each leak.
- Scope ledger that records included/excluded roots and why excluded roots are
  unreachable or irrelevant to the selected route.
- Bounded Claude review of the leak ledger/result.

## Forbidden API/Pattern Scan Set

P1 must scan and classify exact occurrences of:

- `tf.GradientTape`;
- `GradientTape(`;
- `.gradient(`;
- `.jacobian(`;
- `.batch_jacobian(`;
- `tf.gradients`;
- `tf.autodiff.ForwardAccumulator`;
- `ForwardAccumulator(`;
- `tf.custom_gradient`;
- `@tf.custom_gradient`;
- `gradient_override_map`;
- `RegisterGradient`;
- `custom_gradient`;
- `watch(` where associated with TensorFlow autodiff;
- helper/callback names that route gradients through any of the above.

P1 may add additional patterns if discovered by callgraph inspection, but must
record them in the leak ledger before using them as promotion or veto evidence.

## Classification Rubric

Each occurrence must be classified as exactly one of:

- `production_leak`: reachable from the selected production route and uses a
  forbidden autodiff API, including helper/callback-mediated use.
- `custom_gradient_boundary`: a `tf.custom_gradient` boundary reached by the
  production route.  This is not automatically a pass; it is a P2/P6 audit item
  until its `grad` body is proven manual and free of forbidden autodiff.
- `diagnostic_or_test_only`: exact-path or exact-symbol occurrence outside the
  production route, with evidence that it is not imported into or called by the
  production route.  This can explain diagnostics only and cannot certify
  no-autodiff.
- `unreachable_or_irrelevant`: occurrence outside the selected route and not a
  diagnostic used by this program, with a reason for exclusion.
- `production_leak_or_boundary_unknown`: temporary unresolved status for an
  ambiguous occurrence whose reachability or classification cannot yet be
  proven.  This is a blocker status, not a pass.

Any ambiguous occurrence defaults to `production_leak_or_boundary_unknown`.
P1 may advance only if each such occurrence is carried forward as an explicit
P2 audit blocker with exact path/line anchor and required audit action.

## Per-Finding P2 Audit Payload

For every occurrence, the leak ledger must provide:

- exact path and line;
- exact symbol/API/pattern;
- route reachability status and evidence;
- classification from the rubric;
- why the occurrence matters or does not matter for no-autodiff certification;
- exact audit action required in P2, such as static block, runtime sentinel,
  whitelist entry review, custom-gradient `grad` body inspection, or callback
  reachability proof.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Where does autodiff enter the current LEDH production gradient path? |
| Baseline/comparator | P0 contract and inherited `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED` route state. |
| Primary criterion | The leak ledger contains an exact route-binding section, path/line-anchored production callgraph, explicit scope ledger, every forbidden API/pattern occurrence in scoped files classified by the rubric, and a per-finding P2 audit payload. |
| Veto diagnostics | Broad whitelist; missing P0 route binding; missing callgraph section; missing forbidden scan pattern; missing route anchor; ignoring callbacks; classifying production code as diagnostic without evidence; ambiguous occurrence not carried as blocker. |
| Explanatory only | Counts of occurrences by file. |
| Not concluded | No leak fixed yet; no route certified. |

## Forbidden Claims/Actions

- Do not fix implementation in P1 except obvious documentation corrections.
- Do not call any leak harmless without boundary evidence.
- Do not run GPU or FD.
- Do not claim any current route is no-autodiff.
- Do not whitelist production occurrences in P1.
- Do not treat `custom_gradient_boundary` as a pass without later manual
  `grad`-body audit.

## Exact Next-Phase Handoff Conditions

Advance to P2 only if the leak ledger names the route binding, production
callgraph, scope ledger, forbidden occurrence classifications, and exact P2
audit payload for each finding, and the Phase 2 subplan can implement those
audit requirements.

## Stop Conditions

- Callgraph cannot be pinned.
- Forbidden API scan is too broad or too narrow to support audit tooling.
- Route binding cannot identify the selected SIR actual-gradient harness.
- Route binding cannot identify the exact harness symbol/path, concrete command
  path, and path/line-anchored call chain.
- Any ambiguous occurrence cannot be classified or carried as an explicit P2
  blocker.
- Claude review fails to converge.
