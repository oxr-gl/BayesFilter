# Phase 2 Subplan: Audit Tooling

status: DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P2-AUDIT-TOOLING

## Phase Objective

Implement a hard no-autodiff audit tool and runtime sentinel that can fail the
production LEDH route before GPU/FD validation.

## Entry Conditions

- P1 leak ledger passed review.
- Audit requirements are exact and source-anchored.
- P2 must consume P1 leak IDs P1-L001 through P1-L030 from
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-autodiff-leak-ledger-2026-06-23.md`.
- Current reviewed route remains blocked by outer autodiff and transport
  custom-gradient `grad` autodiff.
- No implementation repair, GPU rung, or FD run is authorized.

## Required Artifacts

- Audit script:
  `scripts/audit_ledh_no_autodiff.py`.
- Focused audit tests:
  `tests/test_audit_ledh_no_autodiff.py`.
- Exact whitelist artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json`.
- Route manifest/input fixture:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json`.
- Audit result JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-result-2026-06-23.json`.
- P2 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-result-2026-06-23.md`.
- Refreshed P3 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-subplan-2026-06-23.md`.
- Route manifest stub or audit input fixture binding the current P1 route:
  command path, route flags, production callgraph files, forbidden pattern set,
  and P1 leak IDs.

## Minimal Artifact Schemas

Whitelist JSON minimum fields:

- `schema_version`;
- `zero_default: true`;
- `entries`, each with exact `path` or exact `symbol`, classification,
  diagnostic/test-only reason, and related P1 IDs;
- `forbidden`: no directory-wide entries and no production-route module
  entries.

Route manifest/input JSON minimum fields:

- `schema_version`;
- `route_id`;
- `command_path`;
- `route_flags`;
- `production_files`;
- `diagnostic_or_test_files`;
- `forbidden_patterns`;
- `p1_leak_ids`;
- `expected_negative_control_failures`.

Audit result JSON minimum fields:

- `schema_version`;
- `route_id`;
- `decision`, expected to be `FAIL_CURRENT_ROUTE`;
- `failed_p1_ids`;
- `diagnostic_whitelist_hits`;
- `production_whitelist_vetoes`;
- `bad_route_flag_vetoes`;
- `custom_gradient_boundary_results`;
- `runtime_sentinel_result`;
- `nonclaims`.

## Required Audit Semantics

The audit tool must support at least these checks:

- `static_forbidden_api_scan`: scan exact production-route files for forbidden
  APIs and classify findings using P1 IDs.
- `custom_gradient_grad_body_scan`: inspect `tf.custom_gradient` boundaries and
  fail any production-reachable `grad` body containing `tf.GradientTape`,
  `ForwardAccumulator`, `.gradient`, `.jacobian`, or `.batch_jacobian`.
- `route_flag_gate`: reject production manifests selecting
  `transport_ad_mode=full`, `ad_evaluation_mode=reverse-gradient`,
  `ad_evaluation_mode=forward-jvp`, or `transport_gradient_mode=filterflow_custom_op`.
- `zero_default_whitelist`: allow diagnostic/test-only forbidden API
  occurrences only by exact path or exact symbol, never by directory.
- `production_whitelist_veto`: reject whitelist entries that cover production
  modules or production-route symbols.
- `runtime_sentinel`: provide a visible mechanism to fail if a production route
  opens `tf.GradientTape` or `tf.autodiff.ForwardAccumulator`.

The first expected P2 audit result is a negative control: the audit must fail
the current P1 route for P1-L001/P1-L003 and P1-L013/P1-L015.

## P1 Crosswalk For P2 Negative Control

| P1 IDs | Classification | File/symbol | Audit rule | Expected P2 status |
|---|---|---|---|---|
| P1-L001, P1-L002, P1-L003 | `production_leak` | `benchmark_p8p_regression_fd_reparameterization.py` outer `tf.GradientTape` route | `static_forbidden_api_scan`, `runtime_sentinel`, `route_flag_gate` | FAIL current route |
| P1-L013, P1-L014, P1-L015 | `production_leak` | `annealed_transport_tf.py` manual streaming finite custom-gradient `grad` body | `custom_gradient_grad_body_scan`, `static_forbidden_api_scan` | FAIL current route |
| P1-L012 | `custom_gradient_boundary` | manual streaming finite `@tf.custom_gradient` boundary | `custom_gradient_grad_body_scan` | FAIL because `grad` body contains P1-L013/P1-L015 |
| P1-L016 | `custom_gradient_boundary` | blockwise manual VJP `@tf.custom_gradient` boundary | `custom_gradient_grad_body_scan` | CANDIDATE only if `grad` body scan passes; not certified in P2 |
| P1-L004 | `production_leak_or_boundary_unknown` | forward-JVP selectable route | `route_flag_gate` | FAIL as production flag unless exact diagnostic whitelist |
| P1-L005 through P1-L008 | `production_leak_or_boundary_unknown` | P8p helper `_gradient_diagnostic` | `static_forbidden_api_scan`, whitelist governance | FAIL unless proven outside production route |
| P1-L009 through P1-L011 | `diagnostic_or_test_only` | isolated observation-noise diagnostic | `zero_default_whitelist` | ALLOW only exact diagnostic entry |
| P1-L017 through P1-L020, P1-L025 | mixed unreachable/boundary | dense/custom-op transport helpers | `route_flag_gate`, `custom_gradient_grad_body_scan` | FAIL if selected by production manifest |
| P1-L021 through P1-L028 | `production_leak_or_boundary_unknown` | production-module score helpers/imports | `static_forbidden_api_scan`, `production_whitelist_veto` | FAIL unless exact non-production proof exists |
| P1-L029, P1-L030 | `diagnostic_or_test_only` | test-only autodiff comparisons | `zero_default_whitelist` | ALLOW only exact test-path entry |

## Runtime Sentinel Activation Contract

The runtime sentinel must be implemented as an explicit audit-only context or
wrapper, not as a global permanent monkeypatch.

Minimum behavior:

- enabled only by the audit script or focused tests;
- patches or wraps `tf.GradientTape` and `tf.autodiff.ForwardAccumulator`
  within the sentinel context;
- receives a manifest route ID and production/diagnostic boundary;
- raises or records a hard failure if production-route execution opens a tape
  or forward accumulator;
- permits diagnostic/test-only code only when the manifest and whitelist mark
  that exact path/symbol as diagnostic;
- is not used as proof that a route is no-autodiff unless paired with the
  static audit and route manifest checks.

P2 may implement only a focused sentinel smoke test if executing the full
production route would require GPU or long runtime.  The smoke must still prove
that forbidden runtime APIs fail under the sentinel.

## Required Checks/Tests/Reviews

- Static scan test proves forbidden APIs fail in production path.
- Static scan must fail the current reviewed route because P1-L001/P1-L003 are
  direct outer production autodiff leaks.
- Static scan must fail the manual streaming finite transport route because
  P1-L013/P1-L015 open autodiff inside a custom-gradient `grad` body.
- Test proves `tf.custom_gradient` boundaries are not treated as a pass unless
  their `grad` bodies are scanned.
- Test proves `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`
  remains a candidate boundary only after P1-L016 `grad`-body audit.
- Test proves `transport_ad_mode=full`, reverse-gradient, forward-JVP, and
  `filterflow_custom_op` are rejected for production manifests.
- Whitelist test proves diagnostics/tests are allowed only by exact path.
- Test proving production modules cannot be whitelisted for forbidden autodiff
  APIs.
- Runtime sentinel test proves production route cannot open `GradientTape` or
  `ForwardAccumulator`.
- Bounded Claude review of the audit result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can local tooling detect and block production autodiff leakage? |
| Baseline/comparator | P1 leak ledger. |
| Primary criterion | Audit tool, tests, whitelist artifact, route manifest stub/input, and audit result exist; the audit fails the current P1 route for P1-L001/P1-L003 and P1-L013/P1-L015; tests prove custom-gradient `grad` bodies, route flags, whitelist governance, production whitelist veto, and runtime sentinel behavior. |
| Veto diagnostics | Audit passes current P1 route; audit skips production files; audit treats `tf.custom_gradient` as automatic pass; whitelist allows broad directories or production modules; route flags can select reverse-gradient, forward-JVP, `filterflow_custom_op`, or `transport_ad_mode=full`; runtime sentinel absent. |
| Explanatory only | Occurrence counts and diagnostic-only matches. |
| Not concluded | No implementation is no-autodiff yet. |

## Forbidden Claims/Actions

- Do not weaken the audit to pass current code.
- Do not move production files into diagnostic whitelist.
- Do not use directory-wide whitelists for forbidden autodiff APIs.
- Do not run GPU/FD.
- Do not implement the no-autodiff production route in P2.
- Do not claim any current route is no-autodiff because the audit tool exists.
- Do not classify `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`
  as certified until its custom-gradient `grad` body is audited.

## Exact Next-Phase Handoff Conditions

Advance to P3 only if the audit tool exists, fails current leaks as expected,
tests pass, the result records how later phases must use it, the P3 subplan is
refreshed to consume the audit contract, and bounded Claude review agrees.

## Stop Conditions

- Audit cannot distinguish production from diagnostic code.
- Runtime sentinel is infeasible without broad invasive changes.
- Current leaking route unexpectedly passes the audit.
- Whitelist cannot remain zero-default and exact-path/exact-symbol.
- Custom-gradient `grad` bodies cannot be inspected without implementing route
  repairs.
- Claude review fails to converge.
