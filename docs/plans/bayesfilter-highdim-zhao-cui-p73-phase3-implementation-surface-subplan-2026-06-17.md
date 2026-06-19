# P73 Phase 3 Subplan: Implementation Surface Audit And Focused Test Plan

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE3_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Map the reviewed Phase 2 mathematical contract to the current code and test
surface before implementation.  Phase 3 must identify exact files, functions,
new helper boundaries, focused tests, artifact schemas, and risk controls for
P73-A renewal-only fitting and the P73-B density-aware opt-in diagnostic arm.

This is an audit and planning phase only.  It must not edit implementation
code.

## Entry Conditions Inherited From Phase 2

Phase 3 may begin only if:

- the Phase 2 design result exists;
- Phase 2 local checks pass;
- Claude returns `VERDICT: AGREE` on the Phase 2 result and this Phase 3
  subplan;
- Phase 2 freezes \(F_r,G_r,A_r,L_r\), \(q_\theta\), \(Z_\theta\),
  `lambda_ce`, all inherited P72 gates, and the
  `NO_AUDIT_COEFFICIENT_SELECTION` predicate;
- Phase 2 classifies renewal, cross-entropy, audit exclusion, and P73 gates as
  `extension_or_invention` unless a stricter source anchor is explicitly
  recorded;
- continuation is covered by the reviewed visible runbook unless a
  human-required boundary appears.

## Required Artifacts

Phase 3 must produce:

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-result-2026-06-17.md`;
- implementation-surface map for the reviewed Phase 2 contract;
- focused test plan for P73-A and P73-B;
- artifact/schema plan for P73 diagnostic JSON output;
- Phase 4 opt-in implementation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md`;
- updated execution and review ledgers.

Candidate surfaces to inspect include:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/fitting.py`;
- `bayesfilter/highdim/squared_tt.py`;
- `bayesfilter/highdim/transport.py`;
- `bayesfilter/highdim/__init__.py`;
- `scripts/p72_support_certified_lower_gate_diagnostic.py`;
- `tests/highdim/test_p72_support_certified_lower_gate.py`;
- a possible new test file
  `tests/highdim/test_p73_density_aware_renewal.py`;
- a possible new diagnostic script
  `scripts/p73_density_aware_renewal_diagnostic.py`.

## Required Checks/Tests/Reviews

Read-only local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md
rg -n "DENSITY_AWARE_OBJECTIVE_STATUS|NO_AUDIT_COEFFICIENT_SELECTION|lambda_ce|F_r|G_r|A_r|L_r|q_\\\\theta|Z_\\\\theta" docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md
rg -n "p72_|support_certified|guard|audit|line|normalizer|condition|effective_rank|rank_activity|training_batch" bayesfilter/highdim/source_route.py bayesfilter/highdim/fitting.py scripts/p72_support_certified_lower_gate_diagnostic.py tests/highdim/test_p72_support_certified_lower_gate.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md
```

Reviews:

- Claude read-only review of the Phase 3 result and Phase 4 subplan;
- MathDevMCP may be used only for bounded document/math checks if Phase 3
  introduces a labeled derivation or proof obligation;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Which exact current code and test surfaces can implement the Phase 2 P73 contract without changing default policy or violating source-governance boundaries? |
| Exact baseline/comparator | Phase 2 design result and P72 Phase 5 blocked diagnostic. |
| Primary pass/fail criterion | Phase 3 maps every Phase 2 required operation to an implementation/test surface or records a blocker before code edits. |
| Veto diagnostics | Missing surface for audit exclusion; missing surface for renewed support provenance; density-aware objective mapped as default policy; NumPy chosen for BayesFilter-owned differentiable implementation; source-faithfulness overclaim; implementation edits launched in Phase 3. |
| Explanatory only | Rough implementation size, runtime estimates, possible refactor candidates, optional future rank/degree work. |
| What will not be concluded | No implementation correctness, no diagnostic pass, no validation, no HMC readiness, no scaling, no rank promotion. |
| Artifact preserving result | Phase 3 result, Phase 4 subplan, execution/review ledgers. |

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 3.
- Do not create or run the P73 diagnostic script in Phase 3.
- Do not run Python diagnostics, validation, HMC, scaling, GPU, or rank
  promotion.
- Do not change Phase 2 thresholds.
- Do not make P73-B the default path.
- Do not claim source-faithfulness for renewal sets, density-aware
  cross-entropy, audit exclusion, or P73 gate thresholds.
- Do not certify on points just added to training.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 result exists and maps every Phase 2 operation to code/test surfaces
  or an explicit blocker;
- Phase 4 subplan exists with objective, entry conditions, artifacts, checks,
  evidence contract, forbidden actions, handoff conditions, and stop
  conditions;
- the Phase 4 subplan preserves P73-A as mandatory and P73-B as opt-in;
- the Phase 4 subplan preserves TensorFlow / TensorFlow Probability as the
  BayesFilter algorithmic backend;
- local checks pass;
- Claude returns `VERDICT: AGREE`;
- continuation to Phase 4 is covered by the reviewed visible runbook unless a
  human-required boundary appears.

## Stop Conditions

Stop and write a blocker if:

- current code has no safe surface for renewed support provenance without a
  broader refactor;
- current code has no safe surface for `NO_AUDIT_COEFFICIENT_SELECTION`;
- the density-aware objective would require a default-policy change;
- implementing P73 would require using same-round audit points for coefficient
  selection;
- Phase 3 cannot produce a focused test plan that checks audit exclusion,
  provenance, normalizer, condition, and density-aware objective semantics;
- Claude and Codex do not converge after five rounds for the same blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This Phase 3 subplan passes the initial skeptical audit because it is
read-only with respect to implementation, consumes the reviewed Phase 2
contract as the source of truth, treats P72 as the comparator, and requires a
blocker rather than improvising implementation if a required surface is absent.
