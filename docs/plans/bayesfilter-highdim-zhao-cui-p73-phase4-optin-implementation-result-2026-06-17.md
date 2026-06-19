# P73 Phase 4 Result: Opt-In Implementation And Focused Tests

metadata_date: 2026-06-17
status: PHASE4_PASSED_CLAUDE_AGREE_READY_FOR_PHASE5
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Do the opt-in P73 implementation surfaces implement the Phase 2 design contract and Phase 3 surface map without changing default BayesFilter behavior? |
| Exact baseline/comparator | Phase 2 design result, Phase 3 surface map, and P72 Phase 5 blocked diagnostic. |
| Primary pass/fail criterion | Focused tests pass for P73 policy, provenance, audit exclusion, renewal training, density-aware objective handling, inherited gates, and schema; implementation emits no lower-gate success claim. |
| Veto diagnostics | No P73-B least-squares fake was added; audit points are rejected from coefficient data; P73-B is not default; thresholds are unchanged; no Phase 5 diagnostic, validation, HMC, scaling, GPU, or rank-promotion run was launched. |
| Explanatory only | Toy cross-entropy values, schema smoke payload, code size, unit-test runtime. |
| What is not concluded | No lower-gate repair, no P73 diagnostic pass, no validation, no HMC readiness, no scaling, no rank promotion, no adaptive Zhao--Cui parity. |
| Artifact preserving result | This result, implementation diffs, focused test output, Phase 5 subplan, execution and review ledgers. |

## Skeptical Plan Audit

Phase 4 passed its skeptical audit before implementation.  The phase was
bounded to opt-in code surfaces and focused unit tests, with no diagnostic
execution.  The main proxy-risk was that a training-support objective value
could be mistaken for lower-gate evidence.  The implementation avoids that
risk by exposing cross-entropy evaluation only and by marking the P73-B
optimizer as blocked.

## Implementation Summary

Implemented P73-specific surfaces in:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/__init__.py`;
- `scripts/p73_density_aware_renewal_diagnostic.py`;
- `tests/highdim/test_p73_density_aware_renewal.py`.

No implementation edit was made to `bayesfilter/highdim/fitting.py`.

The implemented surfaces are:

- P73 statuses and constants, including `P73_RENEWAL_COUNT = 1`,
  `P73_LAMBDA_CE = 0.1`,
  `P73_DENSITY_AWARE_OBJECTIVE_STATUS =
  included_as_opt_in_diagnostic_arm`, and `P73_B_OPTIMIZER_BLOCKED`;
- `p73_density_aware_renewal_policy()`;
- `p73_renewal_role_record(...)`;
- `p73_no_audit_coefficient_selection(...)`;
- `p73_training_batch_from_renewed_fit(...)`, which builds coefficient data
  from \(F_1\) only and accepts same-round audit/audit-line records and hashes
  for overlap checks;
- `p73_validate_enrichment_boundary(...)`, which permits guard and guard-line
  enrichment only;
- `p73_density_aware_cross_entropy(...)`, which evaluates the opt-in
  empirical cross-entropy term using `SquaredTTDensity.log_density` and the
  same audit-overlap predicate;
- `p73_density_aware_optimizer_status()`, which reports P73-B as not runnable
  for Phase 5.

The diagnostic script is schema/smoke only.  It records
`phase5_diagnostic_executed = False` and
`smoke_only_not_phase5_evidence = True`.

## P73-B Status

P73-B is not implemented as an optimizer in Phase 4.

The code can evaluate

```text
L_ce(theta; r) = - sum_j alpha_j log q_theta(z_j)
```

on the renewed fit support, with the Phase 2 weight rule and
`lambda_ce = 0.1`.  It does not optimize

```text
L_A(theta; r) + lambda_ce * L_ce(theta; r).
```

Therefore P73-B remains:

```text
P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED
```

Phase 5 may run P73-A only unless a later reviewed phase implements a real
TensorFlow nonlinear refinement and updates this status before any diagnostic
outputs are seen.

## Local Checks

The Phase 4 local checks passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p73_density_aware_renewal_diagnostic.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p73_density_aware_renewal.py
```

Result: 13 passed, 2 TensorFlow Probability deprecation warnings.

```text
rg -n "P73_DENSITY_AWARE_OBJECTIVE_STATUS|P73_LAMBDA_CE|NO_AUDIT_COEFFICIENT_SELECTION|P73_B_OPTIMIZER_BLOCKED|included_as_opt_in_diagnostic_arm|phase5_diagnostic_executed.*False|smoke_only_not_phase5_evidence.*True" bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p73_density_aware_renewal_diagnostic.py tests/highdim/test_p73_density_aware_renewal.py
```

Result: required tokens found in code, exports, script, and tests.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py bayesfilter/highdim/fitting.py scripts/p73_density_aware_renewal_diagnostic.py tests/highdim/test_p73_density_aware_renewal.py docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md
```

Result: passed.

## Boundary Checks

- Default BayesFilter behavior was not changed.
- No Phase 5 bounded diagnostic was run.
- No validation ladder, HMC, scaling, GPU, or rank-promotion command was run.
- No threshold was changed.
- No source-faithfulness claim was made for renewal, audit exclusion,
  cross-entropy, or P73 gates.
- The code rejects audit and audit-line records in coefficient selection.
- The code rejects audit-derived enrichment.

## Handoff To Phase 5

Phase 5 may begin after Claude review agrees with this result and the Phase 5
subplan.

The Phase 5 entry conditions produced by Phase 4 are:

- P73-A implementation surfaces exist and focused tests pass;
- P73-B is explicitly blocked and is not runnable in Phase 5;
- schema/smoke script records Phase 4 non-evidence sentinels;
- Phase 5 subplan freezes CPU-only execution, P73-A-only arm status, row
  labels, pass/block criteria, and forbidden downstream claims.
