# Phase P5 Subplan: Family-By-Family Admission Refresh

metadata_date: 2026-06-23
status: DRAFT_PENDING_P4_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P5
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Refresh the family-by-family SGQF admission ledger after the P4 KSC wrapper-score
certification so that the literature-backed family roster now distinguishes:
- rows that remain blocked,
- rows that are value-admitted only,
- and rows that are analytical-score-admitted within a declared scope.

P5 is a governance refresh phase.  It does not yet touch machine-readable
benchmark matrices; that remains later work.

## Entry Conditions Inherited From Previous Phase

- P4 result status is
  `PASS_P4_FIXED_SGQF_KSC_ANALYTICAL_WRAPPER_SCORE_CERTIFIED` or a reviewed
  equivalent pass token.
- P4 preserved autodiff as diagnostic-only.
- P4 scoped KSC wrapper-score admission to the declared tiny same-target
  surrogate fixture.
- The visible execution ledger and visible stop handoff were updated through P4.
- Any P4 bounded-review findings were patched and the P4 packet rechecked.

## Required Artifacts

- Phase P5 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-result-2026-06-23.md`
- Refreshed Phase P6 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-subplan-2026-06-23.md`
- Visible execution ledger entry
- Review-ledger entry
- Visible stop handoff update

## Required Checks, Tests, And Reviews

Local checks:
```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-subplan-2026-06-23.md
rg -n "admit_analytical_score|admit_value_baseline_only|blocked_not_same_target|blocked_missing_analytical_wrapper_score|tiny same-target surrogate fixture|diagnostic-only" docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-result-2026-06-23.md
```

Required review:
- bounded read-only review on the exact P5 packet after the P5 result and P6
  subplan are written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After P4, how should the SGQF family-by-family admission ledger change, especially for the KSC surrogate row? |
| Baseline/comparator | The prior P1 admission ledger and the P4 wrapper-score certification result. |
| Primary pass criterion | The P5 result updates the family ledger so the KSC surrogate row moves from score-blocked to analytical-score-admitted within its declared tiny same-target surrogate scope, while all other families remain honestly classified. |
| Veto diagnostics | Silent promotion beyond the declared KSC scope, autodiff promotion, hidden blocker removal, or family reclassification without evidence. |
| Explanatory diagnostics | changed family statuses, unchanged blocked families, scope qualifiers, review verdict. |
| Not concluded | No machine-readable matrix integration yet, no broad family-score expansion beyond KSC, no actual-SV or HMC claim. |
| Artifact preserving result | P5 result, visible execution ledger, review ledger, visible stop handoff, refreshed P6 subplan. |

## Forbidden Claims And Actions

- Do not expand KSC analytical-score admission beyond the declared tiny surrogate
  fixture.
- Do not alter blocked-family statuses without new evidence.
- Do not update machine-readable benchmark matrices in P5.
- Do not imply benchmark-wide score readiness from one family-row change.

## Exact Next-Phase Handoff Conditions

Advance to P6 only if:
- the P5 result is written with explicit updated family statuses,
- KSC score admission is scope-qualified correctly,
- blocked families remain explicit,
- P6 subplan exists,
- bounded review agrees or is repaired within the P5 loop.

## Stop Conditions

Stop if the KSC scope cannot be stated precisely, if blocked families would need
silent reinterpretation, or if review finds an unpatchable boundary leak.

## End-Of-Phase Protocol

1. Run focused local checks.
2. Write the P5 result.
3. Draft/refresh the P6 subplan.
4. Update ledgers/handoff.
5. Run bounded review.
6. Patch and rerun if needed.
7. Advance only if handoff conditions hold.
