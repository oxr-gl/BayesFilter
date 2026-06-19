# P73 Phase 3 Result: Implementation Surface Audit And Focused Test Plan

metadata_date: 2026-06-17
status: PHASE3_PASSED_CLAUDE_AGREE_READY_FOR_PHASE4_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md

## Evidence Contract

| Field | Result |
| --- | --- |
| Scientific/engineering question | Which exact current code and test surfaces can implement the Phase 2 P73 contract without changing default policy or violating source-governance boundaries? |
| Exact baseline/comparator | Phase 2 design result and P72 real Phase 5 blocked diagnostic. |
| Primary pass/fail criterion | Every Phase 2 required operation is mapped to an implementation/test surface or an explicit implementation gap before code edits. |
| Veto diagnostics | Missing audit-exclusion surface; missing renewed-support provenance surface; density-aware objective mapped as default policy; NumPy selected for differentiable implementation; source-faithfulness overclaim; implementation edits or diagnostics launched in Phase 3. |
| Explanatory only | Estimated implementation size, local helper reuse opportunities, optional refactor notes, and future rank/degree work. |
| What will not be concluded | No implementation correctness, no lower-gate pass, no validation, no HMC readiness, no scaling, no rank promotion. |
| Artifact preserving result | This Phase 3 result, the Phase 4 subplan, the execution ledger, and the Claude review ledger. |

## Skeptical Plan Audit

Phase 3 passes the skeptical audit as an implementation-surface audit.  It
does not run diagnostics or tests beyond planning checks, does not edit
implementation code, and does not treat the existence of P72 helper functions
as evidence that P73 is already implemented.  The main proxy-metric risk is
the P73-B cross-entropy term: the current least-squares ALS fitter does not
solve a nonlinear density-aware objective merely because it can evaluate
residuals.  This result records that gap explicitly.

## Inspected Surfaces

Bounded read-only inspection covered:

- `bayesfilter/highdim/source_route.py:173-196`, P70/P72 thresholds and seeds;
- `bayesfilter/highdim/source_route.py:3673-4238`, P72 policy, training batch,
  support, line, normalizer, condition/effective-rank, provenance, and gate
  summary helpers;
- `bayesfilter/highdim/source_route.py:4460-4582`, private P70 rank-activity
  and fixed-fitting policy helpers used by existing diagnostics;
- `bayesfilter/highdim/fitting.py:39-194`, fit config, sample batch, and fit
  result contracts;
- `bayesfilter/highdim/fitting.py:221-350`, fixed-rank weighted ridge ALS
  fitting surface;
- `bayesfilter/highdim/fitting.py:947-1082`, objective-preserving scaled
  augmented ridge solve and singular-value diagnostics;
- `bayesfilter/highdim/squared_tt.py:112-194`, \(h_\theta^2+\tau q_0\)
  density, normalizer, and log-density surface;
- `scripts/p72_support_certified_lower_gate_diagnostic.py:231-350`, target
  values, residual gates, and normalizer terms;
- `scripts/p72_support_certified_lower_gate_diagnostic.py:396-820`, P72
  fit/gate row assembly;
- `tests/highdim/test_p72_support_certified_lower_gate.py:64-439`, current
  focused tests for P72 constants, audit exclusion, support, normalizer, line,
  condition, provenance, schema, and structured skip behavior;
- `bayesfilter/highdim/__init__.py:196-280` and `539-693`, current P72 exports.

No MathDevMCP check was required because Phase 3 introduced no new labeled
derivation or proof obligation.

## Implementation Surface Map

| Phase 2 operation | Current surface | Phase 4 mapping | Gap or guardrail |
| --- | --- | --- | --- |
| P73 policy and statuses | P72 constants and `p72_support_certified_policy` in `source_route.py:173-196`, `3673-3714` | Add P73-specific statuses, constants, and `p73_density_aware_renewal_policy()` near P72 helpers; export only subpackage symbols through `bayesfilter.highdim.__init__`. | Must preserve `lambda_ce = 0.1`, `R = 1`, P73-A mandatory, P73-B opt-in, and no rank promotion. |
| \(F_r,G_r,A_r,L_r,E_r,N_r\) role provenance | P72 provenance manifest records fit/guard/audit/line hashes but not per-point renewal rounds: `source_route.py:4140-4169` | Add P73 renewal-role manifest helpers that record `point_id`, `cloud_hash`, `role`, `created_round`, `entered_training_round`, `audit_round`, `source_channel`, `parent_point_ids`, and constructor labels. | P72 provenance is not enough; Phase 4 must not infer `NO_AUDIT_COEFFICIENT_SELECTION` from hash presence alone. |
| `NO_AUDIT_COEFFICIENT_SELECTION` | P72 training manifest records `audit_point_count_used_for_training = 0`: `source_route.py:3728-3783` | Add an explicit P73 predicate over renewal-role records and coefficient-selection hashes. | The predicate must fail closed if audit or audit-line roles enter the coefficient matrix, if audit hashes overlap training hashes, or if an enrichment point comes from audit. |
| P73-A renewal-only training batch | `FixedTTFitSampleBatch` in `fitting.py:111-154`; P72 fit+guard concatenation in `source_route.py:3728-3783` | Use a new P73 helper that builds a `FixedTTFitSampleBatch` from \(F_1\) only, with \(E_0\) and \(N_1\) already recorded as training-role points. | Do not reuse `p72_training_batch_from_fit_and_guard` for final P73 training, because round-1 \(G_1\) is an admission cloud, not same-round training data. |
| Square-root ALS fit for P73-A | `FixedTTFitter.fit` in `fitting.py:221-350`; scaled ridge solve in `fitting.py:947-1082` | Reuse the current TensorFlow ALS fitter and P70 config policy for P73-A. | This implements P73-A only.  It does not implement cross-entropy fitting. |
| Density object \(q_\theta\) and \(Z_\theta\) | `SquaredTTDensity.unnormalized_density`, `normalizer`, and `log_density` in `squared_tt.py:153-190` | Reuse `SquaredTTDensity` for finite \(q_\theta\), \(Z_\theta\), and normalizer terms. | `log_density` raises on normalizer-floor failure; Phase 4 must catch and report that as an arm block, not hide it with `eps_log`. |
| P73-B cross-entropy objective value | No current objective helper; `SquaredTTDensity.log_density` can evaluate \(q_\theta\) | Add `p73_density_aware_cross_entropy(...)` or equivalent TensorFlow helper with frozen `lambda_ce = 0.1` and no audit inputs. | Existing ALS cannot solve \(L_A+\lambda_{\rm ce}L_{\rm ce}\) by reweighting least squares.  Phase 4 must either implement a reviewed opt-in TensorFlow refinement step or mark P73-B optimizer unavailable. |
| P73-B nonlinear optimization | No current safe surface | Phase 4 may add a bounded, opt-in TensorFlow refinement surface initialized from P73-A, with frozen learning rate, step count, gradient clipping, and finite-loss veto checks before any diagnostic. | If this cannot be unit-tested without fake success claims, P73-B must be reported as `P73_B_OPTIMIZER_BLOCKED`, and Phase 5 must not run it. |
| Guard and audit residual gates | P72 residual gate currently script-local: `scripts/p72_support_certified_lower_gate_diagnostic.py:271-302` | Either keep residual gates in the P73 diagnostic script with focused tests, or move a small public helper to `source_route.py` if tests require subpackage access. | The Phase 4 subplan must avoid broad refactors. |
| Line probes and line gates | `p72_guard_line_points` and `p72_line_probe_diagnostics`: `source_route.py:3893-4016` | Reuse P72 line thresholds and diagnostics for P73 guard-line and audit-line channels; record line role in P73 provenance. | Existing P72 line construction is center-to-endpoint style.  Phase 4 must record this as inherited P72 line construction, not as a new nearest-fit theorem. |
| Support diagnostics | `p72_support_clipping_coverage`: `source_route.py:3785-3890` | Reuse for \(F_1,G_1,A_1\), guard-line, and audit-line cloud summaries. | Support warnings remain warnings unless Phase 2 says they block. |
| Normalizer gates | `p72_full_normalizer_gate`: `source_route.py:4018-4085`; script normalizer terms in `scripts/...:305-350` | Reuse P72 normalizer gate and `SquaredTTDensity` normalizer terms. | P73 must preserve the normalizer floor and fit-mass thresholds; no post-output loosening. |
| Condition/effective-rank gates | `p72_condition_effective_rank_gate`: `source_route.py:4087-4138`; script condition records in `scripts/...:556-589` | Reuse P72 gate; P73 script may keep condition-record extraction local unless tests require public access. | Do not lower the bar from `1e10`; low-level `1e14` remains a solver reference only. |
| Rank activity | Private `_p70_channel_activity_diagnostics`: `source_route.py:4460-4519` | Phase 4 may call the existing private helper from the diagnostic script as P72 does, or add a narrow public wrapper if tests require it. | No rank promotion; rank activity is a gate only. |
| Diagnostic JSON schema | P72 base/smoke/phase5 payloads in `scripts/p72_support_certified_lower_gate_diagnostic.py:149-217`, `945-1415` | Add `scripts/p73_density_aware_renewal_diagnostic.py` with schema/smoke support in Phase 4 only if it is not run as Phase 5 evidence. | Phase 4 tests may check schema/smoke helpers; Phase 5 must own the real bounded diagnostic. |
| Focused tests | P72 tests in `tests/highdim/test_p72_support_certified_lower_gate.py` | Add `tests/highdim/test_p73_density_aware_renewal.py`. | Tests must check semantics, not claim lower-gate repair. |

## P73-B Nonlinear Objective Warning

The P73-B objective is

```text
L_B(theta) = L_A(theta) + lambda_ce * L_ce(theta),
L_ce(theta) = - sum_j alpha_j log q_theta(z_j).
```

Since \(q_\theta(z)\) contains \(h_\theta(z)^2\) and \(Z_\theta\), this term is
nonlinear in the TT cores.  The current `FixedTTFitter` solves weighted
square-root ridge least-squares subproblems; it does not optimize this
cross-entropy term.  Therefore Phase 4 is forbidden from implementing P73-B
by silently reweighting the square-root regression and calling it
cross-entropy fitting.

The safe Phase 4 path is:

1. implement P73-A first;
2. implement and test a P73-B objective evaluator;
3. implement a bounded opt-in TensorFlow refinement only if the optimizer
   hyperparameters and finite-loss checks are frozen before diagnostics;
4. otherwise emit `P73_B_OPTIMIZER_BLOCKED` and do not run P73-B in Phase 5.

This is an implementation-surface gap, not a mathematical rejection of the
P73-B idea.

## Focused Test Plan

Phase 4 tests should include at least:

| Test area | Required assertion |
| --- | --- |
| Policy constants | P73 policy exposes `DENSITY_AWARE_OBJECTIVE_STATUS`, `lambda_ce = 0.1`, `R = 1`, inherited P72 thresholds, no rank promotion, and nonclaims. |
| Renewal-role manifest | Each point role records round and source-channel fields; malformed or missing role fields fail closed. |
| Audit exclusion | `NO_AUDIT_COEFFICIENT_SELECTION` passes on clean \(F_1\) and fails if audit or audit-line point ids/hashes enter training. |
| Training batch | P73 training batch is built from \(F_1\) only; fresh \(G_1\) and \(A_1\) are not concatenated into coefficient data. |
| Enrichment boundary | \(E_0\) may contain guard or guard-line points, and must reject audit or audit-line points. |
| Density-aware loss | Cross-entropy evaluator uses `SquaredTTDensity.log_density`, finite `lambda_ce`, finite positive weights, no audit inputs, and fail-closed behavior on normalizer exceptions. |
| P73-B optimizer | If implemented, the opt-in optimizer records frozen learning rate, step count, gradient clip, initial P73-A branch hash, final branch hash, finite-loss status, and nonclaims; if not implemented, tests assert the blocked status. |
| Normalizer and condition gates | P73 summaries reuse P72 normalizer and condition/effective-rank thresholds without loosening. |
| Line gates | Guard-line and audit-line gates are separated by role; round-0 guard-line failures are enrichment-only, while round-1 guard-line and audit-line failures block. |
| Schema | P73 diagnostic schema records P73-A/P73-B arm statuses, renewal provenance, no-audit predicate, and `phase5_diagnostic_executed = false` for Phase 4 schema/smoke tests. |

## Diagnostic Artifact Schema Plan

The future P73 diagnostic JSON should contain:

- `status`;
- `diagnostic_scope`;
- `source_route_controls`;
- `p73_policy`;
- `rows`;
- per-row `arms` with keys `p73_a_renewal_only` and
  `p73_b_density_aware_optin`;
- per-arm `renewal_rounds`;
- per-round cloud hashes for \(F_r,G_r,A_r,L_r,E_r,N_r\);
- `no_audit_coefficient_selection`;
- `training_batch_manifest`;
- `density_object_manifest`;
- `density_aware_objective`;
- residual, support, line, normalizer, condition/effective-rank, and
  rank-activity gates;
- `gate_summary`;
- `nonclaims`;
- run manifest with command, CPU/GPU choice, git state, random seeds, wall
  time, and artifact paths.

Phase 4 may create schema/smoke artifacts for unit tests.  Those artifacts
must state `phase5_diagnostic_executed = false` and
`smoke_only_not_phase5_evidence = true`.

## Phase 4 Handoff

Phase 4 may implement only the reviewed surfaces listed above.  It must:

- implement P73-A renewal-only as the mandatory first implementation target;
- keep P73-B opt-in and non-default;
- not run the real Phase 5 diagnostic;
- not validate, run HMC, scale, or promote rank;
- use TensorFlow / TensorFlow Probability for BayesFilter-owned algorithmic
  implementation;
- preserve every Phase 2 threshold and every Phase 1 classification boundary;
- stop if P73-B cannot be implemented without faking the nonlinear objective.

Required next artifact:

- `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md`.
