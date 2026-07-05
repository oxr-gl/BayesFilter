# Phase P6 Subplan: Deterministic Matrix Integration

metadata_date: 2026-06-23
status: DRAFT_PENDING_P5_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P6
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Propagate the refreshed SGQF family ledger into the machine-readable
deterministic benchmark-governance artifacts so that admitted, blocked,
diagnostic-only, and scope-qualified SGQF cells are represented with no silent
holes.

P6 is the first phase allowed to update machine-readable benchmark-governance
artifacts. It must carry the KSC tiny-scope analytical-score qualifier forward
exactly and must not widen it.

## Entry Conditions Inherited From Previous Phase

- P5 result status is
  `PASS_P5_FIXED_SGQF_FAMILY_ADMISSION_LEDGER_UPDATED` or a reviewed equivalent
  pass token.
- P5 refreshed the KSC row from score-blocked to analytical-score-admitted only
  within the declared tiny same-target surrogate fixture scope.
- All other blocked-family statuses remained explicit.
- The visible execution ledger and visible stop handoff were updated through P5.
- Any P5 bounded-review findings were patched and the P5 packet rechecked.

## Required Artifacts

- Phase P6 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-result-2026-06-23.md`
- Refreshed Phase P7 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p7-preflight-and-smoke-subplan-2026-06-23.md`
- Visible execution ledger entry
- Review-ledger entry
- Visible stop handoff update

## Required Checks, Tests, And Reviews

Local checks:
```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p7-preflight-and-smoke-subplan-2026-06-23.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json
```

Required review:
- bounded read-only review on the exact P6 packet after the P6 result and P7
  subplan are written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the machine-readable deterministic SGQF cells be refreshed so they match the family ledger exactly, especially the KSC tiny-scope analytical-score admission? |
| Baseline/comparator | The P5 family ledger, target registry, deterministic coverage artifact, and source-paper scope contract. |
| Primary pass criterion | P6 updates the machine-readable deterministic SGQF cells so they match the P5 family ledger with no silent holes and no widening of the KSC tiny-scope qualifier. |
| Veto diagnostics | silent SGQF holes, widened KSC score scope, hidden blocked families, inconsistent status words between prose and machine-readable artifacts. |
| Explanatory diagnostics | changed cell count, scope-qualifier propagation, unchanged blocked cells, review verdict. |
| Not concluded | No numeric benchmark run yet, no preflight result yet, no broader family-score expansion beyond KSC. |
| Artifact preserving result | P6 result, updated machine-readable artifacts, visible execution ledger, review ledger, visible stop handoff, refreshed P7 subplan. |

## Forbidden Claims And Actions

- Do not widen the KSC analytical-score admission beyond the declared tiny
  surrogate fixture.
- Do not silently change blocked-family statuses.
- Do not run numeric benchmark ladders in P6.
- Do not infer benchmark performance from registry/coverage integration alone.

## Exact Next-Phase Handoff Conditions

Advance to P7 only if:
- the machine-readable SGQF cells match the refreshed P5 family ledger,
- the KSC tiny-scope qualifier is preserved explicitly,
- no blocked families disappear,
- P7 subplan exists,
- bounded review agrees or is repaired within the P6 loop.

## Stop Conditions

Stop if the machine-readable artifacts cannot express the P5 family distinctions
cleanly, if the KSC scope cannot be preserved exactly, or if review finds an
unpatchable governance inconsistency.

## End-Of-Phase Protocol

1. Run focused local checks.
2. Write the P6 result.
3. Draft/refresh the P7 subplan.
4. Update ledgers/handoff.
5. Run bounded review.
6. Patch and rerun if needed.
7. Advance only if handoff conditions hold.
