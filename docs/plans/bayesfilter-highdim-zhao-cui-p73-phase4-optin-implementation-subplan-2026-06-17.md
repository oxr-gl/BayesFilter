# P73 Phase 4 Subplan: Opt-In Implementation And Focused Tests

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE4_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the reviewed P73 opt-in surfaces and focused tests without changing
default BayesFilter behavior.  P73-A renewal-only fitting is mandatory.
P73-B density-aware fitting is opt-in and may proceed only through an explicit
TensorFlow objective/refinement surface; it must not be faked by reweighting
least-squares regression.

## Entry Conditions Inherited From Phase 3

Phase 4 may begin only if:

- Phase 3 result exists and maps every Phase 2 operation to a code/test
  surface or an explicit implementation gap;
- Phase 4 subplan has passed local checks and Claude review;
- Phase 3 records that P73-A is mandatory and P73-B is opt-in;
- Phase 3 records the nonlinear objective warning for P73-B;
- continuation is covered by the reviewed visible runbook unless a
  human-required boundary appears.

## Required Artifacts

Phase 4 must produce:

- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md`;
- implementation edits, if approved, limited to reviewed surfaces such as:
  - `bayesfilter/highdim/source_route.py`;
  - `bayesfilter/highdim/__init__.py`;
  - possibly `bayesfilter/highdim/fitting.py` only for a narrow public helper
    if the existing private scaled-ridge diagnostics cannot support tests;
  - `scripts/p73_density_aware_renewal_diagnostic.py`;
  - `tests/highdim/test_p73_density_aware_renewal.py`;
- Phase 5 bounded-renewal diagnostic subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md`;
- updated execution and review ledgers.

## Required Implementation Tasks

1. Add P73 policy constants and statuses:
   - P73 pass/block/warn statuses;
   - `P73_RENEWAL_COUNT = 1`;
   - `P73_LAMBDA_CE = 0.1`;
   - `P73_DENSITY_AWARE_OBJECTIVE_STATUS = included_as_opt_in_diagnostic_arm`;
   - inherited P72 thresholds without loosening.
2. Add `p73_density_aware_renewal_policy()` with nonclaims and Phase 1
   classification boundaries.
3. Add renewal-role provenance helpers for \(F_r,G_r,A_r,L_r,E_r,N_r\).
4. Add `NO_AUDIT_COEFFICIENT_SELECTION` helper semantics under a P73-named
   public function.
5. Add a P73 training-batch helper that builds coefficient data from \(F_1\)
   only.
6. Add enrichment-boundary validation: \(E_0\) may come from guard or
   guard-line channels only, never audit or audit-line channels.
7. Reuse P72 support, line, normalizer, condition/effective-rank, and
   rank-activity gates, recording P73 role semantics around them.
8. Add a P73-B cross-entropy objective evaluator using `SquaredTTDensity` and
   frozen `lambda_ce = 0.1`.
9. Either:
   - implement a bounded opt-in TensorFlow density-aware refinement initialized
     from P73-A, with frozen optimizer hyperparameters and finite-loss checks;
     or
   - emit `P73_B_OPTIMIZER_BLOCKED` and ensure Phase 5 cannot run P73-B.
10. Add a P73 diagnostic script with schema/smoke helpers only.  The real
    bounded diagnostic belongs to Phase 5.
11. Add focused tests for policy constants, provenance, audit exclusion,
    training-batch exclusion, enrichment boundary, cross-entropy evaluator,
    P73-B optimizer status, inherited gates, line-role semantics, and schema.

## Required Checks/Tests/Reviews

Local checks after implementation:

```bash
python -m py_compile scripts/p73_density_aware_renewal_diagnostic.py
python -m pytest tests/highdim/test_p73_density_aware_renewal.py
rg -n "P73_DENSITY_AWARE_OBJECTIVE_STATUS|P73_LAMBDA_CE|NO_AUDIT_COEFFICIENT_SELECTION|P73_B_OPTIMIZER_BLOCKED|included_as_opt_in_diagnostic_arm|phase5_diagnostic_executed.*False|smoke_only_not_phase5_evidence.*True" bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p73_density_aware_renewal_diagnostic.py tests/highdim/test_p73_density_aware_renewal.py
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py bayesfilter/highdim/fitting.py scripts/p73_density_aware_renewal_diagnostic.py tests/highdim/test_p73_density_aware_renewal.py docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md
```

Review:

- Claude read-only review of implementation diffs, test results, Phase 4
  result, and Phase 5 subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Do the opt-in P73 implementation surfaces faithfully implement the Phase 2 design contract and Phase 3 surface map without changing default policy? |
| Exact baseline/comparator | Phase 2 design result, Phase 3 surface map, and P72 Phase 5 blocked diagnostic. |
| Primary pass/fail criterion | Focused tests pass for P73 policy, provenance, audit exclusion, renewal training, density-aware objective handling, inherited gates, and schema; implementation emits no lower-gate success claim. |
| Veto diagnostics | P73-B faked through least-squares reweighting; audit points allowed into coefficient data; P73-B made default; thresholds changed; NumPy used in differentiable implementation; Phase 5 real diagnostic launched; validation/HMC/scaling/rank promotion launched. |
| Explanatory only | Unit-test runtime, schema smoke payload, objective values on toy fixtures, code size. |
| What will not be concluded | No lower-gate repair, no P73 diagnostic pass, no validation, no HMC readiness, no scaling, no rank promotion, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 4 result, test output, implementation diffs, Phase 5 subplan, execution/review ledgers. |

## Forbidden Claims/Actions

- Do not run the real Phase 5 bounded diagnostic.
- Do not run validation, HMC, scaling, GPU, or rank-promotion experiments.
- Do not loosen P72/P73 thresholds.
- Do not make P73-B a default path.
- Do not call renewal, cross-entropy, audit-exclusion, or P73 gates
  source-faithful.
- Do not use same-round audit points for coefficient selection.
- Do not certify on points just added to training.
- Do not implement P73-B by pretending the least-squares ALS objective solves
  the nonlinear cross-entropy term.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 result exists;
- local checks pass;
- Claude returns `VERDICT: AGREE`;
- Phase 5 subplan exists and freezes exact commands, CPU/GPU choice, row
  labels, arm labels, seeds, artifact paths, and pass/block criteria;
- Phase 5 subplan explicitly says whether P73-B is runnable or blocked by
  `P73_B_OPTIMIZER_BLOCKED`;
- continuation to Phase 5 is covered by the reviewed visible runbook unless a
  human-required boundary appears.

## Stop Conditions

Stop and write a blocker if:

- P73-A cannot be implemented without using round-1 guard or audit points for
  coefficient selection;
- P73 renewal provenance cannot prove `NO_AUDIT_COEFFICIENT_SELECTION`;
- P73-B cannot be implemented honestly and the blocked status cannot be
  represented safely;
- focused tests require a broad refactor outside reviewed surfaces;
- implementation changes would alter default BayesFilter behavior;
- Claude and Codex do not converge after five rounds for the same blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it limits Phase 4 to
opt-in implementation and focused tests, requires P73-A first, names the
P73-B nonlinear-objective risk explicitly, preserves TensorFlow as the
implementation backend, and forbids the real bounded diagnostic until Phase 5.
